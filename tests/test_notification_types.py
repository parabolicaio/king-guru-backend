"""Regression guard for the notification.type CHECK-constraint gap.

Twice now (0044 placement_complete; 0047 essay_graded + streak_milestone) a
service has emitted a notification type that the DB CHECK constraint didn't
allow, producing an unhandled CheckViolationError → 500 that rolled back the
surrounding write. This is a pure static test (no DB) that catches the NEXT
occurrence at test time instead of in production: every `notif_type="..."`
literal in app/services/ must be in the allowed set below.

When you add a new notification type:
  1. Add the literal at the emitting call site, AND
  2. Add it to _ALLOWED here, AND
  3. Ship an Alembic migration widening `notification_type_check`
     (mirror 0047_notification_type_essay_streak.py).
Keep all three in sync — this test fails loudly if the code drifts ahead of
the migration.
"""

import re
from pathlib import Path

# The values permitted by `notification_type_check` after migration
# 0047_notification_type_essay_streak.py. MUST stay in lockstep with that
# migration's CHECK list.
_ALLOWED = {
    "achievement_unlocked",
    "streak_at_risk",
    "lesson_unlocked",
    "lesson_complete",
    "announcement",
    "content_review_decision",
    "placement_complete",
    "essay_graded",
    "streak_milestone",
}

_SERVICES_DIR = Path(__file__).resolve().parent.parent / "app" / "services"
_NOTIF_TYPE_RE = re.compile(r"""notif_type\s*=\s*["']([^"']+)["']""")


def _emitted_notification_types() -> dict[str, str]:
    """Map each emitted notif_type literal -> a 'file:line' where it occurs."""
    found: dict[str, str] = {}
    for path in _SERVICES_DIR.glob("*.py"):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            m = _NOTIF_TYPE_RE.search(line)
            if m:
                found.setdefault(m.group(1), f"{path.name}:{i}")
    return found


def test_every_emitted_notification_type_is_allowed_by_the_check():
    emitted = _emitted_notification_types()
    # Sanity: the scan actually found the known call sites (guards against a
    # refactor that renames the kwarg making this test silently vacuous).
    assert "essay_graded" in emitted, "scan found no notif_type literals — check the regex"

    offenders = {t: loc for t, loc in emitted.items() if t not in _ALLOWED}
    assert not offenders, (
        "These notification types are emitted by a service but are NOT in the "
        "notification.type CHECK constraint (they will 500 at runtime). Add them "
        "to _ALLOWED here AND ship a migration widening notification_type_check:\n"
        + "\n".join(f"  - {t!r} at {loc}" for t, loc in sorted(offenders.items()))
    )
