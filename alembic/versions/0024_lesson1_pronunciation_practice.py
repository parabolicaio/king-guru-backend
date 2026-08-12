"""Lesson 1 Pronunciation — add 4 pronunciation_practice assessment questions.

Appends graded pronunciation questions to the existing Pronunciation section
of Lesson 1 (Beginner A). The content blocks (headings + phrase cards) are
already present from 0020; these questions follow at display orders 11–14.

  11 — Stress & Intonation : "How are you?"
  12 — Syllables           : "Afternoon"
  13 — Breath Sound        : "Hello"
  14 — Breath Sound        : "Hi"

Revision ID: d1e2f3a4b5c6
Revises:     a1b2c3d4e6f7
Create Date: 2026-06-21
"""
from typing import Sequence, Union

from alembic import op
from seed_helpers import insert_question
from sqlalchemy import text

revision: str = "d1e2f3a4b5c6"
down_revision: Union[str, None] = "d4e5f6a7b8c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    # Locate the pronunciation section for Lesson 1, Beginner A
    row = bind.execute(text("""
        SELECT ls.id::text
        FROM lesson_section ls
        JOIN lesson l ON l.id = ls.lesson_id
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a'
          AND l.lesson_order = 1
          AND ls.category = 'pronunciation'
    """)).fetchone()
    assert row, "Lesson 1 pronunciation section not found — run 0020 first"
    pron_sec_id = row[0]

    # ── A. Stress & Intonation ────────────────────────────────────────────────
    insert_question(
        pron_sec_id,
        "pronunciation_practice",
        "assessment",
        11,
        "Say the sentence. Let your voice rise at the end.",
        {
            "target_text": "How are you?",
            "show_text_before_record": True,
            "max_duration_seconds": 10,
            "feedback": {
                "correct": "Great! Your intonation rose naturally at the end.",
                "incorrect": "Try again — let your voice go up when you say 'you'.",
            },
        },
        15,
        str(uuid7()),
    )

    # ── B. Syllables ──────────────────────────────────────────────────────────
    insert_question(
        pron_sec_id,
        "pronunciation_practice",
        "assessment",
        12,
        "Say the word slowly — three clear beats: Af · ter · noon.",
        {
            "target_text": "Afternoon",
            "show_text_before_record": True,
            "max_duration_seconds": 10,
            "feedback": {
                "correct": "Well done! Each syllable came through clearly.",
                "incorrect": "Take it slow — say each part: Af … ter … noon.",
            },
        },
        15,
        str(uuid7()),
    )

    # ── C. Breath Sounds — Hello ──────────────────────────────────────────────
    insert_question(
        pron_sec_id,
        "pronunciation_practice",
        "assessment",
        13,
        "Say this word with a strong breath at the 'H'.",
        {
            "target_text": "Hello",
            "show_text_before_record": True,
            "max_duration_seconds": 8,
            "feedback": {
                "correct": "Nice! The 'H' breath was clear.",
                "incorrect": "Push a strong breath out as you start — 'Hhhello'.",
            },
        },
        15,
        str(uuid7()),
    )

    # ── C. Breath Sounds — Hi ─────────────────────────────────────────────────
    insert_question(
        pron_sec_id,
        "pronunciation_practice",
        "assessment",
        14,
        "Say this word — short and soft.",
        {
            "target_text": "Hi",
            "show_text_before_record": True,
            "max_duration_seconds": 8,
            "feedback": {
                "correct": "Perfect — short and crisp!",
                "incorrect": "Keep it short — just a quick, light 'Hi'.",
            },
        },
        15,
        str(uuid7()),
    )


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT ls.id::text
        FROM lesson_section ls
        JOIN lesson l ON l.id = ls.lesson_id
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a'
          AND l.lesson_order = 1
          AND ls.category = 'pronunciation'
    """)).fetchone()
    if not row:
        return

    op.execute(f"""
        DELETE FROM question
        WHERE lesson_section_id = '{row[0]}'
          AND type = 'pronunciation_practice'
          AND display_order BETWEEN 11 AND 14
    """)
