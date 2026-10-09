"""Allow 'apple' as a user.auth_provider value.

Sign in with Apple (App Store Guideline 4.8) sets the Supabase JWT's
app_metadata.provider claim to 'apple', and user_service._derive_auth_provider
now maps that straight through — but the original CHECK constraint only
allowed 'email', 'google', 'phone', so every first-time Apple sign-up would
fail its INSERT until this widens it.

Revision ID: 1f2a3b4c5d6e
Revises:     0a1b2c3d4e5f
Create Date: 2026-10-09
"""
from typing import Sequence, Union

from alembic import op

revision: str = "1f2a3b4c5d6e"
down_revision: Union[str, None] = "0a1b2c3d4e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_auth_provider_check')
    op.execute("""
        ALTER TABLE "user" ADD CONSTRAINT user_auth_provider_check
            CHECK (auth_provider IN ('email', 'google', 'phone', 'apple'))
    """)


def downgrade() -> None:
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_auth_provider_check')
    op.execute("""
        ALTER TABLE "user" ADD CONSTRAINT user_auth_provider_check
            CHECK (auth_provider IN ('email', 'google', 'phone'))
    """)
