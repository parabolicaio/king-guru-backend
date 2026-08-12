"""Seed achievements + reconcile level display metadata.

Two things that were previously applied to production by hand (direct SQL) and
so were NOT reproducible on a fresh DB. This migration makes them part of the
chain so `alembic upgrade head` yields a database identical to production:

  1. Achievements — the six starter achievements the rewards system unlocks
     against. No prior migration ever inserted rows into `achievement`; they
     existed only in the live DB. Inserted here with their production UUIDs and
     `ON CONFLICT (id) DO NOTHING`, so re-running on production is a no-op.

  2. Level metadata — 0004_level_display_data seeded placeholder copy (identical
     Sinhala for every level, generic topics, duplicated descriptions). Those
     were later refined by hand to distinct per-level copy + topics. This
     migration UPDATEs the six levels to that refined, production-correct state.

Idempotent: achievements use ON CONFLICT; level updates are keyed by `code` and
set absolute values, so applying twice is harmless.

Revision ID: 4e1f2a3b4c5d
Revises:     3d0e1f2a3b4c
Create Date: 2026-07-05
"""
import json
from typing import Sequence, Union

from alembic import op

revision: str = "4e1f2a3b4c5d"
down_revision: Union[str, None] = "3d0e1f2a3b4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


# ── Achievements (production UUIDs; keep stable so IDs match live) ───────────────
_ACHIEVEMENTS = [
    {
        "id": "5c63bb61-ad5e-40b1-a3f6-596703c3a08c",
        "name": "First Steps",
        "description": "Complete your first lesson",
        "condition_type": "lesson_count",
        "condition_value": 1,
        "xp_reward": 20,
        "translations": {"si": {"name": "පළමු පියවර", "description": "ඔබේ පළමු පාඩම සම්පූර්ණ කරන්න"}},
    },
    {
        "id": "b4721c36-4e35-4ce5-9932-3516cf5291b4",
        "name": "First Essay",
        "description": "Submit your first daily essay",
        "condition_type": "essay_count",
        "condition_value": 1,
        "xp_reward": 25,
        "translations": {"si": {"name": "පළමු රචනාව", "description": "ඔබේ පළමු රචනාව ඉදිරිපත් කරන්න"}},
    },
    {
        "id": "acab4cad-d4ec-4a16-b59f-ca60d08c2634",
        "name": "On Fire",
        "description": "Reach a 3-day streak",
        "condition_type": "streak_days",
        "condition_value": 3,
        "xp_reward": 30,
        "translations": {"si": {"name": "ගිනි ගන්නවා", "description": "දින 3ක අඛණ්ඩතාවයක්"}},
    },
    {
        "id": "0046d717-ab01-4d58-8652-6bc86223a5fc",
        "name": "Getting the Hang of It",
        "description": "Complete 5 lessons",
        "condition_type": "lesson_count",
        "condition_value": 5,
        "xp_reward": 50,
        "translations": {"si": {"name": "පුරුදු වෙනවා", "description": "පාඩම් 5ක් සම්පූර්ණ කරන්න"}},
    },
    {
        "id": "beb4963c-5263-4f8d-8798-af0342a5263c",
        "name": "Word Collector",
        "description": "Master 10 vocabulary words",
        "condition_type": "words_mastered",
        "condition_value": 10,
        "xp_reward": 40,
        "translations": {"si": {"name": "වචන එකතුකරන්නා", "description": "වචන 10ක් ප්‍රගුණ කරන්න"}},
    },
    {
        "id": "d8fd28d4-1cf7-4945-8370-f2fdb95c6229",
        "name": "Century",
        "description": "Earn 100 XP",
        "condition_type": "xp_total",
        "condition_value": 100,
        "xp_reward": 25,
        "translations": {"si": {"name": "ශතකය", "description": "XP 100ක් උපයන්න"}},
    },
]


# ── Level metadata (production-correct, distinct per level) ──────────────────────
_LEVELS = [
    {
        "code": "beginner_a",
        "description": "Start from scratch — A1 basics across 10 lessons",
        "translations": {"si": "මුල සිට පටන් ගන්න — A1 මූලික පාඩම් 10ක්"},
        "topics": ["Greetings", "Family", "Numbers & Time", "Everyday Objects", "Food", "Home", "Health"],
    },
    {
        "code": "beginner_b",
        "description": "Build on the basics — A2 everyday English, 10 lessons",
        "translations": {"si": "මූලික දැනුම දියුණු කරන්න — A2 එදිනෙදා ඉංග්‍රීසි, පාඩම් 10ක්"},
        "topics": ["Daily Routines", "Directions", "Past Tense", "Shopping", "Weather", "Travel", "Work & Tech"],
    },
    {
        "code": "elementary",
        "description": "Everyday conversations and practical English",
        "translations": {"si": "එදිනෙදා සංවාද සහ ප්‍රායෝගික ඉංග්‍රීසි"},
        "topics": ["Conversations", "Opinions", "Making Plans", "Descriptions", "Requests"],
    },
    {
        "code": "intermediate",
        "description": "Professional communication and job interviews",
        "translations": {"si": "වෘත්තීය සන්නිවේදනය සහ රැකියා සම්මුඛ පරීක්ෂණ"},
        "topics": ["Workplace English", "Job Interviews", "Meetings", "Emails", "Phone Calls"],
    },
    {
        "code": "upper_intermediate",
        "description": "Presentations and confident public speaking",
        "translations": {"si": "ඉදිරිපත් කිරීම් සහ විශ්වාසයෙන් ප්‍රසිද්ධ කථනය"},
        "topics": ["Presentations", "Public Speaking", "Discussions", "Reports", "Persuasion"],
    },
    {
        "code": "advanced",
        "description": "Executive communication and strategic leadership",
        "translations": {"si": "විධායක සන්නිවේදනය සහ උපායමාර්ගික නායකත්වය"},
        "topics": ["Leadership", "Negotiation", "Strategy", "Advanced Writing", "Diplomacy"],
    },
]

# 0004_level_display_data values — used to revert level metadata on downgrade.
_LEVELS_PRIOR_DESC = {
    "beginner_a": "Complete A1 course with 10 structured lessons",
    "beginner_b": "Complete A1 course with 10 structured lessons",
    "elementary": "Complete A1 course with 10 structured lessons",
    "intermediate": "Professional communication and job interviews",
    "upper_intermediate": "Presentation and public speaking",
    "advanced": "Executive communication and strategic leadership",
}
_LEVELS_PRIOR_TOPICS = ["Greetings", "Family", "Time", "Objects", "Food", "Home", "Health"]
_LEVELS_PRIOR_SI = {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"}


def upgrade() -> None:
    # 1. Achievements — insert with stable production UUIDs, skip if present.
    for a in _ACHIEVEMENTS:
        op.execute(f"""
            INSERT INTO achievement
                (id, name, description, condition_type, condition_value,
                 xp_reward, is_active, translations, created_at, updated_at)
            VALUES
                ({_s(a['id'])}, {_s(a['name'])}, {_s(a['description'])},
                 {_s(a['condition_type'])}, {a['condition_value']},
                 {a['xp_reward']}, TRUE, {_j(a['translations'])}, now(), now())
            ON CONFLICT (id) DO NOTHING
        """)

    # 2. Level metadata — refine to distinct per-level copy + topics.
    for lvl in _LEVELS:
        op.execute(f"""
            UPDATE level
            SET
                description  = {_s(lvl['description'])},
                translations = {_j(lvl['translations'])},
                topics       = {_j(lvl['topics'])},
                updated_at   = now()
            WHERE code = {_s(lvl['code'])}
        """)


def downgrade() -> None:
    # Revert level metadata to the 0004_level_display_data values.
    for lvl in _LEVELS:
        code = lvl["code"]
        op.execute(f"""
            UPDATE level
            SET
                description  = {_s(_LEVELS_PRIOR_DESC[code])},
                translations = {_j(_LEVELS_PRIOR_SI)},
                topics       = {_j(_LEVELS_PRIOR_TOPICS)},
                updated_at   = now()
            WHERE code = {_s(code)}
        """)

    # Remove the seeded achievements.
    ids = ", ".join(_s(a["id"]) for a in _ACHIEVEMENTS)
    op.execute(f"DELETE FROM achievement WHERE id IN ({ids})")
