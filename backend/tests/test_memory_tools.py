"""Unit tests for Day 4 memory tool orchestration and consent."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from memory.database import temporary_database
from memory.repository import get_user_by_id, initialize_database
from memory.tools import (
    fetch_user_memory,
    lookup_user,
    save_user_memory,
    touch_last_interaction,
    update_last_interaction,
)


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "memory-tools-test.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


def _ctx() -> SimpleNamespace:
    return SimpleNamespace()


@pytest.mark.asyncio
async def test_lookup_save_and_touch_tools(memory_db: Path) -> None:
    missing = await lookup_user(_ctx(), user_id="tool-user-1")
    assert missing is None

    blocked = await save_user_memory(
        _ctx(),
        user_id="tool-user-1",
        name="Asha",
        language_preference="hinglish",
    )
    assert blocked == {
        "saved": False,
        "reason": "consent_required",
        "user_id": "tool-user-1",
    }
    assert get_user_by_id("tool-user-1") is None

    created = await save_user_memory(
        _ctx(),
        user_id="tool-user-1",
        name="Asha",
        language_preference="hinglish",
        learning_level="beginner",
        grammar_level="A1",
        speaking_confidence="low",
        common_mistakes=["articles"],
        last_topics=["greetings"],
        consent=True,
    )
    assert created is not None
    assert created["user_id"] == "tool-user-1"
    assert created["name"] == "Asha"
    assert created["consent"] is True
    assert created["common_mistakes"] == ["articles"]

    looked_up = await lookup_user(_ctx(), user_id="tool-user-1")
    assert looked_up is not None
    assert looked_up["name"] == "Asha"
    assert fetch_user_memory("tool-user-1")["name"] == "Asha"

    # Prior consent allows later updates without re-sending consent=true.
    updated = await save_user_memory(
        _ctx(),
        user_id="tool-user-1",
        speaking_confidence="medium",
        last_topics=["greetings", "shopping"],
    )
    assert updated is not None
    assert updated["name"] == "Asha"
    assert updated["speaking_confidence"] == "medium"
    assert updated["last_topics"] == ["greetings", "shopping"]

    touched = await update_last_interaction(_ctx(), user_id="tool-user-1")
    assert touched is not None
    assert touched["last_interaction"] is not None
    assert touch_last_interaction("tool-user-1") is not None

    stored = get_user_by_id("tool-user-1")
    assert stored is not None
    assert stored.last_interaction is not None


@pytest.mark.asyncio
async def test_update_last_interaction_missing_user(memory_db: Path) -> None:
    result = await update_last_interaction(_ctx(), user_id="missing-user")
    assert result is None
