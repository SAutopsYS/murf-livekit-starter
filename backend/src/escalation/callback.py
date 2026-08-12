"""Outbound resolution callback preparation after escalation resolution."""

from __future__ import annotations

import logging
from typing import Any, Protocol

from escalation.models import EscalationStatus
from escalation.repository import EscalationRepository, get_escalation_repository

logger = logging.getLogger("escalation.callback")

CALLBACK_PURPOSE = "escalation_resolution"
_CALLBACK_UNAVAILABLE: dict[str, Any] = {
    "error": True,
    "message": "Callback unavailable.",
}


class SupportsPrepareCall(Protocol):
    """Minimal telephony surface used for resolution callbacks."""

    def prepare_call(
        self,
        phone_number: str,
        purpose: str,
        language: str = "en-IN",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...


class EscalationCallbackManager:
    """Prepare resolution callbacks with explicit consent and telephony reuse."""

    def __init__(
        self,
        repository: EscalationRepository | None = None,
        telephony: SupportsPrepareCall | None = None,
    ) -> None:
        self._repository = repository or get_escalation_repository()
        self._telephony = telephony

    def _telephony_service(self) -> SupportsPrepareCall | None:
        if self._telephony is not None:
            return self._telephony
        try:
            from telephony.service import get_telephony_service

            return get_telephony_service()
        except Exception:
            return None

    def prepare_resolution_callback(
        self,
        reference_id: str,
        callback_consent: bool,
        phone_number: str,
        language: str = "en-IN",
    ) -> dict[str, Any]:
        """Prepare a resolution callback when all eligibility rules pass."""
        logger.info("Resolution callback requested")

        if callback_consent is not True:
            logger.info("Callback skipped")
            return dict(_CALLBACK_UNAVAILABLE)

        logger.info("Callback consent confirmed")

        if not isinstance(reference_id, str) or not reference_id.strip():
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        request = self._repository.get(reference_id.strip())
        if request is None:
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        if request.status != EscalationStatus.RESOLVED.value:
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        if request.callback_state in {"prepared", "completed"}:
            logger.info("Callback skipped")
            return dict(_CALLBACK_UNAVAILABLE)

        if not isinstance(phone_number, str) or not phone_number.strip():
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        if not isinstance(language, str) or not language.strip():
            language = "en-IN"

        telephony = self._telephony_service()
        if telephony is None:
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        try:
            prepared = telephony.prepare_call(
                phone_number=phone_number,
                purpose=CALLBACK_PURPOSE,
                language=language.strip(),
                metadata={"reference_id": request.reference_id},
            )
        except Exception:
            logger.info("Callback unavailable")
            return dict(_CALLBACK_UNAVAILABLE)

        if not isinstance(prepared, dict) or prepared.get("error") is True:
            logger.info("Callback unavailable")
            self._repository.update_fields(
                request.reference_id,
                callback_state="failed",
            )
            return dict(_CALLBACK_UNAVAILABLE)

        self._repository.update_fields(
            request.reference_id,
            callback_state="prepared",
        )
        logger.info("Callback prepared")
        logger.info("Resolution callback completed")

        return {
            "status": "prepared",
            "reference_id": request.reference_id,
            "purpose": CALLBACK_PURPOSE,
            "callback": {
                "status": "prepared",
                "language": language.strip(),
            },
        }
