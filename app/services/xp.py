"""XP service — rule lookup cache, ledger writes, user total updates."""

import logging
from datetime import datetime, timezone
from uuid import UUID

import asyncpg

from app.db.queries.xp import get_xp_rules, insert_xp_ledger, increment_user_xp
from app.db.utils import new_uuid

logger = logging.getLogger(__name__)

_xp_rule_cache: dict[tuple[str, str | None], int] = {}
_cache_loaded_at: datetime | None = None
CACHE_TTL_SECONDS = 300


async def load_cache(db: asyncpg.Connection) -> None:
    """Populate the XP rule cache from the database."""
    global _xp_rule_cache, _cache_loaded_at
    rows = await get_xp_rules(db)
    _xp_rule_cache = {(r["action_type"], r["context_key"]): r["xp_value"] for r in rows}
    _cache_loaded_at = datetime.now(timezone.utc)


def _is_cache_stale() -> bool:
    if _cache_loaded_at is None:
        return True
    age = (datetime.now(timezone.utc) - _cache_loaded_at).total_seconds()
    return age > CACHE_TTL_SECONDS


async def _ensure_cache(db: asyncpg.Connection) -> None:
    if _is_cache_stale():
        await load_cache(db)


async def lookup(db: asyncpg.Connection, action_type: str, context_key: str | None = None) -> int:
    """Return XP for an action. Never raises — returns 0 on cache miss."""
    await _ensure_cache(db)
    value = _xp_rule_cache.get((action_type, context_key))
    if value is not None:
        return value
    if context_key is not None:
        value = _xp_rule_cache.get((action_type, None))
    if value is None:
        logger.warning("XP_RULE_MISSING action_type=%s context_key=%s", action_type, context_key)
        return 0
    return value


async def award(
    db: asyncpg.Connection,
    user_id: str,
    action_type: str,
    xp_delta: int,
    reference_id: str | None = None,
    reference_type: str | None = None,
) -> None:
    """Insert xp_ledger row and increment user.xp_total. Must be called inside a transaction."""
    if xp_delta <= 0:
        return
    await insert_xp_ledger(
        db,
        ledger_id=str(new_uuid()),
        user_id=user_id,
        action_type=action_type,
        xp_delta=xp_delta,
        reference_id=reference_id,
        reference_type=reference_type,
    )
    await increment_user_xp(db, user_id, xp_delta)

    # Track toward the xp_earned daily goal (skip for goal-complete XP itself)
    if action_type != "daily_goal_complete":
        from app.services import daily_goal_service
        await daily_goal_service.record_activity(
            db, user_id, "xp_earned", increment=xp_delta
        )


async def award_for_question(
    db: asyncpg.Connection,
    user_id: str,
    attempt_id: str,
    question_xp_value: int,
    score_numerator: int,
    score_denominator: int,
) -> int:
    """Award XP for a question attempt. Returns XP awarded (may be 0).

    Must be called inside the same transaction as the attempt INSERT.
    """
    xp_awarded = question_xp_value if score_numerator == score_denominator else 0
    if xp_awarded > 0:
        await award(
            db,
            user_id=user_id,
            action_type="question_attempt",
            xp_delta=xp_awarded,
            reference_id=attempt_id,
            reference_type="attempt",
        )
    return xp_awarded
