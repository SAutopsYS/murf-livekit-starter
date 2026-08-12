"""LiveKit function tools for human-help escalation."""

from __future__ import annotations

import logging
from typing import Any

from livekit.agents import RunContext, function_tool

from escalation.callback import EscalationCallbackManager
from escalation.deduplication import EscalationDeduplicator
from escalation.models import (
    ALLOWED_REASONS,
    normalize_urgency,
    urgency_is_higher,
)
from escalation.notifier import EscalationNotifier
from escalation.repository import EscalationRepository, get_escalation_repository
from escalation.sanitizer import EscalationSanitizer
from escalation.status import EscalationStatusManager

logger = logging.getLogger("escalation.tools")

_CREATE_ERROR: dict[str, Any] = {
    "error": True,
    "message": "Unable to create human help request.",
}


def create_escalation_request(
    reason: str,
    summary: str,
    language: str = "en",
    urgency: str | None = None,
    consent: bool = False,
    *,
    repository: EscalationRepository | None = None,
    notifier: EscalationNotifier | None = None,
    deduplicator: EscalationDeduplicator | None = None,
    sanitizer: EscalationSanitizer | None = None,
) -> dict[str, Any]:
    """Create or reuse a human-help escalation. Never raises to callers."""
    del sanitizer  # Notifier owns sanitization before delivery.

    logger.info("Human help requested")

    if consent is not True:
        logger.info("Escalation consent denied")
        return dict(_CREATE_ERROR)

    logger.info("Escalation consent granted")

    if not isinstance(reason, str) or reason.strip().lower() not in ALLOWED_REASONS:
        logger.info("Escalation unavailable")
        return dict(_CREATE_ERROR)

    if not isinstance(summary, str) or not summary.strip():
        logger.info("Escalation unavailable")
        return dict(_CREATE_ERROR)

    if not isinstance(language, str) or not language.strip():
        language = "en"

    reason_key = reason.strip().lower()
    summary_text = summary.strip()
    language_key = language.strip()
    resolved_urgency = normalize_urgency(urgency, reason=reason_key)
    logger.info("Escalation urgency determined")

    repo = repository or get_escalation_repository()
    dedupe = deduplicator or EscalationDeduplicator(repo)
    notify = notifier or EscalationNotifier()

    existing = dedupe.find_duplicate(reason_key, summary_text)
    if existing is not None:
        upgraded = False
        if urgency_is_higher(resolved_urgency, existing.urgency):
            updated = repo.update_fields(
                existing.reference_id,
                urgency=resolved_urgency,
            )
            if updated is not None:
                existing = updated
                upgraded = True
                logger.info("Escalation urgency upgraded")

        if upgraded:
            notify_result = notify.send(existing.notification_payload())
            notification = str(notify_result.get("notification") or "unavailable")
        else:
            logger.info("Duplicate notification skipped")
            notification = "already_sent"

        return {
            "reference_id": existing.reference_id,
            "status": existing.status,
            "reason": existing.reason,
            "urgency": existing.urgency,
            "duplicate": True,
            "notification": notification,
            "message": "Human help request already open.",
        }

    created = repo.create(
        reason=reason_key,
        summary=summary_text,
        language=language_key,
        urgency=resolved_urgency,
    )
    logger.info("New escalation created")
    logger.info("Escalation created")

    notify_result = notify.send(created.notification_payload())
    notification = str(notify_result.get("notification") or "unavailable")

    return {
        "reference_id": created.reference_id,
        "status": created.status,
        "reason": created.reason,
        "urgency": created.urgency,
        "duplicate": False,
        "notification": notification,
        "message": "Human help request created.",
    }


def get_escalation_status_data(
    reference_id: str,
    *,
    repository: EscalationRepository | None = None,
) -> dict[str, Any]:
    """Return structured escalation status for a reference ID."""
    manager = EscalationStatusManager(repository or get_escalation_repository())
    return manager.get_status(reference_id)


def update_escalation_status_data(
    reference_id: str,
    status: str,
    *,
    repository: EscalationRepository | None = None,
) -> dict[str, Any]:
    """Update escalation status through the status manager."""
    manager = EscalationStatusManager(repository or get_escalation_repository())
    return manager.update_status(reference_id, status)


def prepare_resolution_callback_data(
    reference_id: str,
    callback_consent: bool,
    phone_number: str,
    language: str = "en-IN",
    *,
    repository: EscalationRepository | None = None,
    telephony: Any | None = None,
) -> dict[str, Any]:
    """Prepare a resolution callback using EscalationCallbackManager."""
    manager = EscalationCallbackManager(
        repository=repository or get_escalation_repository(),
        telephony=telephony,
    )
    return manager.prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=callback_consent,
        phone_number=phone_number,
        language=language,
    )


@function_tool()
async def create_escalation(
    context: RunContext,
    reason: str,
    summary: str,
    language: str = "en",
    urgency: str | None = None,
    consent: bool = False,
) -> dict[str, Any]:
    """Create a human-help escalation after learner consent.

    Call only when the learner is clearly upset and asks for a human, or
    explicitly requests a teacher, and has granted permission to share a short
    summary. Returns structured data only.

    Args:
        reason: One of teacher_help, learner_upset, urgent_teacher_help, emergency.
        summary: Short safe summary of the issue, what was tried, and why help is needed.
        language: Learner language code (for example en or hi).
        urgency: Optional urgency override: low, medium, high, or emergency.
        consent: Must be true only after the learner clearly agrees to share a summary.
    """
    del context
    return create_escalation_request(
        reason=reason,
        summary=summary,
        language=language,
        urgency=urgency,
        consent=consent,
    )


@function_tool()
async def get_escalation_status(
    context: RunContext,
    reference_id: str,
) -> dict[str, Any]:
    """Look up the status of an existing human-help request by reference ID.

    Returns structured status data. Does not generate spoken text.

    Args:
        reference_id: Escalation reference such as ESC-000001.
    """
    del context
    return get_escalation_status_data(reference_id)


@function_tool()
async def prepare_resolution_callback(
    context: RunContext,
    reference_id: str,
    callback_consent: bool,
    phone_number: str,
    language: str = "en-IN",
) -> dict[str, Any]:
    """Prepare an outbound callback after a resolved human-help request.

    Requires explicit callback consent. Does not place a call automatically.
    Never returns the phone number.

    Args:
        reference_id: Resolved escalation reference ID.
        callback_consent: True only when the learner clearly agrees to a callback.
        phone_number: Callback destination in a valid phone format.
        language: Callback language (default en-IN).
    """
    del context
    return prepare_resolution_callback_data(
        reference_id=reference_id,
        callback_consent=callback_consent,
        phone_number=phone_number,
        language=language,
    )


ESCALATION_TOOLS = [
    create_escalation,
    get_escalation_status,
    prepare_resolution_callback,
]

__all__ = [
    "ESCALATION_TOOLS",
    "create_escalation",
    "create_escalation_request",
    "get_escalation_status",
    "get_escalation_status_data",
    "prepare_resolution_callback",
    "prepare_resolution_callback_data",
    "update_escalation_status_data",
]
