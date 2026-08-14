"""Day 9 Bonus 9: production hardening and resource cleanup."""

from __future__ import annotations

import logging

import pytest

from specialists.handoff import execute_handoff
from specialists.metrics import get_specialist_metrics, reset_specialist_metrics
from specialists.registry import get_specialist_registry, reset_specialist_registry
from specialists.router import SpecialistRouter
from specialists.shared_context import SharedContextManager


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    reset_specialist_metrics()
    yield
    reset_specialist_registry()
    reset_specialist_metrics()


def test_invalid_context_and_missing_specialist() -> None:
    manager = SharedContextManager()
    loaded, recovered = manager.load_or_recover({"specialist_context": 123})
    assert recovered is True
    assert loaded.context_available is False
    result = execute_handoff(user_text="Hello")
    assert result.get("error") is True
    assert "Traceback" not in str(result)


def test_registry_and_analytics_unavailable() -> None:
    registry = get_specialist_registry()
    assert registry.get("missing") is None
    assert registry.set_health("missing", "READY") is False
    snap = get_specialist_metrics()
    assert snap["total_handoffs"] == 0


def test_no_duplicate_registry_or_router() -> None:
    first = get_specialist_registry()
    second = get_specialist_registry()
    assert first is second
    router = SpecialistRouter(first)
    again = SpecialistRouter(first)
    assert router.validate("math_practice_specialist") is again.validate(
        "math_practice_specialist"
    )


def test_cleanup_on_session_end() -> None:
    userdata = {
        "user_id": "stay",
        "specialist_context": {"language": "en"},
        "resume_from_specialist": True,
    }
    SharedContextManager().clear_temporary(userdata)
    assert "specialist_context" not in userdata
    assert userdata["user_id"] == "stay"


def test_logging_is_minimal_and_private(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        SpecialistRouter().route("Let's practice multiplication")
        execute_handoff(user_text="Let's practice multiplication")
    messages = [record.getMessage() for record in caplog.records]
    assert "Routing started" in messages
    assert all("OTP" not in item for item in messages)
    assert all("password" not in item.lower() for item in messages)
