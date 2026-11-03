"""Give two Lesson 1 Grammar questions exactly one right option (D-82).

'I am ___ Sri Lanka.' offered from / to / in, but 'I am in Sri Lanka' is
also good English. 'Nice to ___ you.' offered meet / see / talk, and
'Nice to see you' is good English too. Both marked the second valid
answer wrong. The extra right answer is swapped for a clearly wrong one:
'in' -> 'at', 'see' -> 'go'.

Options were shuffled and relabelled by 0042, so they are matched by
text, not id. Questions already changed are left alone.

Revision ID: b64d82e1a7c3
Revises:     9b0c1d2e3f4a
Create Date: 2026-11-04
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b64d82e1a7c3"
down_revision: Union[str, None] = "9b0c1d2e3f4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# prompt -> (option text to replace, replacement)
SWAPS = {
    "I am ___ Sri Lanka.": ("in", "at"),
    "Nice to ___ you.": ("see", "go"),
}


def swap_option(payload: dict, old: str, new: str) -> dict | None:
    """Payload with the option `old` renamed to `new`, or None if no change.

    The right answer is never touched.
    """
    options = payload.get("options") or []
    correct = payload.get("correct_option_id")
    changed = False
    out = []
    for o in options:
        if o.get("text", "").strip().lower() == old and o.get("id") != correct:
            o = {**o, "text": new}
            changed = True
        out.append(o)
    return {**payload, "options": out} if changed else None


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, prompt_text, payload FROM question "
            "WHERE type = 'fill_blank_options' AND prompt_text = ANY(:p)"
        ),
        {"p": list(SWAPS)},
    ).fetchall()
    for qid, prompt, raw in rows:
        payload = raw if isinstance(raw, dict) else json.loads(raw)
        old, new = SWAPS[prompt]
        updated = swap_option(payload, old, new)
        if updated is None:
            continue
        bind.execute(
            sa.text("UPDATE question SET payload = CAST(:p AS jsonb), updated_at = now() WHERE id = :id"),
            {"p": json.dumps(updated, ensure_ascii=False), "id": qid},
        )


def downgrade() -> None:
    pass
