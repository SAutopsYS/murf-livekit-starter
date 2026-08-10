"""Day 5 Bonus 3: session-aware exercise rotation."""

from __future__ import annotations

import logging

from tools.exercise_tool import get_next_exercise
from tools.provider_health import ProviderHealth
from tools.request_cache import RequestCache
from tools.session_cache import SessionExerciseCache


class _FixedProvider:
    def __init__(self, result: dict[str, str]) -> None:
        self.result = result
        self.calls = 0

    def fetch_exercise(self, level: str) -> dict[str, str] | None:
        del level
        self.calls += 1
        return self.result


def test_different_exercises_within_session() -> None:
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
    assert first.get("error") is not True
    assert second.get("error") is not True
    assert first["id"] != second["id"]


def test_rotation_resets_after_all_used(caplog: logging.LogCaptureFixture) -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    seen: list[str] = []
    with caplog.at_level(logging.INFO, logger="tools.session_cache"):
        for _ in range(3):
            result = get_next_exercise(
                "beginner",
                source="local",
                cache=cache,
                request_cache=request_cache,
            )
            assert result.get("error") is not True
            seen.append(result["id"])

    assert len(set(seen[:2])) == 2
    assert seen[2] in set(seen[:2])
    assert "Exercise rotation restarted" in [
        record.getMessage() for record in caplog.records
    ]


def test_local_exercises_participate_in_rotation() -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    one = get_next_exercise(
        "intermediate",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    two = get_next_exercise(
        "intermediate",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    assert {one["id"], two["id"]} == {"i1", "i2"}


def test_api_exercises_participate_in_rotation() -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    health = ProviderHealth(cooldown_seconds=30)
    provider = _FixedProvider(
        {
            "id": "api-same",
            "level": "beginner",
            "topic": "API",
            "title": "Same",
            "exercise": "Repeat me.",
            "source": "external_api",
        }
    )

    first = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )
    second = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )

    assert first["source"] == "external_api"
    assert first["id"] == "api-same"
    # Duplicate API id is skipped; local unused exercise is returned instead.
    assert second["source"] == "local_dataset"
    assert second["id"] in {"b1", "b2"}
