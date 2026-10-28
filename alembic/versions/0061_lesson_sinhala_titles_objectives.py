"""Sinhala lesson titles and Level 1 objectives (D-38).

- Adds a Sinhala title (translations.si.title) to every Level 1 and
  Level 2 lesson, matched by its English title.
- Level 1 lessons 2-5 keep their objectives in a markdown card, which
  0060 did not read, so their English objectives are still empty. This
  fills them.
- Adds Sinhala objectives (objectives_translations.si) to Level 1
  lessons whose English objectives match the lists below. Level 2
  already has them.

Only fills what is missing; nothing an editor has changed is
overwritten. The Sinhala text is a draft for a Sinhala speaker to review.

Revision ID: 7f8a9b0c1d2e
Revises:     6e7f8a9b0c1d
Create Date: 2026-10-28
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7f8a9b0c1d2e"
down_revision: Union[str, None] = "6e7f8a9b0c1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# English title -> Sinhala title.
TITLES_SI: dict[str, str] = {
    # Level 1
    "Greetings & Introductions": "ආචාර කිරීම සහ හඳුන්වා දීම",
    "Family and Describing People": "පවුල සහ පුද්ගලයන් විස්තර කිරීම",
    "Numbers, Time & Daily Routines": "අංක, වේලාව සහ දිනචරියාව",
    "Classroom & Everyday Objects": "පන්ති කාමරය සහ එදිනෙදා භාණ්ඩ",
    "Colors, Clothing & Adjectives": "වර්ණ, ඇඳුම් සහ නාම විශේෂණ",
    "Food, Drinks & Preferences": "ආහාර, පාන සහ කැමැත්ත",
    "My Home & Prepositions of Place": "මගේ නිවස සහ ස්ථානය දක්වන නිපාත",
    "Health, Body & Feelings": "සෞඛ්‍යය, ශරීරය සහ හැඟීම්",  # also Level 2 lesson 6
    "Animals, Pets & Abilities": "සතුන්, සුරතල් සතුන් සහ හැකියාවන්",
    "My Town & Community": "මගේ නගරය සහ ප්‍රජාව",
    # Level 2
    "Daily Routines & Frequency": "දිනචරියාව සහ වාර ගණන",
    "My Neighborhood & Directions": "මගේ අසල්වැසි ප්‍රදේශය සහ මාර්ග උපදෙස්",
    "Past Simple (Regular Verbs)": "සරල අතීත කාලය (සාමාන්‍ය ක්‍රියාපද)",
    "Past Simple (Irregular Verbs & Memories)": "සරල අතීත කාලය (අක්‍රමවත් ක්‍රියාපද සහ මතකයන්)",
    "Food, Shopping & Quantifiers": "ආහාර, සාප්පු යාම සහ ප්‍රමාණ දක්වන වචන",
    "Weather & Seasons": "කාලගුණය සහ ඍතු",
    "Future Plans (Going To)": "අනාගත සැලසුම් (Going To)",
    "Travel, Transport & Experiences": "සංචාරය, ප්‍රවාහනය සහ අත්දැකීම්",
    "Work, Technology & Communication": "රැකියාව, තාක්ෂණය සහ සන්නිවේදනය",
}

# Level 1: English title -> list of (English objective, Sinhala objective).
# Lesson 1 matches what 0060 parsed from its intro card; 2-5 come from
# their markdown cards; 6-10 from the OBJECTIVES lists in 0025-0029.
LEVEL1_OBJECTIVES: dict[str, list[tuple[str, str]]] = {
    "Greetings & Introductions": [
        ("Greet people in English", "ඉංග්‍රීසියෙන් අන් අයට ආචාර කිරීම"),
        ("Say your name and ask for someone else's name", "ඔබේ නම පවසා වෙනත් අයෙකුගේ නම විමසීම"),
        ("Use am and are correctly", "am සහ are නිවැරදිව භාවිතා කිරීම"),
        ("Introduce yourself in a few sentences", "වාක්‍ය කිහිපයකින් ඔබව හඳුන්වා දීම"),
    ],
    "Family and Describing People": [
        ("Name immediate and extended family members", "සමීප සහ දුරස්ථ පවුලේ සාමාජිකයන් නම් කිරීම"),
        ("Use possessive adjectives: my, your, his, her",
         "අයිතිය දක්වන නාම විශේෂණ (my, your, his, her) භාවිතා කිරීම"),
        ("Describe family members using 'He is' and 'She is'",
         "'He is' සහ 'She is' භාවිතයෙන් පවුලේ සාමාජිකයන් විස්තර කිරීම"),
    ],
    "Numbers, Time & Daily Routines": [
        ("Use numbers to talk about time, age, and daily activities",
         "වේලාව, වයස සහ දෛනික කටයුතු ගැන කතා කිරීමට අංක භාවිතා කිරීම"),
        ("Tell and ask for the time using o'clock and half past accurately",
         "o'clock සහ half past භාවිතයෙන් වේලාව නිවැරදිව පැවසීම සහ විමසීම"),
        ("Use common action verbs in the present simple tense (I / you)",
         "සරල වර්තමාන කාලයේ (I / you) පොදු ක්‍රියාපද භාවිතා කිරීම"),
        ("Speak about your daily routine in a simple and logical order",
         "ඔබේ දිනචරියාව සරල හා තාර්කික පිළිවෙළකට කතා කිරීම"),
    ],
    "Classroom & Everyday Objects": [
        ("Identify common classroom and everyday objects",
         "පන්ති කාමරයේ සහ එදිනෙදා භාවිත වන භාණ්ඩ හඳුනා ගැනීම"),
        ("Use this, that, these, and those correctly", "this, that, these සහ those නිවැරදිව භාවිතා කිරීම"),
        ("Ask and answer questions about objects around you", "ඔබ අවට ඇති භාණ්ඩ ගැන ප්‍රශ්න අසා පිළිතුරු දීම"),
        ("Use the articles a, an, and the correctly", "a, an සහ the යන උපපද නිවැරදිව භාවිතා කිරීම"),
    ],
    "Colors, Clothing & Adjectives": [
        ("Identify and use vocabulary for colors and common clothing items",
         "වර්ණ සහ පොදු ඇඳුම් සඳහා වචන හඳුනාගෙන භාවිතා කිරීම"),
        ("Use singular and plural nouns correctly in basic sentences",
         "සරල වාක්‍යවල ඒකවචන සහ බහුවචන නාම පද නිවැරදිව භාවිතා කිරීම"),
        ("Use adjectives to describe clothing and colors accurately",
         "ඇඳුම් සහ වර්ණ නිවැරදිව විස්තර කිරීමට නාම විශේෂණ භාවිතා කිරීම"),
        ("Describe what people are wearing using simple sentences",
         "අන් අය ඇඳ සිටින දේ සරල වාක්‍යවලින් විස්තර කිරීම"),
    ],
    "Food, Drinks & Preferences": [
        ("Identify vocabulary for common food and drinks", "පොදු ආහාර සහ පාන සඳහා වචන හඳුනා ගැනීම"),
        ("Use like and don't like to express preferences clearly",
         "කැමැත්ත පැහැදිලිව ප්‍රකාශ කිරීමට like සහ don't like භාවිතා කිරීම"),
        ("Ask and answer simple questions about food and drink preferences",
         "ආහාර පාන කැමැත්ත ගැන සරල ප්‍රශ්න අසා පිළිතුරු දීම"),
        ("Understand spoken conversations about food and eating habits",
         "ආහාර සහ ආහාර පුරුදු ගැන කතාබහ තේරුම් ගැනීම"),
        ("Pronounce food vocabulary and sentence patterns clearly",
         "ආහාර වචන සහ වාක්‍ය රටා පැහැදිලිව උච්චාරණය කිරීම"),
        ("Speak about your food likes and dislikes with confidence",
         "ඔබ කැමති සහ අකමැති ආහාර ගැන විශ්වාසයෙන් කතා කිරීම"),
        ("Write short sentences about your food preferences", "ඔබේ ආහාර කැමැත්ත ගැන කෙටි වාක්‍ය ලිවීම"),
    ],
    "My Home & Prepositions of Place": [
        ("Identify vocabulary for rooms and furniture in a home",
         "නිවසක කාමර සහ ගෘහ භාණ්ඩ සඳහා වචන හඳුනා ගැනීම"),
        ("Use prepositions in, on, and under to describe location",
         "ස්ථානය විස්තර කිරීමට in, on සහ under භාවිතා කිරීම"),
        ("Understand spoken descriptions of homes and rooms", "නිවාස සහ කාමර පිළිබඳ කථිත විස්තර තේරුම් ගැනීම"),
        ("Pronounce home-related vocabulary clearly", "නිවසට අදාළ වචන පැහැදිලිව උච්චාරණය කිරීම"),
        ("Speak about your home and where objects are located", "ඔබේ නිවස සහ භාණ්ඩ ඇති තැන් ගැන කතා කිරීම"),
        ("Write short descriptions of your home using simple sentences",
         "සරල වාක්‍ය භාවිතයෙන් ඔබේ නිවස ගැන කෙටි විස්තර ලිවීම"),
    ],
    "Health, Body & Feelings": [
        ("Identify vocabulary for body parts and common health problems",
         "ශරීර කොටස් සහ පොදු සෞඛ්‍ය ගැටලු සඳහා වචන හඳුනා ගැනීම"),
        ("Use the structure 'I have a...' to talk about health and feelings",
         "සෞඛ්‍යය සහ හැඟීම් ගැන කතා කිරීමට 'I have a...' රටාව භාවිතා කිරීම"),
        ("Understand short spoken health-related conversations", "සෞඛ්‍යයට අදාළ කෙටි කතාබහ තේරුම් ගැනීම"),
        ("Pronounce body and health vocabulary clearly", "ශරීරය සහ සෞඛ්‍යය පිළිබඳ වචන පැහැදිලිව උච්චාරණය කිරීම"),
        ("Speak about how you feel using simple sentences", "ඔබට දැනෙන ආකාරය සරල වාක්‍යවලින් කතා කිරීම"),
        ("Write short sentences describing health problems or feelings",
         "සෞඛ්‍ය ගැටලු හෝ හැඟීම් විස්තර කරන කෙටි වාක්‍ය ලිවීම"),
    ],
    "Animals, Pets & Abilities": [
        ("Identify vocabulary for common animals and pets", "පොදු සතුන් සහ සුරතල් සතුන් සඳහා වචන හඳුනා ගැනීම"),
        ("Use adjectives to describe animals' size and appearance",
         "සතුන්ගේ ප්‍රමාණය සහ පෙනුම විස්තර කිරීමට නාම විශේෂණ භාවිතා කිරීම"),
        ("Use can and can't to talk about abilities", "හැකියාවන් ගැන කතා කිරීමට can සහ can't භාවිතා කිරීම"),
        ("Understand spoken descriptions of animals and abilities",
         "සතුන් සහ හැකියාවන් පිළිබඳ කථිත විස්තර තේරුම් ගැනීම"),
        ("Pronounce adjectives and modal verbs clearly", "නාම විශේෂණ සහ ප්‍රකාර ක්‍රියාපද පැහැදිලිව උච්චාරණය කිරීම"),
        ("Speak about animals and abilities using simple sentences",
         "සරල වාක්‍යවලින් සතුන් සහ හැකියාවන් ගැන කතා කිරීම"),
        ("Write short sentences describing animals and skills", "සතුන් සහ කුසලතා විස්තර කරන කෙටි වාක්‍ය ලිවීම"),
    ],
    "My Town & Community": [
        ("Describe your town using There is / There are accurately",
         "There is / There are නිවැරදිව භාවිතා කරමින් ඔබේ නගරය විස්තර කිරීම"),
        ("Ask and answer questions about places in town", "නගරයේ ස්ථාන ගැන ප්‍රශ්න අසා පිළිතුරු දීම"),
        ("Use adjectives, prepositions, and can/can't together", "නාම විශේෂණ, නිපාත සහ can/can't එකට භාවිතා කිරීම"),
        ("Compare two towns using simple comparative ideas (bigger, smaller)",
         "සරල සංසන්දනාත්මක අදහස් (bigger, smaller) භාවිතයෙන් නගර දෙකක් සංසන්දනය කිරීම"),
        ("Speak for 60 seconds about a familiar topic", "හුරුපුරුදු මාතෘකාවක් ගැන තත්පර 60ක් කතා කිරීම"),
        ("Write a structured paragraph", "සංවිධිත ඡේදයක් ලිවීම"),
        ("Apply grammar from the entire Level 1 course", "පළමු මට්ටමේ මුළු පාඨමාලාවේම ව්‍යාකරණ යොදා ගැනීම"),
    ],
}


def _as_obj(value):
    if value is None:
        return {}
    return value if isinstance(value, (dict, list)) else json.loads(value)


def plan_update(title: str, translations, objectives, objectives_translations) -> dict:
    """Work out which columns to change for one lesson. Returns {} if none.

    Keys in the result: "translations", "objectives", "objectives_translations".
    """
    translations = dict(_as_obj(translations) or {})
    objectives = list(_as_obj(objectives) or [])
    obj_tr = dict(_as_obj(objectives_translations) or {})
    changes: dict = {}

    si_title = TITLES_SI.get(title)
    si = dict(translations.get("si") or {})
    if si_title and not (si.get("title") or "").strip():
        si["title"] = si_title
        translations["si"] = si
        changes["translations"] = translations

    pairs = LEVEL1_OBJECTIVES.get(title)
    if pairs:
        en = [e for e, _ in pairs]
        if not objectives:
            objectives = en
            changes["objectives"] = objectives
        # Only add Sinhala when the English list is exactly ours, so each
        # Sinhala line lines up with its English one.
        if objectives == en and not obj_tr.get("si"):
            obj_tr["si"] = [s for _, s in pairs]
            changes["objectives_translations"] = obj_tr

    return changes


_FIND = sa.text(
    """
    SELECT id, title, translations, objectives, objectives_translations
    FROM lesson
    WHERE deleted_at IS NULL AND title = ANY(:titles)
    """
)


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(_FIND, {"titles": list(TITLES_SI)}).mappings().all()
    for row in rows:
        changes = plan_update(
            row["title"], row["translations"], row["objectives"], row["objectives_translations"]
        )
        if not changes:
            continue
        sets = ", ".join(f"{col} = CAST(:{col} AS jsonb)" for col in changes)
        params = {col: json.dumps(val, ensure_ascii=False) for col, val in changes.items()}
        params["id"] = row["id"]
        bind.execute(sa.text(f"UPDATE lesson SET {sets}, updated_at = now() WHERE id = :id"), params)


def downgrade() -> None:
    # Not reversible safely: the text may have been edited since. No-op.
    pass
