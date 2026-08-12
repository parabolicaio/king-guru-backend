import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.pool import lifespan

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=0.1 if settings.is_production else 0.0,
        send_default_pii=False,
    )

app = FastAPI(
    title="KingGuru API",
    version="0.1.0",
    # docs_url="/docs" if not settings.is_production else None,
    # redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Error envelope — convert all HTTPExceptions to KG format
# { "error": { "code": "...", "message": "...", "details": {} } }
# ---------------------------------------------------------------------------

from fastapi import HTTPException  # noqa: E402


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict) and "code" in detail:
        body = {"error": detail}
    else:
        body = {"error": {"code": "ERROR", "message": str(detail), "details": {}}}
    return JSONResponse(status_code=exc.status_code, content=body)


# ---------------------------------------------------------------------------
# Routers — Learner
# ---------------------------------------------------------------------------

from app.api.v1 import auth as auth_router               # noqa: E402
from app.api.v1 import hooks as hooks_router             # noqa: E402
from app.api.v1 import users as users_router             # noqa: E402
from app.api.v1 import levels as levels_router           # noqa: E402
from app.api.v1 import placement as placement_router     # noqa: E402
from app.api.v1 import lessons as lessons_router         # noqa: E402
from app.api.v1 import progress as progress_router       # noqa: E402
from app.api.v1 import attempts as attempts_router       # noqa: E402
from app.api.v1 import vocabulary as vocabulary_router   # noqa: E402
from app.api.v1 import notifications as notifications_router  # noqa: E402
from app.api.v1 import achievements as achievements_router    # noqa: E402
from app.api.v1 import leaderboard as leaderboard_router      # noqa: E402
from app.api.v1 import daily_essay as daily_essay_router      # noqa: E402
from app.api.v1 import daily_goal as daily_goal_router        # noqa: E402
from app.api.v1 import meta as meta_router                    # noqa: E402

app.include_router(auth_router.router)
app.include_router(meta_router.router)
app.include_router(hooks_router.router)
app.include_router(users_router.router)
app.include_router(levels_router.router)
app.include_router(placement_router.router)
app.include_router(lessons_router.router)
app.include_router(progress_router.router)
app.include_router(attempts_router.router)
app.include_router(vocabulary_router.router)
app.include_router(notifications_router.router)
app.include_router(achievements_router.router)
app.include_router(leaderboard_router.router)
app.include_router(daily_essay_router.router)
app.include_router(daily_goal_router.router)

# ---------------------------------------------------------------------------
# Routers — Admin (B7 + B8)
# ---------------------------------------------------------------------------

from app.api.v1.admin import lessons as admin_lessons_router          # noqa: E402
from app.api.v1.admin import sections as admin_sections_router        # noqa: E402
from app.api.v1.admin import blocks as admin_blocks_router            # noqa: E402
from app.api.v1.admin import questions as admin_questions_router      # noqa: E402
from app.api.v1.admin import vocabulary_words as admin_vocab_router   # noqa: E402
from app.api.v1.admin import users as admin_users_router              # noqa: E402
from app.api.v1 import content_reviews as content_reviews_router      # noqa: E402

app.include_router(admin_lessons_router.router)
app.include_router(admin_sections_router.router)
app.include_router(admin_blocks_router.router)
app.include_router(admin_questions_router.router)
app.include_router(admin_vocab_router.router)
app.include_router(admin_users_router.router)
app.include_router(content_reviews_router.router)


# ---------------------------------------------------------------------------
# Infra
# ---------------------------------------------------------------------------

@app.get("/health", tags=["infra"])
async def health() -> dict[str, str]:
    """Smoke-test endpoint."""
    return {"status": "ok"}
