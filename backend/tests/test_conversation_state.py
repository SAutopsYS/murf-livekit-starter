"""Day 9 Bonus 7: unified conversation state."""

from __future__ import annotations

import logging

import pytest

from specialists.conversation_state import (
    ConversationState,
    append_specialist_history,
    apply_state_to_userdata,
    conversation_state_from_context,
    read_state_from_userdata,
    validate_conversation_state,
)
from specialists.handoff import execute_handback, execute_handoff
from specialists.registry import MATH_SPECIALIST_ID, reset_specialist_registry
from specialists.schemas import SpecialistContext
from specialists.sync import synchronize_progress, synchronize_recommendation


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_conversation_state_creation() -> None:
    context = SpecialistContext(
        language="en", learner_level="beginner", current_topic="fractions"
    )
    state = conversation_state_from_context(context, session_id="room-1")
    assert isinstance(state, ConversationState)
    assert state.session_id == "room-1"
    assert state.preferred_language == "en"
    assert "transcript" not in state.as_public_dict()


def test_specialist_history_tracking() -> None:
    state = ConversationState(session_id="s1")
    append_specialist_history(
        state,
        specialist_id=MATH_SPECIALIST_ID,
        outcome="completed",
        reason_for_handoff="math_request",
    )
    assert len(state.specialist_history) == 1
    assert state.specialist_history[0]["specialist_id"] == MATH_SPECIALIST_ID


def test_recommendation_and_progress_sharing() -> None:
    context = SpecialistContext()
    state = ConversationState()
    synchronize_progress(
        context, state, {"completed": "fractions", "mastery_score": "8/10"}
    )
    synchronize_recommendation(context, state, recommendation="try decimals")
    assert state.mastery_score == "8/10"
    assert "try decimals" in state.recommendations


def test_context_validation_and_missing_field_fallback() -> None:
    state = ConversationState(preferred_language="", active_agent="")
    report = validate_conversation_state(state)
    assert report["usable"] is True
    assert state.preferred_language == "en"
    assert state.active_agent == "main"
    empty = validate_conversation_state(None)
    assert empty["usable"] is True


def test_privacy_safe_context() -> None:
    state = ConversationState(
        conversation_summary="Practicing tables",
        recommendations=["try fractions"],
    )
    public = state.as_public_dict()
    assert "transcript" not in public
    assert "password" not in public
    assert "otp" not in public


def test_main_tutor_receives_updated_state() -> None:
    userdata: dict[str, object] = {"analytics_call_id": "room-9"}
    execute_handoff(
        user_text="Let's practice multiplication",
        language="en",
        userdata=userdata,
    )
    execute_handback(
        reason="solved",
        problem_solved=True,
        recommendations=["try fractions next"],
        userdata=userdata,
    )
    state = read_state_from_userdata(userdata)
    assert state.active_agent == "main"
    assert state.previous_agent == "math_specialist"
    assert "try fractions next" in state.recommendations


def test_future_specialist_compatibility() -> None:
    state = ConversationState(active_agent="main")
    append_specialist_history(
        state,
        specialist_id="english_specialist",
        outcome="placeholder",
        reason_for_handoff="not_enabled",
    )
    userdata: dict[str, object] = {}
    apply_state_to_userdata(userdata, state)
    loaded = read_state_from_userdata(userdata)
    assert loaded.specialist_history[0]["specialist_id"] == "english_specialist"


def test_privacy_safe_state_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        conversation_state_from_context(
            SpecialistContext(language="en"), session_id="s"
        )
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Context created" in text
    assert "transcript" not in text
