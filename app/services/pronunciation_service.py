"""Pronunciation assessment service — Gemini multimodal grading.

Evaluates recorded English speech against a target text.
Rubric (20 marks total): accuracy (10) + clarity (6) + fluency (4).
Overall score = (total / 20) * 100 → GCSE grade.

Sri Lankan English is treated as a valid variety throughout — the Gemini
system prompt explicitly instructs the model not to penalise accent features
typical of Lankan English. Focus is on intelligibility and accuracy.
"""

import base64
import io
import logging
import math
import wave
from dataclasses import dataclass

logger = logging.getLogger(__name__)

_GRADE_THRESHOLDS = [
    (90, "A+"),
    (80, "A"),
    (70, "B+"),
    (60, "B"),
    (50, "C+"),
    (40, "C"),
    (30, "D"),
    (0,  "F"),
]

_AXIS_MAX = {"accuracy": 10, "clarity": 6, "fluency": 4}
_TOTAL_MARKS = 20

_LANGUAGE_NAMES = {"en": "English", "si": "Sinhala"}

# Silence check (D-07): silent clips were graded A+. A take needs at least
# 300 ms of 20 ms windows louder than about -36 dBFS, and must be 0.5 s long.
_MIN_DURATION_S = 0.5
_WINDOW_RMS_THRESHOLD = 0.015
_MIN_SPEECH_MS = 300

_NO_SPEECH_SUMMARY = {
    "en": "We couldn't hear any speech in this recording. Please record again and read the words aloud.",
    "si": "මෙම පටිගත කිරීමේ කතාවක් ඇසුනේ නැත. කරුණාකර නැවත පටිගත කර වචන හඬ නගා කියවන්න.",
}

_SYSTEM_PROMPT = """\
You are an English pronunciation assessor. You will hear a learner reading a target text aloud \
and you must evaluate how well they pronounced it.

Important context: The learner is a Sinhala speaker learning English in Sri Lanka. \
Sri Lankan English is a valid variety of English. Do NOT penalise accent features that are \
typical of Sri Lankan English, such as retroflex consonants, dental stops, syllable-timed \
rhythm, or localised vowel quality. Judge the speech on intelligibility and accuracy \
against the target text, not on conformity to a British or American accent.

Grade the recording out of 20 marks total, distributed across 3 axes:
1. accuracy (max 10 marks) — Were the correct words spoken? Are individual sounds and phonemes \
recognisable? Did the learner cover all the words in the target text?
2. clarity (max 6 marks) — Is the speech clear and easy for an educated English listener \
to understand? Is the volume and articulation adequate?
3. fluency (max 4 marks) — Is the pace natural and appropriate? Minimal hesitation, \
repetition, or unnatural pausing.

Critical: the target text is given to tell you what to LISTEN FOR — it is not evidence that the \
learner said it. Do not assume success just because the target is a short or common word. Actually \
transcribe what you hear in the audio first, then compare that transcription against the target text. \
If the audio is silent, wordless (breathing, background noise, non-speech sound), mumbled beyond \
recognition, or clearly says something other than the target text, accuracy MUST be scored 0-2 \
regardless of how short or familiar the target word is — do not give credit for a plausible-sounding \
guess. Short/common words deserve the SAME scrutiny as long ones, not less.

Provide ALL text (summary and feedback items) in the requested feedback language only.

Respond ONLY with valid JSON matching this exact schema:
{
  "transcript": "<exactly what you heard, word for word; empty string if no words were spoken>",
  "accuracy": <integer 0-10>,
  "clarity": <integer 0-6>,
  "fluency": <integer 0-4>,
  "summary": "<1–2 sentence overall comment on the attempt>",
  "feedback": {
    "accuracy": ["<specific observation>", "<specific observation>"],
    "clarity": ["<observation>"],
    "fluency": ["<observation>"]
  }
}

Rules:
- Each feedback array must contain 1–3 complete sentences.
- Be encouraging and specific — cite examples from what you heard where possible.
- Marks must not exceed their stated maximum (accuracy ≤ 10, clarity ≤ 6, fluency ≤ 4).
- Total marks must not exceed 20.
- Do not include any text outside the JSON object.\
"""


@dataclass
class PronunciationResult:
    accuracy: float
    clarity: float
    fluency: float
    overall_score: float
    grade: str
    summary: str
    feedback: dict
    ai_model: str


def _score_to_grade(score: float) -> str:
    for threshold, grade in _GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


def audio_has_speech(audio_bytes: bytes, audio_mime_type: str) -> bool:
    """Rough check that a recording contains speech.

    Only 16-bit PCM WAV is measured; other formats return True and are left
    to the model (which must also return an empty transcript for silence).
    """
    if "wav" not in (audio_mime_type or "").lower():
        return True
    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as w:
            if w.getsampwidth() != 2:
                return True
            rate = w.getframerate() or 16000
            channels = w.getnchannels() or 1
            frames = w.readframes(w.getnframes())
    except (wave.Error, EOFError):
        return True

    import array

    samples = array.array("h")
    samples.frombytes(frames[: len(frames) - (len(frames) % 2)])
    if channels > 1:
        samples = samples[::channels]
    if len(samples) / rate < _MIN_DURATION_S:
        return False

    window = max(1, rate // 50)  # 20 ms
    voiced = 0
    for start in range(0, len(samples), window):
        chunk = samples[start : start + window]
        rms = math.sqrt(sum((v / 32768.0) ** 2 for v in chunk) / len(chunk))
        if rms >= _WINDOW_RMS_THRESHOLD:
            voiced += 1
    return voiced * 20 >= _MIN_SPEECH_MS


def _no_speech_result(feedback_language: str) -> PronunciationResult:
    summary = _NO_SPEECH_SUMMARY.get(feedback_language, _NO_SPEECH_SUMMARY["en"])
    return PronunciationResult(
        accuracy=0.0,
        clarity=0.0,
        fluency=0.0,
        overall_score=0.0,
        grade="F",
        summary=summary,
        feedback={"accuracy": [summary], "clarity": [], "fluency": []},
        ai_model="no-speech-check",
    )


def _default_failed_result() -> PronunciationResult:
    return PronunciationResult(
        accuracy=0.0,
        clarity=0.0,
        fluency=0.0,
        overall_score=0.0,
        grade="F",
        summary="",
        feedback={"accuracy": [], "clarity": [], "fluency": []},
        ai_model="none",
    )


async def grade(
    audio_bytes: bytes,
    audio_mime_type: str,
    target_text: str,
    feedback_language: str = "en",
) -> PronunciationResult:
    """Grade a pronunciation recording using Gemini multimodal.

    Never raises — falls back to a zero score on any Gemini or parse error.
    """
    from app.core.config import settings

    if not audio_has_speech(audio_bytes, audio_mime_type):
        logger.info("pronunciation no speech detected bytes=%d", len(audio_bytes))
        return _no_speech_result(feedback_language)

    if not getattr(settings, "gemini_api_key", None):
        logger.warning("pronunciation gemini_api_key missing — using fallback grade")
        return _default_failed_result()

    try:
        return await _call_gemini(audio_bytes, audio_mime_type, target_text, feedback_language)
    except Exception as exc:
        logger.exception(
            "pronunciation gemini call failed target_chars=%d error=%s",
            len(target_text),
            exc,
        )
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except Exception:
            pass
        return _default_failed_result()


async def _call_gemini(
    audio_bytes: bytes,
    audio_mime_type: str,
    target_text: str,
    feedback_language: str,
) -> PronunciationResult:
    import httpx
    import json
    from app.core.config import settings

    lang_name = _LANGUAGE_NAMES.get(feedback_language, "English")
    model = settings.gemini_model

    audio_b64 = base64.b64encode(audio_bytes).decode()

    system_prompt = _SYSTEM_PROMPT + f"\n\nFeedback language: {lang_name}"
    user_msg = f"Target text: '{target_text}'"

    logger.info(
        "pronunciation gemini request model=%s audio_bytes=%d mime=%s target_chars=%d",
        model,
        len(audio_bytes),
        audio_mime_type,
        len(target_text),
    )

    gemini_url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            gemini_url,
            params={"key": settings.gemini_api_key},
            json={
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": audio_mime_type,
                                "data": audio_b64,
                            }
                        },
                        {"text": user_msg},
                    ]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0,
                },
            },
        )
        if resp.is_error:
            body_preview = resp.text[:500] if resp.text else "(empty)"
            logger.error(
                "pronunciation gemini http error status=%s body=%s",
                resp.status_code,
                body_preview,
            )
            resp.raise_for_status()
        data = resp.json()

    try:
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("Gemini returned no candidates")
        text = candidates[0]["content"]["parts"][0]["text"]
        scores = json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        logger.error(
            "pronunciation gemini response parse failed error=%s response_keys=%s",
            exc,
            list(data.keys()) if isinstance(data, dict) else type(data).__name__,
        )
        raise

    required = ("accuracy", "clarity", "fluency", "summary")
    missing = [k for k in required if k not in scores]
    if missing:
        raise ValueError(f"Gemini response missing fields: {missing}")

    # The model must say what it heard. No words means no marks (D-07).
    # (Only when the field is present, so a model that skips it isn't failed.)
    transcript = str(scores.get("transcript") or "").strip()
    if "transcript" in scores and not any(ch.isalpha() for ch in transcript):
        logger.info("pronunciation empty transcript, forcing no-speech result")
        return _no_speech_result(feedback_language)

    accuracy = min(float(scores["accuracy"]), _AXIS_MAX["accuracy"])
    clarity  = min(float(scores["clarity"]),  _AXIS_MAX["clarity"])
    fluency  = min(float(scores["fluency"]),  _AXIS_MAX["fluency"])

    overall = (accuracy + clarity + fluency) / _TOTAL_MARKS * 100
    grade = _score_to_grade(overall)

    logger.info(
        "pronunciation gemini success accuracy=%.1f clarity=%.1f fluency=%.1f overall=%.1f grade=%s",
        accuracy, clarity, fluency, overall, grade,
    )

    return PronunciationResult(
        accuracy=accuracy,
        clarity=clarity,
        fluency=fluency,
        overall_score=overall,
        grade=grade,
        summary=scores.get("summary", ""),
        feedback=scores.get("feedback", {"accuracy": [], "clarity": [], "fluency": []}),
        ai_model=model,
    )
