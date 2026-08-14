"""Day 9 Phase 5: multi-specialist routing architecture."""

from __future__ import annotations

import logging

import pytest

from specialists.context import build_specialist_context
from specialists.intent import detect_intent
from specialists.registry import (
    MATH_SPECIALIST_ID,
    PLACEHOLDER_SPECIALISTS,
    SpecialistSpec,
    get_specialist_registry,
    list_specialists,
    register_specialist,
    reset_specialist_registry,
    unregister_specialist,
)
from specialists.router import SpecialistRouter, get_specialist_router
from specialists.schemas import RouteTarget, SpecialistContext


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_math_routed() -> None:
    router = get_specialist_router()
    result = router.route("Let's practice multiplication")
    assert result["target"] == RouteTarget.MATH_SPECIALIST.value
    assert result["specialist_id"] == MATH_SPECIALIST_ID
    assert result["fallback_used"] is False
    assert detect_intent("I need help solving 24 x 18") == "math"


def test_greeting_stays_main_agent() -> None:
    result = get_specialist_router().route("Hello")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result["specialist_id"] is None
    assert detect_intent("Namaste") == "main"


def test_science_stays_main_agent() -> None:
    result = get_specialist_router().route("Explain photosynthesis")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert detect_intent("What is gravity?") == "main"


def test_english_stays_main_agent() -> None:
    result = get_specialist_router().route("Help me with English grammar")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert detect_intent("Let's do speaking practice") == "main"


def test_unknown_stays_main_agent() -> None:
    result = get_specialist_router().route("asdfgh qwerty")
    assert result["target"] == RouteTarget.UNKNOWN.value
    assert result["fallback_used"] is True
    assert result["reason"] == "unknown_stays_main"
    assert detect_intent("asdfgh qwerty") == "unknown"


def test_registry_works() -> None:
    active = list_specialists()
    assert len(active) == 1
    assert active[0]["specialist_id"] == MATH_SPECIALIST_ID
    assert active[0]["active"] is True

    listed = list_specialists(include_placeholders=True)
    ids = {item["specialist_id"] for item in listed}
    assert MATH_SPECIALIST_ID in ids
    for placeholder_id, _name in PLACEHOLDER_SPECIALISTS:
        assert placeholder_id in ids

    register_specialist(
        SpecialistSpec(
            specialist_id="temp_specialist",
            name="Temp Specialist",
            track="learning_and_literacy",
            active=False,
            factory=None,
        )
    )
    ids_after = {
        item["specialist_id"] for item in list_specialists(include_placeholders=True)
    }
    assert "temp_specialist" in ids_after
    assert unregister_specialist("temp_specialist") is True
    ids_final = {
        item["specialist_id"] for item in list_specialists(include_placeholders=True)
    }
    assert "temp_specialist" not in ids_final


def test_placeholders_do_not_route() -> None:
    router = get_specialist_router()
    assert router.validate("english_specialist") is False
    assert router.validate("science_specialist") is False
    result = router.route("Help me with English grammar")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result["specialist_id"] is None


def test_router_fallback_when_math_unregistered() -> None:
    unregister_specialist(MATH_SPECIALIST_ID)
    router = SpecialistRouter(get_specialist_registry())
    result = router.route("Let's practice multiplication")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result["fallback_used"] is True
    assert result["reason"] == "math_specialist_unavailable"


def test_context_preserved() -> None:
    router = get_specialist_router()
    context = router.share_context(
        language="hi",
        learner_level="beginner",
        conversation_summary="Wants tables",
        current_math_question="7 x 8",
        previous_solved_exercises=["2+2"],
        learning_history=["addition"],
        recommendations=["try division"],
    )
    assert isinstance(context, SpecialistContext)
    assert context.language == "hi"
    assert context.learner_level == "beginner"
    assert context.current_math_question == "7 x 8"
    assert context.previous_solved_exercises == ["2+2"]
    rebuilt = build_specialist_context(existing=context, conversation_summary="Updated")
    assert rebuilt.language == "hi"
    assert rebuilt.learner_level == "beginner"
    assert rebuilt.conversation_summary == "Updated"


def test_logging_safe(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        get_specialist_router().route("Let's practice multiplication. Password=hunter2")
    messages = " ".join(record.getMessage() for record in caplog.records)
    assert "Routing started" in messages
    assert "Routing decision" in messages
    assert "Specialist selected" in messages
    assert "Password" not in messages
    assert "hunter2" not in messages
    assert "multiplication" not in messages
