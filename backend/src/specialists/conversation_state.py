"""Unified conversation state shared by the Main Tutor and specialists."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from specialists.events import log_specialist_event
from specialists.schemas import SpecialistContext
from specialists.shared_context import sanitize_mapping
from specialists.utils import normalize_language


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class ConversationState:
    """Structured session state. Never stores transcripts."""

    session_id: str = ""
    active_agent: str = "main"
    previous_agent: str = ""
    learner_level: str = ""
    preferred_language: str = "en"
    active_topic: str = ""
    solved_exercises: list[str] = field(default_factory=list)
    pending_exercises: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    learning_progress: dict[str, Any] = field(default_factory=dict)
    conversation_summary: str = ""
    specialist_history: list[dict[str, Any]] = field(default_factory=list)
    mastery_score: str = ""
    next_topic: str = ""

    def as_public_dict(self) -> dict[str, Any]:
        return sanitize_mapping(asdict(self))


def conversation_state_from_context(
    context: SpecialistContext,
    *,
    session_id: str = "",
    active_agent: str = "main",
    previous_agent: str = "",
    existing: ConversationState | None = None,
) -> ConversationState:
    """Build or refresh state from specialist context. No memory duplication."""
    history = list(existing.specialist_history) if existing is not None else []
    pending = list(existing.pending_exercises) if existing is not None else []
    progress = dict(existing.learning_progress) if existing is not None else {}
    state = ConversationState(
        session_id=session_id or (existing.session_id if existing else ""),
        active_agent=active_agent,
        previous_agent=previous_agent or (existing.previous_agent if existing else ""),
        learner_level=context.learner_level or context.updated_learning_level,
        preferred_language=normalize_language(context.language),
        active_topic=context.active_lesson or context.current_topic,
        solved_exercises=list(context.previous_solved_exercises),
        pending_exercises=pending,
        recommendations=list(context.recommendations),
        learning_progress=progress,
        conversation_summary=context.conversation_summary,
        specialist_history=history,
        mastery_score=str(progress.get("mastery_score") or ""),
        next_topic=str(progress.get("next_topic") or ""),
    )
    log_specialist_event("context_created")
    return state


def append_specialist_history(
    state: ConversationState,
    *,
    specialist_id: str,
    outcome: str,
    reason_for_handoff: str,
    start_time: str | None = None,
    end_time: str | None = None,
) -> ConversationState:
    """Append one lightweight specialist interaction."""
    state.specialist_history.append(
        {
            "specialist_id": specialist_id,
            "start_time": start_time or _utc_now(),
            "end_time": end_time or "",
            "outcome": outcome,
            "reason_for_handoff": reason_for_handoff,
        }
    )
    log_specialist_event("specialist_history_updated")
    return state


def validate_conversation_state(state: ConversationState | None) -> dict[str, Any]:
    """Missing fields default safely. Never crash."""
    if state is None:
        return {"valid": False, "usable": True, "missing": ["state"]}
    missing: list[str] = []
    if not state.preferred_language:
        state.preferred_language = "en"
        missing.append("preferred_language")
    if not state.active_agent:
        state.active_agent = "main"
        missing.append("active_agent")
    return {"valid": not missing, "usable": True, "missing": missing}


def apply_state_to_userdata(
    userdata: dict[str, Any] | None,
    state: ConversationState,
) -> dict[str, Any]:
    store = userdata if isinstance(userdata, dict) else {}
    store["conversation_state"] = state.as_public_dict()
    log_specialist_event("context_updated")
    return store


def read_state_from_userdata(userdata: Any) -> ConversationState:
    if not isinstance(userdata, dict):
        return ConversationState()
    raw = userdata.get("conversation_state")
    if not isinstance(raw, dict):
        return ConversationState()
    safe = sanitize_mapping(raw)
    return ConversationState(
        session_id=str(safe.get("session_id") or ""),
        active_agent=str(safe.get("active_agent") or "main"),
        previous_agent=str(safe.get("previous_agent") or ""),
        learner_level=str(safe.get("learner_level") or ""),
        preferred_language=normalize_language(
            str(safe.get("preferred_language") or "en")
        ),
        active_topic=str(safe.get("active_topic") or ""),
        solved_exercises=list(safe.get("solved_exercises") or []),
        pending_exercises=list(safe.get("pending_exercises") or []),
        recommendations=list(safe.get("recommendations") or []),
        learning_progress=dict(safe.get("learning_progress") or {}),
        conversation_summary=str(safe.get("conversation_summary") or ""),
        specialist_history=list(safe.get("specialist_history") or []),
        mastery_score=str(safe.get("mastery_score") or ""),
        next_topic=str(safe.get("next_topic") or ""),
    )
