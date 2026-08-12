import json
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from fastapi import FastAPI, Request

from app.core.config import settings

_pool: asyncpg.Pool | None = None


async def _init_connection(conn: asyncpg.Connection) -> None:
    """Register JSON/JSONB codecs so asyncpg returns Python dicts/lists.

    Without this, asyncpg returns JSONB columns as raw strings, which causes
    dict() / list() calls downstream to iterate over characters instead of
    the decoded object.
    """
    await conn.set_type_codec(
        "jsonb",
        encoder=json.dumps,
        decoder=json.loads,
        schema="pg_catalog",
        format="text",
    )
    await conn.set_type_codec(
        "json",
        encoder=json.dumps,
        decoder=json.loads,
        schema="pg_catalog",
        format="text",
    )


async def get_pool() -> asyncpg.Pool:
    """Return the app-wide connection pool.

    Useful for background tasks that can't access the pool via the Request object.
    Raises RuntimeError if called before the app lifespan has started.
    """
    if _pool is None:
        raise RuntimeError("DB pool is not initialized — call inside a running app context")
    return _pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan — creates the asyncpg pool on startup, closes it on shutdown.

    Pool is stored on app.state.db_pool so get_db() can access it via the Request.
    Using lifespan (not @app.on_event) is the current FastAPI best practice.
    """
    global _pool
    pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=2,
        max_size=10,
        command_timeout=30,  # seconds; applies to individual queries
        init=_init_connection,
        # Required for Supabase/PgBouncer session pooler: disables prepared
        # statement caching so asyncpg uses simple-query protocol.  Without
        # this, set_type_codec's internal type-introspection query creates a
        # prepared statement whose name collides on the next pool init.
        statement_cache_size=0,
    )
    _pool = pool
    app.state.db_pool = pool
    yield
    await pool.close()
    _pool = None


async def get_db(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    """FastAPI dependency — acquires a connection from the pool for one request.

    Usage in endpoints:
        async def my_endpoint(conn: asyncpg.Connection = Depends(get_db)):
            rows = await conn.fetch("SELECT ...")

    The connection is released back to the pool after the response is sent,
    even if the handler raises an exception.
    """
    async with request.app.state.db_pool.acquire() as conn:
        yield conn
