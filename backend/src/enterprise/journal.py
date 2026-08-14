"""In-memory execution journal. Structured events only. No transcripts."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from enterprise.privacy import sanitize_payload

_MAX_EVENTS = 400

_EVENT_LABELS = {
    "handoff_started": "Math Specialist Joined",
    "handoff_completed": "Handoff Completed",
    "handoff_failed": "Handoff Failed",
    "handback_requested": "Handback Requested",
    "handback_completed": "Returned to Tutor",
    "handback_failed": "Handback Failed",
    "routing_started": "Routing Started",
    "routing_decision": "Routing Decision",
    "specialist_selected": "Math Specialist Selected",
    "fallback_used": "Fallback Activated",
    "context_built": "Context Built",
    "context_transferred": "Memory Retrieved",
    "context_sanitized": "Context Sanitized",
    "summary_created": "Summary Created",
    "clarification_requested": "Clarification Requested",
    "retry_attempted": "Retry Attempted",
    "recovery_triggered": "Recovery Triggered",
    "recovery_completed": "Recovery Completed",
    "handoff_requested": "Handoff Requested",
    "progress_synchronized": "Progress Synchronized",
    "recommendations_synchronized": "Recommendation Generated",
    "exercise_generated": "Exercise Generated",
    "evaluation_completed": "Answer Evaluated",
    "exercise_completed": "Exercise Completed",
    "tutor_started": "Tutor Started",
    "intent_detected": "Intent Detected",
    "knowledge_retrieved": "Knowledge Retrieved",
    "analytics_recorded": "Analytics Recorded",
}

_events: deque[dict[str, Any]] = deque(maxlen=_MAX_EVENTS)
_decisions: deque[dict[str, Any]] = deque(maxlen=_MAX_EVENTS)
_notifications: deque[dict[str, Any]] = deque(maxlen=80)


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def reset_journal() -> None:
    _events.clear()
    _decisions.clear()
    _notifications.clear()


def record_named_event(event: str, **fields: Any) -> dict[str, Any]:
    item = sanitize_payload(
        {
            "id": uuid4().hex[:12],
            "event": event,
            "label": _EVENT_LABELS.get(event, event.replace("_", " ").title()),
            "timestamp": _now(),
            "status": str(fields.get("status") or "ok"),
            "service": str(fields.get("service") or "specialists"),
            "tool": str(fields.get("tool") or ""),
            "duration_ms": fields.get("duration_ms"),
            "agent": str(fields.get("agent") or ""),
        }
    )
    _events.append(item)
    if event in {
        "handoff_completed",
        "handoff_failed",
        "handback_completed",
        "recovery_triggered",
        "exercise_completed",
    }:
        _notifications.appendleft(
            {
                "id": item["id"],
                "event": event,
                "label": item["label"],
                "timestamp": item["timestamp"],
                "unread": True,
            }
        )
    return item


def record_decision(decision: dict[str, Any]) -> dict[str, Any]:
    item = sanitize_payload(
        {
            "id": uuid4().hex[:12],
            "timestamp": decision.get("timestamp") or _now(),
            "selected_agent": decision.get("selected_agent") or "tutor",
            "confidence": float(decision.get("confidence") or 0.0),
            "reason": str(decision.get("reason") or "unknown"),
            "alternative": decision.get("alternative") or "tutor",
            "status": str(decision.get("status") or "routed"),
            "intent": str(decision.get("intent") or ""),
            "rejected": list(decision.get("rejected") or []),
            "fallback": bool(decision.get("fallback") or False),
        }
    )
    _decisions.append(item)
    record_named_event(
        "routing_decision",
        agent=item["selected_agent"],
        status=item["status"],
    )
    return item


def list_events(*, event: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    items = list(_events)
    if event:
        items = [row for row in items if row["event"] == event]
    return items[-max(1, min(limit, _MAX_EVENTS)) :]


def list_decisions(limit: int = 50) -> list[dict[str, Any]]:
    return list(_decisions)[-max(1, min(limit, _MAX_EVENTS)) :]


def list_notifications(limit: int = 20) -> list[dict[str, Any]]:
    return list(_notifications)[: max(1, min(limit, 80))]


def seed_session_start() -> None:
    if _events:
        return
    record_named_event("tutor_started", agent="tutor", service="main_tutor")
