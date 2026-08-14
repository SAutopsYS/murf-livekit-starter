"""Shared conversation context manager for specialist handoff and handback.

Reuses Memory Repository, session userdata, and existing SpecialistContext.
Does not duplicate stored rows. Specialist access is read-only.
"""

from __future__ import annotations

import re
from typing import Any

from specialists.context import (
    USERDATA_ACTIVE_AGENT_KEY,
    USERDATA_CONTEXT_KEY,
    USERDATA_RESUME_KEY,
    apply_context_to_userdata,
    build_specialist_context,
    context_from_mapping,
    merge_handback_context,
    read_context_from_userdata,
)
from specialists.events import log_specialist_event
from specialists.intent import infer_math_topic
from specialists.schemas import SpecialistContext
from specialists.utils import normalize_language

BLOCKED_KEYS = frozenset(
    {
        "transcript",
        "transcripts",
        "phone",
        "phone_number",
        "otp",
        "password",
        "api_key",
        "apikey",
        "secret",
        "authorization",
        "token",
        "user_id",
        "userid",
        "livekit_url",
    }
)

_SECRET_PHRASE_RE = re.compile(
    r"(?i)\b(otp|password|api[_-]?key|secret)\b\s*[:=]?\s*\S+"
)
_PHONE_RE = re.compile(r"(?i)\b(?:\+?\d{1,3}[-.\s])?\d{10,15}\b")

_WRITE_BLOCKED = {
    "error": True,
    "saved": False,
    "message": "Specialist memory is read-only.",
}

CONTEXT_RECOVERY_EN = "I'll continue helping with the information available."
CONTEXT_RECOVERY_HI = "मैं उपलब्ध जानकारी के साथ मदद जारी रखूँगा।"
CONTINUITY_EN = (
    "I see you're practicing {topic}. Let's continue from the last question."
)
CONTINUITY_HI = (
    "मैं देख रहा हूँ कि आप {topic} का अभ्यास कर रहे हैं। चलिए पिछले प्रश्न से जारी रखते हैं।"
)
_TOPIC_HI = {
    "fractions": "भिन्न",
    "multiplication": "गुणा",
    "percentages": "प्रतिशत",
    "division": "भाग",
    "addition": "जोड़",
    "subtraction": "घटाव",
    "algebra": "बीजगणित",
    "geometry": "ज्यामिति",
    "tables": "पहाड़ा",
    "decimals": "दशमलव",
    "word_problems": "शब्द समस्या",
    "mental_math": "मानसिक गणित",
    "arithmetic": "अंकगणित",
    "math": "गणित",
}


def _is_hindi(language: str) -> bool:
    return normalize_language(language) == "hi"


def _redact_text(value: str) -> str:
    cleaned = _SECRET_PHRASE_RE.sub("[redacted]", value)
    return _PHONE_RE.sub("[redacted]", cleaned)


def sanitize_value(value: Any) -> Any:
    """Drop secrets and learner IDs. Keep learning fields."""
    if isinstance(value, dict):
        return sanitize_mapping(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def sanitize_mapping(data: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with blocked keys removed and secret phrases redacted."""
    cleaned: dict[str, Any] = {}
    for key, value in data.items():
        if str(key).strip().lower() in BLOCKED_KEYS:
            continue
        cleaned[str(key)] = sanitize_value(value)
    return cleaned


def continuity_opening(context: SpecialistContext | None) -> str:
    """Spoken continuation. Never asks the learner to repeat prior facts."""
    if context is None or not context.context_available:
        return CONTEXT_RECOVERY_EN
    language = context.language
    topic = (
        context.active_lesson
        or context.current_topic
        or infer_math_topic(context.current_math_question, "math")
    )
    if not topic or (topic == "math" and not context.current_math_question):
        if _is_hindi(language):
            return CONTEXT_RECOVERY_HI
        return CONTEXT_RECOVERY_EN
    if _is_hindi(language):
        return CONTINUITY_HI.format(topic=_TOPIC_HI.get(topic, topic))
    label = topic.replace("_", " ")
    return CONTINUITY_EN.format(topic=label)


def recovery_notice(language: str = "en") -> str:
    """Spoken fallback when shared context cannot be loaded."""
    if _is_hindi(language):
        return CONTEXT_RECOVERY_HI
    return CONTEXT_RECOVERY_EN


_BUILD_KEYS = frozenset(
    {
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
)


class SharedContextManager:
    """Build, sanitize, transfer, validate, and clear specialist context."""

    def build(self, **fields: Any) -> SpecialistContext:
        """Build context from session fields and read-only memory."""
        known = {key: value for key, value in fields.items() if key in _BUILD_KEYS}
        try:
            context = build_specialist_context(**known)
        except Exception:
            log_specialist_event("context_missing")
            return self.recover()
        context = self._enrich(context, fields)
        context = self.sanitize(context)
        log_specialist_event("context_built")
        return context

    def sanitize(
        self, context: SpecialistContext | dict[str, Any] | None
    ) -> SpecialistContext:
        """Keep learning fields only. Never keep IDs, transcripts, or secrets."""
        raw = context_from_mapping(context)
        public = sanitize_mapping(raw.as_public_dict())
        cleaned = context_from_mapping(public)
        cleaned.context_available = raw.context_available
        log_specialist_event("context_sanitized")
        return cleaned

    def transfer(
        self,
        userdata: dict[str, Any] | None,
        context: SpecialistContext,
        *,
        active_agent: str,
        resume: bool = False,
    ) -> dict[str, Any]:
        """Write sanitized context onto existing session userdata."""
        safe = self.sanitize(context)
        store = apply_context_to_userdata(
            userdata,
            safe,
            active_agent=active_agent,
            resume=resume,
        )
        log_specialist_event("context_transferred")
        return store

    def validate(
        self, context: SpecialistContext | dict[str, Any] | None
    ) -> dict[str, Any]:
        """Validate context. Empty context is usable, never fatal."""
        if context is None:
            return {
                "valid": False,
                "usable": True,
                "missing": ["context"],
                "recovered": True,
            }
        current = context_from_mapping(context)
        missing: list[str] = []
        if not current.language:
            missing.append("language")
        if not current.learner_level:
            missing.append("learner_level")
        if not current.current_topic and not current.active_lesson:
            missing.append("topic")
        if not current.current_math_question:
            missing.append("current_math_question")
        return {
            "valid": current.context_available and not missing,
            "usable": True,
            "missing": missing,
            "recovered": not current.context_available,
        }

    def clear_temporary(self, userdata: dict[str, Any] | None) -> dict[str, Any]:
        """Clear temporary specialist context. Does not touch permanent memory."""
        store = userdata if isinstance(userdata, dict) else {}
        store.pop(USERDATA_CONTEXT_KEY, None)
        store.pop(USERDATA_RESUME_KEY, None)
        store[USERDATA_ACTIVE_AGENT_KEY] = "main"
        log_specialist_event("context_cleared")
        return store

    def load_or_recover(
        self,
        userdata: Any,
    ) -> tuple[SpecialistContext, bool]:
        """Load session context, or recover an empty usable context."""
        raw = userdata.get(USERDATA_CONTEXT_KEY) if isinstance(userdata, dict) else None
        if not isinstance(raw, dict):
            log_specialist_event("context_missing")
            return self.recover(), True
        try:
            loaded = read_context_from_userdata(userdata)
        except Exception:
            log_specialist_event("context_missing")
            return self.recover(), True
        if not loaded.context_available:
            log_specialist_event("context_missing")
            return self.sanitize(loaded), True
        return self.sanitize(loaded), False

    def recover(self, language: str = "en") -> SpecialistContext:
        """Return a safe empty context so the session can continue."""
        log_specialist_event("context_missing")
        return SpecialistContext(
            language=normalize_language(language),
            context_available=False,
        )

    def read_memory(self, user_id: str | None) -> dict[str, Any] | None:
        """Read-only learning snapshot. Never writes. Never returns learner IDs."""
        if not user_id:
            return None
        try:
            context = build_specialist_context(user_id=user_id)
        except Exception:
            return None
        snapshot = context.memory_ref or context.learner_preferences
        if not isinstance(snapshot, dict):
            return None
        return sanitize_mapping(snapshot)

    def write_memory(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        """Specialists cannot write permanent memory. Main Tutor owns writes."""
        return dict(_WRITE_BLOCKED)

    def merge_handback(
        self,
        current: SpecialistContext,
        *,
        solved_exercise_summary: str = "",
        conversation_summary: str = "",
        recommendations: list[str] | None = None,
        completion_status: str = "",
        updated_learning_level: str = "",
    ) -> SpecialistContext:
        """Transfer progress back to the Main Tutor without losing state."""
        merged = merge_handback_context(
            current,
            solved_exercise_summary=solved_exercise_summary,
            conversation_summary=conversation_summary,
            recommendations=recommendations,
        )
        completed = list(merged.completed_lessons)
        lesson = merged.active_lesson or merged.current_topic
        if completion_status == "completed" and lesson and lesson not in completed:
            completed.append(lesson)
        if solved_exercise_summary and solved_exercise_summary not in completed:
            completed.append(solved_exercise_summary)
        merged.completed_lessons = completed
        merged.completion_status = completion_status or (
            "completed" if solved_exercise_summary else merged.completion_status
        )
        merged.updated_learning_level = (
            updated_learning_level
            or merged.updated_learning_level
            or merged.learner_level
        )
        merged.learning_streak = len(merged.previous_solved_exercises)
        return self.sanitize(merged)

    def _enrich(
        self, context: SpecialistContext, fields: dict[str, Any]
    ) -> SpecialistContext:
        topic = str(fields.get("current_topic") or context.current_topic or "")
        question = context.current_math_question
        inferred = infer_math_topic(question, topic or "math")
        if not context.current_topic or context.current_topic == "math":
            context.current_topic = inferred
        context.active_lesson = str(
            fields.get("active_lesson") or context.active_lesson or inferred
        )
        if fields.get("learning_streak") not in (None, ""):
            try:
                context.learning_streak = int(fields["learning_streak"])
            except (TypeError, ValueError):
                context.learning_streak = context.learning_streak
        elif not context.learning_streak:
            context.learning_streak = len(context.previous_solved_exercises)
        extra_completed = fields.get("completed_lessons")
        if isinstance(extra_completed, list) and extra_completed:
            context.completed_lessons = [
                str(item) for item in extra_completed if str(item).strip()
            ]
        elif not context.completed_lessons:
            context.completed_lessons = list(context.learning_history)
        context.completion_status = str(
            fields.get("completion_status")
            or context.completion_status
            or "in_progress"
        )
        context.updated_learning_level = str(
            fields.get("updated_learning_level")
            or context.updated_learning_level
            or context.learner_level
        )
        prefs = context.learner_preferences or {}
        if context.memory_ref:
            prefs = {
                "language_preference": context.memory_ref.get("language_preference")
                or context.language,
                "learning_level": context.memory_ref.get("learning_level")
                or context.learner_level,
                "preferred_name": context.memory_ref.get("preferred_name") or "",
                "last_topics": list(context.memory_ref.get("last_topics") or []),
            }
        context.learner_preferences = sanitize_mapping(prefs) if prefs else None
        has_signal = bool(
            context.current_math_question
            or context.conversation_summary
            or context.learner_level
            or context.memory_ref
        )
        context.context_available = has_signal
        return context


_default_manager: SharedContextManager | None = None


def get_shared_context_manager() -> SharedContextManager:
    """Return the process-wide shared context manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = SharedContextManager()
    return _default_manager
