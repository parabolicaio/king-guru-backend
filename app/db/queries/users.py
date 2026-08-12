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
            updated_at  = $2
        WHERE id = $1::uuid AND deleted_at IS NULL
        """,
        user_id, now, anon,
    )
