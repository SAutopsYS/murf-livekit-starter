"""Day 5 Phase 4: Learning tool registration and LiveKit wrappers."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent import AGENT_TOOLS, SYSTEM_PROMPT
from tools import LEARNING_TOOLS, TOOLS
from tools.dataset import clear_dataset_cache, load_exercise_dataset
from tools.exercise_tool import get_next_exercise as lookup_next_exercise
from tools.livekit_tools import get_next_exercise, score_spoken_answer
from tools.metrics import reset_tool_metrics
from tools.provider import clear_exercise_config_cache
from tools.provider_health import (
    clear_provider_health_config_cache,
    reset_provider_health,
)
from tools.request_cache import clear_request_cache_config_cache, reset_request_cache
from tools.score_tool import score_spoken_answer as score_answer
from tools.session_cache import reset_session_exercise_cache


@pytest.fixture(autouse=True)
def _reset_dataset_cache():
    clear_dataset_cache()
    clear_exercise_config_cache()
    clear_provider_health_config_cache()
    clear_request_cache_config_cache()
    reset_provider_health()
    reset_session_exercise_cache()
    reset_request_cache()
    reset_tool_metrics()
    yield
    clear_dataset_cache()
    clear_exercise_config_cache()
    clear_provider_health_config_cache()
    clear_request_cache_config_cache()
    reset_provider_health()
    reset_session_exercise_cache()
    reset_request_cache()
    reset_tool_metrics()


def test_learning_tools_registered() -> None:
    learning_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in LEARNING_TOOLS
    ]
    assert "get_next_exercise" in learning_names
    assert "score_spoken_answer" in learning_names
    assert "recommend_next_practice" in learning_names
    assert TOOLS == LEARNING_TOOLS

    agent_tool_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in AGENT_TOOLS
    ]
    assert "get_next_exercise" in agent_tool_names
    assert "score_spoken_answer" in agent_tool_names
    assert "recommend_next_practice" in agent_tool_names
    assert "lookup_user" in agent_tool_names
    assert "search_learning_knowledge" in agent_tool_names


def test_prompt_includes_exercise_and_scoring_sections() -> None:
    assert "EXERCISES" in SYSTEM_PROMPT
    assert "get_next_exercise" in SYSTEM_PROMPT
    assert "SCORING" in SYSTEM_PROMPT
    assert "score_spoken_answer" in SYSTEM_PROMPT
    assert "Do not invent scoring." in SYSTEM_PROMPT


def test_exercise_dataset_exists() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "tools"
        / "resources"
        / "exercises.json"
    )
    assert path.exists()
    dataset = load_exercise_dataset()
    assert "beginner" in dataset
    assert dataset["beginner"]


@pytest.mark.asyncio
async def test_exercise_lookup_tool_succeeds() -> None:
    result = await get_next_exercise(object(), level="beginner")
    assert result.get("error") is not True
    assert result["level"] == "beginner"
    assert result["source"] == "local_dataset"
    assert result["exercise"]
    assert result["topic"]
    assert result["title"]


@pytest.mark.asyncio
async def test_exercise_lookup_tool_invalid_level() -> None:
    result = await get_next_exercise(object(), level="expert")
    assert result["error"] is True
    assert result["message"] == "Exercise dataset unavailable."


@pytest.mark.asyncio
async def test_score_tool_succeeds() -> None:
    answer = (
        "Hello, my name is Saloni. I wake up early and drink tea. "
        "I like reading books every morning."
    )
    result = await score_spoken_answer(object(), answer=answer, level="beginner")
    assert result.get("error") is not True
    assert result["source"] == "rule_based"
    assert 0 <= result["score"] <= 100
    assert isinstance(result["feedback"], list)
    assert result["metrics"]["word_count"] >= 3


@pytest.mark.asyncio
async def test_score_tool_invalid_input() -> None:
    empty = await score_spoken_answer(object(), answer="   ", level="beginner")
    assert empty["error"] is True
    assert empty["message"] == "Unable to score the spoken answer."

    unknown = await score_spoken_answer(
        object(),
        answer="This is a full practice answer with enough words.",
        level="expert",
    )
    assert unknown["error"] is True


def test_core_helpers_still_available() -> None:
    exercise = lookup_next_exercise("intermediate")
    assert exercise.get("error") is not True
    scored = score_answer(
        "I enjoy traveling because it helps me learn new cultures and languages.",
        "intermediate",
    )
    assert scored.get("error") is not True
