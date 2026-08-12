"""Beginner B — Lesson 10: Work, Technology & Communication (Level 2 final).

Seeds beginner_b Lesson 10 from LEVEL 2 Lesson 10.docx (7 sections). The
end-of-level integrated lesson: opens with a mixed-grammar Review Corner
(leading purpose='practice' questions in grammar — see 0034) that recaps
past/present/future and comparatives, then covers jobs, technology and
comparatives. Text-only scope; audio activities deferred. Sinhala from the .docx.

Revision ID: 3d0e1f2a3b4c
Revises:     3c9d0e1f2a3b
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

revision: str = "3d0e1f2a3b4c"
down_revision: Union[str, None] = "3c9d0e1f2a3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use job vocabulary and describe occupations",
    "Talk about technology, apps and digital devices",
    "Review past, present and future structures",
    "Compare people, jobs, places and technology",
    "Understand longer conversations across different topics",
    "Speak and write combining different grammar structures",
]
OBJECTIVES_SI = [
    "රැකියා වචන භාවිතයෙන් වෘත්තීන් විස්තර කිරීම",
    "තාක්ෂණය, යෙදුම් හා උපකරණ ගැන කතා කිරීම",
    "අතීත, වර්තමාන හා අනාගත ව්‍යුහයන් සමාලෝචනය කිරීම",
    "පුද්ගලයන්, රැකියා, ස්ථාන හා තාක්ෂණය සැසඳීම",
    "විවිධ මාතෘකා හරහා දිගු සංවාද තේරුම් ගැනීම",
    "විවිධ ව්‍යාකරණ ව්‍යුහයන් එකට යොදා කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 10, "Work, Technology & Communication",
                         "The end-of-level lesson: jobs, technology and everything from Level 2 together.", str(uuid7()))
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
    insert_content_block(vocab, "text", 0, {"type": "plain", "text": "Learn job and technology vocabulary."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Jobs"}, str(uuid7()))
    jobs = [
        (2, "Teacher",        "ගුරුවරයා",                  "Teaches students.",            "The teacher works in a school."),
        (3, "Doctor",         "වෛද්‍යවරයා",                "Helps sick people.",           "The doctor works in a hospital."),
        (4, "Nurse",          "හෙදිය",                     "Helps doctors and patients.",  "The nurse works in a hospital."),
        (5, "Engineer",       "ඉංජිනේරුවරයා",              "Designs buildings or systems.", "The engineer designs bridges."),
        (6, "Driver",         "රියදුරු",                   "Drives vehicles.",             "The driver drives a bus."),
        (7, "Chef",           "සූපවේදියා",                 "Cooks food in a restaurant.",  "The chef cooks in a restaurant."),
        (8, "Farmer",         "ගොවියා",                    "Grows crops.",                 "The farmer works on a farm."),
        (9, "Programmer",     "පරිගණක වැඩසටහන් නිර්මාතෘ",   "Creates software and apps.",   "The programmer writes code."),
    ]
    for (d, w, si, defn, ex) in jobs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 10, {"type": "heading", "text": "Technology"}, str(uuid7()))
    tech = [
        (11, "Smartphone", "ස්මාර්ට් දුරකථනය", "A phone with apps and internet.", "I use my smartphone every day."),
        (12, "Laptop",     "ලැප්ටොප් පරිගණකය", "A portable computer.",            "I use a laptop for work."),
        (13, "Internet",   "අන්තර්ජාලය",       "A global network.",               "I browse the internet for information."),
        (14, "Email",      "විද්‍යුත් තැපෑල",  "A digital message.",              "I send an email for formal communication."),
        (15, "Video call",  "වීඩියෝ ඇමතුම",   "A call with picture.",            "We use a video call to talk face-to-face."),
        (16, "Password",   "මුරපදය",           "A secret word to log in.",        "I use a password to protect my account."),
    ]
    for (d, w, si, defn, ex) in tech:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 17, "Match the job to the workplace", {
        "pairs": [
            {"id": "p1", "left": "Teacher", "right": "School"},
            {"id": "p2", "left": "Doctor", "right": "Hospital"},
            {"id": "p3", "left": "Chef", "right": "Restaurant"},
            {"id": "p4", "left": "Farmer", "right": "Farm"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match each job to its workplace."},
    }, 10, str(uuid7()))
    insert_question(vocab, "mcq_single", "assessment", 18, "Who creates software and apps?", {
        "options": [{"id": "a", "text": "Programmer"}, {"id": "b", "text": "Farmer"}, {"id": "c", "text": "Driver"}],
        "correct_option_id": "a",
        "feedback": {"correct": "Correct! A programmer creates software.", "incorrect": "A programmer creates software and apps."},
    }, 5, str(uuid7()))

    # GRAMMAR — Mixed Review Corner + comparatives
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner — Mixed Grammar"}, str(uuid7()))
    review = [
        (1, "Yesterday, I ______ to work. (past)",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}], "a", "Correct! Past simple.", "Past of go is 'went'."),
        (2, "Next week, I ______ visit my friend. (future)",
         [{"id": "a", "text": "am going to"}, {"id": "b", "text": "went"}], "a", "Correct! Future plan.", "Use 'am going to' for the future."),
        (3, "I ______ travelled by plane. (experience)",
         [{"id": "a", "text": "have"}, {"id": "b", "text": "am"}], "a", "Correct! Present perfect.", "Use 'have' for an experience."),
        (4, "Colombo is ______ than Nuwara Eliya. (comparative)",
         [{"id": "a", "text": "hotter"}, {"id": "b", "text": "hot"}], "a", "Correct! Comparative.", "Use the comparative 'hotter'."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 5, {"type": "heading", "text": "Comparatives"}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "plain",
        "text": ("We compare two things with a comparative + than. Short adjectives add -er (fast → faster, "
                 "big → bigger, busy → busier). Longer adjectives use 'more' (difficult → more difficult, "
                 "interesting → more interesting).")}, str(uuid7()))
    insert_content_block(gram, "text", 7, {"type": "example_cards", "label": "Comparatives",
        "sentences": ["A laptop is faster than a tablet.", "A smartphone is smaller than a laptop.",
                      "A video call is more interactive than a phone call."]}, str(uuid7()))
    g = [
        (8, "A laptop is ______ than a tablet.",
         [{"id": "a", "text": "faster"}, {"id": "b", "text": "fast"}, {"id": "c", "text": "fastest"}], "a",
         "Correct! faster than.", "Use the comparative 'faster'."),
        (9, "A smartphone is ______ than a laptop.",
         [{"id": "a", "text": "smaller"}, {"id": "b", "text": "small"}, {"id": "c", "text": "smallest"}], "a",
         "Correct! smaller than.", "Use 'smaller than'."),
        (10, "A doctor is usually ______ than a student.",
         [{"id": "a", "text": "busier"}, {"id": "b", "text": "busy"}, {"id": "c", "text": "busiest"}], "a",
         "Correct! busy → busier.", "Adjectives ending in -y become -ier: 'busier'."),
        (11, "Sending an email is ______ than sending a letter.",
         [{"id": "a", "text": "faster"}, {"id": "b", "text": "fast"}], "a", "Correct!", "Use 'faster than'."),
        (12, "This lesson is ______ than lesson one.",
         [{"id": "a", "text": "more difficult"}, {"id": "b", "text": "difficulter"}], "a",
         "Correct! Long adjectives use 'more'.", "Use 'more difficult' — not 'difficulter'."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 13, "Match the person to the job description", {
        "pairs": [
            {"id": "p1", "left": "Helps sick people", "right": "Doctor"},
            {"id": "p2", "left": "Teaches students", "right": "Teacher"},
            {"id": "p3", "left": "Grows crops", "right": "Farmer"},
            {"id": "p4", "left": "Creates apps", "right": "Programmer"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match each description to the job."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Technology", "ටෙක්නොලජි"), (2, "Communication", "කමියුනිකේෂන්"), (3, "Programmer", "ප්‍රෝග්‍රැමර්")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the word — four beats: tech-no-lo-gy.", "Technology is important today."),
        (5, "Say the sentence. Stress 'work'.", "I work as a teacher."),
        (6, "Say the sentence clearly.", "We have travelled abroad."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "A Day at Work"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Hello. My name is Nuwan. I work as a software programmer. Every day, I use a laptop and "
                 "the internet. I usually start work at 8:30 in the morning. I answer emails and attend "
                 "online meetings. Last year, I travelled to India for a technology conference. Next year, "
                 "I am going to attend another conference in Singapore. I enjoy my job because I learn new "
                 "things every day.")}, str(uuid7()))
    l_mcq = [
        (2, "What is Nuwan's job?", [{"id": "a", "text": "Programmer"}, {"id": "b", "text": "Teacher"}], "a", "Correct!", "Nuwan is a programmer."),
        (3, "What device does he use?", [{"id": "a", "text": "Laptop"}, {"id": "b", "text": "Tablet"}], "a", "Correct!", "He uses a laptop."),
        (4, "Which country did he visit last year?", [{"id": "a", "text": "India"}, {"id": "b", "text": "Singapore"}], "a",
         "Correct!", "He travelled to India last year."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "He starts work at 8:30 a.m. True or False?", True, "Correct!", "He starts work at 8:30 a.m."),
        (6, "He is going to Singapore next year. True or False?", True, "Correct!", "Next year he is going to Singapore."),
        (7, "He dislikes his job. True or False?", False, "Correct! He enjoys it.", "He enjoys his job."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about Kasun and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("My name is Kasun, and I work as a teacher. Every weekday, I wake up at 6:00 a.m. I "
                 "usually travel to school by bus. I teach English. During the day, I use a laptop to "
                 "prepare lessons. Last year, I attended a teacher training workshop in Kandy. I have "
                 "worked as a teacher for five years, and I still enjoy my job. Next month, I am going to "
                 "attend another workshop in Colombo. Technology has made teaching easier and faster than "
                 "before.")}, str(uuid7()))
    r = [
        (2, "What is Kasun's job?", [{"id": "a", "text": "Teacher"}, {"id": "b", "text": "Doctor"}], "a", "Correct!", "Kasun is a teacher."),
        (3, "How does he travel to work?", [{"id": "a", "text": "Bus"}, {"id": "b", "text": "Train"}], "a", "Correct!", "He travels by bus."),
        (4, "Where is he going next month?", [{"id": "a", "text": "Colombo"}, {"id": "b", "text": "Ella"}], "a", "Correct!", "He is going to Colombo next month."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "fill_blank_typed", "assessment", 5, "He has worked as a teacher for ______ years. (a number word)",
                    {"accepted_answers": ["five", "5"], "feedback": {"correct": "Correct! Five years.", "incorrect": "He has worked for five years."}},
                    5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 6, "Technology has made teaching easier. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "Technology has made teaching easier and faster."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I work as a teacher."), (2, "I use a laptop every day."),
                    (3, "I have travelled abroad."), (4, "Next year, I am going to learn new skills.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "What job would you like in the future?",
                                            "answer": "I would like to become a teacher because I enjoy helping people learn."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("End-of-level challenge: speak for 90 seconds about 'My Life Today and My Future Plans'. "
                 "Use present simple, past simple, present perfect, going to and a comparison. "
                 "Congratulations — you have completed Level 2!")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences."}, str(uuid7()))
    fills = [
        (1, "I use ______ every day. (a device)", ["a laptop", "a smartphone", "a tablet", "the internet", "my phone", "laptop", "smartphone"],
         "Good — that's a device!", "Write a device, e.g. 'a laptop'."),
        (2, "A laptop is ______ than a tablet. (fast, comparative)", ["faster"], "Correct! faster.", "Use the comparative 'faster'."),
        (3, "I ______ travelled abroad. (have/has, present perfect)", ["have"], "Correct! With 'I' use 'have'.", "With 'I' use 'have'."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 4,
                    "Fix and type: 'A smartphone is more small than a laptop.'",
                    {"accepted_answers": ["A smartphone is smaller than a laptop", "A smartphone is smaller than a laptop."],
                     "feedback": {"correct": "Correct! Short adjective uses -er: 'smaller'.",
                                  "incorrect": "Short adjectives add -er: 'A smartphone is smaller than a laptop.'"}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 12–15 sentences about 'My Life Journey'. Include daily life, a travel experience, "
                 "technology, work or studies, present perfect, past simple, going to, a comparative and "
                 "your opinion. This shows everything you learned in Level 2.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Describe jobs and technology",
                  "Compare with -er/than and more...than",
                  "Combine past simple, present perfect and going to",
                  "You have completed Level 2 — you are ready for the next level!"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=10
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
