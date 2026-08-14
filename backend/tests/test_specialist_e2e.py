"""Day 9 Bonus 8: end-to-end multi-agent conversation paths."""

from __future__ import annotations

import logging
import time

import pytest

from specialists.handoff import execute_handback, execute_handoff
from specialists.intent import detect_intent, should_handoff_to_math
from specialists.metrics import reset_specialist_metrics
from specialists.registry import (
    MATH_SPECIALIST_ID,
    disable_specialist,
    get_specialist_registry,
    reset_specialist_registry,
)
from specialists.router import SpecialistRouter
from specialists.schemas import RouteTarget, SpecialistContext


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    reset_specialist_metrics()
    yield
    reset_specialist_registry()
    reset_specialist_metrics()


@pytest.mark.parametrize(
    ("utterance", "expect_math"),
    [
        ("Hello", False),
        ("How do I introduce myself?", False),
        ("What is photosynthesis?", False),
        ("Help me with English grammar", False),
        ("I need help solving 24 x 18", True),
        ("Let's practice multiplication", True),
        ("Can you teach fractions?", True),
        ("Help me with percentages", True),
        ("Help me with algebra", True),
        ("Help me with geometry", True),
    ],
)
def test_end_to_end_conversation_paths(utterance: str, expect_math: bool) -> None:
    assert should_handoff_to_math(utterance) is expect_math
    result = execute_handoff(user_text=utterance, language="en")
    assert result["handed_off"] is expect_math


def test_topic_change_thank_you_handback() -> None:
    userdata: dict[str, object] = {"analytics_call_id": "e2e-1"}
    handed = execute_handoff(
        user_text="Let's practice multiplication",
        language="hi",
        learner_level="beginner",
        conversation_summary="Wants tables",
        userdata=userdata,
    )
    assert handed["handed_off"] is True
    assert handed["context"]["language"] == "hi"
    thanks = execute_handback(
        user_text="Thank you", reason="thank_you", userdata=userdata
    )
    assert thanks["returned"] is True
    change = execute_handoff(
        user_text="Let's practice multiplication", userdata=userdata
    )
    back = execute_handback(
        user_text="What is photosynthesis?",
        reason="topic_change",
        userdata=userdata,
    )
    assert change["handed_off"] is True
    assert back["returned"] is True


def test_routing_disabled_unknown_and_registry() -> None:
    router = SpecialistRouter()
    assert router.route("Hello")["target"] == RouteTarget.MAIN_AGENT.value
    assert router.route("xyzabc")["target"] == RouteTarget.UNKNOWN.value
    disable_specialist(MATH_SPECIALIST_ID)
    assert router.route("Let's practice multiplication")["fallback_used"] is True
    assert get_specialist_registry().get(MATH_SPECIALIST_ID) is not None


def test_recovery_timeout_retry() -> None:
    def _timeout(_ctx: SpecialistContext) -> object:
        raise TimeoutError("timeout")

    result = execute_handoff(
        user_text="Let's practice multiplication",
        specialist_factory=_timeout,
        language="en",
        learner_level="advanced",
        conversation_summary="Keep this",
    )
    assert result["handed_off"] is False
    assert result["context"]["learner_level"] == "advanced"


def test_performance_latencies() -> None:
    started = time.perf_counter()
    SpecialistRouter().route("Let's practice multiplication")
    routing_ms = (time.perf_counter() - started) * 1000
    started = time.perf_counter()
    execute_handoff(user_text="Help me with fractions")
    handoff_ms = (time.perf_counter() - started) * 1000
    started = time.perf_counter()
    execute_handback(
        reason="solved", problem_solved=True, current_context=SpecialistContext()
    )
    handback_ms = (time.perf_counter() - started) * 1000
    assert routing_ms < 250
    assert handoff_ms < 2000
    assert handback_ms < 2000


def test_privacy_e2e_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        execute_handoff(user_text="Let's practice multiplication. OTP 999111")
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "999111" not in text
    assert detect_intent("Hello") == "main"
