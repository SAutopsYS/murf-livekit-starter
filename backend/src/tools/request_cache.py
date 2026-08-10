"""In-memory request cache for identical exercise lookups.

Session-only. No LiveKit code and no prompt logic.
"""

from __future__ import annotations

import logging
import os
import time
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger("tools.request_cache")

DEFAULT_TTL_SECONDS = 60.0


@dataclass(frozen=True)
class RequestCacheConfig:
    """TTL configuration for exercise request caching."""

    ttl_seconds: float


_config_cache: RequestCacheConfig | None = None


def _read_request_cache_config() -> RequestCacheConfig:
    raw = os.getenv("EXERCISE_CACHE_TTL_SECONDS", str(DEFAULT_TTL_SECONDS))
    try:
        ttl = float(raw)
    except ValueError:
        ttl = DEFAULT_TTL_SECONDS
    if ttl < 0:
        ttl = DEFAULT_TTL_SECONDS
    return RequestCacheConfig(ttl_seconds=ttl)


def get_request_cache_config(*, force_reload: bool = False) -> RequestCacheConfig:
    """Read request-cache TTL once (cached)."""
    global _config_cache
    if _config_cache is None or force_reload:
        _config_cache = _read_request_cache_config()
    return _config_cache


def clear_request_cache_config_cache() -> None:
    """Clear cached TTL configuration (used by tests)."""
    global _config_cache
    _config_cache = None


@dataclass
class _CacheEntry:
    value: dict[str, Any]
    expires_at: float


class RequestCache:
    """Cache exercise responses keyed by request parameters."""

    def __init__(self, ttl_seconds: float | None = None) -> None:
        config = get_request_cache_config()
        self._ttl_seconds = config.ttl_seconds if ttl_seconds is None else float(ttl_seconds)
        self._entries: dict[str, _CacheEntry] = {}

    @property
    def ttl_seconds(self) -> float:
        return self._ttl_seconds

    @staticmethod
    def make_key(level: str, source: str, topic: str | None = None) -> str:
        """Build a stable cache key for an exercise request."""
        level_key = level.strip().lower()
        source_key = source.strip().lower()
        topic_key = (topic or "").strip().lower()
        if topic_key:
            return f"exercise:{level_key}:{source_key}:{topic_key}"
        return f"exercise:{level_key}:{source_key}"

    def get(self, key: str, *, now: float | None = None) -> dict[str, Any] | None:
        """Return a cached value when present and unexpired."""
        current = time.monotonic() if now is None else now
        self.clear_expired(now=current)
        entry = self._entries.get(key)
        if entry is None:
            logger.info("Exercise cache miss")
            return None
        if current >= entry.expires_at:
            self._entries.pop(key, None)
            logger.info("Cache expired")
            logger.info("Exercise cache miss")
            return None
        logger.info("Exercise cache hit")
        return deepcopy(entry.value)

    def set(self, key: str, value: dict[str, Any], *, now: float | None = None) -> None:
        """Store a successful exercise response."""
        if value.get("error") is True:
            return
        current = time.monotonic() if now is None else now
        self._entries[key] = _CacheEntry(
            value=deepcopy(value),
            expires_at=current + self._ttl_seconds,
        )
        logger.info("Exercise cached")

    def clear_expired(self, *, now: float | None = None) -> None:
        """Remove expired entries."""
        current = time.monotonic() if now is None else now
        expired = [key for key, entry in self._entries.items() if current >= entry.expires_at]
        for key in expired:
            self._entries.pop(key, None)
            logger.info("Cache expired")

    def clear(self) -> None:
        """Clear the entire request cache."""
        self._entries.clear()
        logger.info("Cache cleared")


_default_request_cache: RequestCache | None = None


def get_request_cache() -> RequestCache:
    """Return the process-wide exercise request cache."""
    global _default_request_cache
    if _default_request_cache is None:
        _default_request_cache = RequestCache()
    return _default_request_cache


def reset_request_cache() -> None:
    """Reset the process-wide request cache (used by tests/session resets)."""
    global _default_request_cache
    if _default_request_cache is None:
        _default_request_cache = RequestCache()
    else:
        _default_request_cache.clear()
