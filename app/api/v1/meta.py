"""App-meta endpoints — feature flags + mobile version gate.

Both are intentionally public (no auth): feature flags must be readable
before login (pre-auth screens gate on them too), and the version gate has
to run before a stale sideloaded APK can even reach a sign-in screen.
"""

import asyncpg
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.db.pool import get_db
from app.schemas.meta import AppMetaResponse
from app.services import feature_flag_service

router = APIRouter(prefix="/api/v1", tags=["meta"])


@router.get("/feature-flags", response_model=dict[str, bool])
async def get_feature_flags(
    db: asyncpg.Connection = Depends(get_db),
) -> dict[str, bool]:
    return await feature_flag_service.get_flags(db)


@router.get("/meta", response_model=AppMetaResponse)
async def get_meta() -> AppMetaResponse:
    return AppMetaResponse(
        min_mobile_version=settings.min_mobile_version,
        latest_mobile_version=settings.latest_mobile_version,
    )
