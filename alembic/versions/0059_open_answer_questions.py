"""Open fill-in questions accept any real answer (D-72).

Lesson 1 Writing asks "I am from ____." but only accepted "Sri Lanka", so
learners who wrote their town ("Kandy") were marked wrong. This sets
payload.accept_any on that question (scoring then accepts any answer with
at least two letters) and rewords its feedback. The original feedback is
kept in payload.original_feedback for downgrade.

Revision ID: 5d6e7f8a9b0c
Revises:     4c5d6e7f8a9b
Create Date: 2026-10-28
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "5d6e7f8a9b0c"
down_revision: Union[str, None] = "4c5d6e7f8a9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Open questions: any place, name or answer of the learner's own is right.
OPEN_PROMPTS = ["I am from ____."]

NEW_FEEDBACK = {
    "correct": "Good! You said where you are from, e.g. 'I am from Kandy.'",
    "incorrect": "Write the name of your town or country, e.g. 'Sri Lanka' or 'Kandy'.",
}


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, payload FROM question "
            "WHERE type = 'fill_blank_typed' AND prompt_text = ANY(:prompts) "
            "AND NOT (payload ? 'accept_any')"
        ),
        {"prompts": OPEN_PROMPTS},
    ).mappings().all()
    for row in rows:
        payload = row["payload"] if isinstance(row["payload"], dict) else json.loads(row["payload"])
        payload = dict(payload)
        payload["original_feedback"] = payload.get("feedback")
        payload["feedback"] = NEW_FEEDBACK
        payload["accept_any"] = True
        bind.execute(
            sa.text("UPDATE question SET payload = CAST(:p AS jsonb), updated_at = now() WHERE id = :id"),
            {"p": json.dumps(payload), "id": row["id"]},
        )


def downgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text("SELECT id, payload FROM question WHERE payload ? 'accept_any' AND payload ? 'original_feedback'")
    ).mappings().all()
    for row in rows:
        payload = row["payload"] if isinstance(row["payload"], dict) else json.loads(row["payload"])
        payload = dict(payload)
        payload.pop("accept_any", None)
        original = payload.pop("original_feedback", None)
        if original is not None:
            payload["feedback"] = original
        bind.execute(
            sa.text("UPDATE question SET payload = CAST(:p AS jsonb), updated_at = now() WHERE id = :id"),
            {"p": json.dumps(payload), "id": row["id"]},
        )
