"""Raw SQL query functions for admin content authoring."""

from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid


# ── Lessons ──────────────────────────────────────────────────────────────────

async def create_lesson(
    db: asyncpg.Connection,
    *,
    level_id: str,
    title: str,
    description: str | None,
    lesson_order: int,
    is_guest_accessible: bool,
    thumbnail_url: str | None,
    translations: dict,
    objectives: list,
    objectives_translations: dict,
    created_by: str,
) -> asyncpg.Record:
    lesson_id = new_uuid()
    now = datetime.now(timezone.utc)
    return await db.fetchrow(
        """
        INSERT INTO lesson (id, level_id, title, description, lesson_order,
                            status, is_guest_accessible, thumbnail_url, translations,
                            objectives, objectives_translations,
                            created_at, updated_at)
        VALUES ($1, $2::uuid, $3, $4, $5, 'draft', $6, $7, $8, $9, $10, $11, $11)
        RETURNING *
        """,
        lesson_id, level_id, title, description, lesson_order,
        is_guest_accessible, thumbnail_url, translations,
        objectives, objectives_translations, now,
    )


async def list_lessons_admin(
    db: asyncpg.Connection,
    *,
    level_id: str | None = None,
    status: str | None = None,
    cm_id: str | None = None,
    admin_sees_all: bool = False,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[asyncpg.Record], int]:
    conditions = ["l.deleted_at IS NULL"]
    params: list = []
    idx = 1

    if level_id:
        conditions.append(f"l.level_id = ${idx}::uuid")
        params.append(level_id)
        idx += 1

    if status:
        conditions.append(f"l.status = ${idx}")
        params.append(status)
        idx += 1

    if not admin_sees_all and cm_id:
        # Content managers only see their own lessons via audit_log
        # Simplified: all CM see all lessons in their level scope for Phase 1
        pass

    where = " AND ".join(conditions)
    offset = (page - 1) * page_size

    rows = await db.fetch(
        f"""
        SELECT l.*, lv.code AS level_code
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE {where}
        ORDER BY l.level_id, l.lesson_order
        LIMIT ${idx} OFFSET ${idx + 1}
        """,
        *params, page_size, offset,
    )
    count_row = await db.fetchrow(
        f'SELECT COUNT(*) AS total FROM lesson l WHERE {where}',
        *params,
    )
    return list(rows), int(count_row["total"])


async def get_lesson_admin(
    db: asyncpg.Connection, lesson_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM lesson WHERE id = $1::uuid",
        lesson_id,
    )


async def update_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
    *,
    title: str | None = None,
    description: str | None = ...,  # type: ignore[assignment]
    is_guest_accessible: bool | None = None,
    thumbnail_url: str | None = ...,  # type: ignore[assignment]
    translations: dict | None = None,
    objectives: list | None = None,
    objectives_translations: dict | None = None,
    status: str | None = None,
) -> asyncpg.Record:
    sets: list[str] = []
    params: list = []
    idx = 1

    sentinel = ...

    def add(col: str, val) -> None:  # type: ignore[no-untyped-def]
        nonlocal idx
        if val is not sentinel and val is not None or (col in ("description", "thumbnail_url") and val is not sentinel):
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1

    if title is not None:
        sets.append(f"title = ${idx}")
        params.append(title)
        idx += 1
    if description is not sentinel:
        sets.append(f"description = ${idx}")
        params.append(description)
        idx += 1
    if is_guest_accessible is not None:
        sets.append(f"is_guest_accessible = ${idx}")
        params.append(is_guest_accessible)
        idx += 1
    if thumbnail_url is not sentinel:
        sets.append(f"thumbnail_url = ${idx}")
        params.append(thumbnail_url)
        idx += 1
    if translations is not None:
        sets.append(f"translations = ${idx}")
        params.append(translations)
        idx += 1
    if objectives is not None:
        sets.append(f"objectives = ${idx}")
        params.append(objectives)
        idx += 1
    if objectives_translations is not None:
        sets.append(f"objectives_translations = ${idx}")
        params.append(objectives_translations)
        idx += 1
    if status is not None:
        sets.append(f"status = ${idx}")
        params.append(status)
        idx += 1

    if not sets:
        return await get_lesson_admin(db, lesson_id)  # type: ignore[return-value]

    now = datetime.now(timezone.utc)
    sets.append(f"updated_at = ${idx}")
    params.append(now)
    idx += 1
    params.append(lesson_id)

    return await db.fetchrow(
        f"UPDATE lesson SET {', '.join(sets)} WHERE id = ${idx}::uuid RETURNING *",
        *params,
    )


async def soft_delete_lesson(db: asyncpg.Connection, lesson_id: str) -> None:
    await db.execute(
        "UPDATE lesson SET deleted_at = now(), updated_at = now() WHERE id = $1::uuid AND deleted_at IS NULL",
        lesson_id,
    )


async def archive_lesson(db: asyncpg.Connection, lesson_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        "UPDATE lesson SET archived_at = COALESCE(archived_at, now()), updated_at = now() WHERE id = $1::uuid RETURNING *",
        lesson_id,
    )


# ── Sections ─────────────────────────────────────────────────────────────────

async def create_section(
    db: asyncpg.Connection,
    *,
    lesson_id: str,
    category: str,
    display_order: int,
    title: str | None,
    translations: dict,
) -> asyncpg.Record:
    section_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO lesson_section (id, lesson_id, category, display_order, title, translations)
        VALUES ($1, $2::uuid, $3, $4, $5, $6)
        RETURNING *
        """,
        section_id, lesson_id, category, display_order, title, translations,
    )


async def get_section_admin(db: asyncpg.Connection, section_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM lesson_section WHERE id = $1::uuid",
        section_id,
    )


async def update_section(
    db: asyncpg.Connection, section_id: str, **fields
) -> asyncpg.Record:
    sets = []
    params = []
    idx = 1
    for col, val in fields.items():
        if val is not None:
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1
    sets.append(f"updated_at = ${idx}")
    params.append(datetime.now(timezone.utc))
    idx += 1
    params.append(section_id)
    return await db.fetchrow(
        f"UPDATE lesson_section SET {', '.join(sets)} WHERE id = ${idx}::uuid RETURNING *",
        *params,
    )


async def delete_section(db: asyncpg.Connection, section_id: str) -> None:
    await db.execute(
        "DELETE FROM lesson_section WHERE id = $1::uuid",
        section_id,
    )


async def section_has_attempts(db: asyncpg.Connection, section_id: str) -> bool:
    row = await db.fetchrow(
        "SELECT EXISTS(SELECT 1 FROM attempt WHERE lesson_section_id = $1::uuid) AS has_attempts",
        section_id,
    )
    return bool(row["has_attempts"])


# ── Content Blocks ───────────────────────────────────────────────────────────

async def create_block(
    db: asyncpg.Connection,
    *,
    lesson_section_id: str,
    block_type: str,
    display_order: int,
    payload: dict,
    translations: dict,
) -> asyncpg.Record:
    block_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO content_block (id, lesson_section_id, block_type, display_order, payload, translations)
        VALUES ($1, $2::uuid, $3, $4, $5, $6)
        RETURNING *
        """,
        block_id, lesson_section_id, block_type, display_order, payload, translations,
    )


async def get_block_admin(db: asyncpg.Connection, block_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM content_block WHERE id = $1::uuid",
        block_id,
    )


async def update_block(
    db: asyncpg.Connection, block_id: str, **fields
) -> asyncpg.Record:
    sets = []
    params = []
    idx = 1
    for col, val in fields.items():
        if val is not None:
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1
    sets.append(f"updated_at = ${idx}")
    params.append(datetime.now(timezone.utc))
    idx += 1
    params.append(block_id)
    return await db.fetchrow(
        f"UPDATE content_block SET {', '.join(sets)} WHERE id = ${idx}::uuid RETURNING *",
        *params,
    )


async def delete_block(db: asyncpg.Connection, block_id: str) -> None:
    await db.execute("DELETE FROM content_block WHERE id = $1::uuid", block_id)


async def display_order_exists_in_section(
    db: asyncpg.Connection, section_id: str, display_order: int, exclude_block_id: str | None = None
) -> bool:
    if exclude_block_id:
        row = await db.fetchrow(
            "SELECT EXISTS(SELECT 1 FROM content_block WHERE lesson_section_id = $1::uuid AND display_order = $2 AND id != $3::uuid) AS exists",
            section_id, display_order, exclude_block_id,
        )
    else:
        row = await db.fetchrow(
            "SELECT EXISTS(SELECT 1 FROM content_block WHERE lesson_section_id = $1::uuid AND display_order = $2) AS exists",
            section_id, display_order,
        )
    return bool(row["exists"])


# ── Questions ────────────────────────────────────────────────────────────────

async def create_question(
    db: asyncpg.Connection,
    *,
    lesson_section_id: str,
    question_type: str,
    purpose: str,
    display_order: int,
    prompt_text: str | None,
    prompt_audio_url: str | None,
    prompt_image_url: str | None,
    payload: dict,
    xp_value: int,
    hint_text: str | None,
    vocabulary_word_id: str | None,
    translations: dict,
) -> asyncpg.Record:
    qid = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO question (id, lesson_section_id, type, purpose, display_order,
                              prompt_text, prompt_audio_url, prompt_image_url,
                              payload, xp_value, hint_text, vocabulary_word_id, translations)
        VALUES ($1, $2::uuid, $3, $4, $5, $6, $7, $8, $9, $10, $11,
                CASE WHEN $12::text IS NULL THEN NULL ELSE $12::uuid END, $13)
        RETURNING *
        """,
        qid, lesson_section_id, question_type, purpose, display_order,
        prompt_text, prompt_audio_url, prompt_image_url,
        payload, xp_value, hint_text, vocabulary_word_id, translations,
    )


async def get_question_admin(db: asyncpg.Connection, question_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM question WHERE id = $1::uuid",
        question_id,
    )


async def update_question(
    db: asyncpg.Connection, question_id: str, **fields
) -> asyncpg.Record:
    sets = []
    params = []
    idx = 1
    for col, val in fields.items():
        if val is not None:
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1
    sets.append(f"updated_at = ${idx}")
    params.append(datetime.now(timezone.utc))
    idx += 1
    params.append(question_id)
    return await db.fetchrow(
        f"UPDATE question SET {', '.join(sets)} WHERE id = ${idx}::uuid RETURNING *",
        *params,
    )


async def delete_question(db: asyncpg.Connection, question_id: str) -> None:
    await db.execute("DELETE FROM question WHERE id = $1::uuid", question_id)


async def question_has_attempts(db: asyncpg.Connection, question_id: str) -> bool:
    row = await db.fetchrow(
        "SELECT EXISTS(SELECT 1 FROM attempt WHERE question_id = $1::uuid) AS has_attempts",
        question_id,
    )
    return bool(row["has_attempts"])


# ── Vocabulary Words ─────────────────────────────────────────────────────────

async def create_vocabulary_word(
    db: asyncpg.Connection,
    *,
    lesson_section_id: str,
    word: str,
    definition: str,
    example_sentence: str | None,
    pronunciation_guide_si: str | None,
    difficulty: str,
    image_url: str | None,
    translations: dict,
) -> asyncpg.Record:
    wid = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO vocabulary_word (id, lesson_section_id, word, definition,
                                     example_sentence, pronunciation_guide_si,
                                     difficulty, image_url, translations)
        VALUES ($1, $2::uuid, $3, $4, $5, $6, $7, $8, $9)
        RETURNING *
        """,
        wid, lesson_section_id, word, definition,
        example_sentence, pronunciation_guide_si, difficulty, image_url, translations,
    )


async def get_vocabulary_word_admin(
    db: asyncpg.Connection, word_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT * FROM vocabulary_word WHERE id = $1::uuid",
        word_id,
    )


async def update_vocabulary_word(
    db: asyncpg.Connection, word_id: str, **fields
) -> asyncpg.Record:
    sets = []
    params = []
    idx = 1
    for col, val in fields.items():
        if val is not None:
            sets.append(f"{col} = ${idx}")
            params.append(val)
            idx += 1
    sets.append(f"updated_at = ${idx}")
    params.append(datetime.now(timezone.utc))
    idx += 1
    params.append(word_id)
    return await db.fetchrow(
        f"UPDATE vocabulary_word SET {', '.join(sets)} WHERE id = ${idx}::uuid RETURNING *",
        *params,
    )


async def delete_vocabulary_word(db: asyncpg.Connection, word_id: str) -> None:
    await db.execute("DELETE FROM vocabulary_word WHERE id = $1::uuid", word_id)


async def vocabulary_word_has_mastery(db: asyncpg.Connection, word_id: str) -> bool:
    row = await db.fetchrow(
        "SELECT EXISTS(SELECT 1 FROM vocabulary_mastery WHERE vocabulary_word_id = $1::uuid) AS has_mastery",
        word_id,
    )
    return bool(row["has_mastery"])
