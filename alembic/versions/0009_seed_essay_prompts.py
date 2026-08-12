"""Seed 10 universal essay prompts (level_id = NULL, date_assigned = NULL).

These are always-available fallback prompts for any level that has
daily_essay_enabled = TRUE (Elementary and above).  Each prompt has an
English text and a Sinhala translation stored in the translations JSONB.

Revision ID: c2d3e4f5a6b7
Revises:     b1c2d3e4f5a6
Create Date: 2026-06-08
"""
from typing import Sequence, Union

from alembic import op

revision: str = "c2d3e4f5a6b7"
down_revision: Union[str, None] = "b1c2d3e4f5a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Hardcoded UUIDs keep the seed idempotent across environments.
PROMPTS = [
    (
        "11111111-e001-0000-0000-000000000001",
        "Describe a typical day in your life from morning to night.",
        "ඔබේ සාමාන්‍ය දිනය උදේ සිට රාත්‍රිය දක්වා විස්තර කරන්න.",
    ),
    (
        "11111111-e001-0000-0000-000000000002",
        "Write about your favourite food. What is it, and why do you enjoy it?",
        "ඔබේ ප්‍රිය ආහාරය ගැන ලියන්න. එය කුමක්ද, ඔබ එය ප්‍රිය කරන්නේ ඇයි?",
    ),
    (
        "11111111-e001-0000-0000-000000000003",
        "Describe your hometown or neighbourhood. What do you love most about where you live?",
        "ඔබේ නගරය හෝ අසල්වැසි ප්‍රදේශය විස්තර කරන්න. ඔබ ජීවත්වන ස්ථානය ගැන ඔබ ප්‍රිය කරන්නේ ඇයි?",
    ),
    (
        "11111111-e001-0000-0000-000000000004",
        "Write about a person who has had a big influence on your life. Who are they and what did they teach you?",
        "ඔබේ ජීවිතයට විශාල බලපෑමක් ඇති කළ කෙනෙකු ගැන ලියන්න. ඔවුන් කවුද සහ ඔවුන් ඔබට ඉගැන්නූ දේ කුමක්ද?",
    ),
    (
        "11111111-e001-0000-0000-000000000005",
        "What is your favourite hobby? How did you start doing it and why do you enjoy it?",
        "ඔබේ ප්‍රිය විනෝදාංශය කුමක්ද? ඔබ එය ආරම්භ කළේ කෙසේද සහ ඔබ එය ප්‍රිය කරන්නේ ඇයි?",
    ),
    (
        "11111111-e001-0000-0000-000000000006",
        "Describe your best friend. What makes them a good friend to you?",
        "ඔබේ හොඳම මිතුරා විස්තර කරන්න. ඔවුන් ඔබට හොඳ මිතුරෙකු වන්නේ ඇයි?",
    ),
    (
        "11111111-e001-0000-0000-000000000007",
        "Write about a time you helped someone. What happened and how did it make you feel?",
        "ඔබ කෙනෙකුට උදව් කළ අවස්ථාවක් ගැන ලියන්න. කුමක් සිදු විය සහ ඔබට කෙසේ දැනුනිද?",
    ),
    (
        "11111111-e001-0000-0000-000000000008",
        "What is your dream job? Describe what you would do and explain why you want to do it.",
        "ඔබේ සිහිනයේ රැකියාව කුමක්ද? ඔබ කරන දේ විස්තර කර ඔබ එය කිරීමට කැමති ඇයි යන්න පැහැදිලි කරන්න.",
    ),
    (
        "11111111-e001-0000-0000-000000000009",
        "Describe a memorable celebration or festival you have attended. What made it special?",
        "ඔබ සහභාගී වූ අමතක නොවෙන උත්සවයක් හෝ සැමරීමක් විස්තර කරන්න. එය විශේෂ වූයේ ඇයි?",
    ),
    (
        "11111111-e001-0000-0000-000000000010",
        "Write about the importance of learning English in your daily life. How does it help you?",
        "ඔබේ දෛනික ජීවිතයේ ඉංග්‍රීසි ඉගෙනීමේ වැදගත්කම ගැන ලියන්න. එය ඔබට කෙසේ උපකාර වේද?",
    ),
]


def upgrade() -> None:
    for uid, prompt_text, sinhala in PROMPTS:
        op.execute(f"""
            INSERT INTO essay_prompt (id, prompt_text, translations, is_active, created_at, updated_at)
            VALUES (
                '{uid}',
                $prompt${prompt_text}$prompt$,
                jsonb_build_object('si', $si${sinhala}$si$),
                TRUE,
                now(),
                now()
            )
            ON CONFLICT (id) DO NOTHING
        """)


def downgrade() -> None:
    ids = ", ".join(f"'{uid}'" for uid, _, __ in PROMPTS)
    op.execute(f"DELETE FROM essay_prompt WHERE id IN ({ids})")
