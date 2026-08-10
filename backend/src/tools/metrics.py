"""In-memory performance metrics for Learning & Literacy tools.

Backend observability only. Never persists and never registers as a LiveKit tool.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar

logger = logging.getLogger("tools.metrics")

T = TypeVar("T")


@dataclass
class _ToolStats:
    calls: int = 0
    success: int = 0
    failures: int = 0
    total_ms: float = 0.0

    @property
    def average_ms(self) -> float:
        if self.calls <= 0:
            return 0.0
        return round(self.total_ms / self.calls, 1)


@dataclass
class ToolMetrics:
    """Collect invocation counts and average durations for learning tools."""

    _stats: dict[str, _ToolStats] = field(default_factory=dict)

    def record(self, tool_name: str, duration_ms: float, *, success: bool) -> None:
        """Record one tool execution."""
        stats = self._stats.setdefault(tool_name, _ToolStats())
        stats.calls += 1
        stats.total_ms += max(duration_ms, 0.0)
        if success:
            stats.success += 1
        else:
            stats.failures += 1
        logger.info("Tool metrics updated")

    def snapshot(self) -> dict[str, dict[str, float | int]]:
        """Return structured metrics for all tracked tools."""
        payload: dict[str, dict[str, float | int]] = {}
        for name, stats in self._stats.items():
            payload[name] = {
                "calls": stats.calls,
                "success": stats.success,
                "failures": stats.failures,
                "average_ms": stats.average_ms,
            }
        return payload

    def reset(self) -> None:
        """Clear all in-memory metrics."""
        self._stats.clear()


_default_metrics = ToolMetrics()


def get_tool_metrics() -> dict[str, dict[str, float | int]]:
    """Return current in-memory tool metrics (debug helper)."""
    return _default_metrics.snapshot()


def reset_tool_metrics() -> None:
    """Clear process-wide tool metrics (used by tests)."""
    _default_metrics.reset()


def track_tool_call(tool_name: str, fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Execute fn while recording duration and success/failure metrics."""
    started = time.perf_counter()
    success = False
    try:
        result = fn(*args, **kwargs)
        success = not (isinstance(result, dict) and result.get("error") is True)
        return result
    except Exception:
        success = False
        raise
    finally:
        duration_ms = (time.perf_counter() - started) * 1000.0
        _default_metrics.record(tool_name, duration_ms, success=success)
        rounded = int(round(duration_ms))
        label = {
            "exercise_tool": "Exercise tool completed",
            "score_tool": "Score tool completed",
            "recommendation_tool": "Recommendation tool completed",
        }.get(tool_name, f"{tool_name} completed")
        logger.info("%s (%s ms)", label, rounded)
