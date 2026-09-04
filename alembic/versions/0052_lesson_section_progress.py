"""Track content-navigation progress within a lesson section.

Section progress on the lesson-overview screen was computed only from
answered assessment questions — a section with no questions attempted yet
always showed 0%/"Not started", even after a learner read through most of
its content (word cards, grammar explanations, etc.). That navigation
position (current step index into the section's content+question sequence,
see LessonSectionPage.tsx's buildSteps()) was only ever persisted to the
browser's localStorage, never to the server, so it couldn't be reflected
back — for guests AND registered users alike, on any other device/session.

This table tracks the furthest step index reached per section, keyed the
same dual-identity way `attempt` already is (exactly one of user_id/
guest_token per row) so guest progress carries the same as attempts do.

Revision ID: 8b9c0d1e2f3a
Revises:     7a8b9c0d1e2f
Create Date: 2026-09-04
"""
from typing import Sequence, Union

from alembic import op

revision: str = "8b9c0d1e2f3a"
down_revision: Union[str, None] = "7a8b9c0d1e2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE lesson_section_progress (
            id                  UUID        NOT NULL PRIMARY KEY,
            user_id             UUID        REFERENCES "user"(id) ON DELETE CASCADE,
            guest_token         TEXT,
            lesson_section_id   UUID        NOT NULL REFERENCES lesson_section(id) ON DELETE CASCADE,
            furthest_step_index INTEGER     NOT NULL DEFAULT 0,
            total_steps         INTEGER     NOT NULL DEFAULT 0,
            created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT lesson_section_progress_identity_chk CHECK (
                (user_id IS NOT NULL AND guest_token IS NULL) OR
                (user_id IS NULL AND guest_token IS NOT NULL)
            )
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX lesson_section_progress_user_section_uq
            ON lesson_section_progress (user_id, lesson_section_id)
            WHERE user_id IS NOT NULL
    """)
    op.execute("""
        CREATE UNIQUE INDEX lesson_section_progress_guest_section_uq
            ON lesson_section_progress (guest_token, lesson_section_id)
            WHERE guest_token IS NOT NULL
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS lesson_section_progress")
