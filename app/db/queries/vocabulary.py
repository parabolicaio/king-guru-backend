import asyncpg


async def get_vocabulary_for_user(
    db: asyncpg.Connection,
    user_id: str,
    limit: int = 40,
    cursor: str | None = None,
    mastered: bool | None = None,
    level_id: str | None = None,
) -> list[asyncpg.Record]:
    conditions = ["vw.deleted_at IS NULL"]
    params: list = [user_id, limit + 1]
    idx = 3

    if mastered is not None:
        conditions.append(f"COALESCE(vm.is_mastered, false) = ${idx}")
        params.append(mastered)
        idx += 1

    if level_id is not None:
        conditions.append(f"l.id = ${idx}")
        params.append(level_id)
        idx += 1

    if cursor is not None:
        conditions.append(f"vw.id > ${idx}")
        params.append(cursor)
        idx += 1

    where = " AND ".join(conditions)

    sql = f"""
        SELECT vw.id, vw.word, vw.definition, vw.example_sentence,
               vw.pronunciation_guide_si, vw.difficulty,
               vw.image_url, vw.audio_url, vw.translations,
               l.code AS level_code,
               COALESCE(vm.attempt_count, 0) AS attempt_count,
               COALESCE(vm.correct_attempt_count, 0) AS correct_attempt_count,
               COALESCE(vm.is_mastered, false) AS is_mastered,
               vm.last_seen_at
        FROM vocabulary_word vw
        JOIN lesson_section ls ON ls.id = vw.section_id
        JOIN lesson le ON le.id = ls.lesson_id
        JOIN level l ON l.id = le.level_id
        LEFT JOIN vocabulary_mastery vm
            ON vm.vocabulary_word_id = vw.id AND vm.user_id = $1
        WHERE {where}
        ORDER BY vw.id ASC
        LIMIT $2
    """

    return await db.fetch(sql, *params)
