"""Allow 'essay_graded' and 'streak_milestone' in the notification.type CHECK.

Found by the 2026-07-31 production review (contract-parity + release-migration
agents, independently). Same bug class as 0044: two live service call sites emit
notification types the CHECK constraint never listed —

  - `daily_essay_service.grade_submission()` calls
    notification_service.create(..., notif_type="essay_graded", ...)
    (app/services/daily_essay_service.py:431), on the SAME db session that just
    persisted the essay grade + awarded XP. The CheckViolationError aborts that
    transaction, so every daily-essay grading fails/rolls back.
  - `streak.py` calls create(..., notif_type="streak_milestone", ...)
    (app/services/streak.py:94) when a streak hits a seeded milestone day
    (7/14/30/60/90/180/365, seeded in 0002_seed_data.py). Same transaction as the
    streak update + XP award → the surrounding write path 500s on those days.

The 0044 author fixed only the one instance (placement_complete) they hit in the
browser; these two literals were never reconciled against the constraint. This
migration widens `notification_type_check` to the full set of 9 types the code
actually emits (the 7 from 0044 + these 2). Deferred/best-effort hardening — making
the notification insert non-fatal to the primary write — is tracked separately as a
P1 follow-up; this migration is the minimal fix that stops the 500s.

Revision ID: c5d6e7f8a9b0
Revises:     0e1f2a3b4c5d
Create Date: 2026-07-31
"""
from typing import Sequence, Union

from alembic import op

revision: str = "c5d6e7f8a9b0"
down_revision: Union[str, None] = "0e1f2a3b4c5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE notification DROP CONSTRAINT notification_type_check")
    op.execute("""
        ALTER TABLE notification ADD CONSTRAINT notification_type_check
            CHECK (type IN (
                'achievement_unlocked', 'streak_at_risk',
                'lesson_unlocked', 'lesson_complete',
                'announcement', 'content_review_decision',
                'placement_complete',
                'essay_graded', 'streak_milestone'
            ))
    """)


def downgrade() -> None:
    # Remove rows carrying the newly-allowed types before narrowing the CHECK,
    # so the constraint can be re-added (mirrors 0044's downgrade).
    op.execute(
        "DELETE FROM notification WHERE type IN ('essay_graded', 'streak_milestone')"
    )
    op.execute("ALTER TABLE notification DROP CONSTRAINT notification_type_check")
    op.execute("""
        ALTER TABLE notification ADD CONSTRAINT notification_type_check
            CHECK (type IN (
                'achievement_unlocked', 'streak_at_risk',
                'lesson_unlocked', 'lesson_complete',
                'announcement', 'content_review_decision',
                'placement_complete'
            ))
    """)
