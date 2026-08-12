"""Shuffle MCQ option order so the correct answer isn't always first.

User-test feedback (2026-07-10): testers noticed the first option is almost
always the right answer. Root cause is a content-generation artifact — the
correct option was authored as option 'a' in 13/13 placement MCQs and ~87%
of lesson mcq_single / mcq_long_short_form / fill_blank_options questions.

Fix at the data level so BOTH clients are covered without code changes:
shuffle each affected question's options array, then relabel option ids
sequentially ('a', 'b', 'c', ...) in the new display order and repoint
correct_option_id at the relocated correct option. Relabeling keeps
id == position, which matters because the Flutter client submits the
selected option's id positionally while the web client submits the option
object's own id — after this migration both remain correct.

Grading is unaffected: scoring.py / placement_service.py compare the
submitted id against payload->>'correct_option_id' at attempt time, and
already-graded attempts stored their is_correct verdict when made.

Safe to re-run (it just reshuffles). Skips questions whose stored
correct_option_id doesn't match any option id (none exist today) so a
malformed row can never lose its answer key.

Revision ID: 6b3c4d5e6f7a
Revises:     5a2b3c4d5e6f
Create Date: 2026-07-10
"""
from typing import Sequence, Union

from alembic import op

revision: str = "6b3c4d5e6f7a"
down_revision: Union[str, None] = "5a2b3c4d5e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_OPTION_TYPES = "('mcq_single', 'mcq_long_short_form', 'fill_blank_options')"


def _shuffle_sql(table: str) -> str:
    return f"""
        WITH opt AS (
            SELECT q.id AS qid,
                   q.payload->>'correct_option_id' AS correct_id,
                   elem AS option,
                   row_number() OVER (PARTITION BY q.id ORDER BY random()) AS rn
            FROM {table} q
            CROSS JOIN LATERAL jsonb_array_elements(q.payload->'options') AS elem
            WHERE q.type IN {_OPTION_TYPES}
              AND q.payload->>'correct_option_id' IS NOT NULL
              AND jsonb_typeof(q.payload->'options') = 'array'
              AND jsonb_array_length(q.payload->'options') > 1
        ),
        agg AS (
            SELECT qid,
                   jsonb_agg(
                       jsonb_set(option, '{{id}}', to_jsonb(chr(96 + rn::int)))
                       ORDER BY rn
                   ) AS new_options,
                   min(chr(96 + rn::int))
                       FILTER (WHERE option->>'id' = correct_id) AS new_correct
            FROM opt
            GROUP BY qid
        )
        UPDATE {table} q
        SET payload = jsonb_set(
                jsonb_set(q.payload, '{{options}}', a.new_options),
                '{{correct_option_id}}', to_jsonb(a.new_correct)
            ),
            updated_at = now()
        FROM agg a
        WHERE q.id = a.qid
          AND a.new_correct IS NOT NULL
    """


def upgrade() -> None:
    op.execute(_shuffle_sql("question"))
    op.execute(_shuffle_sql("placement_question"))


def downgrade() -> None:
    # Irreversible: the original option order is not preserved. The shuffled
    # state is equally valid content, so there is nothing to restore.
    pass
