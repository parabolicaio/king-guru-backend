"""Supabase Admin API client.

Used for three operations:
  1. Revoke all sessions for a user (on DELETE /users/me)
  2. Update app_metadata JWT claim (on admin role change — Slice 8)
  3. Purge a user's uploaded recordings from Storage (on DELETE /users/me)

All calls use the service-role key with no retry logic.  Failures are logged
and swallowed so a Supabase API outage never blocks a DB-level operation.
"""

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(10.0)


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
        "apikey": settings.supabase_anon_key,
        "Content-Type": "application/json",
    }


async def sign_out_user(supabase_uid: str) -> None:
    """Revoke all active sessions for the given Supabase user.

    Called during account deletion.  Swallows errors — the DB-level
    soft-delete has already happened and must not be rolled back if Supabase
    is unreachable.
    """
    url = f"{settings.supabase_url}/auth/v1/admin/users/{supabase_uid}/logout"
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, headers=_headers(), params={"scope": "global"})
            if resp.status_code not in (200, 204):
                logger.warning(
                    "Supabase sign-out returned %s for uid=%s: %s",
                    resp.status_code,
                    supabase_uid,
                    resp.text,
                )
    except Exception:
        logger.exception("Supabase sign-out failed for uid=%s", supabase_uid)


# Bucket that holds pronunciation-practice recordings uploaded in
# attempts.py::_score_pronunciation under recordings/{user_id}/{attempt_id}.{ext}.
_RECORDINGS_BUCKET = "audio"
_LIST_PAGE_SIZE = 100


async def delete_user_recordings(user_id: str) -> None:
    """Purge all objects under recordings/{user_id}/ in the ``audio`` bucket.

    Called during account deletion so the user's uploaded voice recordings are
    removed alongside their PII — the account-deletion promise in the privacy
    policy / Play Data-safety form requires this (GDPR/COPPA).

    Lists the folder (paginated) then bulk-deletes.  Swallows errors — like the
    other admin calls, the DB-level soft-delete has already happened and must
    not be rolled back if Storage is unreachable.  A failure here leaves orphan
    files behind, which is a cleanup problem, not a data-integrity one.
    """
    prefix = f"recordings/{user_id}"
    list_url = f"{settings.supabase_url}/storage/v1/object/list/{_RECORDINGS_BUCKET}"
    delete_url = f"{settings.supabase_url}/storage/v1/object/{_RECORDINGS_BUCKET}"
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            paths: list[str] = []
            offset = 0
            while True:
                resp = await client.post(
                    list_url,
                    headers=_headers(),
                    json={
                        "prefix": prefix,
                        "limit": _LIST_PAGE_SIZE,
                        "offset": offset,
                    },
                )
                resp.raise_for_status()
                objects = resp.json()
                # Storage returns file entries with a non-null ``id``; folder
                # pseudo-entries have id=None and cannot be deleted by path.
                for obj in objects:
                    name = obj.get("name")
                    if name and obj.get("id") is not None:
                        paths.append(f"{prefix}/{name}")
                if len(objects) < _LIST_PAGE_SIZE:
                    break
                offset += _LIST_PAGE_SIZE

            if not paths:
                return

            del_resp = await client.request(
                "DELETE",
                delete_url,
                headers=_headers(),
                json={"prefixes": paths},
            )
            if del_resp.status_code not in (200, 204):
                logger.warning(
                    "Supabase recordings delete returned %s for user_id=%s: %s",
                    del_resp.status_code,
                    user_id,
                    del_resp.text,
                )
    except Exception:
        logger.exception("Supabase recordings purge failed for user_id=%s", user_id)


async def update_admin_role_claim(supabase_uid: str, admin_role: str | None) -> None:
    """Update the app_metadata.admin_role JWT claim for a user.

    Called when an Admin changes another user's role (Slice 8).
    The updated claim takes effect on the user's NEXT token refresh.
    Swallows errors with a structured log.
    """
    url = f"{settings.supabase_url}/auth/v1/admin/users/{supabase_uid}"
    body = {"app_metadata": {"admin_role": admin_role}}
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.put(url, headers=_headers(), json=body)
            if resp.status_code != 200:
                logger.warning(
                    "Supabase claim update returned %s for uid=%s: %s",
                    resp.status_code,
                    supabase_uid,
                    resp.text,
                )
    except Exception:
        logger.exception("Supabase claim update failed for uid=%s", supabase_uid)
