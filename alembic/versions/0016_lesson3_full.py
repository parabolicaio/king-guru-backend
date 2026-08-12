"""Lesson 3 — Numbers, Time & Daily Routines (full Phase 1 seed).

Creates Lesson 3 from scratch: lesson row, vocabulary section (41 words across
three groups: Numbers 1–20+extras, Time Expressions, Daily Routine Verbs), and
grammar section (4 teaching blocks, 15 assessment questions, 2 practice
questions, self_check block).

Phase 2+ sections (Pronunciation, Listening, Reading, Speaking, Writing)
are deferred.

Revision ID: 4e3d2c1b0a9f
Revises:     5f4e3d2c1b0a
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

revision: str = "4e3d2c1b0a9f"
down_revision: Union[str, None] = "5f4e3d2c1b0a"
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
    # Create Lesson 3
    # =========================================================================
    l3_id = ensure_lesson(
        bind, level_id, 3,
        "Numbers, Time & Daily Routines",
        "Learn to count, tell the time, and talk about your daily routine.",
        str(uuid7()),
    )
    l3_vocab_sec_id = ensure_section(
        bind, l3_id, "vocabulary", 1, "Vocabulary", str(uuid7()),
    )
    l3_gram_sec_id = ensure_section(
        bind, l3_id, "grammar", 2, "Grammar", str(uuid7()),
    )

    # =========================================================================
    # A — Vocabulary: objectives block (display_order 0)
    # =========================================================================
    obj_md = (
        "## Lesson Objectives\n\n"
        "By the end of this lesson you will be able to:\n\n"
        "- Use numbers to talk about time, age, and daily activities\n"
        "- Tell and ask for the time using *o'clock* and *half past* accurately\n"
        "- Use common action verbs in the present simple tense (I / you)\n"
        "- Speak about your daily routine in a simple and logical order"
    )
    insert_content_block(
        l3_vocab_sec_id, "text", 0, {"markdown": obj_md}, str(uuid7()),
    )

    # =========================================================================
    # B — Vocabulary: Numbers 1–20 (display_order 1–21)
    # =========================================================================
    insert_content_block(
        l3_vocab_sec_id, "text", 1, {"markdown": "### Numbers (1–20)"}, str(uuid7()),
    )

    number_words = [
        (2,  "one",       "The number 1.", "I have one book."),
        (3,  "two",       "The number 2.", "I have two sisters."),
        (4,  "three",     "The number 3.", "There are three students."),
        (5,  "four",      "The number 4.", "I have four brothers."),
        (6,  "five",      "The number 5.", "She is five years old."),
        (7,  "six",       "The number 6.", "I wake up at six o'clock."),
        (8,  "seven",     "The number 7.", "I eat at seven o'clock."),
        (9,  "eight",     "The number 8.", "School starts at eight o'clock."),
        (10, "nine",      "The number 9.", "I study until nine o'clock."),
        (11, "ten",       "The number 10.", "I sleep at ten o'clock."),
        (12, "eleven",    "The number 11.", "It is eleven o'clock."),
        (13, "twelve",    "The number 12.", "I have lunch at twelve o'clock."),
        (14, "thirteen",  "The number 13.", "There are thirteen students."),
        (15, "fourteen",  "The number 14.", "He is fourteen years old."),
        (16, "fifteen",   "The number 15.", "There are fifteen books."),
        (17, "sixteen",   "The number 16.", "She is sixteen years old."),
        (18, "seventeen", "The number 17.", "He is seventeen years old."),
        (19, "eighteen",  "The number 18.", "She is eighteen years old."),
        (20, "nineteen",  "The number 19.", "He is nineteen years old."),
        (21, "twenty",    "The number 20.", "There are twenty students."),
    ]
    for (disp, word, defn, example) in number_words:
        insert_word_card(
            bind, l3_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # C — Vocabulary: Extra Numbers — thirty, forty (display_order 22–24)
    # =========================================================================
    insert_content_block(
        l3_vocab_sec_id, "text", 22, {"markdown": "### Extra Numbers"}, str(uuid7()),
    )

    extra_numbers = [
        (23, "thirty", "The number 30.", "Half past means thirty minutes after the hour."),
        (24, "forty",  "The number 40.", "He is forty years old."),
    ]
    for (disp, word, defn, example) in extra_numbers:
        insert_word_card(
            bind, l3_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # D — Vocabulary: Time Expressions (display_order 25–31)
    # =========================================================================
    insert_content_block(
        l3_vocab_sec_id, "text", 25, {"markdown": "### Time Expressions"}, str(uuid7()),
    )

    time_expressions = [
        (26, "o'clock",   "Used for exact hours.",                "It is seven o'clock."),
        (27, "half past", "30 minutes after the hour.",           "It is half past six."),
        (28, "morning",   "Early part of the day.",               "I wake up in the morning."),
        (29, "afternoon", "The time after 12:00.",                "I have lunch in the afternoon."),
        (30, "evening",   "Late part of the day, before night.",  "I study in the evening."),
        (31, "night",     "Sleeping time.",                       "I sleep at night."),
    ]
    for (disp, word, defn, example) in time_expressions:
        insert_word_card(
            bind, l3_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # E — Vocabulary: Daily Routine Verbs (display_order 32–45)
    # =========================================================================
    insert_content_block(
        l3_vocab_sec_id, "text", 32, {"markdown": "### Daily Routine Verbs"}, str(uuid7()),
    )

    routine_verbs = [
        (33, "wake up",         "Stop sleeping.",                 "I wake up at six o'clock."),
        (34, "get up",          "Leave the bed.",                 "I get up and brush my teeth."),
        (35, "brush my teeth",  "Clean your teeth.",              "I brush my teeth in the morning."),
        (36, "take a shower",   "Wash your body.",                "I take a shower every day."),
        (37, "eat breakfast",   "Have morning food.",             "I eat breakfast at seven."),
        (38, "go to school",    "Travel to study at school.",     "I go to school at eight."),
        (39, "work",            "Do a job.",                      "I work every day."),
        (40, "study",           "Learn something.",               "I study in the evening."),
        (41, "have lunch",      "Eat the afternoon meal.",        "I have lunch at twelve."),
        (42, "come home",       "Return to your home.",           "I come home at four o'clock."),
        (43, "do homework",     "Complete school work at home.",  "I do my homework in the evening."),
        (44, "watch TV",        "Watch television.",              "I watch TV after dinner."),
        (45, "sleep",           "Rest at night.",                 "I sleep at ten o'clock."),
    ]
    for (disp, word, defn, example) in routine_verbs:
        insert_word_card(
            bind, l3_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # F — Grammar: 4 teaching text blocks (display_order 0–3)
    # =========================================================================

    # Block 0: Telling the Time
    telling_time_md = (
        "## Telling the Time\n\n"
        "Use **o'clock** for exact hours:\n\n"
        "- It is six o'clock.\n"
        "- It is nine o'clock.\n\n"
        "Use **half past** for 30 minutes after the hour:\n\n"
        "- It is half past seven. (= 7:30)\n"
        "- It is half past four. (= 4:30)"
    )
    insert_content_block(
        l3_gram_sec_id, "text", 0, {"markdown": telling_time_md}, str(uuid7()),
    )

    # Block 1: Asking About Time
    asking_time_md = (
        "## Asking About Time\n\n"
        "- **What time is it?** → It is eight o'clock.\n"
        "- **What time do you wake up?** → I wake up at six o'clock.\n"
        "- **What time do you go to school?** → I go to school at eight o'clock."
    )
    insert_content_block(
        l3_gram_sec_id, "text", 1, {"markdown": asking_time_md}, str(uuid7()),
    )

    # Block 2: Present Simple (I / You)
    present_simple_md = (
        "## Present Simple (I / You)\n\n"
        "Use the **base verb** — no “s” needed with I or You:\n\n"
        "| Subject | Correct | Wrong |\n"
        "|---------|---------|-------|\n"
        "| I       | wake up | wakes up |\n"
        "| You     | go      | goes |\n"
        "| I       | eat     | eats |\n\n"
        "**Examples:**\n\n"
        "- I wake up at six.\n"
        "- You go to school at eight.\n"
        "- I study in the evening."
    )
    insert_content_block(
        l3_gram_sec_id, "text", 2, {"markdown": present_simple_md}, str(uuid7()),
    )

    # Block 3: Sequence Words
    sequence_md = (
        "## Sequence Words\n\n"
        "Use these words to show the order of events:\n\n"
        "1. **First** — the first thing\n"
        "2. **Then** — the next thing\n"
        "3. **After that** — what comes next\n"
        "4. **Finally** — the last thing\n\n"
        "**Example:**\n\n"
        "First, I wake up.\n"
        "Then, I brush my teeth.\n"
        "After that, I go to school.\n"
        "Finally, I sleep."
    )
    insert_content_block(
        l3_gram_sec_id, "text", 3, {"markdown": sequence_md}, str(uuid7()),
    )

    # =========================================================================
    # G — Grammar: Set A — Choose the correct word (8 fill_blank_options)
    # display_order 4–11, assessment, xp=5
    # =========================================================================
    set_a = [
        (4,  "It is seven ___.",
         [{"id": "a", "text": "o'clock"}, {"id": "b", "text": "clock"}], "a",
         "Correct! We use 'o'clock' for exact hours.",
         "Use 'o'clock' — not 'clock' — for exact hours."),
        (5,  "It is half ___ eight.",
         [{"id": "a", "text": "past"}, {"id": "b", "text": "to"}], "a",
         "Correct! 'Half past eight' means 8:30.",
         "We say 'half past' for 30 minutes after the hour."),
        (6,  "I ___ up at six o'clock.",
         [{"id": "a", "text": "wake"}, {"id": "b", "text": "wakes"}], "a",
         "Correct! With 'I', we use the base verb 'wake'.",
         "With 'I', use the base verb: 'wake', not 'wakes'."),
        (7,  "You ___ to school at eight.",
         [{"id": "a", "text": "go"}, {"id": "b", "text": "goes"}], "a",
         "Correct! With 'You', we use the base verb 'go'.",
         "With 'You', use the base verb: 'go', not 'goes'."),
        (8,  "What time ___ it?",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'What time is it?' uses 'is'.",
         "Use 'is' — 'time' is singular."),
        (9,  "I ___ breakfast at seven.",
         [{"id": "a", "text": "eat"}, {"id": "b", "text": "eats"}], "a",
         "Correct! With 'I', we use the base verb 'eat'.",
         "With 'I', use the base verb: 'eat', not 'eats'."),
        (10, "I study in the ___.",
         [{"id": "a", "text": "morning"}, {"id": "b", "text": "number"}], "a",
         "Correct! 'Morning' is a time of day.",
         "'Morning' is the early part of the day — 'number' is not a time."),
        (11, "It is half past ___.",
         [{"id": "a", "text": "six"}, {"id": "b", "text": "o'clock"}], "a",
         "Correct! 'Half past six' means 6:30.",
         "After 'half past' we name the hour: 'six', not 'o'clock'."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_a:
        payload = {
            "sentence_with_blank": blank_sentence,
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l3_gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # H — Grammar: Set B — Choose the correct time (4 mcq_single)
    # display_order 12–15, assessment, xp=5
    # =========================================================================
    set_b = [
        (12, "7:00",
         [{"id": "a", "text": "Seven o'clock"}, {"id": "b", "text": "Half past seven"}], "a",
         "Correct! 7:00 is an exact hour — seven o'clock.",
         "7:00 is an exact hour, so we say 'seven o'clock'."),
        (13, "8:30",
         [{"id": "a", "text": "Eight o'clock"}, {"id": "b", "text": "Half past eight"}], "b",
         "Correct! 8:30 is 30 minutes after eight — half past eight.",
         "8:30 has 30 extra minutes, so we say 'half past eight'."),
        (14, "6:30",
         [{"id": "a", "text": "Half past six"}, {"id": "b", "text": "Six o'clock"}], "a",
         "Correct! 6:30 is 30 minutes after six — half past six.",
         "6:30 has 30 extra minutes, so we say 'half past six'."),
        (15, "4:00",
         [{"id": "a", "text": "Four o'clock"}, {"id": "b", "text": "Half past four"}], "a",
         "Correct! 4:00 is an exact hour — four o'clock.",
         "4:00 is an exact hour, so we say 'four o'clock'."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_b:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l3_gram_sec_id, "mcq_single", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # I — Grammar: Set C — Choose the correct long form (3 mcq_long_short_form)
    # display_order 16–18, assessment, xp=5
    # =========================================================================
    set_c = [
        (16, "It's seven o'clock.",
         [{"id": "a", "text": "It is seven o'clock."}, {"id": "b", "text": "It are seven o'clock."}], "a",
         "Correct! 'It's' expands to 'It is'.",
         "'It's' is short for 'It is'. 'It are' is never correct."),
        (17, "I wake up at six.",
         [{"id": "a", "text": "I wake up at six o'clock."}, {"id": "b", "text": "I wakes up at six."}], "a",
         "Correct! The full form uses 'o'clock' and keeps the base verb 'wake'.",
         "The full form adds 'o'clock'. 'I wakes' is never correct with 'I'."),
        (18, "You go to school at eight.",
         [{"id": "a", "text": "You go to school at eight o'clock."}, {"id": "b", "text": "You goes to school at eight."}], "a",
         "Correct! The full form uses 'o'clock' and keeps the base verb 'go'.",
         "The full form adds 'o'clock'. 'You goes' is never correct with 'You'."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_c:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            l3_gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # J — Grammar: Extra Practice (2 fill_blank_options, practice, xp=0)
    # display_order 19–20
    # =========================================================================
    insert_question(
        l3_gram_sec_id, "fill_blank_options", "practice", 19,
        "I ___ up at six o'clock.",
        {
            "sentence_with_blank": "I ___ up at six o'clock.",
            "options": [{"id": "a", "text": "wake"}, {"id": "b", "text": "wakes"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! With 'I', we use the base verb.",
                "incorrect": "With 'I', use 'wake' not 'wakes'.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        l3_gram_sec_id, "fill_blank_options", "practice", 20,
        "It is half ___ seven.",
        {
            "sentence_with_blank": "It is half ___ seven.",
            "options": [{"id": "a", "text": "past"}, {"id": "b", "text": "to"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Half past seven' = 7:30.",
                "incorrect": "We say 'half past' for 30 minutes after the hour.",
            },
        },
        0, str(uuid7()),
    )

    # =========================================================================
    # K — Grammar: Self-check block (display_order 99)
    # =========================================================================
    insert_content_block(
        l3_gram_sec_id, "self_check", 99,
        {
            "prompt": "Can you say this without reading?",
            "text": (
                "First, I wake up at six o'clock.\n"
                "Then, I eat breakfast.\n"
                "After that, I go to school.\n"
                "Finally, I sleep at ten o'clock."
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
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 3
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
