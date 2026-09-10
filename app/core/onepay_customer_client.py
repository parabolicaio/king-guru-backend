"""OnePay Customer Tokenizer / Card on File API client
(https://docs.onepay.lk/api-documentation/customer-tokenizer).

A SEPARATE API from onepay_client.py's Redirection checkout: different base
resource (`/v3/customers/`), and a different auth scheme — a single Access
Token in the Authorization header (no hash, no app_id in the body). Flow:

1. POST /v3/customers/  → creates (or reuses) a customer profile, returns a
   `customer_id` and a hosted `redirect_url` where the customer enters card
   details and consents to future charges.
2. GET /v3/customers/{id}/cards/  → call after the customer returns from
   that redirect, to retrieve the new `token_id` (+ card_type/masked_number/
   expiry) and store it.
3. POST /v3/customers/{id}/payments/  → charge a stored token_id for any
   amount, any time, entirely server-side — no redirect needed.

NOTE: unlike the Redirection API (whose live behavior around auth headers
and status-check HTTP method both diverged from OnePay's public docs and
had to be reverse-engineered), this client has not yet been exercised
against a live Access Token — that credential is a separate one from the
App ID/Hash Salt/App Token already configured, and hasn't been supplied
yet. Treat request/response shapes here as the documented starting point,
not confirmed-correct — re-verify each call the first time a real Access
Token is available, the same way the Redirection integration needed a few
live corrections.
"""

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(15.0)
_BASE = "https://api.onepay.lk/v3/customers"


class OnePayCustomerError(Exception):
    """Raised on any non-success response from OnePay, or a network failure."""


def _headers() -> dict[str, str]:
    return {"Authorization": settings.onepay_access_token}


async def _request(method: str, url: str, *, json: dict | None = None) -> dict:
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.request(method, url, json=json, headers=_headers())
    except httpx.HTTPError as e:
        logger.exception("OnePay customer-API request failed: %s %s", method, url)
        raise OnePayCustomerError(f"OnePay request failed: {e}") from e

    if resp.status_code not in (200, 201):
        logger.warning(
            "OnePay customer-API returned %s for %s %s: %s",
            resp.status_code, method, url, resp.text,
        )
        raise OnePayCustomerError(f"OnePay returned {resp.status_code}: {resp.text}")

    data = resp.json()
    return data.get("data", data)


async def create_customer(
    *,
    existing_customer_id: str | None,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
    address: str,
    redirect_url: str,
) -> dict:
    """Starts (or restarts) card tokenization. When `existing_customer_id`
    is set, only that + redirect_url is sent — OnePay reuses the existing
    profile and issues a fresh card-entry session for it. Returns a dict
    with `customer_id` and `redirect_url`.
    """
    body: dict = {"redirect_url": redirect_url}
    if existing_customer_id:
        body["customer_id"] = existing_customer_id
    else:
        body.update({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
        })
    return await _request("POST", f"{_BASE}/", json=body)


async def list_cards(customer_id: str) -> list[dict]:
    """Returns this customer's card token objects (token_id, card_type,
    masked_number, expiry, is_deleted)."""
    data = await _request(
        "GET", f"{_BASE}/{customer_id}/cards/?app_id={settings.onepay_app_id}",
    )
    return data if isinstance(data, list) else data.get("cards", [])


async def delete_card(customer_id: str, token_id: str) -> None:
    await _request("DELETE", f"{_BASE}/{customer_id}/cards/{token_id}/")


async def charge_card(
    *, customer_id: str, token_id: str, amount: str, currency: str,
) -> dict:
    """Charges a stored token for `amount` (a fixed 2-decimal string, e.g.
    "500.00"). Returns a dict with transaction_id/status/amount/currency."""
    return await _request(
        "POST",
        f"{_BASE}/{customer_id}/payments/",
        json={"token_id": token_id, "amount": amount, "currency": currency},
    )
