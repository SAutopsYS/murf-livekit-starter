"""Persistence ports. SQL stays in existing memory/analytics/knowledge modules."""

from __future__ import annotations

from typing import Any, Protocol

from analytics.repository import AnalyticsRepository, get_analytics_repository
from knowledge.repository import KnowledgeEntry, get_all_entries
from memory.models import User
from memory.repository import get_user_by_id, list_users


class MemoryPort(Protocol):
    def get(self, user_id: str) -> User | None: ...
    def list_consented(self) -> list[User]: ...


class AnalyticsPort(Protocol):
    def inner(self) -> AnalyticsRepository: ...


class KnowledgePort(Protocol):
    def entries(self) -> list[KnowledgeEntry]: ...


class MemoryRepositoryAdapter:
    def get(self, user_id: str) -> User | None:
        return get_user_by_id(user_id)

    def list_consented(self) -> list[User]:
        return [user for user in list_users() if user.consent]


class AnalyticsRepositoryAdapter:
    def inner(self) -> AnalyticsRepository:
        return get_analytics_repository()


class KnowledgeRepositoryAdapter:
    def entries(self) -> list[KnowledgeEntry]:
        return get_all_entries()


class InMemoryDocumentStore:
    """Studio/whiteboard documents until a real table exists. No SQL here."""

    def __init__(self) -> None:
        self._rows: dict[str, dict[str, Any]] = {}

    def put(self, key: str, value: dict[str, Any]) -> dict[str, Any]:
        self._rows[key] = value
        return value

    def get(self, key: str) -> dict[str, Any] | None:
        return self._rows.get(key)

    def list(self) -> list[dict[str, Any]]:
        return list(self._rows.values())

    def delete(self, key: str) -> None:
        self._rows.pop(key, None)

    def clear(self) -> None:
        self._rows.clear()
