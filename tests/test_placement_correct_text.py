"""D-21: every placement review row has a readable correct answer."""

import pytest

from app.services.placement_service import _extract_correct_answer as extract


@pytest.mark.parametrize(
    "qtype,payload,text",
    [
        ("mcq_single", {"options": [{"id": "a", "text": "My"}, {"id": "b", "text": "Me"}],
                        "correct_option_id": "a"}, "My"),
        ("mcq_single", {"options": [{"id": "a", "label": "Apple"}], "correct_option_id": "a"}, "Apple"),
        ("true_false", {"correct_answer": True}, "True"),
        ("true_false", {"correct_answer": False}, "False"),
        ("fill_blank_options", {"options": [{"id": "x", "text": "on"}], "correct_option_id": "x"}, "on"),
        ("fill_blank_typed", {"accepted_answers": ["went", "Went"]}, "went"),
        ("correct_mistake", {"accepted_corrections": ["She goes."]}, "She goes."),
        ("match_pairs", {"pairs": [{"id": "p1", "left": "hi", "right": "hello"}]}, "hi = hello"),
        ("sentence_builder", {"correct_order": ["I", "am", "fine"]}, "I am fine"),
        ("mcq_single", {"options": [], "correct_option_id": "a"}, None),
    ],
)
def test_correct_text(qtype, payload, text):
    assert extract(qtype, payload)["correct_text"] == text


def test_existing_keys_kept():
    out = extract("true_false", {"correct_answer": True})
    assert out["correct_answer"] is True
    out = extract("mcq_single", {"options": [{"id": "a", "text": "My"}], "correct_option_id": "a"})
    assert out["correct_option_id"] == "a"
