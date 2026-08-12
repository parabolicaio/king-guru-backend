"""Add display fields to level table.

- level.translations: JSONB for name/description in si/singlish
- level.icon_url:     storage path or emoji for the level card icon
- level.topics:       JSONB array of topic strings shown on the level card

The 'translations' column was already referenced in queries but missing from
the CREATE TABLE — this migration adds it retroactively.

Revision ID: b2c3d4e5f6a7
Revises:     a1b2c3d4e5f6
Create Date: 2026-06-07
"""
from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: str | None = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE level
            ADD COLUMN IF NOT EXISTS translations JSONB NOT NULL DEFAULT '{}',
            ADD COLUMN IF NOT EXISTS icon_url     TEXT,
            ADD COLUMN IF NOT EXISTS topics       JSONB NOT NULL DEFAULT '[]'
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE level DROP COLUMN IF EXISTS topics")
    op.execute("ALTER TABLE level DROP COLUMN IF EXISTS icon_url")
    op.execute("ALTER TABLE level DROP COLUMN IF EXISTS translations")
