"""Daily Essay service — draft management, submission, and Gemini grading."""

import logging
from dataclasses import dataclass
from datetime import date
from zoneinfo import ZoneInfo

import asyncpg

from app.core.errors import AppError
from app.db.queries.daily_essay import (
    create_draft,
    create_submission,
    get_submission_for_today,
    get_today_prompt,
    promote_draft_to_submission,
    update_draft_text,
    update_submission_grade,
)

logger = logging.getLogger(__name__)

SLST = ZoneInfo("Asia/Colombo")

# GCSE-style grade scale
_GRADE_THRESHOLDS = [
    (90, "A+"),
    (80, "A"),
    (70, "B+"),
    (60, "B"),
    (50, "C+"),
    (40, "C"),
    (30, "D"),
    (0,  "F"),
]

ALREADY_SUBMITTED  = ("ESSAY_ALREADY_SUBMITTED",  "You have already submitted an essay today.", 409)
ESSAY_NOT_AVAILABLE = ("ESSAY_NOT_AVAILABLE", "Daily Essay is not available for your level.", 403)
NO_PROMPT_AVAILABLE = ("NO_PROMPT_AVAILABLE", "No essay prompt is available today.", 404)
DRAFT_AFTER_SUBMIT  = ("ESSAY_ALREADY_SUBMITTED",  "Cannot save a draft — today's essay is already submitted.", 409)

_LANGUAGE_NAMES = {"en": "English", "si": "Sinhala"}

# CEFR rubric per KingGuru level code.
# axis_max values must sum to 20 across all four axes.
# DB column mapping: score_content=task_completion, score_grammar=grammar,
#   score_vocabulary=vocabulary, score_suggestions=organization.
# Keyed by the 5 live level codes (Task #25 restructure renamed beginner_a->beginner,
# beginner_b->elementary). The grader looks these up by the user's current level code.
_CEFR_RUBRIC: dict[str, dict] = {
    "beginner": {
        "cefr": "A1",
        "axis_max": {"task_completion": 8, "grammar": 6, "vocabulary": 4, "organization": 2},
        "axis_labels": {
            "task_completion": "Task Completion",
            "grammar": "Grammar",
            "vocabulary": "Vocabulary",
            "organization": "Organization",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer address the prompt with relevant ideas? Simple ideas expressed clearly.",
            "grammar": "Correctness of basic sentence structures, verb forms, and punctuation.",
            "vocabulary": "Use of simple, familiar words and phrases; accurate spelling.",
            "organization": "Basic sequencing and paragraph structure; simple linking words.",
        },
    },
    "beginner_b": {
        "cefr": "A1/A2",
        "axis_max": {"task_completion": 7, "grammar": 5, "vocabulary": 5, "organization": 3},
        "axis_labels": {
            "task_completion": "Task Completion",
            "grammar": "Grammar",
            "vocabulary": "Vocabulary",
            "organization": "Organization",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer address the prompt with relevant ideas and some development?",
            "grammar": "Correctness of basic-to-simple sentence structures with occasional errors accepted.",
            "vocabulary": "Range and accuracy of everyday vocabulary; attempts to vary word choice.",
            "organization": "Basic paragraph structure with some use of linking words.",
        },
    },
    "elementary": {
        "cefr": "A2",
        "axis_max": {"task_completion": 7, "grammar": 5, "vocabulary": 5, "organization": 3},
        "axis_labels": {
            "task_completion": "Task Completion",
            "grammar": "Grammar",
            "vocabulary": "Vocabulary",
            "organization": "Organization",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer address the prompt clearly with relevant ideas and development?",
            "grammar": "Correctness of simple sentence structures; variety attempted.",
            "vocabulary": "Range and accuracy of everyday vocabulary.",
            "organization": "Paragraph structure and appropriate use of linking words.",
        },
    },
    "intermediate": {
        "cefr": "B1",
        "axis_max": {"task_completion": 6, "grammar": 5, "vocabulary": 5, "organization": 4},
        "axis_labels": {
            "task_completion": "Task Completion",
            "grammar": "Grammar",
            "vocabulary": "Vocabulary",
            "organization": "Organization & Coherence",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer address the prompt clearly with relevant ideas and some development of arguments?",
            "grammar": "Accurate use of a range of simple and complex structures.",
            "vocabulary": "Appropriate and varied vocabulary for the topic.",
            "organization": "Logical structure, paragraph cohesion, and effective linking devices.",
        },
    },
    "upper_intermediate": {
        "cefr": "B2",
        "axis_max": {"task_completion": 6, "grammar": 4, "vocabulary": 5, "organization": 5},
        "axis_labels": {
            "task_completion": "Task Completion & Development",
            "grammar": "Grammar",
            "vocabulary": "Vocabulary Range",
            "organization": "Organization & Cohesion",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer address the prompt with well-developed ideas and clear arguments?",
            "grammar": "Accurate and varied grammatical structures with few errors.",
            "vocabulary": "Precise, topic-specific vocabulary used accurately.",
            "organization": "Well-organized paragraphs with sophisticated linking and cohesive devices.",
        },
    },
    "advanced": {
        "cefr": "C1",
        "axis_max": {"task_completion": 5, "grammar": 4, "vocabulary": 5, "organization": 6},
        "axis_labels": {
            "task_completion": "Task Completion & Critical Thinking",
            "grammar": "Grammar Accuracy & Complexity",
            "vocabulary": "Vocabulary Range & Appropriacy",
            "organization": "Organization & Cohesion",
        },
        "axis_descriptions": {
            "task_completion": "Did the writer engage critically with the prompt, demonstrate nuanced thinking, and provide well-supported arguments?",
            "grammar": "Sophisticated and varied grammatical structures with minimal errors.",
            "vocabulary": "Precise, stylistically appropriate vocabulary demonstrating advanced command.",
            "organization": "Coherent structure, effective discourse markers, and sophisticated paragraph development.",
        },
    },
}

_DEFAULT_RUBRIC_KEY = "intermediate"


def today_slst() -> date:
    from datetime import datetime
    return datetime.now(SLST).date()


def _score_to_grade(score: float) -> str:
    for threshold, grade in _GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


async def _check_level_eligibility(db: asyncpg.Connection, user: asyncpg.Record) -> None:
    if user["current_level_id"]:
        level_row = await db.fetchrow(
            "SELECT daily_essay_enabled FROM level WHERE id = $1::uuid",
            str(user["current_level_id"]),
        )
        if level_row and not level_row["daily_essay_enabled"]:
            raise AppError(*ESSAY_NOT_AVAILABLE)


@dataclass
class EssayResult:
    submission_id: str
    grade: str
    xp_awarded: int
    score_grammar: float
    score_vocabulary: float
    score_content: float
    score_suggestions: float
    ai_feedback: dict
    ai_model: str


async def save_draft(
    db: asyncpg.Connection,
    user: asyncpg.Record,
    essay_prompt_id: str,
    draft_text: str,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Create or update a draft for today.

    - New draft → inserts row with is_draft=TRUE, submitted_at=NULL.
    - Existing draft → overwrites essay_text and feedback_language.
    - Already submitted today → raises DRAFT_AFTER_SUBMIT (409).
    """
    await _check_level_eligibility(db, user)

    today = today_slst()
    existing = await get_submission_for_today(db, str(user["id"]), today)

    if existing is not None and not existing["is_draft"]:
        logger.info(
            "daily_essay draft blocked user_id=%s submission_id=%s already submitted",
            user["id"],
            existing["id"],
        )
        raise AppError(*DRAFT_AFTER_SUBMIT)

    # Fetch prompt to snapshot its text
    prompt_row = await db.fetchrow(
        "SELECT * FROM essay_prompt WHERE id = $1::uuid AND is_active = TRUE",
        essay_prompt_id,
    )
    if prompt_row is None:
        logger.warning(
            "daily_essay draft prompt not found user_id=%s essay_prompt_id=%s",
            user["id"],
            essay_prompt_id,
        )
        raise AppError(*NO_PROMPT_AVAILABLE)

    if existing is not None:
        logger.debug(
            "daily_essay draft updating user_id=%s submission_id=%s chars=%d",
            user["id"],
            existing["id"],
            len(draft_text),
        )
        return await update_draft_text(
            db, str(existing["id"]), draft_text, feedback_language
        )

    logger.debug(
        "daily_essay draft creating user_id=%s essay_prompt_id=%s chars=%d date=%s",
        user["id"],
        essay_prompt_id,
        len(draft_text),
        today,
    )
    return await create_draft(
        db,
        user_id=str(user["id"]),
        essay_prompt_id=essay_prompt_id,
        prompt_text=prompt_row["prompt_text"],
        draft_text=draft_text,
        submission_date=today,
        feedback_language=feedback_language,
    )


async def submit(
    db: asyncpg.Connection,
    user: asyncpg.Record,
    essay_prompt_id: str,
    essay_text: str,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Submit today's essay for grading.

    - If a draft exists → promotes it (flips is_draft=FALSE, sets submitted_at).
    - If no prior row → creates a new submitted row directly.
    - If already submitted → raises ALREADY_SUBMITTED (409).
    """
    await _check_level_eligibility(db, user)

    today = today_slst()
    existing = await get_submission_for_today(db, str(user["id"]), today)

    if existing is not None and not existing["is_draft"]:
        logger.info(
            "daily_essay submit blocked user_id=%s submission_id=%s already submitted",
            user["id"],
            existing["id"],
        )
        raise AppError(*ALREADY_SUBMITTED)

    if existing is not None and existing["is_draft"]:
        logger.info(
            "daily_essay submit promoting draft user_id=%s submission_id=%s chars=%d",
            user["id"],
            existing["id"],
            len(essay_text),
        )
        return await promote_draft_to_submission(
            db, str(existing["id"]), essay_text, feedback_language
        )

    # No prior row — fetch prompt and create directly as submitted
    prompt_row = await db.fetchrow(
        "SELECT * FROM essay_prompt WHERE id = $1::uuid AND is_active = TRUE",
        essay_prompt_id,
    )
    if prompt_row is None:
        logger.warning(
            "daily_essay submit prompt not found user_id=%s essay_prompt_id=%s",
            user["id"],
            essay_prompt_id,
        )
        raise AppError(*NO_PROMPT_AVAILABLE)

    logger.info(
        "daily_essay submit creating user_id=%s essay_prompt_id=%s chars=%d date=%s",
        user["id"],
        essay_prompt_id,
        len(essay_text),
        today,
    )
    return await create_submission(
        db,
        user_id=str(user["id"]),
        essay_prompt_id=essay_prompt_id,
        prompt_text=prompt_row["prompt_text"],
        essay_text=essay_text,
        submission_date=today,
        feedback_language=feedback_language,
    )


async def grade_submission(
    db: asyncpg.Connection,
    submission_id: str,
    essay_text: str,
    prompt_text: str,
    feedback_language: str = "en",
    level_code: str | None = None,
) -> EssayResult:
    """Grade essay with Gemini using CEFR level-specific rubric.

    Called from a BackgroundTask after submission. On Gemini error, assigns F grade.
    DB column mapping: score_content=task_completion, score_grammar=grammar,
      score_vocabulary=vocabulary, score_suggestions=organization (raw marks, not 0-100).
    Overall score = (sum of raw marks / 20) * 100, mapped to GCSE grade.
    """
    logger.info(
        "daily_essay grade_submission started submission_id=%s essay_chars=%d level_code=%s feedback_language=%s",
        submission_id,
        len(essay_text),
        level_code,
        feedback_language,
    )
    rubric = _CEFR_RUBRIC.get(level_code or "", _CEFR_RUBRIC[_DEFAULT_RUBRIC_KEY])

    try:
        result = await _call_gemini(essay_text, prompt_text, feedback_language, rubric)
    except Exception as exc:
        logger.exception(
            "daily_essay gemini call failed submission_id=%s error=%s",
            submission_id,
            exc,
        )
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except Exception:
            pass
        result = _default_failed_grade(rubric)
        logger.warning(
            "daily_essay using fallback grade submission_id=%s model=%s",
            submission_id,
            result.get("model"),
        )

    grade = _score_to_grade(result["overall_score"])

    xp_map = {"A+": 60, "A": 50, "B+": 40, "B": 30, "C+": 20, "C": 15, "D": 5, "F": 0}
    xp_awarded = xp_map.get(grade, 0)

    logger.info(
        "daily_essay scores submission_id=%s task_completion=%s grammar=%s vocabulary=%s organization=%s overall=%.1f grade=%s xp=%d model=%s",
        submission_id,
        result.get("task_completion"),
        result.get("grammar"),
        result.get("vocabulary"),
        result.get("organization"),
        result.get("overall_score"),
        grade,
        xp_awarded,
        result.get("model"),
    )

    # Store axis metadata in ai_feedback so the frontend can display correctly.
    feedback_to_store = {
        **result["feedback"],
        "overall_summary": result.get("overall_summary", ""),
        "level_code": level_code,
        "axis_max_marks": rubric["axis_max"],
        "axis_labels": rubric["axis_labels"],
    }

    # score_content stores task_completion; score_suggestions stores organization.
    updated = await update_submission_grade(
        db,
        submission_id,
        grade=grade,
        score_grammar=result["grammar"],
        score_vocabulary=result["vocabulary"],
        score_content=result["task_completion"],
        score_suggestions=result["organization"],
        ai_feedback=feedback_to_store,
        ai_model=result.get("model", "gemini"),
        xp_awarded=xp_awarded,
    )

    user_id = str(updated["user_id"])

    if xp_awarded > 0:
        from app.services import xp as xp_service
        await xp_service.award(
            db,
            user_id=user_id,
            action_type="essay_submitted",
            xp_delta=xp_awarded,
            reference_id=submission_id,
            reference_type="essay",
        )
        logger.info(
            "daily_essay xp awarded submission_id=%s user_id=%s xp=%d",
            submission_id,
            user_id,
            xp_awarded,
        )

    from app.services import notification as notification_service
    await notification_service.create(
        db,
        user_id=user_id,
        notif_type="essay_graded",
        title="Your essay has been graded!",
        body=(
            f"You received a {grade} grade and {xp_awarded} XP."
            if xp_awarded > 0
            else f"You received a {grade} grade. Keep practicing!"
        ),
        reference_id=submission_id,
        reference_type="essay",
    )

    logger.info(
        "daily_essay grade persisted submission_id=%s grade=%s",
        submission_id,
        grade,
    )

    return EssayResult(
        submission_id=submission_id,
        grade=grade,
        xp_awarded=xp_awarded,
        score_grammar=result["grammar"],
        score_vocabulary=result["vocabulary"],
        score_content=result["task_completion"],
        score_suggestions=result["organization"],
        ai_feedback=feedback_to_store,
        ai_model=result.get("model", "gemini"),
    )


def _default_failed_grade(rubric: dict) -> dict:
    axis_max = rubric["axis_max"]
    return {
        "overall_score": 0,
        "task_completion": 0.0,
        "grammar": 0.0,
        "vocabulary": 0.0,
        "organization": 0.0,
        "overall_summary": "",
        "feedback": {
            "task_completion": [],
            "grammar": [],
            "vocabulary": [],
            "organization": [],
        },
        "model": "none",
        "axis_max": axis_max,
    }


async def _call_gemini(
    essay_text: str,
    prompt_text: str,
    feedback_language: str = "en",
    rubric: dict | None = None,
) -> dict:
    """Call Google Gemini to grade the essay using a CEFR level-specific rubric.

    Scores are raw marks (0 to axis max), not 0-100.
    Overall score = (sum of raw marks / 20) * 100.
    """
    from app.core.config import settings

    if not getattr(settings, "gemini_api_key", None):
        logger.warning("daily_essay gemini_api_key missing — using fallback grade")
        return _default_failed_grade(rubric or _CEFR_RUBRIC[_DEFAULT_RUBRIC_KEY])

    import httpx

    if rubric is None:
        rubric = _CEFR_RUBRIC[_DEFAULT_RUBRIC_KEY]

    axis_max = rubric["axis_max"]
    axis_desc = rubric["axis_descriptions"]
    cefr = rubric.get("cefr", "B1")
    lang_name = _LANGUAGE_NAMES.get(feedback_language, "English")

    model = settings.gemini_model
    logger.info(
        "daily_essay gemini request model=%s cefr=%s essay_chars=%d feedback_language=%s",
        model,
        cefr,
        len(essay_text),
        feedback_language,
    )

    max_tc = axis_max["task_completion"]
    max_g  = axis_max["grammar"]
    max_v  = axis_max["vocabulary"]
    max_o  = axis_max["organization"]

    system_prompt = (
        f"You are an English writing assessor grading an essay at CEFR {cefr} level.\n\n"
        f"Grade the following essay out of 20 marks total, distributed across 4 axes:\n"
        f"1. task_completion (max {max_tc} marks) — {axis_desc['task_completion']}\n"
        f"2. grammar (max {max_g} marks) — {axis_desc['grammar']}\n"
        f"3. vocabulary (max {max_v} marks) — {axis_desc['vocabulary']}\n"
        f"4. organization (max {max_o} marks) — {axis_desc['organization']}\n\n"
        f"Provide ALL text (overall_summary and every feedback item) in {lang_name} only.\n\n"
        "Respond ONLY with valid JSON matching this exact schema:\n"
        "{\n"
        f'  "task_completion": <integer 0-{max_tc}>,\n'
        f'  "grammar": <integer 0-{max_g}>,\n'
        f'  "vocabulary": <integer 0-{max_v}>,\n'
        f'  "organization": <integer 0-{max_o}>,\n'
        '  "overall_summary": "<1–2 sentence general comment on the essay overall>",\n'
        '  "feedback": {\n'
        '    "task_completion": ["<specific observation>", "<specific observation>"],\n'
        '    "grammar": ["<specific observation>", "<specific observation>"],\n'
        '    "vocabulary": ["<specific observation>", "<specific observation>"],\n'
        '    "organization": ["<specific observation>", "<specific observation>"]\n'
        "  }\n"
        "}\n\n"
        "Rules:\n"
        "- Each feedback array must contain 2–4 complete sentences.\n"
        "- Be specific and cite examples from the essay where possible.\n"
        f"- Marks must not exceed the stated maximum: task_completion≤{max_tc}, grammar≤{max_g}, vocabulary≤{max_v}, organization≤{max_o}.\n"
        "- Total marks across all axes must not exceed 20.\n"
        "- Do not include any text outside the JSON object."
    )
    user_msg = f"Prompt: {prompt_text}\n\nEssay:\n{essay_text}"

    gemini_url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            gemini_url,
            params={"key": settings.gemini_api_key},
            json={
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"parts": [{"text": user_msg}]}],
                "generationConfig": {"responseMimeType": "application/json"},
            },
        )
        if resp.is_error:
            body_preview = resp.text[:500] if resp.text else "(empty)"
            logger.error(
                "daily_essay gemini http error status=%s body=%s",
                resp.status_code,
                body_preview,
            )
            resp.raise_for_status()
        data = resp.json()

    import json

    try:
        candidates = data.get("candidates") or []
        if not candidates:
            logger.error(
                "daily_essay gemini empty candidates response_keys=%s",
                list(data.keys()),
            )
            raise ValueError("Gemini returned no candidates")

        text = candidates[0]["content"]["parts"][0]["text"]
        scores = json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        logger.error(
            "daily_essay gemini response parse failed error=%s response_keys=%s",
            exc,
            list(data.keys()) if isinstance(data, dict) else type(data).__name__,
        )
        raise

    required = ("task_completion", "grammar", "vocabulary", "organization")
    missing = [k for k in required if k not in scores]
    if missing:
        logger.error(
            "daily_essay gemini response missing fields=%s got_keys=%s",
            missing,
            list(scores.keys()),
        )
        raise ValueError(f"Gemini response missing fields: {missing}")

    # Clamp to stated maximums to guard against Gemini over-scoring
    scores["task_completion"] = min(float(scores["task_completion"]), max_tc)
    scores["grammar"]         = min(float(scores["grammar"]),         max_g)
    scores["vocabulary"]      = min(float(scores["vocabulary"]),      max_v)
    scores["organization"]    = min(float(scores["organization"]),    max_o)

    raw_total = (
        scores["task_completion"]
        + scores["grammar"]
        + scores["vocabulary"]
        + scores["organization"]
    )
    overall = raw_total / 20 * 100
    scores["overall_score"] = overall
    scores["model"] = model

    logger.info(
        "daily_essay gemini success task_completion=%s grammar=%s vocabulary=%s organization=%s raw_total=%.1f overall=%.1f",
        scores["task_completion"],
        scores["grammar"],
        scores["vocabulary"],
        scores["organization"],
        raw_total,
        overall,
    )
    return scores
