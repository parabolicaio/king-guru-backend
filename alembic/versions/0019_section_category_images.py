"""Add section_category_image lookup table and seed 7 categories.

Revision ID: 0019
Revises: 0018
"""
from alembic import op

revision: str = "c3d4e5f6a7b8"
down_revision: str = "1b0a9f8e7d6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE section_category_image (
            category   TEXT        NOT NULL PRIMARY KEY
                                   CHECK (category IN (
                                       'vocabulary','grammar','pronunciation',
                                       'reading','listening','writing','speaking'
                                   )),
            image_url  TEXT        NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        INSERT INTO section_category_image (category, image_url) VALUES
            ('vocabulary',    'section-categories/vocabulary.png'),
            ('grammar',       'section-categories/grammar.png'),
            ('pronunciation', 'section-categories/pronunciation.png'),
            ('reading',       'section-categories/reading.png'),
            ('listening',     'section-categories/listening.png'),
            ('writing',       'section-categories/writing.png'),
            ('speaking',      'section-categories/speaking.png')
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS section_category_image")
