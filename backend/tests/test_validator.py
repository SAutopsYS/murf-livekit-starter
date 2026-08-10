"""Day 5 Bonus 7: exercise validation and sanitization."""

from __future__ import annotations

from tools.exercise_tool import get_next_exercise
from tools.provider_health import ProviderHealth
from tools.request_cache import RequestCache
from tools.session_cache import SessionExerciseCache
from tools.validator import ExerciseValidator


class _InvalidProvider:
    def fetch_exercise(self, level: str):
        del level
        return {"id": "x", "topic": "T", "title": "", "exercise": "body"}


def test_valid_exercise_passes() -> None:
    validator = ExerciseValidator()
    result = validator.validate(
        {
            "id": " b1 ",
            "topic": " Greetings ",
            "title": " Introduce Yourself ",
            "exercise": " Introduce yourself. ",
        }
    )
    assert result["valid"] is True
    assert result["exercise"]["id"] == "b1"
    assert result["exercise"]["topic"] == "Greetings"


def test_missing_field_rejected() -> None:
    validator = ExerciseValidator()
    result = validator.validate({"id": "1", "topic": "t", "title": "t"})
    assert result["valid"] is False


def test_empty_string_rejected() -> None:
    validator = ExerciseValidator()
    result = validator.validate(
        {"id": "1", "topic": "t", "title": "   ", "exercise": "body"}
    )
    assert result["valid"] is False


def test_wrong_type_rejected() -> None:
    validator = ExerciseValidator()
    result = validator.validate(
        {"id": 1, "topic": "t", "title": "t", "exercise": "body"}
    )
    assert result["valid"] is False


def test_provider_fallback_after_invalid_response() -> None:
    result = get_next_exercise(
        "beginner",
        provider=_InvalidProvider(),  # type: ignore[arg-type]
        source="api",
        health=ProviderHealth(cooldown_seconds=30),
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert result.get("error") is not True
    assert result["source"] == "local_dataset"


def test_local_dataset_validation() -> None:
    result = get_next_exercise(
        "intermediate",
        source="local",
        cache=SessionExerciseCache(),
        request_cache=RequestCache(ttl_seconds=0),
    )
    assert result.get("error") is not True
    for field in ("id", "topic", "title", "exercise"):
        assert isinstance(result[field], str) and result[field].strip()
