"""Admin endpoints for question management (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends

from app.core.errors import (
    AppError,
    QUESTION_HAS_ATTEMPTS,
    QUESTION_NOT_FOUND,
    SECTION_NOT_FOUND,
)
from app.core.security import get_content_manager_user
from app.db.pool import get_db
from app.db.queries.admin_lessons import (
    create_question,
    delete_question,
    get_question_admin,
    get_section_admin,
    question_has_attempts,
    update_question,
)
from app.schemas.admin_content import AdminQuestionItem, CreateQuestionRequest, UpdateQuestionRequest

router = APIRouter(tags=["admin-questions"])


def _row_to_item(row: asyncpg.Record) -> AdminQuestionItem:
    return AdminQuestionItem(
        id=row["id"],
        lesson_section_id=row["lesson_section_id"],
        type=row["type"],
        purpose=row["purpose"],
        display_order=row["display_order"],
        prompt_text=row["prompt_text"],
        prompt_audio_url=row["prompt_audio_url"],
        prompt_image_url=row["prompt_image_url"],
        payload=dict(row["payload"] or {}),
        xp_value=row["xp_value"],
        hint_text=row["hint_text"],
        vocabulary_word_id=row["vocabulary_word_id"],
        translations=dict(row["translations"] or {}),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("/api/v1/admin/sections/{section_id}/questions", response_model=AdminQuestionItem, status_code=201)
async def create_question_endpoint(
    section_id: UUID,
    body: CreateQuestionRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminQuestionItem:
    section = await get_section_admin(db, str(section_id))
    if section is None:
        raise AppError(*SECTION_NOT_FOUND)

    row = await create_question(
        db,
        lesson_section_id=str(section_id),
        question_type=body.type,
        purpose=body.purpose,
        display_order=body.display_order,
        prompt_text=body.prompt_text,
        prompt_audio_url=body.prompt_audio_url,
        prompt_image_url=body.prompt_image_url,
        payload=body.payload,
        xp_value=body.xp_value,
        hint_text=body.hint_text,
        vocabulary_word_id=str(body.vocabulary_word_id) if body.vocabulary_word_id else None,
        translations=body.translations,
    )
    return _row_to_item(row)


@router.patch("/api/v1/admin/questions/{question_id}", response_model=AdminQuestionItem)
async def update_question_endpoint(
    question_id: UUID,
    body: UpdateQuestionRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminQuestionItem:
    row = await get_question_admin(db, str(question_id))
    if row is None:
        raise AppError(*QUESTION_NOT_FOUND)

    updates: dict = {}
    for field in ("type", "purpose", "display_order", "prompt_text", "prompt_audio_url",
                  "prompt_image_url", "payload", "xp_value", "hint_text", "translations"):
        val = getattr(body, field, None)
        if val is not None:
            updates[field] = val
    if body.vocabulary_word_id is not None:
        updates["vocabulary_word_id"] = str(body.vocabulary_word_id)

    if not updates:
        return _row_to_item(row)

    updated = await update_question(db, str(question_id), **updates)
    return _row_to_item(updated)


@router.delete("/api/v1/admin/questions/{question_id}", status_code=204)
async def delete_question_endpoint(
    question_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> None:
    row = await get_question_admin(db, str(question_id))
    if row is None:
        raise AppError(*QUESTION_NOT_FOUND)
    if await question_has_attempts(db, str(question_id)):
        raise AppError(*QUESTION_HAS_ATTEMPTS)
    await delete_question(db, str(question_id))
