"""Add feedback_language to daily_essay_submission.

Revision ID: b1c2d3e4f5a6
Revises:     a7b8c9d0e1f2
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op

revision: str = "b1c2d3e4f5a6"
down_revision: Union[str, None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE daily_essay_submission
            ADD COLUMN IF NOT EXISTS feedback_language TEXT NOT NULL DEFAULT 'en'
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE daily_essay_submission
            DROP COLUMN IF EXISTS feedback_language
    """)
