"""Saved cards — OnePay Card on File (Customer Tokenizer).

New, on both web and mobile: lets a user save a card once (via OnePay's
hosted tokenization page) and pay with it again later with a single server
call, no redirect/checkout page needed. Separate from the `payment` table
added in 0053 — this tracks OUR local mirror of OnePay's customer/card
records so we don't need to call OnePay's List Cards endpoint on every
checkout page load.

onepay_customer: one row per user who has started the add-card flow at
least once — mirrors OnePay's `cus_...` customer id.

saved_card: one row per tokenized card (`tok_...`), soft-deleted (never
hard-deleted) so a stale token can never be resurrected and charged after
the user removed it, matching OnePay's own soft-delete semantics for cards.

Revision ID: 0a1b2c3d4e5f
Revises:     9c0d1e2f3a4b
Create Date: 2026-09-10
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0a1b2c3d4e5f"
down_revision: Union[str, None] = "9c0d1e2f3a4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE onepay_customer (
            id                 UUID        NOT NULL PRIMARY KEY,
            user_id            UUID        NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE CASCADE,
            onepay_customer_id TEXT        NOT NULL UNIQUE,
            created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE saved_card (
            id                 UUID        NOT NULL PRIMARY KEY,
            user_id            UUID        NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            onepay_customer_id TEXT        NOT NULL,
            token_id           TEXT        NOT NULL UNIQUE,
            card_type          TEXT        NOT NULL,
            masked_number      TEXT        NOT NULL,
            expiry             TEXT        NOT NULL,
            is_deleted         BOOLEAN     NOT NULL DEFAULT FALSE,
            created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX saved_card_user_idx ON saved_card (user_id) WHERE is_deleted = FALSE
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS saved_card")
    op.execute("DROP TABLE IF EXISTS onepay_customer")
