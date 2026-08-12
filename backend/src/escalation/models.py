"""Typed models for human-help escalation requests."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class EscalationUrgency(str, Enum):
    """Deterministic urgency levels for human-help requests."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class EscalationStatus(str, Enum):
    """Lifecycle statuses for human-help requests."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


ALLOWED_REASONS: frozenset[str] = frozenset(
    {
        "teacher_help",
        "learner_upset",
        "urgent_teacher_help",
        "emergency",
    }
)

ALLOWED_URGENCIES: frozenset[str] = frozenset(item.value for item in EscalationUrgency)
ALLOWED_STATUSES: frozenset[str] = frozenset(item.value for item in EscalationStatus)

URGENCY_RANK: dict[str, int] = {
    EscalationUrgency.LOW.value: 0,
    EscalationUrgency.MEDIUM.value: 1,
    EscalationUrgency.HIGH.value: 2,
    EscalationUrgency.EMERGENCY.value: 3,
}

DEFAULT_URGENCY = EscalationUrgency.MEDIUM.value
DEFAULT_STATUS = EscalationStatus.OPEN.value
DEFAULT_CALLBACK_STATE = "not_requested"

NOTIFICATION_FIELDS: tuple[str, ...] = (
    "reference_id",
    "reason",
    "summary",
    "urgency",
    "language",
    "status",
)


def determine_urgency(reason: str, context: str | None = None) -> str:
    """Return a deterministic urgency level from reason (no LLM)."""
    del context  # Reserved for future rule extensions.
    key = reason.strip().lower() if isinstance(reason, str) else ""
    mapping = {
        "teacher_help": EscalationUrgency.MEDIUM.value,
        "learner_upset": EscalationUrgency.HIGH.value,
        "urgent_teacher_help": EscalationUrgency.HIGH.value,
        "emergency": EscalationUrgency.EMERGENCY.value,
    }
    return mapping.get(key, EscalationUrgency.MEDIUM.value)


def normalize_urgency(urgency: str | None, *, reason: str = "") -> str:
    """Validate urgency or fall back to reason-based / medium default."""
    if isinstance(urgency, str):
        cleaned = urgency.strip().lower()
        if cleaned in ALLOWED_URGENCIES:
            return cleaned
    if reason:
        return determine_urgency(reason)
    return DEFAULT_URGENCY


def urgency_is_higher(candidate: str, current: str) -> bool:
    """Return True when candidate urgency ranks above current."""
    return URGENCY_RANK.get(candidate, 0) > URGENCY_RANK.get(current, 0)


@dataclass
class EscalationRequest:
    """Structured human-help escalation request (in-memory only)."""

    reference_id: str
    reason: str
    summary: str
    urgency: str = DEFAULT_URGENCY
    language: str = "en"
    status: str = DEFAULT_STATUS
    callback_state: str = DEFAULT_CALLBACK_STATE
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable escalation payload."""
        return asdict(self)

    def notification_payload(self) -> dict[str, Any]:
        """Return only fields approved for human-help notifications."""
        data = self.to_dict()
        return {key: data[key] for key in NOTIFICATION_FIELDS}
