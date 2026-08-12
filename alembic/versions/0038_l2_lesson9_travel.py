"""Beginner B — Lesson 9: Travel, Transport & Experiences (Level 2 seed).

Seeds beginner_b Lesson 9 from LEVEL 2 Lesson 9.docx (7 sections). Opens with a
Review Corner (leading purpose='practice' questions in grammar — see 0034) and
introduces the Present Perfect ('Have you ever...?'). Text-only scope; audio
activities deferred. Sinhala from the .docx source.

Revision ID: 3c9d0e1f2a3b
Revises:     3b8c9d0e1f2a
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

revision: str = "3c9d0e1f2a3b"
down_revision: Union[str, None] = "3b8c9d0e1f2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Identify different types of transport",
    "Use travel-related vocabulary and expressions",
    "Ask and answer questions about travel plans",
    "Use 'Have you ever...?' to talk about experiences",
    "Understand travel conversations and announcements",
    "Speak and write about travel experiences confidently",
]
OBJECTIVES_SI = [
    "විවිධ ප්‍රවාහන වර්ග හඳුනා ගැනීම",
    "සංචාරයට අදාළ වචන හා ප්‍රකාශන භාවිතා කිරීම",
    "සංචාර සැලසුම් ගැන ප්‍රශ්න අසා පිළිතුරු දීම",
    "අත්දැකීම් ගැන කතා කිරීමට 'Have you ever...?' භාවිතා කිරීම",
    "සංචාර සංවාද හා නිවේදන තේරුම් ගැනීම",
    "සංචාර අත්දැකීම් විශ්වාසයෙන් කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 9, "Travel, Transport & Experiences",
                         "Talk about travel and life experiences with 'Have you ever...?'.", str(uuid7()))
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
    insert_content_block(vocab, "text", 0, {"type": "plain", "text": "Learn transport types and travel expressions."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Types of Transport"}, str(uuid7()))
    trans = [
        (2, "Bus",        "බස් රථය",       "Road transport for many people.", "I go to school by bus."),
        (3, "Train",      "දුම්රිය",       "Runs on railway tracks.",         "We travelled by train."),
        (4, "Plane",      "ගුවන් යානය",    "Flies in the sky.",               "I have never travelled by plane."),
        (5, "Taxi",       "ටැක්සිය",       "A car you pay to ride in.",       "We took a taxi to the airport."),
        (6, "Boat",       "බෝට්ටුව",       "Travels on water.",               "We went on a boat."),
        (7, "Bicycle",    "බයිසිකලය",      "Two wheels, no engine.",          "I ride a bicycle."),
        (8, "Tuk Tuk",    "ත්‍රීවිල් රථය",  "A three-wheeler for short trips.", "We took a tuk tuk home."),
    ]
    for (d, w, si, defn, ex) in trans:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 9, {"type": "heading", "text": "Travel Expressions"}, str(uuid7()))
    expr = [
        (10, "Book a ticket",  "ටිකට්පතක් වෙන්කරගන්න", "Reserve a ticket before travelling.", "I booked a ticket to Ella."),
        (11, "Pack a bag",     "බෑගයක් සූදානම් කිරීම",  "Put things in a bag for a trip.",     "I packed a bag for the trip."),
        (12, "Stay in a hotel","හෝටලයක නවාතැන් ගැනීම",  "Sleep at a hotel.",                  "We stayed in a hotel."),
        (13, "Go sightseeing", "සංචාරක ස්ථාන නැරඹීම",  "Visit interesting places.",           "We went sightseeing in Kandy."),
    ]
    for (d, w, si, defn, ex) in expr:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 14, "Match the transport to its category", {
        "pairs": [
            {"id": "p1", "left": "Bus", "right": "Land transport"},
            {"id": "p2", "left": "Train", "right": "Land transport"},
            {"id": "p3", "left": "Plane", "right": "Air transport"},
            {"id": "p4", "left": "Boat", "right": "Water transport"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Sort each into land, air or water."},
    }, 10, str(uuid7()))

    # GRAMMAR — Review Corner + Present Perfect
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner"}, str(uuid7()))
    review = [
        (1, "Last year, we ______ to Kandy.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}], "a", "Correct! go → went.", "Past of go is 'went'."),
        (2, "Next month, we ______ visit Ella.",
         [{"id": "a", "text": "are going to"}, {"id": "b", "text": "went"}], "a", "Correct!", "Future plan → 'are going to'."),
        (3, "The weather was ______ than last week.",
         [{"id": "a", "text": "better"}, {"id": "b", "text": "good"}], "a", "Correct! Comparative 'better'.", "Use the comparative 'better'."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 4, {"type": "heading", "text": "Present Perfect — Experiences"}, str(uuid7()))
    insert_content_block(gram, "text", 5, {"type": "plain",
        "text": ("We use the present perfect (have/has + past participle) for life experiences: 'I have "
                 "travelled by train.' We ask about experiences with 'Have you ever...?' — you don't need "
                 "to say when. Use the past simple with a specific time: 'I travelled by train last year.'")}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "example_cards", "label": "Have you ever...?",
        "sentences": ["Have you ever travelled by plane?", "I have travelled by train.",
                      "She has visited Kandy."]}, str(uuid7()))
    g = [
        (7, "______ you ever travelled by plane?",
         [{"id": "a", "text": "Have"}, {"id": "b", "text": "Did"}], "a", "Correct!", "'Have you ever...?' for experience."),
        (8, "She ______ visited Kandy.",
         [{"id": "a", "text": "has"}, {"id": "b", "text": "have"}], "a", "Correct! With 'she' use 'has'.", "With 'she' use 'has'."),
        (9, "I ______ travelled by train.",
         [{"id": "a", "text": "have"}, {"id": "b", "text": "has"}], "a", "Correct! With 'I' use 'have'.", "With 'I' use 'have'."),
        (10, "I ______ to Kandy last year. (specific time)",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "have gone"}], "a", "Correct! A specific time → past simple.", "With 'last year' use the past simple 'went'."),
        (11, "Has she ever travelled abroad? — No, she ______.",
         [{"id": "a", "text": "hasn't"}, {"id": "b", "text": "didn't"}], "a", "Correct!", "Answer with 'No, she hasn't.'"),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 12, "Match the question to the answer", {
        "pairs": [
            {"id": "p1", "left": "Have you ever travelled by train?", "right": "Yes, I have."},
            {"id": "p2", "left": "Has she ever travelled abroad?", "right": "No, she hasn't."},
            {"id": "p3", "left": "Have you ever visited Kandy?", "right": "Yes, I have."},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match each question to a short answer."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Airport", "එයාර්පෝට්"), (2, "Journey", "ජර්නි — not 'ජර්නියි'"), (3, "Experience", "එක්ස්පීරියන්ස්")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Stress 'have'.", "I have travelled by train."),
        (5, "Say the question clearly.", "Have you ever travelled abroad?"),
        (6, "Say 'journey' — one clear ending.", "It was a long journey."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "At the Airport"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Good morning. Welcome to Bandaranaike International Airport. Passengers travelling to "
                 "Singapore should check in at Counter 12. The flight will depart at 10:30 a.m. Passengers "
                 "should have their passports and tickets ready. After checking in, passengers should "
                 "proceed to Gate 5. We wish you a pleasant journey.")}, str(uuid7()))
    l_mcq = [
        (2, "Where should passengers check in?", [{"id": "a", "text": "Counter 12"}, {"id": "b", "text": "Counter 5"}], "a",
         "Correct!", "Passengers check in at Counter 12."),
        (3, "Which country are they travelling to?", [{"id": "a", "text": "Singapore"}, {"id": "b", "text": "India"}], "a",
         "Correct!", "They are travelling to Singapore."),
        (4, "Which gate should passengers go to?", [{"id": "a", "text": "Gate 5"}, {"id": "b", "text": "Gate 12"}], "a",
         "Correct!", "Passengers proceed to Gate 5."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "The announcement is at an airport. True or False?", True, "Correct!", "It is an airport announcement."),
        (6, "The flight departs at 8:30 a.m. True or False?", False, "Correct! 10:30 a.m.", "The flight departs at 10:30 a.m."),
        (7, "Passengers need passports and tickets. True or False?", True, "Correct!", "Passports and tickets are required."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about a train journey and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Last year, I travelled to Ella with my family. It was my first train journey. We left "
                 "Colombo early in the morning. The train passed through mountains, forests and beautiful "
                 "villages. The weather was cool and sunny. My sister took many photographs. After several "
                 "hours, we arrived in Ella and stayed in a small hotel. The next day, we visited Nine "
                 "Arches Bridge. I had a wonderful experience and I would like to travel by train again.")}, str(uuid7()))
    r = [
        (2, "Where did the writer travel?", [{"id": "a", "text": "Ella"}, {"id": "b", "text": "Galle"}], "a", "Correct!", "The writer travelled to Ella."),
        (3, "What was special about the journey?", [{"id": "a", "text": "First train journey"}, {"id": "b", "text": "First plane journey"}], "a",
         "Correct!", "It was the writer's first train journey."),
        (4, "What did the sister do?", [{"id": "a", "text": "Took photographs"}, {"id": "b", "text": "Bought clothes"}], "a",
         "Correct!", "The sister took many photographs."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "fill_blank_typed", "assessment", 5, "The weather was ______ and sunny. (a word from the text)",
                    {"accepted_answers": ["cool"], "feedback": {"correct": "Correct! cool.", "incorrect": "The text says the weather was cool and sunny."}},
                    5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 6, "The writer wants to travel by train again. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "The writer would like to travel by train again."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I have travelled by train."), (2, "Have you ever travelled by plane?"),
                    (3, "I stayed in a hotel during my trip."), (4, "Next year, I am going to travel again.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "Have you ever travelled by train?",
                                            "answer": "Yes, I have. I travelled by train last year."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 60–90 seconds about your best travel experience: the place, transport, weather, "
                 "activities, accommodation and feelings. Include one present perfect sentence and one "
                 "future travel plan.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences."}, str(uuid7()))
    fills = [
        (1, "I have travelled by ______. (a transport word)",
         ["train", "bus", "plane", "boat", "car", "taxi", "bicycle"],
         "Good — that's a transport word!", "Write a transport word, e.g. 'train'."),
        (2, "She ______ visited Kandy. (have/has)", ["has"], "Correct! With 'she' use 'has'.", "With 'she' use 'has'."),
        (3, "I ______ travelled by train. (have/has)", ["have"], "Correct! With 'I' use 'have'.", "With 'I' use 'have'."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 4,
                    "Fix and type: 'I have travel by train.' (use the past participle)",
                    {"accepted_answers": ["I have travelled by train", "I have travelled by train.",
                                          "I have traveled by train", "I have traveled by train."],
                     "feedback": {"correct": "Correct! 'I have travelled by train.'",
                                  "incorrect": "Use the past participle: 'I have travelled by train.'"}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 8–16 sentences about your last trip: destination, transport, weather, activities, "
                 "accommodation and feelings. Include one 'Have you ever...?' idea and one future plan.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Name types of transport (land, air, water)",
                  "Use the present perfect for life experiences",
                  "Ask 'Have you ever...?' and answer 'Yes, I have / No, I haven't'",
                  "Use the past simple with a specific time"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=9
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
