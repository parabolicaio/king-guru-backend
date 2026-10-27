"""D-75: a skill is available once the level has a section of that type,
even when the section has nothing to answer (Speaking)."""

from unittest.mock import AsyncMock

import pytest

from app.db.queries.progress import get_skill_progress


@pytest.mark.asyncio
async def test_skill_available_when_section_exists_without_questions():
    db = AsyncMock()
    db.fetch.return_value = []
    await get_skill_progress(db, "u", "l")
    sql = " ".join(db.fetch.call_args.args[0].split())
    assert "LEFT JOIN question q ON q.lesson_section_id = ls.id" in sql
    assert "(ls.category IS NOT NULL) AS is_available" in sql
    assert "total_questions > 0" not in sql
