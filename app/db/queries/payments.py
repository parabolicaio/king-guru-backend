"""Raw SQL queries for the payment table (OnePay checkout tracking)."""

import json
from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid


async def create_payment(
    db: asyncpg.Connection,
    *,
    user_id: str,
    level_id: str,
    reference: str,
    amount: str,
    currency: str,
) -> asyncpg.Record:
    payment_id = new_uuid()
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        INSERT INTO payment
            (id, user_id, level_id, reference, amount, currency, status, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, 'pending', $7, $7)
        RETURNING *
        """,
        payment_id, user_id, level_id, reference, amount, currency, now,
    )


async def set_onepay_transaction_id(
    db: asyncpg.Connection, *, reference: str, onepay_transaction_id: str,
) -> None:
    await db.execute(
        """
        UPDATE payment
        SET onepay_transaction_id = $2, updated_at = now()
        WHERE reference = $1
        """,
        reference, onepay_transaction_id,
    )


async def get_payment_by_reference(
    db: asyncpg.Connection, reference: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        'SELECT * FROM payment WHERE reference = $1', reference,
    )


async def get_payment_by_onepay_transaction_id(
    db: asyncpg.Connection, onepay_transaction_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        'SELECT * FROM payment WHERE onepay_transaction_id = $1', onepay_transaction_id,
    )


async def mark_payment_status(
    db: asyncpg.Connection,
    *,
    reference: str,
    status: str,
    raw_callback: dict | None = None,
) -> asyncpg.Record:
    """status: 'success' | 'failed' | 'cancelled'. Sets paid_at only on
    'success'. Idempotent — safe to call again with the same terminal
    status (e.g. webhook and status-poll both confirming the same result)."""
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        UPDATE payment
        SET status       = $2,
            raw_callback = COALESCE($3::jsonb, raw_callback),
            paid_at      = CASE WHEN $2 = 'success' THEN COALESCE(paid_at, $4) ELSE paid_at END,
            updated_at   = $4
        WHERE reference = $1
        RETURNING *
        """,
        reference, status, json.dumps(raw_callback) if raw_callback is not None else None, now,
    )
