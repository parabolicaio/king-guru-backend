"""Learner lesson-read endpoints."""

from fastapi import APIRouter, Depends, Header

import asyncpg

from app.core.config import settings
from app.core.errors import (
    AppError,
    LEVEL_NOT_FOUND,
    LESSON_NOT_FOUND,
    LESSON_LOCKED,
    LESSON_NOT_APPROVED,
    GUEST_ACCESS_DENIED,
    UNAUTHORIZED,
)
from app.core.security import get_current_user, get_optional_user
from app.db.pool import get_db
from app.db.queries.lessons import (
    get_content_blocks_for_section,
    get_latest_attempts_for_lesson,
    get_lesson_for_learner,
    get_lesson_progress_for_user,
    get_lessons_for_level,
    get_level_with_lessons,
    get_questions_for_section,
    get_section_category_image_map,
    get_sections_for_lesson,
    get_vocabulary_mastery_for_lesson,
    get_vocabulary_words_for_section,
)
from app.schemas.lessons import (
    ContentBlock,
    LatestAttempt,
    LessonDetail,
    LessonDetailResponse,
    LessonProgress,
    LessonSection,
    LessonSummary,
    LessonsListResponse,
    LevelInfo,
    QuestionInLesson,
    VocabularyMastery,
    VocabularyWordInLesson,
)
from app.services.lesson_chain import get_lessons_with_progress

router = APIRouter(tags=["lessons"])


def _build_cdn(path: str | None) -> str | None:
    return settings.build_cdn_url(path)


@router.get("/api/v1/levels/{level_id}/lessons", response_model=LessonsListResponse)
async def list_lessons(
    level_id: str,
    x_guest_token: str | None = Header(default=None),
    user: asyncpg.Record | None = Depends(get_optional_user),
    db: asyncpg.Connection = Depends(get_db),
) -> LessonsListResponse:
    level = await get_level_with_lessons(db, level_id)
    if level is None:
        raise AppError(*LEVEL_NOT_FOUND)

    user_id = str(user["id"]) if user else None
    is_guest = user is None or bool(user.get("is_guest"))

    lessons = await get_lessons_with_progress(db, level_id, user_id)

    summaries = []
    for lw in lessons:
        if is_guest and not lw.is_guest_accessible:
            continue

        summaries.append(
            LessonSummary(
                id=lw.id,
                title=lw.title,
                description=lw.description,
                lesson_order=lw.lesson_order,
                thumbnail_url=_build_cdn(lw.thumbnail_url),
                is_guest_accessible=lw.is_guest_accessible,
                translations=lw.translations,
                progress=LessonProgress(
                    status=lw.status,
                    completion_pct=lw.completion_pct,
                    completed_at=lw.completed_at,
                ),
            )
        )

    return LessonsListResponse(
        level=LevelInfo(id=level["id"], name=level["name"], code=level["code"]),
        lessons=summaries,
    )


@router.get("/api/v1/lessons/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson(
    lesson_id: str,
    x_guest_token: str | None = Header(default=None),
    user: asyncpg.Record | None = Depends(get_optional_user),
    db: asyncpg.Connection = Depends(get_db),
) -> LessonDetailResponse:
    lesson = await get_lesson_for_learner(db, lesson_id)
    if lesson is None:
        raise AppError(*LESSON_NOT_FOUND)

    # Any request that carries a valid Bearer JWT is from a registered user,
    # regardless of the is_guest column (which can be stale after guest→register upgrade).
    is_guest = user is None

    if is_guest and not lesson["is_guest_accessible"]:
        raise AppError(*GUEST_ACCESS_DENIED)

    if lesson["status"] not in ("approved",):
        raise AppError(*LESSON_NOT_APPROVED)

    # Check lock state for authenticated users
    user_id: str | None = str(user["id"]) if user else None
    if user_id:
        progress = await get_lesson_progress_for_user(db, user_id, lesson_id)
        if progress is None and lesson["lesson_order"] > 1:
            raise AppError(*LESSON_LOCKED)

    # Build full nested response
    sections_rows = await get_sections_for_lesson(db, lesson_id)
    category_image_map = await get_section_category_image_map(db)

    latest_attempts: dict[str, asyncpg.Record] = {}
    mastery_map: dict[str, asyncpg.Record] = {}

    if user_id:
        attempts = await get_latest_attempts_for_lesson(db, lesson_id, user_id)
        latest_attempts = {str(a["question_id"]): a for a in attempts}

        mastery_rows = await get_vocabulary_mastery_for_lesson(db, lesson_id, user_id)
        mastery_map = {str(m["vocabulary_word_id"]): m for m in mastery_rows}

    sections = []
    for sec in sections_rows:
        sec_id = str(sec["id"])

        blocks_rows = await get_content_blocks_for_section(db, sec_id)
        questions_rows = await get_questions_for_section(db, sec_id)
        vocab_rows = await get_vocabulary_words_for_section(db, sec_id)

        blocks = [
            ContentBlock(
                id=row["id"],
                block_type=row["block_type"],
                display_order=row["display_order"],
                payload=dict(row["payload"]),
                translations=dict(row["translations"] or {}),
            )
            for row in blocks_rows
        ]

        questions = []
        for qrow in questions_rows:
            qid = str(qrow["id"])
            attempt = latest_attempts.get(qid)
            questions.append(
                QuestionInLesson(
                    id=qrow["id"],
                    type=qrow["type"],
                    purpose=qrow["purpose"],
                    display_order=qrow["display_order"],
                    prompt_text=qrow["prompt_text"],
                    prompt_audio_url=_build_cdn(qrow["prompt_audio_url"]),
                    prompt_image_url=_build_cdn(qrow["prompt_image_url"]),
                    payload=dict(qrow["payload"]),
                    xp_value=qrow["xp_value"],
                    hint_text=qrow["hint_text"],
                    vocabulary_word_id=qrow["vocabulary_word_id"],
                    translations=dict(qrow["translations"] or {}),
                    latest_attempt=(
                        LatestAttempt(
                            id=attempt["id"],
                            score_fraction=float(attempt["score_fraction"]),
                            is_correct=(attempt["score_numerator"] == attempt["score_denominator"]),
                            response=dict(attempt["response"]),
                            xp_awarded=attempt["xp_awarded"],
                            created_at=attempt["created_at"],
                        )
                        if attempt else None
                    ),
                )
            )

        vocab_words = []
        for vrow in vocab_rows:
            vid = str(vrow["id"])
            m = mastery_map.get(vid)
            vocab_words.append(
                VocabularyWordInLesson(
                    id=vrow["id"],
                    word=vrow["word"],
                    definition=vrow["definition"],
                    example_sentence=vrow["example_sentence"],
                    pronunciation_guide_si=vrow["pronunciation_guide_si"],
                    difficulty=vrow["difficulty"],
                    image_url=_build_cdn(vrow["image_url"]),
                    audio_url=_build_cdn(vrow["audio_url"]),
                    translations=dict(vrow["translations"] or {}),
                    mastery=(
                        VocabularyMastery(
                            attempt_count=m["attempt_count"],
                            correct_attempt_count=m["correct_attempt_count"],
                            is_mastered=m["is_mastered"],
                        )
                        if m else None
                    ),
                )
            )

        sections.append(
            LessonSection(
                id=sec["id"],
                category=sec["category"],
                display_order=sec["display_order"],
                title=sec["title"],
                image_url=_build_cdn(category_image_map.get(sec["category"])),
                translations=dict(sec["translations"] or {}),
                content_blocks=blocks,
                questions=questions,
                vocabulary_words=vocab_words,
            )
        )

    return LessonDetailResponse(
        lesson=LessonDetail(
            id=lesson["id"],
            title=lesson["title"],
            description=lesson["description"],
            lesson_order=lesson["lesson_order"],
            status=lesson["status"],
            thumbnail_url=_build_cdn(lesson["thumbnail_url"]),
            is_guest_accessible=lesson["is_guest_accessible"],
            translations=dict(lesson["translations"] or {}),
            objectives=list(lesson["objectives"] or []),
            objectives_translations=dict(lesson["objectives_translations"] or {}),
            sections=sections,
        )
    )
