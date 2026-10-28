"""Fill lesson objectives from each lesson's intro card (D-38).

Lessons were seeded with their objectives as a text card ("By the end of
this lesson you will be able to: ...") but the lesson.objectives field
stayed empty, so the overview had nothing to show. This copies them into
lesson.objectives as a list, for lessons whose objectives are still empty.
The card itself is left as it is. Sinhala objectives still need a
translator (objectives_translations is not touched).

Revision ID: 6e7f8a9b0c1d
Revises:     5d6e7f8a9b0c
Create Date: 2026-10-28
"""
import json
import re
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "6e7f8a9b0c1d"
down_revision: Union[str, None] = "5d6e7f8a9b0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_PREFIX = re.compile(r"^\s*By the end of this lesson,? you will be able to\s*", re.IGNORECASE)


def _clean(item: str) -> str:
    item = re.sub(r"\*+", "", item).strip().rstrip(".").strip()
    item = re.sub(r"^(and|or)\s+", "", item, flags=re.IGNORECASE)
    return item[:1].upper() + item[1:] if item else ""


def parse_objectives(text: str) -> list[str]:
    """Turn an intro card's text into a list of objectives ([] if it isn't one)."""
    if not text or not _PREFIX.match(text):
        return []
    rest = _PREFIX.sub("", text, count=1)

    # Bullet list: "...able to:\n\n- Do this\n- Do that"
    bullets = [line.strip()[2:] for line in rest.splitlines() if line.strip().startswith("- ")]
    if bullets:
        return [c for c in (_clean(b) for b in bullets) if c]

    # Single sentence without a colon: one objective.
    if not rest.startswith(":"):
        one = _clean(rest)
        return [one] if one else []

    # Comma list: "...able to: greet people, say your name, and introduce yourself."
    parts = [p.strip() for p in rest[1:].split(",")]
    merged: list[str] = []
    for part in parts:
        # A short fragment is part of the item before it ("in, on and under").
        if merged and len(part.split()) <= 3 and not part.lower().startswith("and "):
            merged[-1] = f"{merged[-1]}, {part}"
        else:
            merged.append(part)
    return [c for c in (_clean(p) for p in merged) if c]


_FIND = sa.text(
    """
    SELECT DISTINCT ON (l.id) l.id AS lesson_id, cb.payload
    FROM lesson l
    JOIN lesson_section ls ON ls.lesson_id = l.id
    JOIN content_block cb ON cb.lesson_section_id = ls.id
    WHERE l.deleted_at IS NULL
      AND l.objectives = '[]'::jsonb
      AND cb.payload->>'text' ILIKE 'By the end of this lesson%'
    ORDER BY l.id, ls.display_order, cb.display_order
    """
)


def upgrade() -> None:
    bind = op.get_bind()
    for row in bind.execute(_FIND).mappings().all():
        payload = row["payload"] if isinstance(row["payload"], dict) else json.loads(row["payload"])
        objectives = parse_objectives(str(payload.get("text") or ""))
        if not objectives:
            continue
        bind.execute(
            sa.text(
                "UPDATE lesson SET objectives = CAST(:o AS jsonb), updated_at = now() "
                "WHERE id = :id AND objectives = '[]'::jsonb"
            ),
            {"o": json.dumps(objectives), "id": row["lesson_id"]},
        )


def downgrade() -> None:
    # Not reversible safely: objectives may have been edited since. No-op.
    pass
