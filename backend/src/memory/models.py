"""Typed models for persistent learner memory."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


def serialize_string_list(values: list[str] | None) -> str:
    """Serialize a string list to JSON for SQLite storage."""
    return json.dumps(list(values or []), ensure_ascii=False)


def deserialize_string_list(raw: str | None) -> list[str]:
    """Deserialize a JSON list from SQLite into a typed string list."""
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [str(item) for item in data]


@dataclass
class User:
    """Learner profile for the Learning & Literacy track."""

    user_id: str
    name: str = ""
    language_preference: str = ""
    learning_level: str = ""
    grammar_level: str = ""
    speaking_confidence: str = ""
    common_mistakes: list[str] = field(default_factory=list)
    last_topics: list[str] = field(default_factory=list)
    consent: bool = False
    last_interaction: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    id: int | None = None

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> User:
        """Build a User from a SQLite row mapping. Never return raw rows."""
        return cls(
            id=int(row["id"]) if row["id"] is not None else None,
            user_id=str(row["user_id"]),
            name=str(row["name"] or ""),
            language_preference=str(row["language_preference"] or ""),
            learning_level=str(row["learning_level"] or ""),
            grammar_level=str(row["grammar_level"] or ""),
            speaking_confidence=str(row["speaking_confidence"] or ""),
            common_mistakes=deserialize_string_list(row["common_mistakes"]),
            last_topics=deserialize_string_list(row["last_topics"]),
            consent=bool(row["consent"]),
            last_interaction=row["last_interaction"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def insert_params(self, created_at: str, updated_at: str) -> tuple[Any, ...]:
        """Parameter tuple for INSERT (JSON fields serialized)."""
        return (
            self.user_id,
            self.name,
            self.language_preference,
            self.learning_level,
            self.grammar_level,
            self.speaking_confidence,
            serialize_string_list(self.common_mistakes),
            serialize_string_list(self.last_topics),
            1 if self.consent else 0,
            self.last_interaction,
            created_at,
            updated_at,
        )

    def update_params(self, updated_at: str) -> tuple[Any, ...]:
        """Parameter tuple for UPDATE (JSON fields serialized)."""
        return (
            self.name,
            self.language_preference,
            self.learning_level,
            self.grammar_level,
            self.speaking_confidence,
            serialize_string_list(self.common_mistakes),
            serialize_string_list(self.last_topics),
            1 if self.consent else 0,
            self.last_interaction,
            updated_at,
            self.user_id,
        )
