"""Lesson 2 content enrichment — 15 missing vocabulary words (with group headers),
Short Forms grammar block, 17 assessment questions (fill_blank_options +
mcq_long_short_form), 2 Extra Practice questions, and a self_check block.

All content derived from docs/lesson-samples/lesson 2.pdf.  Phase 2+ sections
(Pronunciation, Listening, Reading, Speaking, Writing) are deferred.

Revision ID: 5f4e3d2c1b0a
Revises:     8c7b6a5d4e3f
Create Date: 2026-06-09
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import insert_content_block, insert_question, insert_word_card
from sqlalchemy import text

revision: str = "5f4e3d2c1b0a"
down_revision: Union[str, None] = "8c7b6a5d4e3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _get_section_ids(bind):
    """Return (l2_vocab_sec_id, l2_gram_sec_id) for Beginner A Lesson 2."""
    row = bind.execute(text("""
        SELECT
            MAX(CASE WHEN ls.category = 'vocabulary' THEN ls.id::text END) AS vocab_sec_id,
            MAX(CASE WHEN ls.category = 'grammar'    THEN ls.id::text END) AS gram_sec_id
        FROM lesson l
        JOIN level lv          ON lv.id = l.level_id
        JOIN lesson_section ls ON ls.lesson_id = l.id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 2
        GROUP BY l.id
    """)).fetchone()
    assert row and row.vocab_sec_id and row.gram_sec_id, (
        "Beginner A Lesson 2 section IDs not found — run 0002 first"
    )
    return str(row.vocab_sec_id), str(row.gram_sec_id)


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    vocab_sec_id, gram_sec_id = _get_section_ids(bind)

    # =========================================================================
    # A — 15 missing vocabulary words + word_card content blocks + group headers
    # display_order 10–27 (0–9 used by 0002)
    # =========================================================================

    # Each tuple: (display_order, block_type, word_or_None, definition, example, header_markdown)
    vocab_items = [
        # Family group (no header — continuing naturally from 0002 words)
        (10, "word_card", "parents",  "Father and mother.",
         "My parents are kind.", None),
        (11, "word_card", "children", "Sons and daughters.",
         "They are my children.", None),
        # Possessive Adjectives group
        (12, "text",      None,       None, None,
         "### Possessive Adjectives"),
        (13, "word_card", "my",       "Belongs to me.",
         "This is my father.", None),
        (14, "word_card", "your",     "Belongs to you.",
         "Is this your brother?", None),
        (15, "word_card", "his",      "Belongs to a male.",
         "His sister is kind.", None),
        (16, "word_card", "her",      "Belongs to a female.",
         "Her grandmother is old.", None),
        # Appearance Adjectives group
        (17, "text",      None,       None, None,
         "### Appearance Adjectives"),
        (18, "word_card", "tall",     "Having a great height.",
         "My father is tall.", None),
        (19, "word_card", "short",    "Not tall.",
         "My mother is short.", None),
        (20, "word_card", "big",      "Large in size.",
         "It is a big family.", None),
        (21, "word_card", "small",    "Not big.",
         "She is small.", None),
        (22, "word_card", "young",    "Not old.",
         "My cousin is young.", None),
        (23, "word_card", "old",      "Having many years.",
         "My grandfather is old.", None),
        (24, "word_card", "kind",     "Nice and caring.",
         "My parents are kind.", None),
        # People Words group
        (25, "text",      None,       None, None,
         "### People Words"),
        (26, "word_card", "he",       "Used for a male.",
         "He is my uncle.", None),
        (27, "word_card", "she",      "Used for a female.",
         "She is my aunt.", None),
    ]

    for (disp_order, btype, word, defn, example, header_md) in vocab_items:
        if btype == "text":
            insert_content_block(
                vocab_sec_id, "text", disp_order,
                {"markdown": header_md}, str(uuid7()),
            )
        else:
            insert_word_card(
                bind, vocab_sec_id, disp_order,
                word, defn, example, str(uuid7()), str(uuid7()),
            )

    # =========================================================================
    # B — Grammar: Short Forms text block (display_order 1)
    # existing text block is at display_order 0 — no conflict
    # =========================================================================
    short_forms_md = (
        "## Short Forms (Natural English)\n\n"
        "| Long Form    | Short Form |\n"
        "|--------------|------------|\n"
        "| He is        | He's       |\n"
        "| She is       | She's      |\n"
        "| He is not    | He isn't   |\n"
        "| She is not   | She isn't  |\n\n"
        "**Examples:**\n\n"
        "- He's my uncle.\n"
        "- She's tall.\n"
        "- He isn't short."
    )
    insert_content_block(
        gram_sec_id, "text", 1, {"markdown": short_forms_md}, str(uuid7()),
    )

    # =========================================================================
    # C — Grammar: 17 assessment questions
    # Set A (fill_blank_options, display_order 6–15)
    # Set B (mcq_long_short_form short form, display_order 16–19)
    # Set C (mcq_long_short_form long form, display_order 20–22)
    # =========================================================================

    # Set A — choose the correct possessive adjective or noun
    set_a = [
        (6,  "This is ___ father.",
         [{"id": "a", "text": "my"}, {"id": "b", "text": "me"}], "a",
         "Correct! 'My' shows it belongs to you.",
         "Use 'my' (not 'me') before a noun: 'This is my father.'"),
        (7,  "She is ___ sister.",
         [{"id": "a", "text": "her"}, {"id": "b", "text": "she"}], "a",
         "Correct! 'Her' is the possessive form.",
         "Use 'her' before a noun. 'She' is a subject pronoun."),
        (8,  "He is ___ uncle.",
         [{"id": "a", "text": "his"}, {"id": "b", "text": "he"}], "a",
         "Correct! 'His' shows it belongs to him.",
         "Use 'his' before a noun. 'He' is a subject pronoun."),
        (9,  "This is ___ family.",
         [{"id": "a", "text": "your"}, {"id": "b", "text": "you"}], "a",
         "Correct! 'Your' is the possessive form of 'you'.",
         "Use 'your' before a noun. 'You' is a pronoun."),
        (10, "My grandmother is ___.",
         [{"id": "a", "text": "old"}, {"id": "b", "text": "young"}], "a",
         "Correct! Grandmothers are old.",
         "'Old' is the right word for a grandmother in this context."),
        (11, "These are my ___.",
         [{"id": "a", "text": "parents"}, {"id": "b", "text": "parent"}], "a",
         "Correct! 'Parents' is the plural — father and mother.",
         "Two people = plural. Use 'parents', not 'parent'."),
        (12, "Is this ___ aunt?",
         [{"id": "a", "text": "her"}, {"id": "b", "text": "she"}], "a",
         "Correct! 'Her' is the possessive form.",
         "Use 'her' before a noun. 'She' is a subject pronoun."),
        (13, "He is ___ grandfather.",
         [{"id": "a", "text": "his"}, {"id": "b", "text": "him"}], "a",
         "Correct! 'His' shows it belongs to him.",
         "Use 'his' before a noun. 'Him' is an object pronoun."),
        (14, "This is ___ mother.",
         [{"id": "a", "text": "my"}, {"id": "b", "text": "I"}], "a",
         "Correct! 'My' shows it belongs to you.",
         "Use 'my' before a noun. 'I' is a subject pronoun."),
        (15, "Are these ___ children?",
         [{"id": "a", "text": "your"}, {"id": "b", "text": "you"}], "a",
         "Correct! 'Your' is the possessive form.",
         "Use 'your' before a noun. 'You' is a pronoun."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_a:
        payload = {
            "sentence_with_blank": blank_sentence,
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence, payload, 5, str(uuid7()),
        )

    # Set B — choose the correct short form
    set_b = [
        (16, "He is my brother.",
         [{"id": "a", "text": "He's my brother."}, {"id": "b", "text": "Hes my brother."}], "a",
         "Correct! 'He is' shortens to 'He's'.",
         "'He is' → 'He's' (with apostrophe). 'Hes' is not correct."),
        (17, "She is tall.",
         [{"id": "a", "text": "She's tall."}, {"id": "b", "text": "Shes tall."}], "a",
         "Correct! 'She is' shortens to 'She's'.",
         "'She is' → 'She's'. The apostrophe replaces the missing letter."),
        (18, "He is not old.",
         [{"id": "a", "text": "He isn't old."}, {"id": "b", "text": "He isnt old."}], "a",
         "Correct! 'He is not' shortens to 'He isn't'.",
         "'He is not' → 'He isn't'. The apostrophe is between 's' and 't'."),
        (19, "She is my aunt.",
         [{"id": "a", "text": "She's my aunt."}, {"id": "b", "text": "Shes my aunt."}], "a",
         "Correct! 'She is' shortens to 'She's'.",
         "'She is' → 'She's'. Always use the apostrophe."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_b:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # Set C — choose the correct long form
    set_c = [
        (20, "She's my cousin.",
         [{"id": "a", "text": "She is my cousin."}, {"id": "b", "text": "She are my cousin."}], "a",
         "Correct! 'She's' expands to 'She is'.",
         "'She's' is short for 'She is'. 'She are' is never correct."),
        (21, "He's tall.",
         [{"id": "a", "text": "He is tall."}, {"id": "b", "text": "He are tall."}], "a",
         "Correct! 'He's' expands to 'He is'.",
         "'He's' is short for 'He is'. 'He are' is never correct."),
        (22, "He isn't my brother.",
         [{"id": "a", "text": "He is not my brother."}, {"id": "b", "text": "He are not my brother."}], "a",
         "Correct! 'He isn't' expands to 'He is not'.",
         "'He isn't' is short for 'He is not'. 'He are not' is never correct."),
    ]
    for (disp, prompt, options, correct_id, fb_c, fb_i) in set_c:
        payload = {
            "options": options,
            "correct_option_id": correct_id,
            "feedback": {"correct": fb_c, "incorrect": fb_i},
        }
        insert_question(
            gram_sec_id, "mcq_long_short_form", "assessment", disp,
            prompt, payload, 5, str(uuid7()),
        )

    # =========================================================================
    # D — Grammar: Extra Practice questions (purpose=practice, xp=0)
    # display_order 23–24
    # =========================================================================
    insert_question(
        gram_sec_id, "fill_blank_options", "practice", 23,
        "She is ___ sister.",
        {
            "sentence_with_blank": "She is ___ sister.",
            "options": [{"id": "a", "text": "her"}, {"id": "b", "text": "she"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'Her' is the possessive form.",
                "incorrect": "Use 'her' before a noun.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        gram_sec_id, "fill_blank_options", "practice", 24,
        "These are ___ parents.",
        {
            "sentence_with_blank": "These are ___ parents.",
            "options": [{"id": "a", "text": "my"}, {"id": "b", "text": "me"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! 'My' shows they belong to you.",
                "incorrect": "Use 'my' before a noun. 'Me' is an object pronoun.",
            },
        },
        0, str(uuid7()),
    )

    # =========================================================================
    # E — Grammar: Self-check block (display_order 99 — rendered last)
    # =========================================================================
    insert_content_block(
        gram_sec_id, "self_check", 99,
        {
            "prompt": "Can you say this without reading?",
            "text": (
                "This is my family.\n"
                "My parents are kind.\n"
                "Her daughter is my cousin."
            ),
        },
        str(uuid7()),
    )


def downgrade() -> None:
    bind = op.get_bind()
    vocab_sec_id, gram_sec_id = _get_section_ids(bind)

    new_words = (
        "parents", "children", "my", "your", "his", "her",
        "tall", "short", "big", "small", "young", "old", "kind", "he", "she",
    )
    words_list = ", ".join(_s(w) for w in new_words)
    op.execute(f"""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id = '{vocab_sec_id}'
          AND word IN ({words_list})
    """)

    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id = '{vocab_sec_id}'
          AND display_order BETWEEN 10 AND 27
    """)

    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id = '{gram_sec_id}'
          AND display_order IN (1, 99)
    """)

    op.execute(f"""
        DELETE FROM question
        WHERE lesson_section_id = '{gram_sec_id}'
          AND display_order BETWEEN 6 AND 24
    """)
