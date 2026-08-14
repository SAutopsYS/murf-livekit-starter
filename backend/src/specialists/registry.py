"""Specialist registry with future extension points.

Only the Math Practice Specialist is active. Other tracks are placeholders.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Any

from specialists.events import log_specialist_event
from specialists.schemas import SpecialistContext

SpecialistFactory = Callable[[SpecialistContext], Any]

MATH_SPECIALIST_ID = "math_practice_specialist"

HEALTH_READY = "READY"
HEALTH_BUSY = "BUSY"
HEALTH_DISABLED = "DISABLED"
HEALTH_ERROR = "ERROR"

PLACEHOLDER_SPECIALISTS = (
    ("english_specialist", "English Specialist"),
    ("science_specialist", "Science Specialist"),
    ("reading_specialist", "Reading Specialist"),
    ("writing_specialist", "Writing Specialist"),
    ("grammar_specialist", "Grammar Specialist"),
    ("homework_specialist", "Homework Specialist"),
    ("teacher_specialist", "Teacher Assistant"),
    ("career_specialist", "Career Specialist"),
    ("motivation_specialist", "Motivation Specialist"),
)

MATH_TOPICS = (
    "arithmetic",
    "addition",
    "subtraction",
    "multiplication",
    "division",
    "fractions",
    "decimals",
    "percentages",
    "algebra",
    "geometry",
    "tables",
    "mental_math",
    "word_problems",
    "math",
)


@dataclass(frozen=True)
class SpecialistSpec:
    """Metadata for one specialist or future placeholder."""

    specialist_id: str
    name: str
    track: str
    active: bool
    factory: SpecialistFactory | None = None
    display_name: str = ""
    description: str = ""
    supported_topics: tuple[str, ...] = ()
    supported_languages: tuple[str, ...] = ("en", "hi")
    version: str = "1.0"
    enabled: bool = False
    priority: int = 100

    def as_public_dict(self) -> dict[str, Any]:
        return {
            "id": self.specialist_id,
            "specialist_id": self.specialist_id,
            "name": self.name,
            "display_name": self.display_name or self.name,
            "description": self.description,
            "track": self.track,
            "active": self.active,
            "enabled": self.enabled,
            "supported_topics": list(self.supported_topics),
            "supported_languages": list(self.supported_languages),
            "version": self.version,
            "priority": self.priority,
        }


class SpecialistRegistry:
    """Register, list, enable, disable, and look up specialists."""

    def __init__(self) -> None:
        self._specs: dict[str, SpecialistSpec] = {}
        self._health: dict[str, str] = {}

    def register(self, spec: SpecialistSpec) -> None:
        self._specs[spec.specialist_id] = spec
        self._health[spec.specialist_id] = (
            HEALTH_READY if spec.enabled and spec.active else HEALTH_DISABLED
        )
        log_specialist_event("registration")

    def unregister(self, specialist_id: str) -> bool:
        self._health.pop(specialist_id, None)
        return self._specs.pop(specialist_id, None) is not None

    def get(self, specialist_id: str) -> SpecialistSpec | None:
        return self._specs.get(specialist_id)

    def get_specialist(self, specialist_id: str) -> dict[str, Any] | None:
        spec = self._specs.get(specialist_id)
        if spec is None:
            return None
        payload = spec.as_public_dict()
        payload["health"] = self.health(specialist_id)
        return payload

    def list_specialists(
        self, *, include_placeholders: bool = False
    ) -> list[dict[str, Any]]:
        items = [
            spec for spec in self._specs.values() if include_placeholders or spec.active
        ]
        return [spec.as_public_dict() for spec in items]

    def list_active_specialists(self) -> list[dict[str, Any]]:
        return [
            spec.as_public_dict()
            for spec in self._specs.values()
            if spec.enabled and spec.active
        ]

    def list_disabled_specialists(self) -> list[dict[str, Any]]:
        return [
            spec.as_public_dict()
            for spec in self._specs.values()
            if not spec.enabled or not spec.active
        ]

    def enable(self, specialist_id: str) -> bool:
        spec = self._specs.get(specialist_id)
        if spec is None:
            return False
        self._specs[specialist_id] = replace(spec, active=True, enabled=True)
        self._health[specialist_id] = HEALTH_READY
        log_specialist_event("enable")
        return True

    def disable(self, specialist_id: str) -> bool:
        spec = self._specs.get(specialist_id)
        if spec is None:
            return False
        self._specs[specialist_id] = replace(spec, active=False, enabled=False)
        self._health[specialist_id] = HEALTH_DISABLED
        log_specialist_event("disable")
        return True

    def set_health(self, specialist_id: str, status: str) -> bool:
        if specialist_id not in self._specs:
            return False
        if status not in {HEALTH_READY, HEALTH_BUSY, HEALTH_DISABLED, HEALTH_ERROR}:
            return False
        self._health[specialist_id] = status
        log_specialist_event("health_status")
        return True

    def health(self, specialist_id: str) -> str:
        spec = self._specs.get(specialist_id)
        if spec is None:
            return HEALTH_ERROR
        return self._health.get(
            specialist_id,
            HEALTH_READY if spec.enabled else HEALTH_DISABLED,
        )

    def is_active(self, specialist_id: str) -> bool:
        spec = self._specs.get(specialist_id)
        return bool(
            spec is not None
            and spec.active
            and spec.enabled
            and spec.factory is not None
            and self.health(specialist_id) == HEALTH_READY
        )

    def supports_topic(self, specialist_id: str, topic: str) -> bool:
        spec = self._specs.get(specialist_id)
        if spec is None or not spec.supported_topics:
            return True
        return topic in spec.supported_topics or topic == "math"

    def supports_language(self, specialist_id: str, language: str) -> bool:
        spec = self._specs.get(specialist_id)
        if spec is None:
            return False
        return language in spec.supported_languages or not spec.supported_languages


def _math_factory(context: SpecialistContext) -> Any:
    from specialists.math_specialist import MathPracticeSpecialist

    return MathPracticeSpecialist(specialist_context=context)


def build_default_registry() -> SpecialistRegistry:
    """Create a registry with Math active and future specialists as placeholders."""
    registry = SpecialistRegistry()
    registry.register(
        SpecialistSpec(
            specialist_id=MATH_SPECIALIST_ID,
            name="Math Practice Specialist",
            display_name="Math Practice Specialist",
            description="Helps learners solve mathematics practice exercises.",
            track="learning_and_literacy",
            active=True,
            enabled=True,
            factory=_math_factory,
            supported_topics=MATH_TOPICS,
            supported_languages=("en", "hi"),
            version="1.0",
            priority=10,
        )
    )
    for specialist_id, name in PLACEHOLDER_SPECIALISTS:
        registry.register(
            SpecialistSpec(
                specialist_id=specialist_id,
                name=name,
                display_name=name,
                description=f"Future {name} placeholder. Not enabled.",
                track="learning_and_literacy",
                active=False,
                enabled=False,
                factory=None,
                priority=100,
            )
        )
    return registry


_default_registry: SpecialistRegistry | None = None


def get_specialist_registry() -> SpecialistRegistry:
    """Return the process-wide specialist registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = build_default_registry()
    return _default_registry


def reset_specialist_registry() -> None:
    """Reset the process-wide registry (tests)."""
    global _default_registry
    _default_registry = None


def register_specialist(spec: SpecialistSpec) -> None:
    get_specialist_registry().register(spec)


def unregister_specialist(specialist_id: str) -> bool:
    return get_specialist_registry().unregister(specialist_id)


def enable_specialist(specialist_id: str) -> bool:
    return get_specialist_registry().enable(specialist_id)


def disable_specialist(specialist_id: str) -> bool:
    return get_specialist_registry().disable(specialist_id)


def get_specialist(specialist_id: str) -> dict[str, Any] | None:
    return get_specialist_registry().get_specialist(specialist_id)


def list_specialists(*, include_placeholders: bool = False) -> list[dict[str, Any]]:
    return get_specialist_registry().list_specialists(
        include_placeholders=include_placeholders
    )


def list_active_specialists() -> list[dict[str, Any]]:
    return get_specialist_registry().list_active_specialists()


def list_disabled_specialists() -> list[dict[str, Any]]:
    return get_specialist_registry().list_disabled_specialists()


def discover_capabilities() -> dict[str, Any]:
    """Return enabled specialists only for Main Tutor capability queries."""
    active = list_active_specialists()
    return {
        "specialists": active,
        "count": len(active),
        "message": "Available specialists: "
        + ", ".join(item["display_name"] for item in active),
    }
