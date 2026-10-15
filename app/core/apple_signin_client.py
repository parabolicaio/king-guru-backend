"""Sign in with Apple — server-side token exchange and revocation
(https://developer.apple.com/documentation/sign_in_with_apple/generate_and_validate_tokens).

A SEPARATE concern from the native sign-in flow itself (Supabase
signInWithIdToken verifies the identityToken locally and never calls this
module). This client exists for exactly one reason: App Store Guideline
5.1.1(v) requires that deleting an account also disconnect it from the
user's Apple ID, and the only way to do that is to revoke the refresh token
Apple issues during sign-in — which means first exchanging the
authorization code the mobile app receives at sign-in for that refresh
token, then calling Apple's revoke endpoint for it at deletion time. Flow:

1. Mobile sign-in gets an `authorizationCode` from AuthorizationCredentialAppleID
   (one-shot — only usable once, expires in minutes) and POSTs it to our own
   /auth/apple/link endpoint.
2. exchange_code_for_tokens() trades that code for Apple's refresh_token at
   POST https://appleid.apple.com/auth/token. The refresh_token itself
   (unlike the code) doesn't expire until revoked — it's what gets stored.
3. At account-deletion time, revoke_token() calls
   POST https://appleid.apple.com/auth/revoke with that stored refresh_token.

Both endpoints authenticate with a client_secret that is NOT a static
credential — it's a short-lived JWT, signed ES256, that this module builds
fresh per call from the Team ID / Key ID / .p8 private key configured in
Settings. Every public function here no-ops with a logged warning when
those settings are empty, so sign-in and account deletion both keep working
before Nisal supplies the key — the same pattern onepay_customer_client.py
uses for its own not-yet-configured credential.
"""

import logging
import time

import httpx
import jwt

from app.core.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(15.0)
_TOKEN_URL = "https://appleid.apple.com/auth/token"
_REVOKE_URL = "https://appleid.apple.com/auth/revoke"
# Apple allows up to 6 months; there's no benefit to living that long since
# we build a fresh one per call, and a short lifetime limits the blast
# radius if one ever leaked in a log.
_CLIENT_SECRET_TTL_SECONDS = 5 * 60


class AppleSignInError(Exception):
    """Raised on any non-success response from Apple, or a network failure."""


def _is_configured() -> bool:
    return bool(
        settings.apple_signin_team_id
        and settings.apple_signin_key_id
        and settings.apple_signin_private_key
    )


def _build_client_secret() -> str:
    now = int(time.time())
    payload = {
        "iss": settings.apple_signin_team_id,
        "iat": now,
        "exp": now + _CLIENT_SECRET_TTL_SECONDS,
        "aud": "https://appleid.apple.com",
        "sub": settings.apple_signin_client_id,
    }
    return jwt.encode(
        payload,
        settings.apple_signin_private_key,
        algorithm="ES256",
        headers={"kid": settings.apple_signin_key_id},
    )


async def exchange_code_for_tokens(authorization_code: str) -> dict | None:
    """Exchange a one-shot authorization code for Apple's refresh_token (+ others).

    Returns the parsed JSON body (access_token, refresh_token, id_token,
    expires_in, token_type) on success, or None if Apple Sign-In isn't
    configured yet or the exchange fails — callers treat a None return as
    "couldn't link this time," never as a reason to block sign-in, since the
    code was already consumed by Supabase's own identityToken verification.
    """
    if not _is_configured():
        logger.warning(
            "Apple Sign-In not configured — skipping authorization_code exchange"
        )
        return None

    data = {
        "client_id": settings.apple_signin_client_id,
        "client_secret": _build_client_secret(),
        "code": authorization_code,
        "grant_type": "authorization_code",
    }
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(_TOKEN_URL, data=data)
    except httpx.HTTPError:
        logger.exception("Apple token exchange request failed")
        return None

    if resp.status_code != 200:
        logger.warning(
            "Apple token exchange returned %s: %s", resp.status_code, resp.text
        )
        return None

    return resp.json()


async def revoke_token(refresh_token: str) -> None:
    """Revoke a previously-issued Apple refresh_token.

    Called during account deletion. Swallows errors — like the Supabase
    admin calls in supabase_admin.py, the DB-level soft-delete has already
    happened and must not be rolled back if Apple's API is unreachable.
    """
    if not _is_configured():
        logger.warning("Apple Sign-In not configured — skipping token revocation")
        return

    data = {
        "client_id": settings.apple_signin_client_id,
        "client_secret": _build_client_secret(),
        "token": refresh_token,
        "token_type_hint": "refresh_token",
    }
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(_REVOKE_URL, data=data)
            if resp.status_code != 200:
                logger.warning(
                    "Apple token revocation returned %s: %s",
                    resp.status_code,
                    resp.text,
                )
    except Exception:
        logger.exception("Apple token revocation failed")
