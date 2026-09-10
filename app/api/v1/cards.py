"""Saved card endpoints — OnePay Card on File. Registered users only, same
reasoning as /payments: a guest has no durable account to attach a card to.
"""

import asyncpg
from fastapi import APIRouter, Depends

from app.core.ratelimit import rate_limit
from app.core.security import get_current_user
from app.db.pool import get_db
from app.schemas.cards import (
    AddCardResponse,
    SavedCardResponse,
    SavedCardsListResponse,
)
from app.services import card_service

router = APIRouter(prefix="/api/v1/cards", tags=["cards"])


@router.post(
    "/add-card",
    response_model=AddCardResponse,
    dependencies=[Depends(rate_limit(10, 60, "card_add"))],
)
async def add_card(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AddCardResponse:
    redirect_url = await card_service.start_add_card(db, dict(user))
    return AddCardResponse(redirect_url=redirect_url)


@router.post("/sync")
async def sync_cards(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> dict:
    """Call once the add-card WebView/redirect detects a return, to pull the
    new token from OnePay and store it."""
    await card_service.sync_cards_after_return(db, dict(user))
    return {"synced": True}


@router.get("", response_model=SavedCardsListResponse)
async def list_cards(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> SavedCardsListResponse:
    cards = await card_service.list_saved_cards(db, dict(user))
    return SavedCardsListResponse(
        cards=[
            SavedCardResponse(
                token_id=c["token_id"],
                card_type=c["card_type"],
                masked_number=c["masked_number"],
                expiry=c["expiry"],
            )
            for c in cards
        ]
    )


@router.delete("/{token_id}")
async def delete_card(
    token_id: str,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> dict:
    await card_service.delete_saved_card(db, dict(user), token_id)
    return {"deleted": True}
