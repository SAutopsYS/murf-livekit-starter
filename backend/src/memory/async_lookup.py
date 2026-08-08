"""Session-scoped background memory lookup with a one-shot cache.

Uses asyncio tasks only. Does not change repository or tool behavior.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from memory.tools import fetch_user_memory

logger = logging.getLogger("memory.async_lookup")

_UNSET: object = object()


class SessionMemoryLookup:
    """Start learner lookup once in the background and cache the result."""

    def __init__(self) -> None:
        self._user_id: str | None = None
        self._task: asyncio.Task[dict[str, Any] | None] | None = None
        self._cache: dict[str, Any] | None | object = _UNSET
        self._fetch_calls: int = 0

    @property
    def fetch_calls(self) -> int:
        """Number of underlying SQLite lookups performed (for tests)."""
        return self._fetch_calls

    @property
    def is_started(self) -> bool:
        return self._task is not None or self._cache is not _UNSET

    def start(self, user_id: str) -> None:
        """Kick off background lookup once. Safe to call repeatedly."""
        if self.is_started:
            return

        self._user_id = user_id
        logger.info("Background memory lookup started")
        self._task = asyncio.create_task(self._run(user_id))

    async def _run(self, user_id: str) -> dict[str, Any] | None:
        try:
            # Yield so greeting preparation can proceed concurrently.
            await asyncio.sleep(0)
            self._fetch_calls += 1
            profile = fetch_user_memory(user_id)
            self._cache = profile
            logger.info("Background memory lookup completed")
            return profile
        except Exception:
            logger.info("Memory lookup failed")
            self._cache = None
            return None

    async def get(self) -> dict[str, Any] | None:
        """Return cached profile, awaiting the background task if needed."""
        if self._cache is not _UNSET:
            logger.info("Memory cache hit")
            return self._cache  # type: ignore[return-value]

        if self._task is None:
            return None

        profile = await self._task
        if self._cache is _UNSET:
            self._cache = profile
        return profile
