"""Lesson 9 — Animals, Pets & Abilities (Level 1 batch 2 seed).

Seeds Beginner A Lesson 9 with all 7 sections from the Level 1 lesson 9 PDF:
  Vocabulary  — 13 word cards (Animals / Adjectives) + 2 assessment questions
  Grammar     — can / can't teaching blocks + 8 assessment questions
  Pronunciation — can vs can't + practice + 3 pronunciation questions
  Listening   — At the Zoo dialogue + 14 assessment questions
  Reading     — Bruno the dog story + 8 assessment questions
  Speaking    — guided speaking prompts, content only
  Writing     — 2 option fills + 3 typed corrections + self_check + summary

Text-only scope: picture-tap and audio-select activities are deferred until
assets exist; audio lines are embedded in question prompts (0020 convention).

Sinhala vocabulary translations reconstructed from the PDF (embedded font
mangles extracted Sinhala glyphs) — flag for content-team review.

Revision ID: b5c6d7e8f9a0
Revises:     a4b5c6d7e8f9
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

revision: str = "b5c6d7e8f9a0"
down_revision: Union[str, None] = "a4b5c6d7e8f9"
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
    "Identify vocabulary for common animals and pets",
    "Use adjectives to describe animals' size and appearance",
    "Use can and can't to talk about abilities",
    "Understand spoken descriptions of animals and abilities",
    "Pronounce adjectives and modal verbs clearly",
    "Speak about animals and abilities using simple sentences",
    "Write short sentences describing animals and skills",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    l9_id = ensure_lesson(
        bind, level_id, 9,
        "Animals, Pets & Abilities",
        "Learn animal words and adjectives, and talk about abilities with can and can't.",
        str(uuid7()),
    )
    op.execute(f"UPDATE lesson SET objectives = {_j(OBJECTIVES)} WHERE id = '{l9_id}'")

    vocab_sec_id = ensure_section(bind, l9_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram_sec_id  = ensure_section(bind, l9_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron_sec_id  = ensure_section(bind, l9_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    list_sec_id  = ensure_section(bind, l9_id, "listening",     4, "Listening",     str(uuid7()))
    read_sec_id  = ensure_section(bind, l9_id, "reading",       5, "Reading",       str(uuid7()))
    speak_sec_id = ensure_section(bind, l9_id, "speaking",      6, "Speaking",      str(uuid7()))
    write_sec_id = ensure_section(bind, l9_id, "writing",       7, "Writing",       str(uuid7()))

    # =========================================================================
    # VOCABULARY
    # =========================================================================
    insert_content_block(vocab_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "By the end of this lesson you will be able to: name common "
            "animals and pets, describe them with adjectives, and say what "
            "they can and can't do."
        ),
    }, str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 1, {"type": "heading", "text": "Animals & Pets"}, str(uuid7()))
    animals = [
        (2, "Dog",      "බල්ලා",     "A friendly pet that can run fast.",   "The dog is big and strong."),
        (3, "Cat",      "බළලා",      "A small pet that says meow.",         "The cat is small but fast."),
        (4, "Bird",     "කුරුල්ලා",  "A small animal that can fly.",        "There is a bird in the tree."),
        (5, "Fish",     "මාළුවා",    "An animal that lives in water.",      "The fish can swim very well."),
        (6, "Elephant", "අලියා",     "A very big and strong animal.",       "The elephant is big and heavy."),
        (7, "Monkey",   "වඳුරා",     "A clever animal that climbs trees.",  "The monkey can climb trees."),
    ]
    for (disp, word, si, defn, example) in animals:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_content_block(vocab_sec_id, "text", 8, {"type": "heading", "text": "Adjectives — Size & Appearance"}, str(uuid7()))
    adjectives = [
        (9,  "Big",       "ලොකු",       "Large in size.",             "The elephant is big."),
        (10, "Small",     "පොඩි",       "Little in size.",            "The bird is small."),
        (11, "Fast",      "වේගවත්",     "Moving quickly.",            "A dog can run fast."),
        (12, "Slow",      "මන්දගාමී",   "Not moving quickly.",        "The turtle is slow."),
        (13, "Strong",    "ශක්තිමත්",   "Having a lot of power.",     "The elephant is strong."),
        (14, "Cute",      "ලස්සන",      "Nice and pretty to look at.", "The bird is yellow and cute."),
        (15, "Dangerous", "භයානක",      "Can hurt you.",              "Some animals are dangerous."),
    ]
    for (disp, word, si, defn, example) in adjectives:
        _word_card_si(vocab_sec_id, disp, word, si, defn, example, str(uuid7()), str(uuid7()))

    insert_question(
        vocab_sec_id, "match_pairs", "assessment", 16,
        "Match each animal to what it can do",
        {
            "pairs": [
                {"id": "mp1", "left": "Bird",     "right": "It can fly."},
                {"id": "mp2", "left": "Fish",     "right": "It can swim."},
                {"id": "mp3", "left": "Dog",      "right": "It can run fast."},
                {"id": "mp4", "left": "Monkey",   "right": "It can climb trees."},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well done! You matched every animal to its ability.",
                "incorrect": "Think about what each animal can do best.",
            },
        },
        10, str(uuid7()),
    )
    insert_question(
        vocab_sec_id, "mcq_single", "assessment", 17,
        "Which animal can fly?",
        {
            "options": [
                {"id": "a", "text": "Bird"},
                {"id": "b", "text": "Fish"},
                {"id": "c", "text": "Dog"},
                {"id": "d", "text": "Elephant"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! A bird can fly.",
                "incorrect": "Only the bird can fly — fish swim, dogs run, elephants walk.",
            },
        },
        5, str(uuid7()),
    )

    # =========================================================================
    # GRAMMAR — can / can't
    # =========================================================================
    insert_content_block(gram_sec_id, "text", 0, {
        "type": "plain",
        "text": (
            "Use 'can' to talk about abilities: subject + can + verb. The "
            "negative is 'cannot' or 'can't'. The verb after can never "
            "changes: 'A bird can fly' — not 'can flies' or 'can to fly'."
        ),
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 1, {
        "type": "example_cards",
        "label": "Can",
        "sentences": ["A bird can fly.", "A fish can swim.", "A dog can run fast."],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 2, {
        "type": "example_cards",
        "label": "Can't",
        "sentences": ["An elephant can't fly.", "A cat can't swim well."],
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 3, {
        "type": "qa_pair",
        "question": "Can a bird fly?",
        "answer": "Yes, it can.",
    }, str(uuid7()))
    insert_content_block(gram_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "Can a fish run?",
        "answer": "No, it can't.",
    }, str(uuid7()))

    can_cant = [{"id": "a", "text": "can"}, {"id": "b", "text": "can't"}]
    gram_fbo = [
        (5, "Elephants ______ fly.",          can_cant, "b",
         "Correct! Elephants can't fly.",
         "Elephants are too heavy — they can't fly."),
        (6, "A bird ______ fly very fast.",   can_cant, "a",
         "Correct! A bird can fly very fast.",
         "Birds fly — 'A bird can fly very fast.'"),
        (7, "A fish ______ walk.",            can_cant, "b",
         "Correct! A fish can't walk — it can only swim.",
         "Fish have no legs — 'A fish can't walk.'"),
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
        (8, [{"id": "a", "text": "A bird can fly."}, {"id": "b", "text": "A bird can flies."}], "a",
         "Correct! After 'can' the verb never changes.",
         "After 'can' use the base verb: 'A bird can fly.'"),
        (9, [{"id": "a", "text": "A fish can swim."}, {"id": "b", "text": "A fish can to swim."}], "a",
         "Correct! No 'to' after 'can'.",
         "We never use 'to' after 'can': 'A fish can swim.'"),
        (10, [{"id": "a", "text": "An elephant can't fly."}, {"id": "b", "text": "An elephant can't to fly."}], "a",
         "Correct! No 'to' after 'can't'.",
         "We never use 'to' after 'can't': 'An elephant can't fly.'"),
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
        (11, "Put the words in order: can / fly / bird / A",
         [{"id": "c1", "text": "A"}, {"id": "c2", "text": "bird"}, {"id": "c3", "text": "can"}, {"id": "c4", "text": "fly"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'A bird can fly.'", "The correct order is: A bird can fly."),
        (12, "Put the words in order: walk / can't / fish / A",
         [{"id": "c1", "text": "A"}, {"id": "c2", "text": "fish"}, {"id": "c3", "text": "can't"}, {"id": "c4", "text": "walk"}],
         ["c1", "c2", "c3", "c4"],
         "Correct! 'A fish can't walk.'", "The correct order is: A fish can't walk."),
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
    # PRONUNCIATION — can vs can't
    # =========================================================================
    insert_content_block(pron_sec_id, "text", 0, {"type": "heading", "text": "Can vs Can't"}, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 1, {
        "type": "phrase_card", "text": "can",
        "note": "Weak, soft sound — කෑන්",
    }, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 2, {
        "type": "phrase_card", "text": "can't",
        "note": "Strong ending 't' — කාන්ට්",
    }, str(uuid7()))
    insert_content_block(pron_sec_id, "text", 3, {"type": "heading", "text": "Practice"}, str(uuid7()))
    for (disp, phrase) in [
        (4, "A bird can fly."),
        (5, "A dog can run."),
        (6, "A fish can't walk."),
    ]:
        insert_content_block(pron_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))

    pron_qs = [
        (7, "Say the sentence with a soft 'can'.",             "A bird can fly."),
        (8, "Say the sentence clearly.",                       "A dog can run."),
        (9, "Say the sentence with a strong 't' in \"can't\".", "A fish can't walk."),
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
                    "correct": "Great! Your 'can' and 'can't' were clear.",
                    "incorrect": "Try again — make 'can't' end with a strong 't'.",
                },
            },
            15, str(uuid7()),
        )

    # =========================================================================
    # LISTENING — At the Zoo
    # =========================================================================
    insert_content_block(list_sec_id, "text", 0, {"type": "heading", "text": "Dialogue — At the Zoo"}, str(uuid7()))
    insert_content_block(list_sec_id, "dialogue", 1, {
        "turns": [
            {"speaker": "Boy",  "text": "Look at that elephant! It is very big and strong."},
            {"speaker": "Girl", "text": "Yes! It is very heavy too."},
            {"speaker": "Boy",  "text": "Can it run fast?"},
            {"speaker": "Girl", "text": "Yes, it can run, but it can't run very fast."},
            {"speaker": "Boy",  "text": "Can it fly?"},
            {"speaker": "Girl", "text": "No, it can't fly. Elephants can't fly!"},
            {"speaker": "Boy",  "text": "Look at that bird in the tree."},
            {"speaker": "Girl", "text": "It is small and colorful."},
            {"speaker": "Boy",  "text": "Can it fly?"},
            {"speaker": "Girl", "text": "Yes, it can fly very fast. It can sing too."},
            {"speaker": "Boy",  "text": "Wow! Look at the fish in the water."},
            {"speaker": "Girl", "text": "The fish is small but it can swim very well."},
            {"speaker": "Boy",  "text": "Can a fish walk?"},
            {"speaker": "Girl", "text": "No, it can't walk. It can only swim."},
            {"speaker": "Boy",  "text": "I like animals. They are interesting!"},
            {"speaker": "Girl", "text": "Me too!"},
        ],
    }, str(uuid7()))

    list_fbo = [
        (2, "The elephant ___ fly.", can_cant, "b",
         "Correct! The girl says elephants can't fly.",
         "The girl says 'Elephants can't fly!'"),
        (3, "The bird ___ sing.",    can_cant, "a",
         "Correct! The bird can fly and sing.",
         "The girl says 'It can sing too.'"),
        (4, "The fish ___ swim.",    can_cant, "a",
         "Correct! The fish can swim very well.",
         "The girl says the fish can swim very well."),
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

    list_tf = [
        (5, "The elephant can fly. True or False?",  False,
         "Correct! Elephants can't fly.",
         "The girl says 'Elephants can't fly!'"),
        (6, "The bird is small. True or False?",     True,
         "Correct! The bird is small and colorful.",
         "The girl says the bird is small and colorful."),
        (7, "The fish can walk. True or False?",     False,
         "Correct! The fish can only swim.",
         "The girl says 'It can only swim.'"),
        (8, "The elephant is heavy. True or False?", True,
         "Correct! It is very heavy.",
         "The girl says 'It is very heavy too.'"),
        (9, "The bird can sing. True or False?",     True,
         "Correct! It can fly and sing.",
         "The girl says 'It can sing too.'"),
    ]
    for (disp, prompt, answer, fb_c, fb_i) in list_tf:
        insert_question(
            list_sec_id, "true_false", "assessment", disp,
            prompt,
            {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    who_says = [
        (10, "Who says: 'Can it run fast?'", "a",
         "Correct! The boy asks about the elephant.",
         "The boy asks 'Can it run fast?'"),
        (11, "Who says: 'It can't fly.'",    "b",
         "Correct! The girl answers about the elephant.",
         "The girl says 'No, it can't fly.'"),
        (12, "Who says: 'I like animals.'",  "a",
         "Correct! The boy says he likes animals.",
         "The boy says 'I like animals. They are interesting!'"),
    ]
    for (disp, prompt, correct_id, fb_c, fb_i) in who_says:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {
                "options": [{"id": "a", "text": "Boy"}, {"id": "b", "text": "Girl"}],
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    summary_mcq = [
        (13, "Which animal is strong?",
         [{"id": "a", "text": "Bird"}, {"id": "b", "text": "Elephant"}], "b",
         "Correct! The elephant is big and strong.",
         "The elephant is big and strong."),
        (14, "Which animal can sing?",
         [{"id": "a", "text": "Bird"}, {"id": "b", "text": "Fish"}], "a",
         "Correct! The bird can fly and sing.",
         "The bird can fly and sing."),
        (15, "Which animal can't walk?",
         [{"id": "a", "text": "Fish"}, {"id": "b", "text": "Elephant"}], "a",
         "Correct! The fish can swim but it can't walk.",
         "The fish can swim but it can't walk."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in summary_mcq:
        insert_question(
            list_sec_id, "mcq_single", "assessment", disp,
            prompt,
            {"options": options, "correct_option_id": correct_id,
             "feedback": {"correct": fb_c, "incorrect": fb_i}},
            5, str(uuid7()),
        )

    # =========================================================================
    # READING — Bruno the dog
    # =========================================================================
    insert_content_block(read_sec_id, "text", 0, {
        "type": "plain",
        "text": "Read the story and answer the questions.",
    }, str(uuid7()))
    insert_content_block(read_sec_id, "text", 1, {
        "type": "plain",
        "text": (
            "This is Ravi's pet dog, Bruno. Bruno is big and brown. He is "
            "very strong and friendly. Bruno can run very fast, and he can "
            "jump high. He likes to play in the garden.\n\nRavi also has a "
            "small bird. The bird is yellow and cute. It can fly around the "
            "house, but it can't swim. Bruno cannot fly, but he can swim in "
            "the river near Ravi's house.\n\nThere are many animals in "
            "Ravi's village. There are cows, goats, and chickens. Some "
            "animals are big and strong, and some are small and fast. Ravi "
            "loves animals because they are beautiful and interesting."
        ),
    }, str(uuid7()))

    insert_question(
        read_sec_id, "fill_blank_typed", "assessment", 2,
        "What is the name of Ravi's dog?",
        {
            "accepted_answers": ["Bruno", "bruno"],
            "feedback": {
                "correct": "Correct! The dog's name is Bruno.",
                "incorrect": "Read again — Ravi's pet dog is called Bruno.",
            },
        },
        5, str(uuid7()),
    )
    read_mcq = [
        (3, "What color is Bruno?",
         [{"id": "a", "text": "Brown"}, {"id": "b", "text": "Yellow"}], "a",
         "Correct! Bruno is big and brown.",
         "The story says Bruno is big and brown."),
        (4, "Where can Bruno swim?",
         [{"id": "a", "text": "In the river near Ravi's house"}, {"id": "b", "text": "In the sea"}], "a",
         "Correct! He can swim in the river near Ravi's house.",
         "The story says he can swim in the river near Ravi's house."),
        (5, "Is the bird big or small?",
         [{"id": "a", "text": "Small"}, {"id": "b", "text": "Big"}], "a",
         "Correct! The bird is small, yellow and cute.",
         "The story says Ravi has a small bird."),
        (6, "Why does Ravi love animals?",
         [{"id": "a", "text": "They are beautiful and interesting"}, {"id": "b", "text": "They are big and dangerous"}], "a",
         "Correct! He loves them because they are beautiful and interesting.",
         "The story says he loves animals because they are beautiful and interesting."),
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
        (7, "Bruno can run fast. True or False?",                    True,
         "Correct! Bruno can run very fast and jump high.",
         "The story says Bruno can run very fast."),
        (8, "The bird can swim. True or False?",                     False,
         "Correct! The bird can fly but it can't swim.",
         "The story says the bird can't swim."),
        (9, "There are many animals in Ravi's village. True or False?", True,
         "Correct! There are cows, goats, and chickens.",
         "The story says there are many animals in the village."),
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
        (1, "The dog is big and strong."),
        (2, "The bird can fly."),
        (3, "The fish can't walk."),
    ]:
        insert_content_block(speak_sec_id, "text", disp, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 4, {
        "type": "qa_pair",
        "question": "Can a monkey climb trees?",
        "answer": "Yes, it can.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 5, {
        "type": "qa_pair",
        "question": "Can a dog sing?",
        "answer": "No, it can't.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 6, {
        "type": "qa_pair",
        "question": "Can an elephant jump high?",
        "answer": "No, it can't.",
    }, str(uuid7()))
    insert_content_block(speak_sec_id, "text", 7, {
        "type": "plain",
        "text": (
            "Personal Speaking: talk for 40 seconds about your favorite "
            "animal. Include two adjectives, two abilities and one \"can't\" "
            "sentence."
        ),
    }, str(uuid7()))

    # =========================================================================
    # WRITING
    # =========================================================================
    insert_content_block(write_sec_id, "text", 0, {
        "type": "plain",
        "text": "Choose the correct word, then fix the broken sentences.",
    }, str(uuid7()))

    write_fbo = [
        (1, "The monkey can ______ trees.",
         [{"id": "a", "text": "climb"}, {"id": "b", "text": "fly"}], "a",
         "Correct! Monkeys climb trees.",
         "Monkeys climb trees — they can't fly."),
        (2, "It can't ______ like a bird.",
         [{"id": "a", "text": "fly"}, {"id": "b", "text": "run"}], "a",
         "Correct! Only birds fly.",
         "Birds fly — other animals can't fly like a bird."),
    ]
    for (disp, sentence, options, correct_id, fb_c, fb_i) in write_fbo:
        insert_question(
            write_sec_id, "fill_blank_options", "assessment", disp,
            sentence,
            {
                "sentence_with_blank": sentence,
                "options": options,
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    corrections = [
        (3, "Fix the mistake and type the correct sentence: 'A bird can flies.'",
         ["A bird can fly", "A bird can fly."],
         "Correct! After 'can' the verb never changes.",
         "After 'can' use the base verb: 'A bird can fly.'"),
        (4, "Fix the mistake and type the correct sentence: 'A fish can to swim.'",
         ["A fish can swim", "A fish can swim."],
         "Correct! No 'to' after 'can'.",
         "We never use 'to' after 'can': 'A fish can swim.'"),
        (5, "Fix the mistake and type the correct sentence: 'The monkey can climbs trees.'",
         ["The monkey can climb trees", "The monkey can climb trees."],
         "Correct! After 'can' use the base verb.",
         "After 'can' use the base verb: 'The monkey can climb trees.'"),
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

    insert_content_block(write_sec_id, "self_check", 6, {
        "prompt": "Can you write this on your own?",
        "text": (
            "Write 5–7 sentences about an animal.\nInclude 2 adjectives, 2 "
            "abilities, 1 negative sentence and 1 'There is / There are' "
            "sentence.\n\nExample: The elephant is big but the monkey is "
            "small. The elephant can run but it can't climb trees."
        ),
    }, str(uuid7()))

    insert_content_block(write_sec_id, "text", 7, {
        "type": "summary",
        "items": [
            "Name common animals and pets",
            "Describe animals with adjectives like big, small and strong",
            "Say what animals can and can't do",
            "Ask 'Can it...?' and answer 'Yes, it can' / 'No, it can't'",
        ],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 9
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
