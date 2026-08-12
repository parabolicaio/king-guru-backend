from fastapi import APIRouter, Depends
from uuid import UUID

import asyncpg

from app.core.errors import AppError, NOTIFICATION_NOT_FOUND, NOTIFICATION_NOT_OWNED
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.notifications import (
    count_unread_notifications,
    get_notifications_for_user,
)
from app.schemas.notifications import (
    MarkAllReadResponse,
    MarkReadResponse,
    NotificationItem,
    NotificationsListResponse,
)
from app.services import notification as notification_service

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.get("", response_model=NotificationsListResponse)
async def list_notifications(
    cursor: str | None = None,
    limit: int = 20,
    unread_only: bool = False,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> NotificationsListResponse:
    rows = await get_notifications_for_user(
        db,
        user_id=str(user["id"]),
        limit=limit + 1,
        cursor=cursor,
        unread_only=unread_only,
    )
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = str(rows[-1]["id"]) if has_more else None
    unread_count = await count_unread_notifications(db, str(user["id"]))

    return NotificationsListResponse(
        unread_count=unread_count,
        data=[
            NotificationItem(
                id=r["id"],
                type=r["type"],
                title=r["title"],
                body=r["body"],
                is_read=r["read_at"] is not None,
                read_at=r["read_at"],
                reference_id=r["reference_id"],
                reference_type=r["reference_type"],
                created_at=r["created_at"],
                translations=dict(r.get("translations") or {}),
            )
            for r in rows
        ],
        cursor=next_cursor,
        has_more=has_more,
    )


@router.patch("/{notification_id}/read", response_model=MarkReadResponse)
async def mark_notification_read(
    notification_id: UUID,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> MarkReadResponse:
    row = await notification_service.mark_read(db, str(user["id"]), str(notification_id))
    return MarkReadResponse(id=row["id"], is_read=True, read_at=row["read_at"])


@router.post("/read-all", response_model=MarkAllReadResponse)
async def mark_all_read(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> MarkAllReadResponse:
    count = await notification_service.mark_all_read(db, str(user["id"]))
    return MarkAllReadResponse(updated_count=count)
