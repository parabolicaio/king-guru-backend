"""Lesson 1 content enrichment — 10 missing vocabulary words, Short Forms grammar
block, 12 assessment questions (fill_blank_options + mcq_long_short_form), 3 Extra
Practice questions, and a self_check block.

All content derived from docs/lesson-samples/lesson 1.pdf.  Phase 2+ sections
(Pronunciation, Listening, Reading, Speaking, Writing) are deferred.

Revision ID: 8c7b6a5d4e3f
Revises:     9b8a7c6d5e4f
Create Date: 2026-06-09
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import insert_content_block, insert_question, insert_word_card
from sqlalchemy import text

revision: str = "8c7b6a5d4e3f"
down_revision: Union[str, None] = "9b8a7c6d5e4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _get_section_ids(bind):
    """Return (l1_vocab_sec_id, l1_gram_sec_id) for Beginner A Lesson 1."""
    row = bind.execute(text("""
        SELECT
            MAX(CASE WHEN ls.category = 'vocabulary' THEN ls.id::text END) AS vocab_sec_id,
            MAX(CASE WHEN ls.category = 'grammar'    THEN ls.id::text END) AS gram_sec_id
        FROM lesson l
        JOIN level lv        ON lv.id = l.level_id
        JOIN lesson_section ls ON ls.lesson_id = l.id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 1
        GROUP BY l.id
    """)).fetchone()
    assert row and row.vocab_sec_id and row.gram_sec_id, (
        "Beginner A Lesson 1 section IDs not found — run 0002 first"
    )
    return str(row.vocab_sec_id), str(row.gram_sec_id)


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    vocab_sec_id, gram_sec_id = _get_section_ids(bind)

    # =========================================================================
    # A — 10 missing vocabulary words + word_card content blocks
    # display_order 6–20 (0–5 used by 0002)
    # =========================================================================

    # Group headers and word list:
    # Each tuple: (display_order, block_type, word_or_None, definition, example, header_markdown)
    vocab_items = [
        # Personal Words group
        (6,  "text",      None,        None, None,
         "### Personal Words"),
        (7,  "word_card", "i",         "Used to talk about yourself.",
         "I am from Sri Lanka.", None),
        (8,  "word_card", "you",       "Used to talk to another person.",
         "You are my teacher.", None),
        (9,  "word_card", "name",      "What people call you.",
         "What is your name?", None),
        # Linking Verbs group
        (10, "text",      None,        None, None,
         "### Linking Verbs"),
        (11, "word_card", "am",        "Used with I.",
         "I am a student.", None),
        (12, "word_card", "are",       "Used with You.",
         "You are fine.", None),
        # Feelings & Roles group
        (13, "text",      None,        None, None,
         "### Feelings & Roles"),
        (14, "word_card", "fine",      "Feeling good.",
         "I am fine, thank you.", None),
        (15, "word_card", "student",   "A person who studies.",
         "I am a student.", None),
        (16, "word_card", "teacher",   "A person who teaches.",
         "She is a teacher.", None),
        # Places group
        (17, "text",      None,        None, None,
         "### Places"),
        (18, "word_card", "sri lanka", "A country.",
         "I am from Sri Lanka.", None),
        # Question Word group
        (19, "text",      None,        None, None,
         "### Question Word"),
        (20, "word_card", "what",      "Used to ask about things.",
         "What is your name?", None),
    ]

    for (disp_order, btype, word, defn, example, header_md) in vocab_items:
        if btype == "text":
            insert_content_block(
                vocab_sec_id, "text", disp_order,
                {"markdown": header_md}, str(uuid7()),
            )
        else:
            insert_word_card(
                bind, vocab_sec_id, disp_order,
                word, defn, example, str(uuid7()), str(uuid7()),
            )

    # =========================================================================
    # B — Grammar: Short Forms text block (display_order 1)
    # existing text block is at display_order 0 — no conflict
    # =========================================================================
    short_forms_md = (
        "## Short Forms (Natural English)\n\n"
        "| Long Form | Short Form |\n"
        "|-----------|------------|\n"
        "| I am      | I'm        |\n"
        "| What is   | What's     |\n"
        "| You are   | You're     |\n\n"
        "**Examples:**\n\n"
        "- I'm Kamal.\n"
        "- What's your name?\n"
        "- You're my teacher."
    )
    insert_content_block(
        gram_sec_id, "text", 1, {"markdown": short_forms_md}, str(uuid7()),
    )

    # =========================================================================
    # C — Grammar: 12 assessment questions
    # Set A (fill_blank_options, display_order 6–11)
    # Set B (mcq_long_short_form short form, display_order 12–14)
    # Set C (mcq_long_short_form long form, display_order 15–17)
    # =========================================================================

    # Set A — choose the correct verb form
    set_a = [
        (6,  "I ___ a student.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "are"}], "a",
         "Correct! With 'I' we use 'am'.",
         "With 'I', we always use 'am'."),
        (7,  "You ___ my teacher.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "are"}], "b",
         "Correct! With 'You' we use 'are'.",
         "With 'You', we always use 'are'."),
        (8,  "What ___ your name?",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'What is your name?' is the standard question.",
         "'What is your name?' — use 'is' here."),
        (9,  "I ___ Kamal.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'I am Kamal' — 'am' goes with 'I'.",
         "With 'I', we use 'am': I am Kamal."),
        (10, "You ___ from Sri Lanka.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "are"}], "b",
         "Correct! 'You are from Sri Lanka.'",
         "With 'You', use 'are': You are from Sri Lanka."),
        (11, "What ___ this?",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'What is this?' uses 'is'.",
         "'What is this?' — use 'is' for a single object."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_a:
        payload = {
            "sentence_with_blank": blank_sentence,
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence, payload, 5, str(uuid7()),
        )

    # Set B — choose the correct short form
    set_b = [
        (12, "I am Kamal.",
         [{"id": "a", "text": "I'm Kamal."}, {"id": "b", "text": "Im Kamal."}], "a",
         "Correct! 'I am' shortens to 'I'm'.",
         "'I am' → 'I'm' (with apostrophe). 'Im' is not correct."),
        (13, "What is your name?",
         [{"id": "a", "text": "Whats your name?"}, {"id": "b", "text": "What's your name?"}], "b",
         "Correct! 'What is' shortens to 'What's' (with apostrophe).",
         "'What is' → 'What's'. The apostrophe replaces the missing letter."),
        (14, "You are my teacher.",
         [{"id": "a", "text": "You're my teacher."}, {"id": "b", "text": "Your my teacher."}], "a",
         "Correct! 'You are' shortens to 'You're'.",
         "'You are' → 'You're'. 'Your' is a possessive — a different word."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_b:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # Set C — choose the correct long form
    set_c = [
        (15, "I'm a student.",
         [{"id": "a", "text": "I am a student."}, {"id": "b", "text": "I are a student."}], "a",
         "Correct! 'I'm' expands to 'I am'.",
         "'I'm' is short for 'I am'. 'I are' is never correct."),
        (16, "What's your name?",
         [{"id": "a", "text": "What is your name?"}, {"id": "b", "text": "What are your name?"}], "a",
         "Correct! 'What's' expands to 'What is'.",
         "'What's' is short for 'What is'. 'What are your name?' is incorrect."),
        (17, "You're from Sri Lanka.",
         [{"id": "a", "text": "You are from Sri Lanka."}, {"id": "b", "text": "You am from Sri Lanka."}], "a",
         "Correct! 'You're' expands to 'You are'.",
         "'You're' is short for 'You are'. 'You am' is never correct."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_c:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # D — Grammar: Extra Practice questions (purpose=practice, xp=0)
    # display_order 18–20
    # =========================================================================
    insert_question(
        gram_sec_id, "match_pairs", "practice", 18,
        "Match each word to its category.",
        {
            "pairs": [
                {"id": "p1", "left": "Hello",     "right": "Greeting"},
                {"id": "p2", "left": "Student",   "right": "Person"},
                {"id": "p3", "left": "Fine",      "right": "Feeling"},
                {"id": "p4", "left": "Sri Lanka", "right": "Country"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well matched!",
                "incorrect": "Try again — match each word to its group.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        gram_sec_id, "fill_blank_options", "practice", 19,
        "I ___ a student.",
        {
            "sentence_with_blank": "I ___ a student.",
            "options": [{"id": "a", "text": "am"}, {"id": "b", "text": "are"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'I am a student.'",
                "incorrect": "With 'I', use 'am'.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        gram_sec_id, "fill_blank_options", "practice", 20,
        "What's your ___?",
        {
            "sentence_with_blank": "What's your ___?",
            "options": [{"id": "a", "text": "name"}, {"id": "b", "text": "fine"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'What's your name?' asks for someone's name.",
                "incorrect": "'Name' is the answer — 'fine' is a feeling, not a question target.",
            },
        },
        0, str(uuid7()),
    )

    # =========================================================================
    # E — Grammar: Self-check block (display_order 99 — rendered last)
    # =========================================================================
    insert_content_block(
        gram_sec_id, "self_check", 99,
        {
            "prompt": "Can you say this without reading?",
            "text": (
                "Hello! My name is ______.\n"
                "I am a student from Sri Lanka.\n"
                "Nice to meet you!"
            ),
        },
        str(uuid7()),
    )


def downgrade() -> None:
    bind = op.get_bind()
    vocab_sec_id, gram_sec_id = _get_section_ids(bind)

    # Remove new vocabulary words (by word value within this section)
    new_words = (
        "i", "you", "name", "am", "are",
        "fine", "student", "teacher", "sri lanka", "what",
    )
    words_list = ", ".join(_s(w) for w in new_words)
    op.execute(f"""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id = '{vocab_sec_id}'
          AND word IN ({words_list})
    """)

    # Remove new vocabulary content_blocks (display_order 6–20)
    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id = '{vocab_sec_id}'
          AND display_order BETWEEN 6 AND 20
    """)

    # Remove Short Forms text block and Self-check block from grammar section
    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id = '{gram_sec_id}'
          AND display_order IN (1, 99)
    """)

    # Remove all new grammar questions (display_order 6–20)
    op.execute(f"""
        DELETE FROM question
        WHERE lesson_section_id = '{gram_sec_id}'
          AND display_order BETWEEN 6 AND 20
    """)
