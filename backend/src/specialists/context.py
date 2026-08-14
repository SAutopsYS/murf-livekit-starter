"""Read-only context transfer between the Main Agent and specialists."""

from __future__ import annotations

from typing import Any

from specialists.schemas import SpecialistContext
from specialists.utils import detect_language, normalize_language
from tools.chaining import resolve_exercise_level

USERDATA_CONTEXT_KEY = "specialist_context"
USERDATA_ACTIVE_AGENT_KEY = "active_agent"
USERDATA_RESUME_KEY = "resume_from_specialist"


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _memory_snapshot(profile: dict[str, Any] | None) -> dict[str, Any] | None:
    """Copy safe learning fields only. No secrets, IDs, or contact data."""
    if not isinstance(profile, dict):
        return None
    return {
        "learning_level": str(profile.get("learning_level") or ""),
        "language_preference": str(profile.get("language_preference") or ""),
        "preferred_name": str(profile.get("name") or ""),
        "last_topics": _as_string_list(profile.get("last_topics")),
    }


def _memory_summary(snapshot: dict[str, Any] | None) -> str:
    if not snapshot:
        return ""
    topics = ", ".join(snapshot.get("last_topics") or [])
    level = snapshot.get("learning_level") or "unknown"
    language = snapshot.get("language_preference") or "unknown"
    return f"level={level}; language={language}; topics={topics or 'none'}"


def _lookup_memory(user_id: str | None) -> dict[str, Any] | None:
    if not user_id:
        return None
    from memory.tools import fetch_user_memory

    try:
        return fetch_user_memory(user_id)
    except Exception:
        return None


def build_specialist_context(
    *,
    language: str = "",
    learner_level: str = "",
    conversation_summary: str = "",
    current_topic: str = "",
    current_math_question: str = "",
    previous_solved_exercises: list[str] | None = None,
    learning_history: list[str] | None = None,
    recommendations: list[str] | None = None,
    solved_exercise_summary: str = "",
    user_id: str | None = None,
    memory_profile: dict[str, Any] | None = None,
    existing: SpecialistContext | None = None,
) -> SpecialistContext:
    """Build transferred context. Memory is a read-only snapshot."""
    profile = memory_profile
    if profile is None and user_id:
        profile = _lookup_memory(user_id)
    snapshot = _memory_snapshot(profile)

    language_value = normalize_language(language) if language else ""
    if not language_value and snapshot:
        language_value = normalize_language(
            str(snapshot.get("language_preference") or "")
        )
    if not language_value and current_math_question:
        language_value = detect_language(current_math_question)
    if not language_value:
        language_value = existing.language if existing is not None else "en"

    level_value = (learner_level or "").strip()
    if not level_value:
        resolved = resolve_exercise_level(profile)
        if resolved:
            level_value = resolved
        elif snapshot:
            level_value = str(snapshot.get("learning_level") or "")
        elif existing is not None:
            level_value = existing.learner_level

    base = existing.as_public_dict() if existing is not None else {}
    memory_ref = snapshot or (existing.memory_ref if existing is not None else None)
    preferences = None
    if memory_ref:
        preferences = {
            "language_preference": str(memory_ref.get("language_preference") or ""),
            "learning_level": str(memory_ref.get("learning_level") or ""),
            "preferred_name": str(memory_ref.get("preferred_name") or ""),
            "last_topics": _as_string_list(memory_ref.get("last_topics")),
        }
    return SpecialistContext(
        language=language_value or "en",
        learner_level=level_value,
        conversation_summary=conversation_summary
        or str(base.get("conversation_summary") or ""),
        current_topic=current_topic or str(base.get("current_topic") or ""),
        current_math_question=current_math_question
        or str(base.get("current_math_question") or ""),
        previous_solved_exercises=list(
            previous_solved_exercises or base.get("previous_solved_exercises") or []
        ),
        learning_history=list(learning_history or base.get("learning_history") or []),
        recommendations=list(recommendations or base.get("recommendations") or []),
        solved_exercise_summary=solved_exercise_summary
        or str(base.get("solved_exercise_summary") or ""),
        memory_summary=_memory_summary(snapshot)
        or str(base.get("memory_summary") or ""),
        memory_ref=memory_ref,
        active_lesson=str(base.get("active_lesson") or ""),
        learning_streak=int(base.get("learning_streak") or 0),
        completed_lessons=_as_string_list(base.get("completed_lessons")),
        completion_status=str(base.get("completion_status") or ""),
        updated_learning_level=str(base.get("updated_learning_level") or level_value),
        learner_preferences=preferences
        or (existing.learner_preferences if existing is not None else None),
        context_available=True,
    )


def merge_handback_context(
    current: SpecialistContext,
    *,
    solved_exercise_summary: str = "",
    conversation_summary: str = "",
    recommendations: list[str] | None = None,
) -> SpecialistContext:
    """Preserve progress when returning to the Main Agent."""
    previous = list(current.previous_solved_exercises)
    if solved_exercise_summary and solved_exercise_summary not in previous:
        previous.append(solved_exercise_summary)
    history = list(current.learning_history)
    if current.current_math_question and current.current_math_question not in history:
        history.append(current.current_math_question)
    return SpecialistContext(
        language=current.language,
        learner_level=current.learner_level,
        conversation_summary=conversation_summary or current.conversation_summary,
        current_topic=current.current_topic,
        current_math_question=current.current_math_question,
        previous_solved_exercises=previous,
        learning_history=history,
        recommendations=list(recommendations or current.recommendations),
        solved_exercise_summary=solved_exercise_summary
        or current.solved_exercise_summary,
        memory_summary=current.memory_summary,
        memory_ref=current.memory_ref,
        active_lesson=current.active_lesson,
        learning_streak=current.learning_streak,
        completed_lessons=list(current.completed_lessons),
        completion_status=current.completion_status,
        updated_learning_level=current.updated_learning_level or current.learner_level,
        learner_preferences=current.learner_preferences,
        context_available=current.context_available,
    )


def context_from_mapping(data: Any) -> SpecialistContext:
    """Rebuild context from userdata or a public dict."""
    if isinstance(data, SpecialistContext):
        return data
    if not isinstance(data, dict):
        return SpecialistContext()
    try:
        streak = int(data.get("learning_streak") or 0)
    except (TypeError, ValueError):
        streak = 0
    available = data.get("context_available")
    return SpecialistContext(
        language=normalize_language(str(data.get("language") or "en")),
        learner_level=str(data.get("learner_level") or ""),
        conversation_summary=str(data.get("conversation_summary") or ""),
        current_topic=str(data.get("current_topic") or ""),
        current_math_question=str(data.get("current_math_question") or ""),
        previous_solved_exercises=_as_string_list(
            data.get("previous_solved_exercises")
        ),
        learning_history=_as_string_list(data.get("learning_history")),
        recommendations=_as_string_list(data.get("recommendations")),
        solved_exercise_summary=str(data.get("solved_exercise_summary") or ""),
        memory_summary=str(data.get("memory_summary") or ""),
        memory_ref=data.get("memory_ref")
        if isinstance(data.get("memory_ref"), dict)
        else None,
        active_lesson=str(data.get("active_lesson") or ""),
        learning_streak=streak,
        completed_lessons=_as_string_list(data.get("completed_lessons")),
        completion_status=str(data.get("completion_status") or ""),
        updated_learning_level=str(data.get("updated_learning_level") or ""),
        learner_preferences=data.get("learner_preferences")
        if isinstance(data.get("learner_preferences"), dict)
        else None,
        context_available=True if available is None else bool(available),
    )


def apply_context_to_userdata(
    userdata: dict[str, Any] | None,
    context: SpecialistContext,
    *,
    active_agent: str,
    resume: bool = False,
) -> dict[str, Any]:
    """Write context onto session userdata without replacing other keys."""
    store = userdata if isinstance(userdata, dict) else {}
    store[USERDATA_CONTEXT_KEY] = context.as_public_dict()
    store[USERDATA_ACTIVE_AGENT_KEY] = active_agent
    store[USERDATA_RESUME_KEY] = resume
    return store


def read_context_from_userdata(userdata: Any) -> SpecialistContext:
    """Read transferred context from session userdata."""
    if not isinstance(userdata, dict):
        return SpecialistContext()
    return context_from_mapping(userdata.get(USERDATA_CONTEXT_KEY))
