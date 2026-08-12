"""Lesson 6 — Food, Drinks & Preferences (Level 1 batch 2 seed).

Seeds Beginner A Lesson 6 with all 7 sections from the Level 1 lesson 6 PDF:
  Vocabulary  — 10 word cards (Food / Drinks) + 2 assessment questions
  Grammar     — like / don't like teaching blocks + 10 assessment questions
  Pronunciation — phrase cards + 3 pronunciation_practice questions
  Listening   — Anna & Tom dialogue + 4 assessment questions
  Reading     — Kavindu & Malmi story + 14 assessment questions
  Speaking    — guided speaking phrase cards, content only
  Writing     — 4 sentence_builder + 3 typed corrections + self_check + summary

Text-only scope: picture-tap and audio-select activities from the PDF are
deferred until image/audio assets exist. Audio lines are embedded in question
prompts (same convention as 0020's listening section).

Sinhala vocabulary translations were reconstructed from the PDF (its embedded
font mangles extracted Sinhala glyphs) — flag for content-team review.

Revision ID: e2f3a4b5c6d7
Revises:     d1e2f3a4b5c6
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

revision: str = "e2f3a4b5c6d7"
down_revision: Union[str, None] = "d1e2f3a4b5c6"
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
    """insert_word_card + Sinhala translation ({"si": {"word": ...}} — the
    format the admin API reads)."""
    op.execute(
        f"INSERT INTO vocabulary_word "
        f"(id, lesson_section_id, word, definition, example_sentence, difficulty, translations) "
        f"VALUES ('{ww_id}', '{section_id}', {_s(word)}, {_s(definition)}, "
        f"{_s(example)}, 'easy', {_j({'si': {'word': word_si}})})"
    )
    insert_content_block(section_id, "word_card", display_order, {"vocabulary_word_id": ww_id}, cb_id)


OBJECTIVES = [
    "Identify vocabulary for common food and drinks",
    "Use like and don't like to express preferences clearly",
    "Ask and answer simple questions about food and drink preferences",
    "Understand spoken conversations about food and eating habits",
    "Pronounce food vocabulary and sentence patterns clearly",
    "Speak about your food likes and dislikes with confidence",
    "Write short sentences about your food preferences",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    l6_id = ensure_lesson(
        bind, level_id, 6,
        "Food, Drinks & Preferences",
        "Learn food and drink words and say what you like and don't like.",
        str(uuid7()),
    )
    op.execute(f"UPDATE lesson SET objectives = {_j(OBJECTIVES)} WHERE id = '{l6_id}'")

    vocab_sec_id = ensure_section(bind, l6_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id  = ensure_section(bind, l6_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id  = ensure_section(bind, l6_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id  = ensure_section(bind, l6_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id  = ensure_section(bind, l6_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id = ensure_section(bind, l6_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id = ensure_section(bind, l6_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY
    # =========================================================================
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: name common food "
            "and drinks, say what you like and don't like, and ask and answer "
            "simple questions about food."
        ),
    }, str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Food"}, str(uuid7()))
    food_words = [
        (2, "Apple",   "ඇපල්",      "A round red or green fruit.",            "I eat an apple every day."),
        (3, "Banana",  "කෙසෙල්",    "A long yellow fruit.",                   "The banana is sweet."),
        (4, "Rice",    "බත්",       "Cooked grains eaten as a main food.",    "We eat rice every day."),
        (5, "Pizza",   "පීට්සා",    "A flat round food with cheese on top.",  "I like pizza very much."),
        (6, "Bread",   "පාන්",      "A baked food made from flour.",          "I eat bread in the morning."),
        (7, "Chicken", "කුකුල් මස්", "Meat from a hen.",                       "My mother cooks chicken."),
    ]
    for (disp, word, si, defn, example) in food_words:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 8, {"type": "heading", "text": "Drinks"}, str(uuid7()))
    drink_words = [
        (9,  "Milk",  "කිරි",  "A white drink from cows.",         "I drink milk in the morning."),
        (10, "Juice", "ජූස්",  "A drink made from fruit.",         "I drink juice in the afternoon."),
        (11, "Tea",   "තේ",    "A hot drink made from leaves.",    "My father drinks tea."),
        (12, "Water", "වතුර",  "A clear drink everyone needs.",    "I drink water every day."),
    ]
    for (disp, word, si, defn, example) in drink_words:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 13,
        "Match each word to its group",
        {
            "pairs": [
                {"id": "mp1", "left": "Apple",   "right": "Food"},
                {"id": "mp2", "left": "Chicken", "right": "Food"},
                {"id": "mp3", "left": "Milk",    "right": "Drink"},
                {"id": "mp4", "left": "Tea",     "right": "Drink"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! You know your food and drinks.",
                "incorrect": "Think about which words are things you eat and which you drink.",
            },
        },
        10, str(uuid7()),
    )
    insert_question(
        vocab_sec_id, "mcq_single", "assessment", 14,
        "Which of these is a drink?",
        {
            "options": [
                {"id": "a", "text": "Juice"},
                {"id": "b", "text": "Bread"},
                {"id": "c", "text": "Rice"},
                {"id": "d", "text": "Pizza"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Juice is a drink.",
                "incorrect": "Bread, rice and pizza are food — juice is a drink.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR — like / don't like
    # =========================================================================
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "We use 'like' to talk about food we enjoy and 'don't like' for "
            "food we do not enjoy. The pattern is: I like + noun, "
            "I don't like + noun."
        ),
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "Like / Don't Like",
        "sentences": ["I like pizza.", "I don't like milk."],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 2, {
        "type": "qa_pair",
        "question": "Do you like rice?",
        "answer": "Yes, I do.",
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "Do you like milk?",
        "answer": "No, I don't.",
    }, str(uuid7()))

    gram_fbo = [
        (4, "___ you like rice?",
         [{"id": "a", "text": "Do"}, {"id": "b", "text": "Does"}, {"id": "c", "text": "Are"}], "a",
         "Correct! Questions with 'you' use 'Do'.",
         "With 'you' we ask: 'Do you like rice?'"),
        (5, "Do you like rice? — Yes, I ___.",
         [{"id": "a", "text": "do"}, {"id": "b", "text": "don't"}, {"id": "c", "text": "like"}], "a",
         "Correct! The short answer is 'Yes, I do.'",
         "A yes answer is 'Yes, I do.'"),
        (6, "Do you like tea? — No, I ___.",
         [{"id": "a", "text": "do"}, {"id": "b", "text": "don't"}], "b",
         "Correct! The short answer is 'No, I don't.'",
         "A no answer is 'No, I don't.'"),
        (7, "He ______ pizza. (He loves it.)",
         [{"id": "a", "text": "like"}, {"id": "b", "text": "likes"}], "b",
         "Correct! With 'he' and 'she' we add -s: 'He likes pizza.'",
         "With 'he' and 'she' we use 'likes'."),
        (8, "She ______ milk. (She never drinks it.)",
         [{"id": "a", "text": "likes"}, {"id": "b", "text": "doesn't like"}], "b",
         "Correct! 'She doesn't like milk.'",
         "She never drinks it, so 'She doesn't like milk.'"),
        (9, "She ______ juice. (She drinks it every day.)",
         [{"id": "a", "text": "likes"}, {"id": "b", "text": "don't like"}], "a",
         "Correct! 'She likes juice.'",
         "She drinks it every day, so 'She likes juice.'"),
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
        (10, [{"id": "a", "text": "I like rice."},        {"id": "b", "text": "I likes rice."}], "a",
         "Correct! With 'I' we use 'like'.",
         "With 'I' we use 'like', not 'likes'."),
        (11, [{"id": "a", "text": "He likes milk."},      {"id": "b", "text": "He like milk."}], "a",
         "Correct! With 'he' we use 'likes'.",
         "With 'he' we add -s: 'He likes milk.'"),
        (12, [{"id": "a", "text": "She doesn't like tea."}, {"id": "b", "text": "She don't like tea."}], "a",
         "Correct! With 'she' we use 'doesn't'.",
         "With 'she' we use 'doesn't like'."),
        (13, [{"id": "a", "text": "I don't like pizza."},  {"id": "b", "text": "I doesn't like pizza."}], "a",
         "Correct! With 'I' we use 'don't'.",
         "With 'I' we use 'don't like'."),
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
    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Don't and Like"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 1, {"type": "phrase_card", "text": "don't", "note": "/doʊnt/ — ඩෝන්ට්"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 2, {"type": "phrase_card", "text": "like",  "note": "/laɪk/ — ලයික්"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 3, {"type": "heading", "text": "Practice"}, str(uuid7()))
    for (disp, phrase) in [
        (4, "I like rice."),
        (5, "I don't like tea."),
        (6, "I like ice cream."),
        (7, "I don't like chocolate ice cream."),
    ]:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    pron_qs = [
        (8,  "Say the sentence clearly.",                        "I like rice."),
        (9,  "Say the sentence. Make the 't' in \"don't\" clear.", "I don't like tea."),
        (10, "Say the long sentence slowly and clearly.",        "I don't like chocolate ice cream."),
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
                    "incorrect": "Try again — say each word slowly and clearly.",
                },
            },
            15, str(uuid7()),
        )

    # =========================================================================
    # LISTENING
    # =========================================================================
    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Dialogue — Do You Like...?"}, str(uuid7()))
    insert_content_block(list_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "Anna", "text": "Hi Tom!"},
            {"speaker": "Tom",  "text": "Hi Anna!"},
            {"speaker": "Anna", "text": "Do you like pizza?"},
            {"speaker": "Tom",  "text": "Yes, I do. I like pizza very much."},
            {"speaker": "Anna", "text": "Do you like rice?"},
            {"speaker": "Tom",  "text": "Yes, I do. I like rice."},
            {"speaker": "Anna", "text": "Do you like milk?"},
            {"speaker": "Tom",  "text": "No, I don't. I don't like milk."},
            {"speaker": "Anna", "text": "Do you like juice?"},
            {"speaker": "Tom",  "text": "Yes, I do. I like juice."},
            {"speaker": "Anna", "text": "What about tea?"},
            {"speaker": "Tom",  "text": "No, I don't like tea."},
            {"speaker": "Anna", "text": "Oh, I like tea!"},
        ],
    }, str(uuid7()))

    insert_question(
        list_sec_id, "mcq_single", "assessment", 2,
        "Anna says: 'I like tea.' Who likes tea?",
        {
            "options": [{"id": "a", "text": "Tom"}, {"id": "b", "text": "Anna"}],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! Anna says 'Oh, I like tea!'",
                "incorrect": "Anna says 'Oh, I like tea!' — Anna likes tea.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "mcq_single", "assessment", 3,
        "Who likes juice?",
        {
            "options": [{"id": "a", "text": "Tom"}, {"id": "b", "text": "Anna"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Tom says 'I like juice.'",
                "incorrect": "Tom says 'Yes, I do. I like juice.'",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "mcq_single", "assessment", 4,
        "Does Tom like milk?",
        {
            "options": [
                {"id": "a", "text": "Yes, he does."},
                {"id": "b", "text": "No, he doesn't."},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! Tom says 'I don't like milk.'",
                "incorrect": "Tom says 'No, I don't. I don't like milk.'",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "true_false", "assessment", 5,
        "Tom likes pizza very much. True or False?",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Correct! Tom says 'I like pizza very much.'",
                "incorrect": "Tom says 'I like pizza very much.' — it is true.",
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
            "This is Kavindu and his sister Malmi. They are at home after "
            "school. Kavindu is hungry. He likes rice and chicken very much. "
            "He also likes juice and water. Every day, he drinks juice in the "
            "afternoon. However, he doesn't like milk. He doesn't like tea "
            "either.\n\nMalmi is different. She likes milk and tea. She drinks "
            "milk in the morning. She doesn't like juice, but she likes rice "
            "and bread. Kavindu and Malmi like some of the same food, but "
            "they like different drinks."
        ),
    }, str(uuid7()))

    read_tf = [
        (2, "Kavindu likes rice. True or False?",        True,
         "Correct! Kavindu likes rice and chicken very much.",
         "The story says Kavindu likes rice and chicken very much."),
        (3, "Kavindu likes milk. True or False?",        False,
         "Correct! Kavindu doesn't like milk.",
         "The story says he doesn't like milk."),
        (4, "Malmi likes tea. True or False?",           True,
         "Correct! Malmi likes milk and tea.",
         "The story says Malmi likes milk and tea."),
        (5, "Malmi likes juice. True or False?",         False,
         "Correct! Malmi doesn't like juice.",
         "The story says she doesn't like juice."),
        (6, "They like the same drinks. True or False?", False,
         "Correct! They like different drinks.",
         "The story ends: 'they like different drinks.'"),
    ]
    for (disp, prompt, answer, fb_c, fb_i) in read_tf:
        insert_question(
            read_sec_id, "true_false", "assessment", disp,
            prompt,
            {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    read_mcq = [
        (7, "What does Kavindu drink in the afternoon?",
         [{"id": "a", "text": "Milk"}, {"id": "b", "text": "Juice"}], "b",
         "Correct! He drinks juice in the afternoon.",
         "The story says he drinks juice in the afternoon."),
        (8, "What does Malmi drink in the morning?",
         [{"id": "a", "text": "Tea"}, {"id": "b", "text": "Milk"}], "b",
         "Correct! She drinks milk in the morning.",
         "The story says she drinks milk in the morning."),
        (9, "Who likes bread?",
         [{"id": "a", "text": "Kavindu"}, {"id": "b", "text": "Malmi"}], "b",
         "Correct! Malmi likes rice and bread.",
         "The story says Malmi likes rice and bread."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in read_mcq:
        insert_question(
            read_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    read_fbo = [
        (10, "Kavindu likes ______.",
         [{"id": "a", "text": "rice"}, {"id": "b", "text": "tea"}], "a",
         "Correct! Kavindu likes rice.",
         "Kavindu likes rice — he doesn't like tea."),
        (11, "Malmi doesn't like ______.",
         [{"id": "a", "text": "juice"}, {"id": "b", "text": "milk"}], "a",
         "Correct! Malmi doesn't like juice.",
         "Malmi doesn't like juice — she likes milk."),
        (12, "Kavindu ___ milk.",
         [{"id": "a", "text": "likes"}, {"id": "b", "text": "doesn't like"}], "b",
         "Correct! Kavindu doesn't like milk.",
         "The story says he doesn't like milk."),
        (13, "Malmi ___ tea.",
         [{"id": "a", "text": "likes"}, {"id": "b", "text": "doesn't like"}], "a",
         "Correct! Malmi likes tea.",
         "The story says Malmi likes milk and tea."),
    ]
    for (disp, sentence, options, correct_id, fb_c, fb_i) in read_fbo:
        insert_question(
            read_sec_id, "fill_blank_options", "assessment", disp,
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
        read_sec_id, "fill_blank_typed", "assessment", 14,
        "Who likes juice?",
        {
            "accepted_answers": ["Kavindu", "kavindu"],
            "feedback": {
                "correct": "Correct! Kavindu likes juice and water.",
                "incorrect": "Read again — Kavindu drinks juice every afternoon.",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 15,
        "Who likes milk?",
        {
            "accepted_answers": ["Malmi", "malmi"],
            "feedback": {
                "correct": "Correct! Malmi likes milk and tea.",
                "incorrect": "Read again — Malmi drinks milk in the morning.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # SPEAKING — content only
    # =========================================================================
    insert_content_block(speak_sec_id, "text", 0, {"type": "heading", "text": "Guided Speaking"}, str(uuid7()))
    for (disp, phrase) in [
        (1, "I like pizza."),
        (2, "I don't like milk."),
        (3, "I like rice."),
        (4, "I don't like bread."),
        (5, "I like to drink juice but I don't like milk."),
    ]:
        insert_content_block(speak_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 6, {
        "type": "plain",
        "text": (
            "Mini Speaking Challenge: say 10 sentences about food and drinks "
            "you like and don't like."
        ),
    }, str(uuid7()))

    # =========================================================================
    # WRITING
    # =========================================================================
    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Put the words in the correct order, then fix the broken sentences.",
    }, str(uuid7()))

    builders = [
        (1, "Put the words in order: like / I / rice",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "like"}, {"id": "c3", "text": "rice"}],
         ["c1", "c2", "c3"],
         "Correct! 'I like rice.'", "The correct order is: I like rice."),
        (2, "Put the words in order: milk / don't / I / like",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "don't"}, {"id": "c3", "text": "like"}, {"id": "c4", "text": "milk"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'I don't like milk.'", "The correct order is: I don't like milk."),
        (3, "Put the words in order: likes / He / pizza",
         [{"id": "c1", "text": "He"}, {"id": "c2", "text": "likes"}, {"id": "c3", "text": "pizza"}],
         ["c1", "c2", "c3"],
         "Correct! 'He likes pizza.'", "The correct order is: He likes pizza."),
        (4, "Put the words in order: tea / doesn't / like / She",
         [{"id": "c1", "text": "She"}, {"id": "c2", "text": "doesn't"}, {"id": "c3", "text": "like"}, {"id": "c4", "text": "tea"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'She doesn't like tea.'", "The correct order is: She doesn't like tea."),
    ]
    for (disp, prompt, items, order, fb_c, fb_i) in builders:
        insert_question(
            write_sec_id, "sentence_builder", "assessment", disp,
            prompt,
            {
                "items": items,
                "distractors": [],
                "correct_order": order,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            8, str(uuid7()),
        )

    corrections = [
        (5, "Fix the mistake and type the correct sentence: 'I likes rice.'",
         ["I like rice", "I like rice."],
         "Correct! With 'I' we use 'like'.",
         "With 'I' we use 'like': 'I like rice.'"),
        (6, "Fix the mistake and type the correct sentence: 'He like milk.'",
         ["He likes milk", "He likes milk."],
         "Correct! With 'he' we use 'likes'.",
         "With 'he' we add -s: 'He likes milk.'"),
        (7, "Fix the mistake and type the correct sentence: 'She don't like tea.'",
         ["She doesn't like tea", "She doesn't like tea."],
         "Correct! With 'she' we use 'doesn't'.",
         "With 'she' we use 'doesn't': 'She doesn't like tea.'"),
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

    insert_content_block(write_sec_id, "self_check", 8, {
        "prompt": "Can you write this on your own?",
        "text": (
            "Write 8 sentences about yourself using 'I like' and "
            "'I don't like'.\nWord bank: rice, milk, pizza, juice, tea, bread."
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 9, {
        "type": "summary",
        "items": [
            "Name common food and drinks",
            "Say what you like and don't like",
            "Ask 'Do you like...?' and answer with 'Yes, I do' / 'No, I don't'",
            "Use like and likes correctly",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 6
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
