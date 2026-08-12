"""Admin endpoints for content block management (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.errors import AppError, BLOCK_NOT_FOUND, DISPLAY_ORDER_CONFLICT, SECTION_NOT_FOUND
from app.core.security import get_content_manager_user
from app.db.pool import get_db
from app.db.queries.admin_lessons import (
    create_block,
    delete_block,
    display_order_exists_in_section,
    get_block_admin,
    get_section_admin,
    update_block,
)
from app.schemas.admin_content import AdminBlockItem, CreateBlockRequest, UpdateBlockRequest
from app.services import tts_service

router = APIRouter(tags=["admin-blocks"])


def _row_to_item(row: asyncpg.Record) -> AdminBlockItem:
    return AdminBlockItem(
        id=row["id"],
        lesson_section_id=row["lesson_section_id"],
        block_type=row["block_type"],
        display_order=row["display_order"],
        payload=dict(row["payload"] or {}),
        translations=dict(row["translations"] or {}),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("/api/v1/admin/sections/{section_id}/blocks", response_model=AdminBlockItem, status_code=201)
async def create_block_endpoint(
    section_id: UUID,
    body: CreateBlockRequest,
    background_tasks: BackgroundTasks,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminBlockItem:
    section = await get_section_admin(db, str(section_id))
    if section is None:
        raise AppError(*SECTION_NOT_FOUND)

    if await display_order_exists_in_section(db, str(section_id), body.display_order):
        raise AppError(*DISPLAY_ORDER_CONFLICT)

    row = await create_block(
        db,
        lesson_section_id=str(section_id),
        block_type=body.block_type,
        display_order=body.display_order,
        payload=body.payload,
        translations=body.translations,
    )

    # Queue TTS for word_card blocks
    if body.block_type == "word_card":
        word_text_en = body.payload.get("word") or body.payload.get("text_en", "")
        word_text_si = body.payload.get("text_si")
        if word_text_en:
            tts_service.generate_async(background_tasks, str(row["id"]), word_text_en, word_text_si)

    return _row_to_item(row)


@router.patch("/api/v1/admin/blocks/{block_id}", response_model=AdminBlockItem)
async def update_block_endpoint(
    block_id: UUID,
    body: UpdateBlockRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminBlockItem:
    row = await get_block_admin(db, str(block_id))
    if row is None:
        raise AppError(*BLOCK_NOT_FOUND)

    updates: dict = {}
    if body.block_type is not None:
        updates["block_type"] = body.block_type
    if body.display_order is not None:
        if await display_order_exists_in_section(db, str(row["lesson_section_id"]), body.display_order, exclude_block_id=str(block_id)):
            raise AppError(*DISPLAY_ORDER_CONFLICT)
        updates["display_order"] = body.display_order
    if body.payload is not None:
        updates["payload"] = body.payload
    if body.translations is not None:
        updates["translations"] = body.translations

    if not updates:
        return _row_to_item(row)

    updated = await update_block(db, str(block_id), **updates)
    return _row_to_item(updated)


@router.delete("/api/v1/admin/blocks/{block_id}", status_code=204)
async def delete_block_endpoint(
    block_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> None:
    row = await get_block_admin(db, str(block_id))
    if row is None:
        raise AppError(*BLOCK_NOT_FOUND)
    await delete_block(db, str(block_id))
