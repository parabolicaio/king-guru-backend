"""Restrict free/guest content to Level 1 (beginner) only.

Supersedes 0049_enable_guest_content_all_levels.py. Product decision changed:
instead of every level's first lesson being a free preview, now only the
FIRST LEVEL is free in its entirety (all its lessons) — for guests and for
registered users who manually self-select a level. Every other level is
locked behind payment_required, enforced at the API layer in
app/api/v1/placement.py's choose_level endpoint (the manual-selection path
only — the placement-quiz recommendation path stays exempt, unchanged).

Revision ID: 7a8b9c0d1e2f
Revises:     6f7a8b9c0d1e
Create Date: 2026-08-27
"""
from typing import Sequence, Union

from alembic import op

revision: str = "7a8b9c0d1e2f"
down_revision: Union[str, None] = "6f7a8b9c0d1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE level
        SET guest_enabled = TRUE, payment_required = FALSE, updated_at = now()
        WHERE code = 'beginner'
        """
    )
    op.execute(
        """
        UPDATE level
        SET guest_enabled = FALSE, payment_required = TRUE, updated_at = now()
        WHERE code != 'beginner'
        """
    )
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = TRUE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND lv.code = 'beginner'
          AND l.deleted_at IS NULL
          AND l.is_guest_accessible = FALSE
        """
    )
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = FALSE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND lv.code != 'beginner'
          AND l.deleted_at IS NULL
          AND l.is_guest_accessible = TRUE
        """
    )


def downgrade() -> None:
    # Restores 0049's end-state (all levels open, lesson_order=1 free per
    # level with content) rather than a blanket false, so this is a
    # meaningful rollback rather than a dead end.
    op.execute(
        """
        UPDATE level
        SET guest_enabled = TRUE, payment_required = FALSE, updated_at = now()
        """
    )
    op.execute(
        """
        UPDATE lesson l
        SET is_guest_accessible = TRUE, updated_at = now()
        FROM level lv
        WHERE lv.id = l.level_id
          AND l.lesson_order = 1
          AND l.deleted_at IS NULL
        """
    )
