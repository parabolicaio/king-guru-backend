"""Enable guest access on the first lesson of Beginner A & B.

Guest mode lets a visitor try the app without signing up. The backend already
enforces guest access at the lesson level (lesson.is_guest_accessible, checked
in lessons.py / attempts.py) and exposes level.guest_enabled to the client.
This migration opens the minimal guest surface:

  - level.guest_enabled       = TRUE for beginner_a, beginner_b
  - lesson.is_guest_accessible = TRUE for their Lesson 1 (order 1)

A guest is placed via the placement assessment, then routed into the first
lesson of their placed level (falling back to Beginner A when the placed level
has no content). Only these two lessons are opened; everything else stays gated
behind the sign-up wall.

Idempotent — keyed by level code + lesson order; safe to re-run.

Revision ID: 5a2b3c4d5e6f
Revises:     4e1f2a3b4c5d
Create Date: 2026-07-05
"""
from typing import Sequence, Union

from alembic import op

revision: str = "5a2b3c4d5e6f"
down_revision: Union[str, None] = "4e1f2a3b4c5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_GUEST_CODES = ("beginner_a", "beginner_b")


def upgrade() -> None:
    op.execute(
        """
        UPDATE level
        SET guest_enabled = TRUE, updated_at = now()
        WHERE code IN ('beginner_a', 'beginner_b')
        """
    )
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = TRUE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND lv.code IN ('beginner_a', 'beginner_b')
          AND l.lesson_order = 1
          AND l.deleted_at IS NULL
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = FALSE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND lv.code IN ('beginner_a', 'beginner_b')
          AND l.lesson_order = 1
        """
    )
    op.execute(
        """
        UPDATE level
        SET guest_enabled = FALSE, updated_at = now()
        WHERE code IN ('beginner_a', 'beginner_b')
        """
    )
