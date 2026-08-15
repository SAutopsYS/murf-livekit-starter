"""Day 5 Phase 7: external exercise provider and local failover."""

from __future__ import annotations

import io
import json
import logging
from typing import Any
from urllib.error import HTTPError, URLError

import pytest

from tools.exercise_tool import get_next_exercise
from tools.livekit_tools import get_next_exercise as livekit_get_next_exercise
from tools.metrics import reset_tool_metrics
from tools.provider import (
    ExerciseProvider,
    clear_exercise_config_cache,
    get_exercise_config,
    validate_exercise_payload,
)
from tools.provider_health import (
    clear_provider_health_config_cache,
    reset_provider_health,
)
from tools.request_cache import clear_request_cache_config_cache, reset_request_cache
from tools.session_cache import reset_session_exercise_cache


class _FakeResponse:
    def __init__(self, payload: bytes, status: int = 200) -> None:
        self._payload = payload
        self.status = status

    def read(self) -> bytes:
        return self._payload

    def getcode(self) -> int:
        return self.status

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None


class _StubProvider:
    def __init__(self, result: dict[str, str] | None) -> None:
        self.result = result
        self.calls: list[str] = []

    def fetch_exercise(self, level: str) -> dict[str, str] | None:
        self.calls.append(level)
        return self.result


@pytest.fixture(autouse=True)
def _reset_config(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("EXERCISE_SOURCE", raising=False)
    monkeypatch.delenv("EXERCISE_API_URL", raising=False)
    monkeypatch.delenv("EXERCISE_API_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("EXERCISE_API_MAX_ATTEMPTS", raising=False)
    monkeypatch.delenv("EXERCISE_PROVIDER_COOLDOWN_SECONDS", raising=False)
    clear_exercise_config_cache()
    clear_provider_health_config_cache()
    clear_request_cache_config_cache()
    reset_provider_health()
    reset_session_exercise_cache()
    reset_request_cache()
    reset_tool_metrics()
    yield
    clear_exercise_config_cache()
    clear_provider_health_config_cache()
    clear_request_cache_config_cache()
    reset_provider_health()
    reset_session_exercise_cache()
    reset_request_cache()
    reset_tool_metrics()


def test_local_mode_default() -> None:
    config = get_exercise_config(force_reload=True)
    assert config.source == "local"
    result = get_next_exercise("beginner")
    assert result.get("error") is not True
    assert result["source"] == "local_dataset"


def test_api_success_uses_provider(caplog: pytest.LogCaptureFixture) -> None:
    from tools.request_cache import RequestCache
    from tools.session_cache import SessionExerciseCache

    provider = _StubProvider(
        {
            "id": "api-1",
            "level": "beginner",
            "topic": "API Topic",
            "title": "API Title",
            "exercise": "Say hello using the API exercise.",
            "source": "external_api",
        }
    )
    with caplog.at_level(logging.INFO, logger="tools.exercise"):
        result = get_next_exercise(
            "beginner",
            provider=provider,
            source="api",
            cache=SessionExerciseCache(),
            request_cache=RequestCache(ttl_seconds=0),
        )

    assert provider.calls == ["beginner"]
    assert result["source"] == "external_api"
    assert result["topic"] == "API Topic"
    assert "Exercise provider: API" in [r.getMessage() for r in caplog.records]
    assert "Exercise delivered" in [r.getMessage() for r in caplog.records]


def test_api_unavailable_falls_back_to_local(caplog: pytest.LogCaptureFixture) -> None:
    from tools.request_cache import RequestCache
    from tools.session_cache import SessionExerciseCache

    provider = _StubProvider(None)
    with caplog.at_level(logging.INFO):
        result = get_next_exercise(
            "intermediate",
            provider=provider,
            source="api",
            cache=SessionExerciseCache(),
            request_cache=RequestCache(ttl_seconds=0),
        )

    assert result.get("error") is not True
    assert result["source"] == "local_dataset"
    assert result["level"] == "intermediate"
    messages = [r.getMessage() for r in caplog.records]
    assert "Exercise provider unavailable" in messages
    assert "Cooldown started" in messages
    assert "Using local exercise" in messages
    assert "Exercise delivered" in messages


def test_provider_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def _timeout(*args: Any, **kwargs: Any) -> Any:
        raise TimeoutError("timed out")

    monkeypatch.setattr("tools.provider.urlopen", _timeout)
    provider = ExerciseProvider("https://example.com/exercises", timeout_seconds=0.1)
    assert provider.fetch_exercise("beginner") is None


def test_provider_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "tools.provider.urlopen",
        lambda *args, **kwargs: _FakeResponse(b"not-json"),
    )
    provider = ExerciseProvider("https://example.com/exercises")
    assert provider.fetch_exercise("beginner") is None


def test_provider_http_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def _http_error(*args: Any, **kwargs: Any) -> Any:
        raise HTTPError(
            "https://example.com/exercises",
            500,
            "server error",
            hdrs=None,
            fp=io.BytesIO(b""),
        )

    monkeypatch.setattr("tools.provider.urlopen", _http_error)
    provider = ExerciseProvider("https://example.com/exercises")
    assert provider.fetch_exercise("beginner") is None


def test_provider_unavailable_url_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def _url_error(*args: Any, **kwargs: Any) -> Any:
        raise URLError("connection refused")

    monkeypatch.setattr("tools.provider.urlopen", _url_error)
    provider = ExerciseProvider("https://example.com/exercises")
    assert provider.fetch_exercise("beginner") is None


def test_provider_malformed_exercise(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = json.dumps({"topic": "Only topic"}).encode("utf-8")
    monkeypatch.setattr(
        "tools.provider.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload),
    )
    provider = ExerciseProvider("https://example.com/exercises")
    assert provider.fetch_exercise("beginner") is None
    assert (
        validate_exercise_payload({"topic": "Only topic"}, expected_level="beginner")
        is None
    )


def test_provider_success_http(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = json.dumps(
        {
            "level": "beginner",
            "topic": "Greetings",
            "title": "Hello",
            "exercise": "Introduce yourself.",
        }
    ).encode("utf-8")
    monkeypatch.setattr(
        "tools.provider.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload),
    )
    provider = ExerciseProvider("https://example.com/exercises")
    result = provider.fetch_exercise("beginner")
    assert result is not None
    assert result["source"] == "external_api"
    assert result["title"] == "Hello"


def test_config_reads_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXERCISE_SOURCE", "api")
    monkeypatch.setenv("EXERCISE_API_URL", "https://example.com/exercises")
    clear_exercise_config_cache()
    first = get_exercise_config()
    monkeypatch.setenv("EXERCISE_SOURCE", "local")
    second = get_exercise_config()
    assert first.source == "api"
    assert second.source == "api"
    reloaded = get_exercise_config(force_reload=True)
    assert reloaded.source == "local"


@pytest.mark.asyncio
async def test_livekit_tool_unchanged_signature() -> None:
    result = await livekit_get_next_exercise(object(), level="beginner")
    assert result.get("error") is not True
    assert result["source"] == "local_dataset"
    assert {"level", "topic", "title", "exercise", "source"} <= set(result)
