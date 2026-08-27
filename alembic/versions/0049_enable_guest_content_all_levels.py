"""Enable guest access on the first lesson of every active level.

Extends 0041_enable_guest_content.py from a hardcoded two-level allowlist
(beginner_a, beginner_b) to every active level. Product decision: a guest can
preview the first lesson of ANY level — including payment-required ones — as
a standing, repeatable permission (not single-use). The guest button now
routes straight to a level picker instead of the placement quiz, so every
level needs its lesson 1 opened up, not just the two the quiz used to
recommend into.

The backend already enforces guest access generically at the lesson level
(lesson.is_guest_accessible, checked in api/v1/lessons.py) and exposes
level.guest_enabled to the client — this migration is purely a data backfill,
no application code changes.

Idempotent — re-running only touches rows not already flagged; safe to re-run.
Self-completing: as new levels/lessons are approved, a future re-run (or the
WHERE clause matching newly-active rows) would pick them up automatically,
though today it only runs once against whatever is active at migration time.

Revision ID: 5e6f7a8b9c0d
Revises:     48d1e2f3a4b5
Create Date: 2026-08-25
"""
from typing import Sequence, Union

from alembic import op

revision: str = "5e6f7a8b9c0d"
down_revision: Union[str, None] = "48d1e2f3a4b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE level
        SET guest_enabled = TRUE, updated_at = now()
        WHERE is_active = TRUE
          AND guest_enabled = FALSE
        """
    )
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = TRUE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND lv.is_active = TRUE
          AND l.lesson_order = 1
          AND l.deleted_at IS NULL
          AND l.is_guest_accessible = FALSE
        """
    )


def downgrade() -> None:
    # Note: not lossless relative to 0041 — this also reverts Beginner/
    # Elementary's guest flags that 0041 originally set, since this migration
    # reasserted them as part of "all levels." Intentional, monotonic history.
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = FALSE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND l.lesson_order = 1
        """
    )
    op.execute(
        """
        UPDATE level
        SET guest_enabled = FALSE, updated_at = now()
        """
    )
