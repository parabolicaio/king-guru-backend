"""Extend daily_goal table for level-based templates.

Adds level_id FK and expands goal_type CHECK to include the three new types:
  correct_answers, assessment_questions_answered, lesson_sections_completed

Revision ID: d3e4f5a6b7c8
Revises:     c2d3e4f5a6b7
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op

revision: str = "d3e4f5a6b7c8"
down_revision: Union[str, None] = "c2d3e4f5a6b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NEW_TYPES = (
    "questions_answered",
    "correct_answers",
    "assessment_questions_answered",
    "lesson_sections_completed",
    "lessons_completed",
    "xp_earned",
    "words_learned",
    "essay_submitted",
)

_OLD_TYPES = (
    "questions_answered",
    "lessons_completed",
    "xp_earned",
    "words_learned",
    "essay_submitted",
)


def _constraint_values(types: tuple) -> str:
    return ", ".join(f"'{t}'" for t in types)


def upgrade() -> None:
    # Drop old inline CHECK (auto-named by PostgreSQL)
    op.execute("""
        DO $$
        BEGIN
            ALTER TABLE daily_goal DROP CONSTRAINT daily_goal_goal_type_check;
        EXCEPTION WHEN undefined_object THEN NULL;
        END $$
    """)

    op.execute(f"""
        ALTER TABLE daily_goal
        ADD CONSTRAINT daily_goal_goal_type_check
        CHECK (goal_type IN ({_constraint_values(_NEW_TYPES)}))
    """)

    # Add level_id — table is empty in all environments at this point
    op.execute("""
        ALTER TABLE daily_goal
        ADD COLUMN level_id UUID NOT NULL REFERENCES level(id) ON DELETE RESTRICT
    """)

    op.execute("""
        CREATE INDEX daily_goal_level_idx ON daily_goal (level_id)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS daily_goal_level_idx")
    op.execute("ALTER TABLE daily_goal DROP COLUMN IF EXISTS level_id")

    op.execute("""
        DO $$
        BEGIN
            ALTER TABLE daily_goal DROP CONSTRAINT daily_goal_goal_type_check;
        EXCEPTION WHEN undefined_object THEN NULL;
        END $$
    """)

    op.execute(f"""
        ALTER TABLE daily_goal
        ADD CONSTRAINT daily_goal_goal_type_check
        CHECK (goal_type IN ({_constraint_values(_OLD_TYPES)}))
    """)
