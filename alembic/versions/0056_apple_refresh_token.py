"""Add user.apple_refresh_token for Sign in with Apple revocation on delete.

App Store Guideline 5.1.1(v): an app offering Sign in with Apple must let
deleting the account also disconnect it from the user's Apple ID. That
requires calling Apple's /auth/revoke with the refresh_token issued at
sign-in — which has to be stored somewhere between sign-in and whenever the
user later deletes their account. Nullable: every non-Apple user, and any
Apple user who signed in before this shipped, simply has none to revoke.

Revision ID: 2a3b4c5d6e7f
Revises:     1f2a3b4c5d6e
Create Date: 2026-10-16
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "2a3b4c5d6e7f"
down_revision: Union[str, None] = "1f2a3b4c5d6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("apple_refresh_token", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user", "apple_refresh_token")
