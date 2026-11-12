"""Level 3 (Intermediate, B1) lessons.

Content is in seed_level3/ (one data file per lesson, built by
seed_level3/build.py) from the experts' solo versions in
'Lesson Contents/Kingguru L3 Activities'. The team's suggested solo lines
(follow-up Parts C and D) are applied, and answer keys or model answers
written by the King Guru team carry payload.needs_expert_review = true.

Adds each lesson to the 'intermediate' level (approved), with its seven
sections. A lesson or section that already exists keeps its content, so
this is safe to re-run.

Revision ID: e67a1b2c3d4f
Revises:     d66f0a1b2c3e
Create Date: 2026-11-04
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from uuid6 import uuid7

from seed_level3 import load_lessons
from seed_level3.build import build_lesson

revision: str = "e67a1b2c3d4f"
down_revision: Union[str, None] = "d66f0a1b2c3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LEVEL_CODE = "intermediate"


def _j(v) -> str:
    return json.dumps(v, ensure_ascii=False)


def _lesson_id(bind, level_id: str, spec: dict) -> str:
    row = bind.execute(sa.text(
        "SELECT id::text FROM lesson WHERE level_id = :lv AND lesson_order = :o AND deleted_at IS NULL"
    ), {"lv": level_id, "o": spec["order"]}).fetchone()
    if row:
        return row[0]
    lid = str(uuid7())
    bind.execute(sa.text(
        "INSERT INTO lesson (id, level_id, lesson_order, title, description, status, is_guest_accessible, "
        "objectives, objectives_translations, translations) VALUES (:id, :lv, :o, :t, :d, 'approved', FALSE, "
        "CAST(:obj AS jsonb), '{}'::jsonb, CAST(:tr AS jsonb))"
    ), {"id": lid, "lv": level_id, "o": spec["order"], "t": spec["title"], "d": spec["description"],
        "obj": _j(spec["objectives"]),
        "tr": _j({"si": {"title": spec["title_si"]}} if spec.get("title_si") else {})})
    return lid


def _section_id(bind, lesson_id: str, sec: dict) -> tuple[str, bool]:
    """(section id, whether it already had content)."""
    row = bind.execute(sa.text(
        "SELECT id::text FROM lesson_section WHERE lesson_id = :l AND category = :c"
    ), {"l": lesson_id, "c": sec["category"]}).fetchone()
    if row:
        has = bind.execute(sa.text(
            "SELECT EXISTS (SELECT 1 FROM content_block WHERE lesson_section_id = :s) "
            "OR EXISTS (SELECT 1 FROM question WHERE lesson_section_id = :s)"
        ), {"s": row[0]}).scalar()
        return row[0], bool(has)
    sid = str(uuid7())
    bind.execute(sa.text(
        "INSERT INTO lesson_section (id, lesson_id, category, display_order, title) VALUES (:id, :l, :c, :o, :t)"
    ), {"id": sid, "l": lesson_id, "c": sec["category"], "o": sec["display_order"], "t": sec["title"]})
    return sid, False


def _insert_rows(bind, section_id: str, rows: list[dict]) -> None:
    for r in rows:
        if r["t"] == "block":
            bind.execute(sa.text(
                "INSERT INTO content_block (id, lesson_section_id, block_type, display_order, payload) "
                "VALUES (:id, :s, :bt, :o, CAST(:p AS jsonb))"
            ), {"id": str(uuid7()), "s": section_id, "bt": r["block_type"], "o": r["order"], "p": _j(r["payload"])})
        elif r["t"] == "word":
            wid = str(uuid7())
            bind.execute(sa.text(
                "INSERT INTO vocabulary_word (id, lesson_section_id, word, definition, example_sentence, "
                "difficulty, translations) VALUES (:id, :s, :w, :d, NULL, 'medium', CAST(:tr AS jsonb))"
            ), {"id": wid, "s": section_id, "w": r["word"], "d": r["definition"],
                "tr": _j({"si": {"word": r["si"]}} if r["si"] else {})})
            bind.execute(sa.text(
                "INSERT INTO content_block (id, lesson_section_id, block_type, display_order, payload) "
                "VALUES (:id, :s, 'word_card', :o, CAST(:p AS jsonb))"
            ), {"id": str(uuid7()), "s": section_id, "o": r["order"], "p": _j({"vocabulary_word_id": wid})})
        else:
            bind.execute(sa.text(
                "INSERT INTO question (id, lesson_section_id, type, purpose, display_order, prompt_text, "
                "payload, xp_value) VALUES (:id, :s, :t, 'assessment', :o, :pr, CAST(:p AS jsonb), :xp)"
            ), {"id": str(uuid7()), "s": section_id, "t": r["type"], "o": r["order"], "pr": r["prompt"],
                "p": _j(r["payload"]), "xp": r["xp"]})


QUESTION_TYPES = [
    "mcq_single", "mcq_long_short_form", "fill_blank_typed", "fill_blank_options", "match_pairs",
    "true_false", "order_events", "sentence_builder", "correct_mistake", "audio_mcq",
    "audio_image_select", "audio_fill_blank", "reading_passage_mcq", "reading_passage_short_answer",
    "pronunciation_practice", "picture_speak_target", "free_speak", "picture_describe",
    # Scored and shown by both apps, but never allowed for lesson questions until now.
    "categorization", "guided_writing",
]


def upgrade() -> None:
    bind = op.get_bind()
    types = ", ".join(f"'{t}'" for t in QUESTION_TYPES)
    op.execute("ALTER TABLE question DROP CONSTRAINT IF EXISTS question_type_check")
    op.execute(f"ALTER TABLE question ADD CONSTRAINT question_type_check CHECK (type IN ({types}))")
    level =bind.execute(sa.text("SELECT id::text FROM level WHERE code = :c"), {"c": LEVEL_CODE}).fetchone()
    if not level:
        return
    for spec in load_lessons():
        lesson_id = _lesson_id(bind, level[0], spec)
        for sec in build_lesson(spec):
            section_id, has_content = _section_id(bind, lesson_id, sec)
            if not has_content:
                _insert_rows(bind, section_id, sec["rows"])


def downgrade() -> None:
    # Learners may have progress in these lessons; leave them.
    pass
