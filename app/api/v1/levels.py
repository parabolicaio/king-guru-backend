from fastapi import APIRouter, Depends

import asyncpg

from app.core.config import settings
from app.db.pool import get_db
from app.db.queries.levels import get_all_active_levels
from app.schemas.levels import LevelResponse, LevelsListResponse

router = APIRouter(prefix="/api/v1/levels", tags=["levels"])


@router.get("", response_model=LevelsListResponse)
async def list_levels(
    db: asyncpg.Connection = Depends(get_db),
) -> LevelsListResponse:
    rows = await get_all_active_levels(db)
    return LevelsListResponse(
        levels=[
            LevelResponse(
                id=row["id"],
                code=row["code"],
                name=row["name"],
                description=row["description"],
                display_order=row["display_order"],
                daily_essay_enabled=row["daily_essay_enabled"],
                translations=dict(row["translations"] or {}),
                icon_url=settings.build_cdn_url(row["icon_url"]),
                topics=list(row["topics"] or []),
                guest_enabled=row["guest_enabled"],
                payment_required=row["payment_required"],
            )
            for row in rows
        ]
    )
