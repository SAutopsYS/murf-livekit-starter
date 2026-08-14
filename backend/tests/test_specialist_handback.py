"""Day 9 Phase 4: Math Practice Specialist → Main Agent handback."""

from __future__ import annotations

import logging
from pathlib import Path
from types import SimpleNamespace

import pytest

from agent import Assistant
from memory.database import temporary_database
from memory.repository import initialize_database
from memory.tools import fetch_user_memory, save_user_memory
from specialists.context import build_specialist_context
from specialists.handoff import execute_handback, execute_handoff, return_to_main_agent
from specialists.intent import should_return_to_main
from specialists.prompts import (
    MAIN_AGENT_RESUME_EN,
    build_main_agent_resume_instructions,
    handback_notice,
)
from specialists.registry import reset_specialist_registry
from specialists.schemas import SpecialistContext


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "specialist-handback.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


class _FakeSession:
    def __init__(self, userdata: dict[str, object] | None = None) -> None:
        self.userdata = userdata or {}
        self.updated = None

    async def update_agent(self, agent: object) -> None:
        self.updated = agent


def test_solved_math_problem_returns_to_main_agent() -> None:
    assert should_return_to_main("done", problem_solved=True) is True
    result = execute_handback(
        reason="solved",
        solved_exercise_summary="Solved 6x7",
        problem_solved=True,
        current_context=SpecialistContext(language="en", learner_level="beginner"),
    )
    assert result.get("error") is not True
    assert result["returned"] is True
    assert isinstance(result.get("agent"), Assistant)
    assert result["agent"]._resume_from_specialist is True


def test_topic_change_returns_to_main_agent() -> None:
    assert should_return_to_main("What is photosynthesis?") is True
    result = execute_handback(
        user_text="What is photosynthesis?",
        reason="topic_change",
        current_context=SpecialistContext(language="en"),
    )
    assert result["returned"] is True


def test_thank_you_triggers_return() -> None:
    assert should_return_to_main("Thank you") is True
    result = execute_handback(
        user_text="Thank you",
        reason="thank_you",
        current_context=SpecialistContext(language="en"),
    )
    assert result["returned"] is True
    assert "main learning assistant" in result["message"].lower()


def test_conversation_context_preserved() -> None:
    current = SpecialistContext(
        language="en",
        learner_level="intermediate",
        conversation_summary="Practicing fractions",
        current_math_question="1/2 + 1/4",
        previous_solved_exercises=["6x7"],
        learning_history=["tables"],
        recommendations=["try decimals next"],
    )
    result = execute_handback(
        reason="solved",
        problem_solved=True,
        solved_exercise_summary="Solved 1/2 + 1/4",
        conversation_summary="Finished fractions",
        current_context=current,
    )
    context = result["context"]
    assert context["conversation_summary"] == "Finished fractions"
    assert "Solved 1/2 + 1/4" in context["previous_solved_exercises"]
    assert context["recommendations"] == ["try decimals next"]
    assert context["current_math_question"] == "1/2 + 1/4"


@pytest.mark.asyncio
async def test_memory_preserved(memory_db: Path) -> None:
    del memory_db
    saved = await save_user_memory(
        object(),
        user_id="handback-learner",
        language_preference="hindi",
        learning_level="beginner",
        last_topics=["math"],
        consent=True,
    )
    assert saved is not None
    context = build_specialist_context(
        user_id="handback-learner",
        current_math_question="2 + 2",
        language="hi",
    )
    assert context.memory_ref is not None
    assert context.memory_ref["learning_level"] == "beginner"
    result = execute_handback(
        reason="solved",
        problem_solved=True,
        current_context=context,
    )
    assert result["returned"] is True
    assert result["context"]["memory_ref"]["learning_level"] == "beginner"
    assert result["context"]["memory_ref"]["language_preference"] == "hindi"
    profile = fetch_user_memory("handback-learner")
    assert profile is not None
    assert profile["learning_level"] == "beginner"
    assert profile["last_topics"] == ["math"]


def test_language_preserved() -> None:
    result = execute_handback(
        reason="completed",
        practice_completed=True,
        current_context=SpecialistContext(language="hi", learner_level="beginner"),
    )
    assert result["context"]["language"] == "hi"
    assert "मुख्य शिक्षण सहायक" in result["message"]


def test_failed_handback_fallback() -> None:
    def _boom(**_kwargs: object) -> object:
        raise RuntimeError("main agent unavailable")

    result = execute_handback(
        reason="solved",
        problem_solved=True,
        current_context=SpecialistContext(language="en"),
        main_agent_factory=_boom,
    )
    assert result.get("error") is True
    assert result["returned"] is False
    assert result["fallback"] == "specialist_continues"


def test_main_agent_resumes_correctly() -> None:
    tutor = Assistant(resume_from_specialist=True)
    assert tutor._resume_from_specialist is True
    instructions = build_main_agent_resume_instructions(
        "resume-learner",
        {"language": "en", "learner_level": "beginner"},
    )
    assert "Do not restart the conversation" in instructions
    assert MAIN_AGENT_RESUME_EN in instructions
    assert "resume-learner" in instructions
    assert handback_notice("en")


@pytest.mark.asyncio
async def test_handback_tool_updates_session_agent() -> None:
    userdata = {
        "user_id": "tool-learner",
        "specialist_context": SpecialistContext(language="en").as_public_dict(),
    }
    session = _FakeSession(userdata)
    result = await return_to_main_agent(
        SimpleNamespace(session=session),
        reason="solved",
        solved_exercise_summary="Solved 2+2",
        conversation_summary="Math done",
    )
    assert result.get("error") is not True
    assert result["returned"] is True
    assert isinstance(session.updated, Assistant)
    assert session.userdata["resume_from_specialist"] is True
    assert session.userdata["active_agent"] == "main"


def test_handoff_then_handback_keeps_progress() -> None:
    userdata: dict[str, object] = {}
    handed = execute_handoff(
        user_text="Let's practice multiplication",
        current_math_question="8 x 9",
        learner_level="advanced",
        language="en",
        conversation_summary="Started with multiplication",
        userdata=userdata,
    )
    assert handed["handed_off"] is True
    returned = execute_handback(
        reason="solved",
        problem_solved=True,
        solved_exercise_summary="Solved 8 x 9",
        userdata=userdata,
    )
    assert returned["returned"] is True
    assert returned["context"]["learner_level"] == "advanced"
    assert returned["context"]["language"] == "en"
    assert "Solved 8 x 9" in returned["context"]["previous_solved_exercises"]


def test_handback_logging_is_privacy_safe(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        execute_handback(
            user_text="Thank you OTP 123456",
            reason="thank_you",
            current_context=SpecialistContext(language="en"),
        )
    messages = " ".join(record.getMessage() for record in caplog.records)
    assert "Handback requested" in messages
    assert "Handback completed" in messages
    assert "OTP" not in messages
    assert "123456" not in messages
