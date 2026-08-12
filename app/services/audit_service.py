"""Audit log service.

Writes rows to the audit_log table for significant admin/system actions.
All calls are fire-and-forget — DB errors are swallowed so the audit log
never causes a main request to fail.
"""

import logging
from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid

logger = logging.getLogger(__name__)

# ── Action type constants ────────────────────────────────────────────────────
USER_CREATED      = "user.created"
USER_DELETED      = "user.deleted"
USER_ROLE_CHANGED = "user.role_changed"


async def log(
    conn: asyncpg.Connection,
    *,
    action: str,
    actor_id: str | None,
    target_type: str,
    target_id: str,
    before_state: dict | None = None,
    after_state: dict | None = None,
) -> None:
    """Insert an audit_log row.  Swallows all exceptions.

    actor_id     — UUID of the user who performed the action (None for system)
    target_type  — entity type string, e.g. "user", "lesson", "content_review"
    target_id    — UUID of the affected entity
    before_state — optional JSONB snapshot before the change (keep small; no PII)
    after_state  — optional JSONB snapshot after the change
    """
    import json

    try:
        now = datetime.now(timezone.utc)
        await conn.execute(
            """
            INSERT INTO audit_log (
                id, actor_id, action, target_type, target_id,
                before_state, after_state, created_at
            ) VALUES (
                $1::uuid, $2::uuid, $3, $4, $5::uuid,
                $6::jsonb, $7::jsonb, $8
            )
            """,
            new_uuid(),
            actor_id,
            action,
            target_type,
            target_id,
            json.dumps(before_state) if before_state is not None else None,
            json.dumps(after_state) if after_state is not None else None,
            now,
        )
    except Exception:
        logger.exception("audit_service.log failed: action=%s actor=%s", action, actor_id)
