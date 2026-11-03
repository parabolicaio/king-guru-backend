"""Convert chips/correct_sequence sentence builders to the current shape (D-77).

Lesson 2 Grammar's 'Arrange the words' question (seeded in 0002) uses
    {chips: [{id, text}], correct_sequence: [ids]}
which no layer reads, so the app shows no word chips and Check stays off.
0048 converted the other old shape ({words: [...]}) but not this one.

This rewrites it to {items, distractors, correct_order, feedback}: chips in
correct_sequence become items (in that order), the rest become
distractors. Rows already in the current shape are skipped, so a re-run
does nothing.

Revision ID: 8a9b0c1d2e3f
Revises:     7f8a9b0c1d2e
Create Date: 2026-11-04
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "8a9b0c1d2e3f"
down_revision: Union[str, None] = "7f8a9b0c1d2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def convert(payload: dict) -> dict:
    chips = {str(c["id"]): str(c.get("text", "")) for c in payload.get("chips") or [] if c.get("id")}
    sequence = [str(i) for i in payload.get("correct_sequence") or [] if str(i) in chips]
    items = [{"id": i, "text": chips[i]} for i in sequence]
    distractors = [{"id": i, "text": t} for i, t in chips.items() if i not in sequence]
    return {
        "items": items,
        "distractors": distractors,
        "correct_order": sequence,
        "feedback": payload.get("feedback", {}),
    }


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, payload FROM question "
            "WHERE type = 'sentence_builder' "
            "AND jsonb_exists(payload, 'chips') "
            "AND NOT jsonb_exists(payload, 'correct_order')"
        )
    ).fetchall()
    for qid, raw in rows:
        payload = raw if isinstance(raw, dict) else json.loads(raw)
        bind.execute(
            sa.text("UPDATE question SET payload = CAST(:p AS jsonb), updated_at = now() WHERE id = :id"),
            {"p": json.dumps(convert(payload), ensure_ascii=False), "id": qid},
        )


def downgrade() -> None:
    # The old shape never worked, so there is nothing to restore.
    pass
