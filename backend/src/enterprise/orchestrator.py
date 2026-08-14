"""Enterprise orchestrator. Reuses SpecialistRouter. No duplicate routing."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from enterprise.journal import record_decision, seed_session_start
from specialists.confidence import score_routing_confidence
from specialists.intent import detect_intent, infer_math_topic
from specialists.registry import (
    MATH_SPECIALIST_ID,
    get_specialist_registry,
    list_active_specialists,
    list_specialists,
)
from specialists.router import SpecialistRouter, get_specialist_router
from specialists.schemas import RouteTarget, SpecialistContext

TUTOR_ID = "tutor"
FUTURE_PLACEHOLDERS = (
    "english_specialist",
    "science_specialist",
    "reading_specialist",
    "grammar_specialist",
    "homework_specialist",
    "teacher_specialist",
    "career_specialist",
    "motivation_specialist",
)


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _agent_label(target: str, specialist_id: str | None) -> str:
    if (
        target == RouteTarget.MATH_SPECIALIST.value
        or specialist_id == MATH_SPECIALIST_ID
    ):
        return "math_specialist"
    return TUTOR_ID


class AgentOrchestrator:
    """Choose agent, score confidence, retry/fallback via existing router."""

    def __init__(self, router: SpecialistRouter | None = None) -> None:
        self._router = router or get_specialist_router()

    def list_agents(self) -> list[dict[str, Any]]:
        registry = get_specialist_registry()
        agents = [
            {
                "id": TUTOR_ID,
                "display_name": "Main Tutor",
                "enabled": True,
                "routable": True,
            }
        ]
        for spec in list_specialists(include_placeholders=True):
            sid = spec["specialist_id"]
            agents.append(
                {
                    "id": sid,
                    "display_name": spec.get("display_name") or spec.get("name"),
                    "enabled": bool(spec.get("enabled")),
                    "routable": registry.is_active(sid),
                }
            )
        return agents

    def decide(
        self,
        text: str,
        context: SpecialistContext | None = None,
    ) -> dict[str, Any]:
        seed_session_start()
        routed = self._router.route(text, context)
        score, reason = score_routing_confidence(text, context)
        intent = detect_intent(text)
        topic = infer_math_topic(text, context.current_topic if context else "")
        selected = _agent_label(routed["target"], routed.get("specialist_id"))
        fallback = bool(routed.get("fallback_used"))
        status = "fallback" if fallback else "routed"
        if routed.get("reason") == "clarification_needed":
            status = "clarification"
        rejected = list(FUTURE_PLACEHOLDERS)
        if selected == TUTOR_ID:
            rejected = [MATH_SPECIALIST_ID, *FUTURE_PLACEHOLDERS]
        else:
            rejected = [TUTOR_ID, *FUTURE_PLACEHOLDERS]
        decision = {
            "selected_agent": selected,
            "confidence": round(float(routed.get("confidence") or score), 2),
            "reason": str(routed.get("reason") or reason),
            "alternative": TUTOR_ID if selected != TUTOR_ID else "none",
            "timestamp": _now(),
            "status": status,
            "intent": topic or intent,
            "rejected": rejected,
            "fallback": fallback,
            "routing": {
                "target": routed["target"],
                "specialist_id": routed.get("specialist_id"),
            },
        }
        record_decision(decision)
        return decision

    def capabilities(self) -> dict[str, Any]:
        return {
            "active": list_active_specialists(),
            "agents": self.list_agents(),
            "math_only": True,
        }


_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator


def reset_orchestrator() -> None:
    global _orchestrator
    _orchestrator = None
