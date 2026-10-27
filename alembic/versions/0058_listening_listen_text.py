"""Move the spoken line of listening questions out of the question text (D-08).

Listening questions were seeded as "<what you hear> <question>", e.g.
"My name is Kamal. What is his name?", so the answer was printed on screen
and there was nothing to listen to. This moves the heard part into
payload.listen_text (the app plays it with a Play button) and leaves only
the question in prompt_text.

Only questions in listening sections that clearly have that shape are
changed; True/False claims and questions with no heard part are left as
they are. The original text is kept in payload.original_prompt_text so
downgrade can restore it.

Revision ID: 4c5d6e7f8a9b
Revises:     3b4c5d6e7f8a
Create Date: 2026-10-28
"""
import json
import re
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "4c5d6e7f8a9b"
down_revision: Union[str, None] = "3b4c5d6e7f8a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_QUOTES = "'‘’\""

# "'Where is your book?' — choose the correct answer."
_QUOTED_THEN_INSTRUCTION = re.compile(
    r"^[" + _QUOTES + r"](?P<heard>[^" + _QUOTES + r"]+)[" + _QUOTES + r"]\s*[—–-]\s*(?P<ask>.+)$"
)
# "My name is Kamal. What is his name?"  /  "Anna says: 'I like tea.' Who likes tea?"
_STATEMENT_THEN_QUESTION = re.compile(
    r"^(?P<heard>.*[.!][" + _QUOTES + r"]?)\s+(?P<ask>[^.!?]+\?)$"
)


def split_listening_prompt(prompt: str) -> tuple[str, str] | None:
    """Return (listen_text, question) or None when the prompt has no heard part."""
    text = (prompt or "").strip()
    if not text:
        return None

    m = _QUOTED_THEN_INSTRUCTION.match(text)
    if m:
        heard, ask = m.group("heard").strip(), m.group("ask").strip()
    else:
        m = _STATEMENT_THEN_QUESTION.match(text)
        if not m:
            return None
        heard, ask = m.group("heard").strip(), m.group("ask").strip()
        if ask.lower().rstrip("?").strip() == "true or false":
            return None  # the statement is the claim to judge, not audio

    heard = re.sub(r"[" + _QUOTES + r"]", "", heard).strip()
    if not heard or not ask:
        return None
    return heard, ask[0].upper() + ask[1:]


_SELECT = sa.text(
    """
    SELECT q.id, q.type, q.prompt_text, q.payload, q.translations
    FROM question q
    JOIN lesson_section ls ON ls.id = q.lesson_section_id
    WHERE ls.category = 'listening'
      AND q.type IN ('mcq_single', 'mcq_long_short_form', 'fill_blank_options')
      AND NOT (q.payload ? 'listen_text')
    """
)


def _as_dict(value) -> dict:
    if value is None:
        return {}
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def upgrade() -> None:
    bind = op.get_bind()
    for row in bind.execute(_SELECT).mappings().all():
        split = split_listening_prompt(row["prompt_text"])
        if split is None:
            continue
        heard, ask = split
        payload = _as_dict(row["payload"])
        payload["listen_text"] = heard
        payload["original_prompt_text"] = row["prompt_text"]

        translations = _as_dict(row["translations"])
        si = translations.get("si")
        if isinstance(si, dict) and si.get("prompt_text"):
            si_split = split_listening_prompt(si["prompt_text"])
            if si_split is not None:
                payload["original_prompt_text_si"] = si["prompt_text"]
                si["prompt_text"] = si_split[1]

        bind.execute(
            sa.text(
                "UPDATE question SET prompt_text = :ask, payload = CAST(:payload AS jsonb), "
                "translations = CAST(:translations AS jsonb), updated_at = now() WHERE id = :id"
            ),
            {
                "ask": ask,
                "payload": json.dumps(payload),
                "translations": json.dumps(translations),
                "id": row["id"],
            },
        )


def downgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, payload, translations FROM question "
            "WHERE payload ? 'original_prompt_text'"
        )
    ).mappings().all()
    for row in rows:
        payload = _as_dict(row["payload"])
        original = payload.pop("original_prompt_text")
        payload.pop("listen_text", None)
        translations = _as_dict(row["translations"])
        original_si = payload.pop("original_prompt_text_si", None)
        if original_si and isinstance(translations.get("si"), dict):
            translations["si"]["prompt_text"] = original_si
        bind.execute(
            sa.text(
                "UPDATE question SET prompt_text = :p, payload = CAST(:payload AS jsonb), "
                "translations = CAST(:translations AS jsonb), updated_at = now() WHERE id = :id"
            ),
            {"p": original, "payload": json.dumps(payload),
             "translations": json.dumps(translations), "id": row["id"]},
        )
