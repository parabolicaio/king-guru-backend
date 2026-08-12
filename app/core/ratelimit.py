"""Lightweight in-process rate limiting.

The backend runs as a single Render instance, so an in-memory sliding-window
counter is sufficient (no Redis / external dep). If the app is ever scaled to
multiple instances, swap the `_hits` store for a shared one (Redis) — the public
`rate_limit` dependency API can stay the same.

Usage (as a route dependency — no signature change needed):

    @router.post("/x", dependencies=[Depends(rate_limit(60, 60, "x"))])

Keys per caller: authenticated token (hashed) > guest token > client IP taken
from X-Forwarded-For (Render sets it) so limiting is per-caller, not per-proxy.
On limit it raises AppError → the standard KG error envelope with a 429.
"""

import hashlib
import time
from collections import defaultdict, deque
from collections.abc import Callable, Coroutine

from fastapi import Request

from app.core.errors import AppError

# key -> monotonic timestamps of recent hits
_hits: dict[str, deque[float]] = defaultdict(deque)

RATE_LIMITED = ("RATE_LIMITED", "Too many requests. Please slow down.", 429)

_MAX_TRACKED_KEYS = 10_000  # opportunistic prune threshold


def _caller_key(request: Request) -> str:
    """Stable per-caller identity: auth token (hashed) > guest token > IP."""
    auth = request.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        # Hash so raw tokens are never used as (loggable) dict keys.
        return "u:" + hashlib.sha256(auth.encode()).hexdigest()[:24]
    guest = request.headers.get("x-guest-token")
    if guest:
        return "g:" + guest
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return "ip:" + xff.split(",")[0].strip()
    return "ip:" + (request.client.host if request.client else "unknown")


def _prune(now: float) -> None:
    stale = [k for k, dq in _hits.items() if not dq or dq[-1] < now - 3600]
    for k in stale:
        _hits.pop(k, None)


def rate_limit(
    max_hits: int, window_seconds: int, scope: str
) -> Callable[[Request], Coroutine[None, None, None]]:
    """Build a FastAPI dependency allowing `max_hits` per `window_seconds` per caller.

    `scope` namespaces the counter so different endpoints don't share a budget.
    """

    async def _dependency(request: Request) -> None:
        now = time.monotonic()
        key = f"{scope}:{_caller_key(request)}"
        dq = _hits[key]
        cutoff = now - window_seconds
        while dq and dq[0] < cutoff:
            dq.popleft()
        if len(dq) >= max_hits:
            raise AppError(*RATE_LIMITED, details={"retry_after_seconds": window_seconds})
        dq.append(now)
        if len(_hits) > _MAX_TRACKED_KEYS:
            _prune(now)

    return _dependency
