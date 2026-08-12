"""100% coverage — JWT decode logic in app.core.security.

All tests call decode_token() directly with crafted tokens so no DB or
FastAPI app is needed.
"""

import pytest

from app.core.errors import AppError
from app.core.security import decode_token
from tests.conftest import TEST_JWT_SECRET, make_token

SECRET = TEST_JWT_SECRET


# ── Happy path ───────────────────────────────────────────────────────────────

def test_valid_email_token():
    token = make_token(email="a@b.com", phone=None)
    payload = decode_token(token, SECRET)
    assert payload.supabase_uid == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    assert payload.email == "a@b.com"
    assert payload.phone is None
    assert payload.admin_role is None


def test_valid_phone_token():
    token = make_token(email=None, phone="+94771234567")
    payload = decode_token(token, SECRET)
    assert payload.phone == "+94771234567"
    assert payload.email is None


def test_admin_role_extracted():
    token = make_token(admin_role="admin")
    payload = decode_token(token, SECRET)
    assert payload.admin_role == "admin"


def test_content_manager_role_extracted():
    token = make_token(admin_role="content_manager")
    payload = decode_token(token, SECRET)
    assert payload.admin_role == "content_manager"


def test_no_admin_role_in_metadata():
    token = make_token(admin_role=None)
    payload = decode_token(token, SECRET)
    assert payload.admin_role is None


# ── Failure paths ────────────────────────────────────────────────────────────

def test_expired_token_raises_jwt_expired():
    token = make_token(expired=True)
    with pytest.raises(AppError) as exc:
        decode_token(token, SECRET)
    assert exc.value.status_code == 401
    assert exc.value.detail["code"] == "JWT_EXPIRED"


def test_bad_signature_raises_jwt_invalid():
    token = make_token(bad_signature=True)
    with pytest.raises(AppError) as exc:
        decode_token(token, SECRET)
    assert exc.value.status_code == 401
    assert exc.value.detail["code"] == "JWT_INVALID"


def test_garbage_string_raises_jwt_invalid():
    with pytest.raises(AppError) as exc:
        decode_token("not.a.token", SECRET)
    assert exc.value.detail["code"] == "JWT_INVALID"


def test_empty_string_raises_jwt_invalid():
    with pytest.raises(AppError) as exc:
        decode_token("", SECRET)
    assert exc.value.detail["code"] == "JWT_INVALID"


def test_missing_sub_raises_jwt_invalid():
    token = make_token(omit_sub=True)
    with pytest.raises(AppError) as exc:
        decode_token(token, SECRET)
    assert exc.value.detail["code"] == "JWT_INVALID"


def test_wrong_secret_raises_jwt_invalid():
    token = make_token(secret=SECRET)
    with pytest.raises(AppError) as exc:
        decode_token(token, "completely-different-secret")
    assert exc.value.detail["code"] == "JWT_INVALID"
