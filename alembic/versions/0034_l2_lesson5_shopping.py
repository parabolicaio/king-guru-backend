"""Beginner B — Lesson 5: Food, Shopping & Quantifiers (Level 2 seed).

Seeds beginner_b Lesson 5 from LEVEL 2 Lesson 5.docx (7 sections). This is the
first Level 2 lesson with a "Review Corner" recapping earlier lessons; per the
content team's design it opens each lesson from 5 onward. The DB schema has no
'review' section category, so the Review Corner is seeded as leading
purpose='practice' (xp=0) questions in the grammar section — the frontend only
counts purpose='assessment' toward progress, so review recall does not distort
scoring. Text-only scope; audio activities deferred. Sinhala from the .docx.

Revision ID: 2e5f6a7b8c9d
Revises:     2d4e5f6a7b8c
Create Date: 2026-07-04
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import (
    ensure_lesson,
    ensure_section,
    insert_content_block,
    insert_question,
    insert_word_card_tr,
)
from sqlalchemy import text

revision: str = "2e5f6a7b8c9d"
down_revision: Union[str, None] = "2d4e5f6a7b8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use food and shopping vocabulary in context",
    "Use quantifiers (some, any, much, many, a lot of)",
    "Ask and answer about prices",
    "Understand simple shopping conversations",
    "Role-play buying items in a shop",
    "Write a shopping list or shopping dialogue",
]
OBJECTIVES_SI = [
    "ආහාර හා සාප්පු වචන සන්දර්භය තුළ භාවිතා කිරීම",
    "quantifiers (some, any, much, many, a lot of) භාවිතා කිරීම",
    "මිල ගැන අසා පිළිතුරු දීම",
    "සරල සාප්පු සංවාද තේරුම් ගැනීම",
    "කඩයක බඩු මිලදී ගැනීම role-play කිරීම",
    "සාප්පු ලැයිස්තුවක් හෝ සංවාදයක් ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 5, "Food, Shopping & Quantifiers",
                         "Shop for food using some, any, much and many, and ask about prices.", str(uuid7()))
    op.execute(f"UPDATE lesson SET objectives={_j(OBJECTIVES)}, "
               f"objectives_translations={_j({'si': OBJECTIVES_SI})} WHERE id='{l_id}'")

    vocab = ensure_section(bind, l_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram  = ensure_section(bind, l_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron  = ensure_section(bind, l_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    listn = ensure_section(bind, l_id, "listening",     4, "Listening",     str(uuid7()))
    read  = ensure_section(bind, l_id, "reading",       5, "Reading",       str(uuid7()))
    speak = ensure_section(bind, l_id, "speaking",      6, "Speaking",      str(uuid7()))
    write = ensure_section(bind, l_id, "writing",       7, "Writing",       str(uuid7()))

    # VOCABULARY
    insert_content_block(vocab, "text", 0, {"type": "plain",
        "text": "Learn food and shopping words, and the quantifiers we use with them."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Food"}, str(uuid7()))
    food = [
        (2, "Rice",       "බත්",       "A grain eaten as a main food.",  "We eat rice every day."),
        (3, "Bread",      "පාන්",      "A baked food from flour.",       "I bought some bread."),
        (4, "Egg",        "බිත්තර",    "A food from a hen.",             "I ate two eggs."),
        (5, "Vegetables", "එළවළු",     "Plants we eat.",                 "I like fresh vegetables."),
        (6, "Sugar",      "සීනි",      "A sweet white food.",            "There is some sugar in the tea."),
        (7, "Cake",       "කේක්",      "A sweet baked food.",            "We bought a cake."),
    ]
    for (d, w, si, defn, ex) in food:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 8, {"type": "heading", "text": "Shopping"}, str(uuid7()))
    shop = [
        (9,  "Customer", "පාරිභෝගිකයා", "A person who buys things.",     "The customer paid the cashier."),
        (10, "Cashier",  "මුදල් අයකැමි", "The person who receives money.", "The cashier gave a receipt."),
        (11, "Price",    "මිල",         "The cost of an item.",          "What is the price of the milk?"),
        (12, "Receipt",  "රිසිට්පත",    "Proof of payment.",             "The cashier gave me a receipt."),
        (13, "Buy",      "මිලදී ගන්නවා", "Get something for money.",      "I want to buy some apples."),
    ]
    for (d, w, si, defn, ex) in shop:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 14, "Match the shopping word to its meaning", {
        "pairs": [
            {"id": "p1", "left": "Customer", "right": "Person who buys things"},
            {"id": "p2", "left": "Cashier", "right": "Person who receives money"},
            {"id": "p3", "left": "Receipt", "right": "Proof of payment"},
            {"id": "p4", "left": "Price", "right": "Cost of an item"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match each word to its meaning."},
    }, 10, str(uuid7()))

    # GRAMMAR — Review Corner first (practice), then new grammar (assessment)
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner"}, str(uuid7()))
    insert_content_block(gram, "text", 1, {"type": "plain",
        "text": ("Before we start, let's review past simple and prepositions from earlier lessons.")}, str(uuid7()))
    review = [
        (2, "Yesterday, I ______ to the supermarket.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}, {"id": "c", "text": "going"}], "a",
         "Correct! go → went.", "Past of go is 'went'."),
        (3, "Then, I ______ some apples.",
         [{"id": "a", "text": "bought"}, {"id": "b", "text": "buy"}, {"id": "c", "text": "buying"}], "a",
         "Correct! buy → bought.", "Past of buy is 'bought'."),
        (4, "The pharmacy is ______ the bank.",
         [{"id": "a", "text": "next to"}, {"id": "b", "text": "bought"}, {"id": "c", "text": "yesterday"}], "a",
         "Correct! A place word — 'next to'.", "Use the preposition 'next to'."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 5, {"type": "heading", "text": "Some, Any, Much & Many"}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "plain",
        "text": ("Use SOME in positive sentences (I have some apples) and ANY in questions and "
                 "negatives (Do you have any milk? / I don't have any milk). Use MANY with countable "
                 "nouns (many apples) and MUCH with uncountable nouns (much rice). A LOT OF works with "
                 "both.")}, str(uuid7()))
    insert_content_block(gram, "text", 7, {"type": "example_cards", "label": "Asking About Prices",
        "sentences": ["How much is the milk? — It is 450 rupees.",
                      "How much are the apples? — They are 200 rupees."]}, str(uuid7()))
    g = [
        (8, "I have ______ apples.",
         [{"id": "a", "text": "some"}, {"id": "b", "text": "any"}], "a",
         "Correct! Positive sentence → 'some'.", "Positive sentences use 'some'."),
        (9, "Do you have ______ milk?",
         [{"id": "a", "text": "any"}, {"id": "b", "text": "some"}], "a",
         "Correct! Question → 'any'.", "Questions use 'any'."),
        (10, "I don't have ______ eggs.",
         [{"id": "a", "text": "any"}, {"id": "b", "text": "some"}], "a",
         "Correct! Negative → 'any'.", "Negatives use 'any'."),
        (11, "______ apples (countable)",
         [{"id": "a", "text": "Many"}, {"id": "b", "text": "Much"}], "a",
         "Correct! Countable → 'many'.", "Countable nouns use 'many'."),
        (12, "______ rice (uncountable)",
         [{"id": "a", "text": "Much"}, {"id": "b", "text": "Many"}], "a",
         "Correct! Uncountable → 'much'.", "Uncountable nouns use 'much'."),
        (13, "How much ______ the milk?",
         [{"id": "a", "text": "is"}, {"id": "b", "text": "are"}], "a",
         "Correct! Milk is uncountable — 'is'.", "'How much is the milk?'"),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "sentence_builder", "assessment", 14, "Put in order: much / How / milk / the / is",
                    {"items": [{"id": "c1", "text": "How"}, {"id": "c2", "text": "much"}, {"id": "c3", "text": "is"},
                               {"id": "c4", "text": "the"}, {"id": "c5", "text": "milk"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4", "c5"],
                     "feedback": {"correct": "Correct! 'How much is the milk?'", "incorrect": "How much is the milk?"}},
                    8, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Receipt", "රිසීට් — the 'p' is silent"), (2, "Vegetables", "වෙජ්ටබල්ස්"),
                       (3, "Supermarket", "සුපර්මාර්කට්")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say 'receipt' — the 'p' is silent.", "Can I have a receipt?"),
        (5, "Raise your voice at the end of the question.", "How much is it?"),
        (6, "Say the sentence clearly.", "Do you have any apples?"),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "A Shopping Trip"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Yesterday, I went to the supermarket after school. First, I bought some apples and "
                 "milk. Then, I went to the pharmacy. After that, I visited my grandmother. Finally, I "
                 "came home.")}, str(uuid7()))
    l_mcq = [
        (2, "Where did the speaker go first?", [{"id": "a", "text": "Supermarket"}, {"id": "b", "text": "Pharmacy"}], "a",
         "Correct!", "The speaker went to the supermarket first."),
        (3, "What did the speaker buy?", [{"id": "a", "text": "Apples and milk"}, {"id": "b", "text": "Rice and tea"}], "a",
         "Correct!", "The speaker bought some apples and milk."),
        (4, "Who did the speaker visit?", [{"id": "a", "text": "Grandmother"}, {"id": "b", "text": "Teacher"}], "a",
         "Correct!", "The speaker visited their grandmother."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "The speaker went to the supermarket. True or False?", True, "Correct!", "Yes — the supermarket."),
        (6, "The speaker bought milk. True or False?", True, "Correct!", "The speaker bought some milk."),
        (7, "The speaker visited a teacher. True or False?", False, "Correct! A grandmother.", "The speaker visited a grandmother."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about the shopping trip and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Last Saturday, my mother and I went to the supermarket. First, we walked to the bus "
                 "stop. Then, we went to the supermarket and bought some apples, milk, bread, and eggs. "
                 "After that, we visited my grandmother. Finally, we came home. We had a wonderful day "
                 "together.")}, str(uuid7()))
    r = [
        (2, "Where did they go?", [{"id": "a", "text": "Supermarket"}, {"id": "b", "text": "School"}], "a", "Correct!", "They went to the supermarket."),
        (3, "How did they travel first?", [{"id": "a", "text": "Walk"}, {"id": "b", "text": "Train"}], "a", "Correct!", "They walked to the bus stop first."),
        (4, "Who did they visit?", [{"id": "a", "text": "Grandmother"}, {"id": "b", "text": "Friend"}], "a", "Correct!", "They visited grandmother."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "sentence_builder", "assessment", 5, "Sequence the story.",
                    {"items": [{"id": "c1", "text": "Walked to the bus stop"}, {"id": "c2", "text": "Bought food"},
                               {"id": "c3", "text": "Visited grandmother"}, {"id": "c4", "text": "Came home"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Walk → buy → visit → home."}}, 8, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I'd like some apples."), (2, "Can I have some milk?"),
                    (3, "How much is it?"), (4, "Do you have any eggs?")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "Can I help you?",
                                            "answer": "Yes, I'd like some apples, please."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 45 seconds about a shopping trip: where you went, what you bought, one price, "
                 "and what happened after. Use some/any and first/then/after that/finally.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences."}, str(uuid7()))
    fills = [
        (1, "Yesterday I ______ to the supermarket. (past of go)", ["went"], "Correct! went.", "Past of go is 'went'."),
        (2, "I don't have ______ milk. (some/any)", ["any"], "Correct! Negative → any.", "Negatives use 'any'."),
        (3, "How ______ is the bread? (much/many)", ["much"], "Correct! Bread is uncountable → much.", "Use 'much' for uncountable bread."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "sentence_builder", "assessment", 4, "Put in order: Can / have / I / some / apples",
                    {"items": [{"id": "c1", "text": "Can"}, {"id": "c2", "text": "I"}, {"id": "c3", "text": "have"},
                               {"id": "c4", "text": "some"}, {"id": "c5", "text": "apples"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4", "c5"],
                     "feedback": {"correct": "Correct! 'Can I have some apples?'", "incorrect": "Can I have some apples?"}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 8–10 sentences about a shopping trip. Use first/then/after that/finally, at least "
                 "2 irregular past verbs, 2 food items, some or any, and one price.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Use 'some' in positives, 'any' in questions and negatives",
                  "Use 'many' with countable nouns and 'much' with uncountable",
                  "Ask prices with 'How much is/are...?'",
                  "Order a shopping story with first, then, after that, finally"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=5
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
