"""Add draft support to daily_essay_submission.

Changes:
  - submitted_at: NOT NULL → nullable  (NULL while essay is a draft)
  - is_draft BOOLEAN NOT NULL DEFAULT FALSE  (TRUE = saved draft, FALSE = submitted)
  - UNIQUE (user_id, submission_date) constraint  (one row per user per day)

Existing rows are all real submissions so is_draft stays FALSE and
submitted_at remains set.

Revision ID: a7b8c9d0e1f2
Revises:     f6a7b8c9d0e1
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op

revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make submitted_at nullable — drafts have no submitted_at until final submit
    op.execute("""
        ALTER TABLE daily_essay_submission
            ALTER COLUMN submitted_at DROP NOT NULL,
            ALTER COLUMN submitted_at DROP DEFAULT,
            ADD COLUMN IF NOT EXISTS is_draft BOOLEAN NOT NULL DEFAULT FALSE
    """)

    # One row per user per calendar day — enforced at DB level
    op.execute("""
        ALTER TABLE daily_essay_submission
            ADD CONSTRAINT daily_essay_submission_user_date_unique
            UNIQUE (user_id, submission_date)
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE daily_essay_submission
            DROP CONSTRAINT IF EXISTS daily_essay_submission_user_date_unique
    """)
    op.execute("""
        ALTER TABLE daily_essay_submission
            DROP COLUMN IF EXISTS is_draft,
            ALTER COLUMN submitted_at SET DEFAULT now(),
            ALTER COLUMN submitted_at SET NOT NULL
    """)
