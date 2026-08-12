"""Unit tests for pronunciation audio validation (MIME allowlist + size cap)."""

import base64

import pytest
from fastapi import HTTPException

from app.api.v1 import attempts
from app.api.v1.attempts import _decode_and_validate_audio


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def test_valid_audio_returns_bytes():
    raw = b"\x00\x01\x02fake-webm-bytes"
    assert _decode_and_validate_audio(_b64(raw), "audio/webm") == raw


def test_mime_with_codecs_param_ok():
    raw = b"abc"
    assert _decode_and_validate_audio(_b64(raw), "audio/webm;codecs=opus") == raw


def test_wav_and_m4a_allowed():
    raw = b"riff-ish"
    assert _decode_and_validate_audio(_b64(raw), "audio/wav") == raw
    assert _decode_and_validate_audio(_b64(raw), "audio/mp4") == raw


def test_unknown_mime_rejected_415():
    with pytest.raises(HTTPException) as ei:
        _decode_and_validate_audio(_b64(b"abc"), "application/json")
    assert ei.value.status_code == 415


def test_invalid_base64_rejected_422():
    with pytest.raises(HTTPException) as ei:
        _decode_and_validate_audio("aaa", "audio/webm")  # bad padding
    assert ei.value.status_code == 422


def test_empty_audio_rejected_422():
    with pytest.raises(HTTPException) as ei:
        _decode_and_validate_audio(_b64(b""), "audio/webm")
    assert ei.value.status_code == 422


def test_oversized_base64_precheck_rejected_413(monkeypatch):
    monkeypatch.setattr(attempts, "_MAX_AUDIO_B64_LEN", 10)
    with pytest.raises(HTTPException) as ei:
        _decode_and_validate_audio("a" * 50, "audio/webm")
    assert ei.value.status_code == 413


def test_oversized_decoded_rejected_413(monkeypatch):
    monkeypatch.setattr(attempts, "_MAX_AUDIO_BYTES", 100)
    monkeypatch.setattr(attempts, "_MAX_AUDIO_B64_LEN", 10_000)  # let pre-check pass
    with pytest.raises(HTTPException) as ei:
        _decode_and_validate_audio(_b64(b"x" * 500), "audio/webm")
    assert ei.value.status_code == 413
