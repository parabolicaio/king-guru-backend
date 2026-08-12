"""Lesson 4 — Classroom & Everyday Objects (full Phase 1 seed).

Creates Lesson 4 from scratch: lesson row, vocabulary section (19 words across
three groups: Classroom Objects, Everyday Objects, Demonstratives), and grammar
section (3 teaching blocks, 8 assessment questions, 2 practice questions,
self_check block).

Phase 2+ sections (Pronunciation, Listening, Reading, Speaking, Writing)
are deferred.

Revision ID: 2c1b0a9f8e7d
Revises:     4e3d2c1b0a9f
Create Date: 2026-06-09
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import (
    ensure_lesson,
    ensure_section,
    insert_content_block,
    insert_question,
    insert_word_card,
)
from sqlalchemy import text

revision: str = "2c1b0a9f8e7d"
down_revision: Union[str, None] = "4e3d2c1b0a9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    # =========================================================================
    # Create Lesson 4
    # =========================================================================
    l4_id = ensure_lesson(
        bind, level_id, 4,
        "Classroom & Everyday Objects",
        "Learn to identify and describe classroom and everyday objects using demonstratives.",
        str(uuid7()),
    )
    l4_vocab_sec_id = ensure_section(
        bind, l4_id, "vocabulary", 1, "Vocabulary", str(uuid7()),
    )
    l4_gram_sec_id = ensure_section(
        bind, l4_id, "grammar", 2, "Grammar", str(uuid7()),
    )

    # =========================================================================
    # A — Vocabulary: objectives block (display_order 0)
    # =========================================================================
    obj_md = (
        "## Lesson Objectives\n\n"
        "By the end of this lesson you will be able to:\n\n"
        "- Identify common classroom and everyday objects\n"
        "- Use **this**, **that**, **these**, and **those** correctly\n"
        "- Ask and answer questions about objects around you\n"
        "- Use the articles *a*, *an*, and *the* correctly"
    )
    insert_content_block(
        l4_vocab_sec_id, "text", 0, {"markdown": obj_md}, str(uuid7()),
    )

    # =========================================================================
    # B — Vocabulary: Classroom Objects (display_order 1–11)
    # =========================================================================
    insert_content_block(
        l4_vocab_sec_id, "text", 1, {"markdown": "### Classroom Objects"}, str(uuid7()),
    )

    classroom_objects = [
        (2,  "book",     "An object you read or study from.",              "This is my book."),
        (3,  "pen",      "A tool used to write with ink.",                 "This is my pen."),
        (4,  "pencil",   "A tool used to write or draw.",                  "This is my pencil."),
        (5,  "bag",      "A container you carry your things in.",          "My bag is on the desk."),
        (6,  "desk",     "A table you sit at to study or work.",           "This is my desk."),
        (7,  "chair",    "A seat with a back that you sit on.",            "That is my chair."),
        (8,  "board",    "A large flat surface for writing in class.",     "That is the board."),
        (9,  "eraser",   "A tool used to rub out pencil marks.",           "This is an eraser."),
        (10, "ruler",    "A tool used to draw straight lines or measure.", "I use a ruler to draw."),
        (11, "notebook", "A book used for writing notes.",                 "This is my notebook."),
    ]
    for (disp, word, defn, example) in classroom_objects:
        insert_word_card(
            bind, l4_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # C — Vocabulary: Everyday Objects (display_order 12–17)
    # =========================================================================
    insert_content_block(
        l4_vocab_sec_id, "text", 12, {"markdown": "### Everyday Objects"}, str(uuid7()),
    )

    everyday_objects = [
        (13, "phone",  "A device used to call and message people.",   "This is my phone."),
        (14, "key",    "A small object used to open a lock.",          "That is my key."),
        (15, "bottle", "A container used to hold water or drinks.",    "This is my water bottle."),
        (16, "door",   "An entrance to a room or building.",           "That is the door."),
        (17, "window", "An opening in a wall that lets in light.",     "Those are the windows."),
    ]
    for (disp, word, defn, example) in everyday_objects:
        insert_word_card(
            bind, l4_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # D — Vocabulary: Demonstratives (display_order 18–22)
    # =========================================================================
    insert_content_block(
        l4_vocab_sec_id, "text", 18, {"markdown": "### Demonstratives"}, str(uuid7()),
    )

    demonstratives = [
        (19, "this",  "Used for one thing that is near.",   "This is my pen."),
        (20, "that",  "Used for one thing that is far.",    "That is the board."),
        (21, "these", "Used for many things that are near.", "These are my books."),
        (22, "those", "Used for many things that are far.", "Those are the chairs."),
    ]
    for (disp, word, defn, example) in demonstratives:
        insert_word_card(
            bind, l4_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # E — Grammar: 3 teaching text blocks (display_order 0–2)
    # =========================================================================

    # Block 0: Demonstratives — near/far, singular/plural
    dem_md = (
        "## Demonstratives: This / That / These / Those\n\n"
        "Use demonstratives to talk about objects.\n"
        "They show **distance** (near/far) and **number** (one/many).\n\n"
        "| | Near | Far |\n"
        "|---|---|---|\n"
        "| **Singular (one)** | This | That |\n"
        "| **Plural (many)** | These | Those |\n\n"
        "**Singular — one object:**\n\n"
        "- This is a book. *(near)*\n"
        "- This is my pen.\n"
        "- That is a chair. *(far)*\n"
        "- That is the board.\n\n"
        "**Plural — more than one:**\n\n"
        "- These are books. *(near)*\n"
        "- These are my pencils.\n"
        "- Those are desks. *(far)*\n"
        "- Those are windows.\n\n"
        "**With possessive adjectives:**\n\n"
        "- This is my book.\n"
        "- That is your bag.\n"
        "- These are his pencils.\n"
        "- Those are her chairs."
    )
    insert_content_block(
        l4_gram_sec_id, "text", 0, {"markdown": dem_md}, str(uuid7()),
    )

    # Block 1: Questions with Demonstratives
    q_md = (
        "## Questions with Demonstratives\n\n"
        "**Asking about one object:**\n\n"
        "- What is this? → This is a pen.\n"
        "- What is that? → That is a desk.\n\n"
        "**Asking about many objects:**\n\n"
        "- What are these? → These are books.\n"
        "- What are those? → Those are chairs.\n\n"
        "**Yes / No questions:**\n\n"
        "- Is this your pen? → Yes, it is. / No, it isn't.\n"
        "- Is that the board? → Yes, it is. / No, it isn't.\n"
        "- Are these your books? → Yes, they are. / No, they aren't.\n"
        "- Are those your pencils? → Yes, they are. / No, they aren't."
    )
    insert_content_block(
        l4_gram_sec_id, "text", 1, {"markdown": q_md}, str(uuid7()),
    )

    # Block 2: Articles, Negatives & Common Mistakes
    art_md = (
        "## Articles, Negatives & Common Mistakes\n\n"
        "**Articles (a / an / the):**\n\n"
        "- **a** → before consonant sound: a pen, a book, a bag\n"
        "- **an** → before vowel sound: an eraser\n"
        "- **the** → specific object: That is the board.\n\n"
        "**Negative sentences:**\n\n"
        "| Long Form | Short Form |\n"
        "|-----------|------------|\n"
        "| is not    | isn't      |\n"
        "| are not   | aren't     |\n\n"
        "Examples:\n\n"
        "- This is not my pen. → This isn't my pen.\n"
        "- These are not my books. → These aren't my books.\n\n"
        "**Common Mistakes:**\n\n"
        "- ✗ This are my books. → ✓ These are my books.\n"
        "- ✗ Those is my chair. → ✓ That is my chair.\n"
        "- ✗ These is my pen. → ✓ This is my pen."
    )
    insert_content_block(
        l4_gram_sec_id, "text", 2, {"markdown": art_md}, str(uuid7()),
    )

    # =========================================================================
    # F — Grammar: Set A — Choose the correct demonstrative (4 fill_blank_options)
    # display_order 4–7, assessment, xp=5
    # =========================================================================
    set_a = [
        (4, "___ is my pencil.",
         [{"id": "a", "text": "This"}, {"id": "b", "text": "These"}], "a",
         "Correct! 'This' is used for one thing that is near.",
         "'Pencil' is singular — use 'This' (near, one), not 'These' (near, many)."),
        (5, "___ are my books.",
         [{"id": "a", "text": "These"}, {"id": "b", "text": "That"}], "a",
         "Correct! 'These' is used for many things that are near.",
         "'Books' is plural — use 'These' (near, many), not 'That' (far, one)."),
        (6, "___ is the board.",
         [{"id": "a", "text": "That"}, {"id": "b", "text": "Those"}], "a",
         "Correct! 'That' is used for one thing that is far.",
         "'Board' is singular — use 'That' (far, one), not 'Those' (far, many)."),
        (7, "___ are the desks.",
         [{"id": "a", "text": "Those"}, {"id": "b", "text": "This"}], "a",
         "Correct! 'Those' is used for many things that are far.",
         "'Desks' is plural — use 'Those' (far, many), not 'This' (near, one)."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_a:
        payload = {
            "sentence_with_blank": blank_sentence,
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l4_gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # G — Grammar: Set B — Yes/No question responses (2 mcq_single)
    # display_order 8–9, assessment, xp=5
    # =========================================================================
    set_b = [
        (8, "Is this your bag?",
         [{"id": "a", "text": "Yes, it is."}, {"id": "b", "text": "Yes, they are."}], "a",
         "Correct! 'This' refers to one thing — use 'it'.",
         "'Is this' asks about one thing, so the answer uses 'it', not 'they'."),
        (9, "Are these your pens?",
         [{"id": "a", "text": "Yes, they are."}, {"id": "b", "text": "Yes, it is."}], "a",
         "Correct! 'These' refers to many things — use 'they'.",
         "'Are these' asks about many things, so the answer uses 'they', not 'it'."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_b:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l4_gram_sec_id, "mcq_single", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # H — Grammar: Set C — Choose is or are (2 fill_blank_options)
    # display_order 10–11, assessment, xp=5
    # =========================================================================
    set_c = [
        (10, "That ___ my chair.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'That' is singular — use 'is'.",
         "'That' refers to one thing, so use 'is', not 'are'."),
        (11, "These ___ my books.",
         [{"id": "a", "text": "are"}, {"id": "b", "text": "is"}], "a",
         "Correct! 'These' is plural — use 'are'.",
         "'These' refers to many things, so use 'are', not 'is'."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_c:
        payload = {
            "sentence_with_blank": blank_sentence,
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l4_gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # I — Grammar: Extra Practice (2 questions, purpose=practice, xp=0)
    # display_order 12–13
    # =========================================================================
    insert_question(
        l4_gram_sec_id, "match_pairs", "practice", 12,
        "Match each word to its correct category or meaning.",
        {
            "pairs": [
                {"id": "p1", "left": "Book",  "right": "Classroom object"},
                {"id": "p2", "left": "Door",  "right": "Everyday object"},
                {"id": "p3", "left": "This",  "right": "Near (one)"},
                {"id": "p4", "left": "Those", "right": "Far (many)"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well matched!",
                "incorrect": "Try again — match each word to its group or meaning.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        l4_gram_sec_id, "fill_blank_options", "practice", 13,
        "___ is an eraser.",
        {
            "sentence_with_blank": "___ is an eraser.",
            "options": [{"id": "a", "text": "This"}, {"id": "b", "text": "These"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'This' is singular and near — 'an eraser' is one object.",
                "incorrect": "'Eraser' is singular — use 'This' not 'These'.",
            },
        },
        0, str(uuid7()),
    )

    # =========================================================================
    # J — Grammar: Self-check block (display_order 99)
    # =========================================================================
    insert_content_block(
        l4_gram_sec_id, "self_check", 99,
        {
            "prompt": "Can you say this without reading?",
            "text": (
                "This is my desk.\n"
                "That is the board.\n"
                "These are my books.\n"
                "Those are the chairs."
            ),
        },
        str(uuid7()),
    )


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 4
    """)).fetchone()
    if not row:
        return
    lesson_id = row[0]

    op.execute(f"""
        DELETE FROM question
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"""
        DELETE FROM lesson_section WHERE lesson_id = '{lesson_id}'
    """)
    op.execute(f"""
        DELETE FROM lesson WHERE id = '{lesson_id}'
    """)
