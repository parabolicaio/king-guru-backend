"""Level restructure: collapse 6 levels to 5 (Task #25 Phase 1).

Domain experts fixed the model at 5 levels — Beginner, Elementary, Intermediate,
Upper Intermediate, Advanced. Our DB carries an extra split (Beginner A +
Beginner B) plus a redundant empty 'elementary' row. This migration is a RELABEL,
not a merge: it preserves every surviving level's UUID, so all user progress
(user.current_level_id), XP, certificates, daily-goal assignments, lessons, and
essay prompts stay attached untouched.

Mapping:
  beginner_a  -> beginner   "Beginner"    (order 1, unchanged)
  beginner_b  -> elementary "Elementary"  (order 2, unchanged; its 10 lessons are CEFR A2)
  elementary  -> DELETED (redundant empty row: 0 lessons, 0 users, 0 certs)
  intermediate / upper_intermediate / advanced -> renumbered to 3 / 4 / 5

Everything is keyed by the stable `code` values (consistent across every DB),
never by UUID — UUIDs regenerate per-DB (Task #17 lesson). Statement order is
load-bearing because level.code, level.name and level.display_order are all
UNIQUE: the old 'elementary' row must be deleted before beginner_b can take that
code/name, and renumbering happens after the order-3 slot is freed.

Placement scoring bands collapse 6 -> 5 (Nisal-confirmed 2026-07-21):
  0-30 beginner, 31-50 elementary, 51-70 intermediate, 71-88 upper_int, 89-100 advanced.
Only beginner/elementary are reachable until Level 3 content ships (recommended
level is capped to populated levels), so the upper three bands are inert for now.

Verified against live DB (project aptimrrjvjucszmpsvsg, 2026-07-21) before authoring:
the old 'elementary' row had 8 orphan daily_goal templates (0 assignments reference
them) + 1 scoring rule; those are cleared here so the row is deletable. 15 users sit
on beginner_a (0 on any other), 0 certificates issued.

Revision ID: b1a2c3d4e5f6
Revises:     8d9e6f1a2b3c
Create Date: 2026-07-21
"""
from typing import Sequence, Union

from alembic import op

revision: str = "b1a2c3d4e5f6"
down_revision: Union[str, None] = "8d9e6f1a2b3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# All SQL is plain (no per-row Python), so a dry-run harness can import and run
# these same strings inside a rolled-back transaction with zero drift.
_UPGRADE_SQL: list[str] = [
    # 1. Clear the old empty 'elementary' row's dependents so it can be deleted.
    #    8 orphan daily_goal templates (daily_goal_assignment references = 0) ...
    "DELETE FROM daily_goal WHERE level_id = (SELECT id FROM level WHERE code = 'elementary')",
    #    ... and its single scoring rule (the 51-65 band, removed in the re-span below).
    "DELETE FROM placement_scoring_rule WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'elementary')",
    # 2. Delete the redundant empty 'elementary' level row (0 lessons/users/certs).
    "DELETE FROM level WHERE code = 'elementary'",
    # 3. Relabel. beginner_b must take code/name 'elementary'/'Elementary' only AFTER
    #    the old row above is gone (UNIQUE code + name). UUIDs are preserved.
    "UPDATE level SET code = 'beginner', name = 'Beginner' WHERE code = 'beginner_a'",
    "UPDATE level SET code = 'elementary', name = 'Elementary' WHERE code = 'beginner_b'",
    # 4. Renumber to close the gap. display_order is UNIQUE; order 3 is now free
    #    (deleted row), then each move frees the next slot in turn.
    "UPDATE level SET display_order = 3 WHERE code = 'intermediate'",
    "UPDATE level SET display_order = 4 WHERE code = 'upper_intermediate'",
    "UPDATE level SET display_order = 5 WHERE code = 'advanced'",
    # 5. Re-span placement scoring bands onto the 5 surviving levels (keyed by the
    #    post-rename codes, so these rows are the same UUIDs, just re-bounded).
    "UPDATE placement_scoring_rule SET min_percent = 0,  max_percent = 30,  updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'beginner')",
    "UPDATE placement_scoring_rule SET min_percent = 31, max_percent = 50,  updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'elementary')",
    "UPDATE placement_scoring_rule SET min_percent = 51, max_percent = 70,  updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'intermediate')",
    "UPDATE placement_scoring_rule SET min_percent = 71, max_percent = 88,  updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'upper_intermediate')",
    "UPDATE placement_scoring_rule SET min_percent = 89, max_percent = 100, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'advanced')",
    # 6. Remap the 17 placement_question difficulty tags to the 5-code taxonomy.
    #    ORDER MATTERS: drop the old CHECK first — the new value 'beginner' is NOT in
    #    the old allow-list, so remapping before the drop would violate it.
    "ALTER TABLE placement_question DROP CONSTRAINT placement_question_difficulty_check",
    "UPDATE placement_question SET difficulty = 'beginner'   WHERE difficulty = 'beginner_a'",
    "UPDATE placement_question SET difficulty = 'elementary' WHERE difficulty = 'beginner_b'",
    "ALTER TABLE placement_question ADD CONSTRAINT placement_question_difficulty_check "
    "CHECK (difficulty = ANY (ARRAY['beginner', 'elementary', 'intermediate', 'upper_intermediate', 'advanced']))",
]


# Downgrade restores the 6-level shape functionally. The old empty 'elementary'
# row is recreated with a fresh UUID (nothing user-owned referenced it) and its
# scoring rule re-added; the 8 orphan daily_goal templates are NOT recreated (they
# were seeded by a data migration, not this one, and are re-seedable).
_DOWNGRADE_SQL: list[str] = [
    # 6'. difficulty CHECK + tags back to the 6-code taxonomy. The upgrade merged
    #     beginner_b INTO elementary (lossy — the two are indistinguishable after),
    #     so only the beginner<-beginner_a rename is separable; merged rows stay
    #     tagged 'elementary' (still valid under the restored 6-code CHECK).
    "ALTER TABLE placement_question DROP CONSTRAINT placement_question_difficulty_check",
    "UPDATE placement_question SET difficulty = 'beginner_a' WHERE difficulty = 'beginner'",
    "ALTER TABLE placement_question ADD CONSTRAINT placement_question_difficulty_check "
    "CHECK (difficulty = ANY (ARRAY['beginner_a', 'beginner_b', 'elementary', 'intermediate', 'upper_intermediate', 'advanced']))",
    # 4'. Renumber back: advanced 5->6, upper 4->5, intermediate 3->4 (each frees the next).
    "UPDATE level SET display_order = 6 WHERE code = 'advanced'",
    "UPDATE level SET display_order = 5 WHERE code = 'upper_intermediate'",
    "UPDATE level SET display_order = 4 WHERE code = 'intermediate'",
    # 3'. Relabel elementary(ex-beginner_b) -> beginner_b, beginner -> beginner_a.
    "UPDATE level SET code = 'beginner_b', name = 'Beginner B' WHERE code = 'elementary'",
    "UPDATE level SET code = 'beginner_a', name = 'Beginner A' WHERE code = 'beginner'",
    # 2'. Recreate the empty 'elementary' level row at order 3 (fresh UUID).
    "INSERT INTO level (id, code, name, display_order, created_at, updated_at) "
    "VALUES (gen_random_uuid(), 'elementary', 'Elementary', 3, now(), now())",
    # 5'. Restore the 6-band scoring curve.
    "UPDATE placement_scoring_rule SET min_percent = 0,  max_percent = 30, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'beginner_a')",
    "UPDATE placement_scoring_rule SET min_percent = 31, max_percent = 50, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'beginner_b')",
    "INSERT INTO placement_scoring_rule (id, min_percent, max_percent, recommended_level_id, created_at, updated_at) "
    "VALUES (gen_random_uuid(), 51, 65, (SELECT id FROM level WHERE code = 'elementary'), now(), now())",
    "UPDATE placement_scoring_rule SET min_percent = 66, max_percent = 80, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'intermediate')",
    "UPDATE placement_scoring_rule SET min_percent = 81, max_percent = 92, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'upper_intermediate')",
    "UPDATE placement_scoring_rule SET min_percent = 93, max_percent = 100, updated_at = now() WHERE recommended_level_id = (SELECT id FROM level WHERE code = 'advanced')",
]


def upgrade() -> None:
    for stmt in _UPGRADE_SQL:
        op.execute(stmt)


def downgrade() -> None:
    for stmt in _DOWNGRADE_SQL:
        op.execute(stmt)
