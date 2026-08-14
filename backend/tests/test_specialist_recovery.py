"""Day 9 Bonus 4: fault-tolerant handoff and recovery."""

from __future__ import annotations

import logging

import pytest

from specialists.handoff import execute_handoff
from specialists.metrics import get_specialist_metrics, reset_specialist_metrics
from specialists.prompts import handoff_fallback_notice
from specialists.registry import (
    MATH_SPECIALIST_ID,
    disable_specialist,
    reset_specialist_registry,
    unregister_specialist,
)
from specialists.schemas import SpecialistContext


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    reset_specialist_metrics()
    yield
    reset_specialist_registry()
    reset_specialist_metrics()


def test_specialist_unavailable() -> None:
    unregister_specialist(MATH_SPECIALIST_ID)
    result = execute_handoff(user_text="Let's practice multiplication", language="en")
    assert result["handed_off"] is False
    assert result.get("error") is True


def test_disabled_specialist() -> None:
    disable_specialist(MATH_SPECIALIST_ID)
    result = execute_handoff(user_text="Help me with fractions", language="en")
    assert result["handed_off"] is False


def test_timeout_and_init_and_prompt_failures() -> None:
    def _timeout(_ctx: SpecialistContext) -> object:
        raise TimeoutError("timeout")

    timeout = execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        specialist_factory=_timeout,
    )
    assert timeout["code"] == "specialist_timeout"
    assert timeout["message"] == handoff_fallback_notice("en")

    def _init(_ctx: SpecialistContext) -> object:
        raise RuntimeError("initialization error")

    init = execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        specialist_factory=_init,
    )
    assert init["code"] == "specialist_start_failed"

    def _prompt(_ctx: SpecialistContext) -> object:
        raise ValueError("prompt loading failure")

    prompt = execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        specialist_factory=_prompt,
    )
    assert prompt["code"] == "prompt_load_failed"


def test_retry_once_only() -> None:
    calls = {"n": 0}

    def _flaky(_ctx: SpecialistContext) -> object:
        calls["n"] += 1
        raise RuntimeError("still down")

    execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        specialist_factory=_flaky,
    )
    assert calls["n"] == 2
    assert get_specialist_metrics()["retry_count"] == 1


def test_fallback_preserves_context_and_structured_error() -> None:
    userdata: dict[str, object] = {}

    def _boom(_ctx: SpecialistContext) -> object:
        raise RuntimeError("boom")

    result = execute_handoff(
        user_text="Let's practice multiplication",
        current_math_question="6 x 7",
        language="en",
        learner_level="beginner",
        conversation_summary="Started multiplication",
        userdata=userdata,
        specialist_factory=_boom,
    )
    assert result["handed_off"] is False
    assert "stack" not in str(result).lower()
    assert "Traceback" not in str(result)
    assert result["context"]["learner_level"] == "beginner"
    assert result["context"]["current_math_question"] == "6 x 7"
    assert userdata["active_agent"] == "main"


def test_no_duplicate_success_after_failure() -> None:
    result = execute_handoff(user_text="Hello")
    assert result["handed_off"] is False
    assert result.get("agent") is None


def test_privacy_safe_recovery_logs(caplog: pytest.LogCaptureFixture) -> None:
    def _boom(_ctx: SpecialistContext) -> object:
        raise RuntimeError("boom")

    with caplog.at_level(logging.INFO, logger="specialists.events"):
        execute_handoff(
            user_text="SECRET_ANSWER 24 x 18",
            language="en",
            specialist_factory=_boom,
        )
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Retry attempted" in text
    assert "Recovery triggered" in text
    assert "SECRET_ANSWER" not in text
