"""Seed daily goal templates — one per (level, goal_type).

46 rows total:
  Beginner A/B  — 7 types each (no essay_submitted, daily_essay_enabled=FALSE)
  Elementary+   — 8 types each

Level IDs are looked up by code at migration time so this migration is
portable across environments.

Revision ID: f5a6b7c8d9e0
Revises:     e4f5a6b7c8d9
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid6 import uuid7

revision: str = "f5a6b7c8d9e0"
down_revision: Union[str, None] = "e4f5a6b7c8d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ---------------------------------------------------------------------------
# Template definitions
# Each row: (goal_type, title, target_per_level, xp_reward_per_level)
# Indices align with LEVELS list order: beg_a, beg_b, elem, inter, upper, adv
# A target of 0 means "skip this level for this type".
# ---------------------------------------------------------------------------

LEVELS = [
    "beginner_a",
    "beginner_b",
    "elementary",
    "intermediate",
    "upper_intermediate",
    "advanced",
]

TEMPLATES = [
    # (goal_type, title_template, [targets], [xp_rewards])
    (
        "questions_answered",
        "Answer {n} questions today",
        [10, 10, 15, 20, 25, 30],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "correct_answers",
        "Get {n} correct answers today",
        [6, 6, 10, 15, 18, 22],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "assessment_questions_answered",
        "Complete {n} graded questions today",
        [8, 8, 12, 15, 20, 25],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "lesson_sections_completed",
        "Complete {n} lesson {section} today",
        [1, 1, 2, 2, 3, 3],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "lessons_completed",
        "Complete {n} {lesson} today",
        [1, 1, 1, 1, 2, 2],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "essay_submitted",
        "Submit today's essay",
        [0, 0, 1, 1, 1, 1],   # 0 = skip Beginner A/B
        [0, 0, 30, 40, 50, 60],
    ),
    (
        "words_learned",
        "Master {n} vocabulary {word} today",
        [2, 2, 3, 4, 5, 6],
        [20, 20, 30, 40, 50, 60],
    ),
    (
        "xp_earned",
        "Earn {n} XP today",
        [50, 50, 80, 120, 150, 180],
        [20, 20, 30, 40, 50, 60],
    ),
]


def _title(goal_type: str, template: str, n: int) -> str:
    """Render a human-readable goal title with correct pluralisation."""
    if goal_type == "lesson_sections_completed":
        return template.format(n=n, section="section" if n == 1 else "sections")
    if goal_type == "lessons_completed":
        return template.format(n=n, lesson="lesson" if n == 1 else "lessons")
    if goal_type == "words_learned":
        return template.format(n=n, word="word" if n == 1 else "words")
    if goal_type == "essay_submitted":
        return template  # no {n}
    return template.format(n=n)


def upgrade() -> None:
    conn = op.get_bind()

    for level_code in LEVELS:
        level_row = conn.execute(
            sa.text("SELECT id FROM level WHERE code = :code"),
            {"code": level_code},
        ).fetchone()
        if level_row is None:
            raise RuntimeError(f"Level '{level_code}' not found — run 0002_seed_data first")
        level_id = str(level_row[0])
        level_idx = LEVELS.index(level_code)

        for goal_type, title_tpl, targets, xp_rewards in TEMPLATES:
            target = targets[level_idx]
            xp_reward = xp_rewards[level_idx]

            if target == 0:
                continue  # skip (e.g. essay for Beginner A/B)

            title = _title(goal_type, title_tpl, target)
            row_id = str(uuid7())

            conn.execute(
                sa.text("""
                    INSERT INTO daily_goal
                        (id, level_id, goal_type, title, target_value, xp_reward,
                         is_active, translations, created_at, updated_at)
                    VALUES (
                        :id, :level_id, :goal_type, :title,
                        :target, :xp_reward,
                        TRUE, '{}', now(), now()
                    )
                    ON CONFLICT DO NOTHING
                """),
                {
                    "id": row_id,
                    "level_id": level_id,
                    "goal_type": goal_type,
                    "title": title,
                    "target": target,
                    "xp_reward": xp_reward,
                },
            )


def downgrade() -> None:
    op.execute("DELETE FROM daily_goal")
