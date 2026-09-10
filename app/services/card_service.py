"""OnePay Card on File orchestration — add/list/delete/charge saved cards.

A successful saved-card charge grants a level through the same
placement_service.choose_level() call payment_service.verify_and_complete()
uses for a fresh Redirection checkout — one authoritative grant point for
every way a level can be paid for.
"""

import logging

from app.core import onepay_customer_client
from app.core.config import settings
from app.core.errors import (
    AppError,
    CARD_NOT_FOUND,
    CARD_NOT_OWNED,
    LEVEL_NOT_FOUND,
    LEVEL_NOT_PAID,
    LEVEL_PRICE_NOT_SET,
    PAYMENT_GATEWAY_ERROR,
)
from app.db.queries.cards import (
    create_onepay_customer,
    get_onepay_customer,
    get_saved_card_by_token,
    list_saved_cards as query_list_saved_cards,
    soft_delete_saved_card,
    upsert_saved_card,
)
from app.db.queries.levels import get_level_by_id
from app.db.queries.users import sanitise_phone
from decimal import Decimal

logger = logging.getLogger(__name__)


def _split_name(full_name: str) -> tuple[str, str]:
    parts = (full_name or "").strip().split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    if len(parts) == 1:
        return parts[0], parts[0]
    return "Customer", "Customer"


async def start_add_card(db, user: dict) -> str:
    """Returns the OnePay-hosted card-entry URL. Reuses an existing OnePay
    customer profile if this user already has one (a second card added to
    the same profile), otherwise creates a fresh one.
    """
    existing = await get_onepay_customer(db, str(user["id"]))

    first_name, last_name = _split_name(user.get("full_name") or "")
    phone_with_plus, _ = sanitise_phone(user.get("phone") or "")
    phone_digits = "".join(ch for ch in phone_with_plus if ch.isdigit())
    email = user.get("email") or f"{phone_digits or user['id']}@no-reply.kingguru.ai"

    try:
        data = await onepay_customer_client.create_customer(
            existing_customer_id=existing["onepay_customer_id"] if existing else None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_with_plus,
            # No address field exists in this app's profile data — OnePay's
            # docs don't mark it required; sent empty rather than guessed.
            address="",
            redirect_url=settings.onepay_card_redirect_url,
        )
    except onepay_customer_client.OnePayCustomerError:
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    onepay_customer_id = data.get("customer_id")
    redirect_url = data.get("redirect_url")
    if not onepay_customer_id or not redirect_url:
        logger.error("OnePay create-customer response missing fields: %s", data)
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    if existing is None:
        await create_onepay_customer(
            db, user_id=str(user["id"]), onepay_customer_id=onepay_customer_id,
        )

    return redirect_url


async def sync_cards_after_return(db, user: dict) -> None:
    """Pulls this user's current card tokens from OnePay and mirrors them
    locally. Call once the add-card WebView/redirect detects a return."""
    customer = await get_onepay_customer(db, str(user["id"]))
    if customer is None:
        return

    try:
        cards = await onepay_customer_client.list_cards(customer["onepay_customer_id"])
    except onepay_customer_client.OnePayCustomerError:
        logger.exception("OnePay list-cards failed for user_id=%s", user["id"])
        return

    for card in cards:
        if card.get("is_deleted"):
            continue
        token_id = card.get("token_id")
        if not token_id:
            continue
        await upsert_saved_card(
            db,
            user_id=str(user["id"]),
            onepay_customer_id=customer["onepay_customer_id"],
            token_id=token_id,
            card_type=card.get("card_type") or "",
            masked_number=card.get("masked_number") or "",
            expiry=card.get("expiry") or "",
        )


async def list_saved_cards(db, user: dict) -> list:
    return await query_list_saved_cards(db, str(user["id"]))


async def delete_saved_card(db, user: dict, token_id: str) -> None:
    card = await get_saved_card_by_token(db, token_id)
    if card is None:
        raise AppError(*CARD_NOT_FOUND)
    if str(card["user_id"]) != str(user["id"]):
        raise AppError(*CARD_NOT_OWNED)

    try:
        await onepay_customer_client.delete_card(card["onepay_customer_id"], token_id)
    except onepay_customer_client.OnePayCustomerError:
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    await soft_delete_saved_card(db, token_id)


async def charge_with_saved_card(db, user: dict, token_id: str, level_id: str) -> None:
    """Charges an existing saved card for a payment_required level and, on
    success, grants it — no redirect/WebView needed for a returning payer."""
    from app.services import placement_service

    card = await get_saved_card_by_token(db, token_id)
    if card is None:
        raise AppError(*CARD_NOT_FOUND)
    if str(card["user_id"]) != str(user["id"]):
        raise AppError(*CARD_NOT_OWNED)

    level = await get_level_by_id(db, level_id)
    if level is None:
        raise AppError(*LEVEL_NOT_FOUND)
    if not level["payment_required"]:
        raise AppError(*LEVEL_NOT_PAID)
    if level["price_amount"] is None:
        raise AppError(*LEVEL_PRICE_NOT_SET)

    amount = f"{Decimal(str(level['price_amount'])):.2f}"
    currency = level["price_currency"] or "LKR"

    try:
        result = await onepay_customer_client.charge_card(
            customer_id=card["onepay_customer_id"],
            token_id=token_id,
            amount=amount,
            currency=currency,
        )
    except onepay_customer_client.OnePayCustomerError:
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    if result.get("status") is not True:
        logger.warning("OnePay saved-card charge did not succeed: %s", result)
        raise AppError(*PAYMENT_GATEWAY_ERROR)

    await placement_service.choose_level(db, str(user["id"]), level_id)
