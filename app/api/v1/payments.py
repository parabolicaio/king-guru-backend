"""Payment endpoints — OnePay checkout creation, status polling, webhook."""

import logging

from fastapi import APIRouter, Depends, Request

import asyncpg

from app.core.errors import AppError, UNAUTHORIZED
from app.core.ratelimit import rate_limit
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.levels import get_level_by_id
from app.schemas.cards import CheckoutSavedCardRequest
from app.schemas.levels import CreateCheckoutRequest, CreateCheckoutResponse, PaymentStatusResponse
from app.services import card_service, payment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post(
    "/checkout",
    response_model=CreateCheckoutResponse,
    dependencies=[Depends(rate_limit(10, 60, "payment_checkout"))],
)
async def create_checkout(
    body: CreateCheckoutRequest,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> CreateCheckoutResponse:
    """Starts a OnePay checkout for a payment_required level. Registered
    users only — a guest has no durable account to grant the level to."""
    reference, redirect_url = await payment_service.start_checkout(db, dict(user), str(body.level_id))
    return CreateCheckoutResponse(reference=reference, redirect_url=redirect_url)


@router.get("/{reference}/status", response_model=PaymentStatusResponse)
async def get_payment_status(
    reference: str,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> PaymentStatusResponse:
    """Re-verifies with OnePay (not just a DB read) and returns the current
    status. The frontend's post-redirect return page polls this — since a
    webhook may not be reachable in every environment (e.g. a local
    backend during sandbox testing), this poll is what actually drives
    verification+level-grant in practice, not just a status display."""
    payment = await payment_service.verify_and_complete(db, reference)
    if str(payment["user_id"]) != str(user["id"]):
        raise AppError(*UNAUTHORIZED)

    level = await get_level_by_id(db, str(payment["level_id"]))
    return PaymentStatusResponse(
        reference=payment["reference"],
        status=payment["status"],
        level_id=payment["level_id"],
        level_name=level["name"] if level else "",
        amount=payment["amount"],
        currency=payment["currency"],
    )


@router.post(
    "/checkout-saved-card",
    dependencies=[Depends(rate_limit(10, 60, "payment_checkout_saved_card"))],
)
async def checkout_saved_card(
    body: CheckoutSavedCardRequest,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> dict:
    """Charges an existing saved card directly and grants the level on
    success — the payoff of Card on File: a returning payer completes a
    purchase in one call, no redirect/WebView needed."""
    await card_service.charge_with_saved_card(db, dict(user), body.token_id, str(body.level_id))
    return {"success": True}


@router.post("/webhook")
async def onepay_webhook(request: Request, db: asyncpg.Connection = Depends(get_db)) -> dict:
    """OnePay's server-to-server callback (configured in the OnePay merchant
    portal's APP section). Never trusted directly — the payload only tells
    us WHICH transaction to re-check; the actual success/failure comes from
    calling OnePay's own status endpoint (payment_service.verify_and_complete),
    per OnePay's documented guidance to never rely on redirect/callback data
    alone. Always returns 200 so OnePay doesn't endlessly retry a payload
    naming a transaction we don't recognize or can't currently reach.
    """
    from app.db.queries.payments import get_payment_by_onepay_transaction_id

    body = await request.json()
    onepay_transaction_id = body.get("transaction_id")
    if not onepay_transaction_id:
        logger.warning("OnePay webhook missing transaction_id: %s", body)
        return {"received": True}

    payment = await get_payment_by_onepay_transaction_id(db, onepay_transaction_id)
    if payment is None:
        logger.warning("OnePay webhook for unknown transaction_id=%s", onepay_transaction_id)
        return {"received": True}

    await payment_service.verify_and_complete(db, payment["reference"])
    return {"received": True}
