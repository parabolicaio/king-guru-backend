"""OnePay checkout orchestration.

Payment is just another legitimate way to pass the payment_required guard
that POST /placement/choose-level enforces for self-selection — a
successful, gateway-verified payment calls placement_service.choose_level()
to actually grant the level, the same function self-selection already uses.
There's no separate "entitlements" concept; the data model still has one
current_level_id per user.

Security note (per OnePay's own docs): a customer's redirect back to our
site, and an unverified webhook body, are NOT proof of payment on their
own. Every completion path here re-confirms via
onepay_client.get_transaction_status() before granting anything.
"""

import logging
import secrets
from decimal import Decimal

from app.core import onepay_client
from app.core.config import settings
from app.core.errors import (
    AppError,
    LEVEL_NOT_FOUND,
    LEVEL_NOT_PAID,
    LEVEL_PRICE_NOT_SET,
    PAYMENT_GATEWAY_ERROR,
    PAYMENT_NOT_FOUND,
)
from app.db.queries.levels import get_level_by_id
from app.db.queries.payments import (
    create_payment,
    get_payment_by_reference,
    mark_payment_status,
    set_onepay_transaction_id,
)
from app.db.queries.users import sanitise_phone

logger = logging.getLogger(__name__)


def _new_reference() -> str:
    # OnePay caps `reference` at 21 characters — a raw UUID (36 chars) blows
    # past that. "kg" + 18 hex chars (9 random bytes) stays well under the
    # limit while remaining effectively collision-proof.
    return f"kg{secrets.token_hex(9)}"


def _split_name(full_name: str) -> tuple[str, str]:
    parts = (full_name or "").strip().split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    if len(parts) == 1:
        return parts[0], parts[0]
    return "Customer", "Customer"


async def start_checkout(db, user: dict, level_id: str) -> tuple[str, str]:
    """Creates a pending payment row + a OnePay checkout session.
    Returns (reference, redirect_url). Raises AppError on any validation
    failure or gateway error.
    """
    level = await get_level_by_id(db, level_id)
    if level is None:
        raise AppError(*LEVEL_NOT_FOUND)
    if not level["payment_required"]:
        raise AppError(*LEVEL_NOT_PAID)
    if level["price_amount"] is None:
        raise AppError(*LEVEL_PRICE_NOT_SET)

    reference = _new_reference()
    # Format to EXACTLY two decimals, e.g. "500.00". OnePay rebuilds the
    # security hash on its side from app_id + currency + amount + hash_salt,
    # so the amount string sent here must match OnePay's own formatting or the
    # whole request is rejected as "Invalid app credentials". A bare
    # str(level["price_amount"]) on a value stored without a scale (e.g. 500,
    # or 500.0) would send "500" / "500.0" and silently break the hash.
    # Going through Decimal(str(...)) handles Decimal, int and float safely.
    amount = f"{Decimal(str(level['price_amount'])):.2f}"
    currency = level["price_currency"] or "LKR"

    await create_payment(
        db,
        user_id=str(user["id"]),
        level_id=str(level["id"]),
        reference=reference,
        amount=amount,
        currency=currency,
    )

    first_name, last_name = _split_name(user.get("full_name") or "")
    phone_with_plus, _ = sanitise_phone(user.get("phone") or "")
    # This app is phone-only: auth is phone + OTP and no email is ever
    # collected. OnePay still requires a validly-formatted email for its
    # receipt field, so synthesise one from the phone number. Digits only
    # keeps the local part valid, and it makes the customer recognisable in
    # OnePay's dashboard when reconciling payments. Falls back to the user id
    # if a phone somehow isn't present, so the address is never malformed.
    # If a real email ever does exist on the account, prefer it.
    phone_digits = "".join(ch for ch in phone_with_plus if ch.isdigit())
    customer_email = user.get("email") or f"{phone_digits or user['id']}@no-reply.kingguru.ai"

    try:
        data = await onepay_client.create_checkout_link(
            reference=reference,
            amount=amount,
            currency=currency,
            customer_first_name=first_name,
            customer_last_name=last_name,
            customer_phone_number=phone_with_plus,
            customer_email=customer_email,
            redirect_url=f"{settings.onepay_redirect_url}?reference={reference}",
        )
        redirect_url = (data.get("gateway") or {}).get("redirect_url")
        ipg_transaction_id = data.get("ipg_transaction_id")
        if not redirect_url or not ipg_transaction_id:
            logger.error("OnePay create-checkout response missing fields: %s", data)
            raise onepay_client.OnePayError(f"Unexpected response shape: {data}")
    except onepay_client.OnePayError:
        await mark_payment_status(db, reference=reference, status="failed")
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    await set_onepay_transaction_id(db, reference=reference, onepay_transaction_id=ipg_transaction_id)
    return reference, redirect_url


async def verify_and_complete(db, reference: str) -> dict:
    """Re-confirms a payment's status with OnePay and, on genuine success,
    grants the level. Idempotent — safe to call repeatedly (from the
    frontend's return-page poll AND the webhook both hitting the same
    payment). Returns the payment row as a dict.
    """
    from app.services import placement_service

    payment = await get_payment_by_reference(db, reference)
    if payment is None:
        raise AppError(*PAYMENT_NOT_FOUND)

    if payment["status"] == "success":
        return dict(payment)

    if not payment["onepay_transaction_id"]:
        # Checkout session was never confirmed as created — nothing to verify yet.
        return dict(payment)

    try:
        status_data = await onepay_client.get_transaction_status(payment["onepay_transaction_id"])
    except onepay_client.OnePayError:
        logger.exception("OnePay status check failed for reference=%s", reference)
        return dict(payment)

    if status_data.get("status") is True:
        updated = await mark_payment_status(
            db, reference=reference, status="success", raw_callback=status_data,
        )
        await placement_service.choose_level(db, str(payment["user_id"]), str(payment["level_id"]))
        return dict(updated)

    # OnePay's status boolean is false BOTH while a payment is still settling
    # (the first seconds right after the redirect back) AND for one the
    # customer genuinely abandoned — paid_on is null in both, so the response
    # alone can't tell them apart. Marking "failed" on a false here therefore
    # fails legitimate payments that simply haven't cleared yet, which is
    # exactly what made the return page show failure while the webhook later
    # granted the level. Leave it PENDING instead: the client keeps polling
    # and picks up success once OnePay settles. A truly abandoned payment just
    # stays pending forever, which is harmless — no level is ever granted
    # without a true status.
    return dict(payment)