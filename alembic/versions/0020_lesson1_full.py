"""Lesson 1 — Greetings & Introductions (full Phase 1 seed).

Rebuilds Lesson 1 from scratch with all 7 sections:
  Vocabulary  — 21 words across 6 groups + 1 match_pairs assessment question
  Grammar     — 7 teaching blocks + 13 assessment questions
  Pronunciation — 4 phrase groups, content only
  Listening   — 1 phrase group + 5 assessment questions
  Reading     — dialogue block + 3 assessment questions
  Speaking    — phrase groups, content only
  Writing     — 4 assessment questions + self_check + summary blocks

Performs the Lesson 1 cleanup (scripts/cleanup_lesson_content.sql, scoped to
beginner_a / lesson_order = 1) as its first step, so the full chain replays
cleanly on an empty database. On production this cleanup was run manually
before this revision was applied; databases already at or past this revision
never execute it again.

Revision ID: a1b2c3d4e5f6
Revises:     c3d4e5f6a7b8
Create Date: 2026-06-10
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

revision: str = "a1b2c3d4e6f7"
down_revision: Union[str, None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _cleanup_lesson1(bind, level_id: str) -> None:
    """Remove the pre-0020 Lesson 1 (seeded by 0002 + 0014) and any progress
    tied to it, mirroring scripts/cleanup_lesson_content.sql. Deletion order
    matters: vocabulary_mastery / attempt / lesson_progress / vocabulary_word
    are RESTRICT FKs that block the lesson delete; sections, content blocks
    and questions cascade from the lesson row.
    """
    row = bind.execute(
        text("SELECT id::text FROM lesson WHERE level_id = :lid AND lesson_order = 1"),
        {"lid": level_id},
    ).fetchone()
    if not row:
        return
    l1 = str(row[0])

    op.execute(f"""
        DELETE FROM vocabulary_mastery
        WHERE vocabulary_word_id IN (
            SELECT vw.id
            FROM   vocabulary_word vw
            JOIN   lesson_section ls ON ls.id = vw.lesson_section_id
            WHERE  ls.lesson_id = '{l1}'
        )
    """)
    op.execute(f"""
        DELETE FROM xp_ledger
        WHERE reference_type = 'attempt'
          AND reference_id IN (SELECT id FROM attempt WHERE lesson_id = '{l1}')
    """)
    op.execute(f"""
        DELETE FROM xp_ledger
        WHERE reference_type = 'lesson' AND reference_id = '{l1}'
    """)
    op.execute(f"DELETE FROM attempt WHERE lesson_id = '{l1}'")
    op.execute(f"DELETE FROM lesson_progress WHERE lesson_id = '{l1}'")
    op.execute(f"""
        DELETE FROM content_review
        WHERE (content_type = 'lesson' AND content_id = '{l1}')
           OR (content_type = 'question'
               AND content_id IN (
                   SELECT q.id
                   FROM   question q
                   JOIN   lesson_section ls ON ls.id = q.lesson_section_id
                   WHERE  ls.lesson_id = '{l1}'
               ))
    """)
    op.execute(f"""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{l1}'
        )
    """)
    op.execute(f"DELETE FROM lesson WHERE id = '{l1}'")
    op.execute("""
        UPDATE "user"
        SET    xp_total = COALESCE(
                   (SELECT SUM(xp_delta) FROM xp_ledger WHERE xp_ledger.user_id = "user".id),
                   0
               ),
               updated_at = now()
    """)


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    _cleanup_lesson1(bind, level_id)

    # =========================================================================
    # Create Lesson 1
    # =========================================================================
    l1_id = ensure_lesson(
        bind, level_id, 1,
        "Greetings & Introductions",
        "Learn to greet people, say your name, and introduce yourself in English.",
        str(uuid7()),
    )
    vocab_sec_id  = ensure_section(bind, l1_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id   = ensure_section(bind, l1_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id   = ensure_section(bind, l1_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id   = ensure_section(bind, l1_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id   = ensure_section(bind, l1_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id  = ensure_section(bind, l1_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id  = ensure_section(bind, l1_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY SECTION
    # =========================================================================

    # Block 0 — objectives
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: greet people in "
            "English, say your name and ask for someone else's name, use "
            "am and are correctly, and introduce yourself in a few sentences."
        ),
    }, str(uuid7()))

    # ── Group 1: Greetings ────────────────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Greetings"}, str(uuid7()))

    greetings = [
        (2,  "Hello",          "A friendly greeting.",                               "Hello! How are you?"),
        (3,  "Good morning",   "A greeting used in the morning.",                    "Good morning, teacher!"),
        (4,  "Good evening",   "A greeting used in the late afternoon or evening.",  "Good evening! Nice to see you."),
        (5,  "Goodbye",        "Said when you are leaving.",                         "Goodbye! See you tomorrow."),
        (6,  "Nice to meet you", "Said when meeting someone for the first time.",    "Nice to meet you, Kamal."),
    ]
    for (disp, word, defn, example) in greetings:
        insert_word_card(bind, vocab_sec_id, disp, word, defn, example, str(uuid7()), str(uuid7()))

    # ── Group 2: Personal Words ───────────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 7, {"type": "heading", "text": "Personal Words"}, str(uuid7()))

    personal_words = [
        (8,  "I",    "Used to talk about yourself.",          "I am a student."),
        (9,  "You",  "Used to talk to another person.",       "You are my teacher."),
        (10, "Name", "What people call you.",                  "My name is Kamal."),
    ]
    for (disp, word, defn, example) in personal_words:
        insert_word_card(bind, vocab_sec_id, disp, word, defn, example, str(uuid7()), str(uuid7()))

    # ── Group 3: Linking Verbs ────────────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 11, {"type": "heading", "text": "Linking Verbs"}, str(uuid7()))

    linking_verbs = [
        (12, "Am",  "Used with 'I' to describe yourself.",      "I am fine."),
        (13, "Are", "Used with 'you' to describe someone.",     "You are my friend."),
    ]
    for (disp, word, defn, example) in linking_verbs:
        insert_word_card(bind, vocab_sec_id, disp, word, defn, example, str(uuid7()), str(uuid7()))

    # ── Group 4: Feelings and Roles ───────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 14, {"type": "heading", "text": "Feelings and Roles"}, str(uuid7()))

    feelings_roles = [
        (15, "Fine",    "Feeling good or well.",          "I am fine, thank you."),
        (16, "Student", "A person who studies.",          "I am a student."),
        (17, "Teacher", "A person who teaches.",          "She is a teacher."),
    ]
    for (disp, word, defn, example) in feelings_roles:
        insert_word_card(bind, vocab_sec_id, disp, word, defn, example, str(uuid7()), str(uuid7()))

    # ── Group 5: Places ───────────────────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 18, {"type": "heading", "text": "Places"}, str(uuid7()))
    insert_word_card(bind, vocab_sec_id, 19, "Sri Lanka",
                     "A beautiful island country in Asia.",
                     "I am from Sri Lanka.",
                     str(uuid7()), str(uuid7()))

    # ── Group 6: Question Words ───────────────────────────────────────────────
    insert_content_block(vocab_sec_id, "text", 20, {"type": "heading", "text": "Question Words"}, str(uuid7()))

    question_words = [
        (21, "What",  "Asking for information about something.", "What is your name?"),
        (22, "Where", "Asking about a place.",                   "Where are you from?"),
        (23, "Who",   "Asking about a person.",                  "Who is your teacher?"),
        (24, "When",  "Asking about time.",                      "When do you go to school?"),
        (25, "Why",   "Asking for a reason.",                    "Why are you here?"),
        (26, "How",   "Asking about the way or manner.",         "How are you?"),
        (27, "Which", "Asking to choose between things.",        "Which book is yours?"),
    ]
    for (disp, word, defn, example) in question_words:
        insert_word_card(bind, vocab_sec_id, disp, word, defn, example, str(uuid7()), str(uuid7()))

    # ── Vocabulary assessment: match_pairs ────────────────────────────────────
    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 28,
        "Match each word to its category",
        {
            "pairs": [
                {"id": "mp1", "left": "Hello",     "right": "Greeting"},
                {"id": "mp2", "left": "Student",   "right": "Person"},
                {"id": "mp3", "left": "Fine",      "right": "Feeling"},
                {"id": "mp4", "left": "Sri Lanka", "right": "Country"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! You matched all the words correctly.",
                "incorrect": "Some matches are wrong. Think about what category each word belongs to.",
            },
        },
        10, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR SECTION
    # =========================================================================

    # Block 0 — intro
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": "We use 'am' with 'I' and 'are' with 'you'. Short forms make speech sound natural.",
    }, str(uuid7()))

    # Block 1–3 — sentence pattern example cards
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "Sentence Pattern 1 — Name",
        "sentences": ["I am Ravi.", "My name is Ravi.", "What is your name?"],
    }, str(uuid7()))

    insert_content_block(gram_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "Sentence Pattern 2 — Role",
        "sentences": ["I am a student.", "You are a teacher."],
    }, str(uuid7()))

    insert_content_block(gram_sec_id, "text", 3, {
        "type": "example_cards",
        "label": "Sentence Pattern 3 — Place",
        "sentences": ["I am from Sri Lanka.", "I am in the classroom."],
    }, str(uuid7()))

    # Block 4–5 — Q&A pairs
    insert_content_block(gram_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "How are you?",
        "answer": "I am fine.",
    }, str(uuid7()))

    insert_content_block(gram_sec_id, "text", 5, {
        "type": "qa_pair",
        "question": "What is your name?",
        "answer": "My name is Kamal.",
    }, str(uuid7()))

    # Block 6 — short forms
    insert_content_block(gram_sec_id, "text", 6, {
        "type": "short_forms",
        "pairs": [
            {"long": "I am",    "short": "I’m",    "example": "I’m Kamal."},
            {"long": "What is", "short": "What’s", "example": "What’s your name?"},
            {"long": "You are", "short": "You’re", "example": "You’re my teacher."},
        ],
    }, str(uuid7()))

    # ── Grammar questions (display_order 7–19) ────────────────────────────────

    # Set A: fill_blank_options — verb form (am/is/are)
    fill_opts_abc = [
        {"id": "a", "text": "am"},
        {"id": "b", "text": "is"},
        {"id": "c", "text": "are"},
    ]
    verb_questions = [
        (7,  "I ___ Kamal.",        "a", "Correct! Use 'am' with 'I'.",         "Use 'am' with 'I' — 'I am Kamal.'"),
        (8,  "You ___ my friend.",  "c", "Correct! Use 'are' with 'you'.",      "Use 'are' with 'you' — 'You are my friend.'"),
        (9,  "She ___ a teacher.",  "b", "Correct! Use 'is' with 'she'.",       "Use 'is' with 'she' — 'She is a teacher.'"),
    ]
    for (disp, sentence, correct_id, fb_c, fb_i) in verb_questions:
        insert_question(
            gram_sec_id, "fill_blank_options", "assessment", disp,
            sentence,
            {
                "sentence_with_blank": sentence,
                "options": fill_opts_abc,
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    # Set B: fill_blank_options — preposition / verb after 'am'
    insert_question(
        gram_sec_id, "fill_blank_options", "assessment", 10,
        "I am ___ Sri Lanka.",
        {
            "sentence_with_blank": "I am ___ Sri Lanka.",
            "options": [
                {"id": "a", "text": "from"},
                {"id": "b", "text": "to"},
                {"id": "c", "text": "in"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'I am from Sri Lanka' tells us where you are from.",
                "incorrect": "Use 'from' to say where you are from — 'I am from Sri Lanka.'",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        gram_sec_id, "fill_blank_options", "assessment", 11,
        "Nice to ___ you.",
        {
            "sentence_with_blank": "Nice to ___ you.",
            "options": [
                {"id": "a", "text": "meet"},
                {"id": "b", "text": "see"},
                {"id": "c", "text": "talk"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Nice to meet you' is a standard greeting when meeting someone.",
                "incorrect": "The fixed phrase is 'Nice to meet you' — use 'meet'.",
            },
        },
        5, str(uuid7()),
    )

    # Set C: mcq_long_short_form — short forms
    short_form_qs = [
        (12, "What is the short form of 'I am'?",
         [{"id": "a", "text": "I'm"}, {"id": "b", "text": "Im"}, {"id": "c", "text": "I are"}, {"id": "d", "text": "I's"}],
         "a",
         "Correct! 'I am' shortens to 'I’m'.",
         "'I am' shortens to 'I’m' — the apostrophe replaces the 'a'."),
        (13, "What is the short form of 'What is'?",
         [{"id": "a", "text": "What's"}, {"id": "b", "text": "Whats"}, {"id": "c", "text": "What're"}, {"id": "d", "text": "Whatss"}],
         "a",
         "Correct! 'What is' shortens to 'What’s'.",
         "'What is' shortens to 'What’s' — the apostrophe replaces the 'i'."),
        (14, "What is the short form of 'You are'?",
         [{"id": "a", "text": "You're"}, {"id": "b", "text": "Yours"}, {"id": "c", "text": "You's"}, {"id": "d", "text": "Your"}],
         "a",
         "Correct! 'You are' shortens to 'You’re'.",
         "'You are' shortens to 'You’re' — the apostrophe replaces the 'a'."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in short_form_qs:
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # Set D: mcq_long_short_form — long forms
    long_form_qs = [
        (15, "What is the long form of 'I’m'?",
         [{"id": "a", "text": "I am"}, {"id": "b", "text": "I is"}, {"id": "c", "text": "I are"}, {"id": "d", "text": "Am I"}],
         "a",
         "Correct! 'I’m' expands to 'I am'.",
         "'I’m' is the short form of 'I am'."),
        (16, "What is the long form of 'What’s'?",
         [{"id": "a", "text": "What is"}, {"id": "b", "text": "What are"}, {"id": "c", "text": "What am"}, {"id": "d", "text": "Is what"}],
         "a",
         "Correct! 'What’s' expands to 'What is'.",
         "'What’s' is the short form of 'What is'."),
        (17, "What is the long form of 'You’re'?",
         [{"id": "a", "text": "You are"}, {"id": "b", "text": "You am"}, {"id": "c", "text": "You is"}, {"id": "d", "text": "Are you"}],
         "a",
         "Correct! 'You’re' expands to 'You are'.",
         "'You’re' is the short form of 'You are'."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in long_form_qs:
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # Set E: fill_blank_options — question word & article
    insert_question(
        gram_sec_id, "fill_blank_options", "assessment", 18,
        "___ is your name?",
        {
            "sentence_with_blank": "___ is your name?",
            "options": [
                {"id": "a", "text": "What"},
                {"id": "b", "text": "Where"},
                {"id": "c", "text": "Who"},
                {"id": "d", "text": "When"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'What is your name?' asks for a name.",
                "incorrect": "'What' asks for information — 'What is your name?' is the correct question.",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        gram_sec_id, "fill_blank_options", "assessment", 19,
        "I am ___ student.",
        {
            "sentence_with_blank": "I am ___ student.",
            "options": [
                {"id": "a", "text": "a"},
                {"id": "b", "text": "an"},
                {"id": "c", "text": "the"},
                {"id": "d", "text": "one"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Use 'a' before a consonant sound — 'a student'.",
                "incorrect": "Use 'a' before a consonant sound. 'student' starts with a consonant, so 'a student'.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # PRONUNCIATION SECTION — content only, no questions
    # =========================================================================

    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Listen and Repeat"}, str(uuid7()))
    for (disp, phrase) in [(1, "Hello"), (2, "Good morning"), (3, "Nice to meet you")]:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    insert_content_block(pron_sec_id, "text", 4, {"type": "heading", "text": "Stress and Intonation"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 5, {"type": "phrase_card", "text": "How are YOU?", "note": "Stress on YOU"}, str(uuid7()))

    insert_content_block(pron_sec_id, "text", 6, {"type": "heading", "text": "Syllables"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 7, {"type": "phrase_card", "text": "Afternoon", "note": "Af · ter · noon — 3 clear beats"}, str(uuid7()))

    insert_content_block(pron_sec_id, "text", 8, {"type": "heading", "text": "Breath Sounds"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 9,  {"type": "phrase_card", "text": "Hello", "note": "Strong breath at H"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 10, {"type": "phrase_card", "text": "Hi",    "note": "Short and soft"}, str(uuid7()))

    # =========================================================================
    # LISTENING SECTION
    # =========================================================================

    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Listen and Repeat"}, str(uuid7()))
    listen_phrases = [
        (1, "Hello!"),
        (2, "My name is Kamal."),
        (3, "I am a student."),
        (4, "I am from Sri Lanka."),
        (5, "How are you?"),
        (6, "Nice to meet you."),
    ]
    for (disp, phrase) in listen_phrases:
        insert_content_block(list_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    # ── Listening questions ───────────────────────────────────────────────────
    insert_question(
        list_sec_id, "mcq_single", "assessment", 7,
        "My name is Kamal. What is his name?",
        {
            "options": [
                {"id": "a", "text": "Ravi"},
                {"id": "b", "text": "Kamal"},
                {"id": "c", "text": "Nimal"},
                {"id": "d", "text": "Saman"},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! He says 'My name is Kamal.'",
                "incorrect": "Listen again: 'My name is Kamal.' — his name is Kamal.",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        list_sec_id, "mcq_single", "assessment", 8,
        "I am a student. What is Kamal?",
        {
            "options": [
                {"id": "a", "text": "Student"},
                {"id": "b", "text": "Teacher"},
                {"id": "c", "text": "Doctor"},
                {"id": "d", "text": "Friend"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'I am a student' — Kamal is a student.",
                "incorrect": "He says 'I am a student' — Kamal is a student.",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        list_sec_id, "mcq_single", "assessment", 9,
        "I am from Sri Lanka. Where is Kamal from?",
        {
            "options": [
                {"id": "a", "text": "India"},
                {"id": "b", "text": "China"},
                {"id": "c", "text": "Sri Lanka"},
                {"id": "d", "text": "England"},
            ],
            "correct_option_id": "c",
            "feedback": {
                "correct": "Correct! 'I am from Sri Lanka.'",
                "incorrect": "He says 'I am from Sri Lanka.' — Kamal is from Sri Lanka.",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        list_sec_id, "true_false", "assessment", 10,
        "Kamal is introducing himself. True or False?",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Correct! Kamal says his name and tells us about himself.",
                "incorrect": "Kamal says 'My name is Kamal. I am a student.' — that is introducing himself.",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        list_sec_id, "true_false", "assessment", 11,
        "You say 'Nice to meet you' when meeting someone new. True or False?",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Correct! 'Nice to meet you' is used when you meet someone for the first time.",
                "incorrect": "'Nice to meet you' is always said when meeting someone for the first time.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # READING SECTION
    # =========================================================================

    insert_content_block(read_sec_id, "text", 0, {
        "type": "plain",
        "text": "Read the conversation below and answer the questions.",
    }, str(uuid7()))

    insert_content_block(read_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "A", "text": "Good evening!"},
            {"speaker": "B", "text": "Good evening! What is your name?"},
            {"speaker": "A", "text": "My name is Nimal. Nice to meet you."},
            {"speaker": "B", "text": "Nice to meet you too. I am Kasun. How are you?"},
            {"speaker": "A", "text": "I am fine, thank you. Where are you from?"},
            {"speaker": "B", "text": "I am from Kandy. Goodbye!"},
            {"speaker": "A", "text": "Goodbye!"},
        ],
    }, str(uuid7()))

    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 2,
        "What is the first speaker's name?",
        {
            "accepted_answers": ["Nimal", "nimal"],
            "feedback": {
                "correct": "Correct! The first speaker says 'My name is Nimal.'",
                "incorrect": "Read again — the first speaker says 'My name is Nimal.'",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 3,
        "How is Nimal feeling?",
        {
            "accepted_answers": ["fine", "i am fine", "i'm fine", "fine thank you", "fine, thank you"],
            "feedback": {
                "correct": "Correct! Nimal says 'I am fine, thank you.'",
                "incorrect": "Read again — Nimal says 'I am fine, thank you.'",
            },
        },
        5, str(uuid7()),
    )

    insert_question(
        read_sec_id, "true_false", "assessment", 4,
        "Nimal and Kasun are meeting for the first time. True or False?",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Correct! They say 'Nice to meet you' which is said when meeting someone for the first time.",
                "incorrect": "They say 'Nice to meet you' to each other — that phrase is used when meeting for the first time.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # SPEAKING SECTION — content only, no questions
    # =========================================================================

    insert_content_block(speak_sec_id, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    repeat_phrases = [
        (1, "Hello."),
        (2, "Good morning."),
        (3, "My name is Kamal."),
        (4, "I am a student."),
        (5, "Nice to meet you."),
    ]
    for (disp, phrase) in repeat_phrases:
        insert_content_block(speak_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    insert_content_block(speak_sec_id, "text", 6, {
        "type": "plain",
        "text": "Now speak 3 sentences about yourself: your greeting, your name, and where you are from.",
    }, str(uuid7()))

    insert_content_block(speak_sec_id, "text", 7, {
        "type": "example_cards",
        "label": "Example",
        "sentences": ["Hello! My name is Kamal. I am from Sri Lanka."],
    }, str(uuid7()))

    # =========================================================================
    # WRITING SECTION
    # =========================================================================

    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Fill in each blank with the correct word.",
    }, str(uuid7()))

    writing_qs = [
        (1, "Hello, my ____ is Kamal.",  ["name"],
         "Correct! 'Hello, my name is Kamal.'",
         "The blank is asking for your name — 'Hello, my name is Kamal.'"),
        (2, "I ____ a student.",          ["am"],
         "Correct! 'I am a student.' — use 'am' with 'I'.",
         "Use 'am' with 'I' — 'I am a student.'"),
        (3, "I am from ____.",            ["Sri Lanka", "sri lanka", "sri Lanka"],
         "Correct! 'I am from Sri Lanka.'",
         "The answer is 'Sri Lanka' — the country."),
        (4, "Nice ____ meet you.",        ["to"],
         "Correct! 'Nice to meet you.' is the full phrase.",
         "The full phrase is 'Nice to meet you.' — use 'to'."),
    ]
    for (disp, sentence, accepted, fb_c, fb_i) in writing_qs:
        insert_question(
            write_sec_id, "fill_blank_typed", "assessment", disp,
            sentence,
            {
                "accepted_answers": accepted,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    insert_content_block(write_sec_id, "self_check", 5, {
        "prompt": "Can you say this without reading?",
        "text": (
            "Hello! My name is ___.\n"
            "I am a student from Sri Lanka.\n"
            "Nice to meet you!"
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 6, {
        "type": "summary",
        "items": [
            "Greet someone in English",
            "Say your name and where you are from",
            "Ask someone’s name",
            "Use am and are correctly",
            "Use short forms like I’m and What’s",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 1
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
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id = '{lesson_id}'")
    op.execute(f"DELETE FROM lesson WHERE id = '{lesson_id}'")
