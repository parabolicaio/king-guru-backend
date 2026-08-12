"""Raw SQL query functions for admin user management (B8)."""

from datetime import datetime, timezone

import asyncpg


async def list_users(
    db: asyncpg.Connection,
    *,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    auth_provider: str | None = None,
    subscription_tier: str | None = None,
    admin_role: str | None = None,
    level_code: str | None = None,
    active_only: bool = True,
) -> tuple[list[asyncpg.Record], int]:
    conditions: list[str] = ["u.is_guest = FALSE"]
    params: list = []
    idx = 1

    if active_only:
        conditions.append("u.deleted_at IS NULL")

    if search:
        conditions.append(
            f"(u.full_name ILIKE ${idx} OR u.email ILIKE ${idx} OR u.phone ILIKE ${idx})"
        )
        params.append(f"%{search}%")
        idx += 1

    if auth_provider:
        conditions.append(f"u.auth_provider = ${idx}")
        params.append(auth_provider)
        idx += 1

    if subscription_tier:
        conditions.append(f"u.subscription_tier = ${idx}")
        params.append(subscription_tier)
        idx += 1

    if admin_role is not None:
        if admin_role == "learner":
            conditions.append("u.admin_role IS NULL")
        else:
            conditions.append(f"u.admin_role = ${idx}")
            params.append(admin_role)
            idx += 1

    if level_code:
        conditions.append(f"lv.code = ${idx}")
        params.append(level_code)
        idx += 1

    where = "WHERE " + " AND ".join(conditions)
    offset = (page - 1) * page_size

    level_join = "LEFT JOIN level lv ON lv.id = u.current_level_id" if level_code else ""

    rows = await db.fetch(
        f"""
        SELECT u.*
        FROM "user" u
        {level_join}
        {where}
        ORDER BY u.created_at DESC
        LIMIT ${idx} OFFSET ${idx + 1}
        """,
        *params, page_size, offset,
    )
    count_row = await db.fetchrow(
        f'SELECT COUNT(*) AS total FROM "user" u {level_join} {where}',
        *params,
    )
    return list(rows), int(count_row["total"])


async def get_user_with_progress(
    db: asyncpg.Connection, user_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT u.*,
               COALESCE(lc.completed_lesson_count, 0) AS completed_lesson_count
        FROM "user" u
        LEFT JOIN (
            SELECT user_id, COUNT(*) AS completed_lesson_count
            FROM lesson_progress
            WHERE status = 'completed'
            GROUP BY user_id
        ) lc ON lc.user_id = u.id
        WHERE u.id = $1::uuid
        """,
        user_id,
    )


async def get_recent_xp_ledger(
    db: asyncpg.Connection, user_id: str, limit: int = 10
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT action_type, xp_delta, reference_type, reference_id, awarded_at
        FROM xp_ledger
        WHERE user_id = $1::uuid
        ORDER BY awarded_at DESC
        LIMIT $2
        """,
        user_id, limit,
    )


async def update_user_role(
    db: asyncpg.Connection, user_id: str, admin_role: str | None
) -> asyncpg.Record:
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        UPDATE "user"
        SET admin_role = $2,
            updated_at = $3
        WHERE id = $1::uuid
        RETURNING id, admin_role, updated_at
        """,
        user_id, admin_role, now,
    )
