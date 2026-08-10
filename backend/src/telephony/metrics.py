"""In-memory telephony operational metrics.

Development/testing observability only. Never persists. No networking.
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from typing import Any

logger = logging.getLogger("telephony.metrics")

_KNOWN_COUNTERS: frozenset[str] = frozenset(
    {
        "calls_started",
        "calls_completed",
        "calls_failed",
        "bootstrap_generated",
        "learning_sessions_started",
        "exercises_prepared",
        "evaluations_completed",
        "recommendations_generated",
        "follow_up_exercises",
        "outcomes_processed",
        "retry_recommended",
        "completed_sessions",
    }
)


@dataclass
class TelephonyStats:
    """Lifecycle counters for outbound telephony operations."""

    calls_started: int = 0
    calls_completed: int = 0
    calls_failed: int = 0
    bootstrap_generated: int = 0
    learning_sessions_started: int = 0
    exercises_prepared: int = 0
    evaluations_completed: int = 0
    recommendations_generated: int = 0
    follow_up_exercises: int = 0
    outcomes_processed: int = 0
    retry_recommended: int = 0
    completed_sessions: int = 0


@dataclass
class TelephonyMetrics:
    """Collect in-memory telephony counters and optional call durations."""

    _stats: TelephonyStats = field(default_factory=TelephonyStats)
    _call_starts: dict[str, float] = field(default_factory=dict)
    _duration_total: float = 0.0
    _duration_samples: int = 0
    _enabled: bool = True

    def __post_init__(self) -> None:
        logger.info("Telephony metrics initialized")
        logger.info("Metrics initialized")

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def increment(self, metric: str) -> None:
        """Increment a known counter. Unknown metrics are ignored."""
        if not self._enabled:
            return
        name = (metric or "").strip()
        if name not in _KNOWN_COUNTERS:
            return
        current = getattr(self._stats, name)
        setattr(self._stats, name, int(current) + 1)
        logger.info("Metric incremented")
        logger.info("Telephony metrics updated")
        logger.info("Call metrics updated")

    def record_call_start(self, call_id: str) -> None:
        """Mark a call start timestamp for duration tracking (no counter bump)."""
        if not self._enabled:
            return
        cid = (call_id or "").strip()
        if not cid:
            return
        # Keep the earliest start if called twice; ignore duplicates.
        self._call_starts.setdefault(cid, time.monotonic())

    def record_call_end(self, call_id: str) -> None:
        """Record call end duration. Duplicate ends are ignored."""
        if not self._enabled:
            return
        cid = (call_id or "").strip()
        if not cid:
            return
        started = self._call_starts.pop(cid, None)
        if started is None:
            return
        elapsed = max(time.monotonic() - started, 0.0)
        self._duration_total += elapsed
        self._duration_samples += 1

    def record_call_started(self) -> None:
        """Increment outbound attempt counter."""
        self.increment("calls_started")

    def record_call_success(self) -> None:
        """Increment successful / completed call counter."""
        self.increment("calls_completed")

    def record_call_failed(self) -> None:
        """Increment failed call counter."""
        self.increment("calls_failed")

    def record_retry(self) -> None:
        """Increment retry-recommended counter."""
        self.increment("retry_recommended")

    def record_session_completed(self) -> None:
        """Increment completed learning session counter."""
        self.increment("completed_sessions")
        logger.info("Learning session completed")

    def snapshot(self) -> dict[str, Any]:
        """Return a structured metrics snapshot (safe for health/debug)."""
        logger.info("Metrics snapshot requested")
        logger.info("Metrics snapshot generated")
        base = asdict(self._stats)
        avg = 0.0
        if self._duration_samples > 0:
            avg = round(self._duration_total / self._duration_samples, 1)
        base["average_call_duration_seconds"] = avg
        # Compatibility aliases for Bonus 3 observability docs/tests.
        base["total_calls"] = self._stats.calls_started
        base["successful_calls"] = self._stats.calls_completed
        base["failed_calls"] = self._stats.calls_failed
        base["outbound_attempts"] = self._stats.calls_started
        base["outbound_success"] = self._stats.calls_completed
        base["outbound_failed"] = self._stats.calls_failed
        base["bootstrap_started"] = self._stats.bootstrap_generated
        base["learning_sessions"] = self._stats.learning_sessions_started
        base["evaluations"] = self._stats.evaluations_completed
        return base

    def reset(self) -> None:
        """Clear all in-memory counters and duration state."""
        self._stats = TelephonyStats()
        self._call_starts.clear()
        self._duration_total = 0.0
        self._duration_samples = 0
        logger.info("Metrics reset")


_default_metrics: TelephonyMetrics | None = None


def get_telephony_metrics(*, force_new: bool = False) -> TelephonyMetrics:
    """Return the process-wide TelephonyMetrics singleton."""
    global _default_metrics
    if _default_metrics is None or force_new:
        _default_metrics = TelephonyMetrics()
    return _default_metrics


def reset_telephony_metrics() -> None:
    """Reset process-wide telephony metrics (tests)."""
    get_telephony_metrics().reset()
