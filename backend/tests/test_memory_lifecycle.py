"""Day 4 Phase 5: memory lifecycle + SQLite restart persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from memory.database import get_database_path, temporary_database
from memory.repository import (
    count_users,
    delete_user,
    get_user_by_id,
    initialize_database,
    list_users,
)
from memory.tools import (
    fetch_user_memory,
    lookup_user,
    save_user_memory,
    touch_last_interaction,
)


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "memory-lifecycle.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


@pytest.mark.asyncio
async def test_first_and_second_session_memory_lifecycle(memory_db: Path) -> None:
    user_id = "phase5-learner"

    # First session: new learner, consent required, then save.
    assert await lookup_user(object(), user_id=user_id) is None
    assert fetch_user_memory(user_id) is None

    denied = await save_user_memory(
        object(),
        user_id=user_id,
        name="Saloni",
        language_preference="hinglish",
        learning_level="beginner",
        last_topics=["grammar"],
    )
    assert denied["reason"] == "consent_required"
    assert get_user_by_id(user_id) is None

    saved = await save_user_memory(
        object(),
        user_id=user_id,
        name="Saloni",
        language_preference="hinglish",
        learning_level="beginner",
        grammar_level="A2",
        speaking_confidence="medium",
        common_mistakes=["articles"],
        last_topics=["grammar"],
        consent=True,
    )
    assert saved is not None
    assert saved["name"] == "Saloni"
    assert count_users() == 1

    touched = touch_last_interaction(user_id)
    assert touched is not None
    assert touched["last_interaction"] is not None

    # Second session: returning learner, no duplicate row.
    found = await lookup_user(object(), user_id=user_id)
    assert found is not None
    assert found["name"] == "Saloni"
    assert found["last_topics"] == ["grammar"]
    assert count_users() == 1
    assert len(list_users()) == 1


@pytest.mark.asyncio
async def test_sqlite_persists_across_restart(tmp_path: Path) -> None:
    db_path = tmp_path / "memory-restart.db"

    with temporary_database(db_path):
        assert initialize_database() is True
        assert get_database_path() == db_path

        # Simulate first backend process writing memory.
        saved = await save_user_memory(
            object(),
            user_id="restart-learner",
            name="Asha",
            language_preference="hindi",
            last_topics=["vocabulary"],
            consent=True,
        )
        assert saved is not None
        assert db_path.exists()

    # Simulate backend restart: new process opens the same SQLite file.
    with temporary_database(db_path):
        assert initialize_database() is True
        assert get_database_path() == db_path
        assert db_path.exists()

        profile = fetch_user_memory("restart-learner")
        assert profile is not None
        assert profile["name"] == "Asha"
        assert profile["last_topics"] == ["vocabulary"]
        assert count_users() == 1

        # Cleanup path still works after restart.
        assert delete_user("restart-learner") is True
        assert fetch_user_memory("restart-learner") is None


def test_prompt_and_stt_multilingual_config() -> None:
    from agent import SYSTEM_PROMPT

    assert "LANGUAGE & SCRIPT" in SYSTEM_PROMPT
    assert "Devanagari" in SYSTEM_PROMPT
    assert "Never romanize Hindi" in SYSTEM_PROMPT

    source = Path(__file__).resolve().parents[1] / "src" / "agent.py"
    text = source.read_text(encoding="utf-8")
    assert 'deepgram.STT(model="nova-3", language="multi")' in text
    assert 'voice="Anisha"' in text
    assert 'style="Conversation"' in text
    assert "text_pacing=True" in text
    assert 'locale="en-IN"' not in text
