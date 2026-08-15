"""Session-only cache of served exercises.

Tracks exercise IDs by difficulty level for the current conversation.
Never writes to SQLite or persistent memory.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable

logger = logging.getLogger("tools.session_cache")


class SessionExerciseCache:
    """Remember exercises already served in the current session."""

    def __init__(self) -> None:
        self._served: dict[str, set[str]] = {}

    def served_ids(self, level: str) -> set[str]:
        """Return exercise IDs already served for a level."""
        return set(self._served.get(level, set()))

    def has_seen(self, level: str, exercise_id: str) -> bool:
        """Return True when this exercise was already served at level."""
        return exercise_id in self._served.get(level, set())

    def mark_served(self, level: str, exercise_id: str) -> None:
        """Record that an exercise was delivered for a level."""
        if not exercise_id:
            return
        bucket = self._served.setdefault(level, set())
        bucket.add(exercise_id)
        logger.info("Exercise cached")

    def unused(
        self,
        level: str,
        items: Iterable[dict[str, str]],
    ) -> list[dict[str, str]]:
        """Filter items down to those not yet served in this session."""
        seen = self._served.get(level, set())
        unused_items: list[dict[str, str]] = []
        for item in items:
            exercise_id = str(item.get("id", "")).strip()
            if not exercise_id:
                unused_items.append(item)
                continue
            if exercise_id in seen:
                logger.info("Skipping previously served exercise")
                continue
            unused_items.append(item)
        return unused_items

    def reset_level(self, level: str) -> None:
        """Clear served history for one difficulty level."""
        self._served.pop(level, None)
        logger.info("Exercise rotation restarted")

    def clear(self) -> None:
        """Clear the entire session cache."""
        self._served.clear()


_default_cache: SessionExerciseCache | None = None


def get_session_exercise_cache() -> SessionExerciseCache:
    """Return the process-wide session exercise cache."""
    global _default_cache
    if _default_cache is None:
        _default_cache = SessionExerciseCache()
    return _default_cache


def reset_session_exercise_cache() -> None:
    """Reset the process-wide session exercise cache (used by tests)."""
    global _default_cache
    if _default_cache is None:
        _default_cache = SessionExerciseCache()
    else:
        _default_cache.clear()

    # Session reset also clears short-lived request dedupe cache.
    from tools.request_cache import reset_request_cache

    reset_request_cache()
