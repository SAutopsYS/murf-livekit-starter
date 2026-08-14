"""Incremental learning-progress sync. Read-only memory. No full rewrites."""

from __future__ import annotations

from typing import Any

from specialists.conversation_state import ConversationState
from specialists.events import log_specialist_event
from specialists.schemas import SpecialistContext
from specialists.shared_context import sanitize_mapping
from tools.recommendation import recommend_next_practice


def build_incremental_progress(
    *,
    completed: str = "",
    score: str = "",
    recommendation: str = "",
    mastery_score: str = "",
    next_topic: str = "",
    skill_level: str = "",
) -> dict[str, str]:
    """Return only new structured progress fields."""
    payload = {
        "completed": completed,
        "score": score,
        "recommendation": recommendation,
        "mastery_score": mastery_score,
        "next_topic": next_topic,
        "skill_level": skill_level,
    }
    return {key: value for key, value in payload.items() if str(value).strip()}


def synchronize_progress(
    context: SpecialistContext,
    state: ConversationState,
    incremental: dict[str, str] | None = None,
) -> tuple[SpecialistContext, ConversationState]:
    """Merge new progress only. Does not rewrite permanent memory."""
    update = sanitize_mapping(incremental or {})
    if update.get("completed"):
        completed = str(update["completed"])
        if completed not in context.completed_lessons:
            context.completed_lessons.append(completed)
        if completed not in state.solved_exercises:
            state.solved_exercises.append(completed)
    if update.get("skill_level"):
        context.updated_learning_level = str(update["skill_level"])
        state.learner_level = str(update["skill_level"])
    if update.get("mastery_score"):
        state.mastery_score = str(update["mastery_score"])
        state.learning_progress["mastery_score"] = state.mastery_score
    if update.get("next_topic"):
        state.next_topic = str(update["next_topic"])
        state.learning_progress["next_topic"] = state.next_topic
    log_specialist_event("progress_synchronized")
    return context, state


def synchronize_recommendation(
    context: SpecialistContext,
    state: ConversationState,
    *,
    score: int | None = None,
    level: str = "",
    recommendation: str = "",
) -> tuple[SpecialistContext, ConversationState]:
    """Reuse the existing recommendation engine. Deduplicate results."""
    text = recommendation
    if not text and score is not None and level:
        try:
            result = recommend_next_practice(score, level)
        except Exception:
            log_specialist_event("synchronization_failed")
            return context, state
        if isinstance(result, dict) and result.get("error") is not True:
            text = str(result.get("reason") or result.get("recommendation") or "")
            next_level = str(result.get("next_level") or "")
            if next_level:
                context.updated_learning_level = next_level
                state.learner_level = next_level
    if text and text not in context.recommendations:
        context.recommendations.append(text)
    if text and text not in state.recommendations:
        state.recommendations.append(text)
    log_specialist_event("recommendations_synchronized")
    return context, state


def specialist_history_entry(state: ConversationState) -> list[dict[str, Any]]:
    return list(state.specialist_history)
