"""Lesson 7 — My Home & Prepositions of Place (Level 1 batch 2 seed).

Seeds Beginner A Lesson 7 with all 7 sections from the Level 1 lesson 7 PDF:
  Vocabulary  — 15 word cards (Rooms / More Words / Furniture) + 2 questions
  Grammar     — in/on/under + There is/There are + 9 assessment questions
  Pronunciation — focus words + practice sentences + 3 pronunciation questions
  Listening   — Father & Son dialogue + 12 assessment questions
  Reading     — Tharushi's home story + 9 assessment questions
  Speaking    — guided description prompts, content only
  Writing     — 5 typed fills + 3 typed corrections + self_check + summary

Text-only scope: picture-tap and audio-select activities are deferred until
assets exist; audio lines are embedded in question prompts (0020 convention).

Sinhala vocabulary translations reconstructed from the PDF (embedded font
mangles extracted Sinhala glyphs) — flag for content-team review.

Revision ID: f3a4b5c6d7e8
Revises:     e2f3a4b5c6d7
Create Date: 2026-07-04
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import (
    ensure_lesson,
    ensure_section,
    insert_content_block,
    insert_question,
)
from sqlalchemy import text

revision: str = "f3a4b5c6d7e8"
down_revision: Union[str, None] = "e2f3a4b5c6d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _word_card_si(
    section_id: str,
    display_order: int,
    word: str,
    word_si: str,
    definition: str,
    example: str,
    cb_id: str,
    ww_id: str,
) -> None:
    op.execute(
        f"INSERT INTO vocabulary_word "
        f"(id, lesson_section_id, word, definition, example_sentence, difficulty, translations) "
        f"VALUES ('{ww_id}', '{section_id}', {_s(word)}, {_s(definition)}, "
        f"{_s(example)}, 'easy', {_j({'si': {'word': word_si}})})"
    )
    insert_content_block(section_id, "word_card", display_order, {"vocabulary_word_id": ww_id}, cb_id)


OBJECTIVES = [
    "Identify vocabulary for rooms and furniture in a home",
    "Use prepositions in, on, and under to describe location",
    "Understand spoken descriptions of homes and rooms",
    "Pronounce home-related vocabulary clearly",
    "Speak about your home and where objects are located",
    "Write short descriptions of your home using simple sentences",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    l7_id = ensure_lesson(
        bind, level_id, 7,
        "My Home & Prepositions of Place",
        "Learn rooms and furniture words and say where things are with in, on and under.",
        str(uuid7()),
    )
    op.execute(f"UPDATE lesson SET objectives = {_j(OBJECTIVES)} WHERE id = '{l7_id}'")

    vocab_sec_id = ensure_section(bind, l7_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id  = ensure_section(bind, l7_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id  = ensure_section(bind, l7_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id  = ensure_section(bind, l7_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id  = ensure_section(bind, l7_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id = ensure_section(bind, l7_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id = ensure_section(bind, l7_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY
    # =========================================================================
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: name the rooms in "
            "a home and common furniture, and say where things are using in, "
            "on and under."
        ),
    }, str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Rooms"}, str(uuid7()))
    rooms = [
        (2, "Living room", "විසිත්ත කාමරය", "The room where the family sits together.", "There is a sofa in the living room."),
        (3, "Bedroom",     "නිදන කාමරය",    "The room where you sleep.",                "My bed is in the bedroom."),
        (4, "Kitchen",     "මුළුතැන්ගෙය",   "The room where you cook food.",            "My mother is in the kitchen."),
        (5, "Bathroom",    "නාන කාමරය",     "The room where you wash.",                 "The towels are in the bathroom."),
        (6, "Dining room", "ආහාර කාමරය",    "The room where you eat meals.",            "We eat dinner in the dining room."),
    ]
    for (disp, word, si, defn, example) in rooms:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 7, {"type": "heading", "text": "More Words"}, str(uuid7()))
    more_words = [
        (8,  "Garden", "උද්‍යානය", "The green space outside a house.", "The dog plays in the garden."),
        (9,  "Door",   "දොර",     "You open it to enter a room.",     "Please close the door."),
        (10, "Window", "ජනේලය",   "You look outside through it.",     "The chairs are near the window."),
    ]
    for (disp, word, si, defn, example) in more_words:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 11, {"type": "heading", "text": "Furniture"}, str(uuid7()))
    furniture = [
        (12, "Sofa",       "සෝෆාව",       "A long soft seat for two or more people.", "The sofa is in the living room."),
        (13, "Bed",        "ඇඳ",          "You sleep on it.",                         "My shoes are under the bed."),
        (14, "Table",      "මේසය",        "You put things on it.",                    "The book is on the table."),
        (15, "Chair",      "පුටුව",       "You sit on it.",                           "There are three chairs near the window."),
        (16, "Cupboard",   "අල්මාරිය",    "You keep clothes or plates inside it.",    "The plates are in the cupboard."),
        (17, "Television", "රූපවාහිනිය",  "You watch shows on it.",                   "The television is on the table."),
        (18, "Fridge",     "ශීතකරණය",     "It keeps food and drinks cold.",           "The milk is in the fridge."),
    ]
    for (disp, word, si, defn, example) in furniture:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 19,
        "Room or furniture? Match each word to its group",
        {
            "pairs": [
                {"id": "mp1", "left": "Living room", "right": "Room"},
                {"id": "mp2", "left": "Kitchen",     "right": "Room"},
                {"id": "mp3", "left": "Bed",         "right": "Furniture"},
                {"id": "mp4", "left": "Chair",       "right": "Furniture"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! Rooms and furniture sorted correctly.",
                "incorrect": "Rooms are places; furniture is the things inside them.",
            },
        },
        10, str(uuid7()),
    )
    insert_question(
        vocab_sec_id, "mcq_single", "assessment", 20,
        "Which of these is a room?",
        {
            "options": [
                {"id": "a", "text": "Bedroom"},
                {"id": "b", "text": "Sofa"},
                {"id": "c", "text": "Chair"},
                {"id": "d", "text": "Fridge"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! A bedroom is a room.",
                "incorrect": "Sofa, chair and fridge are furniture — bedroom is a room.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR — in / on / under, There is / There are
    # =========================================================================
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "Prepositions tell us where things are: in means inside (ඇතුළේ), "
            "on means touching the top (මත), under means below (යට)."
        ),
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "in / on / under",
        "sentences": [
            "The milk is in the fridge.",
            "The book is on the table.",
            "The shoes are under the bed.",
        ],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "There is / There are",
        "sentences": [
            "There is a sofa in the living room.",
            "There are two chairs in the living room.",
        ],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "Where is the book?",
        "answer": "It is on the table.",
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "Where are the shoes?",
        "answer": "They are under the bed.",
    }, str(uuid7()))

    prep_opts = [
        {"id": "a", "text": "in"},
        {"id": "b", "text": "on"},
        {"id": "c", "text": "under"},
    ]
    gram_fbo = [
        (5, "The book is ______ the table.",  prep_opts, "b",
         "Correct! The book is on the table.",
         "The book touches the top of the table — 'on'."),
        (6, "The shoes are ______ the bed.",  prep_opts, "c",
         "Correct! The shoes are under the bed.",
         "The shoes are below the bed — 'under'."),
        (7, "The milk is ______ the fridge.", prep_opts, "a",
         "Correct! The milk is in the fridge.",
         "The milk is inside the fridge — 'in'."),
        (8, "The shoes ______ under the bed.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "b",
         "Correct! 'Shoes' is plural, so we use 'are'.",
         "'Shoes' is plural — 'The shoes are under the bed.'"),
        (9, "The book ______ on the table.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'Book' is singular, so we use 'is'.",
         "'Book' is singular — 'The book is on the table.'"),
        (10, "There ______ a sofa in the living room.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! One sofa — 'There is'.",
         "Singular things use 'There is'."),
        (11, "There ______ two chairs in the bedroom.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "b",
         "Correct! Two chairs — 'There are'.",
         "Plural things use 'There are'."),
    ]
    for (disp, sentence, options, correct_id, fb_c, fb_i) in gram_fbo:
        insert_question(
            gram_sec_id, "fill_blank_options", "assessment", disp,
            sentence,
            {
                "sentence_with_blank": sentence,
                "options": options,
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    gram_fix = [
        (12, [{"id": "a", "text": "The shoes are under the bed."},
              {"id": "b", "text": "The shoes is under the bed."}], "a",
         "Correct! Plural 'shoes' takes 'are'.",
         "'Shoes' is plural, so 'The shoes are under the bed.'"),
        (13, [{"id": "a", "text": "There is a sofa in the living room."},
              {"id": "b", "text": "There are a sofa in the living room."}], "a",
         "Correct! One sofa takes 'There is'.",
         "One sofa — 'There is a sofa in the living room.'"),
    ]
    for (disp, options, correct_id, fb_c, fb_i) in gram_fix:
        insert_question(
            gram_sec_id, "mcq_single", "assessment", disp,
            "Choose the correct sentence.",
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # =========================================================================
    # PRONUNCIATION
    # =========================================================================
    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Focus Words"}, str(uuid7()))
    focus = [
        (1, "bedroom",  "බෙඩ්රූම් — two clear parts: bed + room"),
        (2, "cupboard", "කප්බඩ් — the 'p' is silent"),
        (3, "under",    "අන්ඩර් — say the 'r' clearly"),
        (4, "fridge",   "ෆ්‍රිජ්"),
    ]
    for (disp, word, note) in focus:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": word, "note": note}, str(uuid7()))

    insert_content_block(pron_sec_id, "text", 5, {"type": "heading", "text": "Practice Sentences"}, str(uuid7()))
    for (disp, phrase) in [
        (6,  "The bag is on the table."),
        (7,  "The book is in the cupboard."),
        (8,  "The cat is under the chair."),
        (9,  "The keys are on the table."),
        (10, "The television is on the wall."),
    ]:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    pron_qs = [
        (11, "Say the sentence. Stress the strong words: BAG, ON, TABLE.", "The bag is on the table."),
        (12, "Say the sentence. Remember the silent 'p' in cupboard.",     "The book is in the cupboard."),
        (13, "Say the sentence. Make 'under' clear.",                      "The cat is under the chair."),
    ]
    for (disp, prompt, target) in pron_qs:
        insert_question(
            pron_sec_id, "pronunciation_practice", "assessment", disp,
            prompt,
            {
                "target_text": target,
                "show_text_before_record": True,
                "max_duration_seconds": 10,
                "feedback": {
                    "correct": "Great! That was clear.",
                    "incorrect": "Try again — say the strong words clearly.",
                },
            },
            15, str(uuid7()),
        )

    # =========================================================================
    # LISTENING
    # =========================================================================
    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Dialogue — After School"}, str(uuid7()))
    insert_content_block(list_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "Father", "text": "Where is your bag?"},
            {"speaker": "Son",    "text": "It is on the table in the living room."},
            {"speaker": "Father", "text": "Where are your shoes?"},
            {"speaker": "Son",    "text": "They are under the bed."},
            {"speaker": "Father", "text": "Is your book in your bedroom?"},
            {"speaker": "Son",    "text": "Yes, it is. It is in my cupboard."},
            {"speaker": "Father", "text": "Good. Clean your room."},
        ],
    }, str(uuid7()))

    list_tf = [
        (2, "The bag is under the table. True or False?",   False,
         "Correct! The bag is on the table.",
         "The son says it is on the table in the living room."),
        (3, "The shoes are under the bed. True or False?",  True,
         "Correct! They are under the bed.",
         "The son says 'They are under the bed.'"),
        (4, "The book is in the kitchen. True or False?",   False,
         "Correct! The book is in the cupboard in his bedroom.",
         "The son says the book is in his cupboard."),
        (5, "The father asks about the shoes. True or False?", True,
         "Correct! He asks 'Where are your shoes?'",
         "The father asks 'Where are your shoes?'"),
    ]
    for (disp, prompt, answer, fb_c, fb_i) in list_tf:
        insert_question(
            list_sec_id, "true_false", "assessment", disp,
            prompt,
            {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    list_fbo = [
        (6, "The bag ______ on the table.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'Bag' is singular — 'is'.",
         "'Bag' is singular, so 'The bag is on the table.'"),
        (7, "The shoes ______ under the bed.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "b",
         "Correct! 'Shoes' is plural — 'are'.",
         "'Shoes' is plural, so 'The shoes are under the bed.'"),
    ]
    for (disp, sentence, options, correct_id, fb_c, fb_i) in list_fbo:
        insert_question(
            list_sec_id, "fill_blank_options", "assessment", disp,
            sentence,
            {
                "sentence_with_blank": sentence,
                "options": options,
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    who_says = [
        (8,  "Who says: 'Where is your bag?'",        "a",
         "Correct! The father asks about the bag.",
         "The father asks 'Where is your bag?'"),
        (9,  "Who says: 'They are under the bed.'",   "b",
         "Correct! The son answers about his shoes.",
         "The son answers 'They are under the bed.'"),
        (10, "Who says: 'Clean your room.'",          "a",
         "Correct! The father tells the son to clean his room.",
         "The father says 'Clean your room.'"),
    ]
    for (disp, prompt, correct_id, fb_c, fb_i) in who_says:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {
                "options": [{"id": "a", "text": "Father"}, {"id": "b", "text": "Son"}],
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    insert_question(
        list_sec_id, "mcq_single", "assessment", 11,
        "'Where are your shoes?' — choose the correct answer.",
        {
            "options": [
                {"id": "a", "text": "They are on the bed."},
                {"id": "b", "text": "They are under the bed."},
                {"id": "c", "text": "They are in the cupboard."},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! The shoes are under the bed.",
                "incorrect": "In the dialogue the shoes are under the bed.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "mcq_single", "assessment", 12,
        "'Where is your book?' — choose the correct answer.",
        {
            "options": [
                {"id": "a", "text": "It is in the cupboard."},
                {"id": "b", "text": "It is under the bed."},
                {"id": "c", "text": "It is on the sofa."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! The book is in the cupboard.",
                "incorrect": "In the dialogue the book is in the cupboard.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "fill_blank_options", "assessment", 13,
        "The book is ______ the cupboard.",
        {
            "sentence_with_blank": "The book is ______ the cupboard.",
            "options": prep_opts,
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! The book is in the cupboard.",
                "incorrect": "The book is inside the cupboard — 'in'.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # READING
    # =========================================================================
    insert_content_block(read_sec_id, "text", 0, {
        "type": "plain",
        "text": "Read the story and answer the questions.",
    }, str(uuid7()))
    insert_content_block(read_sec_id, "text", 1, {
        "type": "plain",
        "text": (
            "This is Tharushi's home. It is not very big, but it is "
            "comfortable and clean. There are five rooms in her house: a "
            "living room, a kitchen, a bathroom, and two bedrooms.\n\n"
            "In the living room, there is a large sofa and a small wooden "
            "table. The television is on the table. There are three chairs "
            "near the window. The room is bright and beautiful.\n\n"
            "In Tharushi's bedroom, there is a bed, a cupboard, and a study "
            "table. Her school bag is on the study table. Her shoes are under "
            "the bed. Her books are in the cupboard. There is also a small "
            "lamp on the table.\n\nIn the kitchen, there is a fridge and a "
            "cupboard. The milk is in the fridge. The plates are in the "
            "cupboard.\n\nTharushi loves her home because it is peaceful and "
            "tidy."
        ),
    }, str(uuid7()))

    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 2,
        "How many rooms are there in the house?",
        {
            "accepted_answers": ["five", "5", "five rooms", "5 rooms"],
            "feedback": {
                "correct": "Correct! There are five rooms.",
                "incorrect": "Read again — there are five rooms in her house.",
            },
        },
        5, str(uuid7()),
    )
    read_mcq = [
        (3, "Where is the television?",
         [{"id": "a", "text": "On the table"}, {"id": "b", "text": "On the wall"}, {"id": "c", "text": "In the cupboard"}], "a",
         "Correct! The television is on the table.",
         "The story says the television is on the table."),
        (4, "Where is Tharushi's school bag?",
         [{"id": "a", "text": "On the study table"}, {"id": "b", "text": "Under the bed"}], "a",
         "Correct! Her bag is on the study table.",
         "The story says her school bag is on the study table."),
        (5, "Where are her shoes?",
         [{"id": "a", "text": "Under the bed"}, {"id": "b", "text": "On the table"}], "a",
         "Correct! Her shoes are under the bed.",
         "The story says her shoes are under the bed."),
        (6, "Where are her books?",
         [{"id": "a", "text": "In the cupboard"}, {"id": "b", "text": "On the bed"}], "a",
         "Correct! Her books are in the cupboard.",
         "The story says her books are in the cupboard."),
        (7, "What is in the kitchen?",
         [{"id": "a", "text": "A fridge and a cupboard"}, {"id": "b", "text": "A sofa and a television"}], "a",
         "Correct! The kitchen has a fridge and a cupboard.",
         "The story says the kitchen has a fridge and a cupboard."),
        (8, "Is the living room dark or bright?",
         [{"id": "a", "text": "Bright"}, {"id": "b", "text": "Dark"}], "a",
         "Correct! The room is bright and beautiful.",
         "The story says the room is bright and beautiful."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in read_mcq:
        insert_question(
            read_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )
    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 9,
        "How many chairs are in the living room?",
        {
            "accepted_answers": ["three", "3", "three chairs", "3 chairs"],
            "feedback": {
                "correct": "Correct! There are three chairs near the window.",
                "incorrect": "Read again — there are three chairs near the window.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        read_sec_id, "true_false", "assessment", 10,
        "The house is very big. True or False?",
        {
            "correct_answer": False,
            "feedback": {
                "correct": "Correct! It is not very big, but comfortable and clean.",
                "incorrect": "The story says it is not very big.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # SPEAKING — content only
    # =========================================================================
    insert_content_block(speak_sec_id, "text", 0, {"type": "heading", "text": "Guided Speaking"}, str(uuid7()))
    for (disp, phrase) in [
        (1, "There is a sofa in the living room."),
        (2, "The television is on the table."),
        (3, "The shoes are under the bed."),
    ]:
        insert_content_block(speak_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "Where is the book?",
        "answer": "It is on the table.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 5, {
        "type": "qa_pair",
        "question": "Where are the shoes?",
        "answer": "They are under the bed.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 6, {
        "type": "plain",
        "text": (
            "Personal Speaking: talk about your bedroom for 30–45 seconds. "
            "Use 'There is / There are', two furniture words and two "
            "prepositions."
        ),
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 7, {
        "type": "example_cards",
        "label": "Example",
        "sentences": [
            "There is a bed in my bedroom.",
            "There is a table near the window.",
            "My bag is on the table.",
            "My shoes are under the bed.",
        ],
    }, str(uuid7()))

    # =========================================================================
    # WRITING
    # =========================================================================
    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Type the missing word, then fix the broken sentences.",
    }, str(uuid7()))

    fills = [
        (1, "The book is ______ the table.",              ["on"],
         "Correct! The book is on the table.",
         "The book touches the top of the table — 'on'."),
        (2, "The shoes are ______ the bed.",              ["under"],
         "Correct! The shoes are under the bed.",
         "The shoes are below the bed — 'under'."),
        (3, "The milk is ______ the fridge.",             ["in"],
         "Correct! The milk is in the fridge.",
         "The milk is inside the fridge — 'in'."),
        (4, "There ______ a sofa in the living room.",    ["is"],
         "Correct! One sofa — 'There is'.",
         "Singular things use 'There is'."),
        (5, "There ______ two chairs in the bedroom.",    ["are"],
         "Correct! Two chairs — 'There are'.",
         "Plural things use 'There are'."),
    ]
    for (disp, sentence, accepted, fb_c, fb_i) in fills:
        insert_question(
            write_sec_id, "fill_blank_typed", "assessment", disp,
            sentence,
            {
                "accepted_answers": accepted,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    corrections = [
        (6, "Fix the mistake and type the correct sentence: 'The shoes is under the bed.'",
         ["The shoes are under the bed", "The shoes are under the bed."],
         "Correct! Plural 'shoes' takes 'are'.",
         "'Shoes' is plural: 'The shoes are under the bed.'"),
        (7, "Fix the mistake and type the correct sentence: 'There are a sofa in the living room.'",
         ["There is a sofa in the living room", "There is a sofa in the living room."],
         "Correct! One sofa takes 'There is'.",
         "One sofa: 'There is a sofa in the living room.'"),
        (8, "Fix the mistake and type the correct sentence: 'The milk are in the fridge.'",
         ["The milk is in the fridge", "The milk is in the fridge."],
         "Correct! 'Milk' takes 'is'.",
         "'Milk' is singular: 'The milk is in the fridge.'"),
    ]
    for (disp, prompt, accepted, fb_c, fb_i) in corrections:
        insert_question(
            write_sec_id, "fill_blank_typed", "assessment", disp,
            prompt,
            {
                "accepted_answers": accepted,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            8, str(uuid7()),
        )

    insert_content_block(write_sec_id, "self_check", 9, {
        "prompt": "Can you write this on your own?",
        "text": (
            "Write 6–8 sentences about your home.\nInclude 3 rooms, 3 "
            "furniture items, 3 prepositions and one 'There are' sentence."
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 10, {
        "type": "summary",
        "items": [
            "Name the rooms in a home and common furniture",
            "Use in, on and under to say where things are",
            "Use 'There is' for one thing and 'There are' for many",
            "Ask and answer 'Where is...?' and 'Where are...?'",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 7
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
