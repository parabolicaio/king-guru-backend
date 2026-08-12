"""Unit tests for the in-process rate limiter (app/core/ratelimit.py)."""

from types import SimpleNamespace

import pytest

from app.core import ratelimit
from app.core.errors import AppError


def _req(*, auth=None, guest=None, xff=None, host="1.2.3.4"):
    headers = {}
    if auth:
        headers["authorization"] = auth
    if guest:
        headers["x-guest-token"] = guest
    if xff:
        headers["x-forwarded-for"] = xff
    return SimpleNamespace(headers=headers, client=SimpleNamespace(host=host))


@pytest.fixture(autouse=True)
def _clear_hits():
    ratelimit._hits.clear()
    yield
    ratelimit._hits.clear()


async def test_allows_up_to_limit_then_blocks():
    dep = ratelimit.rate_limit(3, 60, "t1")
    req = _req(host="10.0.0.1")
    for _ in range(3):
        await dep(req)  # within budget — no raise
    with pytest.raises(AppError) as ei:
        await dep(req)
    assert ei.value.status_code == 429
    assert ei.value.detail["code"] == "RATE_LIMITED"


async def test_separate_callers_have_separate_budgets():
    dep = ratelimit.rate_limit(1, 60, "t2")
    await dep(_req(host="10.0.0.2"))
    await dep(_req(host="10.0.0.3"))  # different IP → own budget
    with pytest.raises(AppError):
        await dep(_req(host="10.0.0.2"))  # first IP again → blocked


async def test_scopes_are_isolated():
    a = ratelimit.rate_limit(1, 60, "scope_a")
    b = ratelimit.rate_limit(1, 60, "scope_b")
    req = _req(host="10.0.0.9")
    await a(req)
    await b(req)  # different scope → not affected by scope_a's hit
    with pytest.raises(AppError):
        await a(req)


async def test_auth_token_keyed_not_ip():
    dep = ratelimit.rate_limit(1, 60, "t4")
    # Same IP, different bearer tokens → independent budgets.
    await dep(_req(auth="Bearer aaa", host="9.9.9.9"))
    await dep(_req(auth="Bearer bbb", host="9.9.9.9"))
    with pytest.raises(AppError):
        await dep(_req(auth="Bearer aaa", host="9.9.9.9"))


async def test_window_expiry_allows_again(monkeypatch):
    clock = {"t": 1000.0}
    monkeypatch.setattr(ratelimit.time, "monotonic", lambda: clock["t"])
    dep = ratelimit.rate_limit(1, 60, "t5")
    req = _req(host="10.0.0.5")
    await dep(req)
    with pytest.raises(AppError):
        await dep(req)
    clock["t"] += 61  # window elapsed
    await dep(req)  # allowed again


async def test_xff_takes_precedence_over_client_host():
    dep = ratelimit.rate_limit(1, 60, "t6")
    # Two requests from the same proxy host but different real client IPs.
    await dep(_req(xff="203.0.113.7, 10.0.0.1", host="10.0.0.1"))
    await dep(_req(xff="203.0.113.8, 10.0.0.1", host="10.0.0.1"))  # different XFF → own budget
    with pytest.raises(AppError):
        await dep(_req(xff="203.0.113.7, 10.0.0.1", host="10.0.0.1"))
