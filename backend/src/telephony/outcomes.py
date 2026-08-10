"""Outbound call outcome classification and retry recommendations.

No LiveKit/Twilio SDK usage. Deterministic mapping only.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass

logger = logging.getLogger("telephony.outcomes")

_OUTCOME_MAP: dict[str, tuple[str, bool, str]] = {
    # provider_status -> (normalized, retry_recommended, next_action)
    "answered": ("answered", False, "continue_session"),
    "busy": ("busy", True, "retry_later"),
    "no_answer": ("no_answer", True, "retry_later"),
    "no-answer": ("no_answer", True, "retry_later"),
    "voicemail": ("voicemail", False, "do_not_retry"),
    "rejected": ("rejected", False, "do_not_retry"),
    "failed": ("failed", True, "retry_later"),
}


@dataclass(frozen=True)
class CallOutcome:
    """Structured outbound call outcome."""

    status: str
    completed: bool
    retry_recommended: bool
    reason: str
    next_action: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CallOutcomeManager:
    """Normalize provider call results into retry guidance."""

    def classify(self, provider_status: str) -> dict[str, object]:
        """Classify a provider status into a structured CallOutcome.

        Never raises.
        """
        if not isinstance(provider_status, str) or not provider_status.strip():
            logger.info("Call failed")
            outcome = CallOutcome(
                status="failed",
                completed=False,
                retry_recommended=True,
                reason="invalid_status",
                next_action="retry_later",
            )
            logger.info("Call outcome processed")
            logger.info("Retry recommended")
            return outcome.as_dict()

        key = provider_status.strip().lower().replace(" ", "_")
        mapped = _OUTCOME_MAP.get(key)
        if mapped is None:
            logger.info("Call failed")
            outcome = CallOutcome(
                status="failed",
                completed=False,
                retry_recommended=True,
                reason="unknown_status",
                next_action="retry_later",
            )
            logger.info("Call outcome processed")
            logger.info("Retry recommended")
            return outcome.as_dict()

        status, retry_recommended, next_action = mapped
        completed = status == "answered"
        outcome = CallOutcome(
            status=status,
            completed=completed,
            retry_recommended=retry_recommended,
            reason=status,
            next_action=next_action,
        )

        logger.info("Call outcome processed")
        if completed:
            logger.info("Call completed")
        elif retry_recommended:
            logger.info("Retry recommended")
        else:
            logger.info("Call failed")
        return outcome.as_dict()
