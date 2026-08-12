"""Lesson 5 — Colors, Clothing & Adjectives (full Phase 1 seed).

Creates Lesson 5 from scratch: lesson row, vocabulary section (16 words across
two groups: Colors and Clothing Items), and grammar section (3 teaching blocks,
10 assessment questions across three question types, 2 practice questions,
self_check block).

Phase 2+ sections deferred:
- Pronunciation Practice (Listen & Repeat AI)
- Listening Practice (audio-dependent dialogue + picture selection)
- Reading Practice (passage + 27 comprehension questions)
- Speaking Practice
- Writing sections that require images (Choose & Write, Describe the Picture)

Phase 1 included from Writing section:
- Sentence Builder (tap-to-order) — sentence_builder type ✓
- Correct the Sentence — correct_mistake type ✓

Revision ID: 1b0a9f8e7d6c
Revises:     2c1b0a9f8e7d
Create Date: 2026-06-09
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import (
    ensure_lesson,
    ensure_section,
    insert_content_block,
    insert_question,
    insert_word_card,
)
from sqlalchemy import text

revision: str = "1b0a9f8e7d6c"
down_revision: Union[str, None] = "2c1b0a9f8e7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


def _s(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_a'")).fetchone()
    assert row, "beginner_a level not found — run 0002 first"
    level_id = str(row[0])

    # =========================================================================
    # Create Lesson 5
    # =========================================================================
    l5_id = ensure_lesson(
        bind, level_id, 5,
        "Colors, Clothing & Adjectives",
        "Learn colors and clothing vocabulary, and describe what people are wearing.",
        str(uuid7()),
    )
    l5_vocab_sec_id = ensure_section(
        bind, l5_id, "vocabulary", 1, "Vocabulary", str(uuid7()),
    )
    l5_gram_sec_id = ensure_section(
        bind, l5_id, "grammar", 2, "Grammar", str(uuid7()),
    )

    # =========================================================================
    # A — Vocabulary: objectives block (display_order 0)
    # =========================================================================
    obj_md = (
        "## Lesson Objectives\n\n"
        "By the end of this lesson you will be able to:\n\n"
        "- Identify and use vocabulary for colors and common clothing items\n"
        "- Use singular and plural nouns correctly in basic sentences\n"
        "- Use adjectives to describe clothing and colors accurately\n"
        "- Describe what people are wearing using simple sentences"
    )
    insert_content_block(
        l5_vocab_sec_id, "text", 0, {"markdown": obj_md}, str(uuid7()),
    )

    # =========================================================================
    # B — Vocabulary: Colors (display_order 1–9)
    # =========================================================================
    insert_content_block(
        l5_vocab_sec_id, "text", 1, {"markdown": "### Colors"}, str(uuid7()),
    )

    colors = [
        (2,  "red",    "A warm, bright color like fire or blood.",     "She is wearing a red dress."),
        (3,  "blue",   "A cool color like the sky or the sea.",        "He is wearing a blue shirt."),
        (4,  "green",  "The color of leaves and grass.",               "Kasun is wearing a green T-shirt."),
        (5,  "yellow", "A bright color like the sun.",                 "She is wearing a yellow dress."),
        (6,  "black",  "The darkest color, like the night sky.",       "His shoes are black."),
        (7,  "white",  "The lightest color, like snow or milk.",       "He is wearing a white hat."),
        (8,  "pink",   "A light, soft red color.",                     "She is wearing a pink dress."),
        (9,  "brown",  "A warm, earthy color like wood or soil.",      "He is wearing brown shoes."),
    ]
    for (disp, word, defn, example) in colors:
        insert_word_card(
            bind, l5_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # C — Vocabulary: Clothing Items (display_order 10–18)
    # =========================================================================
    insert_content_block(
        l5_vocab_sec_id, "text", 10, {"markdown": "### Clothing Items"}, str(uuid7()),
    )

    clothing = [
        (11, "shirt",    "A piece of clothing worn on the upper body, often with buttons.", "Nimal is wearing a blue shirt."),
        (12, "t-shirt",  "A casual top with short sleeves and no buttons.",                 "Kasun is wearing a green T-shirt."),
        (13, "trousers", "Long clothing that covers both legs.",                            "He is wearing black trousers."),
        (14, "dress",    "A one-piece item that covers from the shoulders to the legs.",    "She is wearing a red dress."),
        (15, "shoes",    "Hard footwear worn on the feet for walking.",                     "His shoes are black."),
        (16, "hat",      "A covering worn on the head for style or sun protection.",        "He is wearing a white hat."),
        (17, "skirt",    "A piece of clothing worn around the waist that hangs down.",      "She is wearing a pink skirt."),
        (18, "socks",    "Soft fabric coverings worn on the feet inside shoes.",            "He is wearing white socks."),
    ]
    for (disp, word, defn, example) in clothing:
        insert_word_card(
            bind, l5_vocab_sec_id, disp, word, defn, example,
            str(uuid7()), str(uuid7()),
        )

    # =========================================================================
    # D — Grammar: 3 teaching text blocks (display_order 0–2)
    # =========================================================================

    # Block 0: Singular & Plural Nouns
    plural_md = (
        "## Singular & Plural Nouns\n\n"
        "**Singular** → one item\n"
        "**Plural** → more than one\n\n"
        "**Most nouns: add -s**\n\n"
        "- shirt → shirts\n"
        "- shoe → shoes\n"
        "- hat → hats\n"
        "- skirt → skirts\n\n"
        "**Nouns ending in -s, -sh, -ch, -x, -z: add -es**\n\n"
        "- dress → dresses\n\n"
        "**Examples:**\n\n"
        "- This is a shirt. → These are shirts.\n"
        "- That is a shoe. → Those are shoes.\n"
        "- This is a dress. → These are dresses."
    )
    insert_content_block(
        l5_gram_sec_id, "text", 0, {"markdown": plural_md}, str(uuid7()),
    )

    # Block 1: Adjectives Before Nouns
    adj_md = (
        "## Adjectives Before Nouns\n\n"
        "Put the color or describing word **before** the noun (object).\n\n"
        "**Structure:** Adjective + Noun\n\n"
        "| Singular | Plural |\n"
        "|----------|--------|\n"
        "| a **red** shirt | **red** shirts |\n"
        "| a **blue** dress | **blue** dresses |\n"
        "| a **black** shoe | **black** shoes |\n"
        "| a **white** hat | **white** hats |\n\n"
        "**Note:** The adjective does **not** change for singular or plural.\n\n"
        "- a red shirt → red shirts *(not reds shirts)*"
    )
    insert_content_block(
        l5_gram_sec_id, "text", 1, {"markdown": adj_md}, str(uuid7()),
    )

    # Block 2: Using "is wearing"
    wearing_md = (
        "## Using \"is wearing\"\n\n"
        "**Structure:** Subject + am/is/are + wearing + adjective + clothing\n\n"
        "| Subject | Verb | |\n"
        "|---------|------|-|\n"
        "| I | am wearing | a red shirt. |\n"
        "| He / She | is wearing | black shoes. |\n"
        "| They / We | are wearing | white socks. |\n\n"
        "**Examples:**\n\n"
        "- She is wearing a red dress.\n"
        "- He is wearing black shoes.\n"
        "- They are wearing white shirts.\n\n"
        "**Negative:**\n\n"
        "- She is not wearing a hat. *(She isn't wearing a hat.)*\n"
        "- They are not wearing green shoes. *(They aren't wearing green shoes.)*\n\n"
        "**Questions:**\n\n"
        "- What is she wearing? → She is wearing a red dress.\n"
        "- What color are his shoes? → They are black."
    )
    insert_content_block(
        l5_gram_sec_id, "text", 2, {"markdown": wearing_md}, str(uuid7()),
    )

    # =========================================================================
    # E — Grammar: Set A — Choose am / is / are (2 fill_blank_options, 3 options)
    # display_order 4–5, assessment, xp=5
    # =========================================================================
    set_a = [
        (4, "She ___ wearing a red dress.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "is"}, {"id": "c", "text": "are"}], "b",
         "Correct! Use 'is' with she/he/it.",
         "Use 'is' with 'she' — I am, she/he is, they/we are."),
        (5, "They ___ wearing white shirts.",
         [{"id": "a", "text": "am"}, {"id": "b", "text": "is"}, {"id": "c", "text": "are"}], "c",
         "Correct! Use 'are' with they/we.",
         "Use 'are' with 'they' — I am, she/he is, they/we are."),
    ]
    for (disp, blank_sentence, options, correct_id, fb_c, fb_i) in set_a:
        insert_question(
            l5_gram_sec_id, "fill_blank_options", "assessment", disp,
            blank_sentence,
            {
                "sentence_with_blank": blank_sentence,
                "options": options,
                "correct_option_id": correct_id,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    # =========================================================================
    # F — Grammar: Set B — Sentence Builder (4 sentence_builder questions)
    # display_order 6–9, assessment, xp=5
    # From Writing Practice — Sentence Builder section of the lesson PDF
    # =========================================================================
    set_b = [
        (6,
         "Put the words in the correct order.",
         ["She", "is", "wearing", "a", "yellow", "dress"],
         ["He", "are", "blue"],
         "She is wearing a yellow dress.",
         "Correct! Subject + is wearing + adjective + noun.",
         "Remember: She is wearing a yellow dress."),
        (7,
         "Put the words in the correct order.",
         ["He", "is", "wearing", "black", "shoes"],
         ["She", "are", "red", "hat"],
         "He is wearing black shoes.",
         "Correct! Subject + is wearing + color + noun.",
         "Remember: He is wearing black shoes."),
        (8,
         "Put the words in the correct order.",
         ["These", "are", "blue", "socks"],
         ["This", "is", "black", "hat"],
         "These are blue socks.",
         "Correct! 'These' is plural — use 'are'.",
         "Remember: These are blue socks. (plural → are)"),
        (9,
         "Put the words in the correct order.",
         ["That", "is", "a", "white", "hat"],
         ["Those", "are", "red", "dress"],
         "That is a white hat.",
         "Correct! 'That' is singular — use 'is'.",
         "Remember: That is a white hat. (singular → is)"),
    ]
    for (disp, prompt, words, distractors, answer, fb_c, fb_i) in set_b:
        insert_question(
            l5_gram_sec_id, "sentence_builder", "assessment", disp,
            prompt,
            {
                "words": words,
                "distractors": distractors,
                "correct_answer": answer,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    # =========================================================================
    # G — Grammar: Set C — Correct the Mistake (4 correct_mistake questions)
    # display_order 10–13, assessment, xp=5
    # From Writing Practice — Correct the Sentence section of the lesson PDF
    # =========================================================================
    set_c = [
        (10,
         "She wearing a red dress.",
         ["She is wearing a red dress."],
         "Correct! The verb 'is' was missing.",
         "The verb 'is' is missing — the correct form is 'She is wearing'."),
        (11,
         "He is wearing a black shoe.",
         ["He is wearing black shoes."],
         "Correct! Use the plural 'shoes' — two shoes, not one.",
         "Use the plural 'shoes' — people wear two shoes, not one."),
        (12,
         "These is blue socks.",
         ["These are blue socks."],
         "Correct! 'These' is plural — use 'are', not 'is'.",
         "'These' is plural — use 'are', not 'is'."),
        (13,
         "That are a white hat.",
         ["That is a white hat."],
         "Correct! 'That' is singular — use 'is', not 'are'.",
         "'That' is singular — use 'is', not 'are'."),
    ]
    for (disp, wrong, accepted, fb_c, fb_i) in set_c:
        insert_question(
            l5_gram_sec_id, "correct_mistake", "assessment", disp,
            wrong,
            {
                "wrong_sentence": wrong,
                "accepted_corrections": accepted,
                "feedback": {"correct": fb_c, "incorrect": fb_i},
            },
            5, str(uuid7()),
        )

    # =========================================================================
    # H — Grammar: Extra Practice (2 questions, purpose=practice, xp=0)
    # display_order 14–15
    # =========================================================================
    # match_pairs: categorise words (from "Quick Challenge" section of PDF)
    insert_question(
        l5_gram_sec_id, "match_pairs", "practice", 14,
        "Match each word to its correct category.",
        {
            "pairs": [
                {"id": "p1", "left": "Pink",     "right": "Color"},
                {"id": "p2", "left": "Trousers", "right": "Clothing"},
                {"id": "p3", "left": "Wearing",  "right": "Action"},
                {"id": "p4", "left": "Hats",     "right": "Plural"},
            ],
            "display_shuffle": True,
            "feedback": {
                "correct": "Well matched!",
                "incorrect": "Try again — match each word to Color, Clothing, Action, or Plural.",
            },
        },
        0, str(uuid7()),
    )

    insert_question(
        l5_gram_sec_id, "fill_blank_options", "practice", 15,
        "She is wearing a ___ dress.",
        {
            "sentence_with_blank": "She is wearing a ___ dress.",
            "options": [{"id": "a", "text": "red"}, {"id": "b", "text": "blue"}],
            "correct_option_id": "a",
            "feedback": {
                "correct": "Correct! She is wearing a red dress.",
                "incorrect": "The dress is red, not blue.",
            },
        },
        0, str(uuid7()),
    )

    # =========================================================================
    # I — Grammar: Self-check block (display_order 99)
    # =========================================================================
    insert_content_block(
        l5_gram_sec_id, "self_check", 99,
        {
            "prompt": "Can you say this without reading?",
            "text": (
                "She is wearing a red dress.\n"
                "He is wearing black shoes.\n"
                "These are blue socks.\n"
                "That is a white hat."
            ),
        },
        str(uuid7()),
    )


def downgrade() -> None:
    bind = op.get_bind()

    row = bind.execute(text("""
        SELECT l.id::text
        FROM lesson l
        JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_a' AND l.lesson_order = 5
    """)).fetchone()
    if not row:
        return
    lesson_id = row[0]

    op.execute(f"""
        DELETE FROM question
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"""
        DELETE FROM vocabulary_word
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"""
        DELETE FROM content_block
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = '{lesson_id}'
        )
    """)
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id = '{lesson_id}'")
    op.execute(f"DELETE FROM lesson WHERE id = '{lesson_id}'")
