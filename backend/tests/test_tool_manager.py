"""Day 5 Bonus 9: unified tool manager execution pipeline."""

from __future__ import annotations

from tools.manager import ToolManager
from tools.metrics import get_tool_metrics, reset_tool_metrics
from tools.request_cache import reset_request_cache
from tools.session_cache import reset_session_exercise_cache


def test_manager_executes_exercise_score_and_recommendation() -> None:
    reset_tool_metrics()
    reset_session_exercise_cache()
    reset_request_cache()
    manager = ToolManager()

    exercise = manager.execute("get_next_exercise", level="beginner")
    assert exercise.get("error") is not True
    assert exercise["exercise"]

    scored = manager.execute(
        "score_spoken_answer",
        answer=(
            "Hello, my name is Saloni. I wake up early and drink tea. "
            "I like reading books every morning."
        ),
        level="beginner",
    )
    assert scored.get("error") is not True
    assert 0 <= scored["score"] <= 100

    recommendation = manager.execute(
        "recommend_next_practice",
        score=scored["score"],
        level="beginner",
    )
    assert recommendation.get("error") is not True
    assert recommendation["next_level"]

    metrics = get_tool_metrics()
    assert metrics["exercise_tool"]["calls"] >= 1
    assert metrics["score_tool"]["success"] >= 1
    assert metrics["recommendation_tool"]["calls"] >= 1


def test_manager_invalid_input_returns_structured_error() -> None:
    manager = ToolManager()
    result = manager.execute("get_next_exercise", level="")
    assert result == {
        "error": True,
        "message": "Tool execution unavailable.",
    }
