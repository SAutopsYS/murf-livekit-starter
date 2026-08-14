"""Central specialist router. Deterministic. Never fails closed."""

from __future__ import annotations

import time
from typing import Any

from specialists.confidence import (
    CLARIFICATION_EN,
    confidence_band,
    score_routing_confidence,
)
from specialists.context import build_specialist_context
from specialists.events import log_specialist_event
from specialists.intent import detect_intent, infer_math_topic
from specialists.metrics import record_routing
from specialists.registry import (
    MATH_SPECIALIST_ID,
    SpecialistRegistry,
    get_specialist_registry,
)
from specialists.schemas import RouteTarget, RoutingResult, SpecialistContext
from specialists.utils import normalize_language


class SpecialistRouter:
    """Validate and route requests to an active specialist or the Main Agent."""

    def __init__(self, registry: SpecialistRegistry | None = None) -> None:
        self._registry = registry or get_specialist_registry()

    def validate(self, specialist_id: str) -> bool:
        """Return True when the specialist is registered, enabled, and READY."""
        return self._registry.is_active(specialist_id)

    def get_factory(self, specialist_id: str) -> Any:
        """Return the registered factory, or None."""
        spec = self._registry.get(specialist_id)
        if spec is None:
            return None
        return spec.factory

    def route(
        self,
        text: str,
        context: SpecialistContext | None = None,
    ) -> RoutingResult:
        """Decide MAIN_AGENT, MATH_SPECIALIST, or UNKNOWN (stays on Main)."""
        started = time.perf_counter()
        log_specialist_event("routing_started")
        score, reason = score_routing_confidence(text, context)
        band = confidence_band(score)
        language = normalize_language(context.language if context else "en")
        topic = infer_math_topic(text, context.current_topic if context else "")

        result: RoutingResult
        if band == "high" and self.validate(MATH_SPECIALIST_ID):
            if not self._registry.supports_language(MATH_SPECIALIST_ID, language):
                result = self._fallback("language_unsupported", score, reason)
            elif topic and not self._registry.supports_topic(MATH_SPECIALIST_ID, topic):
                result = self._fallback("topic_unsupported", score, reason)
            else:
                log_specialist_event("routing_decision")
                log_specialist_event("specialist_selected")
                result = {
                    "target": RouteTarget.MATH_SPECIALIST.value,
                    "specialist_id": MATH_SPECIALIST_ID,
                    "fallback_used": False,
                    "reason": "math_request",
                }
        elif band == "medium":
            log_specialist_event("clarification_requested")
            result = {
                "target": RouteTarget.MAIN_AGENT.value,
                "specialist_id": None,
                "fallback_used": False,
                "reason": "clarification_needed",
            }
            result["clarification"] = True  # type: ignore[typeddict-unknown-key]
            result["message"] = CLARIFICATION_EN  # type: ignore[typeddict-unknown-key]
        elif detect_intent(text) == "main":
            log_specialist_event("routing_decision")
            result = {
                "target": RouteTarget.MAIN_AGENT.value,
                "specialist_id": None,
                "fallback_used": False,
                "reason": "main_agent_topic",
            }
        elif detect_intent(text) == "math":
            result = self._fallback("math_specialist_unavailable", score, reason)
        else:
            log_specialist_event("routing_decision")
            log_specialist_event("fallback_used")
            result = {
                "target": RouteTarget.UNKNOWN.value,
                "specialist_id": None,
                "fallback_used": True,
                "reason": "unknown_stays_main",
            }

        result["confidence"] = score  # type: ignore[typeddict-unknown-key]
        result["explanation"] = f"reason={reason}; confidence={score:.2f}"  # type: ignore[typeddict-unknown-key]
        record_routing((time.perf_counter() - started) * 1000.0)
        return result

    def _fallback(self, reason: str, score: float, detail: str) -> RoutingResult:
        del score, detail
        log_specialist_event("routing_decision")
        log_specialist_event("fallback_used")
        return {
            "target": RouteTarget.MAIN_AGENT.value,
            "specialist_id": None,
            "fallback_used": True,
            "reason": reason,
        }

    def share_context(self, **fields: object) -> SpecialistContext:
        """Build transferred context using existing memory as a read-only ref."""
        allowed = {
            "language",
            "learner_level",
            "conversation_summary",
            "current_topic",
            "current_math_question",
            "previous_solved_exercises",
            "learning_history",
            "recommendations",
            "solved_exercise_summary",
            "user_id",
            "memory_profile",
            "existing",
        }
        payload = {key: value for key, value in fields.items() if key in allowed}
        return build_specialist_context(**payload)  # type: ignore[arg-type]


def get_specialist_router() -> SpecialistRouter:
    """Return a router bound to the process-wide registry."""
    return SpecialistRouter()
