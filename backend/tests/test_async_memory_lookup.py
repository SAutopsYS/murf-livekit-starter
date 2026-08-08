"""Day 4 Phase 7: background memory lookup + session cache tests."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from memory.async_lookup import SessionMemoryLookup
from memory.database import temporary_database
from memory.repository import initialize_database
from memory.tools import save_user_memory


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "memory-async.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


@pytest.mark.asyncio
async def test_background_lookup_runs_once_and_caches(memory_db: Path) -> None:
    await save_user_memory(
        object(),
        user_id="async-learner",
        name="Saloni",
        last_topics=["grammar"],
        consent=True,
    )

    lookup = SessionMemoryLookup()
    lookup.start("async-learner")
    # Duplicate start must not create another query.
    lookup.start("async-learner")

    assert lookup.is_started

    first = await lookup.get()
    assert first is not None
    assert first["name"] == "Saloni"
    assert lookup.fetch_calls == 1

    second = await lookup.get()
    assert second == first
    assert lookup.fetch_calls == 1


@pytest.mark.asyncio
async def test_background_lookup_overlaps_other_async_work(memory_db: Path) -> None:
    await save_user_memory(
        object(),
        user_id="overlap-learner",
        name="Asha",
        consent=True,
    )

    lookup = SessionMemoryLookup()
    events: list[str] = []

    async def prepare_greeting() -> None:
        events.append("prep_start")
        await asyncio.sleep(0)
        events.append("prep_done")

    lookup.start("overlap-learner")
    await prepare_greeting()
    profile = await lookup.get()

    assert profile is not None
    assert profile["name"] == "Asha"
    assert "prep_start" in events
    assert "prep_done" in events
    assert lookup.fetch_calls == 1


@pytest.mark.asyncio
async def test_failed_lookup_does_not_crash(memory_db: Path) -> None:
    lookup = SessionMemoryLookup()

    def _boom(_user_id: str) -> dict[str, Any] | None:
        raise RuntimeError("db unavailable")

    with patch("memory.async_lookup.fetch_user_memory", side_effect=_boom):
        lookup.start("broken-learner")
        profile = await lookup.get()

    assert profile is None
    # Cached failure should not retry SQLite.
    again = await lookup.get()
    assert again is None
    assert lookup.fetch_calls == 1


@pytest.mark.asyncio
async def test_new_learner_background_lookup(memory_db: Path) -> None:
    lookup = SessionMemoryLookup()
    lookup.start("brand-new-learner")
    profile = await lookup.get()
    assert profile is None
    assert lookup.fetch_calls == 1
    assert await lookup.get() is None
    assert lookup.fetch_calls == 1
