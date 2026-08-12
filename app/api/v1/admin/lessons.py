"""Admin endpoints for lesson management (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.errors import AppError, LESSON_NOT_FOUND, LEVEL_NOT_FOUND
from app.core.security import get_admin_user, get_content_manager_user
from app.db.pool import get_db
from app.db.queries.admin_lessons import (
    archive_lesson,
    create_lesson,
    get_lesson_admin,
    list_lessons_admin,
    soft_delete_lesson,
    update_lesson,
)
from app.db.queries.levels import get_level_by_id
from app.schemas.admin_content import (
    AdminLessonItem,
    AdminLessonListResponse,
    CreateLessonRequest,
    UpdateLessonRequest,
)
from app.services.lesson_chain import compute_next_order

router = APIRouter(prefix="/api/v1/admin/lessons", tags=["admin-lessons"])


def _row_to_item(row: asyncpg.Record) -> AdminLessonItem:
    return AdminLessonItem(
        id=row["id"],
        level_id=row["level_id"],
        title=row["title"],
        description=row["description"],
        lesson_order=row["lesson_order"],
        status=row["status"],
        is_guest_accessible=row["is_guest_accessible"],
        thumbnail_url=row["thumbnail_url"],
        translations=dict(row["translations"] or {}),
        objectives=list(row["objectives"] or []),
        objectives_translations=dict(row["objectives_translations"] or {}),
        archived_at=row["archived_at"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("", response_model=AdminLessonItem, status_code=201)
async def create_lesson_endpoint(
    body: CreateLessonRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminLessonItem:
    level = await get_level_by_id(db, str(body.level_id))
    if level is None:
        raise AppError(*LEVEL_NOT_FOUND)

    lesson_order = await compute_next_order(db, str(body.level_id))
    row = await create_lesson(
        db,
        level_id=str(body.level_id),
        title=body.title,
        description=body.description,
        lesson_order=lesson_order,
        is_guest_accessible=body.is_guest_accessible,
        thumbnail_url=body.thumbnail_url,
        translations=body.translations,
        objectives=body.objectives,
        objectives_translations=body.objectives_translations,
        created_by=str(user["id"]),
    )

    from app.services import audit_service
    await audit_service.log(
        db,
        action="lesson.created",
        actor_id=str(user["id"]),
        target_type="lesson",
        target_id=str(row["id"]),
    )

    return _row_to_item(row)


@router.get("", response_model=AdminLessonListResponse)
async def list_lessons_endpoint(
    level_id: UUID | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminLessonListResponse:
    is_admin = user["admin_role"] == "admin"
    rows, total = await list_lessons_admin(
        db,
        level_id=str(level_id) if level_id else None,
        status=status,
        cm_id=str(user["id"]),
        admin_sees_all=is_admin,
        page=page,
        page_size=page_size,
    )
    return AdminLessonListResponse(
        data=[_row_to_item(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{lesson_id}", response_model=AdminLessonItem)
async def get_lesson_endpoint(
    lesson_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminLessonItem:
    row = await get_lesson_admin(db, str(lesson_id))
    if row is None:
        raise AppError(*LESSON_NOT_FOUND)
    return _row_to_item(row)


@router.patch("/{lesson_id}", response_model=AdminLessonItem)
async def update_lesson_endpoint(
    lesson_id: UUID,
    body: UpdateLessonRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminLessonItem:
    row = await get_lesson_admin(db, str(lesson_id))
    if row is None:
        raise AppError(*LESSON_NOT_FOUND)

    is_admin = user["admin_role"] == "admin"
    is_minor = body.is_minor_edit and is_admin

    new_status: str | None = None
    if not is_minor and row["status"] == "approved":
        new_status = "pending_review"

    updated = await update_lesson(
        db,
        str(lesson_id),
        title=body.title,
        description=body.description,
        is_guest_accessible=body.is_guest_accessible,
        thumbnail_url=body.thumbnail_url,
        translations=body.translations,
        objectives=body.objectives,
        objectives_translations=body.objectives_translations,
        status=new_status,
    )

    action = "lesson.minor_edit" if is_minor else "lesson.edited"
    from app.services import audit_service
    await audit_service.log(db, action=action, actor_id=str(user["id"]), target_type="lesson", target_id=str(lesson_id))

    return _row_to_item(updated)


@router.delete("/{lesson_id}", status_code=204)
async def delete_lesson_endpoint(
    lesson_id: UUID,
    user: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> None:
    row = await get_lesson_admin(db, str(lesson_id))
    if row is None:
        raise AppError(*LESSON_NOT_FOUND)
    await soft_delete_lesson(db, str(lesson_id))
    from app.services import audit_service
    await audit_service.log(db, action="lesson.deleted", actor_id=str(user["id"]), target_type="lesson", target_id=str(lesson_id))


@router.patch("/{lesson_id}/archive", response_model=AdminLessonItem)
async def archive_lesson_endpoint(
    lesson_id: UUID,
    user: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminLessonItem:
    row = await get_lesson_admin(db, str(lesson_id))
    if row is None:
        raise AppError(*LESSON_NOT_FOUND)
    updated = await archive_lesson(db, str(lesson_id))
    from app.services import audit_service
    await audit_service.log(db, action="lesson.archived", actor_id=str(user["id"]), target_type="lesson", target_id=str(lesson_id))
    return _row_to_item(updated)
