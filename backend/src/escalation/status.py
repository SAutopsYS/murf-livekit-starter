"""Deterministic escalation status tracking and transitions."""

from __future__ import annotations

import logging
from typing import Any

from escalation.models import ALLOWED_STATUSES, EscalationStatus
from escalation.repository import EscalationRepository, get_escalation_repository

logger = logging.getLogger("escalation.status")

_ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    EscalationStatus.OPEN.value: frozenset(
        {
            EscalationStatus.IN_PROGRESS.value,
            EscalationStatus.RESOLVED.value,
        }
    ),
    EscalationStatus.IN_PROGRESS.value: frozenset(
        {
            EscalationStatus.RESOLVED.value,
        }
    ),
    EscalationStatus.RESOLVED.value: frozenset(),
}

_NEXT_ACTION: dict[str, str] = {
    EscalationStatus.OPEN.value: "await_human_review",
    EscalationStatus.IN_PROGRESS.value: "human_review_in_progress",
    EscalationStatus.RESOLVED.value: "issue_resolved",
}


def normalize_status(status: str) -> str | None:
    """Normalize a status string. Returns None when invalid."""
    if not isinstance(status, str):
        return None
    cleaned = status.strip().lower()
    if cleaned in ALLOWED_STATUSES:
        return cleaned
    return None


class EscalationStatusManager:
    """Validate and transition escalation status values."""

    def __init__(self, repository: EscalationRepository | None = None) -> None:
        self._repository = repository or get_escalation_repository()

    def get_status(self, reference_id: str) -> dict[str, Any]:
        """Return structured status for a reference ID."""
        logger.info("Escalation status requested")
        if not isinstance(reference_id, str) or not reference_id.strip():
            return {"error": True, "message": "Escalation not found."}

        request = self._repository.get(reference_id.strip())
        if request is None:
            return {"error": True, "message": "Escalation not found."}

        status = normalize_status(request.status) or EscalationStatus.OPEN.value
        return {
            "reference_id": request.reference_id,
            "status": status,
            "next_action": _NEXT_ACTION.get(status, "await_human_review"),
        }

    def update_status(self, reference_id: str, status: str) -> dict[str, Any]:
        """Apply an allowed status transition and return structured data."""
        if not isinstance(reference_id, str) or not reference_id.strip():
            logger.info("Invalid escalation transition")
            return {
                "error": True,
                "message": "Unable to update escalation status.",
            }

        target = normalize_status(status)
        if target is None:
            logger.info("Invalid escalation transition")
            return {
                "error": True,
                "message": "Unable to update escalation status.",
            }

        current = self._repository.get(reference_id.strip())
        if current is None:
            logger.info("Invalid escalation transition")
            return {
                "error": True,
                "message": "Unable to update escalation status.",
            }

        current_status = normalize_status(current.status) or EscalationStatus.OPEN.value
        if target == current_status:
            logger.info("Escalation status updated")
            return self.get_status(current.reference_id)

        allowed = _ALLOWED_TRANSITIONS.get(current_status, frozenset())
        if target not in allowed:
            logger.info("Invalid escalation transition")
            return {
                "error": True,
                "message": "Unable to update escalation status.",
            }

        updated = self._repository.update_fields(
            current.reference_id,
            status=target,
        )
        if updated is None:
            logger.info("Invalid escalation transition")
            return {
                "error": True,
                "message": "Unable to update escalation status.",
            }

        logger.info("Escalation status updated")
        if target == EscalationStatus.IN_PROGRESS.value:
            logger.info("Escalation marked in progress")
        elif target == EscalationStatus.RESOLVED.value:
            logger.info("Escalation resolved")

        return {
            "reference_id": updated.reference_id,
            "status": target,
            "next_action": _NEXT_ACTION.get(target, "await_human_review"),
        }
