"""Azure Neural TTS service — generates audio for vocabulary words.

Runs as a BackgroundTasks job. Never raises — errors are swallowed and logged
to Sentry; audio_url stays null until the job succeeds.
"""

import logging

from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)


def generate_async(
    background_tasks: BackgroundTasks,
    vocabulary_word_id: str,
    text_en: str,
    text_si: str | None,
) -> None:
    """Queue TTS generation as a background task.

    English audio is always generated.
    Sinhala audio generated only when text_si is provided.
    Singlish is text-only — no audio generated (language code guard inside job).
    """
    background_tasks.add_task(_run_tts, vocabulary_word_id, text_en, text_si)


async def _run_tts(
    vocabulary_word_id: str,
    text_en: str,
    text_si: str | None,
) -> None:
    """Background job: call Azure TTS, upload to Supabase Storage, update vocabulary_word.audio_url.

    On any Azure or upload error: log to Sentry, leave audio_url null, do not raise.
    """
    try:
        from app.core.config import settings
        from app.db.pool import get_pool

        audio_url = await _call_azure_tts(text_en, language="en-US", voice="en-US-JennyNeural")

        if audio_url:
            pool = await get_pool()
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE vocabulary_word SET audio_url = $1, updated_at = now() WHERE id = $2::uuid",
                    audio_url, vocabulary_word_id,
                )
    except Exception as exc:
        logger.exception("TTS generation failed for word %s: %s", vocabulary_word_id, exc)
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except Exception:
            pass


async def _call_azure_tts(
    text: str,
    language: str,
    voice: str,
) -> str | None:
    """Call Azure Neural TTS API. Returns Supabase Storage path or None on error."""
    try:
        from app.core.config import settings

        if not settings.azure_tts_key or not settings.azure_tts_region:
            logger.warning("Azure TTS credentials not configured — skipping TTS generation")
            return None

        import httpx
        import uuid

        endpoint = (
            f"https://{settings.azure_tts_region}.tts.speech.microsoft.com"
            "/cognitiveservices/v1"
        )
        ssml = (
            f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'>"
            f"<voice name='{voice}'>{text}</voice></speak>"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": settings.azure_tts_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-48khz-192kbitrate-mono-mp3",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(endpoint, content=ssml.encode(), headers=headers)
            resp.raise_for_status()
            audio_bytes = resp.content

        # Upload to Supabase Storage via REST API
        file_name = f"tts/{uuid.uuid4()}.mp3"
        storage_url = (
            f"{settings.supabase_url}/storage/v1/object/audio/{file_name}"
        )
        upload_headers = {
            "Authorization": f"Bearer {settings.supabase_service_role_key}",
            "Content-Type": "audio/mpeg",
        }
        async with httpx.AsyncClient(timeout=30) as upload_client:
            up_resp = await upload_client.post(storage_url, content=audio_bytes, headers=upload_headers)
            up_resp.raise_for_status()
        return f"audio/{file_name}"

    except Exception:
        raise
