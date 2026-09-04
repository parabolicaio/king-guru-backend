"""OnePay REST API client (https://docs.onepay.lk/api-documentation).

Two calls: create a checkout link (POST /v3/checkout/link/) and verify a
transaction's status (GET /v3/transaction/status/). Every create-checkout
request is signed with SHA256(app_id + currency + amount + HASH_SALT) —
plain string concatenation, no separators, per OnePay's docs. Hash Salt
never leaves this process: it's read from settings (server-side env) and
used only to compute the hash, never sent or logged.

Per OnePay's own guidance, a redirect back to our site is NOT proof of
payment on its own — callers must always confirm via get_transaction_status
before granting anything. See payment_service.py.
"""

import hashlib
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(15.0)


class OnePayError(Exception):
    """Raised on any non-success response from OnePay, or a network failure."""


def _headers() -> dict[str, str]:
    # OnePay expects the App Token RAW in the Authorization header, with NO
    # "Bearer " prefix. Sending "Bearer <token>" makes OnePay read the literal
    # string "Bearer <token>" as the token, which it rejects as
    # "Invalid app credentials" (a 400 that looks like a hash/credential
    # problem but is really a malformed auth header). Confirmed against a
    # standalone request that succeeds with the bare token.
    return {"Authorization": settings.onepay_app_token}


def _format_amount(amount: float | str) -> str:
    """OnePay requires the hash's amount component to match the request
    body's amount string exactly — always format as a fixed 2-decimal string."""
    return f"{float(amount):.2f}"


def _compute_hash(currency: str, amount: float | str) -> str:
    raw = f"{settings.onepay_app_id}{currency}{_format_amount(amount)}{settings.onepay_hash_salt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def create_checkout_link(
    *,
    reference: str,
    amount: float | str,
    currency: str,
    customer_first_name: str,
    customer_last_name: str,
    customer_phone_number: str,
    customer_email: str,
    redirect_url: str,
) -> dict:
    """Creates a OnePay checkout session. Returns OnePay's response `data`
    dict (contains redirect_url and ipg_transaction_id among other fields).
    Raises OnePayError on failure.
    """
    body = {
        "app_id": settings.onepay_app_id,
        "hash": _compute_hash(currency, amount),
        "amount": _format_amount(amount),
        "currency": currency,
        "reference": reference,
        "customer_first_name": customer_first_name,
        "customer_last_name": customer_last_name,
        "customer_phone_number": customer_phone_number,
        "customer_email": customer_email,
        "transaction_redirect_url": redirect_url,
    }
    url = f"{settings.onepay_base_url}/v3/checkout/link/"
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=body, headers=_headers())
    except httpx.HTTPError as e:
        logger.exception("OnePay create-checkout request failed: reference=%s", reference)
        raise OnePayError(f"OnePay request failed: {e}") from e

    if resp.status_code != 200:
        logger.warning(
            "OnePay create-checkout returned %s for reference=%s: %s",
            resp.status_code, reference, resp.text,
        )
        raise OnePayError(f"OnePay returned {resp.status_code}: {resp.text}")

    data = resp.json()
    return data.get("data", data)


async def get_transaction_status(onepay_transaction_id: str) -> dict:
    """Fetches the current status of a transaction from OnePay. Raises
    OnePayError on failure. Always call this to confirm a payment — never
    trust the customer's redirect-back URL or an unverified webhook body
    on their own.
    """
    url = f"{settings.onepay_base_url}/v3/transaction/status/"
    body = {
        "app_id": settings.onepay_app_id,
        "onepay_transaction_id": onepay_transaction_id,
    }
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json=body, headers=_headers())
    except httpx.HTTPError as e:
        logger.exception(
            "OnePay status check request failed: onepay_transaction_id=%s", onepay_transaction_id,
        )
        raise OnePayError(f"OnePay request failed: {e}") from e

    if resp.status_code != 200:
        logger.warning(
            "OnePay status check returned %s for onepay_transaction_id=%s: %s",
            resp.status_code, onepay_transaction_id, resp.text,
        )
        raise OnePayError(f"OnePay returned {resp.status_code}: {resp.text}")

    data = resp.json()
    return data.get("data", data)