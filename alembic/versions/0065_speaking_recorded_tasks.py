"""Speaking sections get recorded, graded tasks (D-84).

Every Speaking section was content only: a 'Repeat After Me' list and a
challenge, then 'Section complete' with nothing recorded. This adds a
pronunciation_practice question (record, then graded like Pronunciation)
for each phrase card, and for each question-and-answer card (the learner
answers out loud, with the model answer as the target). Sections that
already have questions are left alone.

Runs after 0063, so Lessons 2-5's new Speaking sections are included.

Revision ID: c75e84f2b9d1
Revises:     b64d82e1a7c3
Create Date: 2026-11-04
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from uuid6 import uuid7

revision: str = "c75e84f2b9d1"
down_revision: Union[str, None] = "b64d82e1a7c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

MAX_TASKS = 6

_FEEDBACK = {
    "correct": "Great speaking! That was clear.",
    "incorrect": "Try again — say each word slowly and clearly.",
}


def plan_tasks(blocks: list[dict]) -> list[tuple[str, str]]:
    """(prompt, target sentence) for each speaking task, from the section's
    content blocks in display order. Duplicates are dropped; at most
    MAX_TASKS."""
    tasks: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(prompt: str, target: str | None) -> None:
        target = (target or "").strip()
        if not target or target.lower() in seen or len(tasks) >= MAX_TASKS:
            return
        seen.add(target.lower())
        tasks.append((prompt, target))

    for b in blocks:
        kind = b.get("type")
        if kind == "phrase_card":
            add("Say it out loud.", b.get("text"))
        elif kind == "qa_pair":
            q = (b.get("question") or "").strip()
            add(f"Answer out loud: '{q}'" if q else "Say the answer out loud.", b.get("answer"))
    return tasks


_SECTIONS = sa.text(
    """
    SELECT ls.id
    FROM lesson_section ls
    JOIN lesson l ON l.id = ls.lesson_id
    WHERE ls.category = 'speaking' AND l.deleted_at IS NULL
      AND NOT EXISTS (SELECT 1 FROM question q WHERE q.lesson_section_id = ls.id)
    """
)
_BLOCKS = sa.text(
    "SELECT display_order, payload FROM content_block "
    "WHERE lesson_section_id = :s ORDER BY display_order"
)


def upgrade() -> None:
    bind = op.get_bind()
    for (section_id,) in bind.execute(_SECTIONS).fetchall():
        rows = bind.execute(_BLOCKS, {"s": section_id}).fetchall()
        blocks = [r[1] if isinstance(r[1], dict) else json.loads(r[1]) for r in rows]
        start = (max((r[0] for r in rows), default=-1)) + 1
        for i, (prompt, target) in enumerate(plan_tasks(blocks)):
            payload = {
                "target_text": target,
                "show_text_before_record": True,
                "max_duration_seconds": 15,
                "feedback": _FEEDBACK,
            }
            bind.execute(
                sa.text(
                    "INSERT INTO question (id, lesson_section_id, type, purpose, display_order, "
                    "prompt_text, payload, xp_value) VALUES (:id, :s, 'pronunciation_practice', "
                    "'assessment', :d, :p, CAST(:payload AS jsonb), 15)"
                ),
                {"id": str(uuid7()), "s": section_id, "d": start + i, "p": prompt,
                 "payload": json.dumps(payload, ensure_ascii=False)},
            )


def downgrade() -> None:
    # Learners may have recordings against these; leave them.
    pass
