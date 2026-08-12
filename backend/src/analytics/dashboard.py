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
            return summary
        assert isinstance(summary, AnalyticsSummary)
        return summary.to_dict()
