"""Enable row-level security on payment, saved_card, onepay_customer,
lesson_section_progress (D-64).

Every other table in this schema already has RLS enabled with zero
policies — confirmed live via pg_class.relrowsecurity and pg_policies
before writing this migration. That combination denies all access to any
non-owner Postgres role (the anon/authenticated roles PostgREST uses) by
default, while the backend's own DB connection (table owner) is unaffected
since it never goes through PostgREST — everything here is served by the
FastAPI backend, which does its own authorization in Python. These four
tables were the only ones missing that lockout: currently ungranted to
anon/authenticated too (also confirmed live via has_table_privilege), so
not an active PostgREST exposure today, but with no RLS-level safety net
if a future migration or Supabase CLI default ever grants broader access —
unlike every other table, which would still be protected by RLS even then.
This closes that gap the same way it's already closed everywhere else, for
the two tables holding payment data plus the two flagged alongside them.

Revision ID: 3b4c5d6e7f8a
Revises:     2a3b4c5d6e7f
Create Date: 2026-10-16
"""
from typing import Sequence, Union

from alembic import op

revision: str = "3b4c5d6e7f8a"
down_revision: Union[str, None] = "2a3b4c5d6e7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_TABLES = ("payment", "saved_card", "onepay_customer", "lesson_section_progress")


def upgrade() -> None:
    for table in _TABLES:
        op.execute(f'ALTER TABLE "{table}" ENABLE ROW LEVEL SECURITY')


def downgrade() -> None:
    for table in _TABLES:
        op.execute(f'ALTER TABLE "{table}" DISABLE ROW LEVEL SECURITY')
