"""Supabase Auth hooks — HTTP hook endpoints called by Supabase during auth flows."""

import base64
import hashlib
import hmac
import json
import logging
import time

import httpx
from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/hooks", tags=["hooks"])

TEXT_LK_SEND_URL = "https://app.text.lk/api/v3/sms/send"

_WEBHOOK_TIMESTAMP_TOLERANCE_SECS = 300  # 5 minutes


def _verify_standard_webhook(body: bytes, request: Request) -> bool:
    """Verify a Supabase HTTP hook request using the Standard Webhooks spec.

    Supabase signs hook requests with three headers:
      webhook-id, webhook-timestamp, webhook-signature

    The secret from the Supabase dashboard has the form "v1,whsec_<base64>".
    Strip the prefix, base64-decode to get raw key bytes, then verify:
      HMAC-SHA256("<webhook-id>.<webhook-timestamp>.<body>") == signature
    """
    secret = settings.supabase_hook_secret
    if not secret:
        if settings.is_production:
            logger.error("supabase_hook_secret not set in production — rejecting hook call")
            return False
        logger.warning("supabase_hook_secret not set — skipping verification (dev only)")
        return True

    # Strip the "v1,whsec_" prefix Supabase prepends to the secret
    if secret.startswith("v1,whsec_"):
        secret = secret[len("v1,whsec_"):]
    try:
        secret_bytes = base64.b64decode(secret)
    except Exception:
        logger.error("supabase_hook_secret is not valid base64 after stripping prefix")
        return False

    webhook_id        = request.headers.get("webhook-id")
    webhook_timestamp = request.headers.get("webhook-timestamp")
    webhook_signature = request.headers.get("webhook-signature")

    if not webhook_id or not webhook_timestamp or not webhook_signature:
        logger.warning("Missing Standard Webhooks headers on hook request")
        return False

    # Reject requests outside the timestamp tolerance window
    try:
        ts = int(webhook_timestamp)
        if abs(time.time() - ts) > _WEBHOOK_TIMESTAMP_TOLERANCE_SECS:
            logger.warning("Hook request timestamp out of tolerance: %s", webhook_timestamp)
            return False
    except ValueError:
        return False

    # Build the signed content: "<id>.<timestamp>.<raw-body>"
    signed_content = f"{webhook_id}.{webhook_timestamp}.{body.decode()}".encode()

    computed_sig = base64.b64encode(
        hmac.new(secret_bytes, signed_content, hashlib.sha256).digest()
    ).decode()

    # Header may contain multiple space-separated "v1,<base64-sig>" entries
    incoming_sigs = [
        part.split(",", 1)[-1]
        for part in webhook_signature.split(" ")
        if "," in part
    ]
    return any(hmac.compare_digest(computed_sig, sig) for sig in incoming_sigs)


def _e164_to_local(phone: str) -> str:
    """Strip leading '+' so text.lk receives '94724999547' not '+94724999547'."""
    return phone.lstrip("+")


@router.post("/send-sms", status_code=200)
async def send_sms_hook(request: Request) -> dict:
    """Supabase Send SMS hook — delivers OTPs via text.lk.

    Supabase calls this endpoint instead of Twilio when phone OTP is requested.
    Verifies the request signature, then forwards the OTP to the recipient via text.lk.
    Returns an empty 200 on success; any non-2xx causes Supabase to surface an error.
    """
    body_bytes = await request.body()

    if not _verify_standard_webhook(body_bytes, request):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = json.loads(body_bytes)
        phone = payload["user"]["phone"]
        otp   = payload["sms"]["otp"]
    except (KeyError, json.JSONDecodeError) as exc:
        logger.error("Malformed hook payload: %s", exc)
        raise HTTPException(status_code=400, detail="Malformed hook payload") from exc

    if not settings.text_lk_api_key:
        logger.error("text_lk_api_key not configured — cannot send OTP")
        raise HTTPException(status_code=500, detail="SMS provider not configured")

    message = f"Your KingGuru verification code is {otp}. Valid for 10 minutes. Do not share this code."

    async with httpx.AsyncClient(timeout=4.0) as client:
        try:
            response = await client.post(
                TEXT_LK_SEND_URL,
                headers={
                    "Authorization": f"Bearer {settings.text_lk_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "recipient": _e164_to_local(phone),
                    "sender_id": settings.text_lk_sender_id,
                    "type": "plain",
                    "message": message,
                },
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "text.lk returned %s for %s: %s",
                exc.response.status_code,
                phone,
                exc.response.text,
            )
            raise HTTPException(status_code=502, detail="SMS delivery failed") from exc
        except httpx.RequestError as exc:
            logger.error("text.lk request error for %s: %s", phone, exc)
            raise HTTPException(status_code=502, detail="SMS provider unreachable") from exc

    result = response.json()
    if result.get("status") != "success":
        logger.error("text.lk non-success response for %s: %s", phone, result)
        raise HTTPException(status_code=502, detail="SMS delivery failed")

    logger.info("OTP sent via text.lk to %s", phone)
    return {}
