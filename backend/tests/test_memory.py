"""CRUD and error-handling tests for the Day 4 memory layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from memory.database import temporary_database
from memory.models import User, deserialize_string_list, serialize_string_list
from memory.repository import (
    count_users,
    create_user,
    delete_user,
    get_user_by_id,
    initialize_database,
    list_users,
    update_last_interaction,
    update_user,
    user_exists,
)


@pytest.fixture()
def memory_db(tmp_path: Path):
    db_path = tmp_path / "memory-test.db"
    with temporary_database(db_path):
        assert initialize_database() is True
        yield db_path


def test_json_list_roundtrip() -> None:
    raw = serialize_string_list(["articles", "tenses"])
    assert deserialize_string_list(raw) == ["articles", "tenses"]
    assert deserialize_string_list("not-json") == []
    assert deserialize_string_list(None) == []


def test_create_get_update_delete(memory_db: Path) -> None:
    created = create_user(
        User(
            user_id="learner-1",
            name="Saloni",
            language_preference="hinglish",
            learning_level="beginner",
            grammar_level="A1",
            speaking_confidence="low",
            common_mistakes=["articles"],
            last_topics=["greetings"],
            consent=True,
        )
    )
    assert created is not None
    assert isinstance(created, User)
    assert created.id is not None
    assert created.common_mistakes == ["articles"]
    assert created.last_topics == ["greetings"]
    assert created.consent is True

    fetched = get_user_by_id("learner-1")
    assert fetched is not None
    assert fetched.name == "Saloni"
    assert user_exists("learner-1") is True
    assert count_users() == 1

    fetched.name = "Saloni S"
    fetched.speaking_confidence = "medium"
    fetched.common_mistakes = ["articles", "prepositions"]
    updated = update_user(fetched)
    assert updated is not None
    assert updated.name == "Saloni S"
    assert updated.speaking_confidence == "medium"
    assert updated.common_mistakes == ["articles", "prepositions"]

    touched = update_last_interaction("learner-1")
    assert touched is not None
    assert touched.last_interaction is not None

    assert delete_user("learner-1") is True
    assert get_user_by_id("learner-1") is None
    assert user_exists("learner-1") is False
    assert count_users() == 0


def test_duplicate_user_id_returns_none(memory_db: Path) -> None:
    first = create_user(User(user_id="dup-1", name="One"))
    second = create_user(User(user_id="dup-1", name="Two"))
    assert first is not None
    assert second is None
    assert count_users() == 1
    remaining = get_user_by_id("dup-1")
    assert remaining is not None
    assert remaining.name == "One"


def test_missing_user_operations(memory_db: Path) -> None:
    assert get_user_by_id("missing") is None
    assert user_exists("missing") is False
    assert update_user(User(user_id="missing", name="Nope")) is None
    assert update_last_interaction("missing") is None
    assert delete_user("missing") is False


def test_list_and_count_users(memory_db: Path) -> None:
    assert list_users() == []
    assert count_users() == 0

    create_user(User(user_id="a", name="A", last_topics=["vocab"]))
    create_user(User(user_id="b", name="B", common_mistakes=["tense"]))

    users = list_users()
    assert len(users) == 2
    assert all(isinstance(user, User) for user in users)
    assert {user.user_id for user in users} == {"a", "b"}
    assert count_users() == 2
