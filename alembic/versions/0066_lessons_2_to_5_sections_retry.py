"""Re-run the Lesson 2-5 sections with the right level code (D-78).

0063 looked up Level 1 by its old code 'beginner_a', but 0045 renamed it
'beginner', so on the live database it found no lessons and added
nothing. 0063 now accepts both codes; this runs it again, then adds the
recorded Speaking tasks from 0065 to the new Speaking sections. Both
skip sections that already have content, so nothing is duplicated.

Revision ID: d66f0a1b2c3e
Revises:     c75e84f2b9d1
Create Date: 2026-11-04
"""
import importlib.util
from pathlib import Path
from typing import Sequence, Union

revision: str = "d66f0a1b2c3e"
down_revision: Union[str, None] = "c75e84f2b9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_HERE = Path(__file__).parent


def _load(filename: str):
    spec = importlib.util.spec_from_file_location(filename[:4] + "_mod", _HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def upgrade() -> None:
    _load("0063_lessons_2_to_5_skill_sections.py").upgrade()
    _load("0065_speaking_recorded_tasks.py").upgrade()


def downgrade() -> None:
    pass
