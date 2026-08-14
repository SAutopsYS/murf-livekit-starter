"""Day 9 Bonus 6: deterministic intent confidence and clarification."""

from __future__ import annotations

import logging

import pytest

from specialists.confidence import (
    CLARIFICATION_EN,
    confidence_band,
    score_routing_confidence,
)
from specialists.registry import reset_specialist_registry
from specialists.router import SpecialistRouter
from specialists.schemas import RouteTarget, SpecialistContext


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_high_confidence_routes() -> None:
    result = SpecialistRouter().route("solve 24 x 18")
    assert result["target"] == RouteTarget.MATH_SPECIALIST.value
    assert result["confidence"] >= 0.70


def test_medium_confidence_clarification() -> None:
    result = SpecialistRouter().route("I need help")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result.get("clarification") is True
    assert result.get("message") == CLARIFICATION_EN
    assert 0.40 <= result["confidence"] <= 0.69


def test_low_confidence_stays_main() -> None:
    result = SpecialistRouter().route("asdfgh qwerty")
    assert result["target"] == RouteTarget.UNKNOWN.value
    assert result["confidence"] < 0.40


def test_ambiguous_homework_query() -> None:
    result = SpecialistRouter().route("My homework is difficult")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result["reason"] == "clarification_needed"


def test_greeting_science_english_stay() -> None:
    router = SpecialistRouter()
    assert router.route("Hello")["target"] == RouteTarget.MAIN_AGENT.value
    assert (
        router.route("What is photosynthesis?")["target"]
        == RouteTarget.MAIN_AGENT.value
    )
    assert (
        router.route("Help me with English grammar")["target"]
        == RouteTarget.MAIN_AGENT.value
    )


def test_context_aware_and_confidence_calculation() -> None:
    context = SpecialistContext(current_topic="fractions", active_lesson="fractions")
    score, reason = score_routing_confidence("Can you teach fractions?", context)
    assert score >= 0.70
    assert "fraction" in reason
    assert confidence_band(0.92) == "high"
    assert confidence_band(0.55) == "medium"
    assert confidence_band(0.10) == "low"


def test_privacy_safe_confidence_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        SpecialistRouter().route("I need help with password hunter2")
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Clarification requested" in text or "Routing decision" in text
    assert "hunter2" not in text
    assert "password" not in text
