"""Day 5 Bonus 5: request cache and deduplication."""

from __future__ import annotations

from tools.exercise_tool import get_next_exercise
from tools.request_cache import RequestCache, get_request_cache_config
from tools.session_cache import SessionExerciseCache, reset_session_exercise_cache


def test_cache_hit_returns_same_result() -> None:
    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=60)
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
    assert first == second
    assert first.get("error") is not True


def test_cache_miss_loads_normally() -> None:
    request_cache = RequestCache(ttl_seconds=60)
    key = RequestCache.make_key("beginner", "local")
    assert request_cache.get(key) is None
    result = get_next_exercise(
        "beginner",
        source="local",
        cache=SessionExerciseCache(),
        request_cache=request_cache,
    )
    assert result.get("error") is not True
    assert request_cache.get(key) is not None


def test_ttl_expiration_reloads_exercise() -> None:
    request_cache = RequestCache(ttl_seconds=10)
    session = SessionExerciseCache()
    first = get_next_exercise(
        "beginner",
        source="local",
        cache=session,
        request_cache=request_cache,
    )
    key = RequestCache.make_key("beginner", "local")
    # Force expire.
    request_cache._entries[key].expires_at = 0
    assert request_cache.get(key, now=1.0) is None

    second = get_next_exercise(
        "beginner",
        source="local",
        cache=session,
        request_cache=request_cache,
    )
    assert first.get("error") is not True
    assert second.get("error") is not True


def test_session_reset_clears_request_cache() -> None:
    request_cache = RequestCache(ttl_seconds=60)
    get_next_exercise(
        "beginner",
        source="local",
        cache=SessionExerciseCache(),
        request_cache=request_cache,
    )
    # Global reset path used by session resets.
    reset_session_exercise_cache()
    from tools.request_cache import get_request_cache

    assert get_request_cache().get(RequestCache.make_key("beginner", "local")) is None


def test_ttl_config_default() -> None:
    assert get_request_cache_config(force_reload=True).ttl_seconds == 60.0
