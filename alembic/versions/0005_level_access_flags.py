"""Add guest_enabled and payment_required to level table.

guest_enabled:    TRUE  → level is accessible without authentication (guest mode).
payment_required: TRUE  → level requires an active subscription; guests are
                           also blocked regardless of guest_enabled.

Both default to FALSE — all levels are sign-up-gated by default.
Change per level via a subsequent migration or admin panel action.

Revision ID: e5f6a7b8c9d0
Revises:     d4e5f6a7b8c9
Create Date: 2026-06-07
"""
from typing import Sequence, Union

from alembic import op

revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE level
            ADD COLUMN IF NOT EXISTS guest_enabled    BOOLEAN NOT NULL DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS payment_required BOOLEAN NOT NULL DEFAULT FALSE
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE level DROP COLUMN IF EXISTS payment_required")
    op.execute("ALTER TABLE level DROP COLUMN IF EXISTS guest_enabled")
