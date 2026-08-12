from fastapi import APIRouter, Depends, Response

import asyncpg

from app.core.config import settings
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.users import complete_onboarding, update_user_profile
from app.schemas.users import (
    OnboardingRequest,
    OnboardingResponse,
    UpdateProfileRequest,
    UserProfile,
)
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def _row_to_profile(row: asyncpg.Record) -> UserProfile:
    return UserProfile(
        id=str(row["id"]),
        email=row["email"],
        phone=row["phone"],
        full_name=row["full_name"],
        display_name=row["display_name"],
        avatar_url=settings.build_cdn_url(row["avatar_url"]),
        age_group=row["age_group"],
        role_tag=row["role_tag"],
        english_level=row["english_level"],
        language_preference=row["language_preference"],
        admin_role=row["admin_role"],
        subscription_tier=row["subscription_tier"],
        xp_total=row["xp_total"],
        streak_current=row["streak_current"],
        streak_longest=row["streak_longest"],
        onboarding_completed=row["onboarding_completed_at"] is not None,
        placement_completed=row["placement_completed_at"] is not None,
        current_level_id=row["current_level_id"],
        current_level_name=row["current_level_name"],
        deleted_at=row["deleted_at"],
        created_at=row["created_at"],
    )


@router.get("/me", response_model=UserProfile)
async def get_me(
    row: asyncpg.Record = Depends(get_current_user),
) -> UserProfile:
    return _row_to_profile(row)


@router.patch("/me", response_model=UserProfile)
async def update_me(
    body: UpdateProfileRequest,
    row: asyncpg.Record = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db),
) -> UserProfile:
    updated = await update_user_profile(
        conn,
        str(row["id"]),
        display_name=body.display_name,
        avatar_url=body.avatar_url,
        age_group=body.age_group,
        role_tag=body.role_tag,
        english_level=body.english_level,
        language_preference=body.language_preference,
    )
    return _row_to_profile(updated)


@router.delete("/me", status_code=204)
async def delete_me(
    row: asyncpg.Record = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db),
) -> Response:
    await user_service.delete_account(
        conn,
        user_id=str(row["id"]),
        supabase_uid=str(row["supabase_uid"]),
    )
    return Response(status_code=204)


@router.post("/me/onboarding", response_model=OnboardingResponse)
async def complete_onboarding_endpoint(
    body: OnboardingRequest,
    row: asyncpg.Record = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db),
) -> OnboardingResponse:
    updated = await complete_onboarding(
        conn,
        str(row["id"]),
        full_name=body.full_name,
        age_group=body.age_group,
        role_tag=body.role_tag,
        english_level=body.english_level,
        language_preference=body.language_preference,
    )
    return OnboardingResponse(
        onboarding_completed_at=updated["onboarding_completed_at"]
    )
