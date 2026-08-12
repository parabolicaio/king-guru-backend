"""Raw SQL queries for achievements and leaderboard."""

import asyncpg

from app.db.utils import new_uuid


async def get_all_achievements_with_user_state(
    db: asyncpg.Connection,
    user_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT a.id, a.name, a.description, a.icon_url,
               a.condition_type, a.condition_value, a.xp_reward,
               a.is_active, a.translations,
               ua.unlocked_at
        FROM achievement a
        LEFT JOIN user_achievement ua
               ON ua.achievement_id = a.id AND ua.user_id = $1::uuid
        WHERE a.is_active = TRUE
        ORDER BY a.condition_type, a.condition_value
        """,
        user_id,
    )


async def get_user_achievement(
    db: asyncpg.Connection,
    user_id: str,
    achievement_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM user_achievement WHERE user_id = $1::uuid AND achievement_id = $2::uuid",
        user_id, achievement_id,
    )


async def unlock_achievement(
    db: asyncpg.Connection,
    user_id: str,
    achievement_id: str,
) -> asyncpg.Record:
    rec_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO user_achievement (id, user_id, achievement_id, unlocked_at)
        VALUES ($1, $2::uuid, $3::uuid, now())
        ON CONFLICT (user_id, achievement_id) DO UPDATE SET unlocked_at = user_achievement.unlocked_at
        RETURNING *
        """,
        rec_id, user_id, achievement_id,
    )


async def get_leaderboard(
    db: asyncpg.Connection,
    limit: int = 50,
) -> list[asyncpg.Record]:
    """Return top N users by xp_total (all-time), with their level code."""
    return await db.fetch(
        """
        SELECT u.id, COALESCE(u.display_name, u.full_name, 'Learner') AS display_name,
               u.avatar_url, u.xp_total,
               lv.code AS level_code,
               RANK() OVER (ORDER BY u.xp_total DESC) AS rank
        FROM "user" u
        LEFT JOIN level lv ON lv.id = u.current_level_id
        WHERE u.deleted_at IS NULL
          AND u.is_guest = FALSE
          AND u.onboarding_completed_at IS NOT NULL
        ORDER BY u.xp_total DESC
        LIMIT $1
        """,
        limit,
    )


async def get_user_rank(
    db: asyncpg.Connection,
    user_id: str,
) -> int | None:
    row = await db.fetchrow(
        """
        SELECT rank FROM (
            SELECT id, RANK() OVER (ORDER BY xp_total DESC) AS rank
            FROM "user"
            WHERE deleted_at IS NULL AND is_guest = FALSE AND onboarding_completed_at IS NOT NULL
        ) ranked
        WHERE id = $1::uuid
        """,
        user_id,
    )
    return int(row["rank"]) if row else None
