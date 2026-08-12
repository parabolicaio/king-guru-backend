"""Seed data — levels, XP rules, placement config, Beginner A Lessons 1–2, feature flags.

Revision ID: f2b3c4d5e6a7
Revises:     e1a2b3c4d5f6
Create Date: 2026-05-29

Lesson content derived from docs/lesson-samples/lesson 1.pdf and lesson 2.pdf:
  - Lesson 1: Greetings & Personal Introductions
  - Lesson 2: Family & Describing People

Phase 1 seeds Vocabulary and Grammar sections only. Pronunciation, Listening,
Reading, Speaking, and Writing sections from the PDFs are Phase 2+ and will be
seeded in later migrations when those engines ship.

PLACEMENT QUESTIONS: all 15 rows are content stubs (payload contains
"_placeholder": true). A pedagogy review is required before these are shown to
users. See specs/02-decisions-log.md OQ-4.1.
"""
import json
from typing import Sequence, Union

from alembic import op

revision: str = "f2b3c4d5e6a7"
down_revision: Union[str, None] = "e1a2b3c4d5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    """Return a single-quoted PostgreSQL JSONB literal from a Python object."""
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(value: str) -> str:
    """Return a single-quoted PostgreSQL TEXT literal with internal quotes escaped."""
    return "'" + value.replace("'", "''") + "'"


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    # -------------------------------------------------------------------------
    # Level IDs — declared up front; referenced by placement_scoring_rule and
    # lesson FK columns later in this same migration.
    # -------------------------------------------------------------------------
    lvl_beg_a_id       = str(uuid7())
    lvl_beg_b_id       = str(uuid7())
    lvl_elem_id        = str(uuid7())
    lvl_inter_id       = str(uuid7())
    lvl_upper_inter_id = str(uuid7())
    lvl_adv_id         = str(uuid7())

    # =========================================================================
    # streak_milestone — per OQ-1.1; formula: bonus_xp = days + ceil(days×0.10)
    # =========================================================================
    op.execute("""
        INSERT INTO streak_milestone (days, bonus_xp) VALUES
            (7,   8),
            (14,  16),
            (30,  33),
            (60,  66),
            (90,  99),
            (180, 198),
            (365, 402)
    """)

    # =========================================================================
    # xp_rule — per OQ-1.1
    # streak_milestone and achievement_unlocked XP come from their own tables,
    # not from here.
    # =========================================================================
    xp_rows = [
        # (action_type,           context_key,  xp_value)
        ("lesson_complete",       None,          50),
        ("daily_goal_complete",   None,          30),
        ("streak_day",            None,           1),
        ("word_learned",          "easy",         1),
        ("word_learned",          "medium",       2),
        ("word_learned",          "hard",         3),
        ("essay_submitted",       "A+",          60),
        ("essay_submitted",       "A",           50),
        ("essay_submitted",       "B+",          40),
        ("essay_submitted",       "B",           30),
        ("essay_submitted",       "C+",          20),
        ("essay_submitted",       "C",           15),
        ("essay_submitted",       "D",            5),
        ("essay_submitted",       "F",            0),
    ]
    for action_type, context_key, xp_value in xp_rows:
        xp_id = str(uuid7())
        ctx_sql = _s(context_key) if context_key is not None else "NULL"
        op.execute(f"""
            INSERT INTO xp_rule
                (id, action_type, context_key, xp_value, created_at, updated_at)
            VALUES ('{xp_id}', '{action_type}', {ctx_sql}, {xp_value}, now(), now())
        """)

    # =========================================================================
    # level — per OQ-3.7 daily_essay_enabled defaults
    # =========================================================================
    op.execute(f"""
        INSERT INTO level
            (id, name, code, display_order, description, daily_essay_enabled,
             created_at, updated_at)
        VALUES
            ('{lvl_beg_a_id}', 'Beginner A', 'beginner_a', 1,
             'The starting point for complete English beginners.',
             FALSE, now(), now()),
            ('{lvl_beg_b_id}', 'Beginner B', 'beginner_b', 2,
             'Building on Beginner A with more vocabulary and grammar.',
             FALSE, now(), now()),
            ('{lvl_elem_id}', 'Elementary', 'elementary', 3,
             'Forming simple sentences and everyday conversations.',
             TRUE, now(), now()),
            ('{lvl_inter_id}', 'Intermediate', 'intermediate', 4,
             'Expressing ideas with growing fluency and accuracy.',
             TRUE, now(), now()),
            ('{lvl_upper_inter_id}', 'Upper Intermediate', 'upper_intermediate', 5,
             'Handling complex topics with confidence.',
             TRUE, now(), now()),
            ('{lvl_adv_id}', 'Advanced', 'advanced', 6,
             'Near-native proficiency and nuanced expression.',
             TRUE, now(), now())
    """)

    # =========================================================================
    # placement_scoring_rule — per OQ-4.1 buckets
    # =========================================================================
    psr_rows = [
        (0.00,   30.00, lvl_beg_a_id),
        (31.00,  50.00, lvl_beg_b_id),
        (51.00,  65.00, lvl_elem_id),
        (66.00,  80.00, lvl_inter_id),
        (81.00,  92.00, lvl_upper_inter_id),
        (93.00, 100.00, lvl_adv_id),
    ]
    for min_pct, max_pct, level_id in psr_rows:
        psr_id = str(uuid7())
        op.execute(f"""
            INSERT INTO placement_scoring_rule
                (id, min_percent, max_percent, recommended_level_id, created_at, updated_at)
            VALUES ('{psr_id}', {min_pct}, {max_pct}, '{level_id}', now(), now())
        """)

    # =========================================================================
    # placement_question — 15 placeholder rows; _placeholder:true marks stubs.
    # Distribution: 3 beginner_a, 3 beginner_b, 3 elementary,
    #               3 intermediate, 2 upper_intermediate, 1 advanced.
    # =========================================================================
    pq_rows = [
        ("mcq_single", "beginner_a", 1, {
            "prompt": "What do you say when you meet someone?",
            "options": [{"id":"a","text":"Hello"},{"id":"b","text":"Goodbye"},
                        {"id":"c","text":"Thank you"},{"id":"d","text":"Sorry"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct!", "incorrect": "'Hello' is a greeting."},
            "_placeholder": True,
        }),
        ("true_false", "beginner_a", 2, {
            "prompt": "Is 'cat' the name of an animal?",
            "correct_answer": True,
            "feedback": {"correct": "Yes, a cat is an animal.",
                         "incorrect": "A cat is indeed an animal."},
            "_placeholder": True,
        }),
        ("mcq_single", "beginner_a", 3, {
            "prompt": "Choose the correct word: I ___ a student.",
            "options": [{"id":"a","text":"am"},{"id":"b","text":"is"},
                        {"id":"c","text":"are"},{"id":"d","text":"be"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! With 'I' we use 'am'.",
                         "incorrect": "With 'I', we use 'am'."},
            "_placeholder": True,
        }),
        ("mcq_single", "beginner_b", 4, {
            "prompt": "What is the plural of 'book'?",
            "options": [{"id":"a","text":"books"},{"id":"b","text":"bookes"},
                        {"id":"c","text":"book"},{"id":"d","text":"bookses"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct!",
                         "incorrect": "Add -s to form the plural: books."},
            "_placeholder": True,
        }),
        ("mcq_single", "beginner_b", 5, {
            "prompt": "Which sentence is correct?",
            "options": [{"id":"a","text":"She has two cats."},
                        {"id":"b","text":"She have two cats."},
                        {"id":"c","text":"She are two cats."},
                        {"id":"d","text":"She am two cats."}],
            "correct_option_id": "a",
            "feedback": {"correct": "Well done!", "incorrect": "With 'she', use 'has'."},
            "_placeholder": True,
        }),
        ("true_false", "beginner_b", 6, {
            "prompt": "The past tense of 'go' is 'goed'.",
            "correct_answer": False,
            "feedback": {"correct": "Correct — the past tense is 'went'.",
                         "incorrect": "The past tense of 'go' is 'went', not 'goed'."},
            "_placeholder": True,
        }),
        ("mcq_single", "elementary", 7, {
            "prompt": "She ___ to school every day.",
            "options": [{"id":"a","text":"goes"},{"id":"b","text":"go"},
                        {"id":"c","text":"going"},{"id":"d","text":"gone"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! Third-person singular: she goes.",
                         "incorrect": "Third-person singular requires 'goes'."},
            "_placeholder": True,
        }),
        ("fill_blank_typed", "elementary", 8, {
            "prompt": "If it rains, I _____ an umbrella.",
            "accepted_answers": ["use", "will use", "take", "will take",
                                 "carry", "will carry"],
            "feedback": {"correct": "Good job!",
                         "incorrect": "We need an umbrella when it rains."},
            "_placeholder": True,
        }),
        ("mcq_single", "elementary", 9, {
            "prompt": "The book is ___ the table.",
            "options": [{"id":"a","text":"on"},{"id":"b","text":"in"},
                        {"id":"c","text":"at"},{"id":"d","text":"by"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! 'On' means on top of a surface.",
                         "incorrect": "Use 'on' for position on a surface."},
            "_placeholder": True,
        }),
        ("mcq_single", "intermediate", 10, {
            "prompt": "By the time she arrived, the meeting ___ already started.",
            "options": [{"id":"a","text":"had"},{"id":"b","text":"has"},
                        {"id":"c","text":"have"},{"id":"d","text":"was"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! Past perfect: had started.",
                         "incorrect": "Use past perfect (had + past participle)."},
            "_placeholder": True,
        }),
        ("fill_blank_typed", "intermediate", 11, {
            "prompt": "Despite the rain, they _____ to complete the project.",
            "accepted_answers": ["managed", "were able to manage"],
            "feedback": {"correct": "Excellent!", "incorrect": "'Managed' fits here."},
            "_placeholder": True,
        }),
        ("mcq_single", "intermediate", 12, {
            "prompt": "Which sentence uses the passive voice correctly?",
            "options": [{"id":"a","text":"The letter was written by her."},
                        {"id":"b","text":"She written the letter."},
                        {"id":"c","text":"Her wrote the letter."},
                        {"id":"d","text":"The letter wrote by her."}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct passive voice!",
                         "incorrect": "Passive: subject + was/were + past participle."},
            "_placeholder": True,
        }),
        ("mcq_single", "upper_intermediate", 13, {
            "prompt": "I wish I ___ more time to study when I was young.",
            "options": [{"id":"a","text":"had had"},{"id":"b","text":"have had"},
                        {"id":"c","text":"had have"},{"id":"d","text":"had"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! Past unreal wish: had + past participle.",
                         "incorrect": "'Had had' expresses a past unreal wish."},
            "_placeholder": True,
        }),
        ("mcq_single", "upper_intermediate", 14, {
            "prompt": "The scientist whose ___ was published won a Nobel Prize.",
            "options": [{"id":"a","text":"research"},{"id":"b","text":"researches"},
                        {"id":"c","text":"researching"},{"id":"d","text":"researcher"}],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct!",
                         "incorrect": "'Research' is uncountable here."},
            "_placeholder": True,
        }),
        ("mcq_single", "advanced", 15, {
            "prompt": "Select the sentence that uses the subjunctive correctly.",
            "options": [
                {"id":"a","text":"The committee insists that he be present."},
                {"id":"b","text":"The committee insists that he is present."},
                {"id":"c","text":"The committee insists that he was present."},
                {"id":"d","text":"The committee insists that he were present."},
            ],
            "correct_option_id": "a",
            "feedback": {"correct": "Correct! Mandative subjunctive uses the base form.",
                         "incorrect": "Mandative subjunctive: insist + that + base verb."},
            "_placeholder": True,
        }),
    ]
    for pq_type, pq_difficulty, pq_display_order, pq_payload in pq_rows:
        pq_id = str(uuid7())
        op.execute(f"""
            INSERT INTO placement_question
                (id, type, payload, difficulty, display_order, created_at, updated_at)
            VALUES ('{pq_id}', '{pq_type}', {_j(pq_payload)},
                    '{pq_difficulty}', {pq_display_order}, now(), now())
        """)

    # =========================================================================
    # Beginner A — Lesson 1: Greetings and Personal Introductions
    # Source: docs/lesson-samples/lesson 1.pdf
    # Phase 1 scope: Vocabulary + Grammar sections only.
    # Pronunciation / Listening / Reading / Speaking / Writing sections from
    # the PDF are seeded in later migrations when those engines ship (Phase 2).
    # is_guest_accessible = TRUE (only this lesson, per CLAUDE.md).
    # status = 'approved' so it appears in the learner chain immediately.
    # =========================================================================
    l1_id           = str(uuid7())
    l1_vocab_sec_id = str(uuid7())
    l1_gram_sec_id  = str(uuid7())

    op.execute(f"""
        INSERT INTO lesson
            (id, level_id, title, description, lesson_order,
             status, is_guest_accessible, created_at, updated_at)
        VALUES
            ('{l1_id}', '{lvl_beg_a_id}',
             'Greetings and Personal Introductions',
             'Learn common English greetings and how to introduce yourself.',
             1, 'approved', TRUE, now(), now())
    """)

    op.execute(f"""
        INSERT INTO lesson_section
            (id, lesson_id, category, display_order, title, created_at, updated_at)
        VALUES
            ('{l1_vocab_sec_id}', '{l1_id}', 'vocabulary', 1, 'Vocabulary', now(), now()),
            ('{l1_gram_sec_id}',  '{l1_id}', 'grammar',    2, 'Grammar',    now(), now())
    """)

    # --- Lesson 1 / Vocabulary — objectives text block (display_order=0) ---
    l1_obj_cb_id = str(uuid7())
    _l1_obj_md = (
        "## Lesson Objectives\n\n"
        "By the end of this lesson you will be able to:\n\n"
        "- Use common English greetings "
        "(hello, good morning, good evening, goodbye)\n"
        "- Say 'Nice to meet you' when meeting someone for the first time\n"
        "- Introduce yourself and ask someone's name"
    )
    op.execute(f"""
        INSERT INTO content_block
            (id, lesson_section_id, block_type, display_order, payload,
             created_at, updated_at)
        VALUES ('{l1_obj_cb_id}', '{l1_vocab_sec_id}', 'text', 0,
                {_j({"markdown": _l1_obj_md})}, now(), now())
    """)

    # --- Lesson 1 / Vocabulary — word cards and vocabulary_word rows ---
    # Vocabulary per lesson 1.pdf: Hello, Good morning, Good evening, Goodbye,
    # Nice to meet you
    l1_vw_hello_id  = str(uuid7())
    l1_vw_gm_id     = str(uuid7())  # good morning
    l1_vw_ge_id     = str(uuid7())  # good evening
    l1_vw_bye_id    = str(uuid7())  # goodbye
    l1_vw_ntmy_id   = str(uuid7())  # nice to meet you

    l1_vocab_words = [
        # (vw_id, word, definition, example_sentence, display_order)
        (l1_vw_hello_id, "hello",
         "A general greeting used at any time of day.",
         "Hello! How are you today?", 1),
        (l1_vw_gm_id, "good morning",
         "A greeting used in the morning.",
         "Good morning! Did you sleep well?", 2),
        (l1_vw_ge_id, "good evening",
         "A greeting used in the evening.",
         "Good evening! Welcome to our home.", 3),
        (l1_vw_bye_id, "goodbye",
         "A word used when leaving or parting from someone.",
         "Goodbye! See you tomorrow.", 4),
        (l1_vw_ntmy_id, "nice to meet you",
         "A phrase used when meeting someone for the first time.",
         "Nice to meet you, Saman. I am Kumari.", 5),
    ]
    for vw_id, word, defn, example, disp_order in l1_vocab_words:
        cb_id = str(uuid7())
        op.execute(f"""
            INSERT INTO vocabulary_word
                (id, lesson_section_id, word, definition, example_sentence,
                 difficulty, created_at, updated_at)
            VALUES ('{vw_id}', '{l1_vocab_sec_id}',
                    {_s(word)}, {_s(defn)}, {_s(example)},
                    'easy', now(), now())
        """)
        op.execute(f"""
            INSERT INTO content_block
                (id, lesson_section_id, block_type, display_order, payload,
                 created_at, updated_at)
            VALUES ('{cb_id}', '{l1_vocab_sec_id}', 'word_card', {disp_order},
                    {_j({"vocabulary_word_id": vw_id})}, now(), now())
        """)

    # --- Lesson 1 / Vocabulary — questions ---
    # (id, type, purpose, display_order, xp_value, vocabulary_word_id,
    #  prompt_text, payload)
    l1_vq_rows = [
        (str(uuid7()), "mcq_single", "practice", 1, 0, l1_vw_gm_id,
         "Which greeting do you use in the morning?",
         {"options": [{"id":"a","text":"Good morning"},
                      {"id":"b","text":"Good evening"},
                      {"id":"c","text":"Goodbye"},
                      {"id":"d","text":"Nice to meet you"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'Good morning' is a morning greeting.",
                       "incorrect": "'Good morning' is used in the morning."}}),
        (str(uuid7()), "mcq_single", "assessment", 2, 5, l1_vw_ntmy_id,
         "What do you say when meeting someone for the first time?",
         {"options": [{"id":"a","text":"Nice to meet you"},
                      {"id":"b","text":"Goodbye"},
                      {"id":"c","text":"Good morning"},
                      {"id":"d","text":"Hello"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'Nice to meet you' is for first meetings.",
                       "incorrect": "We say 'Nice to meet you' when meeting someone new."}}),
        (str(uuid7()), "true_false", "assessment", 3, 3, l1_vw_ge_id,
         "'Good evening' is used as a greeting in the evening.",
         {"correct_answer": True,
          "feedback": {"correct": "Correct! 'Good evening' is an evening greeting.",
                       "incorrect": "'Good evening' is indeed used in the evening."}}),
        (str(uuid7()), "fill_blank_typed", "assessment", 4, 5, l1_vw_bye_id,
         "When leaving someone, we say '___'.",
         {"sentence_with_blank": "When leaving someone, we say '___'.",
          "accepted_answers": ["goodbye", "bye"],
          "feedback": {"correct": "Correct! 'Goodbye' is used when leaving.",
                       "incorrect": "'Goodbye' is what we say when leaving someone."}}),
        (str(uuid7()), "match_pairs", "assessment", 5, 10, None,
         "Match each greeting to when it is used.",
         {"pairs": [
             {"id":"p1","left":"hello",          "right":"any time of day"},
             {"id":"p2","left":"good morning",   "right":"in the morning"},
             {"id":"p3","left":"good evening",   "right":"in the evening"},
             {"id":"p4","left":"goodbye",        "right":"when leaving"},
         ],
          "display_shuffle": True,
          "feedback": {"correct": "Well matched!",
                       "incorrect": "Try matching each greeting to the right time."}}),
    ]
    for (q_id, q_type, q_purpose, q_disp, q_xp,
         q_vw_id, q_prompt, q_payload) in l1_vq_rows:
        vw_sql = f"'{q_vw_id}'" if q_vw_id else "NULL"
        op.execute(f"""
            INSERT INTO question
                (id, lesson_section_id, type, purpose, display_order,
                 prompt_text, payload, xp_value, vocabulary_word_id,
                 created_at, updated_at)
            VALUES ('{q_id}', '{l1_vocab_sec_id}', '{q_type}', '{q_purpose}',
                    {q_disp}, {_s(q_prompt)}, {_j(q_payload)},
                    {q_xp}, {vw_sql}, now(), now())
        """)

    # --- Lesson 1 / Grammar — teaching text block (display_order=0) ---
    # Grammar topics from lesson 1.pdf: I am / You are,
    # "What is your name?", "How are you?"
    l1_g_text_id = str(uuid7())
    _l1_gram_md = (
        "## I am / You are\n\n"
        "Use **I am** to talk about yourself:\n\n"
        "- I am Saman.\n"
        "- I am a student.\n\n"
        "Use **You are** to talk to someone else:\n\n"
        "- You are Kumari.\n"
        "- You are kind.\n\n"
        "## Asking Questions\n\n"
        "- **What is your name?** — *Mama nam mokakda?*\n"
        "- **How are you?** — *Kohomada?*\n\n"
        "Common responses:\n"
        "- I am fine, thank you.\n"
        "- I am Nimal."
    )
    op.execute(f"""
        INSERT INTO content_block
            (id, lesson_section_id, block_type, display_order, payload,
             created_at, updated_at)
        VALUES ('{l1_g_text_id}', '{l1_gram_sec_id}', 'text', 0,
                {_j({"markdown": _l1_gram_md})}, now(), now())
    """)

    # --- Lesson 1 / Grammar — questions ---
    l1_gq_rows = [
        (str(uuid7()), "mcq_single", "practice", 1, 0,
         "Which sentence is correct?",
         {"options": [{"id":"a","text":"I am Saman."},
                      {"id":"b","text":"I is Saman."},
                      {"id":"c","text":"I are Saman."},
                      {"id":"d","text":"I be Saman."}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'I am' is the right form.",
                       "incorrect": "With 'I', we always use 'am'."}}),
        (str(uuid7()), "fill_blank_typed", "assessment", 2, 5,
         "Complete: '___ am fine, thank you.'",
         {"sentence_with_blank": "___ am fine, thank you.",
          "accepted_answers": ["i", "I"],
          "feedback": {"correct": "Correct! 'I am' is the first-person form.",
                       "incorrect": "The subject here is 'I'."}}),
        (str(uuid7()), "mcq_single", "assessment", 3, 5,
         "How ___ you?",
         {"options": [{"id":"a","text":"are"},{"id":"b","text":"is"},
                      {"id":"c","text":"am"},{"id":"d","text":"be"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'How are you?' is the standard greeting.",
                       "incorrect": "'How are you?' — 'are' is used with 'you'."}}),
        (str(uuid7()), "sentence_builder", "assessment", 4, 8,
         "Arrange the words to form a correct question.",
         {"chips": [{"id":"c1","text":"What"},{"id":"c2","text":"is"},
                    {"id":"c3","text":"your"},{"id":"c4","text":"name?"},
                    {"id":"c5","text":"are"},{"id":"c6","text":"How"}],
          "correct_sequence": ["c1","c2","c3","c4"],
          "feedback": {"correct": "Correct! 'What is your name?'",
                       "incorrect": "The correct question is: What is your name?"}}),
        (str(uuid7()), "correct_mistake", "assessment", 5, 8,
         "Find and fix the mistake in this sentence.",
         {"wrong_sentence": "How is you?",
          "accepted_corrections": ["How are you?"],
          "feedback": {"correct": "Correct! 'How are you?' uses 'are', not 'is'.",
                       "incorrect": "Replace 'is' with 'are': How are you?"}}),
    ]
    for (q_id, q_type, q_purpose, q_disp, q_xp, q_prompt, q_payload) in l1_gq_rows:
        op.execute(f"""
            INSERT INTO question
                (id, lesson_section_id, type, purpose, display_order,
                 prompt_text, payload, xp_value, created_at, updated_at)
            VALUES ('{q_id}', '{l1_gram_sec_id}', '{q_type}', '{q_purpose}',
                    {q_disp}, {_s(q_prompt)}, {_j(q_payload)},
                    {q_xp}, now(), now())
        """)

    # =========================================================================
    # Beginner A — Lesson 2: Family and Describing People
    # Source: docs/lesson-samples/lesson 2.pdf
    # Phase 1 scope: Vocabulary + Grammar sections only.
    # status = 'approved'; is_guest_accessible = FALSE
    # =========================================================================
    l2_id           = str(uuid7())
    l2_vocab_sec_id = str(uuid7())
    l2_gram_sec_id  = str(uuid7())

    op.execute(f"""
        INSERT INTO lesson
            (id, level_id, title, description, lesson_order,
             status, is_guest_accessible, created_at, updated_at)
        VALUES
            ('{l2_id}', '{lvl_beg_a_id}',
             'Family and Describing People',
             'Learn family vocabulary and how to describe people using '
             'possessive adjectives.',
             2, 'approved', FALSE, now(), now())
    """)

    op.execute(f"""
        INSERT INTO lesson_section
            (id, lesson_id, category, display_order, title, created_at, updated_at)
        VALUES
            ('{l2_vocab_sec_id}', '{l2_id}', 'vocabulary', 1, 'Vocabulary', now(), now()),
            ('{l2_gram_sec_id}',  '{l2_id}', 'grammar',    2, 'Grammar',    now(), now())
    """)

    # --- Lesson 2 / Vocabulary — objectives text block ---
    l2_obj_cb_id = str(uuid7())
    _l2_obj_md = (
        "## Lesson Objectives\n\n"
        "By the end of this lesson you will be able to:\n\n"
        "- Name immediate and extended family members\n"
        "- Use possessive adjectives: my, your, his, her\n"
        "- Describe family members using 'He is' and 'She is'"
    )
    op.execute(f"""
        INSERT INTO content_block
            (id, lesson_section_id, block_type, display_order, payload,
             created_at, updated_at)
        VALUES ('{l2_obj_cb_id}', '{l2_vocab_sec_id}', 'text', 0,
                {_j({"markdown": _l2_obj_md})}, now(), now())
    """)

    # --- Lesson 2 / Vocabulary — word cards and vocabulary_word rows ---
    # Vocabulary per lesson 2.pdf: Father, Mother, Brother, Sister,
    # Grandfather, Grandmother, Uncle, Aunt, Cousin
    l2_family_words = [
        # (word, definition, example_sentence, display_order)
        ("father",       "Your male parent.",
         "My father is a teacher.", 1),
        ("mother",       "Your female parent.",
         "My mother is kind.", 2),
        ("brother",      "A male sibling.",
         "My brother is tall.", 3),
        ("sister",       "A female sibling.",
         "My sister is smart.", 4),
        ("grandfather",  "The father of your mother or father.",
         "My grandfather is old and wise.", 5),
        ("grandmother",  "The mother of your mother or father.",
         "My grandmother cooks very well.", 6),
        ("uncle",        "The brother of your mother or father.",
         "My uncle lives in Colombo.", 7),
        ("aunt",         "The sister of your mother or father.",
         "My aunt is a doctor.", 8),
        ("cousin",       "The child of your uncle or aunt.",
         "My cousin and I go to the same school.", 9),
    ]
    l2_vw_ids = {}  # word → uuid; used for vocabulary_word_id FK on questions
    for word, defn, example, disp_order in l2_family_words:
        vw_id = str(uuid7())
        cb_id = str(uuid7())
        l2_vw_ids[word] = vw_id
        op.execute(f"""
            INSERT INTO vocabulary_word
                (id, lesson_section_id, word, definition, example_sentence,
                 difficulty, created_at, updated_at)
            VALUES ('{vw_id}', '{l2_vocab_sec_id}',
                    {_s(word)}, {_s(defn)}, {_s(example)},
                    'easy', now(), now())
        """)
        op.execute(f"""
            INSERT INTO content_block
                (id, lesson_section_id, block_type, display_order, payload,
                 created_at, updated_at)
            VALUES ('{cb_id}', '{l2_vocab_sec_id}', 'word_card', {disp_order},
                    {_j({"vocabulary_word_id": vw_id})}, now(), now())
        """)

    # --- Lesson 2 / Vocabulary — questions ---
    l2_vq_rows = [
        (str(uuid7()), "mcq_single", "practice", 1, 0, "mother",
         "What do we call the female parent?",
         {"options": [{"id":"a","text":"Mother"},{"id":"b","text":"Father"},
                      {"id":"c","text":"Sister"},{"id":"d","text":"Aunt"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! The female parent is the mother.",
                       "incorrect": "The female parent is the 'mother'."}}),
        (str(uuid7()), "mcq_single", "assessment", 2, 5, "grandfather",
         "What do we call the father of your father?",
         {"options": [{"id":"a","text":"Grandfather"},{"id":"b","text":"Uncle"},
                      {"id":"c","text":"Father"},{"id":"d","text":"Cousin"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! Your father's father is your grandfather.",
                       "incorrect": "Your father's father is your 'grandfather'."}}),
        (str(uuid7()), "true_false", "assessment", 3, 3, "aunt",
         "An aunt is a male family member.",
         {"correct_answer": False,
          "feedback": {"correct": "Correct! An aunt is female.",
                       "incorrect": "An aunt is female — the brother would be an uncle."}}),
        (str(uuid7()), "fill_blank_typed", "assessment", 4, 5, "sister",
         "My father's daughter is my '___'.",
         {"sentence_with_blank": "My father's daughter is my '___'.",
          "accepted_answers": ["sister"],
          "feedback": {"correct": "Correct! Your father's daughter is your sister.",
                       "incorrect": "Your father's daughter is your 'sister'."}}),
        (str(uuid7()), "match_pairs", "assessment", 5, 10, None,
         "Match each family member to their description.",
         {"pairs": [
             {"id":"p1","left":"father",      "right":"male parent"},
             {"id":"p2","left":"mother",      "right":"female parent"},
             {"id":"p3","left":"brother",     "right":"male sibling"},
             {"id":"p4","left":"sister",      "right":"female sibling"},
         ],
          "display_shuffle": True,
          "feedback": {"correct": "Well matched!",
                       "incorrect": "Try matching each family member again."}}),
    ]
    for (q_id, q_type, q_purpose, q_disp, q_xp,
         q_vw_key, q_prompt, q_payload) in l2_vq_rows:
        vw_sql = f"'{l2_vw_ids[q_vw_key]}'" if q_vw_key else "NULL"
        op.execute(f"""
            INSERT INTO question
                (id, lesson_section_id, type, purpose, display_order,
                 prompt_text, payload, xp_value, vocabulary_word_id,
                 created_at, updated_at)
            VALUES ('{q_id}', '{l2_vocab_sec_id}', '{q_type}', '{q_purpose}',
                    {q_disp}, {_s(q_prompt)}, {_j(q_payload)},
                    {q_xp}, {vw_sql}, now(), now())
        """)

    # --- Lesson 2 / Grammar — teaching text block ---
    # Grammar topics from lesson 2.pdf: My/Your/His/Her, He is/She is,
    # Who is he?, Is she your sister?
    l2_g_text_id = str(uuid7())
    _l2_gram_md = (
        "## Possessive Adjectives\n\n"
        "| | |\n"
        "|---|---|\n"
        "| **my** | belongs to me |\n"
        "| **your** | belongs to you |\n"
        "| **his** | belongs to a boy or man |\n"
        "| **her** | belongs to a girl or woman |\n\n"
        "Examples:\n\n"
        "- **My** brother is tall.\n"
        "- **His** name is Saman.\n"
        "- **Her** sister is kind.\n\n"
        "## Describing Family Members\n\n"
        "- **He is** my brother. *(for a boy or man)*\n"
        "- **She is** my sister. *(for a girl or woman)*\n\n"
        "## Asking Questions\n\n"
        "- **Who is he?** — He is my uncle.\n"
        "- **Is she your sister?** — Yes, she is."
    )
    op.execute(f"""
        INSERT INTO content_block
            (id, lesson_section_id, block_type, display_order, payload,
             created_at, updated_at)
        VALUES ('{l2_g_text_id}', '{l2_gram_sec_id}', 'text', 0,
                {_j({"markdown": _l2_gram_md})}, now(), now())
    """)

    # --- Lesson 2 / Grammar — questions ---
    l2_gq_rows = [
        (str(uuid7()), "mcq_single", "practice", 1, 0,
         "Which sentence correctly uses 'his'?",
         {"options": [{"id":"a","text":"His brother is tall."},
                      {"id":"b","text":"He brother is tall."},
                      {"id":"c","text":"Her brother is tall."},
                      {"id":"d","text":"Hers brother is tall."}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'His' is the possessive for a boy or man.",
                       "incorrect": "'His' is used before a noun to show it belongs to him."}}),
        (str(uuid7()), "fill_blank_typed", "assessment", 2, 5,
         "Complete: '___ name is Kumari.' (Kumari is a girl.)",
         {"sentence_with_blank": "___ name is Kumari.",
          "accepted_answers": ["her"],
          "feedback": {"correct": "Correct! 'Her' is used for a girl or woman.",
                       "incorrect": "Kumari is a girl, so we use 'Her'."}}),
        (str(uuid7()), "mcq_single", "assessment", 3, 5,
         "___ is he? — He is my uncle.",
         {"options": [{"id":"a","text":"Who"},{"id":"b","text":"How"},
                      {"id":"c","text":"What"},{"id":"d","text":"Where"}],
          "correct_option_id": "a",
          "feedback": {"correct": "Correct! 'Who' asks about a person's identity.",
                       "incorrect": "'Who' is used to ask about a person."}}),
        (str(uuid7()), "sentence_builder", "assessment", 4, 8,
         "Arrange the words to form a correct sentence.",
         {"chips": [{"id":"c1","text":"She"},{"id":"c2","text":"is"},
                    {"id":"c3","text":"my"},{"id":"c4","text":"sister."},
                    {"id":"c5","text":"He"},{"id":"c6","text":"your"}],
          "correct_sequence": ["c1","c2","c3","c4"],
          "feedback": {"correct": "Well done! 'She is my sister.'",
                       "incorrect": "The correct sentence is: She is my sister."}}),
        (str(uuid7()), "correct_mistake", "assessment", 5, 8,
         "Find and fix the mistake in this sentence.",
         {"wrong_sentence": "He are my brother.",
          "accepted_corrections": ["He is my brother."],
          "feedback": {"correct": "Correct! 'He is', not 'He are'.",
                       "incorrect": "Replace 'are' with 'is': He is my brother."}}),
    ]
    for (q_id, q_type, q_purpose, q_disp, q_xp, q_prompt, q_payload) in l2_gq_rows:
        op.execute(f"""
            INSERT INTO question
                (id, lesson_section_id, type, purpose, display_order,
                 prompt_text, payload, xp_value, created_at, updated_at)
            VALUES ('{q_id}', '{l2_gram_sec_id}', '{q_type}', '{q_purpose}',
                    {q_disp}, {_s(q_prompt)}, {_j(q_payload)},
                    {q_xp}, now(), now())
        """)

    # =========================================================================
    # feature_flag — per OQ-5.1 tier mapping
    # =========================================================================
    ff_rows = [
        ("ai_tutor",
         "AI Tutor Chat access",
         False, ["basic", "premium"]),
        ("daily_essay",
         "Daily Essay writing and AI-graded submission",
         False, ["basic", "premium"]),
        ("premium_levels",
         "Access to Elementary level and above",
         False, ["premium"]),
    ]
    for ff_key, ff_desc, ff_default, ff_tiers in ff_rows:
        ff_id = str(uuid7())
        tiers_sql = "ARRAY[" + ", ".join(f"'{t}'" for t in ff_tiers) + "]"
        default_sql = "TRUE" if ff_default else "FALSE"
        op.execute(f"""
            INSERT INTO feature_flag
                (id, flag_key, description, default_value, enabled_for_tiers,
                 created_at, updated_at)
            VALUES ('{ff_id}', '{ff_key}', {_s(ff_desc)},
                    {default_sql}, {tiers_sql}, now(), now())
        """)


def downgrade() -> None:
    # Delete in reverse FK dependency order.

    # vocabulary_word has ON DELETE RESTRICT on lesson_section; must be removed
    # before deleting lesson (which cascades through lesson_section).
    op.execute("""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id IN (
            SELECT ls.id
            FROM   lesson_section ls
            JOIN   lesson l  ON l.id  = ls.lesson_id
            JOIN   level  lv ON lv.id = l.level_id
            WHERE  lv.code IN (
                'beginner_a', 'beginner_b', 'elementary',
                'intermediate', 'upper_intermediate', 'advanced'
            )
        )
    """)

    # Deleting lesson cascades to lesson_section → content_block + question.
    op.execute("""
        DELETE FROM lesson
        WHERE level_id IN (
            SELECT id FROM level
            WHERE code IN (
                'beginner_a', 'beginner_b', 'elementary',
                'intermediate', 'upper_intermediate', 'advanced'
            )
        )
    """)

    # placement_scoring_rule has ON DELETE RESTRICT on level.
    op.execute("""
        DELETE FROM placement_scoring_rule
        WHERE recommended_level_id IN (
            SELECT id FROM level
            WHERE code IN (
                'beginner_a', 'beginner_b', 'elementary',
                'intermediate', 'upper_intermediate', 'advanced'
            )
        )
    """)

    op.execute("""
        DELETE FROM level
        WHERE code IN (
            'beginner_a', 'beginner_b', 'elementary',
            'intermediate', 'upper_intermediate', 'advanced'
        )
    """)

    # This migration seeds ALL placement questions; full delete is safe.
    op.execute("DELETE FROM placement_question")

    # This migration seeds ALL xp_rules; full delete is safe.
    op.execute("DELETE FROM xp_rule")

    op.execute("""
        DELETE FROM streak_milestone WHERE days IN (7, 14, 30, 60, 90, 180, 365)
    """)

    op.execute("""
        DELETE FROM feature_flag
        WHERE flag_key IN ('ai_tutor', 'daily_essay', 'premium_levels')
    """)
