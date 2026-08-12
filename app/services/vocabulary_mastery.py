"""Vocabulary mastery service."""

from dataclasses import dataclass

import asyncpg

from app.db.queries.vocabulary_mastery import (
    get_vocabulary_word_difficulty,
    set_mastered,
    upsert_vocabulary_mastery,
)
from app.db.utils import new_uuid
from app.services import xp as xp_service


@dataclass
class MasteryResult:
    attempt_count: int
    correct_attempt_count: int
    is_mastered: bool
    newly_mastered: bool


async def record(
    db: asyncpg.Connection,
    user_id: str,
    vocabulary_word_id: str,
    is_correct: bool,
) -> MasteryResult:
    """Update mastery for a word after an attempt.

    Only call when question.vocabulary_word_id IS NOT NULL.
    Mastery is irreversible in Phase 1.
    """
    row = await upsert_vocabulary_mastery(
        db,
        mastery_id=str(new_uuid()),
        user_id=user_id,
        vocabulary_word_id=vocabulary_word_id,
        is_correct=is_correct,
    )

    attempt_count = row["attempt_count"]
    correct_count = row["correct_attempt_count"]
    already_mastered = row["is_mastered"]

    newly_mastered = False
    new_is_mastered = already_mastered

    if not already_mastered and attempt_count >= 3:
        accuracy = correct_count / attempt_count
        if accuracy >= 0.80:
            await set_mastered(db, user_id, vocabulary_word_id)
            new_is_mastered = True
            newly_mastered = True

            difficulty = await get_vocabulary_word_difficulty(db, vocabulary_word_id)
            xp = await xp_service.lookup(db, "word_learned", difficulty)
            if xp > 0:
                await xp_service.award(
                    db,
                    user_id=user_id,
                    action_type="word_learned",
                    xp_delta=xp,
                    reference_id=vocabulary_word_id,
                    reference_type="vocabulary_word",
                )

    return MasteryResult(
        attempt_count=attempt_count,
        correct_attempt_count=correct_count,
        is_mastered=new_is_mastered,
        newly_mastered=newly_mastered,
    )
