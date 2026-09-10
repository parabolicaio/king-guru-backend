"""Raw SQL queries for onepay_customer / saved_card (Card on File)."""

import asyncpg

from app.db.utils import new_uuid


async def get_onepay_customer(db: asyncpg.Connection, user_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM onepay_customer WHERE user_id = $1", user_id,
    )


async def create_onepay_customer(
    db: asyncpg.Connection, *, user_id: str, onepay_customer_id: str,
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        INSERT INTO onepay_customer (id, user_id, onepay_customer_id, created_at, updated_at)
        VALUES ($1, $2, $3, now(), now())
        RETURNING *
        """,
        new_uuid(), user_id, onepay_customer_id,
    )


async def upsert_saved_card(
    db: asyncpg.Connection,
    *,
    user_id: str,
    onepay_customer_id: str,
    token_id: str,
    card_type: str,
    masked_number: str,
    expiry: str,
) -> asyncpg.Record:
    """Idempotent — safe to call again for a token already on file (e.g.
    re-syncing after a repeat card-entry redirect)."""
    return await db.fetchrow(
        """
        INSERT INTO saved_card
            (id, user_id, onepay_customer_id, token_id, card_type, masked_number, expiry,
             is_deleted, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, FALSE, now(), now())
        ON CONFLICT (token_id) DO UPDATE SET
            card_type     = EXCLUDED.card_type,
            masked_number = EXCLUDED.masked_number,
            expiry        = EXCLUDED.expiry,
            is_deleted    = FALSE,
            updated_at    = now()
        RETURNING *
        """,
        new_uuid(), user_id, onepay_customer_id, token_id, card_type, masked_number, expiry,
    )


async def list_saved_cards(db: asyncpg.Connection, user_id: str) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT * FROM saved_card
        WHERE user_id = $1 AND is_deleted = FALSE
        ORDER BY created_at DESC
        """,
        user_id,
    )


async def get_saved_card_by_token(
    db: asyncpg.Connection, token_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM saved_card WHERE token_id = $1 AND is_deleted = FALSE", token_id,
    )


async def soft_delete_saved_card(db: asyncpg.Connection, token_id: str) -> None:
    await db.execute(
        "UPDATE saved_card SET is_deleted = TRUE, updated_at = now() WHERE token_id = $1",
        token_id,
    )
