"""D-07: silent or wordless recordings must never get marks."""

import io
import json
import math
import struct
import wave
from unittest.mock import patch

import pytest

from app.services import pronunciation_service as ps


def _wav(seconds: float, amplitude: float, rate: int = 16000) -> bytes:
    n = int(seconds * rate)
    frames = b"".join(
        struct.pack("<h", int(amplitude * 32767 * math.sin(2 * math.pi * 220 * i / rate)))
        for i in range(n)
    )
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)
    return buf.getvalue()


def test_silent_wav_has_no_speech():
    assert ps.audio_has_speech(_wav(2.0, 0.0), "audio/wav") is False


def test_very_quiet_wav_has_no_speech():
    assert ps.audio_has_speech(_wav(2.0, 0.005), "audio/wav") is False


def test_short_wav_has_no_speech():
    assert ps.audio_has_speech(_wav(0.3, 0.5), "audio/wav") is False


def test_loud_wav_has_speech():
    assert ps.audio_has_speech(_wav(1.5, 0.3), "audio/wav") is True


def test_non_wav_is_left_to_the_model():
    assert ps.audio_has_speech(b"not audio", "audio/m4a") is True


def test_broken_wav_is_left_to_the_model():
    assert ps.audio_has_speech(b"RIFFjunk", "audio/wav") is True


@pytest.mark.asyncio
async def test_grade_silent_wav_skips_gemini_and_fails():
    with patch.object(ps, "_call_gemini") as gemini:
        result = await ps.grade(_wav(2.0, 0.0), "audio/wav", "Hello", "en")
    gemini.assert_not_called()
    assert result.grade == "F"
    assert result.overall_score == 0
    assert result.ai_model == "no-speech-check"
    assert "couldn't hear" in result.summary


@pytest.mark.asyncio
async def test_grade_no_speech_summary_in_sinhala():
    result = await ps.grade(_wav(2.0, 0.0), "audio/wav", "Hello", "si")
    assert result.summary == ps._NO_SPEECH_SUMMARY["si"]


class _Resp:
    is_error = False
    text = ""

    def __init__(self, scores):
        self._scores = scores

    def json(self):
        return {"candidates": [{"content": {"parts": [{"text": json.dumps(self._scores)}]}}]}


class _Client:
    def __init__(self, scores):
        self.scores = scores
        self.sent = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def post(self, url, params=None, json=None):
        self.sent = json
        return _Resp(self.scores)


async def _call_with(scores):
    client = _Client(scores)
    with patch("httpx.AsyncClient", return_value=client):
        result = await ps._call_gemini(b"x", "audio/m4a", "Hello", "en")
    return result, client


@pytest.mark.asyncio
async def test_empty_transcript_forces_zero_even_if_model_praises():
    result, _ = await _call_with(
        {"transcript": "", "accuracy": 10, "clarity": 6, "fluency": 4, "summary": "Perfect!"}
    )
    assert result.grade == "F"
    assert result.overall_score == 0


@pytest.mark.asyncio
async def test_real_transcript_is_graded_and_temperature_is_zero():
    result, client = await _call_with(
        {"transcript": "hello", "accuracy": 9, "clarity": 5, "fluency": 4, "summary": "Good"}
    )
    assert result.grade == "A+"  # 18/20 = 90%
    assert client.sent["generationConfig"]["temperature"] == 0
    assert "transcript" in client.sent["system_instruction"]["parts"][0]["text"]
