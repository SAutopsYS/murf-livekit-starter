"""Typed payloads for specialist routing, context, and errors."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, TypedDict


class RouteTarget(str, Enum):
    """Deterministic routing outcomes."""

    MAIN_AGENT = "MAIN_AGENT"
    MATH_SPECIALIST = "MATH_SPECIALIST"
    UNKNOWN = "UNKNOWN"


class SpecialistError(TypedDict):
    """Structured failure payload. Never raised to the agent layer."""

    error: bool
    message: str
    code: str


class RoutingResult(TypedDict):
    """Router decision payload."""

    target: str
    specialist_id: str | None
    fallback_used: bool
    reason: str


class HandoffResult(TypedDict, total=False):
    """Main Agent → specialist handoff payload."""

    error: bool
    handed_off: bool
    specialist_id: str
    message: str
    context: dict[str, Any]
    code: str


class HandbackResult(TypedDict, total=False):
    """Specialist → Main Agent handback payload."""

    error: bool
    returned: bool
    fallback: str
    message: str
    context: dict[str, Any]
    code: str


class MathSolveResult(TypedDict, total=False):
    """Deterministic math solve payload."""

    error: bool
    topic: str
    expression: str
    steps: list[str]
    answer: str
    message: str


@dataclass
class SpecialistContext:
    """Read-only conversation context shared across tutor and specialist."""

    language: str = "en"
    learner_level: str = ""
    conversation_summary: str = ""
    current_topic: str = ""
    current_math_question: str = ""
    previous_solved_exercises: list[str] = field(default_factory=list)
    learning_history: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    solved_exercise_summary: str = ""
    memory_summary: str = ""
    memory_ref: dict[str, Any] | None = None
    active_lesson: str = ""
    learning_streak: int = 0
    completed_lessons: list[str] = field(default_factory=list)
    completion_status: str = ""
    updated_learning_level: str = ""
    learner_preferences: dict[str, Any] | None = None
    context_available: bool = True

    def as_public_dict(self) -> dict[str, Any]:
        """Return a JSON-safe copy. Memory is a snapshot, not a live handle."""
        return asdict(self)


def specialist_error(message: str, code: str) -> SpecialistError:
    """Build a structured specialist error."""
    return {"error": True, "message": message, "code": code}
