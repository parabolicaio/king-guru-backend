"""Create daily_goal_assignment table.

One row per (level_id, goal_date) — written by lazy generation when the first
user of that level requests today's goal.  The UNIQUE constraint absorbs any
concurrent insert race: ON CONFLICT DO NOTHING + re-fetch pattern in the service.

Revision ID: e4f5a6b7c8d9
Revises:     d3e4f5a6b7c8
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op

revision: str = "e4f5a6b7c8d9"
down_revision: Union[str, None] = "d3e4f5a6b7c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE daily_goal_assignment (
            id            UUID        NOT NULL PRIMARY KEY,
            daily_goal_id UUID        NOT NULL REFERENCES daily_goal(id) ON DELETE RESTRICT,
            level_id      UUID        NOT NULL REFERENCES level(id)      ON DELETE RESTRICT,
            goal_date     DATE        NOT NULL,
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT daily_goal_assignment_unique UNIQUE (level_id, goal_date)
        )
    """)

    op.execute("""
        CREATE INDEX daily_goal_assignment_level_date_idx
        ON daily_goal_assignment (level_id, goal_date DESC)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS daily_goal_assignment_level_date_idx")
    op.execute("DROP TABLE IF EXISTS daily_goal_assignment")
