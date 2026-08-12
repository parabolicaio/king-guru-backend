"""Lesson 8 — Health, Body & Feelings (Level 1 batch 2 seed).

Seeds Beginner A Lesson 8 with all 7 sections from the Level 1 lesson 8 PDF:
  Vocabulary  — 23 word cards (Body Parts / Health Problems / Feelings) + 2 questions
  Grammar     — I have a... / I feel... teaching blocks + 16 assessment questions
  Pronunciation — focus words + rhythm sentences + 3 pronunciation questions
  Listening   — At the Clinic dialogue + 14 assessment questions
  Reading     — Kavishka sick-day story + 10 assessment questions
  Speaking    — guided speaking prompts, content only
  Writing     — 3 typed fills + 3 typed corrections + self_check + summary

Text-only scope: picture-tap and audio-select activities are deferred until
assets exist; audio lines are embedded in question prompts (0020 convention).

Sinhala vocabulary translations reconstructed from the PDF (embedded font
mangles extracted Sinhala glyphs) — flag for content-team review.

Revision ID: a4b5c6d7e8f9
Revises:     f3a4b5c6d7e8
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

revision: str = "a4b5c6d7e8f9"
down_revision: Union[str, None] = "f3a4b5c6d7e8"
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
    "Identify vocabulary for body parts and common health problems",
    "Use the structure 'I have a...' to talk about health and feelings",
    "Understand short spoken health-related conversations",
    "Pronounce body and health vocabulary clearly",
    "Speak about how you feel using simple sentences",
    "Write short sentences describing health problems or feelings",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    l8_id = ensure_lesson(
        bind, level_id, 8,
        "Health, Body & Feelings",
        "Learn body and health words and say how you feel with 'I have a...' and 'I feel...'.",
        str(uuid7()),
    )
    op.execute(f"UPDATE lesson SET objectives = {_j(OBJECTIVES)} WHERE id = '{l8_id}'")

    vocab_sec_id = ensure_section(bind, l8_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id  = ensure_section(bind, l8_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id  = ensure_section(bind, l8_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id  = ensure_section(bind, l8_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id  = ensure_section(bind, l8_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id = ensure_section(bind, l8_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id = ensure_section(bind, l8_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY
    # =========================================================================
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: name body parts, "
            "talk about common health problems with 'I have a...', and say "
            "how you feel with 'I feel...'."
        ),
    }, str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Body Parts"}, str(uuid7()))
    body_parts = [
        (2,  "Head",    "හිස",    "The top part of your body.",        "My head hurts."),
        (3,  "Eye",     "ඇස",     "You see with it.",                  "I have sore eyes."),
        (4,  "Ear",     "කණ",     "You hear with it.",                 "My ear hurts."),
        (5,  "Nose",    "නාසය",   "You smell with it.",                "My nose is blocked."),
        (6,  "Mouth",   "කට",     "You eat and speak with it.",        "Open your mouth."),
        (7,  "Arm",     "බාහුව",  "Between your shoulder and hand.",   "My arm is strong."),
        (8,  "Hand",    "අත",     "You hold things with it.",          "Wash your hands."),
        (9,  "Leg",     "කකුල",   "You walk with it.",                 "I have sore legs."),
        (10, "Foot",    "පාදය",   "The end of your leg.",              "My foot hurts."),
        (11, "Stomach", "බඩ",     "Where your food goes.",             "I have a stomach ache."),
        (12, "Tooth",   "දත",     "You bite with it.",                 "I brush my teeth every day."),
    ]
    for (disp, word, si, defn, example) in body_parts:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 13, {"type": "heading", "text": "Health Problems"}, str(uuid7()))
    health = [
        (14, "Sore throat",  "උගුරේ වේදනාව",   "Pain in your throat.",          "I have a sore throat."),
        (15, "Headache",     "හිසරදය",         "Pain in your head.",            "I have a headache."),
        (16, "Stomach ache", "බඩේ කැක්කුම",    "Pain in your stomach.",         "He has a stomach ache."),
        (17, "Cold",         "හෙම්බිරිස්සාව",  "A common illness with a blocked nose.", "I have a cold."),
        (18, "Fever",        "උණ",             "When your body is too hot.",    "She has a fever."),
    ]
    for (disp, word, si, defn, example) in health:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 19, {"type": "heading", "text": "Feelings"}, str(uuid7()))
    feelings = [
        (20, "Happy",  "සතුටුයි",   "Feeling good and smiling.",       "I feel happy today."),
        (21, "Sad",    "දුකයි",     "Feeling unhappy.",                "She feels sad."),
        (22, "Tired",  "මහන්සියි",  "Needing rest or sleep.",          "I feel very tired."),
        (23, "Sick",   "අසනීපයි",   "Not feeling well.",               "He feels sick."),
        (24, "Hungry", "බඩගිනියි",  "Wanting to eat.",                 "I am not very hungry."),
        (25, "Weak",   "දුර්වලයි",  "Having little strength.",         "I feel tired and weak."),
        (26, "Better", "හොඳ වෙලා",  "Feeling well again.",             "I feel better now."),
    ]
    for (disp, word, si, defn, example) in feelings:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 27,
        "Match each word to its group",
        {
            "pairs": [
                {"id": "mp1", "left": "Headache", "right": "Health problem"},
                {"id": "mp2", "left": "Fever",    "right": "Health problem"},
                {"id": "mp3", "left": "Happy",    "right": "Feeling"},
                {"id": "mp4", "left": "Tired",    "right": "Feeling"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! Health problems and feelings sorted correctly.",
                "incorrect": "Headache and fever are health problems; happy and tired are feelings.",
            },
        },
        10, str(uuid7()),
    )
    insert_question(
        vocab_sec_id, "mcq_single", "assessment", 28,
        "Which word is a body part?",
        {
            "options": [
                {"id": "a", "text": "Leg"},
                {"id": "b", "text": "Fever"},
                {"id": "c", "text": "Tired"},
                {"id": "d", "text": "Happy"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! A leg is a body part.",
                "incorrect": "Fever is a health problem and tired/happy are feelings — leg is a body part.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR — I have a... / I feel...
    # =========================================================================
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "Use 'I have a...' for health problems and 'I feel...' for "
            "feelings. With he and she, use 'has' and 'feels'."
        ),
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "I have a...",
        "sentences": [
            "I have a headache.",
            "I have a cold.",
            "I have a fever.",
            "I have a stomach ache.",
        ],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "I feel...",
        "sentences": ["I feel tired.", "I feel sick.", "I feel better now."],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "What's wrong?",
        "answer": "I have a headache.",
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "How do you feel?",
        "answer": "I feel tired.",
    }, str(uuid7()))

    have_has = [{"id": "a", "text": "have"}, {"id": "b", "text": "has"}]
    gram_fbo = [
        (5, "I ___ a headache.",    have_has, "a",
         "Correct! With 'I' we use 'have'.",
         "With 'I' we use 'have'."),
        (6, "She ___ a fever.",     have_has, "b",
         "Correct! With 'she' we use 'has'.",
         "With 'she' we use 'has'."),
        (7, "He ___ a cold.",       have_has, "b",
         "Correct! With 'he' we use 'has'.",
         "With 'he' we use 'has'."),
        (8, "They ___ sore eyes.",  have_has, "a",
         "Correct! With 'they' we use 'have'.",
         "With 'they' we use 'have'."),
        (9, "___ she have a fever?",
         [{"id": "a", "text": "Do"}, {"id": "b", "text": "Does"}], "b",
         "Correct! With 'she' we ask with 'Does'.",
         "With 'she' we ask 'Does she have...?'"),
        (10, "___ you have a headache?",
         [{"id": "a", "text": "Do"}, {"id": "b", "text": "Does"}], "a",
         "Correct! With 'you' we ask with 'Do'.",
         "With 'you' we ask 'Do you have...?'"),
        (11, "He ___ have a fever.",
         [{"id": "a", "text": "doesn't"}, {"id": "b", "text": "don't"}], "a",
         "Correct! With 'he' we use 'doesn't'.",
         "With 'he' the negative is 'doesn't have'."),
        (12, "I ___ have a headache.",
         [{"id": "a", "text": "don't"}, {"id": "b", "text": "doesn't"}], "a",
         "Correct! With 'I' we use 'don't'.",
         "With 'I' the negative is 'don't have'."),
        (13, "There ___ medicine on the table.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'There is medicine on the table.'",
         "'Medicine' is uncountable — 'There is medicine.'"),
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

    gram_mcq = [
        (14, [{"id": "a", "text": "I have a headache."}, {"id": "b", "text": "I feel a headache."}], "a",
         "Correct! Health problems use 'I have a...'.",
         "A headache is a health problem — 'I have a headache.'"),
        (15, [{"id": "a", "text": "I feel tired."}, {"id": "b", "text": "I have tired."}], "a",
         "Correct! Feelings use 'I feel...'.",
         "Tired is a feeling — 'I feel tired.'"),
        (16, [{"id": "a", "text": "She has a cold."}, {"id": "b", "text": "She have a cold."}], "a",
         "Correct! With 'she' we use 'has'.",
         "With 'she' we use 'has': 'She has a cold.'"),
        (17, [{"id": "a", "text": "I feel happy."}, {"id": "b", "text": "I feel happily."}], "a",
         "Correct! After 'feel' we use an adjective: happy.",
         "After 'feel' we use an adjective — 'I feel happy.'"),
    ]
    for (disp, options, correct_id, fb_c, fb_i) in gram_mcq:
        insert_question(
            gram_sec_id, "mcq_single", "assessment", disp,
            "Choose the correct sentence.",
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    builders = [
        (18, "Put the words in order: have / I / a / fever",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "have"}, {"id": "c3", "text": "a"}, {"id": "c4", "text": "fever"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'I have a fever.'", "The correct order is: I have a fever."),
        (19, "Put the words in order: tired / I / feel",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "feel"}, {"id": "c3", "text": "tired"}],
         ["c1", "c2", "c3"],
         "Correct! 'I feel tired.'", "The correct order is: I feel tired."),
        (20, "Put the words in order: has / She / a / cold",
         [{"id": "c1", "text": "She"}, {"id": "c2", "text": "has"}, {"id": "c3", "text": "a"}, {"id": "c4", "text": "cold"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'She has a cold.'", "The correct order is: She has a cold."),
    ]
    for (disp, prompt, items, order, fb_c, fb_i) in builders:
        insert_question(
            gram_sec_id, "sentence_builder", "assessment", disp,
            prompt,
            {
                "items": items,
                "distractors": [],
                "correct_order": order,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            8, str(uuid7()),
        )

    # =========================================================================
    # PRONUNCIATION
    # =========================================================================
    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Focus Words"}, str(uuid7()))
    focus = [
        (1, "Headache",     "හෙඩ්ඒක් — head + ache"),
        (2, "Stomach ache", "ස්ටමක් ඒක්"),
        (3, "Fever",        "ෆීවර්"),
        (4, "Tired",        "ටයර්ඩ්"),
    ]
    for (disp, word, note) in focus:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": word, "note": note}, str(uuid7()))

    insert_content_block(pron_sec_id, "text", 5, {"type": "heading", "text": "Sentence Rhythm"}, str(uuid7()))
    for (disp, phrase, note) in [
        (6, "I have a HEADache.",  "Stress HEAD"),
        (7, "I feel SICK today.",  "Stress SICK"),
        (8, "She has a FEver.",    "Stress FE"),
    ]:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": note}, str(uuid7()))

    pron_qs = [
        (9,  "Say the sentence. Stress the strong word: HEADache.", "I have a headache."),
        (10, "Say the sentence clearly.",                           "I feel tired."),
        (11, "Say the sentence. Stress the strong word: FEver.",    "She has a fever."),
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
                    "incorrect": "Try again — say the strong word clearly.",
                },
            },
            15, str(uuid7()),
        )

    # =========================================================================
    # LISTENING — At the Clinic
    # =========================================================================
    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Dialogue — At the Clinic"}, str(uuid7()))
    insert_content_block(list_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "Doctor", "text": "Hello. Please come in. What's wrong?"},
            {"speaker": "Girl",   "text": "Hello, doctor. I don't feel well. I have a headache and a sore throat."},
            {"speaker": "Doctor", "text": "I see. Since when do you feel sick?"},
            {"speaker": "Girl",   "text": "Since yesterday evening."},
            {"speaker": "Doctor", "text": "Do you have a fever?"},
            {"speaker": "Girl",   "text": "Yes, I do. I also feel very tired and weak."},
            {"speaker": "Doctor", "text": "Do you have a cold?"},
            {"speaker": "Girl",   "text": "Yes, I have a cold. My nose is blocked."},
            {"speaker": "Doctor", "text": "Are you eating well?"},
            {"speaker": "Girl",   "text": "No, I am not very hungry."},
            {"speaker": "Doctor", "text": "Let me check your temperature. Yes, you have a small fever. You need to rest at home."},
            {"speaker": "Girl",   "text": "Do I need medicine?"},
            {"speaker": "Doctor", "text": "Yes, you need this medicine. There is some medicine in this box. Take it two times a day."},
            {"speaker": "Girl",   "text": "Okay, doctor."},
            {"speaker": "Doctor", "text": "Also drink warm water. Stay in bed and don't go to school tomorrow."},
            {"speaker": "Girl",   "text": "Thank you, doctor."},
            {"speaker": "Doctor", "text": "You're welcome. Get well soon."},
        ],
    }, str(uuid7()))

    list_tf = [
        (2, "The girl has a stomach ache. True or False?",              False,
         "Correct! She has a headache and a sore throat, not a stomach ache.",
         "She says she has a headache and a sore throat."),
        (3, "She has a fever. True or False?",                          True,
         "Correct! The doctor finds a small fever.",
         "She says 'Yes, I do' and the doctor finds a small fever."),
        (4, "She feels tired and weak. True or False?",                 True,
         "Correct! She says she feels very tired and weak.",
         "She says 'I also feel very tired and weak.'"),
        (5, "She is very hungry. True or False?",                       False,
         "Correct! She says she is not very hungry.",
         "She says 'No, I am not very hungry.'"),
        (6, "The doctor says she can go to school tomorrow. True or False?", False,
         "Correct! The doctor says 'don't go to school tomorrow.'",
         "The doctor says 'Stay in bed and don't go to school tomorrow.'"),
    ]
    for (disp, prompt, answer, fb_c, fb_i) in list_tf:
        insert_question(
            list_sec_id, "true_false", "assessment", disp,
            prompt,
            {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    list_fbo = [
        (7, "She ______ a headache.",
         [{"id": "a", "text": "has"}, {"id": "b", "text": "have"}], "a",
         "Correct! With 'she' we use 'has'.",
         "With 'she' we use 'has'."),
        (8, "She ______ very tired.",
         [{"id": "a", "text": "feel"}, {"id": "b", "text": "feels"}], "b",
         "Correct! With 'she' we use 'feels'.",
         "With 'she' we use 'feels'."),
        (9, "There ______ medicine in the box.",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! 'There is medicine in the box.'",
         "'Medicine' is uncountable — 'There is medicine.'"),
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
        (10, "Who says: 'What's wrong?'",       "a",
         "Correct! The doctor asks what's wrong.",
         "The doctor asks 'What's wrong?'"),
        (11, "Who says: 'I have a headache.'",  "b",
         "Correct! The girl describes her problem.",
         "The girl says 'I have a headache and a sore throat.'"),
        (12, "Who says: 'You need to rest.'",   "a",
         "Correct! The doctor tells her to rest.",
         "The doctor says she needs to rest at home."),
    ]
    for (disp, prompt, correct_id, fb_c, fb_i) in who_says:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {
                "options": [{"id": "a", "text": "Doctor"}, {"id": "b", "text": "Girl"}],
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    insert_question(
        list_sec_id, "mcq_single", "assessment", 13,
        "'Do you have a fever?' — choose the correct answer.",
        {
            "options": [
                {"id": "a", "text": "Yes, I do."},
                {"id": "b", "text": "Yes, I am."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Do you have...?' is answered with 'Yes, I do.'",
                "incorrect": "'Do you have...?' is answered with 'Yes, I do.'",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "mcq_single", "assessment", 14,
        "'How do you feel?' — choose the correct answer.",
        {
            "options": [
                {"id": "a", "text": "I have a fever."},
                {"id": "b", "text": "I feel tired."},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! 'How do you feel?' is answered with 'I feel...'.",
                "incorrect": "'How do you feel?' asks about feelings — 'I feel tired.'",
            },
        },
        5, str(uuid7()),
    )
    insert_question(
        list_sec_id, "mcq_single", "assessment", 15,
        "'There is medicine in the box.' Where is the medicine?",
        {
            "options": [
                {"id": "a", "text": "In the box"},
                {"id": "b", "text": "On the table"},
                {"id": "c", "text": "Under the bed"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! The medicine is in the box.",
                "incorrect": "The doctor says 'There is some medicine in this box.'",
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
            "This is Kavishka. Yesterday he did not go to school because he "
            "was sick. In the morning, he had a fever and a headache. His "
            "body felt weak, and he was very tired. He also had a sore "
            "throat, so he could not speak loudly.\n\nHis mother gave him "
            "medicine and warm soup. There was a glass of water on the table "
            "near his bed. The medicine was in the cupboard in his bedroom. "
            "Kavishka stayed in bed all day. He watched television and "
            "rested.\n\nIn the evening, he felt a little better, but he was "
            "still tired. Today he feels much better, and he hopes to go to "
            "school tomorrow."
        ),
    }, str(uuid7()))

    read_mcq = [
        (2, "Why did Kavishka stay at home?",
         [{"id": "a", "text": "He was sick"}, {"id": "b", "text": "He was on holiday"}], "a",
         "Correct! He did not go to school because he was sick.",
         "The story says he did not go to school because he was sick."),
        (3, "What did he have in the morning?",
         [{"id": "a", "text": "A fever and a headache"}, {"id": "b", "text": "A stomach ache"}], "a",
         "Correct! He had a fever and a headache.",
         "The story says he had a fever and a headache."),
        (4, "How did he feel?",
         [{"id": "a", "text": "Weak and tired"}, {"id": "b", "text": "Happy and strong"}], "a",
         "Correct! His body felt weak and he was very tired.",
         "The story says his body felt weak and he was very tired."),
        (5, "Where was the water?",
         [{"id": "a", "text": "On the table near his bed"}, {"id": "b", "text": "In the kitchen"}], "a",
         "Correct! The glass of water was on the table near his bed.",
         "The story says there was a glass of water on the table near his bed."),
        (6, "Where was the medicine?",
         [{"id": "a", "text": "In the cupboard"}, {"id": "b", "text": "On the table"}], "a",
         "Correct! The medicine was in the cupboard in his bedroom.",
         "The story says the medicine was in the cupboard."),
        (7, "What did his mother give him?",
         [{"id": "a", "text": "Medicine and warm soup"}, {"id": "b", "text": "Tea and bread"}], "a",
         "Correct! His mother gave him medicine and warm soup.",
         "The story says his mother gave him medicine and warm soup."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in read_mcq:
        insert_question(
            read_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    read_tf = [
        (8,  "Kavishka went to school yesterday. True or False?", False,
         "Correct! He stayed at home because he was sick.",
         "The story says he did not go to school yesterday."),
        (9,  "He feels much better today. True or False?",        True,
         "Correct! Today he feels much better.",
         "The story ends: today he feels much better."),
        (10, "The medicine was on the table. True or False?",     False,
         "Correct! The medicine was in the cupboard.",
         "The medicine was in the cupboard — the water was on the table."),
        (11, "The water was under the bed. True or False?",       False,
         "Correct! The water was on the table near his bed.",
         "The water was on the table near his bed."),
    ]
    for (disp, prompt, answer, fb_c, fb_i) in read_tf:
        insert_question(
            read_sec_id, "true_false", "assessment", disp,
            prompt,
            {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # =========================================================================
    # SPEAKING — content only
    # =========================================================================
    insert_content_block(speak_sec_id, "text", 0, {"type": "heading", "text": "Guided Speaking"}, str(uuid7()))
    for (disp, phrase) in [
        (1, "I have a headache."),
        (2, "I have a fever."),
        (3, "I feel tired."),
        (4, "There is medicine on the table."),
    ]:
        insert_content_block(speak_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 5, {
        "type": "qa_pair",
        "question": "What's wrong?",
        "answer": "I have a cold.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 6, {
        "type": "qa_pair",
        "question": "How do you feel?",
        "answer": "I feel weak.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 7, {
        "type": "plain",
        "text": (
            "Personal Speaking: talk for 40 seconds about a time when you "
            "were sick. Include two health problems, one feeling and one "
            "sentence with 'There is'."
        ),
    }, str(uuid7()))

    # =========================================================================
    # WRITING
    # =========================================================================
    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Type the missing word, then fix the broken sentences.",
    }, str(uuid7()))

    fills = [
        (1, "I ______ a headache.",              ["have"],
         "Correct! 'I have a headache.'",
         "With 'I' we use 'have'."),
        (2, "She ______ a fever.",               ["has"],
         "Correct! 'She has a fever.'",
         "With 'she' we use 'has'."),
        (3, "There ______ medicine on the table.", ["is"],
         "Correct! 'There is medicine on the table.'",
         "'Medicine' is uncountable — 'There is medicine.'"),
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
        (4, "Fix the mistake and type the correct sentence: 'I has a cold.'",
         ["I have a cold", "I have a cold."],
         "Correct! With 'I' we use 'have'.",
         "With 'I' we use 'have': 'I have a cold.'"),
        (5, "Fix the mistake and type the correct sentence: 'She have a fever.'",
         ["She has a fever", "She has a fever."],
         "Correct! With 'she' we use 'has'.",
         "With 'she' we use 'has': 'She has a fever.'"),
        (6, "Fix the mistake and type the correct sentence: 'There are a glass on the table.'",
         ["There is a glass on the table", "There is a glass on the table."],
         "Correct! One glass takes 'There is'.",
         "One glass: 'There is a glass on the table.'"),
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
            "Write 6–8 sentences about a sick day.\nInclude 2 health "
            "problems, 2 feelings, one 'There is' sentence and one location "
            "sentence with in / on / under.\n\nExample: Yesterday I had a "
            "fever. I had a headache. I felt tired and weak. There was "
            "medicine on the table. Now I feel better."
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 8, {
        "type": "summary",
        "items": [
            "Name body parts, health problems and feelings",
            "Say 'I have a headache' and 'She has a cold'",
            "Say how you feel with 'I feel...'",
            "Ask 'What's wrong?' and 'How do you feel?'",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 8
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
