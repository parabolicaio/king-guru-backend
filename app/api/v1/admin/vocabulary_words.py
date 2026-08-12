"""Admin endpoints for vocabulary word management (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.errors import (
    AppError,
    SECTION_NOT_FOUND,
    VOCABULARY_WORD_HAS_MASTERY,
    VOCABULARY_WORD_NOT_FOUND,
)
from app.core.security import get_content_manager_user
from app.db.pool import get_db
from app.db.queries.admin_lessons import (
    create_vocabulary_word,
    delete_vocabulary_word,
    get_section_admin,
    get_vocabulary_word_admin,
    update_vocabulary_word,
    vocabulary_word_has_mastery,
)
from app.schemas.admin_content import (
    AdminVocabularyWordItem,
    CreateVocabularyWordRequest,
    UpdateVocabularyWordRequest,
)
from app.services import tts_service

router = APIRouter(tags=["admin-vocabulary-words"])


def _row_to_item(row: asyncpg.Record) -> AdminVocabularyWordItem:
    return AdminVocabularyWordItem(
        id=row["id"],
        lesson_section_id=row["lesson_section_id"],
        word=row["word"],
        definition=row["definition"],
        example_sentence=row["example_sentence"],
        pronunciation_guide_si=row["pronunciation_guide_si"],
        difficulty=row["difficulty"],
        image_url=row["image_url"],
        audio_url=row["audio_url"],
        translations=dict(row["translations"] or {}),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post(
    "/api/v1/admin/sections/{section_id}/vocabulary-words",
    response_model=AdminVocabularyWordItem,
    status_code=201,
)
async def create_vocabulary_word_endpoint(
    section_id: UUID,
    body: CreateVocabularyWordRequest,
    background_tasks: BackgroundTasks,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminVocabularyWordItem:
    section = await get_section_admin(db, str(section_id))
    if section is None:
        raise AppError(*SECTION_NOT_FOUND)

    row = await create_vocabulary_word(
        db,
        lesson_section_id=str(section_id),
        word=body.word,
        definition=body.definition,
        example_sentence=body.example_sentence,
        pronunciation_guide_si=body.pronunciation_guide_si,
        difficulty=body.difficulty,
        image_url=body.image_url,
        translations=body.translations,
    )

    # Queue TTS for English (and Sinhala if provided)
    translations_data = body.translations or {}
    text_si = translations_data.get("si", {}).get("word") if isinstance(translations_data.get("si"), dict) else None
    tts_service.generate_async(background_tasks, str(row["id"]), body.word, text_si)

    return _row_to_item(row)


@router.patch(
    "/api/v1/admin/vocabulary-words/{word_id}",
    response_model=AdminVocabularyWordItem,
)
async def update_vocabulary_word_endpoint(
    word_id: UUID,
    body: UpdateVocabularyWordRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminVocabularyWordItem:
    row = await get_vocabulary_word_admin(db, str(word_id))
    if row is None:
        raise AppError(*VOCABULARY_WORD_NOT_FOUND)

    updates: dict = {}
    for field in ("word", "definition", "example_sentence", "pronunciation_guide_si",
                  "difficulty", "image_url", "translations"):
        val = getattr(body, field, None)
        if val is not None:
            updates[field] = val

    if not updates:
        return _row_to_item(row)

    updated = await update_vocabulary_word(db, str(word_id), **updates)
    return _row_to_item(updated)


@router.delete("/api/v1/admin/vocabulary-words/{word_id}", status_code=204)
async def delete_vocabulary_word_endpoint(
    word_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> None:
    row = await get_vocabulary_word_admin(db, str(word_id))
    if row is None:
        raise AppError(*VOCABULARY_WORD_NOT_FOUND)
    if await vocabulary_word_has_mastery(db, str(word_id)):
        raise AppError(*VOCABULARY_WORD_HAS_MASTERY)
    await delete_vocabulary_word(db, str(word_id))
