"""Add two image-based placement questions for UI testing.

Scenario A (display_order 16):
  - prompt_image_url set → image shown above question text
  - options are plain text
  Upload: placement/images/apple.jpg to Supabase Storage

Scenario B (display_order 17):
  - no prompt_image_url
  - each option has image_url + label → rendered as image grid
  Upload: placement/images/sandwich.jpg
          placement/images/pizza.jpg
          placement/images/burger.jpg
          placement/images/salad.jpg

Revision ID: 9b8a7c6d5e4f
Revises:     f5a6b7c8d9e0
Create Date: 2026-06-08
"""
import json
from typing import Sequence, Union
from uuid import uuid4

from alembic import op

revision: str = "9b8a7c6d5e4f"
down_revision: Union[str, None] = "f5a6b7c8d9e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


_QUESTIONS = [
    # ── Scenario A — image as stimulus, text options ──────────────────────────
    # Upload placement/images/apple.jpg to Supabase Storage before testing.
    (
        "mcq_single", "beginner_a", "vocabulary", 16, 3,
        "What is this?",
        {
            "prompt_image_url": "placement/images/apple.jpg",
            "options": [
                {"id": "a", "text": "Apple"},
                {"id": "b", "text": "Banana"},
                {"id": "c", "text": "Mango"},
                {"id": "d", "text": "Orange"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! That is an apple.",
                "incorrect": "That is an apple — a common red or green fruit.",
            },
        },
    ),
    # ── Scenario B — image options with labels ────────────────────────────────
    # Upload these to Supabase Storage before testing:
    #   placement/images/sandwich.jpg
    #   placement/images/pizza.jpg
    #   placement/images/burger.jpg
    #   placement/images/salad.jpg
    (
        "mcq_single", "beginner_a", "vocabulary", 17, 3,
        "Which one of these is a sandwich?",
        {
            "options": [
                {"id": "a", "image_url": "placement/images/sandwich.jpg", "label": "Sandwich"},
                {"id": "b", "image_url": "placement/images/pizza.jpg",    "label": "Pizza"},
                {"id": "c", "image_url": "placement/images/burger.jpg",   "label": "Burger"},
                {"id": "d", "image_url": "placement/images/salad.jpg",    "label": "Salad"},
            ],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! A sandwich has filling between two slices of bread.",
                "incorrect": "The sandwich is two slices of bread with a filling inside.",
            },
        },
    ),
]


def upgrade() -> None:
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
    op.execute("DELETE FROM placement_question WHERE display_order IN (16, 17)")
