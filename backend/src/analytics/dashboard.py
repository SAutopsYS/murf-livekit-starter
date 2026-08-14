"""Read-only dashboard analytics helper."""

from __future__ import annotations

import logging
from typing import Any

from analytics.models import AnalyticsFilter, AnalyticsSummary
from analytics.service import AnalyticsService, get_analytics_service

logger = logging.getLogger("analytics.dashboard")


class DashboardAnalytics:
    """Thin read-only facade over AnalyticsService for dashboard consumers."""

    def __init__(self, service: AnalyticsService | None = None) -> None:
        self._service = service or get_analytics_service()

    def get_metrics(self, filters: AnalyticsFilter | None = None) -> dict[str, Any]:
        result = self._service.get_dashboard_metrics(filters)
        if isinstance(result, dict):
            return result
        return result.to_dict()

    def get_summary(self, filters: AnalyticsFilter | None = None) -> dict[str, Any]:
        summary = self._service.get_filtered_summary(filters)
        if isinstance(summary, dict):
            payload = summary
        else:
            assert isinstance(summary, AnalyticsSummary)
            payload = summary.to_dict()
        try:
            from specialists.metrics import get_specialist_metrics

            payload["specialist_analytics"] = get_specialist_metrics()
        except Exception:
            payload["specialist_analytics"] = {
                "total_handoffs": 0,
                "successful_handoffs": 0,
                "failed_handoffs": 0,
                "recovery_count": 0,
                "average_routing_time_ms": 0.0,
                "average_specialist_session_duration_ms": 0.0,
            }
        return payload
