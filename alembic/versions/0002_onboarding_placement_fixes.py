"""Onboarding and placement schema fixes.

- user.age_group:       replace 3-value CHECK with 5 specific age ranges
- user.english_level:   new column (None / Little / Conversational / Good)
- user.role_tag:        add CHECK constraint; make nullable (collected at onboarding)
- placement_question.prompt_text:    add missing column (was queried but not in schema)
- placement_question.skill_category: new column for skill-breakdown on results screen
- placement_question.xp_value:       new column so assessments award XP

Revision ID: a1b2c3d4e5f6
Revises:     f2b3c4d5e6a7
Create Date: 2026-06-07
"""
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: str | None = "f2b3c4d5e6a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── user.age_group ────────────────────────────────────────────────────────
    # PostgreSQL names the inline check as user_age_group_check.
    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_age_group_check')
    op.execute("""
        ALTER TABLE "user" ADD CONSTRAINT user_age_group_check
            CHECK (age_group IS NULL OR age_group IN (
                'under_15', '15_18', '19_25', '26_40', '40_plus'
            ))
    """)

    # ── user.english_level ────────────────────────────────────────────────────
    op.execute("""
        ALTER TABLE "user" ADD COLUMN english_level TEXT
            CHECK (english_level IS NULL OR english_level IN (
                'none', 'little', 'conversational', 'good'
            ))
    """)

    # ── user.role_tag ─────────────────────────────────────────────────────────
    # Normalise existing empty-string rows to NULL before adding constraint.
    op.execute("UPDATE \"user\" SET role_tag = NULL WHERE role_tag = ''")
    op.execute('ALTER TABLE "user" ALTER COLUMN role_tag DROP NOT NULL')
    op.execute('ALTER TABLE "user" ALTER COLUMN role_tag DROP DEFAULT')
    op.execute("""
        ALTER TABLE "user" ADD CONSTRAINT user_role_tag_check
            CHECK (role_tag IS NULL OR role_tag IN (
                'school_student', 'university_student', 'working_adult', 'other'
            ))
    """)

    # ── placement_question.prompt_text ────────────────────────────────────────
    # Column was referenced in SELECT queries but missing from the CREATE TABLE.
    op.execute("ALTER TABLE placement_question ADD COLUMN IF NOT EXISTS prompt_text TEXT")

    # ── placement_question.skill_category ─────────────────────────────────────
    # Mirrors lesson_section.category values for consistent skill taxonomy.
    op.execute("""
        ALTER TABLE placement_question ADD COLUMN skill_category TEXT
            CHECK (skill_category IS NULL OR skill_category IN (
                'vocabulary', 'grammar', 'pronunciation',
                'reading', 'listening', 'writing', 'speaking'
            ))
    """)

    # ── placement_question.xp_value ───────────────────────────────────────────
    op.execute("""
        ALTER TABLE placement_question
            ADD COLUMN xp_value INTEGER NOT NULL DEFAULT 5
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE placement_question DROP COLUMN IF EXISTS xp_value")
    op.execute("ALTER TABLE placement_question DROP COLUMN IF EXISTS skill_category")
    op.execute("ALTER TABLE placement_question DROP COLUMN IF EXISTS prompt_text")

    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_role_tag_check')
    op.execute("ALTER TABLE \"user\" ALTER COLUMN role_tag SET DEFAULT ''")
    op.execute('ALTER TABLE "user" ALTER COLUMN role_tag SET NOT NULL')

    op.execute('ALTER TABLE "user" DROP COLUMN IF EXISTS english_level')

    op.execute('ALTER TABLE "user" DROP CONSTRAINT IF EXISTS user_age_group_check')
    op.execute("""
        ALTER TABLE "user" ADD CONSTRAINT user_age_group_check
            CHECK (age_group IN ('child', 'teen', 'adult'))
    """)
