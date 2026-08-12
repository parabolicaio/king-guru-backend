"""Admin endpoints for lesson section management (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends

from app.core.errors import (
    AppError,
    DISPLAY_ORDER_CONFLICT,
    LESSON_NOT_FOUND,
    SECTION_HAS_ATTEMPTS,
    SECTION_NOT_FOUND,
)
from app.core.security import get_content_manager_user
from app.db.pool import get_db
from app.db.queries.admin_lessons import (
    create_section,
    delete_section,
    get_lesson_admin,
    get_section_admin,
    section_has_attempts,
    update_section,
)
from app.schemas.admin_content import AdminSectionItem, CreateSectionRequest, UpdateSectionRequest

router = APIRouter(tags=["admin-sections"])


def _row_to_item(row: asyncpg.Record) -> AdminSectionItem:
    return AdminSectionItem(
        id=row["id"],
        lesson_id=row["lesson_id"],
        category=row["category"],
        display_order=row["display_order"],
        title=row["title"],
        translations=dict(row["translations"] or {}),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("/api/v1/admin/lessons/{lesson_id}/sections", response_model=AdminSectionItem, status_code=201)
async def create_section_endpoint(
    lesson_id: UUID,
    body: CreateSectionRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminSectionItem:
    lesson = await get_lesson_admin(db, str(lesson_id))
    if lesson is None:
        raise AppError(*LESSON_NOT_FOUND)

    # Check display_order uniqueness within lesson
    conflict = await db.fetchrow(
        "SELECT id FROM lesson_section WHERE lesson_id = $1::uuid AND display_order = $2",
        str(lesson_id), body.display_order,
    )
    if conflict:
        raise AppError(*DISPLAY_ORDER_CONFLICT)

    row = await create_section(
        db,
        lesson_id=str(lesson_id),
        category=body.category,
        display_order=body.display_order,
        title=body.title,
        translations=body.translations,
    )
    return _row_to_item(row)


@router.patch("/api/v1/admin/sections/{section_id}", response_model=AdminSectionItem)
async def update_section_endpoint(
    section_id: UUID,
    body: UpdateSectionRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminSectionItem:
    row = await get_section_admin(db, str(section_id))
    if row is None:
        raise AppError(*SECTION_NOT_FOUND)

    updates: dict = {}
    if body.category is not None:
        updates["category"] = body.category
    if body.display_order is not None:
        updates["display_order"] = body.display_order
    if body.title is not None:
        updates["title"] = body.title
    if body.translations is not None:
        updates["translations"] = body.translations

    if not updates:
        return _row_to_item(row)

    updated = await update_section(db, str(section_id), **updates)
    return _row_to_item(updated)


@router.delete("/api/v1/admin/sections/{section_id}", status_code=204)
async def delete_section_endpoint(
    section_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> None:
    row = await get_section_admin(db, str(section_id))
    if row is None:
        raise AppError(*SECTION_NOT_FOUND)
    if await section_has_attempts(db, str(section_id)):
        raise AppError(*SECTION_HAS_ATTEMPTS)
    await delete_section(db, str(section_id))
