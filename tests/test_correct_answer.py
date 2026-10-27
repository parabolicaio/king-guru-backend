"""D-39: the attempt response says what the right answer was."""

import pytest

from app.services.scoring import correct_answer_for


@pytest.mark.parametrize(
    "qtype,payload,expected",
    [
        ("mcq_single", {"correct_option_id": "b"}, "b"),
        ("mcq_long_short_form", {"correct_option_id": "c"}, "c"),
        ("fill_blank_options", {"correct_option_id": "a"}, "a"),
        ("true_false", {"correct_answer": True}, "true"),
        ("true_false", {"correct_answer": False}, "false"),
        ("fill_blank_typed", {"accepted_answers": ["am", "'m"]}, "am"),
        ("correct_mistake", {"accepted_corrections": ["She goes"]}, "She goes"),
        ("fill_blank_typed", {"accepted_answers": []}, None),
        ("match_pairs", {"pairs": []}, None),
        ("pronunciation_practice", {"target_text": "Hi"}, None),
        ("mcq_single", {}, None),
    ],
)
def test_correct_answer_for(qtype, payload, expected):
    assert correct_answer_for(qtype, payload) == expected


def test_attempt_response_has_optional_correct_answer():
    from app.schemas.attempts import AttemptResponse

    assert AttemptResponse.model_fields["correct_answer"].default is None
