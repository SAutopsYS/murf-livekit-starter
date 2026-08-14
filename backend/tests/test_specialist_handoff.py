"""Day 9 Phase 3: Main Agent → Math Practice Specialist handoff."""

from __future__ import annotations

import logging
from types import SimpleNamespace

import pytest

from agent import AGENT_TOOLS, SYSTEM_PROMPT, Assistant
from specialists.handoff import execute_handoff, handoff_to_math_specialist
from specialists.intent import should_handoff_to_math
from specialists.math_specialist import MathPracticeSpecialist
from specialists.prompts import (
    MATH_SPECIALIST_INTRODUCTION_EN,
    build_specialist_enter_instructions,
    handoff_fallback_notice,
    handoff_notice,
)
from specialists.registry import reset_specialist_registry


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def _tool_names(tools: list[object]) -> set[str]:
    return {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in tools}


class _FakeSession:
    def __init__(self) -> None:
        self.userdata: dict[str, object] = {"user_id": "handoff-learner"}
        self.updated = None

    async def update_agent(self, agent: object) -> None:
        self.updated = agent


def test_greeting_stays_with_main_agent() -> None:
    assert should_handoff_to_math("Hello") is False
    result = execute_handoff(user_text="Hello")
    assert result["handed_off"] is False
    assert result.get("error") is True


def test_science_stays_with_main_agent() -> None:
    assert should_handoff_to_math("What is photosynthesis?") is False
    result = execute_handoff(user_text="What is photosynthesis?")
    assert result["handed_off"] is False


def test_english_stays_with_main_agent() -> None:
    assert should_handoff_to_math("Help me with English grammar") is False
    result = execute_handoff(user_text="Help me improve my vocabulary")
    assert result["handed_off"] is False


def test_multiplication_triggers_handoff() -> None:
    assert should_handoff_to_math("Let's practice multiplication") is True
    result = execute_handoff(
        user_text="Let's practice multiplication",
        current_math_question="Let's practice multiplication",
        language="en",
        learner_level="beginner",
        conversation_summary="Learner wants tables",
    )
    assert result.get("error") is not True
    assert result["handed_off"] is True
    assert isinstance(result.get("agent"), MathPracticeSpecialist)


def test_fractions_trigger_handoff() -> None:
    assert should_handoff_to_math("Can you teach fractions?") is True
    result = execute_handoff(user_text="Can you teach fractions?")
    assert result["handed_off"] is True


def test_percentages_trigger_handoff() -> None:
    assert should_handoff_to_math("Help me with percentages") is True
    result = execute_handoff(user_text="Help me with percentages")
    assert result["handed_off"] is True


def test_geometry_triggers_handoff() -> None:
    assert should_handoff_to_math("Help me with geometry") is True
    result = execute_handoff(user_text="What is the area of a triangle?")
    assert result["handed_off"] is True


def test_specialist_introduction() -> None:
    specialist = MathPracticeSpecialist()
    assert specialist.introduction() == MATH_SPECIALIST_INTRODUCTION_EN
    instructions = build_specialist_enter_instructions(specialist.specialist_context)
    assert "Math Practice Specialist" in instructions


def test_context_transferred_correctly() -> None:
    userdata: dict[str, object] = {"user_id": "ctx-learner"}
    result = execute_handoff(
        user_text="I need help solving 24 x 18",
        current_math_question="24 x 18",
        conversation_summary="Learner asked for mental math",
        learner_level="intermediate",
        language="en",
        previous_solved_exercises=["6x7"],
        userdata=userdata,
    )
    assert result["handed_off"] is True
    context = result["context"]
    assert context["language"] == "en"
    assert context["learner_level"] == "intermediate"
    assert context["conversation_summary"] == "Learner asked for mental math"
    assert context["current_math_question"] == "24 x 18"
    assert context["previous_solved_exercises"] == ["6x7"]
    stored = userdata["specialist_context"]
    assert stored["current_math_question"] == "24 x 18"
    assert userdata["active_agent"] == "math_specialist"


def test_failed_handoff_fallback() -> None:
    def _boom(_context: object) -> object:
        raise RuntimeError("specialist unavailable")

    result = execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        specialist_factory=_boom,
    )
    assert result.get("error") is True
    assert result["handed_off"] is False
    assert result["message"] == handoff_fallback_notice("en")
    assert result["code"] == "specialist_start_failed"


def test_handoff_notice_is_not_silent() -> None:
    assert "Math Practice Specialist" in handoff_notice("en")
    assert "MATH SPECIALIST HANDOFF" in SYSTEM_PROMPT
    assert "Do not switch silently" in SYSTEM_PROMPT
    assert "handoff_to_math_specialist" in SYSTEM_PROMPT
    assert "handoff_to_math_specialist" in _tool_names(AGENT_TOOLS)
    assert isinstance(Assistant(), Assistant)


@pytest.mark.asyncio
async def test_handoff_tool_updates_session_agent() -> None:
    session = _FakeSession()
    result = await handoff_to_math_specialist(
        SimpleNamespace(session=session),
        current_math_question="Let's practice multiplication",
        conversation_summary="Math request",
        learner_level="beginner",
        language="en",
    )
    assert result.get("error") is not True
    assert result["handed_off"] is True
    assert isinstance(session.updated, MathPracticeSpecialist)


def test_handoff_logging_is_privacy_safe(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        execute_handoff(
            user_text="SECRET_TRANSCRIPT 24 x 18",
            current_math_question="SECRET_TRANSCRIPT 24 x 18",
        )
    messages = " ".join(record.getMessage() for record in caplog.records)
    assert "Handoff started" in messages
    assert "Handoff completed" in messages
    assert "SECRET_TRANSCRIPT" not in messages
    assert "24 x 18" not in messages
