"""Day 5 Final Bonus: production-readiness smoke verification."""

from __future__ import annotations

from pathlib import Path

from agent import AGENT_TOOLS, SYSTEM_PROMPT
from tools import LEARNING_TOOLS
from tools.chaining import resolve_exercise_level
from tools.exercise_tool import get_next_exercise
from tools.manager import get_tool_manager
from tools.metrics import get_tool_metrics, reset_tool_metrics
from tools.provider_health import ProviderHealth
from tools.registry import list_tools
from tools.request_cache import RequestCache
from tools.score_tool import score_spoken_answer
from tools.recommendation import recommend_next_practice
from tools.session_cache import SessionExerciseCache


def test_learning_tools_registered_on_agent() -> None:
    names = {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in AGENT_TOOLS}
    assert "get_next_exercise" in names
    assert "score_spoken_answer" in names
    assert "recommend_next_practice" in names
    assert "lookup_user" in names
    assert "search_learning_knowledge" in names
    assert LEARNING_TOOLS


def test_practice_chain_smoke() -> None:
    reset_tool_metrics()
    level = resolve_exercise_level({"learning_level": "beginner"})
    assert level == "beginner"

    exercise = get_next_exercise(
        level,
        source="local",
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert exercise.get("error") is not True

    scored = score_spoken_answer(
        "Hello, my name is Saloni. I practice English every morning with short stories.",
        level,
    )
    assert scored.get("error") is not True

    recommendation = recommend_next_practice(scored["score"], level)
    assert recommendation.get("error") is not True

    follow_up = get_next_exercise(
        recommendation["next_level"],
        source="local",
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert follow_up.get("error") is not True
    assert get_tool_metrics()["exercise_tool"]["calls"] >= 2


def test_api_failure_falls_back_without_error() -> None:
    class _FailProvider:
        def fetch_exercise(self, level: str):
            del level
            return None

    result = get_next_exercise(
        "beginner",
        provider=_FailProvider(),  # type: ignore[arg-type]
        source="api",
        health=ProviderHealth(cooldown_seconds=30),
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert result.get("error") is not True
    assert result["source"] == "local_dataset"


def test_registry_and_manager_ready() -> None:
    assert len(list_tools()) == 3
    managed = get_tool_manager().execute("get_next_exercise", level="advanced")
    assert managed.get("error") is not True


def test_prompt_covers_day5_flows() -> None:
    assert "EXERCISES" in SYSTEM_PROMPT
    assert "SCORING" in SYSTEM_PROMPT
    assert "FOLLOW-UP PRACTICE" in SYSTEM_PROMPT
    assert "TOPIC PRACTICE" in SYSTEM_PROMPT


def test_datasets_present() -> None:
    root = Path(__file__).resolve().parents[1] / "src"
    assert (root / "tools" / "resources" / "exercises.json").exists()
    assert (root / "knowledge" / "resources" / "english_basics.json").exists()
