"""Seed level display data — descriptions, Sinhala translations, topics, icon paths.

Updates the six level rows created in 0002_seed_data with the display fields
added in 0003_level_display_fields (translations, icon_url, topics).

icon_url stores the Supabase Storage path relative to the configured bucket.
At runtime the backend builds the full CDN URL from STORAGE_BASE_URL + icon_url.

Revision ID: d4e5f6a7b8c9
Revises:     b2c3d4e5f6a7
Create Date: 2026-06-07
"""
import json
from typing import Sequence, Union

from alembic import op

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_TOPICS = ["Greetings", "Family", "Time", "Objects", "Food", "Home", "Health"]

_LEVELS = [
    {
        "code": "beginner_a",
        "description": "Complete A1 course with 10 structured lessons",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/beginner-a-icon.png",
    },
    {
        "code": "beginner_b",
        "description": "Complete A1 course with 10 structured lessons",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/beginner-b-icon.png",
    },
    {
        "code": "elementary",
        "description": "Complete A1 course with 10 structured lessons",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/elementary-icon.png",
    },
    {
        "code": "intermediate",
        "description": "Professional communication and job interviews",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/intermediate-icon.png",
    },
    {
        "code": "upper_intermediate",
        "description": "Presentation and public speaking",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/upper-intermediate-icon.png",
    },
    {
        "code": "advanced",
        "description": "Executive communication and strategic leadership",
        "translations": {"si": "සම්පූර්ණ A1 පාඨමාලාව - පාඩම් 10ක්"},
        "topics": _TOPICS,
        "icon_url": "level-icons/advanced-icon.png",
    },
]


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def upgrade() -> None:
    for lvl in _LEVELS:
        op.execute(f"""
            UPDATE level
            SET
                description  = {_s(lvl['description'])},
                translations = {_j(lvl['translations'])},
                topics       = {_j(lvl['topics'])},
                icon_url     = {_s(lvl['icon_url'])},
                updated_at   = now()
            WHERE code = {_s(lvl['code'])}
        """)


def downgrade() -> None:
    for lvl in _LEVELS:
        op.execute(f"""
            UPDATE level
            SET
                translations = '{{}}',
                topics       = '[]',
                icon_url     = NULL,
                updated_at   = now()
            WHERE code = {_s(lvl['code'])}
        """)
