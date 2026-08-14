"""Day 9 Bonus 3: shared context synchronization."""

from __future__ import annotations

import logging

import pytest

from specialists.conversation_state import (
    ConversationState,
    conversation_state_from_context,
)
from specialists.handoff import execute_handback, execute_handoff
from specialists.math_specialist import MathPracticeSpecialist
from specialists.registry import reset_specialist_registry
from specialists.schemas import SpecialistContext
from specialists.shared_context import SharedContextManager
from specialists.sync import (
    build_incremental_progress,
    synchronize_progress,
    synchronize_recommendation,
)


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_shared_context_creation() -> None:
    context = SharedContextManager().build(
        language="en",
        learner_level="beginner",
        current_math_question="Can you teach fractions?",
        conversation_summary="Started fractions",
    )
    state = conversation_state_from_context(
        context, session_id="s1", active_agent="math_specialist"
    )
    assert state.preferred_language == "en"
    assert state.learner_level == "beginner"
    assert state.conversation_summary == "Started fractions"


def test_memory_read_only_enforcement() -> None:
    manager = SharedContextManager()
    blocked = manager.write_memory(user_id="x", learning_level="advanced")
    assert blocked["saved"] is False
    names = {
        getattr(tool, "name", getattr(tool, "__name__", ""))
        for tool in MathPracticeSpecialist().tools
    }
    assert "save_user_memory" not in names


def test_recommendation_and_progress_sync() -> None:
    context = SpecialistContext(language="en", learner_level="beginner")
    state = ConversationState(learner_level="beginner")
    incremental = build_incremental_progress(
        completed="Multiplication Level 2",
        score="9/10",
        recommendation="Practice Fractions",
        mastery_score="9/10",
        next_topic="fractions",
        skill_level="intermediate",
    )
    assert "transcript" not in incremental
    context, state = synchronize_progress(context, state, incremental)
    context, state = synchronize_recommendation(
        context,
        state,
        recommendation="Practice Fractions",
    )
    assert "Multiplication Level 2" in context.completed_lessons
    assert state.mastery_score == "9/10"
    assert state.next_topic == "fractions"
    assert context.recommendations == ["Practice Fractions"]
    context, state = synchronize_recommendation(
        context,
        state,
        recommendation="Practice Fractions",
    )
    assert context.recommendations == ["Practice Fractions"]


def test_specialist_history_and_main_receives_update() -> None:
    userdata: dict[str, object] = {}
    execute_handoff(
        user_text="Let's practice multiplication",
        current_math_question="6 x 7",
        language="en",
        learner_level="beginner",
        userdata=userdata,
    )
    returned = execute_handback(
        reason="solved",
        problem_solved=True,
        solved_exercise_summary="Solved 6 x 7",
        recommendations=["try fractions next"],
        userdata=userdata,
    )
    assert returned["returned"] is True
    history = userdata["conversation_state"]["specialist_history"]
    assert history
    assert returned["context"]["recommendations"] == ["try fractions next"]


def test_no_transcript_sync_and_privacy_logs(caplog: pytest.LogCaptureFixture) -> None:
    context = SpecialistContext(conversation_summary="Practicing tables")
    state = ConversationState()
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        synchronize_progress(
            context,
            state,
            {"completed": "tables", "transcript": "secret speech"},
        )
    public = state.as_public_dict() if hasattr(state, "as_public_dict") else {}
    blob = str(public) + str(context.as_public_dict())
    assert "secret speech" not in blob
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Progress synchronized" in text
    assert "secret" not in text.lower() or "secret speech" not in text
