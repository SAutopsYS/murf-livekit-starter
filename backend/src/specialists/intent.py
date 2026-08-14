"""Deterministic intent detection for specialist routing.

Keyword-based. Avoids collisions with general practice, furniture tables,
and ordinary conversation. Unknown stays with the Main Agent.
"""

from __future__ import annotations

import re
from typing import Literal

IntentLabel = Literal["math", "main", "unknown"]

# Strong math phrases. Multi-word first to avoid "table" / "practice" collisions.
_MATH_PHRASES = (
    "word problem",
    "word problems",
    "mental math",
    "times table",
    "times tables",
    "multiplication table",
    "multiplication tables",
    "basic algebra",
    "basic geometry",
)

_MATH_KEYWORDS = frozenset(
    {
        "math",
        "maths",
        "mathematics",
        "arithmetic",
        "addition",
        "subtraction",
        "multiplication",
        "division",
        "multiply",
        "multiplied",
        "divide",
        "divided",
        "fraction",
        "fractions",
        "decimal",
        "decimals",
        "percent",
        "percentage",
        "percentages",
        "algebra",
        "geometry",
        "equation",
        "equations",
        "perimeter",
        "triangle",
        "triangles",
        "rectangle",
        "circle",
        "गणित",
        "जोड़",
        "घटाव",
        "गुणा",
        "भाग",
        "भिन्न",
        "प्रतिशत",
        "बीजगणित",
        "ज्यामिति",
        "पहाड़ा",
        "पहाड़े",
    }
)

_GREETING_KEYWORDS = frozenset(
    {
        "hello",
        "hi",
        "hey",
        "namaste",
        "good morning",
        "good evening",
        "good afternoon",
        "नमस्ते",
    }
)

_SCIENCE_KEYWORDS = frozenset(
    {
        "science",
        "photosynthesis",
        "gravity",
        "atom",
        "atoms",
        "chemistry",
        "biology",
        "physics",
        "planet",
        "planets",
        "molecule",
        "विज्ञान",
        "गुरुत्वाकर्षण",
        "प्रकाश संश्लेषण",
    }
)

_ENGLISH_KEYWORDS = frozenset(
    {
        "grammar",
        "vocabulary",
        "pronunciation",
        "english",
        "speaking practice",
        "verb",
        "noun",
        "adjective",
        "tense",
        "tenses",
        "व्याकरण",
        "शब्दावली",
        "अंग्रेज़ी",
        "अंग्रेजी",
    }
)

_MEMORY_KEYWORDS = frozenset(
    {
        "remember me",
        "forget me",
        "delete my",
        "what do you remember",
        "my profile",
    }
)

_ESCALATION_KEYWORDS = frozenset(
    {
        "human help",
        "human teacher",
        "talk to a teacher",
        "escalate",
        "escalation",
    }
)

_TELEPHONY_KEYWORDS = frozenset(
    {
        "call me",
        "phone call",
        "callback",
        "dial",
        "telephony",
    }
)

_ANALYTICS_KEYWORDS = frozenset(
    {
        "analytics",
        "dashboard",
        "call metrics",
        "success rate",
    }
)

_THANKS_RE = re.compile(
    r"\b(thank you|thanks|thx|धन्यवाद|शुक्रिया)\b",
    re.IGNORECASE,
)
_MATH_EXPRESSION_RE = re.compile(
    r"\d+\s*([+\-x\u00d7*\u00f7/]|of)\s*\d+",
    re.IGNORECASE,
)
_PERCENT_RE = re.compile(r"\d+\s*%")
_FRACTION_RE = re.compile(r"\d+\s*/\s*\d+")
_WORD_TOKEN_RE = re.compile(r"[\w']+|[\u0900-\u097F]+", re.UNICODE)


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _has_any(haystack: str, needles: frozenset[str] | tuple[str, ...]) -> bool:
    for needle in needles:
        if " " in needle:
            if needle in haystack:
                return True
            continue
        tokens = set(_WORD_TOKEN_RE.findall(haystack))
        if needle in tokens:
            return True
    return False


def has_math_signal(text: str) -> bool:
    """Return True when the utterance is a mathematics request."""
    if not isinstance(text, str) or not text.strip():
        return False
    lowered = _normalize(text)
    if _has_any(lowered, _MATH_PHRASES):
        return True
    if _has_any(lowered, _MATH_KEYWORDS):
        return True
    if _MATH_EXPRESSION_RE.search(text):
        return True
    return bool(_PERCENT_RE.search(text) or _FRACTION_RE.search(text))


def _is_greeting_only(text: str) -> bool:
    lowered = _normalize(text)
    if not lowered:
        return False
    if has_math_signal(text):
        return False
    stripped = re.sub(r"[^\w\s\u0900-\u097F]", "", lowered).strip()
    return stripped in _GREETING_KEYWORDS or _has_any(lowered, _GREETING_KEYWORDS)


def is_main_agent_topic(text: str) -> bool:
    """Return True for greetings, science, English, memory, and ops topics."""
    if not isinstance(text, str) or not text.strip():
        return False
    if has_math_signal(text):
        return False
    lowered = _normalize(text)
    if _is_greeting_only(text):
        return True
    return any(
        _has_any(lowered, group)
        for group in (
            _SCIENCE_KEYWORDS,
            _ENGLISH_KEYWORDS,
            _MEMORY_KEYWORDS,
            _ESCALATION_KEYWORDS,
            _TELEPHONY_KEYWORDS,
            _ANALYTICS_KEYWORDS,
        )
    )


def is_thanks(text: str) -> bool:
    """Return True when the learner is thanking the specialist."""
    return bool(isinstance(text, str) and _THANKS_RE.search(text))


def detect_intent(text: str) -> IntentLabel:
    """Classify an utterance as math, main, or unknown."""
    if not isinstance(text, str) or not text.strip():
        return "unknown"
    if has_math_signal(text):
        return "math"
    if is_main_agent_topic(text):
        return "main"
    return "unknown"


_TOPIC_ALIASES = (
    ("word problem", "word_problems"),
    ("word problems", "word_problems"),
    ("mental math", "mental_math"),
    ("times table", "tables"),
    ("multiplication", "multiplication"),
    ("multiply", "multiplication"),
    ("fraction", "fractions"),
    ("percentage", "percentages"),
    ("percent", "percentages"),
    ("division", "division"),
    ("divide", "division"),
    ("addition", "addition"),
    ("subtraction", "subtraction"),
    ("algebra", "algebra"),
    ("geometry", "geometry"),
    ("decimal", "decimals"),
    ("arithmetic", "arithmetic"),
    ("भिन्न", "fractions"),
    ("गुणा", "multiplication"),
    ("प्रतिशत", "percentages"),
)


def infer_math_topic(text: str, fallback: str = "") -> str:
    """Infer a short lesson topic from a math request."""
    if not isinstance(text, str) or not text.strip():
        return fallback
    lowered = _normalize(text)
    for needle, topic in _TOPIC_ALIASES:
        if needle in lowered:
            return topic
    if _PERCENT_RE.search(text):
        return "percentages"
    if _FRACTION_RE.search(text):
        return "fractions"
    if _MATH_EXPRESSION_RE.search(text):
        return "arithmetic"
    return fallback


def should_handoff_to_math(text: str) -> bool:
    """Main Agent should hand off only for mathematics requests."""
    return detect_intent(text) == "math"


def should_return_to_main(
    text: str,
    *,
    problem_solved: bool = False,
    practice_completed: bool = False,
) -> bool:
    """Specialist should hand back when math work is done or topic changes."""
    if problem_solved or practice_completed:
        return True
    if not isinstance(text, str) or not text.strip():
        return False
    if is_thanks(text):
        return True
    from specialists.closing import is_continue_request

    if is_continue_request(text):
        return True
    if has_math_signal(text):
        return False
    return bool(is_main_agent_topic(text))
