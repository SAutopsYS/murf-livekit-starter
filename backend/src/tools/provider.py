"""External HTTP exercise provider with safe timeouts, retries, and validation.

No LiveKit code and no prompt logic. Failures return None so callers can fall back.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger("tools.provider")

DEFAULT_TIMEOUT_SECONDS = 2.0
DEFAULT_MAX_ATTEMPTS = 2


@dataclass(frozen=True)
class ExerciseConfig:
    """Runtime configuration for exercise delivery."""

    source: str
    api_url: str
    timeout_seconds: float
    max_attempts: int


_config_cache: ExerciseConfig | None = None


def _read_exercise_config() -> ExerciseConfig:
    raw_source = os.getenv("EXERCISE_SOURCE", "local").strip().lower() or "local"
    source = raw_source if raw_source in {"local", "api"} else "local"
    api_url = os.getenv("EXERCISE_API_URL", "").strip()
    raw_timeout = os.getenv(
        "EXERCISE_API_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)
    )
    try:
        timeout_seconds = float(raw_timeout)
    except ValueError:
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS
    if timeout_seconds <= 0:
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS

    raw_attempts = os.getenv("EXERCISE_API_MAX_ATTEMPTS", str(DEFAULT_MAX_ATTEMPTS))
    try:
        max_attempts = int(raw_attempts)
    except ValueError:
        max_attempts = DEFAULT_MAX_ATTEMPTS
    if max_attempts < 1:
        max_attempts = DEFAULT_MAX_ATTEMPTS

    return ExerciseConfig(
        source=source,
        api_url=api_url,
        timeout_seconds=timeout_seconds,
        max_attempts=max_attempts,
    )


def get_exercise_config(*, force_reload: bool = False) -> ExerciseConfig:
    """Read exercise source configuration once (cached)."""
    global _config_cache
    if _config_cache is None or force_reload:
        _config_cache = _read_exercise_config()
    return _config_cache


def clear_exercise_config_cache() -> None:
    """Clear cached exercise configuration (used by tests)."""
    global _config_cache
    _config_cache = None


def _extract_payload(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        if all(key in payload for key in ("topic", "title", "exercise")):
            return payload
        nested = payload.get("data")
        if isinstance(nested, dict):
            return nested
    return None


def validate_exercise_payload(
    payload: Any,
    *,
    expected_level: str,
) -> dict[str, str] | None:
    """Validate and normalize a remote exercise payload."""
    data = _extract_payload(payload)
    if data is None:
        return None

    topic = str(data.get("topic", "")).strip()
    title = str(data.get("title", "")).strip()
    exercise = str(data.get("exercise", "")).strip()
    if not topic or not title or not exercise:
        return None

    level_raw = str(data.get("level", expected_level)).strip().lower()
    level = level_raw or expected_level
    exercise_id = str(data.get("id", "")).strip()
    if not exercise_id:
        exercise_id = f"api:{level}:{title}"

    return {
        "id": exercise_id,
        "level": level,
        "topic": topic,
        "title": title,
        "exercise": exercise,
        "source": "external_api",
    }


class ExerciseProvider:
    """Fetch one speaking exercise from an optional remote HTTP API."""

    def __init__(
        self,
        api_url: str,
        *,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> None:
        self.api_url = api_url.strip()
        self.timeout_seconds = timeout_seconds
        self.max_attempts = max(1, int(max_attempts))

    def _attempt_fetch(self, level: str) -> dict[str, str] | None:
        if not self.api_url:
            return None

        query = urlencode({"level": level})
        separator = "&" if "?" in self.api_url else "?"
        request_url = f"{self.api_url}{separator}{query}"
        request = Request(
            request_url,
            headers={"Accept": "application/json"},
            method="GET",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                status = getattr(response, "status", None) or response.getcode()
                if int(status) >= 400:
                    return None
                raw = response.read()
        except (TimeoutError, HTTPError, URLError, OSError):
            return None

        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

        return validate_exercise_payload(payload, expected_level=level)

    def fetch_exercise(self, level: str) -> dict[str, str] | None:
        """Fetch and validate one exercise for level, with automatic retries.

        Returns structured exercise data on success, otherwise None.
        Never raises to callers.
        """
        if not self.api_url:
            logger.info("Exercise provider unavailable")
            return None

        for attempt in range(1, self.max_attempts + 1):
            result = self._attempt_fetch(level)
            if result is not None:
                return result
            if attempt < self.max_attempts:
                logger.info("Exercise provider retry")

        logger.info("Exercise provider unavailable")
        return None


def build_exercise_provider(
    config: ExerciseConfig | None = None,
) -> ExerciseProvider | None:
    """Build a provider from config when API mode is enabled."""
    active = config or get_exercise_config()
    if active.source != "api":
        return None
    if not active.api_url:
        return None
    return ExerciseProvider(
        active.api_url,
        timeout_seconds=active.timeout_seconds,
        max_attempts=active.max_attempts,
    )
