import random
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel

import asyncpg

from app.core.errors import AppError, UNAUTHORIZED
from app.core.security import get_optional_user
from app.db.pool import get_db
from app.db.queries.placement import get_placement_questions
from app.schemas.placement import (
    PlacementChooseLevelRequest,
    PlacementChooseLevelResponse,
    PlacementQuestion,
    PlacementQuestionsResponse,
    PlacementSubmitRequest,
    PlacementSubmitResponse,
)
from app.services import placement_service
from app.core.config import settings

router = APIRouter(prefix="/api/v1/placement", tags=["placement"])


def _build_payload_urls(payload: dict) -> dict:
    """Replace raw Supabase Storage paths with CDN URLs inside a payload dict.

    Handles:
      - payload.prompt_image_url  (Scenario A — image as stimulus)
      - payload.options[].image_url  (Scenario B — image as options)

    Questions without image fields pass through unchanged.
    """
    result = dict(payload)

    if result.get("prompt_image_url"):
        result["prompt_image_url"] = settings.build_cdn_url(result["prompt_image_url"])

    if "options" in result and isinstance(result["options"], list):
        result["options"] = [
            {**opt, "image_url": settings.build_cdn_url(opt["image_url"])}
            if opt.get("image_url")
            else opt
            for opt in result["options"]
        ]

    return result

_FACTS: list[str] = [
    "Sri Lanka has one of the highest literacy rates in South Asia — over 92%.",
    "English is an official language of Sri Lanka alongside Sinhala and Tamil.",
    "The word 'serendipity' comes from Serendib, the old Arabic name for Sri Lanka.",
    "Sri Lanka was the first country in the world to elect a female head of government.",
    "Cinnamon was first discovered by the world through Sri Lanka's spice trade.",
    "Sri Lanka is home to eight UNESCO World Heritage Sites.",
    "The island has been inhabited for at least 125,000 years.",
    "Tea was introduced to Sri Lanka by the British in 1867 and it's now the world's fourth-largest producer.",
    "Sri Lanka's flag features a lion holding a sword — one of the oldest national flags still in use.",
    "Adam's Peak (Sri Pada) is climbed by thousands of pilgrims each year; the summit has a footprint sacred to four religions.",
    "English has more words than any other language — the Oxford Dictionary lists over 170,000 words.",
    "About 1.5 billion people speak English as a first or second language worldwide.",
    "Shakespeare invented over 1,700 words still used in English today.",
    "The most common letter in English is 'E'; the least common is 'Z'.",
    "The sentence 'The quick brown fox jumps over the lazy dog' uses every letter of the alphabet.",
]


class FactResponse(BaseModel):
    fact: str


@router.get("/fact", response_model=FactResponse)
async def get_random_fact() -> FactResponse:
    """Return a random educational fact shown on the placement results screen."""
    return FactResponse(fact=random.choice(_FACTS))


async def _resolve_tracking_id(
    user: asyncpg.Record | None,
    x_guest_token: str | None,
    db: asyncpg.Connection,
) -> str | None:
    """Return the UUID to attribute XP/progress to, or None if fully anonymous."""
    if user is not None:
        return str(user["id"])
    if x_guest_token:
        from app.services.guest_service import ensure_guest_user
        guest = await ensure_guest_user(db, x_guest_token)
        return str(guest["id"])
    return None


@router.get("/questions", response_model=PlacementQuestionsResponse)
async def get_questions(
    db: asyncpg.Connection = Depends(get_db),
) -> PlacementQuestionsResponse:
    """Return placement questions. Public — no auth required."""
    rows = await get_placement_questions(db)
    return PlacementQuestionsResponse(
        questions=[
            PlacementQuestion(
                id=row["id"],
                type=row["type"],
                prompt_text=row["prompt_text"],
                payload=_build_payload_urls(dict(row["payload"])),
                difficulty=row["difficulty"],
                skill_category=row["skill_category"],
                xp_value=row["xp_value"],
                display_order=row["display_order"],
                translations=dict(row["translations"] or {}),
            )
            for row in rows
        ]
    )


@router.post("/submit", response_model=PlacementSubmitResponse)
async def submit_placement(
    body: PlacementSubmitRequest,
    x_guest_token: str | None = Header(default=None, alias="X-Guest-Token"),
    user: asyncpg.Record | None = Depends(get_optional_user),
    db: asyncpg.Connection = Depends(get_db),
) -> PlacementSubmitResponse:
    """Score placement answers and return full breakdown with XP.

    Works pre-auth (via X-Guest-Token) and post-auth (via Bearer JWT).
    XP is awarded to whoever is identified; pass neither for anonymous scoring.
    """
    tracking_id = await _resolve_tracking_id(user, x_guest_token, db)

    result = await placement_service.score_answers(
        db,
        [{"question_id": str(a.question_id), "response": a.response} for a in body.answers],
        tracking_user_id=tracking_id,
    )

    if body.confirm_level_id and tracking_id:
        await placement_service.choose_level(db, tracking_id, body.confirm_level_id)

    from uuid import UUID as _UUID
    return PlacementSubmitResponse(
        score_percent=result.score_percent,
        accuracy=result.score_percent,
        recommended_level_id=_UUID(result.recommended_level_id) if result.recommended_level_id else None,
        recommended_level=result.recommended_level_code,
        correct_count=result.correct_count,
        total_count=result.total_count,
        xp_awarded=result.xp_awarded,
        answers=result.answers,
        skill_breakdown=result.skill_breakdown,
    )


@router.post("/choose-level", response_model=PlacementChooseLevelResponse)
async def choose_level(
    body: PlacementChooseLevelRequest,
    x_guest_token: str | None = Header(default=None, alias="X-Guest-Token"),
    user: asyncpg.Record | None = Depends(get_optional_user),
    db: asyncpg.Connection = Depends(get_db),
) -> PlacementChooseLevelResponse:
    """Persist the user's chosen level.

    Works pre-auth (X-Guest-Token) so the level is stored on the guest row
    and transferred to the real account on sign-up via reattribute().
    Requires at least one of: valid JWT or X-Guest-Token.
    """
    tracking_id = await _resolve_tracking_id(user, x_guest_token, db)
    if tracking_id is None:
        raise AppError(*UNAUTHORIZED)

    row = await placement_service.choose_level(db, tracking_id, str(body.level_id))
    return PlacementChooseLevelResponse(
        current_level_id=row["current_level_id"],
        placement_completed_at=row["placement_completed_at"].isoformat(),
    )
