"""Telephony service: config, preparation, outbound placement, learning bridge."""

from __future__ import annotations

import logging
from typing import Any

from telephony.audit import CallAuditLogger
from telephony.bootstrap import ConversationBootstrap
from telephony.caller import OutboundCaller
from telephony.config import TelephonyConfig, get_telephony_config
from telephony.coordinator import OutboundConversationCoordinator
from telephony.diagnostics import TelephonyDiagnostics
from telephony.features import (
    TelephonyFeatureFlags,
    feature_disabled_response,
    get_telephony_feature_flags,
)
from telephony.livekit_client import LiveKitTelephonyClient, OutboundDialer
from telephony.metrics import TelephonyMetrics, get_telephony_metrics
from telephony.outcomes import CallOutcomeManager
from telephony.readiness import TelephonyReadinessReport
from telephony.session import OutboundLearningSession

logger = logging.getLogger("telephony.service")


class TelephonyService:
    """Load telephony configuration and prepare/place outbound calls."""

    def __init__(
        self,
        config: TelephonyConfig | None = None,
        dialer: OutboundDialer | None = None,
        bootstrap: ConversationBootstrap | None = None,
        coordinator: OutboundConversationCoordinator | None = None,
        learning_session: OutboundLearningSession | None = None,
        outcome_manager: CallOutcomeManager | None = None,
        audit_logger: CallAuditLogger | None = None,
        metrics: TelephonyMetrics | None = None,
        feature_flags: TelephonyFeatureFlags | None = None,
    ) -> None:
        self._config = config or get_telephony_config()
        self._caller = OutboundCaller(
            caller_name=self._config.outbound_caller_name,
            default_country_code=self._config.default_country_code,
        )
        self._dialer: OutboundDialer = dialer or LiveKitTelephonyClient(self._config)
        self._bootstrap = bootstrap or ConversationBootstrap()
        self._coordinator = coordinator or OutboundConversationCoordinator()
        self._learning_session = learning_session or OutboundLearningSession()
        self._outcome_manager = outcome_manager or CallOutcomeManager()
        self._features = feature_flags or get_telephony_feature_flags()
        flags = self._features.flags
        self._metrics = metrics or get_telephony_metrics()
        self._metrics.set_enabled(flags.metrics_enabled)
        self._audit = audit_logger or CallAuditLogger(enabled=flags.audit_enabled)
        self._audit.set_enabled(flags.audit_enabled)
        logger.info("Telephony service initialized")

    @property
    def config(self) -> TelephonyConfig:
        return self._config

    @property
    def metrics(self) -> TelephonyMetrics:
        return self._metrics

    @property
    def audit(self) -> CallAuditLogger:
        return self._audit

    def is_ready(self) -> bool:
        """Return True when required LiveKit telephony config is present."""
        if not self._features.flags.telephony_enabled:
            return False
        return self._config.is_valid

    def health(self) -> dict[str, Any]:
        """Return structured readiness information (no secrets)."""
        payload: dict[str, Any] = {
            "ready": self.is_ready(),
            "provider": "twilio",
            "caller_name": self._config.outbound_caller_name,
            "livekit_configured": self._config.livekit_ready,
            "twilio_configured": self._config.twilio_ready,
        }
        if self._features.flags.metrics_enabled:
            payload["metrics"] = self._metrics.snapshot()
        return payload

    def get_metrics(self) -> dict[str, Any]:
        """Return the current in-memory telephony metrics snapshot."""
        return self._metrics.snapshot()

    def run_diagnostics(self) -> dict[str, Any]:
        """Run local telephony diagnostics (no network / no outbound calls)."""
        if not self._features.flags.diagnostics_enabled:
            return feature_disabled_response()
        return TelephonyDiagnostics(
            self._config,
            self._metrics,
            service_initialized=True,
        ).run_checks()

    def generate_readiness_report(self) -> dict[str, Any]:
        """Generate an aggregated production readiness report."""
        return TelephonyReadinessReport(
            self._config,
            self._metrics,
            self._features.flags,
            service_initialized=True,
            audit_available=True,
            bootstrap_available=True,
            learning_available=True,
            evaluation_available=True,
            outcome_available=True,
        ).generate()

    def _feature_guard(self, enabled: bool) -> dict[str, Any] | None:
        if enabled:
            return None
        return feature_disabled_response()

    def prepare_call(
        self,
        phone_number: str,
        purpose: str,
        language: str = "en-IN",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Validate config + number and return prepared call metadata."""
        disabled = self._feature_guard(self._features.flags.telephony_enabled)
        if disabled is not None:
            return disabled
        if not self.is_ready():
            logger.info("Telephony configuration invalid")
            return {
                "error": True,
                "message": "Telephony configuration unavailable.",
            }
        prepared = self._caller.prepare(
            phone_number=phone_number,
            purpose=purpose,
            language=language,
            metadata=metadata,
        )
        if prepared.get("error") is not True:
            self._metrics.increment("calls_started")
            self._audit.log_event(
                "call_started",
                {
                    "purpose": prepared.get("purpose") or purpose,
                    "status": "prepared",
                    "provider": "livekit",
                },
            )
        return prepared

    def build_outbound_intro(
        self,
        learner_name: str | None,
        purpose: str,
        language: str = "en-IN",
    ) -> dict[str, Any]:
        """Build the outbound bootstrap intro (no network, no speech output)."""
        disabled = self._feature_guard(self._features.flags.bootstrap_enabled)
        if disabled is not None:
            return disabled
        if not self._features.flags.telephony_enabled or not self._config.is_valid:
            logger.info("Telephony configuration invalid")
            return {
                "error": True,
                "message": "Telephony configuration unavailable.",
            }

        logger.info("Outbound conversation initialized")
        intro = self._bootstrap.build_intro(
            learner_name=learner_name,
            purpose=purpose,
            language=language,
        )
        if intro.get("error") is not True:
            self._metrics.increment("bootstrap_generated")
            self._audit.log_event(
                "bootstrap_completed",
                {
                    "purpose": purpose,
                    "status": "ready",
                    "provider": "livekit",
                },
            )
        logger.info("Conversation handed to tutor")
        return intro

    def place_call(
        self,
        phone_number: str,
        purpose: str,
        language: str = "en-IN",
        learner_name: str | None = None,
    ) -> dict[str, Any]:
        """Prepare and place an outbound call via LiveKit telephony."""
        disabled = self._feature_guard(self._features.flags.outbound_calling_enabled)
        if disabled is not None:
            return disabled

        prepared = self.prepare_call(
            phone_number=phone_number,
            purpose=purpose,
            language=language,
        )
        if prepared.get("error"):
            logger.info("Outbound call failed")
            self._metrics.record_call_failed()
            self._audit.log_event(
                "call_failed",
                {"purpose": purpose, "status": "failed", "provider": "livekit"},
            )
            return {
                "error": True,
                "message": "Unable to place outbound call.",
            }

        uses_real_client = isinstance(self._dialer, LiveKitTelephonyClient)
        if uses_real_client and not self._config.outbound_ready:
            logger.info("Outbound call failed")
            self._metrics.record_call_failed()
            self._audit.log_event(
                "call_failed",
                {"purpose": purpose, "status": "failed", "provider": "livekit"},
            )
            return {
                "error": True,
                "message": "Unable to place outbound call.",
            }

        try:
            result = self._dialer.place_outbound_call(
                phone_number=str(prepared["phone_number"]),
                purpose=str(prepared["purpose"]),
                language=str(prepared.get("language") or language),
            )
        except Exception:
            logger.info("Outbound call failed")
            self._metrics.record_call_failed()
            self._audit.log_event(
                "call_failed",
                {"purpose": purpose, "status": "failed", "provider": "livekit"},
            )
            return {
                "error": True,
                "message": "Unable to place outbound call.",
            }

        if result.get("error"):
            self._metrics.record_call_failed()
            self._audit.log_event(
                "call_failed",
                {"purpose": purpose, "status": "failed", "provider": "livekit"},
            )
            return {
                "error": True,
                "message": "Unable to place outbound call.",
            }

        call_id = str(result.get("call_id") or "")
        if call_id:
            self._metrics.record_call_start(call_id)
        self._metrics.record_call_success()

        intro = self.build_outbound_intro(
            learner_name=learner_name,
            purpose=str(prepared["purpose"]),
            language=str(prepared.get("language") or language),
        )
        if intro.get("error") is not True:
            result = {
                **result,
                "bootstrap": intro,
            }
        self._audit.log_event(
            "call_completed",
            {
                "purpose": str(prepared["purpose"]),
                "status": result.get("status") or "calling",
                "provider": result.get("provider") or "livekit",
            },
        )
        if call_id:
            self._metrics.record_call_end(call_id)
        return result

    def start_outbound_learning(self, learner_id: str) -> dict[str, Any]:
        """Start outbound daily practice via the learning coordinator."""
        disabled = self._feature_guard(self._features.flags.learning_enabled)
        if disabled is not None:
            return disabled
        if not self._features.flags.telephony_enabled or not self._config.is_valid:
            logger.info("Telephony configuration invalid")
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }
        result = self._coordinator.start_daily_practice(learner_id)
        if result.get("status") == "ready":
            self._metrics.increment("learning_sessions_started")
            self._metrics.increment("exercises_prepared")
            self._audit.log_event(
                "learning_started",
                {"purpose": "daily_practice", "status": "ready", "provider": "livekit"},
            )
            self._audit.log_event(
                "exercise_prepared",
                {
                    "purpose": "daily_practice",
                    "status": "ready",
                    "provider": "livekit",
                },
            )
        return result

    def evaluate_outbound_session(
        self,
        learner_id: str,
        spoken_answer: str,
    ) -> dict[str, Any]:
        """Evaluate a spoken answer for an outbound learning session."""
        disabled = self._feature_guard(self._features.flags.evaluation_enabled)
        if disabled is not None:
            return disabled
        if not self._features.flags.telephony_enabled or not self._config.is_valid:
            logger.info("Telephony configuration invalid")
            return {
                "error": True,
                "message": "Unable to evaluate spoken answer.",
            }
        result = self._learning_session.evaluate_practice(
            learner_id=learner_id,
            spoken_answer=spoken_answer,
        )
        if result.get("error") is not True:
            self._metrics.increment("evaluations_completed")
            self._audit.log_event(
                "evaluation_completed",
                {"purpose": "daily_practice", "status": "scored", "provider": "livekit"},
            )
            if result.get("recommendation"):
                self._metrics.increment("recommendations_generated")
                self._audit.log_event(
                    "recommendation_generated",
                    {
                        "purpose": "daily_practice",
                        "status": str(result.get("recommendation")),
                        "provider": "livekit",
                    },
                )
            if result.get("follow_up"):
                self._metrics.increment("follow_up_exercises")
                self._audit.log_event(
                    "follow_up_prepared",
                    {
                        "purpose": "daily_practice",
                        "status": "ready",
                        "provider": "livekit",
                    },
                )
            self._metrics.record_session_completed()
        return result

    def handle_call_outcome(self, provider_status: str) -> dict[str, Any]:
        """Classify a provider call outcome into structured retry guidance."""
        result = self._outcome_manager.classify(provider_status)
        self._metrics.increment("outcomes_processed")
        self._audit.log_event(
            "outcome_processed",
            {
                "purpose": "outbound",
                "status": str(result.get("status") or provider_status),
                "provider": "livekit",
            },
        )
        if result.get("retry_recommended"):
            self._metrics.record_retry()
        return result

    def prepare_resolution_callback(
        self,
        reference_id: str,
        callback_consent: bool,
        phone_number: str,
        language: str = "en-IN",
    ) -> dict[str, Any]:
        """Delegate resolution-callback eligibility to EscalationCallbackManager."""
        from escalation.callback import EscalationCallbackManager

        return EscalationCallbackManager(telephony=self).prepare_resolution_callback(
            reference_id=reference_id,
            callback_consent=callback_consent,
            phone_number=phone_number,
            language=language,
        )


_default_service: TelephonyService | None = None


def get_telephony_service(*, force_reload: bool = False) -> TelephonyService:
    """Return a process-wide TelephonyService instance."""
    global _default_service
    if _default_service is None or force_reload:
        if force_reload:
            from telephony.config import clear_telephony_config_cache, get_telephony_config
            from telephony.features import clear_telephony_feature_flags
            from telephony.metrics import reset_telephony_metrics

            clear_telephony_config_cache()
            clear_telephony_feature_flags()
            reset_telephony_metrics()
            _default_service = TelephonyService(get_telephony_config(force_reload=True))
        else:
            _default_service = TelephonyService()
    return _default_service
