"""Day 5 Bonus 2: provider health cache and smart cooldown."""

from __future__ import annotations

import logging

import pytest

from tools.exercise_tool import get_next_exercise
from tools.provider_health import ProviderHealth, get_provider_health_config
from tools.request_cache import RequestCache
from tools.session_cache import SessionExerciseCache


class _CountingProvider:
    def __init__(self, result: dict[str, str] | None = None) -> None:
        self.result = result
        self.calls = 0

    def fetch_exercise(self, level: str) -> dict[str, str] | None:
        del level
        self.calls += 1
        return self.result


def test_provider_starts_healthy() -> None:
    health = ProviderHealth(cooldown_seconds=30)
    assert health.is_available() is True


def test_api_failure_starts_cooldown(caplog: pytest.LogCaptureFixture) -> None:
    health = ProviderHealth(cooldown_seconds=30)
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    provider = _CountingProvider(None)

    with caplog.at_level(logging.INFO):
        result = get_next_exercise(
            "beginner",
            provider=provider,  # type: ignore[arg-type]
            source="api",
            health=health,
            cache=cache,
            request_cache=request_cache,
        )

    assert result.get("error") is not True
    assert result["source"] == "local_dataset"
    assert provider.calls == 1
    assert health.is_available() is False
    messages = [record.getMessage() for record in caplog.records]
    assert "Cooldown started" in messages
    assert "Using local exercise" in messages


def test_cooldown_skips_api_requests() -> None:
    health = ProviderHealth(cooldown_seconds=30)
    health.mark_failure()
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    provider = _CountingProvider(None)

    result = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )

    assert result["source"] == "local_dataset"
    assert provider.calls == 0


def test_cooldown_expiration_retries_api() -> None:
    health = ProviderHealth(cooldown_seconds=10)
    health.mark_failure(now=0.0)
    assert health.is_available(now=5.0) is False
    assert health.is_available(now=11.0) is True

    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    provider = _CountingProvider(
        {
            "id": "api-b1",
            "level": "beginner",
            "topic": "Greetings",
            "title": "Hello",
            "exercise": "Introduce yourself.",
            "source": "external_api",
        }
    )
    result = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )
    assert provider.calls == 1
    assert result["source"] == "external_api"


def test_successful_api_clears_cooldown() -> None:
    health = ProviderHealth(cooldown_seconds=30)
    health.mark_failure(now=0.0)
    assert health.is_available(now=31.0) is True

    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    provider = _CountingProvider(
        {
            "id": "api-b2",
            "level": "beginner",
            "topic": "Routine",
            "title": "Morning",
            "exercise": "Describe your morning.",
            "source": "external_api",
        }
    )
    result = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )
    assert result["source"] == "external_api"
    assert health.is_available() is True

    provider.result = {
        "id": "api-b3",
        "level": "beginner",
        "topic": "Food",
        "title": "Lunch",
        "exercise": "Talk about lunch.",
        "source": "external_api",
    }
    again = get_next_exercise(
        "beginner",
        provider=provider,  # type: ignore[arg-type]
        source="api",
        health=health,
        cache=cache,
        request_cache=request_cache,
    )
    assert again["source"] == "external_api"
    assert health.is_available() is True


def test_cooldown_config_default() -> None:
    config = get_provider_health_config(force_reload=True)
    assert config.cooldown_seconds == 30.0
