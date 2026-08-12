"""Replace placeholder placement questions with proper seed data.

The original 15 rows in placement_question were stubs: prompt_text,
skill_category and xp_value were all NULL because those columns were added
in a later migration and never backfilled.  This migration drops them and
inserts 15 proper questions that the placement API endpoint can serve.

Distribution (matches the original intent):
  beginner_a         × 3   (xp_value 3)
  beginner_b         × 3   (xp_value 3)
  elementary         × 3   (xp_value 5)
  intermediate       × 3   (xp_value 5)
  upper_intermediate × 2   (xp_value 8)
  advanced           × 1   (xp_value 8)

Revision ID: f6a7b8c9d0e1
Revises:     e5f6a7b8c9d0
Create Date: 2026-06-08
"""
import json
from typing import Sequence, Union
from uuid import uuid4

from alembic import op

revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


# Each row: (type, difficulty, skill_category, display_order, xp_value,
#            prompt_text, payload)
_QUESTIONS = [
    # ── Beginner A ────────────────────────────────────────────────────────────
    (
        "mcq_single", "beginner_a", "vocabulary", 1, 3,
        "Which word is a greeting?",
        {
            "options": [
                {"id": "a", "text": "Hello"},
                {"id": "b", "text": "Table"},
                {"id": "c", "text": "Run"},
                {"id": "d", "text": "Blue"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Hello' is a common greeting.",
                "incorrect": "'Hello' is the greeting. The others are a noun, verb, and adjective.",
            },
        },
    ),
    (
        "true_false", "beginner_a", "grammar", 2, 3,
        "'I am a student' is a correct English sentence.",
        {
            "correct_answer": True,
            "feedback": {
                "correct": "Yes — 'I am' is correct for first-person singular.",
                "incorrect": "'I am a student' is correct. With 'I' we always use 'am'.",
            },
        },
    ),
    (
        "mcq_single", "beginner_a", "grammar", 3, 3,
        "Choose the correct word: ___ name is Saman.",
        {
            "options": [
                {"id": "a", "text": "My"},
                {"id": "b", "text": "Me"},
                {"id": "c", "text": "I"},
                {"id": "d", "text": "Mine"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'My' is the possessive adjective.",
                "incorrect": "'My' is used before a noun to show possession.",
            },
        },
    ),
    # ── Beginner B ────────────────────────────────────────────────────────────
    (
        "mcq_single", "beginner_b", "grammar", 4, 3,
        "What is the plural of 'child'?",
        {
            "options": [
                {"id": "a", "text": "children"},
                {"id": "b", "text": "childs"},
                {"id": "c", "text": "childes"},
                {"id": "d", "text": "child"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Children' is the irregular plural.",
                "incorrect": "The plural of 'child' is irregular: children.",
            },
        },
    ),
    (
        "mcq_single", "beginner_b", "grammar", 5, 3,
        "Which sentence is correct?",
        {
            "options": [
                {"id": "a", "text": "She has two brothers."},
                {"id": "b", "text": "She have two brothers."},
                {"id": "c", "text": "She are two brothers."},
                {"id": "d", "text": "She am two brothers."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Well done! 'She has' is correct third-person singular.",
                "incorrect": "With 'she', use 'has', not 'have', 'are', or 'am'.",
            },
        },
    ),
    (
        "true_false", "beginner_b", "grammar", 6, 3,
        "The past tense of 'go' is 'goed'.",
        {
            "correct_answer": False,
            "feedback": {
                "correct": "Correct — the past tense of 'go' is 'went'.",
                "incorrect": "The past tense is 'went', not 'goed'. It is an irregular verb.",
            },
        },
    ),
    # ── Elementary ────────────────────────────────────────────────────────────
    (
        "mcq_single", "elementary", "grammar", 7, 5,
        "She ___ to school every morning.",
        {
            "options": [
                {"id": "a", "text": "goes"},
                {"id": "b", "text": "go"},
                {"id": "c", "text": "going"},
                {"id": "d", "text": "gone"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Third-person singular present simple uses 'goes'.",
                "incorrect": "With 'she/he/it' in present simple, add -s or -es: goes.",
            },
        },
    ),
    (
        "fill_blank_typed", "elementary", "grammar", 8, 5,
        "Complete the sentence: If it rains, I _____ an umbrella.",
        {
            "accepted_answers": ["use", "will use", "take", "will take", "carry", "will carry"],
            "feedback": {
                "correct": "Good! You need something to stay dry.",
                "incorrect": "Try: 'use', 'take', or 'carry' — with or without 'will'.",
            },
        },
    ),
    (
        "mcq_single", "elementary", "vocabulary", 9, 5,
        "Which word means the opposite of 'cheap'?",
        {
            "options": [
                {"id": "a", "text": "expensive"},
                {"id": "b", "text": "old"},
                {"id": "c", "text": "slow"},
                {"id": "d", "text": "small"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Expensive' is the opposite of 'cheap'.",
                "incorrect": "The antonym of 'cheap' is 'expensive'.",
            },
        },
    ),
    # ── Intermediate ──────────────────────────────────────────────────────────
    (
        "mcq_single", "intermediate", "grammar", 10, 5,
        "By the time she arrived, the meeting ___ already started.",
        {
            "options": [
                {"id": "a", "text": "had"},
                {"id": "b", "text": "has"},
                {"id": "c", "text": "have"},
                {"id": "d", "text": "was"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! Past perfect 'had started' shows the earlier action.",
                "incorrect": "Use past perfect (had + past participle) for an action completed before another past event.",
            },
        },
    ),
    (
        "fill_blank_typed", "intermediate", "grammar", 11, 5,
        "Despite the rain, they _____ to complete the project on time.",
        {
            "accepted_answers": ["managed", "were able to manage", "were able to"],
            "feedback": {
                "correct": "Excellent! 'Managed' fits perfectly here.",
                "incorrect": "Try 'managed' — it expresses succeeding despite difficulty.",
            },
        },
    ),
    (
        "mcq_single", "intermediate", "grammar", 12, 5,
        "Which sentence uses the passive voice correctly?",
        {
            "options": [
                {"id": "a", "text": "The letter was written by her."},
                {"id": "b", "text": "She written the letter."},
                {"id": "c", "text": "Her wrote the letter."},
                {"id": "d", "text": "The letter wrote by her."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct passive voice structure!",
                "incorrect": "Passive voice: subject + was/were + past participle + by + agent.",
            },
        },
    ),
    # ── Upper Intermediate ────────────────────────────────────────────────────
    (
        "mcq_single", "upper_intermediate", "grammar", 13, 8,
        "I wish I ___ more time to study when I was young.",
        {
            "options": [
                {"id": "a", "text": "had had"},
                {"id": "b", "text": "have had"},
                {"id": "c", "text": "had"},
                {"id": "d", "text": "would have"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Had had' expresses a past unreal wish.",
                "incorrect": "For a past wish about something that did not happen, use 'wish + past perfect (had had)'.",
            },
        },
    ),
    (
        "mcq_single", "upper_intermediate", "vocabulary", 14, 8,
        "Choose the word that best completes the sentence: The politician's speech was deliberately _____, avoiding any clear commitment.",
        {
            "options": [
                {"id": "a", "text": "ambiguous"},
                {"id": "b", "text": "concise"},
                {"id": "c", "text": "eloquent"},
                {"id": "d", "text": "candid"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Ambiguous' means open to more than one interpretation.",
                "incorrect": "'Ambiguous' is the right word — it means unclear or having multiple possible meanings.",
            },
        },
    ),
    # ── Advanced ──────────────────────────────────────────────────────────────
    (
        "mcq_single", "advanced", "grammar", 15, 8,
        "Select the sentence that uses the mandative subjunctive correctly.",
        {
            "options": [
                {"id": "a", "text": "The board requires that he submit a report."},
                {"id": "b", "text": "The board requires that he submits a report."},
                {"id": "c", "text": "The board requires that he submitted a report."},
                {"id": "d", "text": "The board requires that he would submit a report."},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! The mandative subjunctive uses the bare infinitive (submit, not submits).",
                "incorrect": "After verbs like require/insist/demand + that, use the bare infinitive: 'he submit', not 'he submits'.",
            },
        },
    ),
]


def upgrade() -> None:
    op.execute("DELETE FROM placement_question")

    for (q_type, difficulty, skill_category, display_order,
         xp_value, prompt_text, payload) in _QUESTIONS:
        q_id = str(uuid4())
        op.execute(f"""
            INSERT INTO placement_question
                (id, type, difficulty, skill_category, display_order,
                 xp_value, prompt_text, payload, translations,
                 created_at, updated_at)
            VALUES (
                '{q_id}', {_s(q_type)}, {_s(difficulty)}, {_s(skill_category)},
                {display_order}, {xp_value}, {_s(prompt_text)},
                {_j(payload)}, '{{}}', now(), now()
            )
        """)


def downgrade() -> None:
    op.execute("DELETE FROM placement_question")
