"""Day 9 Phase 6: shared conversation context and read-only specialist memory."""

from __future__ import annotations

from pathlib import Path

import pytest

from memory.database import temporary_database
from memory.repository import initialize_database
from memory.tools import fetch_user_memory, save_user_memory
from specialists.handoff import execute_handback, execute_handoff
from specialists.math_specialist import MathPracticeSpecialist
from specialists.prompts import MATH_SPECIALIST_PROMPT
from specialists.registry import reset_specialist_registry
from specialists.schemas import SpecialistContext
from specialists.shared_context import (
    CONTEXT_RECOVERY_EN,
    SharedContextManager,
    continuity_opening,
    get_shared_context_manager,
    sanitize_mapping,
)


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "shared-context.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


def test_context_created() -> None:
    manager = SharedContextManager()
    context = manager.build(
        language="en",
        learner_level="beginner",
        conversation_summary="Started fractions",
        current_math_question="Can you teach fractions?",
        previous_solved_exercises=["2+2"],
        recommendations=["try decimals next"],
    )
    assert isinstance(context, SpecialistContext)
    assert context.context_available is True
    assert context.active_lesson == "fractions"
    assert context.current_topic == "fractions"
    report = manager.validate(context)
    assert report["usable"] is True


@pytest.mark.asyncio
async def test_memory_shared(memory_db: Path) -> None:
    del memory_db
    saved = await save_user_memory(
        object(),
        user_id="shared-learner",
        name="Saloni",
        language_preference="hindi",
        learning_level="intermediate",
        last_topics=["fractions"],
        consent=True,
    )
    assert saved is not None
    manager = SharedContextManager()
    snapshot = manager.read_memory("shared-learner")
    assert snapshot is not None
    assert snapshot["learning_level"] == "intermediate"
    assert snapshot["language_preference"] == "hindi"
    assert snapshot["preferred_name"] == "Saloni"
    assert snapshot["last_topics"] == ["fractions"]
    context = manager.build(
        user_id="shared-learner",
        current_math_question="1/2 + 1/4",
    )
    assert context.memory_ref is not None
    assert context.learner_preferences is not None
    assert context.learner_preferences["learning_level"] == "intermediate"


@pytest.mark.asyncio
async def test_read_only_memory(memory_db: Path) -> None:
    del memory_db
    await save_user_memory(
        object(),
        user_id="readonly-learner",
        language_preference="english",
        learning_level="beginner",
        last_topics=["addition"],
        consent=True,
    )
    manager = SharedContextManager()
    blocked = manager.write_memory(
        user_id="readonly-learner",
        learning_level="advanced",
    )
    assert blocked["error"] is True
    assert blocked["saved"] is False
    profile = fetch_user_memory("readonly-learner")
    assert profile is not None
    assert profile["learning_level"] == "beginner"
    specialist = MathPracticeSpecialist()
    names = {
        getattr(tool, "name", getattr(tool, "__name__", ""))
        for tool in specialist.tools
    }
    assert "save_user_memory" not in names
    assert "lookup_user" not in names


def test_progress_transferred() -> None:
    manager = SharedContextManager()
    current = manager.build(
        language="en",
        learner_level="beginner",
        current_math_question="1/2 + 1/4",
        previous_solved_exercises=["6x7"],
        learning_history=["tables"],
    )
    merged = manager.merge_handback(
        current,
        solved_exercise_summary="Solved 1/2 + 1/4",
        completion_status="completed",
        updated_learning_level="intermediate",
    )
    assert "Solved 1/2 + 1/4" in merged.previous_solved_exercises
    assert merged.completion_status == "completed"
    assert merged.updated_learning_level == "intermediate"
    assert merged.learning_streak >= 1


def test_recommendations_transferred() -> None:
    manager = SharedContextManager()
    context = manager.build(
        language="en",
        current_math_question="Help me with percentages",
        recommendations=["continue same level", "try word problems"],
    )
    assert context.recommendations == ["continue same level", "try word problems"]
    merged = manager.merge_handback(
        context,
        recommendations=["advance to intermediate"],
        completion_status="completed",
    )
    assert merged.recommendations == ["advance to intermediate"]


def test_language_transferred() -> None:
    manager = SharedContextManager()
    context = manager.build(
        language="hi",
        current_math_question="भिन्न सिखाओ",
    )
    assert context.language == "hi"
    userdata: dict[str, object] = {}
    manager.transfer(userdata, context, active_agent="math_specialist")
    loaded, recovered = manager.load_or_recover(userdata)
    assert recovered is False
    assert loaded.language == "hi"


def test_learner_level_transferred() -> None:
    manager = SharedContextManager()
    context = manager.build(
        learner_level="advanced",
        current_math_question="Let's practice multiplication",
    )
    assert context.learner_level == "advanced"
    assert context.updated_learning_level == "advanced"


def test_topic_transferred() -> None:
    manager = SharedContextManager()
    context = manager.build(current_math_question="Can you teach fractions?")
    assert context.current_topic == "fractions"
    assert context.active_lesson == "fractions"
    opening = continuity_opening(context)
    assert "fractions" in opening.lower()
    assert "what you were learning" not in opening.lower()
    assert "I see you're practicing" in opening


def test_context_sanitization() -> None:
    manager = SharedContextManager()
    dirty = SpecialistContext(
        language="en",
        conversation_summary="Practicing fractions. OTP 123456",
        current_math_question="1/2 + 1/4",
        memory_ref={
            "user_id": "secret-learner",
            "learning_level": "beginner",
            "phone": "9999999999",
            "password": "hunter2",
        },
    )
    cleaned = manager.sanitize(dirty)
    public = cleaned.as_public_dict()
    blob = str(public)
    assert "secret-learner" not in blob
    assert "hunter2" not in blob
    assert "9999999999" not in blob
    assert "OTP 123456" not in cleaned.conversation_summary
    assert cleaned.memory_ref is not None
    assert "user_id" not in cleaned.memory_ref
    assert cleaned.memory_ref["learning_level"] == "beginner"


def test_missing_context_recovery() -> None:
    manager = SharedContextManager()
    recovered = manager.recover()
    assert recovered.context_available is False
    assert recovered.language == "en"
    assert continuity_opening(recovered) == CONTEXT_RECOVERY_EN
    loaded, was_recovered = manager.load_or_recover({"specialist_context": "bad"})
    assert was_recovered is True
    assert loaded.context_available is False
    specialist = MathPracticeSpecialist(specialist_context=recovered)
    assert specialist.continuity_opening() == CONTEXT_RECOVERY_EN
    assert "information available" in MATH_SPECIALIST_PROMPT


def test_privacy_filtering() -> None:
    payload = {
        "language": "en",
        "conversation_summary": "Practicing tables",
        "user_id": "learner-99",
        "phone_number": "9876543210",
        "otp": "654321",
        "password": "hunter2",
        "api_key": "sk-secret",
        "transcript": "full spoken transcript",
        "current_math_question": "7 x 8",
    }
    cleaned = sanitize_mapping(payload)
    blob = str(cleaned)
    assert "learner-99" not in blob
    assert "9876543210" not in blob
    assert "654321" not in blob
    assert "hunter2" not in blob
    assert "sk-secret" not in blob
    assert "full spoken transcript" not in blob
    assert cleaned["conversation_summary"] == "Practicing tables"
    assert cleaned["current_math_question"] == "7 x 8"
    assert "user_id" not in cleaned


def test_successful_handback_context() -> None:
    userdata: dict[str, object] = {}
    handed = execute_handoff(
        user_text="Can you teach fractions?",
        current_math_question="1/2 + 1/4",
        learner_level="beginner",
        language="en",
        conversation_summary="Started fractions",
        recommendations=["try another fraction"],
        userdata=userdata,
    )
    assert handed["handed_off"] is True
    assert handed["context"]["language"] == "en"
    assert handed["context"]["learner_level"] == "beginner"
    assert handed["context"]["current_topic"] == "fractions"
    returned = execute_handback(
        reason="solved",
        problem_solved=True,
        solved_exercise_summary="Solved 1/2 + 1/4",
        conversation_summary="Finished fractions",
        recommendations=["try decimals next"],
        userdata=userdata,
        completion_status="completed",
        updated_learning_level="intermediate",
    )
    assert returned["returned"] is True
    context = returned["context"]
    assert context["solved_exercise_summary"] == "Solved 1/2 + 1/4"
    assert context["recommendations"] == ["try decimals next"]
    assert context["completion_status"] == "completed"
    assert context["updated_learning_level"] == "intermediate"
    assert context["language"] == "en"
    assert "user_id" not in str(context)


def test_shared_manager_is_reusable() -> None:
    first = get_shared_context_manager()
    second = get_shared_context_manager()
    assert first is second
    userdata = {"user_id": "stay", "specialist_context": {"language": "en"}}
    first.clear_temporary(userdata)
    assert "specialist_context" not in userdata
    assert userdata["user_id"] == "stay"
    assert userdata["active_agent"] == "main"
