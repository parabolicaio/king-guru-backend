"""Change user.current_level_id FK from ON DELETE SET NULL to ON DELETE RESTRICT.

Previously a hard DELETE on a level row would silently NULL out current_level_id
for all enrolled users. RESTRICT prevents the deletion entirely when any user
references the level, which is the desired safety behaviour.

Revision ID: d4e5f6a7b8c0
Revises:     c3d4e5f6a7b9
Create Date: 2026-06-18
"""
from typing import Sequence, Union

from alembic import op

revision: str = 'd4e5f6a7b8c0'
down_revision: Union[str, None] = 'c3d4e5f6a7b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE "user"
            DROP CONSTRAINT IF EXISTS user_current_level_id_fkey;

        ALTER TABLE "user"
            ADD CONSTRAINT user_current_level_id_fkey
                FOREIGN KEY (current_level_id)
                REFERENCES level(id)
                ON DELETE RESTRICT;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE "user"
            DROP CONSTRAINT IF EXISTS user_current_level_id_fkey;

        ALTER TABLE "user"
            ADD CONSTRAINT user_current_level_id_fkey
                FOREIGN KEY (current_level_id)
                REFERENCES level(id)
                ON DELETE SET NULL;
    """)
