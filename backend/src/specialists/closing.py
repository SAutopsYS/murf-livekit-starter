"""Natural specialist closing summaries for handback."""

from __future__ import annotations

from specialists.events import log_specialist_event
from specialists.schemas import SpecialistContext
from specialists.utils import normalize_language

_TOPIC_EN = {
    "fractions": "fraction",
    "multiplication": "multiplication",
    "percentages": "percentage",
    "division": "division",
    "addition": "addition",
    "subtraction": "subtraction",
    "algebra": "algebra",
    "geometry": "geometry",
    "tables": "times-table",
    "decimals": "decimal",
    "word_problems": "word-problem",
    "mental_math": "mental-math",
    "arithmetic": "arithmetic",
    "math": "math",
}


def build_handback_summary(
    context: SpecialistContext | None, language: str = "en"
) -> str:
    """Two-sentence closing: praise, then return notice."""
    log_specialist_event("summary_created")
    topic_key = "math"
    if context is not None:
        topic_key = context.active_lesson or context.current_topic or "math"
    topic = _TOPIC_EN.get(topic_key, topic_key.replace("_", " "))
    if normalize_language(language) == "hi":
        return (
            f"बहुत बढ़िया! आपने आज का {topic} अभ्यास सही हल किया। "
            "मैं आपको मुख्य शिक्षण सहायक के पास वापस भेज रहा हूँ।"
        )
    return (
        f"Great job! You solved today's {topic} exercise correctly. "
        "I'll return you to your main learning assistant."
    )


def is_continue_request(text: str) -> bool:
    """Return True when the learner wants to leave the specialist and continue."""
    if not isinstance(text, str) or not text.strip():
        return False
    lowered = " ".join(text.strip().lower().split())
    return lowered in {
        "let's continue",
        "lets continue",
        "continue",
        "continue please",
        "let us continue",
    }
