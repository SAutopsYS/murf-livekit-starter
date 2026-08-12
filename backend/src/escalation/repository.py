"""In-memory repository for human-help escalation requests."""

from __future__ import annotations

import logging
import threading
from typing import Any

from escalation.models import (
    DEFAULT_CALLBACK_STATE,
    DEFAULT_STATUS,
    DEFAULT_URGENCY,
    EscalationRequest,
    EscalationStatus,
)

logger = logging.getLogger("escalation.repository")

_ACTIVE_STATUSES: frozenset[str] = frozenset(
    {
        EscalationStatus.OPEN.value,
        EscalationStatus.IN_PROGRESS.value,
    }
)


class EscalationRepository:
    """Store escalation requests in process memory (no SQLite)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: dict[str, EscalationRequest] = {}
        self._counter = 0

    def clear(self) -> None:
        """Reset all in-memory escalations (tests / local resets)."""
        with self._lock:
            self._store.clear()
            self._counter = 0

    def _next_reference_id(self) -> str:
        self._counter += 1
        return f"ESC-{self._counter:06d}"

    def create(
        self,
        reason: str,
        summary: str,
        *,
        language: str = "en",
        urgency: str = DEFAULT_URGENCY,
        status: str = DEFAULT_STATUS,
        callback_state: str = DEFAULT_CALLBACK_STATE,
        metadata: dict[str, Any] | None = None,
    ) -> EscalationRequest:
        """Create and store a new escalation request."""
        with self._lock:
            reference_id = self._next_reference_id()
            request = EscalationRequest(
                reference_id=reference_id,
                reason=reason,
                summary=summary,
                urgency=urgency,
                language=language,
                status=status,
                callback_state=callback_state,
                metadata=dict(metadata or {}),
            )
            self._store[reference_id] = request
            logger.info("Escalation created")
            return EscalationRequest(**request.to_dict())

    def get(self, reference_id: str) -> EscalationRequest | None:
        """Retrieve an escalation by reference ID."""
        with self._lock:
            request = self._store.get(reference_id)
            if request is None:
                return None
            return EscalationRequest(**request.to_dict())

    def list_open(self) -> list[EscalationRequest]:
        """Return all escalations with status open."""
        with self._lock:
            return [
                EscalationRequest(**item.to_dict())
                for item in self._store.values()
                if item.status == EscalationStatus.OPEN.value
            ]

    def list_active(self) -> list[EscalationRequest]:
        """Return open and in_progress escalations (duplicate blocking set)."""
        with self._lock:
            return [
                EscalationRequest(**item.to_dict())
                for item in self._store.values()
                if item.status in _ACTIVE_STATUSES
            ]

    def update(self, request: EscalationRequest) -> EscalationRequest | None:
        """Replace a stored escalation. Returns None when missing."""
        with self._lock:
            if request.reference_id not in self._store:
                return None
            stored = EscalationRequest(**request.to_dict())
            self._store[request.reference_id] = stored
            return EscalationRequest(**stored.to_dict())

    def update_fields(
        self,
        reference_id: str,
        **fields: Any,
    ) -> EscalationRequest | None:
        """Update selected fields on an existing escalation."""
        with self._lock:
            current = self._store.get(reference_id)
            if current is None:
                return None
            data = current.to_dict()
            for key, value in fields.items():
                if key in data and key != "reference_id":
                    data[key] = value
            updated = EscalationRequest(**data)
            self._store[reference_id] = updated
            return EscalationRequest(**updated.to_dict())


_default_repository: EscalationRepository | None = None


def get_escalation_repository() -> EscalationRepository:
    """Return the process-wide escalation repository."""
    global _default_repository
    if _default_repository is None:
        _default_repository = EscalationRepository()
    return _default_repository


def reset_escalation_repository() -> EscalationRepository:
    """Replace the process-wide repository (used by tests)."""
    global _default_repository
    _default_repository = EscalationRepository()
    return _default_repository
