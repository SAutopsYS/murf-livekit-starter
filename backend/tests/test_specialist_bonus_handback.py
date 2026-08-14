"""Day 9 Bonus 1: natural specialist handback."""

from __future__ import annotations

import logging

import pytest

from specialists.closing import build_handback_summary, is_continue_request
from specialists.handoff import execute_handback
from specialists.intent import should_return_to_main
from specialists.prompts import (
    MAIN_AGENT_RESUME_EN,
    build_main_agent_resume_instructions,
)
from specialists.registry import reset_specialist_registry
from specialists.schemas import SpecialistContext


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_summary_generated() -> None:
    context = SpecialistContext(language="en", active_lesson="multiplication")
    summary = build_handback_summary(context, "en")
    assert summary.count(".") <= 2
    assert "multiplication" in summary.lower()
    assert "main learning assistant" in summary.lower()


def test_main_agent_resumes_naturally() -> None:
    instructions = build_main_agent_resume_instructions(
        "learner",
        {"language": "en", "learner_level": "beginner"},
    )
    assert MAIN_AGENT_RESUME_EN in instructions
    assert "Do not restart the conversation" in instructions
    assert "another activity" in MAIN_AGENT_RESUME_EN.lower()


def test_lets_continue_triggers_handback() -> None:
    assert is_continue_request("Let's continue") is True
    assert should_return_to_main("Let's continue") is True
    result = execute_handback(
        user_text="Let's continue",
        current_context=SpecialistContext(language="en", learner_level="beginner"),
    )
    assert result["returned"] is True


def test_context_and_recommendations_preserved() -> None:
    result = execute_handback(
        reason="solved",
        problem_solved=True,
        solved_exercise_summary="Solved 6x7",
        recommendations=["try fractions next"],
        current_context=SpecialistContext(
            language="hi",
            learner_level="intermediate",
            previous_solved_exercises=["2+2"],
        ),
    )
    assert result["context"]["language"] == "hi"
    assert result["context"]["recommendations"] == ["try fractions next"]
    assert "Solved 6x7" in result["context"]["previous_solved_exercises"]


def test_same_session_maintained() -> None:
    userdata: dict[str, object] = {"analytics_call_id": "room-1"}
    result = execute_handback(
        reason="solved",
        problem_solved=True,
        userdata=userdata,
        current_context=SpecialistContext(language="en"),
    )
    assert result["returned"] is True
    assert userdata["analytics_call_id"] == "room-1"
    assert userdata["active_agent"] == "main"


def test_privacy_safe_handback_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        execute_handback(
            user_text="Thank you OTP 111222",
            reason="thank_you",
            current_context=SpecialistContext(language="en"),
        )
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Handback requested" in text
    assert "Summary created" in text
    assert "Handback completed" in text
    assert "OTP" not in text
    assert "111222" not in text
