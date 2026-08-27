"""Narrow user.language_preference to two values: en, si.

Product decision: the app now has exactly two display modes, English and
Sinhala — no more separate "Singlish" concept. 'singlish' and 'en' have
always behaved identically on both clients (English-only), so existing rows
are simply normalised to 'en' before the constraint narrows.

Revision ID: 6f7a8b9c0d1e
Revises:     5e6f7a8b9c0d
Create Date: 2026-08-26
"""
from typing import Sequence, Union

from alembic import op

revision: str = "6f7a8b9c0d1e"
down_revision: Union[str, None] = "5e6f7a8b9c0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE "user"
        SET language_preference = 'en', updated_at = now()
        WHERE language_preference = 'singlish'
        """
    )
    # PostgreSQL names the inline check as user_language_preference_check.
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_language_preference_check')
    op.execute(
        """
        ALTER TABLE "user" ADD CONSTRAINT user_language_preference_check
            CHECK (language_preference IN ('en', 'si'))
        """
    )


def downgrade() -> None:
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_language_preference_check')
    op.execute(
        """
        ALTER TABLE "user" ADD CONSTRAINT user_language_preference_check
            CHECK (language_preference IN ('en', 'si', 'singlish'))
        """
    )
