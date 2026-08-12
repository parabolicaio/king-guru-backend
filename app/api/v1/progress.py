"""User progress endpoints."""

from fastapi import APIRouter, Depends

import asyncpg

from app.core.errors import AppError, LEVEL_NOT_SET
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.levels import get_level_by_id
from app.db.queries.progress import get_skill_progress, get_user_progress_summary
from app.schemas.progress import SkillProgress, SkillsProgressResponse
from app.schemas.lessons import (
    LessonProgress,
    LessonSummary,
    LevelInfo,
    UserProgressResponse,
    UserProgressSummary,
)
from app.services.lesson_chain import get_lessons_with_progress
from app.core.config import settings

router = APIRouter(prefix="/api/v1/users/me", tags=["progress"])


@router.get("/progress", response_model=UserProgressResponse)
async def get_progress(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> UserProgressResponse:
    summary = await get_user_progress_summary(db, str(user["id"]))

    current_level: LevelInfo | None = None
    lessons: list[LessonSummary] = []

    level_id = str(user["current_level_id"]) if user["current_level_id"] else None
    if level_id:
        level_row = await get_level_by_id(db, level_id)
        if level_row:
            current_level = LevelInfo(
                id=level_row["id"],
                name=level_row["name"],
                code=level_row["code"],
            )
            lesson_list = await get_lessons_with_progress(db, level_id, str(user["id"]))
            lessons = [
                LessonSummary(
                    id=lw.id,
                    title=lw.title,
                    description=lw.description,
                    lesson_order=lw.lesson_order,
                    thumbnail_url=settings.build_cdn_url(lw.thumbnail_url),
                    is_guest_accessible=lw.is_guest_accessible,
                    translations=lw.translations,
                    progress=LessonProgress(
                        status=lw.status,
                        completion_pct=lw.completion_pct,
                        completed_at=lw.completed_at,
                    ),
                )
                for lw in lesson_list
            ]

    last_date = None
    if summary and summary["streak_last_activity_date"]:
        last_date = str(summary["streak_last_activity_date"])

    return UserProgressResponse(
        user=UserProgressSummary(
            xp_total=summary["xp_total"] if summary else 0,
            streak_current=summary["streak_current"] if summary else 0,
            streak_longest=summary["streak_longest"] if summary else 0,
            streak_last_activity_date=last_date,
            current_level_id=user["current_level_id"],
            completed_lesson_count=int(summary["completed_lesson_count"]) if summary else 0,
        ),
        current_level=current_level,
        lessons=lessons,
    )


@router.get("/skills", response_model=SkillsProgressResponse)
async def get_skills_progress(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> SkillsProgressResponse:
    if not user["current_level_id"]:
        raise AppError(*LEVEL_NOT_SET)

    rows = await get_skill_progress(db, str(user["id"]), str(user["current_level_id"]))
    return SkillsProgressResponse(
        skills=[
            SkillProgress(
                category=row["category"],
                total_questions=int(row["total_questions"]),
                is_available=bool(row["is_available"]),
                questions_answered=int(row["questions_answered"]),
                accuracy=float(row["accuracy"]) if row["accuracy"] is not None else None,
            )
            for row in rows
        ]
    )
