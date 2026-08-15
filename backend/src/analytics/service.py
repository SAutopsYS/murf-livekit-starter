"""Analytics service: validate, record, and summarize call metrics."""

from __future__ import annotations

import logging
import re
from datetime import date, datetime, timedelta
from typing import Any

from analytics.models import (
    ALLOWED_FAILURE_TYPES,
    ALLOWED_OUTCOMES,
    AnalyticsFilter,
    AnalyticsInsights,
    AnalyticsReport,
    AnalyticsSummary,
    CallAnalyticsRecord,
    DashboardMetrics,
    LanguageChannelMetrics,
    PerformanceMetrics,
    RecentCall,
    isoformat,
    utc_now,
)
from analytics.repository import AnalyticsRepository, get_analytics_repository

logger = logging.getLogger("analytics.service")

_UNSAFE_KEYS = frozenset(
    {
        "transcript",
        "spoken_answer",
        "phone_number",
        "password",
        "otp",
        "pin",
        "account_number",
        "learner_name",
        "learner_id",
        "user_id",
        "name",
        "email",
        "secret",
        "token",
        "webhook",
    }
)


class AnalyticsService:
    """Operational call analytics without transcripts or learner PII."""

    def __init__(self, repository: AnalyticsRepository | None = None) -> None:
        self._repository = repository or get_analytics_repository()

    def record_call(
        self,
        call_id: str,
        channel: str,
        language: str,
        started_at: datetime | None = None,
        outcome: str | None = None,
    ) -> dict[str, Any]:
        """Validate and create a call analytics record."""
        validation = self._validate_start(call_id, channel, language, outcome)
        if validation is not None:
            return validation

        existing = self._repository.get_call(call_id.strip())
        if existing is not None:
            return {"status": "recorded", "call_id": existing.call_id}

        record = CallAnalyticsRecord(
            call_id=call_id.strip(),
            started_at=started_at or utc_now(),
            channel=channel.strip().lower(),
            language=language.strip(),
            outcome=outcome,
        )
        created = self._repository.create_call(record)
        if created is None:
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Unable to record analytics."}
        logger.info("Analytics record created")
        return {"status": "recorded", "call_id": created.call_id}

    def start_call(
        self,
        call_id: str,
        channel: str,
        language: str,
    ) -> dict[str, Any]:
        logger.info("Analytics call started")
        return self.record_call(
            call_id=call_id,
            channel=channel,
            language=language,
            outcome=None,
        )

    def record_outcome(
        self,
        call_id: str,
        outcome: str,
        *,
        failure_type: str | None = None,
    ) -> dict[str, Any]:
        return self.complete_call(
            call_id=call_id,
            outcome=outcome,
            failure_type=failure_type,
        )

    def complete_call(
        self,
        call_id: str,
        outcome: str,
        *,
        failure_type: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(call_id, str) or not call_id.strip():
            logger.info("Analytics call unavailable")
            return {"error": True, "message": "Call record unavailable."}

        if (
            not isinstance(outcome, str)
            or outcome.strip().lower() not in ALLOWED_OUTCOMES
        ):
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Invalid call outcome."}

        outcome_key = outcome.strip().lower()
        fail_type: str | None = None
        if outcome_key == "failed":
            if isinstance(failure_type, str) and failure_type.strip():
                candidate = failure_type.strip().lower()
                fail_type = (
                    candidate if candidate in ALLOWED_FAILURE_TYPES else "unknown"
                )
            else:
                fail_type = "incomplete_exercise"

        current = self._repository.get_call(call_id.strip())
        if current is None:
            logger.info("Analytics call unavailable")
            return {"error": True, "message": "Call record unavailable."}

        if current.outcome in ALLOWED_OUTCOMES:
            logger.info("Analytics call already completed")
            return {
                "status": "already_completed",
                "outcome": current.outcome,
            }

        updated = self._repository.update_outcome(
            call_id.strip(),
            outcome_key,
            ended_at=utc_now(),
            failure_type=fail_type,
        )
        if updated is None:
            logger.info("Analytics call unavailable")
            return {"error": True, "message": "Call record unavailable."}

        logger.info("Analytics call completed")
        logger.info("Analytics outcome recorded")
        return {"status": "completed", "outcome": updated.outcome}

    def mark_first_response(self, call_id: str) -> dict[str, Any]:
        if not isinstance(call_id, str) or not call_id.strip():
            return {"error": True, "message": "Call record unavailable."}
        updated = self._repository.update_first_response(call_id.strip(), utc_now())
        if updated is None:
            return {"error": True, "message": "Call record unavailable."}
        return {"status": "recorded", "call_id": updated.call_id}

    def get_summary(self, filters: AnalyticsFilter | None = None) -> dict[str, Any]:
        logger.info("Analytics summary requested")
        try:
            metrics = self.get_dashboard_metrics(filters)
            if isinstance(metrics, dict) and metrics.get("error"):
                return metrics
            assert isinstance(metrics, DashboardMetrics)
            rate = self._rates(metrics)
            return {
                "total_calls": metrics.total_calls,
                "successful_calls": metrics.successful_calls,
                "failed_calls": metrics.failed_calls,
                **rate,
            }
        except Exception:
            logger.info("Analytics data unavailable")
            return {"error": True, "message": "Analytics data unavailable."}

    def get_dashboard_metrics(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> DashboardMetrics | dict[str, Any]:
        logger.info("Analytics metrics requested")
        try:
            metrics = self._repository.get_dashboard_metrics(filters)
            logger.info("Analytics metrics calculated")
            return metrics
        except Exception:
            logger.info("Analytics data unavailable")
            return {"error": True, "message": "Analytics data unavailable."}

    def get_success_rate(self, filters: AnalyticsFilter | None = None) -> float:
        metrics = self._repository.get_dashboard_metrics(filters)
        return self._rates(metrics)["success_rate"]

    def get_failure_rate(self, filters: AnalyticsFilter | None = None) -> float:
        metrics = self._repository.get_dashboard_metrics(filters)
        return self._rates(metrics)["failure_rate"]

    def get_recent_calls(
        self,
        limit: int = 10,
        filters: AnalyticsFilter | None = None,
    ) -> list[RecentCall] | dict[str, Any]:
        try:
            return self._repository.get_recent_calls(limit=limit, filters=filters)
        except Exception:
            return {
                "error": True,
                "message": "Recent call history is temporarily unavailable.",
            }

    def get_performance_metrics(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> PerformanceMetrics | dict[str, Any]:
        try:
            records = self._repository.list_records_for_performance(filters)
            durations: list[float] = []
            latencies: list[float] = []
            for record in records:
                if (
                    record.started_at
                    and record.ended_at
                    and record.ended_at >= record.started_at
                ):
                    durations.append(
                        (record.ended_at - record.started_at).total_seconds()
                    )
                if (
                    record.started_at
                    and record.first_response_at
                    and record.first_response_at >= record.started_at
                ):
                    latencies.append(
                        (record.first_response_at - record.started_at).total_seconds()
                        * 1000.0
                    )
            avg_duration = (
                round(sum(durations) / len(durations), 1) if durations else 0.0
            )
            avg_latency = (
                round(sum(latencies) / len(latencies), 1) if latencies else 0.0
            )
            return PerformanceMetrics(
                average_call_duration_seconds=avg_duration,
                average_first_response_ms=avg_latency,
            )
        except Exception:
            return {
                "error": True,
                "message": "Performance analytics unavailable.",
            }

    def get_language_channel_metrics(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> LanguageChannelMetrics | dict[str, Any]:
        try:
            return LanguageChannelMetrics(
                language_breakdown=self._repository.get_language_breakdown(filters),
                channel_breakdown=self._repository.get_channel_breakdown(filters),
            )
        except Exception:
            return {
                "error": True,
                "message": "Language and channel analytics unavailable.",
            }

    def get_insights(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> AnalyticsInsights | dict[str, Any]:
        try:
            metrics = self._repository.get_dashboard_metrics(filters)
            rates = self._rates(metrics)
            performance = self.get_performance_metrics(filters)
            if isinstance(performance, dict):
                performance = PerformanceMetrics()
            categories = self._repository.get_failure_categories(filters)
            languages = self._repository.get_language_breakdown(filters)
            channels = self._repository.get_channel_breakdown(filters)
            top_failure = self._top_key(categories)
            top_language = self._top_key(languages)
            top_channel = self._top_key(channels)
            completed = metrics.successful_calls + metrics.failed_calls
            if completed == 0:
                sentence = "No completed calls are available for analysis."
            else:
                minutes = int(performance.average_call_duration_seconds // 60)
                seconds = int(performance.average_call_duration_seconds % 60)
                sentence = (
                    f"{rates['success_rate']}% of completed calls were successful, "
                    f"with an average call duration of {minutes}m {seconds:02d}s."
                )
            return AnalyticsInsights(
                total_calls=metrics.total_calls,
                success_rate=rates["success_rate"],
                average_call_duration_seconds=(
                    performance.average_call_duration_seconds
                ),
                average_first_response_ms=performance.average_first_response_ms,
                top_failure_category=top_failure,
                top_language=top_language,
                top_channel=top_channel,
                summary_sentence=sentence,
            )
        except Exception:
            return {
                "error": True,
                "message": "Analytics insights unavailable.",
            }

    def get_filtered_summary(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> AnalyticsSummary | dict[str, Any]:
        date_error = self._validate_date_range(filters)
        if date_error is not None:
            return date_error
        try:
            metrics = self._repository.get_dashboard_metrics(filters)
            rates = self._rates(metrics)
            recent = self.get_recent_calls(limit=10, filters=filters)
            if isinstance(recent, dict):
                recent_list: list[RecentCall] = []
            else:
                recent_list = recent
            performance = self.get_performance_metrics(filters)
            if isinstance(performance, dict):
                performance = PerformanceMetrics()
            language_channel = self.get_language_channel_metrics(filters)
            if isinstance(language_channel, dict):
                language_channel = LanguageChannelMetrics()
            insights = self.get_insights(filters)
            insights_obj = None if isinstance(insights, dict) else insights
            return AnalyticsSummary(
                total_calls=metrics.total_calls,
                successful_calls=metrics.successful_calls,
                failed_calls=metrics.failed_calls,
                success_rate=rates["success_rate"],
                failure_rate=rates["failure_rate"],
                failure_categories=self._repository.get_failure_categories(filters),
                recent_calls=recent_list,
                performance=performance,
                language_breakdown=language_channel.language_breakdown,
                channel_breakdown=language_channel.channel_breakdown,
                insights=insights_obj,
            )
        except Exception:
            logger.info("Analytics data unavailable")
            return {"error": True, "message": "Analytics data unavailable."}

    def generate_report(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> AnalyticsReport | dict[str, Any]:
        summary = self.get_filtered_summary(filters)
        if isinstance(summary, dict) and summary.get("error"):
            return summary
        assert isinstance(summary, AnalyticsSummary)
        report = AnalyticsReport(
            generated_at=isoformat(utc_now()) or "",
            filters=filters.to_dict() if filters else {},
            total_calls=summary.total_calls,
            successful_calls=summary.successful_calls,
            failed_calls=summary.failed_calls,
            success_rate=summary.success_rate,
            failure_rate=summary.failure_rate,
            failure_categories=dict(summary.failure_categories),
            recent_calls=[item.to_dict() for item in summary.recent_calls],
            average_call_duration_seconds=(
                summary.performance.average_call_duration_seconds
            ),
            average_first_response_ms=summary.performance.average_first_response_ms,
            language_breakdown=dict(summary.language_breakdown),
            channel_breakdown=dict(summary.channel_breakdown),
            insights=summary.insights.to_dict() if summary.insights else None,
        )
        payload = report.to_dict()
        if not self._is_privacy_safe(payload):
            return {"error": True, "message": "Analytics report unavailable."}
        return report

    def build_filter(
        self,
        *,
        preset: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        channel: str | None = None,
        outcome: str | None = None,
    ) -> AnalyticsFilter | dict[str, Any]:
        today = date.today()
        start: date | None = None
        end: date | None = None
        key = (preset or "").strip().lower()
        if key == "today":
            start = today
            end = today
        elif key in {"last_7_days", "7d", "last7"}:
            start = today - timedelta(days=6)
            end = today
        elif key in {"last_30_days", "30d", "last30"}:
            start = today - timedelta(days=29)
            end = today
        elif key in {"", "all", "none"}:
            start = None
            end = None
        else:
            # custom
            start = self._parse_date(start_date)
            end = self._parse_date(end_date)

        channel_key = channel.strip().lower() if isinstance(channel, str) else None
        if channel_key in {"", "all", "none"}:
            channel_key = None
        outcome_key = outcome.strip().lower() if isinstance(outcome, str) else None
        if outcome_key in {"", "all", "none"}:
            outcome_key = None
        if outcome_key not in {None, "success", "failed", "incomplete"}:
            return {"error": True, "message": "Invalid date range."}

        filters = AnalyticsFilter(
            start_date=start,
            end_date=end,
            channel=channel_key,
            outcome=outcome_key,
        )
        date_error = self._validate_date_range(filters)
        if date_error is not None:
            return date_error
        return filters

    @staticmethod
    def _rates(metrics: DashboardMetrics) -> dict[str, float]:
        completed = metrics.successful_calls + metrics.failed_calls
        if completed <= 0:
            return {"success_rate": 0.0, "failure_rate": 0.0}
        success = round(metrics.successful_calls / completed * 100, 1)
        failure = round(metrics.failed_calls / completed * 100, 1)
        return {"success_rate": success, "failure_rate": failure}

    @staticmethod
    def _top_key(counts: dict[str, int]) -> str | None:
        if not counts:
            return None
        best = max(counts.values())
        tied = sorted(key for key, value in counts.items() if value == best)
        return tied[0] if tied else None

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        if not isinstance(value, str) or not value.strip():
            return None
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None

    @staticmethod
    def _validate_date_range(
        filters: AnalyticsFilter | None,
    ) -> dict[str, Any] | None:
        if filters is None:
            return None
        if (
            filters.start_date is not None
            and filters.end_date is not None
            and filters.start_date > filters.end_date
        ):
            return {"error": True, "message": "Invalid date range."}
        return None

    def _validate_start(
        self,
        call_id: str,
        channel: str,
        language: str,
        outcome: str | None,
    ) -> dict[str, Any] | None:
        if not isinstance(call_id, str) or not call_id.strip():
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Invalid analytics record."}
        if not isinstance(channel, str) or not channel.strip():
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Invalid analytics record."}
        if not isinstance(language, str) or not language.strip():
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Invalid analytics record."}
        if outcome is not None and (
            not isinstance(outcome, str)
            or outcome.strip().lower() not in ALLOWED_OUTCOMES
        ):
            logger.info("Analytics validation failed")
            return {"error": True, "message": "Invalid analytics record."}
        return None

    def _is_privacy_safe(self, payload: Any) -> bool:
        text = str(payload).lower()
        for key in _UNSAFE_KEYS:
            # Allow key names in schema docs only when values are empty; reject
            # common secret-like payloads.
            if f"'{key}':" in text or f'"{key}":' in text:
                # Keys in failure_categories etc. are fine; block if value present.
                pattern = rf'["\']{re.escape(key)}["\']\s*:\s*["\'][^"\']+["\']'
                if re.search(pattern, text) and key in {
                    "transcript",
                    "spoken_answer",
                    "phone_number",
                    "password",
                    "otp",
                    "pin",
                }:
                    return False
        # Phone-like sequences in export payload.
        return not re.search(r"\+\d{8,15}", text)


_default_service: AnalyticsService | None = None


def get_analytics_service() -> AnalyticsService:
    global _default_service
    if _default_service is None:
        _default_service = AnalyticsService()
    return _default_service


def reset_analytics_service() -> AnalyticsService:
    global _default_service
    from analytics.repository import reset_analytics_repository

    reset_analytics_repository()
    _default_service = AnalyticsService()
    return _default_service
