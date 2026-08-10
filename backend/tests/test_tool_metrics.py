"""Day 5 Bonus 4: tool performance metrics and execution timing."""

from __future__ import annotations

from tools.exercise_tool import get_next_exercise
from tools.metrics import get_tool_metrics, reset_tool_metrics
from tools.recommendation import recommend_next_practice
from tools.score_tool import score_spoken_answer
from tools.session_cache import SessionExerciseCache


def test_tool_call_and_success_counts() -> None:
    reset_tool_metrics()
    cache = SessionExerciseCache()
    result = get_next_exercise("beginner", source="local", cache=cache)
    assert result.get("error") is not True

    metrics = get_tool_metrics()
    assert metrics["exercise_tool"]["calls"] == 1
    assert metrics["exercise_tool"]["success"] == 1
    assert metrics["exercise_tool"]["failures"] == 0
    assert metrics["exercise_tool"]["average_ms"] >= 0


def test_failure_count_increments() -> None:
    reset_tool_metrics()
    failed = score_spoken_answer("hi", "beginner")
    assert failed.get("error") is True

    metrics = get_tool_metrics()
    assert metrics["score_tool"]["calls"] == 1
    assert metrics["score_tool"]["success"] == 0
    assert metrics["score_tool"]["failures"] == 1


def test_average_execution_time_and_reset() -> None:
    reset_tool_metrics()
    recommend_next_practice(88, "beginner")
    recommend_next_practice(40, "beginner")
    metrics = get_tool_metrics()
    assert metrics["recommendation_tool"]["calls"] == 2
    assert metrics["recommendation_tool"]["average_ms"] >= 0

    reset_tool_metrics()
    assert get_tool_metrics() == {}


def test_score_success_metrics() -> None:
    reset_tool_metrics()
    answer = (
        "Hello, my name is Saloni. I wake up early and drink tea. "
        "I like reading books every morning."
    )
    scored = score_spoken_answer(answer, "beginner")
    assert scored.get("error") is not True
    metrics = get_tool_metrics()
    assert metrics["score_tool"]["success"] == 1
