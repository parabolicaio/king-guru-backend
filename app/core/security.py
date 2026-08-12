"""JWT validation and FastAPI authentication dependencies."""

import logging
from dataclasses import dataclass
from functools import lru_cache

import asyncpg
import jwt
from jwt import PyJWKClient
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import AppError, FORBIDDEN, JWT_EXPIRED, JWT_INVALID, UNAUTHORIZED, USER_DELETED
from app.db.pool import get_db

_log = logging.getLogger(__name__)

_bearer = HTTPBearer(auto_error=False)

_SYMMETRIC_ALGS = {"HS256", "HS384", "HS512"}
_ALLOWED_ALGS   = {"HS256", "RS256", "ES256"}


@lru_cache
def _jwks_client(supabase_url: str) -> PyJWKClient:
    """Cached JWKS client — fetches Supabase public keys once per process."""
    return PyJWKClient(
        f"{supabase_url}/auth/v1/.well-known/jwks.json",
        cache_keys=True,
    )


@dataclass(frozen=True)
class TokenPayload:
    supabase_uid: str
    email: str | None
    phone: str | None
    admin_role: str | None
    provider: str | None


def decode_token(token: str, jwt_secret: str, supabase_url: str | None = None) -> TokenPayload:
    """Validate a Supabase JWT and return its key claims.

    Supports both HS256 (symmetric, legacy) and RS256/ES256 (asymmetric, newer
    Supabase projects).  RS256/ES256 tokens are verified via the JWKS endpoint;
    HS256 tokens are verified with the symmetric jwt_secret.

    Separated from the FastAPI dependency so it can be tested directly.
    Raises AppError (401) on any validation failure.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError as e:
        _log.error("JWT header decode failed: %s", e)
        raise AppError(*JWT_INVALID)

    alg = unverified_header.get("alg", "")
    if alg not in _ALLOWED_ALGS:
        _log.error("JWT rejected — disallowed alg: %s", alg)
        raise AppError(*JWT_INVALID)

    try:
        if alg in _SYMMETRIC_ALGS:
            payload: dict = jwt.decode(
                token,
                jwt_secret,
                algorithms=[alg],
                options={"verify_aud": False},
            )
        else:
            if not supabase_url:
                _log.error("JWT is %s but supabase_url not provided for JWKS lookup", alg)
                raise AppError(*JWT_INVALID)
            signing_key = _jwks_client(supabase_url).get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=[alg],
                options={"verify_aud": False},
            )
    except jwt.ExpiredSignatureError:
        raise AppError(*JWT_EXPIRED)
    except jwt.InvalidTokenError as e:
        _log.error("JWT decode failed: %s: %s", type(e).__name__, e)
        raise AppError(*JWT_INVALID)

    sub = payload.get("sub")
    if not sub:
        raise AppError(*JWT_INVALID)

    app_meta: dict = payload.get("app_metadata") or {}
    return TokenPayload(
        supabase_uid=sub,
        email=payload.get("email"),
        phone=payload.get("phone"),
        admin_role=app_meta.get("admin_role"),
        provider=app_meta.get("provider"),
    )


def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> TokenPayload:
    """Extract and validate the Bearer JWT.  Returns TokenPayload or raises 401."""
    if credentials is None:
        raise AppError(*UNAUTHORIZED)

    from app.core.config import settings

    return decode_token(
        credentials.credentials,
        settings.supabase_jwt_secret,
        settings.supabase_url,
    )


async def get_current_user(
    token: TokenPayload = Depends(get_token_payload),
    conn: asyncpg.Connection = Depends(get_db),
) -> asyncpg.Record:
    """Resolve the authenticated user row from the database."""
    from app.db.queries.users import get_user_by_supabase_uid

    row = await get_user_by_supabase_uid(conn, token.supabase_uid)

    if row is None:
        raise AppError(*UNAUTHORIZED)
    if row["deleted_at"] is not None:
        raise AppError(*USER_DELETED)

    return row


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    conn: asyncpg.Connection = Depends(get_db),
) -> asyncpg.Record | None:
    """Like get_current_user but returns None instead of 401 when no token."""
    if credentials is None:
        return None
    from app.core.config import settings
    from app.db.queries.users import get_user_by_supabase_uid

    try:
        token = decode_token(
            credentials.credentials,
            settings.supabase_jwt_secret,
            settings.supabase_url,
        )
    except AppError:
        return None

    row = await get_user_by_supabase_uid(conn, token.supabase_uid)
    if row is None or row["deleted_at"] is not None:
        return None
    return row


async def get_admin_user(
    row: asyncpg.Record = Depends(get_current_user),
) -> asyncpg.Record:
    if row["admin_role"] != "admin":
        raise AppError(*FORBIDDEN)
    return row


async def get_content_manager_user(
    row: asyncpg.Record = Depends(get_current_user),
) -> asyncpg.Record:
    if row["admin_role"] not in ("admin", "content_manager"):
        raise AppError(*FORBIDDEN)
    return row
