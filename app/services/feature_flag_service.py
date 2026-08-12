"""Feature flag service — public, cached global toggles.

Deliberately simple: one global on/off per flag_key (feature_flag.default_value).
Per-tier/per-user overrides exist in the schema for future subscription work
but are not read here — wire them in once subscription enforcement (backlog
item 14) actually ships. Until then this is "one toggle flips both apps".
"""

import time

import asyncpg

from app.db.queries.feature_flags import get_all_feature_flags

_CACHE_TTL_SECONDS = 60.0
_cache: dict[str, bool] | None = None
_cache_at: float = 0.0


async def get_flags(db: asyncpg.Connection) -> dict[str, bool]:
    global _cache, _cache_at

    now = time.monotonic()
    if _cache is not None and (now - _cache_at) < _CACHE_TTL_SECONDS:
        return _cache

    rows = await get_all_feature_flags(db)
    _cache = {row["flag_key"]: row["default_value"] for row in rows}
    _cache_at = now
    return _cache
