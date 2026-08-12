"""Shared pytest fixtures for Slice 1 tests.

Environment variables are set before any app import so pydantic-settings
doesn't raise ValidationError on missing required fields.
"""

import os
import time
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

# ---------------------------------------------------------------------------
# Inject test env vars BEFORE any app module is imported.
# These are dummy values — no real DB or Supabase connection is made in tests.
# ---------------------------------------------------------------------------
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
os.environ.setdefault("SUPABASE_JWT_SECRET", TEST_JWT_SECRET := "test-secret-kingguru-slice-1")
os.environ.setdefault("CDN_BASE_URL", "http://cdn.test")

import jwt  # noqa: E402
import pytest  # noqa: E402
import pytest_asyncio  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.main import app  # noqa: E402
from app.db.pool import get_db  # noqa: E402


def make_token(
    sub: str = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    email: str | None = "test@example.com",
    phone: str | None = None,
    admin_role: str | None = None,
    expired: bool = False,
    bad_signature: bool = False,
    omit_sub: bool = False,
    secret: str = TEST_JWT_SECRET,
) -> str:
    """Build a signed JWT for testing."""
    now = int(time.time())
    payload: dict = {
        "aud": "authenticated",
        "iat": now,
        "exp": now - 10 if expired else now + 3600,
        "app_metadata": {},
    }
    if not omit_sub:
        payload["sub"] = sub
    if email:
        payload["email"] = email
    if phone:
        payload["phone"] = phone
    if admin_role:
        payload["app_metadata"]["admin_role"] = admin_role

    sign_secret = "wrong-secret" if bad_signature else secret
    return jwt.encode(payload, sign_secret, algorithm="HS256")


# ---------------------------------------------------------------------------
# Mock DB connection fixture
# ---------------------------------------------------------------------------

def _txn_cm() -> MagicMock:
    """A stand-in for `conn.transaction()` usable as `async with`.

    __aexit__ returns False so exceptions propagate (a truthy value would
    silently swallow errors the tests assert on).
    """
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=cm)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


@pytest.fixture
def mock_conn() -> AsyncMock:
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(return_value=None)
    conn.execute = AsyncMock(return_value=None)
    conn.fetch = AsyncMock(return_value=[])
    # Fresh async-context-manager per call so `async with conn.transaction():`
    # works in service code (user_service, attempts, …).
    conn.transaction = MagicMock(side_effect=lambda *a, **k: _txn_cm())
    return conn


@pytest.fixture
def test_client(mock_conn: AsyncMock) -> TestClient:
    async def _override_get_db():
        yield mock_conn

    app.dependency_overrides[get_db] = _override_get_db
    client = TestClient(app, raise_server_exceptions=False)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(mock_conn: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    async def _override_get_db():
        yield mock_conn

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()
