"""Day 5 Phase 5: memory-aware exercise chaining behavior."""

from __future__ import annotations

import logging

import pytest

from agent import SYSTEM_PROMPT
from tools.chaining import (
    LEVEL_FALLBACK_QUESTION,
    resolve_exercise_level,
    should_ask_for_level,
)
from tools.livekit_tools import get_next_exercise, score_spoken_answer


def test_prompt_requires_memory_aware_exercise_flow() -> None:
    assert "lookup_user" in SYSTEM_PROMPT
    assert "learning_level" in SYSTEM_PROMPT
    assert "get_next_exercise" in SYSTEM_PROMPT
    assert "Do not ask" in SYSTEM_PROMPT
    assert LEVEL_FALLBACK_QUESTION in SYSTEM_PROMPT
    assert "TOOL CHAINING" in SYSTEM_PROMPT
    assert "score_spoken_answer" in SYSTEM_PROMPT
    assert "Check my answer" in SYSTEM_PROMPT


def test_saved_level_skips_asking() -> None:
    profile = {
        "user_id": "learner_1",
        "learning_level": "Intermediate",
        "name": "Saloni",
    }
    assert resolve_exercise_level(profile) == "intermediate"
    assert should_ask_for_level(profile) is False


def test_missing_level_asks_learner() -> None:
    assert resolve_exercise_level(None) is None
    assert should_ask_for_level(None) is True
    assert should_ask_for_level({"learning_level": ""}) is True
    assert should_ask_for_level({"learning_level": "expert"}) is True
    assert LEVEL_FALLBACK_QUESTION.startswith("What is your English level?")


@pytest.mark.asyncio
async def test_exercise_tool_receives_resolved_level() -> None:
    profile = {"learning_level": "advanced"}
    level = resolve_exercise_level(profile)
    assert level == "advanced"

    result = await get_next_exercise(object(), level=level)
    assert result.get("error") is not True
    assert result["level"] == "advanced"
    assert result["source"] == "local_dataset"


@pytest.mark.asyncio
async def test_scoring_after_exercise_chain(caplog: pytest.LogCaptureFixture) -> None:
    level = resolve_exercise_level({"learning_level": "beginner"})
    assert level == "beginner"

    with caplog.at_level(logging.INFO, logger="tools.livekit"):
        exercise = await get_next_exercise(object(), level=level)
        assert exercise.get("error") is not True

        answer = (
            "Hello, my name is Saloni. I wake up early and drink tea. "
            "I like reading books every morning."
        )
        scored = await score_spoken_answer(object(), answer=answer, level=level)

    assert scored.get("error") is not True
    assert scored["level"] == "beginner"
    assert 0 <= scored["score"] <= 100

    messages = [record.getMessage() for record in caplog.records]
    assert "Using saved learning level" in messages
    assert "Exercise selected" in messages
    assert "Answer evaluated" in messages
    assert "Tool chain completed" in messages
