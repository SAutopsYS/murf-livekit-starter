"""Privacy-safe specialist event logging.

Logs fixed event names only. Never logs transcripts, answers, secrets,
phone numbers, OTPs, or passwords.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("specialists.events")

_EVENT_MESSAGES = {
    "handoff_started": "Handoff started",
    "handoff_completed": "Handoff completed",
    "handoff_failed": "Handoff failed",
    "handback_requested": "Handback requested",
    "handback_completed": "Handback completed",
    "handback_failed": "Handback failed",
    "routing_started": "Routing started",
    "routing_decision": "Routing decision",
    "specialist_selected": "Specialist selected",
    "fallback_used": "Fallback used",
    "context_built": "Context built",
    "context_transferred": "Context transferred",
    "context_sanitized": "Context sanitized",
    "context_missing": "Context missing",
    "context_cleared": "Context cleared",
    "summary_created": "Summary created",
    "registration": "Registration",
    "enable": "Enable",
    "disable": "Disable",
    "health_status": "Health status",
    "clarification_requested": "Clarification requested",
    "clarification_result": "Clarification result",
    "retry_attempted": "Retry attempted",
    "recovery_triggered": "Recovery triggered",
    "recovery_completed": "Recovery completed",
    "handoff_requested": "Handoff requested",
    "context_created": "Context created",
    "context_updated": "Context updated",
    "specialist_history_updated": "Specialist history updated",
    "progress_synchronized": "Progress synchronized",
    "recommendations_synchronized": "Recommendations synchronized",
    "synchronization_failed": "Synchronization failed",
}

ALLOWED_EVENTS = frozenset(_EVENT_MESSAGES)


def log_specialist_event(event: str, **_ignored: Any) -> None:
    """Log one allow-listed event. Extra kwargs are discarded."""
    message = _EVENT_MESSAGES.get(event)
    if message is None:
        return
    logger.info(message)
    try:
        from enterprise.journal import record_named_event

        record_named_event(event)
    except Exception:
        return
