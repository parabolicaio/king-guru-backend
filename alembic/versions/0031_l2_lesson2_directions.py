"""Beginner B — Lesson 2: My Neighborhood & Directions (Level 2 seed).

Seeds beginner_b Lesson 2 from LEVEL 2 Lesson 2.docx (7 sections). Text-only
scope; audio/map activities deferred. Sinhala from the .docx source.

Revision ID: 2b2c3d4e5f6a
Revises:     2a1b2c3d4e5f
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

revision: str = "2b2c3d4e5f6a"
down_revision: Union[str, None] = "2a1b2c3d4e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Identify places in a neighborhood",
    "Use prepositions of place correctly",
    "Give and follow simple directions",
    "Understand spoken directions and location descriptions",
    "Ask and answer questions about places",
    "Speak and write about your neighborhood clearly",
]
OBJECTIVES_SI = [
    "අසල්වැසි ප්‍රදේශයේ ස්ථාන හඳුනා ගැනීම",
    "ස්ථාන පෙන්වන prepositions නිවැරදිව භාවිතා කිරීම",
    "සරල මාර්ග උපදෙස් දීම හා අනුගමනය කිරීම",
    "කතා කරන මාර්ග උපදෙස් තේරුම් ගැනීම",
    "ස්ථාන ගැන ප්‍රශ්න අසා පිළිතුරු දීම",
    "ඔබේ අසල්වැසි ප්‍රදේශය පැහැදිලිව කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 2, "My Neighborhood & Directions",
                         "Name places in your neighborhood and give simple directions.", str(uuid7()))
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
        "text": "Learn the places in a neighborhood and words for giving directions."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Places in a Neighborhood"}, str(uuid7()))
    places = [
        (2,  "Bank",           "බැංකුව",              "A place where people keep money.",       "The bank is next to the pharmacy."),
        (3,  "Supermarket",    "සුපිරි වෙළඳසැල",       "A large shop for food and household items.", "I buy groceries at the supermarket."),
        (4,  "Pharmacy",       "ෆාමසිය",              "A place where medicine is sold.",         "You can buy medicine at the pharmacy."),
        (5,  "Hospital",       "රෝහල",                "A place where sick people receive treatment.", "The hospital is near the school."),
        (6,  "School",         "පාසල",                "A place where students study.",           "Students study at school."),
        (7,  "Bus Stop",       "බස් නැවතුම",          "A place where buses stop.",               "The bus stop is in front of the school."),
        (8,  "Park",           "උද්‍යානය",             "A public area for relaxation.",           "I walk to the park after school."),
        (9,  "Restaurant",     "අවන්හල",              "A place where people buy meals.",          "The restaurant is next to the supermarket."),
        (10, "Police Station", "පොලිස් ස්ථානය",       "A place where police officers work.",      "The police station is near the bank."),
        (11, "Post Office",    "තැපැල් කාර්යාලය",     "A place where letters and parcels are sent.", "I send letters at the post office."),
    ]
    for (d, w, si, defn, ex) in places:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_content_block(vocab, "text", 12, {"type": "heading", "text": "Direction Words"}, str(uuid7()))
    dirs = [
        (13, "Turn left",     "වමට හැරෙන්න",       "Go to the left side.",   "Turn left at the bank."),
        (14, "Turn right",    "දකුණට හැරෙන්න",     "Go to the right side.",  "Turn right at the hospital."),
        (15, "Go straight",   "කෙළින්ම යන්න",      "Keep going forward.",    "Go straight to the supermarket."),
        (16, "Cross the road","පාර මාරු කරන්න",   "Move across the road.",  "Cross the road at the school."),
    ]
    for (d, w, si, defn, ex) in dirs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    tap = [
        (17, "Where can you buy medicine?", [{"id": "a", "text": "Pharmacy"}, {"id": "b", "text": "Bank"}, {"id": "c", "text": "School"}], "a",
         "Correct! You buy medicine at a pharmacy.", "Medicine is sold at the pharmacy."),
        (18, "Where do students study?", [{"id": "a", "text": "School"}, {"id": "b", "text": "Park"}, {"id": "c", "text": "Hospital"}], "a",
         "Correct!", "Students study at school."),
        (19, "Where can you send a letter?", [{"id": "a", "text": "Post Office"}, {"id": "b", "text": "Restaurant"}, {"id": "c", "text": "Bus Stop"}], "a",
         "Correct!", "You send letters at the post office."),
        (20, "Where do police officers work?", [{"id": "a", "text": "Police Station"}, {"id": "b", "text": "Hospital"}, {"id": "c", "text": "School"}], "a",
         "Correct!", "Police officers work at the police station."),
    ]
    for (d, p, o, c, fc, fi) in tap:
        insert_question(vocab, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # GRAMMAR
    insert_content_block(gram, "text", 0, {"type": "plain",
        "text": ("We use prepositions of place to show where things are: next to (අසල), between (අතර), "
                 "opposite / across from (ඉදිරිපිට), near (ලඟ), behind (පිටුපස), in front of (ඉදිරියේ). "
                 "For directions we use imperatives: 'Go straight. Turn left.'")}, str(uuid7()))
    insert_content_block(gram, "text", 1, {"type": "example_cards", "label": "Prepositions of Place",
        "sentences": ["The bank is next to the pharmacy.", "The school is opposite the park.",
                      "The restaurant is between the bank and the pharmacy."]}, str(uuid7()))
    insert_content_block(gram, "text", 2, {"type": "qa_pair", "question": "How do I get to the park?",
                                           "answer": "Go straight and turn right."}, str(uuid7()))
    g = [
        (3, "The bank is ______ the pharmacy.",
         [{"id": "a", "text": "next to"}, {"id": "b", "text": "behind"}, {"id": "c", "text": "between"}], "a",
         "Correct! They are side by side — 'next to'.", "Side by side is 'next to'."),
        (4, "The park is ______ the supermarket.",
         [{"id": "a", "text": "across from"}, {"id": "b", "text": "behind"}, {"id": "c", "text": "near"}], "a",
         "Correct! 'Across from' means opposite.", "Opposite is 'across from'."),
        (5, "The restaurant is ______ the bank and the pharmacy.",
         [{"id": "a", "text": "between"}, {"id": "b", "text": "near"}, {"id": "c", "text": "behind"}], "a",
         "Correct! It is between two places.", "It is in the middle — 'between'."),
        (6, "The bus stop is ______ the school.",
         [{"id": "a", "text": "in front of"}, {"id": "b", "text": "behind"}, {"id": "c", "text": "across from"}], "a",
         "Correct!", "It is 'in front of' the school."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    builders = [
        (7, "Put in order: bank / next to / is / pharmacy / the / the",
         [{"id": "c1", "text": "The"}, {"id": "c2", "text": "bank"}, {"id": "c3", "text": "is"},
          {"id": "c4", "text": "next to"}, {"id": "c5", "text": "the"}, {"id": "c6", "text": "pharmacy"}],
         ["c1", "c2", "c3", "c4", "c5", "c6"], "Correct! 'The bank is next to the pharmacy.'",
         "The bank is next to the pharmacy."),
        (8, "Put in order: school / near / hospital / the / is / the",
         [{"id": "c1", "text": "The"}, {"id": "c2", "text": "school"}, {"id": "c3", "text": "is"},
          {"id": "c4", "text": "near"}, {"id": "c5", "text": "the"}, {"id": "c6", "text": "hospital"}],
         ["c1", "c2", "c3", "c4", "c5", "c6"], "Correct! 'The school is near the hospital.'",
         "The school is near the hospital."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(gram, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 9, "Match the question to the answer", {
        "pairs": [
            {"id": "p1", "left": "Where is the bank?", "right": "It is next to the pharmacy."},
            {"id": "p2", "left": "Where is the school?", "right": "It is opposite the park."},
            {"id": "p3", "left": "How do I get to the pharmacy?", "right": "Go straight and turn left."},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match each question to a sensible answer."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Stress the Action Word"}, str(uuid7()))
    for (d, ph, nt) in [(1, "TURN left", "Stress TURN"), (2, "GO straight", "Stress GO"),
                        (3, "CROSS the road", "Stress CROSS")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": ph, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Stress 'turn'.", "Turn left at the hospital."),
        (5, "Say the sentence clearly.", "The bank is next to the pharmacy."),
        (6, "Say 'straight' — not 'strait'.", "Go straight to the supermarket."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great, clear directions!", "incorrect": "Try again, slowly."}},
                        15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "My Neighborhood"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("My neighborhood has many places. There is a bank next to the pharmacy. The supermarket "
                 "is across from the park. The school is near the hospital. The bus stop is in front of "
                 "the school.")}, str(uuid7()))
    l_mcq = [
        (2, "What is next to the pharmacy?", [{"id": "a", "text": "Bank"}, {"id": "b", "text": "Park"}], "a",
         "Correct!", "The bank is next to the pharmacy."),
        (3, "What is across from the park?", [{"id": "a", "text": "Supermarket"}, {"id": "b", "text": "Hospital"}], "a",
         "Correct!", "The supermarket is across from the park."),
        (4, "What is in front of the school?", [{"id": "a", "text": "Bus stop"}, {"id": "b", "text": "Bank"}], "a",
         "Correct!", "The bus stop is in front of the school."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "The bank is next to the pharmacy. True or False?", True, "Correct!", "Yes — next to the pharmacy."),
        (6, "The park is next to the hospital. True or False?", False, "Correct!", "The park is across from the supermarket."),
        (7, "The bus stop is behind the school. True or False?", False, "Correct!", "It is in front of the school."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_content_block(listn, "text", 8, {"type": "plain",
        "text": ("Follow the route: Start at the school. Go straight. Turn left at the bank. Cross the "
                 "road. The pharmacy is on your right.")}, str(uuid7()))
    insert_question(listn, "mcq_single", "assessment", 9, "Where do you arrive?", {
        "options": [{"id": "a", "text": "Pharmacy"}, {"id": "b", "text": "Hospital"}, {"id": "c", "text": "Restaurant"}],
        "correct_option_id": "a",
        "feedback": {"correct": "Correct! You arrive at the pharmacy.", "incorrect": "Follow the route — you reach the pharmacy."},
    }, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about the neighborhood and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("My neighborhood is very busy. There is a supermarket near my house. The bank is next "
                 "to the pharmacy. Across from the supermarket, there is a park. The hospital is behind "
                 "the school. The bus stop is in front of the school. I often walk to the park after school.")}, str(uuid7()))
    r = [
        (2, "What is near the house?", [{"id": "a", "text": "Supermarket"}, {"id": "b", "text": "Hospital"}], "a",
         "Correct!", "The supermarket is near the house."),
        (3, "What is next to the pharmacy?", [{"id": "a", "text": "Bank"}, {"id": "b", "text": "School"}], "a",
         "Correct!", "The bank is next to the pharmacy."),
        (4, "Where is the hospital?", [{"id": "a", "text": "Behind the school"}, {"id": "b", "text": "Near the park"}], "a",
         "Correct!", "The hospital is behind the school."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "The neighborhood is busy. True or False?", True, "Correct!", "The neighborhood is very busy."),
        (6, "The hospital is next to the school. True or False?", False, "Correct!", "The hospital is behind the school."),
        (7, "The park is across from the supermarket. True or False?", True, "Correct!", "Yes — across from the supermarket."),
    ]:
        insert_question(read, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "The bank is next to the pharmacy."), (2, "The school is opposite the park."),
                    (3, "Turn left at the supermarket."), (4, "Go straight to the hospital.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "Where is the bank?",
                                            "answer": "The bank is next to the pharmacy."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 30–45 seconds about your neighborhood. Include at least 4 places, 3 "
                 "prepositions and 2 direction phrases.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Reorder the words, then answer."}, str(uuid7()))
    builders = [
        (1, "Put in order: opposite / school / park / the / is / the",
         [{"id": "c1", "text": "The"}, {"id": "c2", "text": "school"}, {"id": "c3", "text": "is"},
          {"id": "c4", "text": "opposite"}, {"id": "c5", "text": "the"}, {"id": "c6", "text": "park"}],
         ["c1", "c2", "c3", "c4", "c5", "c6"], "Correct! 'The school is opposite the park.'", "The school is opposite the park."),
        (2, "Put in order: in front of / school / the / bus stop / is / the",
         [{"id": "c1", "text": "The"}, {"id": "c2", "text": "bus stop"}, {"id": "c3", "text": "is"},
          {"id": "c4", "text": "in front of"}, {"id": "c5", "text": "the"}, {"id": "c6", "text": "school"}],
         ["c1", "c2", "c3", "c4", "c5", "c6"], "Correct! 'The bus stop is in front of the school.'",
         "The bus stop is in front of the school."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(write, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 3,
                    "Complete: 'Go straight and turn ______.' (left or right)",
                    {"accepted_answers": ["left", "right"],
                     "feedback": {"correct": "Good — that's a direction!", "incorrect": "Write 'left' or 'right'."}},
                    5, str(uuid7()))
    insert_content_block(write, "self_check", 4, {"prompt": "Can you write this on your own?",
        "text": ("Write 6–8 sentences about your neighborhood. Include 4 places, 3 prepositions, 2 "
                 "direction phrases and one place you visit often.")}, str(uuid7()))
    insert_content_block(write, "text", 5, {"type": "summary",
        "items": ["Name common places in a neighborhood",
                  "Use next to, opposite, between, near, behind, in front of",
                  "Give directions with go straight, turn left/right, cross the road",
                  "Ask and answer 'Where is...?' and 'How do I get to...?'"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=2
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
