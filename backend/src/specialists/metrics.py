"""In-process specialist performance metrics. Aggregate only. No PII."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger("specialists.metrics")


@dataclass
class SpecialistMetrics:
    handoff_requests: int = 0
    successful_handoffs: int = 0
    failed_handoffs: int = 0
    recovered_handoffs: int = 0
    successful_handbacks: int = 0
    failed_handbacks: int = 0
    retry_count: int = 0
    math_sessions: int = 0
    successful_math_sessions: int = 0
    exercises_completed: int = 0
    routing_ms_total: float = 0.0
    routing_samples: int = 0
    handoff_ms_total: float = 0.0
    handoff_samples: int = 0
    handback_ms_total: float = 0.0
    handback_samples: int = 0
    session_ms_total: float = 0.0
    session_samples: int = 0

    def snapshot(self) -> dict[str, float | int]:
        def _avg(total: float, samples: int) -> float:
            if samples <= 0:
                return 0.0
            return round(total / samples, 2)

        recovery_rate = 0.0
        if self.failed_handoffs:
            recovery_rate = round(self.recovered_handoffs / self.failed_handoffs, 3)
        return {
            "total_handoffs": self.handoff_requests,
            "successful_handoffs": self.successful_handoffs,
            "failed_handoffs": self.failed_handoffs,
            "recovery_count": self.recovered_handoffs,
            "successful_handbacks": self.successful_handbacks,
            "failed_handbacks": self.failed_handbacks,
            "retry_count": self.retry_count,
            "math_sessions": self.math_sessions,
            "successful_math_sessions": self.successful_math_sessions,
            "average_exercises_completed": _avg(
                float(self.exercises_completed),
                self.math_sessions,
            ),
            "average_routing_time_ms": _avg(
                self.routing_ms_total, self.routing_samples
            ),
            "average_handoff_time_ms": _avg(
                self.handoff_ms_total, self.handoff_samples
            ),
            "average_handback_time_ms": _avg(
                self.handback_ms_total, self.handback_samples
            ),
            "average_specialist_session_duration_ms": _avg(
                self.session_ms_total,
                self.session_samples,
            ),
            "recovery_success_rate": recovery_rate,
        }

    def reset(self) -> None:
        self.handoff_requests = 0
        self.successful_handoffs = 0
        self.failed_handoffs = 0
        self.recovered_handoffs = 0
        self.successful_handbacks = 0
        self.failed_handbacks = 0
        self.retry_count = 0
        self.math_sessions = 0
        self.successful_math_sessions = 0
        self.exercises_completed = 0
        self.routing_ms_total = 0.0
        self.routing_samples = 0
        self.handoff_ms_total = 0.0
        self.handoff_samples = 0
        self.handback_ms_total = 0.0
        self.handback_samples = 0
        self.session_ms_total = 0.0
        self.session_samples = 0


_metrics = SpecialistMetrics()


def get_specialist_metrics() -> dict[str, float | int]:
    return _metrics.snapshot()


def reset_specialist_metrics() -> None:
    global _metrics
    _metrics = SpecialistMetrics()


def record_handoff(
    *, success: bool, recovered: bool = False, duration_ms: float | None = None
) -> None:
    _metrics.handoff_requests += 1
    if success:
        _metrics.successful_handoffs += 1
        _metrics.math_sessions += 1
        logger.info("Handoff success")
    else:
        _metrics.failed_handoffs += 1
        logger.info("Handoff failure")
        if recovered:
            _metrics.recovered_handoffs += 1
            logger.info("Recovery used")
    if duration_ms is not None:
        _metrics.handoff_ms_total += max(duration_ms, 0.0)
        _metrics.handoff_samples += 1


def record_handback(
    *, success: bool, duration_ms: float | None = None, exercises: int = 0
) -> None:
    if success:
        _metrics.successful_handbacks += 1
        _metrics.successful_math_sessions += 1
        _metrics.exercises_completed += max(exercises, 0)
        logger.info("Specialist finished")
    else:
        _metrics.failed_handbacks += 1
    if duration_ms is not None:
        _metrics.handback_ms_total += max(duration_ms, 0.0)
        _metrics.handback_samples += 1
        _metrics.session_ms_total += max(duration_ms, 0.0)
        _metrics.session_samples += 1


def record_retry() -> None:
    _metrics.retry_count += 1


def record_routing(duration_ms: float | None = None) -> None:
    if duration_ms is None:
        return
    _metrics.routing_ms_total += max(duration_ms, 0.0)
    _metrics.routing_samples += 1
    logger.info("Routing completed")
