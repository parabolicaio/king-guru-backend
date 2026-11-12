"""Users can be hidden from the leaderboard (D-89).

Adds user.leaderboard_hidden (default FALSE). Learners can turn it on in
Settings. Staff accounts (admin_role set) start hidden. Test and App Review
accounts can be hidden by setting the flag for them.

Revision ID: f68b2c3d4e5a
Revises:     e67a1b2c3d4f
Create Date: 2026-11-13
"""
from typing import Sequence, Union

from alembic import op

revision: str = "f68b2c3d4e5a"
down_revision: Union[str, None] = "e67a1b2c3d4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS leaderboard_hidden '
        "BOOLEAN NOT NULL DEFAULT FALSE"
    )
    op.execute('UPDATE "user" SET leaderboard_hidden = TRUE WHERE admin_role IS NOT NULL')


def downgrade() -> None:
    op.execute('ALTER TABLE "user" DROP COLUMN IF EXISTS leaderboard_hidden')
