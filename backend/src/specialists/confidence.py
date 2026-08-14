"""Deterministic routing confidence. No LLM."""

from __future__ import annotations

from specialists.intent import (
    detect_intent,
    has_math_signal,
    infer_math_topic,
    is_main_agent_topic,
)
from specialists.schemas import SpecialistContext

CLARIFICATION_EN = "Are you looking for help with a math problem?"
CLARIFICATION_HI = "क्या आपको गणित की समस्या में मदद चाहिए?"

_AMBIGUOUS = (
    "i need help",
    "need help",
    "my homework is difficult",
    "homework is difficult",
    "i don't understand this",
    "i dont understand this",
    "this is hard",
    "help me",
)


def is_ambiguous_request(text: str) -> bool:
    """Homework/help phrasing that must not auto-handoff."""
    if not isinstance(text, str) or not text.strip():
        return False
    lowered = " ".join(text.strip().lower().split())
    if has_math_signal(text):
        return False
    return any(phrase in lowered for phrase in _AMBIGUOUS)


def score_routing_confidence(
    text: str,
    context: SpecialistContext | None = None,
) -> tuple[float, str]:
    """Return (score, reason). Deterministic only."""
    if not isinstance(text, str) or not text.strip():
        return 0.15, "empty_or_unknown"
    if is_main_agent_topic(text) and not has_math_signal(text):
        return 0.08, "main_agent_topic"
    if is_ambiguous_request(text):
        return 0.55, "ambiguous_help_request"
    if has_math_signal(text):
        topic = infer_math_topic(text)
        score = 0.92 if topic and topic != "math" else 0.78
        if context is not None and (
            context.current_topic in {"fractions", "multiplication", "math"}
            or context.active_lesson
        ):
            score = min(1.0, score + 0.04)
        reason = f"{topic or 'math'}_topic" if topic else "math_keyword_detected"
        return round(score, 2), reason
    if (
        context is not None
        and context.current_topic
        and context.current_topic != "math"
        and detect_intent(text) == "unknown"
        and infer_math_topic(context.current_topic)
    ):
        return 0.58, "context_topic_followup"
    return 0.22, "unknown_stays_main"


def confidence_band(score: float) -> str:
    """low < 0.40, medium 0.40-0.69, high >= 0.70."""
    if score >= 0.70:
        return "high"
    if score >= 0.40:
        return "medium"
    return "low"
