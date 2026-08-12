"""Typed analytics models for Learning & Literacy call metrics.

SUCCESS = learner completes the intended speaking exercise.
FAILED = call ends without completing the intended speaking exercise.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from typing import Any

ALLOWED_OUTCOMES: frozenset[str] = frozenset({"success", "failed"})
ALLOWED_CHANNELS: frozenset[str] = frozenset({"browser", "sip", "telephony"})
ALLOWED_FAILURE_TYPES: frozenset[str] = frozenset(
    {
        "user_declined",
        "incomplete_exercise",
        "tool_failure",
        "provider_error",
        "no_response",
        "user_hangup",
        "unknown",
    }
)

# Learning & Literacy success definition (documented for callers).
SUCCESS_DEFINITION = "Learner completed the intended speaking exercise."
FAILED_DEFINITION = "Call ended without completing the intended speaking exercise."


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_datetime(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, str) and value.strip():
        cleaned = value.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(cleaned)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return None


def isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class CallAnalyticsRecord:
    """Safe operational analytics record (no transcripts / PII)."""

    call_id: str
    started_at: datetime
    ended_at: datetime | None = None
    channel: str = "browser"
    language: str = "en-IN"
    outcome: str | None = None
    failure_type: str | None = None
    first_response_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "call_id": self.call_id,
            "started_at": isoformat(self.started_at),
            "ended_at": isoformat(self.ended_at),
            "channel": self.channel,
            "language": self.language,
            "outcome": self.outcome,
            "failure_type": self.failure_type,
            "first_response_at": isoformat(self.first_response_at),
        }


@dataclass
class DashboardMetrics:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_calls": max(0, int(self.total_calls)),
            "successful_calls": max(0, int(self.successful_calls)),
            "failed_calls": max(0, int(self.failed_calls)),
        }


@dataclass
class RecentCall:
    call_id: str
    started_at: str | None
    ended_at: str | None
    duration_seconds: int | None
    channel: str
    outcome: str | None
    failure_type: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PerformanceMetrics:
    average_call_duration_seconds: float = 0.0
    average_first_response_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "average_call_duration_seconds": float(self.average_call_duration_seconds),
            "average_first_response_ms": float(self.average_first_response_ms),
        }


@dataclass
class LanguageChannelMetrics:
    language_breakdown: dict[str, int] = field(default_factory=dict)
    channel_breakdown: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "language_breakdown": dict(self.language_breakdown),
            "channel_breakdown": dict(self.channel_breakdown),
        }


@dataclass
class AnalyticsInsights:
    total_calls: int = 0
    success_rate: float = 0.0
    average_call_duration_seconds: float = 0.0
    average_first_response_ms: float = 0.0
    top_failure_category: str | None = None
    top_language: str | None = None
    top_channel: str | None = None
    summary_sentence: str = "No completed calls are available for analysis."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AnalyticsFilter:
    start_date: date | None = None
    end_date: date | None = None
    channel: str | None = None
    outcome: str | None = None  # success | failed | incomplete

    def to_dict(self) -> dict[str, Any]:
        return {
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "channel": self.channel,
            "outcome": self.outcome,
        }


@dataclass
class AnalyticsSummary:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    success_rate: float = 0.0
    failure_rate: float = 0.0
    failure_categories: dict[str, int] = field(default_factory=dict)
    recent_calls: list[RecentCall] = field(default_factory=list)
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    language_breakdown: dict[str, int] = field(default_factory=dict)
    channel_breakdown: dict[str, int] = field(default_factory=dict)
    insights: AnalyticsInsights | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "failure_categories": dict(self.failure_categories),
            "recent_calls": [item.to_dict() for item in self.recent_calls],
            "performance": self.performance.to_dict(),
            "language_breakdown": dict(self.language_breakdown),
            "channel_breakdown": dict(self.channel_breakdown),
            "insights": self.insights.to_dict() if self.insights else None,
        }


@dataclass
class AnalyticsReport:
    generated_at: str
    filters: dict[str, Any]
    total_calls: int
    successful_calls: int
    failed_calls: int
    success_rate: float
    failure_rate: float
    failure_categories: dict[str, int]
    recent_calls: list[dict[str, Any]]
    average_call_duration_seconds: float
    average_first_response_ms: float
    language_breakdown: dict[str, int]
    channel_breakdown: dict[str, int]
    insights: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "filters": self.filters,
            "summary": {
                "total_calls": self.total_calls,
                "successful_calls": self.successful_calls,
                "failed_calls": self.failed_calls,
                "success_rate": self.success_rate,
                "failure_rate": self.failure_rate,
            },
            "performance": {
                "average_call_duration_seconds": self.average_call_duration_seconds,
                "average_first_response_ms": self.average_first_response_ms,
            },
            "language_breakdown": self.language_breakdown,
            "channel_breakdown": self.channel_breakdown,
            "failure_categories": self.failure_categories,
            "recent_calls": self.recent_calls,
            "insights": self.insights,
        }
