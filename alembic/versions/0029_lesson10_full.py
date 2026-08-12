"""Lesson 10 — My Town & Community (Level 1 final integrated lesson).

Seeds Beginner A Lesson 10 with all 7 sections from the Level 1 lesson 10 PDF:
  Vocabulary  — 14 word cards (Places in Town) + 2 assessment questions
  Grammar     — integrated review (There is/are, can/can't, a/any) + 12 questions
  Pronunciation — place-word syllable cards + 3 pronunciation questions
  Listening   — Nimal & Sara town-comparison dialogue + 12 questions
  Reading     — Aruni's town story + 8 assessment questions
  Speaking    — structured 60-second talk + role-play prompts, content only
  Writing     — 3 typed fills + 3 typed corrections + self_check + summary

Text-only scope: picture/audio activities deferred until assets exist; audio
lines are embedded in question prompts (0020 convention).

Sinhala vocabulary translations reconstructed from the PDF (embedded font
mangles extracted Sinhala glyphs) — flag for content-team review.

Revision ID: c6d7e8f9a0b1
Revises:     b5c6d7e8f9a0
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

revision: str = "c6d7e8f9a0b1"
down_revision: Union[str, None] = "b5c6d7e8f9a0"
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
    "Describe your town using There is / There are accurately",
    "Ask and answer questions about places in town",
    "Use adjectives, prepositions, and can/can't together",
    "Compare two towns using simple comparative ideas (bigger, smaller)",
    "Speak for 60 seconds about a familiar topic",
    "Write a structured paragraph",
    "Apply grammar from the entire Level 1 course",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    l10_id = ensure_lesson(
        bind, level_id, 10,
        "My Town & Community",
        "Describe your town with There is / There are and bring together everything from Level 1.",
        str(uuid7()),
    )
    op.execute(f"UPDATE lesson SET objectives = {_j(OBJECTIVES)} WHERE id = '{l10_id}'")

    vocab_sec_id = ensure_section(bind, l10_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id  = ensure_section(bind, l10_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id  = ensure_section(bind, l10_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id  = ensure_section(bind, l10_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id  = ensure_section(bind, l10_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id = ensure_section(bind, l10_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id = ensure_section(bind, l10_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY — Places in Town
    # =========================================================================
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: name the places "
            "in a town, describe your town with 'There is / There are', and "
            "use everything you learned in Level 1 together."
        ),
    }, str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Places in Town"}, str(uuid7()))
    places = [
        (2,  "School",         "පාසල",             "A place where children learn.",        "There are four schools near the park."),
        (3,  "Hospital",       "රෝහල",             "A place where sick people get help.",  "There is a big hospital in the town center."),
        (4,  "Supermarket",    "සුපිරි වෙළඳසැල",   "A big shop for food and things.",      "The bank is next to the supermarket."),
        (5,  "Park",           "උද්‍යානය",          "A green place to play and relax.",     "Children can play in the park."),
        (6,  "Bank",           "බැංකුව",            "A place that keeps money safe.",       "Is there a bank near your house?"),
        (7,  "Library",        "පුස්තකාලය",         "A place with many books to read.",     "I read books at the library."),
        (8,  "Cinema",         "සිනමාහල",           "A place to watch movies.",             "There isn't a cinema in my town."),
        (9,  "Museum",         "කෞතුකාගාරය",        "A place with old and interesting things.", "There is a museum near the park."),
        (10, "Market",         "වෙළඳපොළ",           "A place to buy fresh food.",           "The market is next to the bus station."),
        (11, "Train station",  "දුම්රිය ස්ථානය",    "A place where trains stop.",           "There is a train station in the center."),
        (12, "Shopping mall",  "සාප්පු සංකීර්ණය",   "A big building with many shops.",      "There is a large shopping mall near the park."),
        (13, "Playground",     "ක්‍රීඩා පිටිය",     "A place where children play.",         "Children can play in the playground."),
        (14, "Restaurant",     "අවන්හල",            "A place to eat meals.",                "There are many restaurants in the town center."),
        (15, "Police station", "පොලිස් ස්ථානය",     "A place where police officers work.",  "The police station is near the bank."),
    ]
    for (disp, word, si, defn, example) in places:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 16,
        "Match each word to its meaning",
        {
            "pairs": [
                {"id": "mp1", "left": "busier", "right": "More active"},
                {"id": "mp2", "left": "modern", "right": "New"},
                {"id": "mp3", "left": "quiet",  "right": "Not noisy"},
                {"id": "mp4", "left": "near",   "right": "Close to"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! You know these describing words.",
                "incorrect": "Think about what each word tells you about a place.",
            },
        },
        10, str(uuid7()),
    )
    insert_question(
        vocab_sec_id, "mcq_single", "assessment", 17,
        "What does 'town center' mean?",
        {
            "options": [
                {"id": "a", "text": "The middle of the town"},
                {"id": "b", "text": "Outside the town"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! The town center is the middle of the town.",
                "incorrect": "The town center is the middle of the town.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR — Integrated review
    # =========================================================================
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "This lesson brings Level 1 grammar together: 'There is' for one "
            "thing, 'There are' for many, 'There isn't a...' for the "
            "negative, can / can't for abilities, and in / on / under / near "
            "for places."
        ),
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "There is / There are",
        "sentences": [
            "There is a museum near the park.",
            "There are three schools in my town.",
        ],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "Negative",
        "sentences": [
            "There isn't a cinema in my village.",
            "There aren't any shops here.",
        ],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "Is there a bus station?",
        "answer": "Yes, there is.",
    }, str(uuid7()))

    is_are = [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}]
    can_cant = [{"id": "a", "text": "can"}, {"id": "b", "text": "can't"}]
    gram_fbo = [
        (4, "There ___ a museum near the park.",   is_are, "a",
         "Correct! One museum — 'There is'.",
         "One museum — 'There is a museum near the park.'"),
        (5, "There ___ three schools in my town.", is_are, "b",
         "Correct! Three schools — 'There are'.",
         "Plural — 'There are three schools.'"),
        (6, "Children ___ play in the playground.", can_cant, "a",
         "Correct! A playground is for playing — children can play there.",
         "A playground is for playing — 'Children can play.'"),
        (7, "There isn't ___ cinema in my village.",
         [{"id": "a", "text": "a"}, {"id": "b", "text": "any"}], "a",
         "Correct! 'There isn't a cinema' — singular uses 'a'.",
         "Singular negative uses 'a': 'There isn't a cinema.'"),
        (8, "People ___ swim in the river because it is dirty.", can_cant, "b",
         "Correct! The river is dirty, so people can't swim there.",
         "The river is dirty — 'People can't swim in it.'"),
        (9, "The park is big and clean. Children ___ play there.", can_cant, "a",
         "Correct! A big, clean park is safe to play in.",
         "The park is big and clean — 'Children can play there.'"),
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

    insert_question(
        gram_sec_id, "mcq_single", "assessment", 10,
        "There ___ many shops in the town center and there ___ a hospital near them.",
        {
            "options": [
                {"id": "a", "text": "are / is"},
                {"id": "b", "text": "is / are"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Many shops → 'are'; one hospital → 'is'.",
                "incorrect": "Many shops take 'are'; one hospital takes 'is'.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        gram_sec_id, "mcq_single", "assessment", 11,
        "'Is there a bus station?' — choose the correct answer.",
        {
            "options": [
                {"id": "a", "text": "Yes, there is."},
                {"id": "b", "text": "Yes, there are."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Is there...?' is answered with 'Yes, there is.'",
                "incorrect": "'Is there...?' is answered with 'Yes, there is.'",
            },
        },
        5, str(uuid7()),
    )

    gram_fix = [
        (12, [{"id": "a", "text": "There is a hospital in my town."},
              {"id": "b", "text": "There are a hospital in my town."}], "a",
         "Correct! One hospital takes 'There is'.",
         "One hospital — 'There is a hospital in my town.'"),
        (13, [{"id": "a", "text": "There are two parks near my house."},
              {"id": "b", "text": "There is two parks near my house."}], "a",
         "Correct! Two parks take 'There are'.",
         "Two parks — 'There are two parks near my house.'"),
        (14, [{"id": "a", "text": "Children can play in the park."},
              {"id": "b", "text": "Children can plays in the park."}], "a",
         "Correct! After 'can' the verb never changes.",
         "After 'can' use the base verb: 'Children can play.'"),
        (15, [{"id": "a", "text": "There aren't any shops here."},
              {"id": "b", "text": "There isn't any shops here."}], "a",
         "Correct! Plural negative uses 'aren't any'.",
         "Plural 'shops' — 'There aren't any shops here.'"),
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
    # PRONUNCIATION — place words
    # =========================================================================
    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Say the Syllables"}, str(uuid7()))
    focus = [
        (1, "Station",    "STA-tion — ස්ටේ-ෂන්"),
        (2, "Museum",     "mu-SE-um — මියූ-සියම්"),
        (3, "Restaurant", "RES-tau-rant — රෙස්-ටො-රන්ට්"),
        (4, "Library",    "LI-bra-ry — ලයි-බ්‍රරි"),
        (5, "Cinema",     "CI-ne-ma — සි-න-මා"),
    ]
    for (disp, word, note) in focus:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": word, "note": note}, str(uuid7()))

    pron_qs = [
        (6, "Say the word in two clear parts: STA-tion.",     "Station"),
        (7, "Say the word in three clear parts: mu-SE-um.",   "Museum"),
        (8, "Say the sentence clearly.",                      "There is a library near the park."),
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
                    "incorrect": "Try again — say each syllable clearly.",
                },
            },
            15, str(uuid7()),
        )

    # =========================================================================
    # LISTENING — Comparing Two Towns
    # =========================================================================
    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Dialogue — Comparing Towns"}, str(uuid7()))
    insert_content_block(list_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "Nimal", "text": "Is there a hospital in your town?"},
            {"speaker": "Sara",  "text": "Yes, there is a big hospital near the market. It is next to the bus station."},
            {"speaker": "Nimal", "text": "That's good. Are there any cinemas?"},
            {"speaker": "Sara",  "text": "Yes, there are two cinemas in the town center. They are new and modern."},
            {"speaker": "Nimal", "text": "Wow! In my town, there isn't a cinema, but there is a large shopping mall near the park."},
            {"speaker": "Sara",  "text": "Is your town big?"},
            {"speaker": "Nimal", "text": "No, it isn't very big, but it is clean and quiet. There are many trees and small shops."},
            {"speaker": "Sara",  "text": "My town is bigger and busier. There are many restaurants and cafés. People can eat and shop there."},
            {"speaker": "Nimal", "text": "Can children play in parks there?"},
            {"speaker": "Sara",  "text": "Yes, they can. There are three parks. One park is very big and children can play football there."},
            {"speaker": "Nimal", "text": "That sounds nice! I think your town is more exciting than mine."},
        ],
    }, str(uuid7()))

    detail_mcq = [
        (2, "How many cinemas are there in Sara's town?",
         [{"id": "a", "text": "One"}, {"id": "b", "text": "Two"}, {"id": "c", "text": "Three"}], "b",
         "Correct! There are two cinemas in the town center.",
         "Sara says there are two cinemas in the town center."),
        (3, "Where is the hospital?",
         [{"id": "a", "text": "Near the market"}, {"id": "b", "text": "Near the park"}, {"id": "c", "text": "Near the school"}], "a",
         "Correct! The hospital is near the market.",
         "Sara says the big hospital is near the market."),
        (4, "Is there a cinema in Nimal's town?",
         [{"id": "a", "text": "Yes"}, {"id": "b", "text": "No"}], "b",
         "Correct! There isn't a cinema in Nimal's town.",
         "Nimal says 'in my town, there isn't a cinema.'"),
        (5, "How many parks are there in Sara's town?",
         [{"id": "a", "text": "One"}, {"id": "b", "text": "Two"}, {"id": "c", "text": "Three"}], "c",
         "Correct! There are three parks.",
         "Sara says there are three parks."),
        (6, "What is near the park in Nimal's town?",
         [{"id": "a", "text": "A shopping mall"}, {"id": "b", "text": "A hospital"}, {"id": "c", "text": "A cinema"}], "a",
         "Correct! There is a large shopping mall near the park.",
         "Nimal says there is a large shopping mall near the park."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in detail_mcq:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    towns = [{"id": "a", "text": "Sara's"}, {"id": "b", "text": "Nimal's"}]
    compare_mcq = [
        (7, "Whose town is bigger?",            towns, "a",
         "Correct! Sara says her town is bigger and busier.",
         "Sara says 'My town is bigger and busier.'"),
        (8, "Which town is quieter?",           towns, "b",
         "Correct! Nimal's town is clean and quiet.",
         "Nimal says his town is clean and quiet."),
        (9, "Which town has a shopping mall?",  towns, "b",
         "Correct! Nimal's town has a large shopping mall near the park.",
         "Nimal says his town has a large shopping mall."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in compare_mcq:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    list_fbo = [
        (10, "There ___ two cinemas in Sara's town.",           is_are, "b",
         "Correct! Two cinemas — 'There are'.",
         "Two cinemas — 'There are two cinemas.'"),
        (11, "There ___ a large shopping mall in Nimal's town.", is_are, "a",
         "Correct! One mall — 'There is'.",
         "One shopping mall — 'There is a large shopping mall.'"),
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

    infer_mcq = [
        (12, "Why does Nimal think Sara's town is exciting?",
         [{"id": "a", "text": "It has more places and activities"},
          {"id": "b", "text": "It is very small"}], "a",
         "Correct! Her town has cinemas, restaurants and parks.",
         "Sara's town has more places and activities."),
        (13, "Why is Nimal's town quiet?",
         [{"id": "a", "text": "It has many trees and small shops"},
          {"id": "b", "text": "It has many cinemas"}], "a",
         "Correct! Many trees and small shops make it quiet.",
         "Nimal says his town has many trees and small shops."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in infer_mcq:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # =========================================================================
    # READING — Aruni's town
    # =========================================================================
    insert_content_block(read_sec_id, "text", 0, {
        "type": "plain",
        "text": "Read the text and answer the questions.",
    }, str(uuid7()))
    insert_content_block(read_sec_id, "text", 1, {
        "type": "plain",
        "text": (
            "This is Aruni's town. It is smaller than Colombo, but it is "
            "very peaceful and clean. There is a large hospital in the town "
            "center and there are four schools near the park. The park is "
            "beautiful and children can play safely there every evening.\n\n"
            "There is a busy market next to the bus station. People can buy "
            "fresh vegetables and fruits there. However, there isn't a "
            "cinema in Aruni's town, so many people travel to the next town "
            "to watch movies.\n\nAruni likes her town because it is friendly "
            "and safe. She walks to school every morning because it is near "
            "her house. On weekends, she goes to the park with her family."
        ),
    }, str(uuid7()))

    insert_question(
        read_sec_id, "mcq_single", "assessment", 2,
        "Is Aruni's town big or small?",
        {
            "options": [
                {"id": "a", "text": "Small — it is smaller than Colombo"},
                {"id": "b", "text": "Big — it is bigger than Colombo"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! It is smaller than Colombo.",
                "incorrect": "The text says it is smaller than Colombo.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 3,
        "How many schools are there?",
        {
            "accepted_answers": ["four", "4", "four schools", "4 schools"],
            "feedback": {
                "correct": "Correct! There are four schools near the park.",
                "incorrect": "Read again — there are four schools near the park.",
            },
        },
        5, str(uuid7()),
    )
    read_mcq = [
        (4, "What can children do in the park?",
         [{"id": "a", "text": "Play safely every evening"}, {"id": "b", "text": "Watch movies"}], "a",
         "Correct! Children can play safely there every evening.",
         "The text says children can play safely there every evening."),
        (5, "Why do people travel to the next town?",
         [{"id": "a", "text": "To watch movies"}, {"id": "b", "text": "To buy vegetables"}], "a",
         "Correct! There isn't a cinema, so they travel to watch movies.",
         "There isn't a cinema in Aruni's town, so people travel to watch movies."),
        (6, "Where is the market?",
         [{"id": "a", "text": "Next to the bus station"}, {"id": "b", "text": "Near the hospital"}], "a",
         "Correct! The busy market is next to the bus station.",
         "The text says there is a busy market next to the bus station."),
        (7, "Why does Aruni like her town?",
         [{"id": "a", "text": "It is friendly and safe"}, {"id": "b", "text": "It is big and busy"}], "a",
         "Correct! She likes it because it is friendly and safe.",
         "The text says she likes her town because it is friendly and safe."),
        (8, "How does Aruni go to school?",
         [{"id": "a", "text": "She walks"}, {"id": "b", "text": "She goes by bus"}], "a",
         "Correct! She walks because the school is near her house.",
         "The text says she walks to school every morning."),
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
        read_sec_id, "true_false", "assessment", 9,
        "Aruni's town is busy and noisy. True or False?",
        {
            "correct_answer": False,
            "feedback": {
                "correct": "Correct! It is very peaceful and clean.",
                "incorrect": "The text says it is very peaceful and clean.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # SPEAKING — content only
    # =========================================================================
    insert_content_block(speak_sec_id, "text", 0, {"type": "heading", "text": "Structured 60-Second Talk"}, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 1, {
        "type": "plain",
        "text": (
            "Talk about your town for 60 seconds. Include: 5 places, 2 "
            "adjectives, 1 negative sentence, 1 ability sentence, 1 "
            "preposition and 1 comparison."
        ),
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "Example",
        "sentences": [
            "My town is small but beautiful.",
            "There is a hospital near my house.",
            "There are two parks in the town center.",
            "There isn't a cinema.",
            "Children can play in the park.",
            "My town is smaller than the city.",
        ],
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "Is there a bank near your house?",
        "answer": "Yes, there is. It is next to the supermarket.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "Can children play there?",
        "answer": "Yes, they can. They can play football and ride bicycles.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 5, {
        "type": "qa_pair",
        "question": "Is your town big?",
        "answer": "It isn't very big, but it is clean and quiet.",
    }, str(uuid7()))

    # =========================================================================
    # WRITING
    # =========================================================================
    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Type the missing word, then fix the broken sentences.",
    }, str(uuid7()))

    fills = [
        (1, "There ______ a hospital near my house.",       ["is"],
         "Correct! One hospital — 'There is'.",
         "One hospital — 'There is a hospital near my house.'"),
        (2, "There ______ two parks in the town center.",   ["are"],
         "Correct! Two parks — 'There are'.",
         "Two parks — 'There are two parks in the town center.'"),
        (3, "People ______ play football in the park.",     ["can"],
         "Correct! The park is for playing — people can play there.",
         "The park is for playing — 'People can play football.'"),
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
        (4, "Fix the mistake and type the correct sentence: 'There are a hospital in my town.'",
         ["There is a hospital in my town", "There is a hospital in my town."],
         "Correct! One hospital takes 'There is'.",
         "One hospital: 'There is a hospital in my town.'"),
        (5, "Fix the mistake and type the correct sentence: 'Children can plays in the park.'",
         ["Children can play in the park", "Children can play in the park."],
         "Correct! After 'can' the verb never changes.",
         "After 'can' use the base verb: 'Children can play in the park.'"),
        (6, "Fix the mistake and type the correct sentence: 'There is two parks near my house.'",
         ["There are two parks near my house", "There are two parks near my house."],
         "Correct! Two parks take 'There are'.",
         "Two parks: 'There are two parks near my house.'"),
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

    insert_content_block(write_sec_id, "self_check", 7, {
        "prompt": "Can you write this on your own?",
        "text": (
            "Write 10–12 sentences about your town.\nInclude 6 places, 2 "
            "adjectives, 1 negative sentence, 1 ability sentence, 1 "
            "comparison, 1 preposition and 1 opinion sentence.\n\nSentence "
            "starters: My town is ___ and ___. There is a ___ near my "
            "house. There are ___ in the town center. There isn't a ___ in "
            "my town. People can ___ in the ___. My town is ___ than ___. "
            "I think my town is ___ because ___."
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 8, {
        "type": "summary",
        "items": [
            "Name the places in a town",
            "Describe your town with 'There is / There are'",
            "Use adjectives, prepositions and can/can't together",
            "Compare two towns with bigger and smaller",
            "You finished Level 1 — well done!",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 10
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
