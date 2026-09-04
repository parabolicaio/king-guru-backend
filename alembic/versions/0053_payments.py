"""Payments — OnePay checkout tracking + level pricing.

Adds price_amount/price_currency to level (no pricing data existed at all
before this) and a payment table tracking each OnePay checkout attempt from
creation through webhook/status-verified completion. A successful payment
grants the level via placement_service.choose_level() — the same function
self-selection already uses — so payment isn't a separate access model,
just another way to legitimately pass the payment_required guard that
POST /placement/choose-level enforces for manual self-selection.

price_amount is left NULL for every level — no real pricing data exists yet.
The checkout endpoint refuses to start a payment for a level with no price
configured rather than guessing one.

Revision ID: 9c0d1e2f3a4b
Revises:     8b9c0d1e2f3a
Create Date: 2026-09-04
"""
from typing import Sequence, Union

from alembic import op

revision: str = "9c0d1e2f3a4b"
down_revision: Union[str, None] = "8b9c0d1e2f3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE level
            ADD COLUMN price_amount   NUMERIC(10, 2),
            ADD COLUMN price_currency TEXT NOT NULL DEFAULT 'LKR'
    """)

    op.execute("""
        CREATE TABLE payment (
            id                   UUID           NOT NULL PRIMARY KEY,
            user_id              UUID           NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            level_id             UUID           NOT NULL REFERENCES level(id),
            reference            TEXT           NOT NULL,
            amount               NUMERIC(10, 2) NOT NULL,
            currency             TEXT           NOT NULL,
            status               TEXT           NOT NULL DEFAULT 'pending'
                                      CHECK (status IN ('pending', 'success', 'failed', 'cancelled')),
            onepay_transaction_id TEXT,
            raw_callback         JSONB,
            created_at           TIMESTAMPTZ    NOT NULL DEFAULT now(),
            updated_at           TIMESTAMPTZ    NOT NULL DEFAULT now(),
            paid_at              TIMESTAMPTZ,
            CONSTRAINT payment_reference_unique UNIQUE (reference)
        )
    """)
    op.execute("""
        CREATE INDEX payment_user_idx ON payment (user_id)
    """)
    op.execute("""
        CREATE INDEX payment_onepay_transaction_idx ON payment (onepay_transaction_id)
            WHERE onepay_transaction_id IS NOT NULL
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS payment")
    op.execute("""
        ALTER TABLE level
            DROP COLUMN IF EXISTS price_amount,
            DROP COLUMN IF EXISTS price_currency
    """)
