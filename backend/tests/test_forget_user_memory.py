"""Day 4 Phase 6: Forget Me privacy tool tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent import SYSTEM_PROMPT, Assistant
from memory.database import temporary_database
from memory.repository import count_users, initialize_database
from memory.tools import (
    MEMORY_TOOLS,
    fetch_user_memory,
    forget_user_memory,
    lookup_user,
    save_user_memory,
)


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "memory-forget.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


@pytest.mark.asyncio
async def test_forget_existing_learner(memory_db: Path) -> None:
    saved = await save_user_memory(
        object(),
        user_id="forget-me-1",
        name="Saloni",
        language_preference="hinglish",
        last_topics=["grammar"],
        consent=True,
    )
    assert saved is not None
    assert count_users() == 1

    result = await forget_user_memory(object(), user_id="forget-me-1")
    assert result == {"deleted": True, "user_id": "forget-me-1"}
    assert await lookup_user(object(), user_id="forget-me-1") is None
    assert fetch_user_memory("forget-me-1") is None
    assert count_users() == 0


@pytest.mark.asyncio
async def test_forget_missing_learner(memory_db: Path) -> None:
    result = await forget_user_memory(object(), user_id="missing-learner")
    assert result == {
        "deleted": False,
        "reason": "not_found",
        "user_id": "missing-learner",
    }


@pytest.mark.asyncio
async def test_forget_persists_after_restart(tmp_path: Path) -> None:
    db_path = tmp_path / "memory-forget-restart.db"

    with temporary_database(db_path):
        assert initialize_database() is True
        saved = await save_user_memory(
            object(),
            user_id="restart-forget",
            name="Asha",
            consent=True,
        )
        assert saved is not None
        deleted = await forget_user_memory(object(), user_id="restart-forget")
        assert deleted["deleted"] is True
        assert db_path.exists()

    # Simulate backend restart against the same SQLite file.
    with temporary_database(db_path):
        assert initialize_database() is True
        assert fetch_user_memory("restart-forget") is None
        assert count_users() == 0


def test_forget_tool_registered_and_privacy_prompt() -> None:
    tool_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in MEMORY_TOOLS
    ]
    assert "forget_user_memory" in tool_names

    assistant = Assistant()
    assistant_tool_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in assistant.tools
    ]
    assert "forget_user_memory" in assistant_tool_names

    assert "PRIVACY" in SYSTEM_PROMPT
    assert "forget_user_memory" in SYSTEM_PROMPT
    assert "Forget me" in SYSTEM_PROMPT
