"""Convert legacy sentence_builder payloads to the canonical id-based shape.

Production review Defect 4: Lesson 5's sentence_builder questions
(seeded in 0018_lesson5_full.py) use a pre-rework payload
    {words:[...], distractors:[...], correct_answer:"..."}
that NO layer reads:
  - scoring.py reads `correct_order` (absent) → denominator 0 → is_correct=(0==0)
    → every answer scored "correct" at a 0.00 fraction;
  - both clients read `items`/`correct_order` (absent) → an unbuildable board.
So these questions are live-but-broken.

This rewrites every sentence_builder whose payload still carries the legacy
`words` key into the shape the engine + both renderers use:
    {items:[{id,text}], distractors:[{id,text}], correct_order:[ids], feedback}
`words` is already in the correct order, so correct_order = the item ids in
sequence; the legacy text `distractors` become {id,text} chips (ids d1..dN) that
sit outside correct_order. Keyed by payload shape (not lesson) so any straggler
elsewhere is fixed too; the WHERE clause skips already-converted rows, so a
re-run is a no-op.

Downgrade is a deliberate no-op: the legacy shape is non-functional, converted
rows can't be cleanly distinguished from natively-authored id-based questions
afterward, and reverting would only re-break the content (same
one-way-content-normalisation rationale as 0042_shuffle_mcq_options).

Revision ID: 48d1e2f3a4b5
Revises:     c5d6e7f8a9b0
Create Date: 2026-08-01
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "48d1e2f3a4b5"
down_revision: Union[str, None] = "c5d6e7f8a9b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, payload FROM question "
            "WHERE type = 'sentence_builder' "
            "AND jsonb_exists(payload, 'words') "
            "AND NOT jsonb_exists(payload, 'correct_order')"
        )
    ).fetchall()

    for row in rows:
        qid = row[0]
        raw = row[1]
        payload = raw if isinstance(raw, dict) else json.loads(raw)

        words = payload.get("words") or []
        distractors = payload.get("distractors") or []

        items = [{"id": f"c{i + 1}", "text": str(w)} for i, w in enumerate(words)]
        correct_order = [f"c{i + 1}" for i in range(len(words))]
        dist_items = [{"id": f"d{i + 1}", "text": str(w)} for i, w in enumerate(distractors)]

        new_payload = {
            "items": items,
            "distractors": dist_items,
            "correct_order": correct_order,
            "feedback": payload.get("feedback", {}),
        }
        op.execute(
            f"UPDATE question SET payload = {_j(new_payload)}, updated_at = now() "
            f"WHERE id = '{qid}'"
        )


def downgrade() -> None:
    # Deliberate no-op — see module docstring. Normalising broken legacy content
    # to the working shape is one-way; reverting would only re-break it.
    pass
