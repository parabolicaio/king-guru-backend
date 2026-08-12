"""Expand the placement question bank from 17 to 30 questions.

Task #24 Phase F prerequisite (kingguru-task24-placement-lessons-production-plan.md
§7): the adaptive ladder needs >=3 questions per level minimum, ~5 for variety.
Live bank before this migration: beginner_a 5, beginner_b 3, elementary 3,
intermediate 3, upper_intermediate 2, advanced 1 (17 total). This adds 13 new
rows (display_order 18-30) to bring every level to 5, matching xp_value tiers
already established in 0006 (beginner 3, elementary/intermediate 5,
upper_intermediate/advanced 8).

Content-authoring notes (Sonnet-drafted, PENDING Nisal review before deploy —
see kingguru-task24-placement-lessons-production-plan.md §10 decision #3):
  - Types restricted to mcq_single / true_false / fill_blank_typed — the only
    3 types the web placement quiz page actually renders (per Task #24 audit).
    match_pairs/order_events/sentence_builder are scoring-engine-only; no
    client UI exists for them in the placement flow.
  - Correct-option position deliberately varied across a/b/c/d (0042 fixed a
    live bug where 13/13 existing MCQs had the answer at option 'a').
  - Sinhala translations follow the 0043 convention: only the prompt is
    translated; the tested English word/sentence stays in English so the
    translation doesn't give the answer away.

Renumbered 0045 -> 0046 for Task #25 Phase 1: the level restructure took the
0045 slot, so this now chains after it. The two rows originally tagged
'beginner_b' are retagged 'elementary' to satisfy the restructure's tightened
5-code difficulty CHECK. Content is still HELD (unpushed) pending Nisal review.

Revision ID: 0e1f2a3b4c5d
Revises:     b1a2c3d4e5f6
Create Date: 2026-07-21
"""
import json
from typing import Sequence, Union
from uuid import uuid4

from alembic import op

revision: str = "0e1f2a3b4c5d"
down_revision: Union[str, None] = "b1a2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


# Each row: (type, difficulty, skill_category, display_order, xp_value,
#            prompt_text, payload, si_prompt_text)
_QUESTIONS = [
    # ── Elementary (ex-Beginner B, retagged for Task #25 5-code taxonomy) ────
    (
        "mcq_single", "elementary", "vocabulary", 18, 3,
        "Which word means the same as 'happy'?",
        {
            "options": [
                {"id": "a", "text": "sad"},
                {"id": "b", "text": "glad"},
                {"id": "c", "text": "angry"},
                {"id": "d", "text": "tired"},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! 'Glad' means the same as 'happy'.",
                "incorrect": "'Glad' is a synonym for 'happy'. The others mean something different.",
            },
        },
        "'happy' යන වචනයට සමාන අර්ථය ඇති වචනය කුමක්ද?",
    ),
    (
        "true_false", "elementary", "grammar", 19, 3,
        "'They is my friends' is a correct English sentence.",
        {
            "correct_answer": False,
            "feedback": {
                "correct": "Correct — it should be 'They are my friends'.",
                "incorrect": "This is incorrect. With 'they', use 'are', not 'is': 'They are my friends'.",
            },
        },
        "'They is my friends' යනු නිවැරදි ඉංග්‍රීසි වාක්‍යයකි.",
    ),
    # ── Elementary (+2, → 5) ─────────────────────────────────────────────────
    (
        "mcq_single", "elementary", "vocabulary", 20, 5,
        "Which word means the opposite of 'difficult'?",
        {
            "options": [
                {"id": "a", "text": "hard"},
                {"id": "b", "text": "heavy"},
                {"id": "c", "text": "easy"},
                {"id": "d", "text": "slow"},
            ],
            "correct_option_id": "c",
            "feedback": {
                "correct": "Correct! 'Easy' is the opposite of 'difficult'.",
                "incorrect": "The antonym of 'difficult' is 'easy'.",
            },
        },
        "'difficult' යන වචනයේ විරුද්ධ පදය කුමක්ද?",
    ),
    (
        "fill_blank_typed", "elementary", "grammar", 21, 5,
        "Complete the sentence: Yesterday, I _____ to the market with my mother.",
        {
            "accepted_answers": ["went", "walked", "traveled", "travelled"],
            "feedback": {
                "correct": "Good! You correctly used the past tense.",
                "incorrect": "Try 'went' or 'walked' — the sentence needs the past tense.",
            },
        },
        "වාක්‍යය සම්පූර්ණ කරන්න: Yesterday, I _____ to the market with my mother.",
    ),
    # ── Intermediate (+2, → 5) ───────────────────────────────────────────────
    (
        "mcq_single", "intermediate", "grammar", 22, 5,
        "I have been working here ___ five years.",
        {
            "options": [
                {"id": "a", "text": "since"},
                {"id": "b", "text": "during"},
                {"id": "c", "text": "while"},
                {"id": "d", "text": "for"},
            ],
            "correct_option_id": "d",
            "feedback": {
                "correct": "Correct! Use 'for' with a duration (five years).",
                "incorrect": "Use 'for' with a length of time (for five years); 'since' is used with a starting point (since 2021).",
            },
        },
        "හිස්තැනට ගැලපෙන වචනය තෝරන්න.",
    ),
    (
        "true_false", "intermediate", "vocabulary", 23, 5,
        "'Enormous' means very small.",
        {
            "correct_answer": False,
            "feedback": {
                "correct": "Correct — 'enormous' means very large.",
                "incorrect": "'Enormous' actually means very large, not small.",
            },
        },
        "'Enormous' යන්නෙහි තේරුම ඉතා කුඩා යනුයි.",
    ),
    # ── Upper Intermediate (+3, → 5) ─────────────────────────────────────────
    (
        "mcq_single", "upper_intermediate", "grammar", 24, 8,
        "Had she studied harder, she ___ the exam.",
        {
            "options": [
                {"id": "a", "text": "would pass"},
                {"id": "b", "text": "would have passed"},
                {"id": "c", "text": "will pass"},
                {"id": "d", "text": "had passed"},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! Third conditional: had + past participle, would have + past participle.",
                "incorrect": "This is a third conditional (an unreal past). Use 'would have passed'.",
            },
        },
        "හිස්තැනට ගැලපෙන පිළිතුර තෝරන්න.",
    ),
    (
        "mcq_single", "upper_intermediate", "vocabulary", 25, 8,
        "Choose the word closest in meaning to 'meticulous'.",
        {
            "options": [
                {"id": "a", "text": "careless"},
                {"id": "b", "text": "hurried"},
                {"id": "c", "text": "thorough"},
                {"id": "d", "text": "confident"},
            ],
            "correct_option_id": "c",
            "feedback": {
                "correct": "Correct! 'Meticulous' means showing great attention to detail — close to 'thorough'.",
                "incorrect": "'Meticulous' means very careful and thorough, not careless or hurried.",
            },
        },
        "'meticulous' යන වචනයට ආසන්නම අර්ථය ඇති වචනය තෝරන්න.",
    ),
    (
        "fill_blank_typed", "upper_intermediate", "grammar", 26, 8,
        "Complete the sentence: She said that she _____ the report by Friday.",
        {
            "accepted_answers": ["would finish", "would have finished", "would submit"],
            "feedback": {
                "correct": "Correct! In reported speech, 'will' shifts to 'would'.",
                "incorrect": "In reported speech, 'will finish' becomes 'would finish'.",
            },
        },
        "වාක්‍යය සම්පූර්ණ කරන්න: She said that she _____ the report by Friday.",
    ),
    # ── Advanced (+4, → 5) ───────────────────────────────────────────────────
    (
        "mcq_single", "advanced", "grammar", 27, 8,
        "Identify the sentence with correct use of the cleft construction.",
        {
            "options": [
                {"id": "a", "text": "It was John who the letter wrote."},
                {"id": "b", "text": "What John wrote was the letter it."},
                {"id": "c", "text": "The letter, John wrote it."},
                {"id": "d", "text": "It was John who wrote the letter."},
            ],
            "correct_option_id": "d",
            "feedback": {
                "correct": "Correct! 'It was John who wrote the letter' is a well-formed it-cleft.",
                "incorrect": "The correct it-cleft keeps normal word order after 'who': 'It was John who wrote the letter.'",
            },
        },
        "Cleft වාක්‍ය ව්‍යුහය නිවැරදිව භාවිතා කරන වාක්‍යය තෝරන්න.",
    ),
    (
        "mcq_single", "advanced", "vocabulary", 28, 8,
        "The critic's review was scathing, leaving the author feeling utterly _____.",
        {
            "options": [
                {"id": "a", "text": "elated"},
                {"id": "b", "text": "crestfallen"},
                {"id": "c", "text": "indifferent"},
                {"id": "d", "text": "vindicated"},
            ],
            "correct_option_id": "b",
            "feedback": {
                "correct": "Correct! 'Crestfallen' means deeply disappointed or dejected, matching a scathing review.",
                "incorrect": "'Crestfallen' (deeply disheartened) best fits the effect of a scathing review.",
            },
        },
        "වාක්‍යයට වඩාත්ම ගැලපෙන වචනය තෝරන්න: The critic's review was scathing, leaving the author feeling utterly _____.",
    ),
    (
        "true_false", "advanced", "grammar", 29, 8,
        "'Were I to accept the offer, I would relocate immediately' is a grammatically correct use of the inverted conditional.",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Correct! Inverting 'If I were to accept' to 'Were I to accept' is a formal, valid conditional structure.",
                "incorrect": "This is actually correct — inverting 'if' with 'were' ('Were I to...') is a formal alternative to 'If I were to...'.",
            },
        },
        "'Were I to accept the offer, I would relocate immediately' යනු inverted conditional ව්‍යුහයේ නිවැරදි භාවිතයකි.",
    ),
    (
        "fill_blank_typed", "advanced", "grammar", 30, 8,
        "Complete the sentence: No sooner had he arrived _____ the phone rang.",
        {
            "accepted_answers": ["than"],
            "feedback": {
                "correct": "Correct! 'No sooner... than...' is the correct inversion structure.",
                "incorrect": "The correct pairing is 'no sooner... than...'.",
            },
        },
        "වාක්‍යය සම්පූර්ණ කරන්න: No sooner had he arrived _____ the phone rang.",
    ),
]


def upgrade() -> None:
    for (q_type, difficulty, skill_category, display_order, xp_value,
         prompt_text, payload, si_prompt_text) in _QUESTIONS:
        q_id = str(uuid4())
        translations = {"si": {"prompt_text": si_prompt_text}}
        op.execute(f"""
            INSERT INTO placement_question
                (id, type, difficulty, skill_category, display_order,
                 xp_value, prompt_text, payload, translations,
                 created_at, updated_at)
            VALUES (
                '{q_id}', {_s(q_type)}, {_s(difficulty)}, {_s(skill_category)},
                {display_order}, {xp_value}, {_s(prompt_text)},
                {_j(payload)}, {_j(translations)}, now(), now()
            )
        """)


def downgrade() -> None:
    op.execute("DELETE FROM placement_question WHERE display_order BETWEEN 18 AND 30")
