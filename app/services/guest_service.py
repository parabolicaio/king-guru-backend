"""Guest mode service.

ensure_guest_user  — resolve/create a guest "user" row from a token
reattribute        — transfer all guest data to a newly-registered user (must be called inside a DB transaction)
discard            — delete guest data when an existing user logs in
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import asyncpg

from app.core.errors import AppError, GUEST_TOKEN_EXPIRED, GUEST_TOKEN_INVALID
from app.db.utils import new_uuid


@dataclass
class ReattributeResult:
    reattributed_attempt_count: int


async def ensure_guest_user(
    conn: asyncpg.Connection,
    guest_token: str,
) -> asyncpg.Record:
    """Fetch or create a guest user row for the given token.

    Raises GUEST_TOKEN_INVALID for empty/blank tokens.
    Raises GUEST_TOKEN_EXPIRED if the row is older than 30 days.
    """
    if not guest_token or not guest_token.strip():
        raise AppError(*GUEST_TOKEN_INVALID)

    row = await conn.fetchrow(
        'SELECT * FROM "user" WHERE guest_token = $1 AND is_guest = TRUE AND deleted_at IS NULL',
        guest_token,
    )

    if row is not None:
        age = datetime.now(timezone.utc) - row["created_at"].replace(tzinfo=timezone.utc)
        if age > timedelta(days=30):
            raise AppError(*GUEST_TOKEN_EXPIRED)
        return row

    user_id = new_uuid()
    now = datetime.now(timezone.utc)
    await conn.execute(
        """
        INSERT INTO "user" (id, is_guest, guest_token, created_at, updated_at)
        VALUES ($1::uuid, TRUE, $2, $3, $3)
        ON CONFLICT DO NOTHING
        """,
        user_id, guest_token, now,
    )
    # Re-fetch — handles race where another request just created it
    row = await conn.fetchrow(
        'SELECT * FROM "user" WHERE guest_token = $1 AND is_guest = TRUE AND deleted_at IS NULL',
        guest_token,
    )
    assert row is not None
    return row


async def reattribute(
    conn: asyncpg.Connection,
    guest_token: str,
    new_user_id: str,
) -> ReattributeResult:
    """Transfer all guest data to a newly-registered user.

    Must be called inside a DB transaction so all steps are atomic.

    Steps:
    1. Fetch guest user row; no-op if not found
    2. UPDATE attempt.user_id → new_user_id WHERE guest_token
    3. INSERT lesson_progress rows for new user (skip duplicates)
    4. INSERT vocabulary_mastery rows for new user (skip duplicates)
    5. INSERT xp_ledger rows for new user
    6. UPDATE new user xp_total += guest xp_total
    7. Soft-delete the guest user row
    """
    guest_row = await conn.fetchrow(
        """
        SELECT id, xp_total, current_level_id, placement_completed_at
        FROM "user"
        WHERE guest_token = $1 AND is_guest = TRUE AND deleted_at IS NULL
        """,
        guest_token,
    )
    if guest_row is None:
        return ReattributeResult(reattributed_attempt_count=0)

    guest_user_id = str(guest_row["id"])
    guest_xp = guest_row["xp_total"] or 0
    now = datetime.now(timezone.utc)

    # 2. Reattribute attempts
    result = await conn.execute(
        """
        UPDATE attempt
        SET user_id = $1::uuid,
            guest_token = NULL
        WHERE guest_token = $2 AND user_id IS NULL
        """,
        new_user_id, guest_token,
    )
    attempt_count = int(result.split()[-1])

    # 3. Reattribute lesson_progress (INSERT … SELECT, skip duplicates)
    await conn.execute(
        """
        INSERT INTO lesson_progress (id, user_id, lesson_id, status, completion_pct,
                                     started_at, completed_at, created_at, updated_at)
        SELECT gen_random_uuid(), $1::uuid, lesson_id, status, completion_pct,
               started_at, completed_at, $2, $2
        FROM lesson_progress
        WHERE user_id = $3::uuid
        ON CONFLICT (user_id, lesson_id) DO NOTHING
        """,
        new_user_id, now, guest_user_id,
    )

    # 4. Reattribute vocabulary_mastery (skip duplicates)
    await conn.execute(
        """
        INSERT INTO vocabulary_mastery (id, user_id, vocabulary_word_id, attempt_count,
                                        correct_attempt_count, is_mastered, last_seen_at,
                                        created_at, updated_at)
        SELECT gen_random_uuid(), $1::uuid, vocabulary_word_id, attempt_count,
               correct_attempt_count, is_mastered, last_seen_at, $2, $2
        FROM vocabulary_mastery
        WHERE user_id = $3::uuid
        ON CONFLICT (user_id, vocabulary_word_id) DO NOTHING
        """,
        new_user_id, now, guest_user_id,
    )

    # 5. Reattribute xp_ledger rows
    await conn.execute(
        """
        INSERT INTO xp_ledger (id, user_id, action_type, xp_delta,
                                reference_id, reference_type, awarded_at)
        SELECT gen_random_uuid(), $1::uuid, action_type, xp_delta,
               reference_id, reference_type, awarded_at
        FROM xp_ledger
        WHERE user_id = $2::uuid
        """,
        new_user_id, guest_user_id,
    )

    # 6. Add guest xp_total to new user
    if guest_xp > 0:
        await conn.execute(
            'UPDATE "user" SET xp_total = xp_total + $1, updated_at = $2 WHERE id = $3::uuid',
            guest_xp, now, new_user_id,
        )

    # 6b. Transfer level choice made pre-auth — only if new user hasn't already chosen a level
    if guest_row["current_level_id"] is not None:
        await conn.execute(
            """
            UPDATE "user"
            SET current_level_id      = $2,
                placement_completed_at = COALESCE(placement_completed_at, $3),
                updated_at             = $4
            WHERE id = $1::uuid
              AND current_level_id IS NULL
            """,
            new_user_id,
            str(guest_row["current_level_id"]),
            guest_row["placement_completed_at"],
            now,
        )

    # 7. Soft-delete guest row
    await conn.execute(
        """
        UPDATE "user"
        SET deleted_at = $2,
            guest_token = NULL,
            updated_at  = $2
        WHERE id = $1::uuid
        """,
        guest_user_id, now,
    )

    return ReattributeResult(reattributed_attempt_count=attempt_count)


async def discard(
    conn: asyncpg.Connection,
    guest_token: str,
) -> None:
    """Discard all guest data when an existing user logs in.

    Hard-deletes guest attempts; soft-deletes the guest user row.
    Existing user's data is completely unaffected.
    """
    guest_row = await conn.fetchrow(
        'SELECT id FROM "user" WHERE guest_token = $1 AND is_guest = TRUE AND deleted_at IS NULL',
        guest_token,
    )
    if guest_row is None:
        return

    guest_user_id = str(guest_row["id"])
    now = datetime.now(timezone.utc)

    await conn.execute(
        "DELETE FROM attempt WHERE guest_token = $1",
        guest_token,
    )
    await conn.execute(
        "DELETE FROM lesson_progress WHERE user_id = $1::uuid",
        guest_user_id,
    )
    await conn.execute(
        "DELETE FROM vocabulary_mastery WHERE user_id = $1::uuid",
        guest_user_id,
    )
    await conn.execute(
        "DELETE FROM xp_ledger WHERE user_id = $1::uuid",
        guest_user_id,
    )
    await conn.execute(
        """
        UPDATE "user"
        SET deleted_at = $2,
            guest_token = NULL,
            updated_at  = $2
        WHERE id = $1::uuid
        """,
        guest_user_id, now,
    )
