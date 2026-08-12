"""Shared helpers for Phase 1 seed migrations (0014–0018).

Alembic adds the versions/ directory to sys.path, so this module is importable
from any migration file in that directory without a package prefix.
"""
import json

from alembic import op
from sqlalchemy import text


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def ensure_lesson(
    bind,
    level_id: str,
    lesson_order: int,
    title: str,
    description: str,
    new_id: str,
) -> str:
    row = bind.execute(
        text("SELECT id::text FROM lesson WHERE level_id = :lid AND lesson_order = :lo"),
        {"lid": level_id, "lo": lesson_order},
    ).fetchone()
    if row:
        return str(row[0])
    op.execute(
        f"INSERT INTO lesson "
        f"(id, level_id, lesson_order, title, description, status, is_guest_accessible) "
        f"VALUES ('{new_id}', '{level_id}', {lesson_order}, {_s(title)}, "
        f"{_s(description)}, 'approved', FALSE)"
    )
    return new_id


def ensure_section(
    bind,
    lesson_id: str,
    category: str,
    display_order: int,
    title: str,
    new_id: str,
) -> str:
    row = bind.execute(
        text(
            "SELECT id::text FROM lesson_section "
            "WHERE lesson_id = :lid AND category = :cat"
        ),
        {"lid": lesson_id, "cat": category},
    ).fetchone()
    if row:
        return str(row[0])
    op.execute(
        f"INSERT INTO lesson_section (id, lesson_id, category, display_order, title) "
        f"VALUES ('{new_id}', '{lesson_id}', {_s(category)}, {display_order}, {_s(title)})"
    )
    return new_id


def insert_content_block(
    section_id: str,
    block_type: str,
    display_order: int,
    payload: dict,
    new_id: str,
) -> None:
    op.execute(
        f"INSERT INTO content_block "
        f"(id, lesson_section_id, block_type, display_order, payload) "
        f"VALUES ('{new_id}', '{section_id}', {_s(block_type)}, {display_order}, {_j(payload)})"
    )


def insert_question(
    section_id: str,
    question_type: str,
    purpose: str,
    display_order: int,
    stem: str,
    payload: dict,
    xp_value: int,
    new_id: str,
) -> None:
    op.execute(
        f"INSERT INTO question "
        f"(id, lesson_section_id, type, purpose, display_order, prompt_text, payload, xp_value) "
        f"VALUES ('{new_id}', '{section_id}', {_s(question_type)}, {_s(purpose)}, "
        f"{display_order}, {_s(stem)}, {_j(payload)}, {xp_value})"
    )


def insert_word_card(
    bind,
    section_id: str,
    display_order: int,
    word: str,
    definition: str,
    example: str,
    cb_id: str,
    ww_id: str,
) -> None:
    op.execute(
        f"INSERT INTO vocabulary_word "
        f"(id, lesson_section_id, word, definition, example_sentence, difficulty) "
        f"VALUES ('{ww_id}', '{section_id}', {_s(word)}, {_s(definition)}, "
        f"{_s(example)}, 'easy')"
    )
    insert_content_block(
        section_id,
        "word_card",
        display_order,
        {"vocabulary_word_id": ww_id},
        cb_id,
    )


def insert_word_card_tr(
    bind,
    section_id: str,
    display_order: int,
    word: str,
    definition: str,
    example: str,
    cb_id: str,
    ww_id: str,
    word_si: str | None = None,
    difficulty: str = "easy",
) -> None:
    """insert_word_card variant carrying a Sinhala translation.

    The Sinhala gloss is stored as {"si": {"word": ...}} — the shape the admin
    vocabulary API reads (see app/api/v1/admin/vocabulary_words.py). Used by the
    Level 2 (beginner_b) seeds, whose source .docx files ship clean Sinhala.
    """
    tr = {"si": {"word": word_si}} if word_si else {}
    op.execute(
        f"INSERT INTO vocabulary_word "
        f"(id, lesson_section_id, word, definition, example_sentence, difficulty, translations) "
        f"VALUES ('{ww_id}', '{section_id}', {_s(word)}, {_s(definition)}, "
        f"{_s(example)}, {_s(difficulty)}, {_j(tr)})"
    )
    insert_content_block(
        section_id,
        "word_card",
        display_order,
        {"vocabulary_word_id": ww_id},
        cb_id,
    )
