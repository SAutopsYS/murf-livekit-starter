"""Informational registry for Learning & Literacy tools.

Development discovery only. Does not execute tools and is not exposed via LiveKit.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any

logger = logging.getLogger("tools.registry")


@dataclass(frozen=True)
class ToolMetadata:
    """Metadata describing one learning tool."""

    name: str
    category: str
    description: str
    version: str
    source: str
    callable: Callable[..., Any]
    capabilities: tuple[str, ...] = ()

    def as_public_dict(self) -> dict[str, Any]:
        """Return metadata without the callable object."""
        data = asdict(self)
        data.pop("callable", None)
        data["capabilities"] = list(self.capabilities)
        return data


class ToolRegistry:
    """Register and discover Learning & Literacy tool metadata."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolMetadata] = {}
        logger.info("Registry initialized")

    def register(self, metadata: ToolMetadata) -> None:
        """Register one tool's metadata."""
        self._tools[metadata.name] = metadata
        logger.info("Tool registered")

    def list_tools(self) -> list[dict[str, Any]]:
        """List public metadata for all registered tools."""
        logger.info("Tool metadata requested")
        return [item.as_public_dict() for item in self._tools.values()]

    def get_tool(self, name: str) -> dict[str, Any] | None:
        """Look up public metadata for one tool."""
        logger.info("Tool metadata requested")
        meta = self._tools.get(name)
        if meta is None:
            return None
        return meta.as_public_dict()

    def get_callable(self, name: str) -> Callable[..., Any] | None:
        """Return the registered callable for internal manager use."""
        meta = self._tools.get(name)
        return None if meta is None else meta.callable

    def list_categories(self) -> list[str]:
        """List unique tool categories."""
        return sorted({meta.category for meta in self._tools.values()})

    def list_capabilities(self) -> list[str]:
        """List unique capabilities across all tools."""
        caps: set[str] = set()
        for meta in self._tools.values():
            caps.update(meta.capabilities)
        return sorted(caps)


def build_default_registry() -> ToolRegistry:
    """Create a registry populated with the Day 5 learning tools."""
    from tools.exercise_tool import get_next_exercise
    from tools.recommendation import recommend_next_practice
    from tools.score_tool import score_spoken_answer

    registry = ToolRegistry()
    registry.register(
        ToolMetadata(
            name="get_next_exercise",
            category="exercise",
            description=(
                "Return the next speaking exercise for a learner level, "
                "with optional topic filtering and local/API sources."
            ),
            version="1.0",
            source="local/api",
            callable=get_next_exercise,
            capabilities=(
                "exercise_lookup",
                "topic_filter",
                "provider_failover",
                "session_rotation",
            ),
        )
    )
    registry.register(
        ToolMetadata(
            name="score_spoken_answer",
            category="scoring",
            description="Score a spoken answer with deterministic rule-based metrics.",
            version="1.0",
            source="rule_based",
            callable=score_spoken_answer,
            capabilities=("rule_based_scoring", "feedback"),
        )
    )
    registry.register(
        ToolMetadata(
            name="recommend_next_practice",
            category="recommendation",
            description="Recommend follow-up practice difficulty from a score.",
            version="1.0",
            source="rule_based",
            callable=recommend_next_practice,
            capabilities=("adaptive_recommendation", "follow_up_practice"),
        )
    )
    return registry


_default_registry: ToolRegistry | None = None


def get_tool_registry() -> ToolRegistry:
    """Return the process-wide learning tool registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = build_default_registry()
    return _default_registry


def list_tools() -> list[dict[str, Any]]:
    return get_tool_registry().list_tools()


def get_tool(name: str) -> dict[str, Any] | None:
    return get_tool_registry().get_tool(name)


def list_categories() -> list[str]:
    return get_tool_registry().list_categories()


def list_capabilities() -> list[str]:
    return get_tool_registry().list_capabilities()
