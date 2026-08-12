from fastapi import APIRouter, Depends, Query, Request
from pydantic import ValidationError

from app.core.errors import AppError, GUEST_TOKEN_INVALID
from app.core.ratelimit import rate_limit
from app.core.security import TokenPayload, get_token_payload
from app.db.pool import get_db
from app.db.queries.users import phone_exists
from app.schemas.auth import (
    CheckPhoneResponse,
    GuestSessionRequest,
    GuestSessionResponse,
    SessionRequest,
)
from app.schemas.users import SignupRequest, UserProfile
from app.services import user_service

import asyncpg

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.get(
    "/auth/check-phone",
    response_model=CheckPhoneResponse,
    # Public + unauthenticated → key by IP; caps account-enumeration probing.
    dependencies=[Depends(rate_limit(20, 60, "check_phone"))],
)
async def check_phone(
    phone: str = Query(..., description="E.164 phone number, e.g. +94771234567"),
    conn: asyncpg.Connection = Depends(get_db),
) -> CheckPhoneResponse:
    """Check whether a phone number belongs to an existing account.

    Public — no auth required.  Used by Sign-In/Sign-Up to gate OTP dispatch.
    """
    exists = await phone_exists(conn, phone)
    return CheckPhoneResponse(exists=exists)


@router.post("/auth/signup", response_model=UserProfile, status_code=200)
async def signup(
    body: SignupRequest,
    token: TokenPayload = Depends(get_token_payload),
    conn: asyncpg.Connection = Depends(get_db),
) -> UserProfile:
    """First-time account creation with onboarding data.

    Collapses create-user + complete-onboarding + optional placement into one
    call. Safe to retry — idempotent if onboarding is already complete.
    """
    return await user_service.create_account(conn, token, body)


@router.post("/auth/session", response_model=UserProfile)
async def create_session(
    body: SessionRequest,
    token: TokenPayload = Depends(get_token_payload),
    conn: asyncpg.Connection = Depends(get_db),
) -> UserProfile:
    """Exchange a Supabase JWT for an app session.

    Creates the user row on first call.  Returns the full profile on every call.
    Guest-token reattribution is wired in Slice 6.
    """
    return await user_service.get_or_create_session_user(
        conn, token, body.guest_token
    )


@router.post("/users/guest", response_model=GuestSessionResponse)
async def create_guest_session(
    body: GuestSessionRequest,
    conn: asyncpg.Connection = Depends(get_db),
) -> GuestSessionResponse:
    """Register or fetch a guest session row.

    Idempotent — returns the existing row if the guest_token is already known.
    Returns GUEST_TOKEN_EXPIRED (401) if the token is older than 30 days.
    """
    try:
        validated = GuestSessionRequest.model_validate(body.model_dump())
    except ValidationError:
        raise AppError(*GUEST_TOKEN_INVALID)

    row = await user_service.get_or_create_guest(conn, validated.guest_token)
    return GuestSessionResponse(
        user_id=str(row["id"]),
        guest_token=row["guest_token"],
        created_at=row["created_at"],
    )
