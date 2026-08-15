"""Day 5 Bonus 6: topic-aware exercise filtering."""

from __future__ import annotations

import pytest

from agent import SYSTEM_PROMPT
from tools.exercise_tool import get_next_exercise
from tools.livekit_tools import get_next_exercise as livekit_get_next_exercise
from tools.request_cache import RequestCache
from tools.session_cache import SessionExerciseCache


def test_topic_filtering_and_case_insensitive() -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    result = get_next_exercise(
        "beginner",
        topic="GREETING",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    assert result.get("error") is not True
    assert "greet" in result["topic"].lower()


def test_partial_topic_matching() -> None:
    result = get_next_exercise(
        "advanced",
        topic="tech",
        source="local",
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert result.get("error") is not True
    assert "technology" in result["topic"].lower()


def test_unknown_topic_falls_back() -> None:
    result = get_next_exercise(
        "beginner",
        topic="quantum-physics",
        source="local",
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert result.get("error") is not True
    assert result["level"] == "beginner"


def test_prompt_has_topic_practice() -> None:
    assert "TOPIC PRACTICE" in SYSTEM_PROMPT


def test_session_rotation_with_topic() -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    first = get_next_exercise(
        "beginner",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    second = get_next_exercise(
        "beginner",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    assert first["id"] != second["id"]


@pytest.mark.asyncio
async def test_livekit_topic_parameter() -> None:
    result = await livekit_get_next_exercise(
        object(), level="beginner", topic="routine"
    )
    assert result.get("error") is not True
