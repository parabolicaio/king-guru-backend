"""Add objectives columns to lesson table.

Revision ID: c3d4e5f6a7b9
Revises:     b2c3d4e5f6a8
Create Date: 2026-06-16
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'c3d4e5f6a7b9'
down_revision: Union[str, None] = 'b2c3d4e5f6a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE lesson
            ADD COLUMN IF NOT EXISTS objectives JSONB NOT NULL DEFAULT '[]',
            ADD COLUMN IF NOT EXISTS objectives_translations JSONB NOT NULL DEFAULT '{}'
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE lesson
            DROP COLUMN IF EXISTS objectives,
            DROP COLUMN IF EXISTS objectives_translations
    """)
