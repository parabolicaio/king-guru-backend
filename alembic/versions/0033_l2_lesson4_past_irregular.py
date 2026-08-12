"""Beginner B — Lesson 4: Past Simple (Irregular Verbs & Memories) (Level 2 seed).

Seeds beginner_b Lesson 4 from LEVEL 2 Lesson 4.docx (7 sections). Text-only
scope; audio activities deferred. Sinhala from the .docx source.

Revision ID: 2d4e5f6a7b8c
Revises:     2c3d4e5f6a7b
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

revision: str = "2d4e5f6a7b8c"
down_revision: Union[str, None] = "2c3d4e5f6a7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use common irregular verbs correctly in the past simple",
    "Describe past experiences and memories",
    "Sequence past events using time markers",
    "Understand short narratives about past experiences",
    "Speak about a past event or memory",
    "Write a short paragraph about a past experience",
]
OBJECTIVES_SI = [
    "සුලභ irregular verbs past simple තුළ නිවැරදිව භාවිතා කිරීම",
    "අතීත අත්දැකීම් හා මතකයන් විස්තර කිරීම",
    "කාල සලකුණු භාවිතයෙන් සිදුවීම් අනුපිළිවෙලට තැබීම",
    "අතීත අත්දැකීම් ගැන කෙටි කතා තේරුම් ගැනීම",
    "අතීත සිදුවීමක් හෝ මතකයක් ගැන කතා කිරීම",
    "අතීත අත්දැකීමක් ගැන කෙටි ඡේදයක් ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 4, "Past Simple (Irregular Verbs & Memories)",
                         "Tell stories about the past with irregular verbs and sequence words.", str(uuid7()))
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
        "text": "Learn common irregular past verbs (they do not take -ed) and story sequence words."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Irregular Verbs (Past)"}, str(uuid7()))
    verbs = [
        (2,  "Went",   "ගියා",         "Past of go.",    "I went to the park yesterday."),
        (3,  "Ate",    "කෑවා",         "Past of eat.",   "She ate pizza last night."),
        (4,  "Saw",    "දැක්කා",       "Past of see.",   "We saw a movie."),
        (5,  "Had",    "තිබුණා",       "Past of have.",  "They had a great day."),
        (6,  "Came",   "ආවා",          "Past of come.",  "I came home late."),
        (7,  "Bought", "මිලදී ගත්තා",  "Past of buy.",   "I bought a new bag."),
        (8,  "Met",    "හමුවුණා",      "Past of meet.",  "He met his cousins."),
        (9,  "Took",   "ගත්තා",        "Past of take.",  "My father took me to Colombo."),
    ]
    for (d, w, si, defn, ex) in verbs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_content_block(vocab, "text", 10, {"type": "heading", "text": "Time Markers"}, str(uuid7()))
    markers = [
        (11, "First",      "මුලින්ම",   "The first thing.",       "First, I went to the beach."),
        (12, "Then",       "ඊට පස්සේ",  "The next thing.",        "Then, I ate lunch."),
        (13, "After that", "ඊට පසුව",   "Following that.",        "After that, I played volleyball."),
        (14, "Finally",    "අවසානයේ",   "The last thing.",        "Finally, I came home."),
    ]
    for (d, w, si, defn, ex) in markers:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_question(vocab, "match_pairs", "assessment", 15, "Match present to past", {
        "pairs": [
            {"id": "p1", "left": "go", "right": "went"},
            {"id": "p2", "left": "eat", "right": "ate"},
            {"id": "p3", "left": "see", "right": "saw"},
            {"id": "p4", "left": "buy", "right": "bought"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "These are irregular — they don't add -ed."},
    }, 10, str(uuid7()))

    # GRAMMAR
    insert_content_block(gram, "text", 0, {"type": "plain",
        "text": ("Some verbs are irregular — they do not add -ed in the past: go → went, eat → ate, "
                 "see → saw, buy → bought. We use sequence words (first, then, after that, finally) to "
                 "tell events in order.")}, str(uuid7()))
    insert_content_block(gram, "text", 1, {"type": "example_cards", "label": "Irregular Past",
        "sentences": ["I went to school.", "She ate breakfast.", "They had fun."]}, str(uuid7()))
    g = [
        (2, "Yesterday I ______ to the park.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}, {"id": "c", "text": "goed"}], "a",
         "Correct! Past of go is 'went'.", "go → went (never 'goed')."),
        (3, "She ______ lunch at school.",
         [{"id": "a", "text": "ate"}, {"id": "b", "text": "eated"}, {"id": "c", "text": "eat"}], "a",
         "Correct! Past of eat is 'ate'.", "eat → ate (never 'eated')."),
        (4, "We ______ a movie last night.",
         [{"id": "a", "text": "saw"}, {"id": "b", "text": "seed"}, {"id": "c", "text": "see"}], "a",
         "Correct! Past of see is 'saw'.", "see → saw."),
        (5, "I ______ a new bag.",
         [{"id": "a", "text": "bought"}, {"id": "b", "text": "buyed"}, {"id": "c", "text": "buy"}], "a",
         "Correct! Past of buy is 'bought'.", "buy → bought (never 'buyed')."),
        (6, "They ______ a good time.",
         [{"id": "a", "text": "had"}, {"id": "b", "text": "haved"}, {"id": "c", "text": "have"}], "a",
         "Correct! Past of have is 'had'.", "have → had."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "sentence_builder", "assessment", 7, "Put in order: went / park / I / the / to",
                    {"items": [{"id": "c1", "text": "I"}, {"id": "c2", "text": "went"}, {"id": "c3", "text": "to"},
                               {"id": "c4", "text": "the"}, {"id": "c5", "text": "park"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4", "c5"],
                     "feedback": {"correct": "Correct! 'I went to the park.'", "incorrect": "I went to the park."}},
                    8, str(uuid7()))
    insert_question(gram, "sentence_builder", "assessment", 8, "Order the story.",
                    {"items": [{"id": "c1", "text": "I went to the beach."}, {"id": "c2", "text": "I ate lunch."},
                               {"id": "c3", "text": "I played volleyball."}, {"id": "c4", "text": "I came home."}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Beach → lunch → volleyball → home."}},
                    8, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Difficult Sounds"}, str(uuid7()))
    for (d, w, nt) in [(1, "Went", "වෙන්ට් — clear final t"), (2, "Bought", "බෝට් — the 'gh' is silent"),
                       (3, "Saw", "සෝ — not 'සව්'")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Clear final 't'.", "I went to the park."),
        (5, "Say 'bought' — the 'gh' is silent.", "I bought a gift."),
        (6, "Say the sentence clearly.", "We saw a movie."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "A Day at the Beach"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Last Sunday, I went to the beach with my family. First, we went swimming. Then, we ate "
                 "lunch together. After that, I saw my friends and played games. Finally, we came home in "
                 "the evening.")}, str(uuid7()))
    l_mcq = [
        (2, "Where did he go?", [{"id": "a", "text": "Beach"}, {"id": "b", "text": "School"}], "a", "Correct!", "He went to the beach."),
        (3, "What did they eat?", [{"id": "a", "text": "Lunch"}, {"id": "b", "text": "Dinner"}], "a", "Correct!", "They ate lunch."),
        (4, "Who did he see?", [{"id": "a", "text": "Friends"}, {"id": "b", "text": "Teacher"}], "a", "Correct!", "He saw his friends."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "He went to the beach. True or False?", True, "Correct!", "He went to the beach."),
        (6, "He ate dinner. True or False?", False, "Correct! He ate lunch.", "He ate lunch, not dinner."),
        (7, "He came home in the morning. True or False?", False, "Correct! In the evening.", "He came home in the evening."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about Nimal's weekend and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Last weekend, Nimal visited his uncle. First, he went to Colombo by train. Then, he "
                 "met his cousins. After that, they ate lunch together. Later, they saw a cricket match. "
                 "Finally, Nimal came home. He had a wonderful weekend.")}, str(uuid7()))
    r = [
        (2, "Who did Nimal visit?", [{"id": "a", "text": "Uncle"}, {"id": "b", "text": "Teacher"}], "a", "Correct!", "He visited his uncle."),
        (3, "How did he go to Colombo?", [{"id": "a", "text": "Train"}, {"id": "b", "text": "Bus"}], "a", "Correct!", "He went by train."),
        (4, "What did they see?", [{"id": "a", "text": "Cricket match"}, {"id": "b", "text": "Movie"}], "a", "Correct!", "They saw a cricket match."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "fill_blank_typed", "assessment", 5, "Nimal ______ to Colombo. (past of go)",
                    {"accepted_answers": ["went"], "feedback": {"correct": "Correct! went.", "incorrect": "Past of go is 'went'."}},
                    5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 6, "He had a wonderful weekend. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "He had a wonderful weekend."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I went to the beach."), (2, "I ate lunch."), (3, "I saw my friends."),
                    (4, "I bought a gift."), (5, "I had fun.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "qa_pair", "question": "Where did you go last weekend?",
                                            "answer": "I went to the beach with my family."}, str(uuid7()))
    insert_content_block(speak, "text", 7, {"type": "plain",
        "text": ("Speak for 45 seconds about a past memory. Use at least 4 irregular verbs and 2 sequence "
                 "words, with a beginning, middle and ending.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Reorder, then correct the mistakes."}, str(uuid7()))
    builders = [
        (1, "Put in order: ate / lunch / we",
         [{"id": "c1", "text": "We"}, {"id": "c2", "text": "ate"}, {"id": "c3", "text": "lunch"}],
         ["c1", "c2", "c3"], "Correct! 'We ate lunch.'", "We ate lunch."),
        (2, "Put in order: saw / friends / my / I",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "saw"}, {"id": "c3", "text": "my"}, {"id": "c4", "text": "friends"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I saw my friends.'", "I saw my friends."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(write, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    corrections = [
        (3, "Fix and type: 'I goed to school.'", ["I went to school", "I went to school."],
         "Correct! go → went.", "The past of go is 'went'."),
        (4, "Fix and type: 'She eated pizza.'", ["She ate pizza", "She ate pizza."],
         "Correct! eat → ate.", "The past of eat is 'ate'."),
    ]
    for (d, p, acc, fc, fi) in corrections:
        insert_question(write, "fill_blank_typed", "assessment", d, p,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write a short paragraph (8–10 sentences) about a past memory. Use at least 5 irregular "
                 "verbs and 3 sequence words (first, then, after that, finally).")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Learn irregular past verbs: went, ate, saw, had, came, bought",
                  "Do NOT add -ed to irregular verbs",
                  "Use first, then, after that, finally to sequence a story",
                  "Tell a memory with a beginning, middle and ending"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=4
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
