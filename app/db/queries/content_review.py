"""Raw SQL query functions for content review workflow."""

from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid


async def get_pending_review_for_content(
    db: asyncpg.Connection,
    content_type: str,
    content_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT id FROM content_review
        WHERE content_type = $1 AND content_id = $2::uuid AND decision = 'pending'
        """,
        content_type, content_id,
    )


async def create_content_review(
    db: asyncpg.Connection,
    *,
    content_type: str,
    content_id: str,
    submitted_by: str,
) -> asyncpg.Record:
    review_id = new_uuid()
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        INSERT INTO content_review (id, content_type, content_id, submitted_by, submitted_at,
                                    decision, created_at, updated_at)
        VALUES ($1, $2, $3::uuid, $4::uuid, $5, 'pending', $5, $5)
        RETURNING *
        """,
        review_id, content_type, content_id, submitted_by, now,
    )


async def get_review_by_id(
    db: asyncpg.Connection, review_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM content_review WHERE id = $1::uuid",
        review_id,
    )


async def decide_review(
    db: asyncpg.Connection,
    review_id: str,
    *,
    reviewer_id: str,
    decision: str,
    reason: str | None,
) -> asyncpg.Record:
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        UPDATE content_review
        SET decision    = $2,
            reason      = $3,
            reviewer_id = $4::uuid,
            reviewed_at = $5,
            updated_at  = $5
        WHERE id = $1::uuid
        RETURNING *
        """,
        review_id, decision, reason, reviewer_id, now,
    )


async def list_content_reviews(
    db: asyncpg.Connection,
    *,
    content_type: str | None = None,
    decision: str | None = None,
    submitted_by: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[asyncpg.Record], int]:
    conditions: list[str] = []
    params: list = []
    idx = 1

    if content_type:
        conditions.append(f"content_type = ${idx}")
        params.append(content_type)
        idx += 1
    if decision:
        conditions.append(f"decision = ${idx}")
        params.append(decision)
        idx += 1
    if submitted_by:
        conditions.append(f"submitted_by = ${idx}::uuid")
        params.append(submitted_by)
        idx += 1

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    offset = (page - 1) * page_size

    rows = await db.fetch(
        f"SELECT * FROM content_review {where} ORDER BY submitted_at DESC LIMIT ${idx} OFFSET ${idx + 1}",
        *params, page_size, offset,
    )
    count_row = await db.fetchrow(
        f"SELECT COUNT(*) AS total FROM content_review {where}",
        *params,
    )
    return list(rows), int(count_row["total"])
