"""User service — business logic for auth session and profile operations.

Endpoints stay thin; all DB interactions and side-effects live here.
"""

import asyncpg

from app.core.config import settings
from app.core.errors import AppError, GUEST_TOKEN_EXPIRED, GUEST_TOKEN_INVALID
from app.core.security import TokenPayload
from app.db.queries.users import (
    complete_onboarding,
    create_guest_user,
    create_user,
    get_guest_user_by_token,
    get_user_by_supabase_uid,
    reactivate_deleted_user,
    soft_delete_user,
)
from app.schemas.users import SignupRequest, UserProfile


def _derive_auth_provider(token: TokenPayload) -> str:
    """Determine auth_provider for a new user row.

    Prefers the Supabase JWT's app_metadata.provider claim; falls back to the
    pre-Google heuristic (phone-vs-email presence) for tokens that predate
    that claim's reliability.
    """
    if token.provider == "google":
        return "google"
    if token.provider == "phone" or (token.phone and not token.email):
        return "phone"
    if token.provider == "email" or token.email:
        return "email"
    return "phone" if token.phone else "email"


def _row_to_profile(row: asyncpg.Record) -> UserProfile:
    """Convert a DB record from _SELECT_USER into a UserProfile schema."""
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


async def get_or_create_session_user(
    conn: asyncpg.Connection,
    token: TokenPayload,
    guest_token: str | None,
) -> UserProfile:
    """Exchange a validated JWT for a user profile row.

    Creates the user row on first call (new sign-up path).
    If guest_token is provided:
      - New user → reattribute all guest progress to new account
      - Existing user → discard guest data
    Side-effect: writes audit_log user.created on new user.
    """
    from app.services import audit_service, guest_service

    from app.core.errors import USER_DELETED

    row = await get_user_by_supabase_uid(conn, token.supabase_uid)

    if row is not None and row["deleted_at"] is not None:
        raise AppError(*USER_DELETED)

    if row is None:
        # Wrap create + audit + reattribute in one transaction: get_db yields an
        # autocommit pooled connection, so without this each step commits alone and
        # a mid-sequence failure leaves a half-migrated guest (and a retry would
        # re-run reattribute's non-idempotent xp_ledger INSERT / xp_total bump).
        async with conn.transaction():
            auth_provider = _derive_auth_provider(token)
            row = await create_user(
                conn,
                supabase_uid=token.supabase_uid,
                email=token.email,
                phone=token.phone,
                auth_provider=auth_provider,
                admin_role=token.admin_role,
            )
            await audit_service.log(
                conn,
                action=audit_service.USER_CREATED,
                actor_id=str(row["id"]),
                target_type="user",
                target_id=str(row["id"]),
            )
            # New user: reattribute guest progress atomically
            if guest_token:
                await guest_service.reattribute(conn, guest_token, str(row["id"]))
                # Reload row so xp_total reflects transferred XP
                row = await get_user_by_supabase_uid(conn, token.supabase_uid)
    else:
        # Existing user: discard guest data (multi-table delete — keep atomic)
        if guest_token:
            async with conn.transaction():
                await guest_service.discard(conn, guest_token)

    return _row_to_profile(row)


async def get_or_create_guest(
    conn: asyncpg.Connection, guest_token: str
) -> asyncpg.Record:
    """Fetch existing guest row or create a new one for this token.

    Raises AppError if the token is expired (>30 days old).
    """
    from datetime import datetime, timedelta, timezone

    row = await get_guest_user_by_token(conn, guest_token)

    if row is not None:
        age = datetime.now(timezone.utc) - row["created_at"].replace(tzinfo=timezone.utc)
        if age > timedelta(days=30):
            raise AppError(*GUEST_TOKEN_EXPIRED)
        return row

    return await create_guest_user(conn, guest_token=guest_token)


async def create_account(
    conn: asyncpg.Connection,
    token: TokenPayload,
    body: SignupRequest,
) -> UserProfile:
    """Atomic sign-up: create user row + complete onboarding + optional placement.

    Idempotent: if onboarding is already complete for this JWT, returns the
    existing profile unchanged (safe for double-taps or retried requests).

    Placement priority: explicit body.placement_level_id takes precedence over
    any level stored on a guest account. The guest reattribute step uses a
    WHERE current_level_id IS NULL guard, so it never overwrites an explicit
    choice made in the same call.
    """
    from app.services import audit_service, guest_service
    from app.db.queries.levels import get_level_by_id
    from app.db.queries.placement import set_user_level_and_placement
    from app.core.errors import AppError, LEVEL_NOT_ACTIVE, LEVEL_NOT_FOUND, LEVEL_PAYMENT_REQUIRED

    row = await get_user_by_supabase_uid(conn, token.supabase_uid)

    if row is not None and row["deleted_at"] is not None:
        # This phone's Supabase Auth identity outlives our own soft-delete
        # (Supabase won't issue a second identity for the same phone), so a
        # repeat sign-up resolves back to this same row. Recycle it into a
        # clean-slate account instead of blocking forever — the deletion
        # already happened; there's nothing left to "continue".
        await reactivate_deleted_user(conn, str(row["id"]), token.phone, token.email)
        row = await get_user_by_supabase_uid(conn, token.supabase_uid)

    # Idempotent — already fully signed up (e.g. double-tap, retry)
    if row is not None and row["onboarding_completed_at"] is not None:
        return _row_to_profile(row)

    # A level is no longer required at sign-up time — placement (quiz or
    # manual select) now happens AFTER account creation, so a brand new
    # account legitimately has no current_level_id yet. RequireOnboarding
    # (frontend) routes a level-less authenticated user to /placement itself;
    # this used to hard-block sign-up here when the old flow required a level
    # to already be picked before an account existed, which no longer holds.

    # Validate placement level before any writes so we fail fast and clean.
    # payment_required is enforced here too, not just in POST
    # /placement/choose-level — a guest picking a locked level's "Buy now"
    # sets this same field before ever reaching signup (PlacementSelectLevelPage
    # -> pendingLevelId -> SignupRequest.placement_level_id), so without this
    # check signup silently grants any paid level for free. The placement-quiz
    # path stays exempt: it goes through POST /placement/submit after signup,
    # never through this field.
    if body.placement_level_id is not None:
        level = await get_level_by_id(conn, body.placement_level_id)
        if level is None:
            raise AppError(*LEVEL_NOT_FOUND)
        if not level["is_active"]:
            raise AppError(*LEVEL_NOT_ACTIVE)
        if level["payment_required"]:
            raise AppError(*LEVEL_PAYMENT_REQUIRED)

    # All writes below run in one transaction so a mid-sequence failure can't
    # leave a half-created account, and a retry can't double-apply reattribute's
    # non-idempotent xp_ledger INSERT / xp_total bump. Validation above is
    # read-only and intentionally stays outside the transaction (fail fast, clean).
    async with conn.transaction():
        if row is None:
            auth_provider = _derive_auth_provider(token)
            row = await create_user(
                conn,
                supabase_uid=token.supabase_uid,
                email=token.email,
                phone=token.phone,
                auth_provider=auth_provider,
                admin_role=token.admin_role,
            )
            await audit_service.log(
                conn,
                action=audit_service.USER_CREATED,
                actor_id=str(row["id"]),
                target_type="user",
                target_id=str(row["id"]),
            )

        user_id = str(row["id"])

        await complete_onboarding(
            conn,
            user_id,
            full_name=body.full_name,
            age_group=body.age_group,
            role_tag=body.role_tag,
            english_level=body.english_level,
            language_preference=body.language_preference,
        )

        if body.placement_level_id is not None:
            await set_user_level_and_placement(conn, user_id, body.placement_level_id)

        if body.guest_token:
            await guest_service.reattribute(conn, body.guest_token, user_id)

        # Reload to pick up XP and level transferred from guest reattribution
        row = await get_user_by_supabase_uid(conn, token.supabase_uid)
        assert row is not None
    return _row_to_profile(row)


async def delete_account(
    conn: asyncpg.Connection,
    user_id: str,
    supabase_uid: str,
) -> None:
    """Soft-delete the user row, anonymise PII, revoke Supabase sessions,
    delete the Supabase Auth identity, purge uploaded recordings.

    Order: DB soft-delete first (reversible by ops if a Supabase call fails),
    then Supabase sign-out, then permanently deleting the Supabase Auth user
    (frees the phone number for a future sign-up — without this, a repeat
    sign-up resolves back to this same, now soft-deleted, identity), then
    Storage purge of the user's pronunciation recordings (all three swallow
    errors), then audit log.
    """
    from app.core import supabase_admin
    from app.services import audit_service

    await soft_delete_user(conn, user_id)
    await supabase_admin.sign_out_user(supabase_uid)
    await supabase_admin.delete_user(supabase_uid)
    await supabase_admin.delete_user_recordings(user_id)
    await audit_service.log(
        conn,
        action=audit_service.USER_DELETED,
        actor_id=user_id,
        target_type="user",
        target_id=user_id,
    )
