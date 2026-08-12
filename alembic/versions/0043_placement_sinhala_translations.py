"""Backfill Sinhala prompt translations for the 17 placement questions.

Task #24 Phase B1 (kingguru-task24-placement-lessons-production-plan.md §3):
the `translations` JSONB column and the API pass-through both exist, but all
17 rows carried `{}`. This seeds `{"si": {"prompt_text": ...}}` per question.

Scope per Nisal: QUESTION prompts only — options stay English. Where the
English term is itself the thing being tested (e.g. "sandwich", "child",
"cheap"), it stays in English inside the Sinhala sentence so the translation
never gives the answer away. For blank-completion prompts that carry no
English instruction, the Sinhala line supplies the instruction ("choose the
word that fits the blank") instead of translating the test sentence.

Keyed by exact `prompt_text` (unique across the bank) rather than id —
question ids are regenerated per-database by the seed migrations, and two
prompts were later edited directly in the prod DB (Task #17b), so prompt
text is the only key that is both stable and content-verified. Rows whose
prompt doesn't match exactly are left untouched (safe no-op), and rows that
already have an "si" translation are skipped (idempotent / re-runnable).

Revision ID: 7c4d5e6f8a9b
Revises:     6b3c4d5e6f7a
Create Date: 2026-07-13
"""
import json
from typing import Sequence, Union

from alembic import op

revision: str = "7c4d5e6f8a9b"
down_revision: Union[str, None] = "6b3c4d5e6f7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


# (exact live prompt_text, Sinhala prompt rendering)
_TRANSLATIONS = [
    (
        "Which one of these is a sandwich?",
        "මේවායින් 'sandwich' එකක් වන්නේ කුමක්ද?",
    ),
    (
        "'I am a student' is a correct English sentence.",
        "'I am a student' යනු නිවැරදි ඉංග්‍රීසි වාක්‍යයකි.",
    ),
    (
        "Choose the correct word: ___ name is Saman.",
        "නිවැරදි වචනය තෝරන්න: ___ name is Saman.",
    ),
    (
        "What is the plural of 'child'?",
        "'child' යන වචනයේ බහුවචනය කුමක්ද?",
    ),
    (
        "Which sentence is correct?",
        "නිවැරදි වාක්‍යය කුමක්ද?",
    ),
    (
        "The past tense of 'go' is 'goed'.",
        "'go' යන වචනයේ අතීත කාලය 'goed' වේ.",
    ),
    (
        "She ___ to school every morning.",
        "හිස්තැනට ගැලපෙන වචනය තෝරන්න.",
    ),
    (
        "Complete the sentence: If it rains, I _____ an umbrella.",
        "වාක්‍යය සම්පූර්ණ කරන්න: If it rains, I _____ an umbrella.",
    ),
    (
        "Which word means the opposite of 'cheap'?",
        "'cheap' යන වචනයේ විරුද්ධ පදය කුමක්ද?",
    ),
    (
        "By the time she arrived, the meeting ___ already started.",
        "හිස්තැනට ගැලපෙන වචනය තෝරන්න.",
    ),
    (
        "Despite the rain, they _____ to complete the project on time.",
        "හිස්තැන සම්පූර්ණ කරන්න.",
    ),
    (
        "Which sentence uses the passive voice correctly?",
        "Passive voice (කර්මකාරක) නිවැරදිව භාවිතා කරන වාක්‍යය කුමක්ද?",
    ),
    (
        "I wish I ___ more time to study when I was young.",
        "හිස්තැනට ගැලපෙන පිළිතුර තෝරන්න.",
    ),
    (
        "Choose the word that best completes the sentence: The politician's speech "
        "was deliberately _____, avoiding any clear commitment.",
        "වාක්‍යයට වඩාත්ම ගැලපෙන වචනය තෝරන්න: The politician's speech was "
        "deliberately _____, avoiding any clear commitment.",
    ),
    (
        "Select the sentence that uses the mandative subjunctive correctly.",
        "Mandative subjunctive නිවැරදිව භාවිතා වන වාක්‍යය තෝරන්න.",
    ),
    (
        "Which one is an apple?",
        "මේවායින් 'apple' එකක් වන්නේ කුමක්ද?",
    ),
    (
        "Which word is a greeting?",
        "ආචාර කිරීමට යොදන වචනය කුමක්ද?",
    ),
]


def upgrade() -> None:
    for prompt_text, si_prompt in _TRANSLATIONS:
        si_json = json.dumps({"prompt_text": si_prompt}, ensure_ascii=False)
        op.execute(
            f"""
            UPDATE placement_question
            SET translations = jsonb_set(
                    COALESCE(translations, '{{}}'::jsonb),
                    '{{si}}',
                    {_s(si_json)}::jsonb
                ),
                updated_at = now()
            WHERE prompt_text = {_s(prompt_text)}
              AND NOT (COALESCE(translations, '{{}}'::jsonb) ? 'si')
            """
        )


def downgrade() -> None:
    op.execute("UPDATE placement_question SET translations = translations - 'si'")
