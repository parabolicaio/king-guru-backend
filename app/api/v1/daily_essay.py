"""Daily Essay endpoints."""

import logging

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Depends

from app.core.errors import AppError
from app.core.ratelimit import rate_limit
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.daily_essay import (
    get_essay_history,
    get_submission_by_id,
    get_submission_for_today,
    get_today_prompt,
)
from app.schemas.daily_essay import (
    EssayGradeDetail,
    EssayHistoryItem,
    EssayHistoryResponse,
    EssayPromptResponse,
    EssaySubmissionResponse,
    SaveDraftRequest,
    SubmitEssayRequest,
    TodayEssayResponse,
)
from app.services import achievement_service
from app.services import daily_essay_service
from app.services import daily_goal_service
from app.services import streak as streak_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/daily-essay", tags=["daily-essay"])


def _submission_row_to_response(row: asyncpg.Record) -> EssaySubmissionResponse:
    grading = None
    if row["grade"] is not None:
        raw = dict(row["ai_feedback"] or {})
        overall_summary = raw.pop("overall_summary", None) or None
        grading = EssayGradeDetail(
            score_grammar=row["score_grammar"],
            score_vocabulary=row["score_vocabulary"],
            score_content=row["score_content"],
            score_suggestions=row["score_suggestions"],
            overall_summary=overall_summary,
            ai_feedback=raw if raw else None,
        )
    return EssaySubmissionResponse(
        id=row["id"],
        essay_prompt_id=row["essay_prompt_id"],
        prompt_text=row["prompt_text"],
        essay_text=row["essay_text"],
        submitted_at=row["submitted_at"],
        submission_date=row["submission_date"],
        is_draft=row["is_draft"],
        grade=row["grade"],
        xp_awarded=row["xp_awarded"],
        feedback_language=row["feedback_language"],
        grading=grading,
    )


async def _grade_in_background(
    submission_id: str,
    essay_text: str,
    prompt_text: str,
    feedback_language: str,
    level_id: str | None = None,
) -> None:
    from app.db.pool import get_pool

    logger.info(
        "daily_essay grading started submission_id=%s essay_chars=%d feedback_language=%s level_id=%s",
        submission_id,
        len(essay_text),
        feedback_language,
        level_id,
    )
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            level_code: str | None = None
            if level_id:
                row = await conn.fetchrow(
                    "SELECT code FROM level WHERE id = $1::uuid",
                    level_id,
                )
                if row:
                    level_code = row["code"]
            result = await daily_essay_service.grade_submission(
                conn, submission_id, essay_text, prompt_text, feedback_language, level_code
            )
        logger.info(
            "daily_essay grading finished submission_id=%s grade=%s xp_awarded=%d model=%s level_code=%s",
            submission_id,
            result.grade,
            result.xp_awarded,
            result.ai_model,
            level_code,
        )
    except Exception:
        logger.exception(
            "daily_essay grading failed submission_id=%s",
            submission_id,
        )


@router.get("/today", response_model=TodayEssayResponse)
async def get_today(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> TodayEssayResponse:
    """Return today's prompt and the user's current submission state.

    submission=null → not started
    submission.is_draft=true → draft saved, not yet submitted
    submission.is_draft=false → submitted (grade may still be pending)
    """
    today = daily_essay_service.today_slst()
    level_id = str(user["current_level_id"]) if user["current_level_id"] else None

    prompt = await get_today_prompt(db, level_id, today)
    if prompt is None:
        raise AppError(*daily_essay_service.NO_PROMPT_AVAILABLE)

    submission_row = await get_submission_for_today(db, str(user["id"]), today)

    return TodayEssayResponse(
        prompt=EssayPromptResponse(
            id=prompt["id"],
            prompt_text=prompt["prompt_text"],
            level_id=prompt["level_id"],
            date_assigned=prompt["date_assigned"],
            translations=dict(prompt["translations"] or {}),
        ),
        submission=_submission_row_to_response(submission_row) if submission_row else None,
    )


@router.put("/draft", response_model=EssaySubmissionResponse, status_code=200)
async def save_draft(
    body: SaveDraftRequest,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> EssaySubmissionResponse:
    """Create or overwrite a draft for today.

    Idempotent — safe to call on every autosave tick.
    Returns 409 if today's essay has already been submitted.
    """
    draft = await daily_essay_service.save_draft(
        db,
        user=user,
        essay_prompt_id=str(body.essay_prompt_id),
        draft_text=body.draft_text,
        feedback_language=body.feedback_language,
    )
    logger.debug(
        "daily_essay draft saved user_id=%s submission_id=%s chars=%d",
        user["id"],
        draft["id"],
        len(body.draft_text),
    )
    return _submission_row_to_response(draft)


@router.post(
    "/submit",
    response_model=EssaySubmissionResponse,
    status_code=201,
    # Essay grading calls Gemini — cap per-user submits (normal use is a few/day).
    dependencies=[Depends(rate_limit(15, 60, "essay_submit"))],
)
async def submit_essay(
    body: SubmitEssayRequest,
    background_tasks: BackgroundTasks,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> EssaySubmissionResponse:
    """Submit today's essay.

    Promotes an existing draft if one exists; otherwise creates a fresh submitted row.
    Grading runs asynchronously — grade will be null in the immediate response.
    """
    logger.info(
        "daily_essay submit requested user_id=%s prompt_id=%s chars=%d feedback_language=%s",
        user["id"],
        body.essay_prompt_id,
        len(body.essay_text),
        body.feedback_language,
    )

    submission = await daily_essay_service.submit(
        db,
        user=user,
        essay_prompt_id=str(body.essay_prompt_id),
        essay_text=body.essay_text,
        feedback_language=body.feedback_language,
    )

    logger.info(
        "daily_essay submit recorded submission_id=%s user_id=%s submission_date=%s",
        submission["id"],
        user["id"],
        submission["submission_date"],
    )

    background_tasks.add_task(
        _grade_in_background,
        str(submission["id"]),
        body.essay_text,
        submission["prompt_text"],
        body.feedback_language,
        str(user["current_level_id"]) if user["current_level_id"] else None,
    )
    logger.info(
        "daily_essay grading queued submission_id=%s",
        submission["id"],
    )

    # Daily goal hook — essay_submitted
    if user["current_level_id"]:
        await daily_goal_service.record_activity(
            db,
            str(user["id"]),
            "essay_submitted",
            level_id=str(user["current_level_id"]),
        )

    # Streak qualification — daily essay counts as a qualifying activity
    await streak_service.record_qualifying_activity(db, str(user["id"]))

    # Achievements (essay_count / streak). XP-based ones from grading are picked
    # up on the next qualifying action since grading runs in the background.
    try:
        fresh_user = await db.fetchrow(
            'SELECT * FROM "user" WHERE id = $1::uuid', str(user["id"])
        )
        if fresh_user is not None:
            await achievement_service.check_and_unlock(db, fresh_user)
    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "achievement check failed for user=%s", user["id"]
        )

    return _submission_row_to_response(submission)


@router.get("/history", response_model=EssayHistoryResponse)

async def get_history(
    cursor: str | None = None,
    limit: int = 10,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> EssayHistoryResponse:
    rows = await get_essay_history(db, str(user["id"]), limit=limit + 1, cursor=cursor)
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = str(rows[-1]["id"]) if has_more else None

    return EssayHistoryResponse(
        data=[
            EssayHistoryItem(
                id=r["id"],
                essay_prompt_id=r["essay_prompt_id"],
                prompt_text=r["prompt_text"],
                submission_date=r["submission_date"],
                grade=r["grade"],
                xp_awarded=r["xp_awarded"],
                submitted_at=r["submitted_at"],
                word_count=r["word_count"],
            )
            for r in rows
        ],
        cursor=next_cursor,
        has_more=has_more,
    )


@router.get("/{submission_id}", response_model=EssaySubmissionResponse)
async def get_submission(
    submission_id: str,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> EssaySubmissionResponse:
    """Return a specific submitted essay (scoped to the authenticated user)."""
    row = await get_submission_by_id(db, str(user["id"]), submission_id)
    if row is None:
        raise AppError("ESSAY_NOT_FOUND", "Essay not found.", 404)
    return _submission_row_to_response(row)
