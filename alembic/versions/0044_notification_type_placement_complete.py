"""Allow 'placement_complete' in the notification.type CHECK constraint.

Discovered while browser-verifying Task #24 Phase E (kingguru-task24 §6):
`placement_service.choose_level()` calls
`notification_service.create(..., notif_type="placement_complete", ...)`
(services/placement_service.py) but the 0001 initial-schema CHECK constraint
on `notification.type` never included that value — only
'achievement_unlocked', 'streak_at_risk', 'lesson_unlocked',
'lesson_complete', 'announcement', 'content_review_decision'. Every call to
POST /api/v1/placement/choose-level (guest AND authenticated) hits a
CheckViolationError, which is unhandled and surfaces as a bare 500 with no
CORS headers — the browser reports it as "Failed to fetch", which is what
sent guests down the "Could not start the lesson" dead end. Live-verified by
curling the endpoint directly against production before this fix.

Revision ID: 8d9e6f1a2b3c
Revises:     7c4d5e6f8a9b
Create Date: 2026-07-20
"""
from typing import Sequence, Union

from alembic import op

revision: str = "8d9e6f1a2b3c"
down_revision: Union[str, None] = "7c4d5e6f8a9b"
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
                'placement_complete'
            ))
    """)


def downgrade() -> None:
    op.execute("DELETE FROM notification WHERE type = 'placement_complete'")
    op.execute("ALTER TABLE notification DROP CONSTRAINT notification_type_check")
    op.execute("""
        ALTER TABLE notification ADD CONSTRAINT notification_type_check
            CHECK (type IN (
                'achievement_unlocked', 'streak_at_risk',
                'lesson_unlocked', 'lesson_complete',
                'announcement', 'content_review_decision'
            ))
    """)
