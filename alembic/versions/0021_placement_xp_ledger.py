"""Allow placement XP entries in xp_ledger.

Placement submit awards XP with action_type=placement_question and
reference_type=placement, which were missing from the original CHECK constraints.

Revision ID: b2c3d4e5f6a8
Revises:     a1b2c3d4e6f7
Create Date: 2026-06-11
"""
from typing import Sequence, Union

from alembic import op

revision: str = "b2c3d4e5f6a8"
down_revision: Union[str, None] = "a1b2c3d4e6f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_ACTION_TYPES_OLD = (
    "lesson_complete",
    "word_learned",
    "essay_submitted",
    "streak_day",
    "streak_milestone",
    "achievement_unlocked",
    "daily_goal_complete",
    "question_attempt",
)

_ACTION_TYPES_NEW = _ACTION_TYPES_OLD + ("placement_question",)

_REFERENCE_TYPES_OLD = (
    "attempt",
    "essay",
    "achievement",
    "daily_goal",
    "lesson",
    "vocabulary_word",
)

_REFERENCE_TYPES_NEW = _REFERENCE_TYPES_OLD + ("placement",)


def _values(types: tuple[str, ...]) -> str:
    return ", ".join(f"'{t}'" for t in types)


def _drop_constraint(table: str, name: str) -> None:
    op.execute(f"""
        DO $$
        BEGIN
            ALTER TABLE {table} DROP CONSTRAINT {name};
        EXCEPTION WHEN undefined_object THEN NULL;
        END $$
    """)


def upgrade() -> None:
    _drop_constraint("xp_ledger", "xp_ledger_action_type_check")
    op.execute(f"""
        ALTER TABLE xp_ledger
        ADD CONSTRAINT xp_ledger_action_type_check
        CHECK (action_type IN ({_values(_ACTION_TYPES_NEW)}))
    """)

    _drop_constraint("xp_ledger", "xp_ledger_reference_type_check")
    op.execute(f"""
        ALTER TABLE xp_ledger
        ADD CONSTRAINT xp_ledger_reference_type_check
        CHECK (reference_type IN ({_values(_REFERENCE_TYPES_NEW)}))
    """)


def downgrade() -> None:
    _drop_constraint("xp_ledger", "xp_ledger_action_type_check")
    op.execute(f"""
        ALTER TABLE xp_ledger
        ADD CONSTRAINT xp_ledger_action_type_check
        CHECK (action_type IN ({_values(_ACTION_TYPES_OLD)}))
    """)

    _drop_constraint("xp_ledger", "xp_ledger_reference_type_check")
    op.execute(f"""
        ALTER TABLE xp_ledger
        ADD CONSTRAINT xp_ledger_reference_type_check
        CHECK (reference_type IN ({_values(_REFERENCE_TYPES_OLD)}))
    """)
