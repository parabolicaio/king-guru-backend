"""Attempt submission — 7-step atomic side-effect chain."""

import base64

import asyncpg
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.errors import (
    AppError,
    GUEST_ACCESS_DENIED,
    LESSON_LOCKED,
    LESSON_NOT_APPROVED,
    QUESTION_NOT_FOUND,
    UNAUTHORIZED,
)
from app.core.ratelimit import rate_limit
from app.core.security import get_current_user, get_optional_user
from app.db.pool import get_db
from app.db.queries.attempts import (
    get_answered_assessment_question_ids,
    get_assessment_question_ids_for_lesson,
    get_question_with_lesson,
    insert_attempt,
)
from app.db.queries.lessons import get_lesson_progress_for_user
from app.db.utils import new_uuid
from app.schemas.attempts import (
    AttemptFeedback,
    AttemptRequest,
    AttemptResponse,
    LessonResult,
    PronunciationDetail,
    StreakResponse,
    StreakResult,
    UnlockedAchievement,
    XPLedgerEntry,
    XPSummaryResponse,
)
from app.services import daily_goal_service
from app.services import achievement_service
from app.services import pronunciation_service
from app.services import scoring as scoring_service
from app.services import streak as streak_service
from app.services import vocabulary_mastery as mastery_service
from app.services import xp as xp_service
from app.services import progress as progress_service
from app.db.queries.xp import get_xp_ledger_for_user
from app.db.queries.streak import get_streak_milestones, get_streak_state

router = APIRouter(tags=["attempts"])

PRONUNCIATION_TYPES = {"pronunciation_practice", "picture_speak_target"}

# Pronunciation audio guards — the recording is client-supplied and flows into
# Supabase Storage (as Content-Type) and Gemini, so bound both type and size.
_MAX_AUDIO_BYTES = 5 * 1024 * 1024        # 5 MB decoded hard cap (~2.5 min of WAV)
_MAX_AUDIO_B64_LEN = _MAX_AUDIO_BYTES * 2  # coarse pre-decode bound (base64 ≈ 1.33x)
_ALLOWED_AUDIO_MIME = {
    "audio/webm", "audio/ogg", "audio/wav", "audio/x-wav",
    "audio/mpeg", "audio/mp3", "audio/mp4", "audio/aac",
    "audio/m4a", "audio/x-m4a",
}


def _decode_and_validate_audio(audio_b64: str, audio_mime: str) -> bytes:
    """Validate a client-supplied recording and return its decoded bytes.

    Rejects unknown MIME types (audio_mime is used verbatim as the Storage
    Content-Type and sent to Gemini) and caps size, so a caller can't blow up
    memory or run up unbounded Gemini/Storage spend with an oversized blob.
    """
    base_mime = audio_mime.split(";")[0].strip().lower()
    if base_mime not in _ALLOWED_AUDIO_MIME:
        raise HTTPException(status_code=415, detail=f"Unsupported audio type: {base_mime}")
    if len(audio_b64) > _MAX_AUDIO_B64_LEN:
        raise HTTPException(status_code=413, detail="Audio recording is too large.")
    try:
        audio_bytes = base64.b64decode(audio_b64)
    except Exception:
        raise HTTPException(status_code=422, detail="audio_data_base64 is not valid base64.")
    if not audio_bytes:
        raise HTTPException(status_code=422, detail="Audio recording is empty.")
    if len(audio_bytes) > _MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio recording is too large.")
    return audio_bytes


async def _score_pronunciation(
    user: asyncpg.Record | None,
    q_row: asyncpg.Record,
    response: dict,
    attempt_id: str,
) -> tuple["scoring_service.ScoringResult", dict]:
    """Upload audio to Supabase Storage, call Gemini, return ScoringResult + ai_feedback.

    Raises HTTP 422 if the response dict is missing required audio fields.
    """
    from decimal import Decimal
    import httpx
    from app.core.config import settings

    audio_b64: str | None = response.get("audio_data_base64")
    audio_mime: str | None = response.get("audio_mime_type")
    if not audio_b64 or not audio_mime:
        raise HTTPException(
            status_code=422,
            detail="Pronunciation attempts require audio_data_base64 and audio_mime_type in response.",
        )

    # MIME allowlist + size cap before any decode/upload/Gemini work.
    audio_bytes = _decode_and_validate_audio(audio_b64, audio_mime)

    # Derive file extension from MIME type
    mime_lower = audio_mime.lower()
    if "ogg" in mime_lower:
        ext = ".ogg"
    elif "mp3" in mime_lower or "mpeg" in mime_lower:
        ext = ".mp3"
    elif "wav" in mime_lower:
        ext = ".wav"
    elif "mp4" in mime_lower or "m4a" in mime_lower or "aac" in mime_lower:
        ext = ".m4a"
    else:
        ext = ".webm"

    # Upload to Supabase Storage
    user_id_str = str(user["id"]) if user else "guest"
    storage_path = f"recordings/{user_id_str}/{attempt_id}{ext}"
    storage_url = f"{settings.supabase_url}/storage/v1/object/audio/{storage_path}"
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            up_resp = await client.post(
                storage_url,
                content=audio_bytes,
                headers={
                    "Authorization": f"Bearer {settings.supabase_service_role_key}",
                    "Content-Type": audio_mime,
                },
            )
            up_resp.raise_for_status()
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(
            "pronunciation storage upload failed attempt_id=%s error=%s", attempt_id, exc
        )
        storage_path = None  # grade still proceeds even if storage fails

    # Determine target text from question payload
    payload = dict(q_row["payload"])
    if q_row["type"] == "pronunciation_practice":
        target_text = payload.get("target_text", "")
    else:
        target_text = payload.get("target_sentence", "")

    feedback_language = response.get("feedback_language", "en")

    result = await pronunciation_service.grade(
        audio_bytes=audio_bytes,
        audio_mime_type=audio_mime,
        target_text=target_text,
        feedback_language=feedback_language,
    )

    total_raw = result.accuracy + result.clarity + result.fluency
    score_fraction = Decimal(str(round(result.overall_score / 100, 2)))
    scored = scoring_service.ScoringResult(
        score_fraction=score_fraction,
        score_numerator=round(total_raw),
        score_denominator=20,
        is_correct=False,
    )

    ai_feedback = {
        "accuracy": result.accuracy,
        "clarity": result.clarity,
        "fluency": result.fluency,
        "overall_score": result.overall_score,
        "grade": result.grade,
        "summary": result.summary,
        "feedback": result.feedback,
        "ai_model": result.ai_model,
    }
    if storage_path:
        ai_feedback["audio_storage_path"] = f"audio/{storage_path}"

    return scored, ai_feedback


@router.post(
    "/api/v1/attempts",
    response_model=AttemptResponse,
    status_code=201,
    # Caps scripted abuse of the Gemini/Storage pronunciation path; generous
    # enough for normal lesson play (per authenticated user / guest / IP).
    dependencies=[Depends(rate_limit(60, 60, "attempts"))],
)
async def submit_attempt(
    body: AttemptRequest,
    x_guest_token: str | None = Header(default=None),
    user: asyncpg.Record | None = Depends(get_optional_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AttemptResponse:
    # --- Identity resolution ---
    if user is None and not x_guest_token:
        raise AppError(*UNAUTHORIZED)

    is_guest = user is None  # guests never hold a Supabase JWT
    real_user_id: str | None = str(user["id"]) if user else None

    # Resolve guest token to a tracking user_id for progress/XP/mastery
    tracking_user_id: str | None = real_user_id
    if is_guest and x_guest_token:
        from app.services import guest_service
        guest_row = await guest_service.ensure_guest_user(db, x_guest_token)
        tracking_user_id = str(guest_row["id"])

    question_id = str(body.question_id)

    # Check for prior attempts before opening the transaction (used to gate XP below)
    is_first_attempt = True
    if tracking_user_id and not is_guest:
        prior_count = await db.fetchval(
            "SELECT COUNT(*) FROM attempt WHERE user_id = $1 AND question_id = $2",
            tracking_user_id,
            question_id,
        )
        is_first_attempt = (prior_count == 0)

    # Fetch question with lesson context
    q_row = await get_question_with_lesson(db, question_id)
    if q_row is None:
        raise AppError(*QUESTION_NOT_FOUND)

    lesson_id = str(q_row["lesson_id"])
    lesson_section_id = str(q_row["lesson_section_id"])

    if q_row["lesson_status"] != "approved":
        raise AppError(*LESSON_NOT_APPROVED)

    if is_guest:
        if not q_row["is_guest_accessible"]:
            raise AppError(*GUEST_ACCESS_DENIED)
    elif real_user_id:
        progress = await get_lesson_progress_for_user(db, real_user_id, lesson_id)
        if progress is None and q_row["lesson_order"] > 1:
            raise AppError(*LESSON_LOCKED)

    attempt_id = str(new_uuid())

    # Score — pronunciation types call Gemini; all others use local scoring
    pronunciation_ai_feedback: dict | None = None
    if q_row["type"] in PRONUNCIATION_TYPES:
        result, pronunciation_ai_feedback = await _score_pronunciation(
            user, q_row, body.response, attempt_id
        )
    else:
        result = scoring_service.score(
            q_row["type"],
            dict(q_row["payload"]),
            body.response,
        )

    # Guests: attempt stored with guest_token, not user_id
    attempt_user_id = None if is_guest else real_user_id
    attempt_guest_token = x_guest_token if is_guest else None

    # For pronunciation, store a sanitised response (strip large base64 before persisting)
    stored_response = dict(body.response)
    if q_row["type"] in PRONUNCIATION_TYPES:
        stored_response.pop("audio_data_base64", None)

    async with db.transaction():
        await insert_attempt(
            db,
            attempt_id=attempt_id,
            user_id=attempt_user_id,
            guest_token=attempt_guest_token,
            question_id=question_id,
            lesson_section_id=lesson_section_id,
            lesson_id=lesson_id,
            response=stored_response,
            score_fraction=str(result.score_fraction),
            score_numerator=result.score_numerator,
            score_denominator=result.score_denominator,
            xp_awarded=0,  # updated below
            ai_feedback=pronunciation_ai_feedback,
        )

        xp_awarded = 0
        streak_result = StreakResult(status=None, current=0, longest=0, milestone_bonus=0)
        lesson_result: LessonResult | None = None

        if tracking_user_id:
            if q_row["type"] in PRONUNCIATION_TYPES:
                # Proportional XP on first attempt — bypass award_for_question which
                # requires numerator == denominator (never true for pronunciation).
                xp_awarded = round(int(q_row["xp_value"]) * float(result.score_fraction)) if is_first_attempt else 0
                if xp_awarded > 0:
                    await xp_service.award(
                        db,
                        user_id=tracking_user_id,
                        action_type="question_attempt",
                        xp_delta=xp_awarded,
                        reference_id=attempt_id,
                        reference_type="attempt",
                    )
            else:
                xp_awarded = await xp_service.award_for_question(
                    db,
                    user_id=tracking_user_id,
                    attempt_id=attempt_id,
                    question_xp_value=q_row["xp_value"] if is_first_attempt else 0,
                    score_numerator=result.score_numerator,
                    score_denominator=result.score_denominator,
                )
            await db.execute(
                "UPDATE attempt SET xp_awarded = $1 WHERE id = $2",
                xp_awarded,
                attempt_id,
            )

            prog = await progress_service.record_attempt(
                db, tracking_user_id, lesson_id, q_row["purpose"]
            )
            if prog.lesson_complete:
                lesson_result = LessonResult(
                    lesson_complete=True,
                    next_lesson_id=prog.next_lesson_id,
                    xp_from_lesson=prog.xp_from_lesson,
                )

            if q_row["vocabulary_word_id"]:
                await mastery_service.record(
                    db,
                    user_id=tracking_user_id,
                    vocabulary_word_id=str(q_row["vocabulary_word_id"]),
                    is_correct=result.is_correct,
                )

            if q_row["purpose"] == "assessment":
                sr = await streak_service.record_qualifying_activity(db, tracking_user_id)
                streak_result = StreakResult(
                    status=sr.status,
                    current=sr.streak_current,
                    longest=sr.streak_longest,
                    milestone_bonus=sr.milestone_bonus,
                )

    # Daily goal hooks — only for authenticated (non-guest) users with a level
    if tracking_user_id and not is_guest and user and user["current_level_id"]:
        level_id = str(user["current_level_id"])

        await daily_goal_service.record_activity(
            db, tracking_user_id, "questions_answered", level_id=level_id
        )
        if result.is_correct:
            await daily_goal_service.record_activity(
                db, tracking_user_id, "correct_answers", level_id=level_id
            )
        if q_row["purpose"] == "assessment":
            await daily_goal_service.record_activity(
                db, tracking_user_id, "assessment_questions_answered", level_id=level_id
            )
            # Fire lesson_sections_completed when this attempt completes a section.
            # "Completes" = all assessment questions in the section have been attempted
            # today (day boundary in SLST), and this is the first attempt today for
            # this specific question (prevents re-firing on re-attempts).
            prior_today = await db.fetchval(
                """
                SELECT COUNT(*) FROM attempt
                WHERE user_id = $1::uuid AND question_id = $2::uuid
                  AND (created_at AT TIME ZONE 'Asia/Colombo')::date
                      = (now() AT TIME ZONE 'Asia/Colombo')::date
                """,
                tracking_user_id,
                question_id,
            )
            if prior_today == 1:  # only the attempt just inserted
                total_in_section = await db.fetchval(
                    """
                    SELECT COUNT(*) FROM question
                    WHERE lesson_section_id = $1::uuid
                      AND purpose = 'assessment'
                    """,
                    lesson_section_id,
                )
                attempted_today = await db.fetchval(
                    """
                    SELECT COUNT(DISTINCT a.question_id)
                    FROM attempt a
                    JOIN question q ON q.id = a.question_id
                    WHERE a.user_id = $1::uuid
                      AND q.lesson_section_id = $2::uuid
                      AND q.purpose = 'assessment'
                      AND (a.created_at AT TIME ZONE 'Asia/Colombo')::date
                          = (now() AT TIME ZONE 'Asia/Colombo')::date
                    """,
                    tracking_user_id,
                    lesson_section_id,
                )
                if attempted_today == total_in_section:
                    await daily_goal_service.record_activity(
                        db, tracking_user_id, "lesson_sections_completed", level_id=level_id
                    )

        if lesson_result and lesson_result.lesson_complete:
            await daily_goal_service.record_activity(
                db, tracking_user_id, "lessons_completed", level_id=level_id
            )

    # Achievements: evaluate against fresh state now that XP/streak/progress are
    # committed. Registered users only; an unlock failure must never break the
    # attempt response.
    newly_unlocked: list = []
    if user is not None:
        try:
            fresh_user = await db.fetchrow(
                'SELECT * FROM "user" WHERE id = $1::uuid', str(user["id"])
            )
            if fresh_user is not None:
                newly_unlocked = await achievement_service.check_and_unlock(
                    db, fresh_user
                )
        except Exception:
            import logging
            logging.getLogger(__name__).exception(
                "achievement check failed for user=%s", user["id"]
            )

    if pronunciation_ai_feedback:
        summary = pronunciation_ai_feedback.get("summary", "")
        feedback = AttemptFeedback(
            correct=summary if float(result.score_fraction) >= 0.5 else None,
            incorrect=summary if float(result.score_fraction) < 0.5 else None,
        )
    else:
        feedback_data = dict(q_row["payload"]).get("feedback", {})
        feedback = AttemptFeedback(
            correct=feedback_data.get("correct") if isinstance(feedback_data, dict) else None,
            incorrect=feedback_data.get("incorrect") if isinstance(feedback_data, dict) else None,
        )

    pronunciation_detail: PronunciationDetail | None = None
    if pronunciation_ai_feedback:
        pronunciation_detail = PronunciationDetail(
            accuracy=pronunciation_ai_feedback["accuracy"],
            clarity=pronunciation_ai_feedback["clarity"],
            fluency=pronunciation_ai_feedback["fluency"],
            grade=pronunciation_ai_feedback["grade"],
            feedback=pronunciation_ai_feedback["feedback"],
        )

    return AttemptResponse(
        attempt_id=attempt_id,
        score_fraction=float(result.score_fraction),
        is_correct=result.is_correct,
        score_numerator=result.score_numerator,
        score_denominator=result.score_denominator,
        xp_awarded=xp_awarded,
        feedback=feedback,
        lesson_result=lesson_result,
        streak=streak_result,
        pronunciation_detail=pronunciation_detail,
        newly_unlocked_achievements=[
            UnlockedAchievement(
                id=ach["id"],
                name=ach["name"],
                xp_reward=ach["xp_reward"],
                condition_type=ach["condition_type"],
            )
            for ach in newly_unlocked
        ],
    )


@router.get("/api/v1/users/me/xp-summary", response_model=XPSummaryResponse)
async def get_xp_summary(
    limit: int = 20,
    cursor: str | None = None,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> XPSummaryResponse:
    rows = await get_xp_ledger_for_user(db, str(user["id"]), limit=limit + 1, cursor=cursor)
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = str(rows[-1]["id"]) if has_more else None

    return XPSummaryResponse(
        xp_total=user["xp_total"],
        data=[
            XPLedgerEntry(
                action_type=r["action_type"],
                xp_delta=r["xp_delta"],
                reference_type=r["reference_type"],
                reference_id=r["reference_id"],
                awarded_at=r["awarded_at"].isoformat(),
            )
            for r in rows
        ],
        cursor=next_cursor,
        has_more=has_more,
    )


@router.get("/api/v1/users/me/streak", response_model=StreakResponse)
async def get_streak(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> StreakResponse:
    state = await get_streak_state(db, str(user["id"]))
    milestones = await get_streak_milestones(db)

    current = state["streak_current"] if state else 0
    next_days: int | None = None
    next_bonus: int | None = None
    for m in milestones:
        if m["days"] > current:
            next_days = m["days"]
            next_bonus = m["bonus_xp"]
            break

    last_date = None
    if state and state["streak_last_activity_date"]:
        last_date = str(state["streak_last_activity_date"])

    return StreakResponse(
        streak_current=current,
        streak_longest=state["streak_longest"] if state else 0,
        streak_last_activity_date=last_date,
        next_milestone_days=next_days,
        next_milestone_bonus_xp=next_bonus,
    )
