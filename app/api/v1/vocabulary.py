from fastapi import APIRouter, Depends
from uuid import UUID

import asyncpg

from app.core.config import settings
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.vocabulary import get_vocabulary_for_user
from app.schemas.vocabulary import VocabMasteryDetail, VocabularyListResponse, VocabularyWordItem

router = APIRouter(prefix="/api/v1/vocabulary", tags=["vocabulary"])


@router.get("", response_model=VocabularyListResponse)
async def list_vocabulary(
    level_id: UUID | None = None,
    mastered: bool | None = None,
    cursor: str | None = None,
    limit: int = 40,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> VocabularyListResponse:
    rows = await get_vocabulary_for_user(
        db,
        user_id=str(user["id"]),
        limit=limit,
        cursor=cursor,
        mastered=mastered,
        level_id=str(level_id) if level_id else None,
    )

    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = str(rows[-1]["id"]) if has_more else None

    return VocabularyListResponse(
        data=[
            VocabularyWordItem(
                id=r["id"],
                word=r["word"],
                definition=r["definition"],
                example_sentence=r["example_sentence"],
                pronunciation_guide_si=r["pronunciation_guide_si"],
                difficulty=r["difficulty"],
                image_url=settings.build_cdn_url(r["image_url"]),
                audio_url=settings.build_cdn_url(r["audio_url"]),
                level_code=r["level_code"],
                translations=dict(r["translations"] or {}),
                mastery=VocabMasteryDetail(
                    attempt_count=r["attempt_count"],
                    correct_attempt_count=r["correct_attempt_count"],
                    is_mastered=r["is_mastered"],
                    last_seen_at=r["last_seen_at"],
                ),
            )
            for r in rows
        ],
        cursor=next_cursor,
        has_more=has_more,
    )
