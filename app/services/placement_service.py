"""Placement service — heuristic scoring + level selection."""

from dataclasses import dataclass, field
from uuid import UUID

import asyncpg

from app.core.errors import AppError, LEVEL_NOT_FOUND, LEVEL_NOT_ACTIVE
from app.db.queries.levels import get_level_by_id
from app.db.queries.placement import (
    get_lesson_1_for_level,
    get_placement_questions,
    get_placement_scoring_rules,
    get_populated_level_ids,
    set_user_level_and_placement,
    get_lesson_progress,
    create_lesson_progress,
)
from app.db.utils import new_uuid
from app.schemas.placement import PlacementAnswerDetail, PlacementSkillBreakdown
from app.services import notification as notification_service
from app.services import scoring as scoring_service


@dataclass
class PlacementScore:
    score_percent: float
    correct_count: int
    total_count: int
    recommended_level_id: str | None
    recommended_level_code: str
    xp_awarded: int
    answers: list[PlacementAnswerDetail] = field(default_factory=list)
    skill_breakdown: list[PlacementSkillBreakdown] = field(default_factory=list)


def _extract_correct_answer(q_type: str, payload: dict) -> dict:
    """Return the answer-key portion of a question payload for display on the results screen."""
    if q_type in ("mcq_single", "mcq_long_short_form"):
        correct_id = payload.get("correct_option_id")
        options = {o["id"]: o.get("text", "") for o in payload.get("options", [])}
        return {"correct_option_id": correct_id, "correct_text": options.get(correct_id)}
    if q_type == "true_false":
        return {"correct_answer": payload.get("correct_answer")}
    if q_type in ("fill_blank_typed", "fill_blank_options"):
        return {"accepted_answers": payload.get("accepted_answers", [])}
    if q_type == "match_pairs":
        return {"pairs": payload.get("pairs", [])}
    if q_type in ("order_events", "sentence_builder"):
        return {"correct_order": payload.get("items", payload.get("words", []))}
    if q_type == "correct_mistake":
        return {"accepted_corrections": payload.get("accepted_corrections", [])}
    return payload


async def score_answers(
    db: asyncpg.Connection,
    answers: list[dict],
    tracking_user_id: str | None = None,
) -> PlacementScore:
    """Score placement answers and optionally award XP.

    answers:          list of {"question_id": UUID, "response": dict}
    tracking_user_id: guest or real user UUID — XP is awarded here if provided.
                      Pass None for fully anonymous callers (no XP persisted).
    """
    questions = await get_placement_questions(db)
    rules = await get_placement_scoring_rules(db)
    populated_level_ids = await get_populated_level_ids(db)

    question_map = {str(q["id"]): q for q in questions}

    answer_details: list[PlacementAnswerDetail] = []
    skill_totals: dict[str, dict] = {}  # skill_category → {correct, total}

    correct_count = 0
    scored = 0
    total_xp = 0

    for answer in answers:
        qid = str(answer["question_id"])
        q = question_map.get(qid)
        if q is None:
            continue

        result = scoring_service.score(q["type"], dict(q["payload"]), answer["response"])
        is_correct = result.is_correct
        xp_for_q = int(q["xp_value"]) if is_correct else 0

        if is_correct:
            correct_count += 1
            total_xp += xp_for_q
        scored += 1

        skill = q["skill_category"]  # may be None
        if skill:
            if skill not in skill_totals:
                skill_totals[skill] = {"correct": 0, "total": 0}
            skill_totals[skill]["total"] += 1
            if is_correct:
                skill_totals[skill]["correct"] += 1

        answer_details.append(
            PlacementAnswerDetail(
                question_id=UUID(qid),
                prompt_text=q["prompt_text"],
                skill_category=skill,
                difficulty=q["difficulty"],
                user_response=answer["response"],
                correct_answer=_extract_correct_answer(q["type"], dict(q["payload"])),
                is_correct=is_correct,
                xp_awarded=xp_for_q,
            )
        )

    total_count = scored or len(questions)
    score_percent = (correct_count / total_count * 100.0) if total_count > 0 else 0.0

    # Skill breakdown list
    skill_breakdown = [
        PlacementSkillBreakdown(
            skill_category=sk,
            correct=vals["correct"],
            total=vals["total"],
            accuracy=round(vals["correct"] / vals["total"] * 100.0, 1) if vals["total"] > 0 else 0.0,
        )
        for sk, vals in skill_totals.items()
    ]

    # Recommended level from placement_scoring_rule, capped at the highest
    # level that actually has lessons (recommending empty content dead-ends
    # the user — Task #17). Data-driven via populated_level_ids, so the cap
    # self-removes as levels get content; no hardcoded level list here.
    recommended_level_id: str | None = None
    recommended_level_code: str = "beginner"

    for rule in rules:
        if rule["min_percent"] <= score_percent <= rule["max_percent"]:
            recommended_level_id = str(rule["recommended_level_id"])
            break

    if recommended_level_id is None and rules:
        recommended_level_id = str(rules[0]["recommended_level_id"])

    if recommended_level_id is not None and recommended_level_id not in populated_level_ids:
        # Walk down through every rule the score still qualifies for
        # (min_percent <= score_percent), highest first, and take the first
        # one backed by actual lesson content.
        qualifying = sorted(
            (r for r in rules if r["min_percent"] <= score_percent),
            key=lambda r: r["min_percent"],
            reverse=True,
        )
        for rule in qualifying:
            candidate = str(rule["recommended_level_id"])
            if candidate in populated_level_ids:
                recommended_level_id = candidate
                break

    if recommended_level_id:
        level = await get_level_by_id(db, recommended_level_id)
        if level:
            recommended_level_code = level["code"]

    # Award XP — written inside the caller's connection (no explicit transaction needed
    # for a simple ledger insert + counter increment)
    if total_xp > 0 and tracking_user_id:
        from app.services import xp as xp_service
        await xp_service.award(
            db,
            user_id=tracking_user_id,
            action_type="placement_question",
            xp_delta=total_xp,
            reference_id=None,
            reference_type="placement",
        )

    return PlacementScore(
        score_percent=round(score_percent, 2),
        correct_count=correct_count,
        total_count=total_count,
        recommended_level_id=recommended_level_id,
        recommended_level_code=recommended_level_code,
        xp_awarded=total_xp,
        answers=answer_details,
        skill_breakdown=skill_breakdown,
    )


async def choose_level(
    db: asyncpg.Connection,
    user_id: str,
    level_id: str,
) -> asyncpg.Record:
    """Persist chosen level and seed lesson_progress for lesson 1.

    Idempotent — calling again with a different level_id updates it.
    Works for both real users and guest users (called with the guest row's UUID).
    """
    level = await get_level_by_id(db, level_id)
    if level is None:
        raise AppError(*LEVEL_NOT_FOUND)
    if not level["is_active"]:
        raise AppError(*LEVEL_NOT_ACTIVE)

    row = await set_user_level_and_placement(db, user_id, level_id)

    await notification_service.create(
        db,
        user_id=user_id,
        notif_type="placement_complete",
        title="Placement complete!",
        body=f"You've been placed at {level['name']}.",
        reference_id=level_id,
        reference_type="level",
    )

    lesson_1 = await get_lesson_1_for_level(db, level_id)
    if lesson_1 is not None:
        existing = await get_lesson_progress(db, user_id, str(lesson_1["id"]))
        if existing is None:
            await create_lesson_progress(
                db,
                progress_id=str(new_uuid()),
                user_id=user_id,
                lesson_id=str(lesson_1["id"]),
                status="not_started",
            )

    return row
