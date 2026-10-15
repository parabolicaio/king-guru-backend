"""Raw SQL query functions for the "user" table.

All functions accept an asyncpg Connection and return asyncpg Record objects
(or None).  Callers convert records to Pydantic schemas.

Rules:
  - Every INSERT passes the PK via new_uuid() — never DEFAULT gen_random_uuid().
  - Every query is parameterised — no string-formatted user input.
  - "user" is a PostgreSQL reserved word — quoted in every statement.
"""

from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid


_SELECT_USER = """
    SELECT
        u.id,
        u.supabase_uid::text,
        u.email,
        u.phone,
        u.full_name,
        u.display_name,
        u.avatar_url,
        u.age_group,
        u.role_tag,
        u.english_level,
        u.auth_provider,
        u.language_preference,
        u.is_guest,
        u.guest_token,
        u.admin_role,
        u.xp_total,
        u.streak_current,
        u.streak_longest,
        u.onboarding_completed_at,
        u.placement_completed_at,
        u.current_level_id::text,
        lv.name AS current_level_name,
        u.subscription_tier,
        u.deleted_at,
        u.created_at,
        u.updated_at
    FROM "user" u
    LEFT JOIN level lv ON lv.id = u.current_level_id
"""


async def get_user_by_supabase_uid(
    conn: asyncpg.Connection, supabase_uid: str
) -> asyncpg.Record | None:
    return await conn.fetchrow(
        _SELECT_USER + "WHERE u.supabase_uid = $1::uuid",
        supabase_uid,
    )


async def get_user_by_id(
    conn: asyncpg.Connection, user_id: str
) -> asyncpg.Record | None:
    return await conn.fetchrow(
        _SELECT_USER + "WHERE u.id = $1::uuid",
        user_id,
    )


import re as _re


def sanitise_phone(phone: str) -> tuple[str, str]:
    """Sanitise a raw phone input and return (with_plus, without_plus) variants.

    Handles:
    - Leading/trailing ASCII and Unicode whitespace
    - Internal spaces, dashes, dots, parentheses, unicode spaces (\\u00a0, \\u202f, etc.)
    - Multiple leading '+' characters
    - Mixed formatting e.g. '+94 (72) 499-9547'

    Returns both '+94...' and '94...' so callers can match either DB storage form.
    """
    # Strip outer whitespace (including unicode)
    phone = phone.strip()
    # Remove all formatting characters: spaces (incl. unicode), dashes, dots, parens
    phone = _re.sub(r"[\s   ​\-\.\(\)]+", "", phone)
    # Collapse multiple leading '+' into one
    phone = _re.sub(r"^\++", "+", phone)
    # Drop any remaining non-digit, non-plus characters
    phone = _re.sub(r"[^\d+]", "", phone)

    digits = phone.lstrip("+")
    return f"+{digits}", digits


async def phone_exists(
    conn: asyncpg.Connection, phone: str
) -> bool:
    """Return True if an active (non-deleted) user exists with this phone number.

    Sanitises the input and matches both '+94...' and '94...' storage forms.
    """
    with_plus, without_plus = sanitise_phone(phone)
    row = await conn.fetchrow(
        """
        SELECT 1 FROM "user"
        WHERE phone IN ($1, $2)
          AND deleted_at IS NULL
          AND is_guest = FALSE
        LIMIT 1
        """,
        with_plus,
        without_plus,
    )
    return row is not None


async def get_guest_user_by_token(
    conn: asyncpg.Connection, guest_token: str
) -> asyncpg.Record | None:
    return await conn.fetchrow(
        _SELECT_USER + "WHERE u.guest_token = $1 AND u.is_guest = TRUE",
        guest_token,
    )


async def create_user(
    conn: asyncpg.Connection,
    *,
    supabase_uid: str,
    email: str | None,
    phone: str | None,
    auth_provider: str,
    admin_role: str | None = None,
) -> asyncpg.Record:
    user_id = new_uuid()
    now = datetime.now(timezone.utc)
    await conn.execute(
        """
        INSERT INTO "user" (
            id, supabase_uid, email, phone, auth_provider, admin_role,
            created_at, updated_at
        ) VALUES (
            $1::uuid, $2::uuid, $3, $4, $5, $6, $7, $7
        )
        """,
        user_id, supabase_uid, email, phone, auth_provider, admin_role, now,
    )
    row = await get_user_by_id(conn, user_id)
    assert row is not None  # just inserted
    return row


async def create_guest_user(
    conn: asyncpg.Connection, *, guest_token: str
) -> asyncpg.Record:
    user_id = new_uuid()
    now = datetime.now(timezone.utc)
    await conn.execute(
        """
        INSERT INTO "user" (
            id, is_guest, guest_token, created_at, updated_at
        ) VALUES (
            $1::uuid, TRUE, $2, $3, $3
        )
        """,
        user_id, guest_token, now,
    )
    row = await get_user_by_id(conn, user_id)
    assert row is not None
    return row


async def update_user_profile(
    conn: asyncpg.Connection,
    user_id: str,
    *,
    display_name: str | None = ...,        # type: ignore[assignment]
    avatar_url: str | None = ...,          # type: ignore[assignment]
    age_group: str | None = ...,           # type: ignore[assignment]
    role_tag: str | None = ...,            # type: ignore[assignment]
    english_level: str | None = ...,       # type: ignore[assignment]
    language_preference: str | None = ..., # type: ignore[assignment]
) -> asyncpg.Record:
    """Update only the fields that were explicitly passed (not sentinel ...)."""
    sets: list[str] = []
    params: list = []
    idx = 1

    _sentinel = ...

    def add(col: str, val) -> None:  # type: ignore[no-untyped-def]
        nonlocal idx
        if val is not _sentinel:
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1

    add("display_name", display_name)
    add("avatar_url", avatar_url)
    add("age_group", age_group)
    add("role_tag", role_tag)
    add("english_level", english_level)
    add("language_preference", language_preference)

    if not sets:
        row = await get_user_by_id(conn, user_id)
        assert row is not None
        return row

    sets.append(f"updated_at = ${idx}")
    params.append(datetime.now(timezone.utc))
    idx += 1
    params.append(user_id)

    await conn.execute(
        f'UPDATE "user" SET {", ".join(sets)} WHERE id = ${idx}::uuid',
        *params,
    )
    row = await get_user_by_id(conn, user_id)
    assert row is not None
    return row


async def complete_onboarding(
    conn: asyncpg.Connection,
    user_id: str,
    *,
    full_name: str,
    age_group: str,
    role_tag: str,
    english_level: str,
    language_preference: str,
) -> asyncpg.Record:
    now = datetime.now(timezone.utc)
    await conn.execute(
        """
        UPDATE "user"
        SET full_name           = $2,
            age_group           = $3,
            role_tag            = $4,
            english_level       = $5,
            language_preference = $6,
            onboarding_completed_at = COALESCE(onboarding_completed_at, $7),
            updated_at          = $7
        WHERE id = $1::uuid
        """,
        user_id, full_name, age_group, role_tag, english_level, language_preference, now,
    )
    row = await get_user_by_id(conn, user_id)
    assert row is not None
    return row


async def soft_delete_user(
    conn: asyncpg.Connection, user_id: str
) -> None:
    """Soft-delete and PII-anonymise in a single statement."""
    now = datetime.now(timezone.utc)
    anon = f"[deleted-{user_id}]"
    await conn.execute(
        """
        UPDATE "user"
        SET deleted_at  = $2,
            full_name   = $3,
            email       = $3,
            phone       = $3,
            avatar_url  = NULL,
            apple_refresh_token = NULL,
            updated_at  = $2
        WHERE id = $1::uuid AND deleted_at IS NULL
        """,
        user_id, now, anon,
    )


async def get_apple_refresh_token(
    conn: asyncpg.Connection, user_id: str
) -> str | None:
    row = await conn.fetchrow(
        'SELECT apple_refresh_token FROM "user" WHERE id = $1::uuid',
        user_id,
    )
    return row["apple_refresh_token"] if row else None


async def set_apple_refresh_token(
    conn: asyncpg.Connection, user_id: str, refresh_token: str
) -> None:
    await conn.execute(
        'UPDATE "user" SET apple_refresh_token = $2, updated_at = $3 WHERE id = $1::uuid',
        user_id, refresh_token, datetime.now(timezone.utc),
    )


# Every table holding a user's own activity/progress data, keyed by user_id
# (ai_tutor_message cascades automatically from ai_tutor_conversation).
# Deliberately EXCLUDES:
#   - payment: Privacy Policy promises payment records are kept for as long
#     as Sri Lankan tax/accounting law requires — never purged on request.
#   - audit_log: our own accountability trail of actions taken; its FK is
#     ON DELETE RESTRICT by design and is never meant to be erasable.
_USER_ACTIVITY_TABLES = (
    "lesson_progress",
    "lesson_section_progress",
    "daily_goal_progress",
    "notification",
    "attempt",
    "xp_ledger",
    "daily_essay_submission",
    "vocabulary_mastery",
    "user_achievement",
    "certificate",
    "ai_tutor_conversation",
    "ai_usage_log",
    "saved_card",
    "onepay_customer",
)


async def purge_user_activity_data(conn: asyncpg.Connection, user_id: str) -> None:
    """Delete every row of a user's own activity/progress data.

    Soft-deleting the "user" row alone (see soft_delete_user) only resets
    columns on that one row — every other table still holds the deleted
    user's lesson progress, daily goals, notifications, attempts, XP,
    essays and AI-tutor history under the same user_id, because the row is
    recycled (not hard-deleted) on a repeat sign-up with the same phone
    number (see reactivate_deleted_user). Without this, that recycled
    account silently "revives" all of it. Called both at deletion time and
    defensively at reactivation time, so accounts soft-deleted before this
    fix shipped get cleaned up the next time they're signed into again.
    """
    async with conn.transaction():
        for table in _USER_ACTIVITY_TABLES:
            await conn.execute(f'DELETE FROM "{table}" WHERE user_id = $1::uuid', user_id)


async def reactivate_deleted_user(
    conn: asyncpg.Connection,
    user_id: str,
    phone: str | None,
    email: str | None,
) -> None:
    """Recycle a soft-deleted row into a genuinely fresh account.

    A phone number's Supabase Auth identity persists even after our own
    soft-delete (Supabase doesn't let two identities share a phone), so a
    repeat sign-up's OTP verification resolves back to this same row instead
    of creating a new one. Rather than blocking that sign-up forever, this
    resets the row to a clean-slate state — restores the real phone/email,
    clears deleted_at and every progress/stat field, and strips admin_role so
    a deleted admin's privileges never carry over to whoever signs up next
    with that number. full_name/age_group/role_tag/language_preference are
    left alone here — create_account's complete_onboarding() call
    immediately after this overwrites them with the new sign-up's data.
    """
    now = datetime.now(timezone.utc)
    await conn.execute(
        """
        UPDATE "user"
        SET deleted_at                = NULL,
            phone                     = $2,
            email                     = $3,
            onboarding_completed_at   = NULL,
            placement_completed_at    = NULL,
            current_level_id          = NULL,
            xp_total                  = 0,
            streak_current            = 0,
            streak_longest            = 0,
            streak_last_activity_date = NULL,
            subscription_tier         = 'free',
            admin_role                = NULL,
            updated_at                = $4
        WHERE id = $1::uuid
        """,
        user_id, phone, email, now,
    )
