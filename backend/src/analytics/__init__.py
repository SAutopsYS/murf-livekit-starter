"""Call analytics package for the Learning & Literacy tutor.

SUCCESS = learner completes the intended speaking exercise.
FAILED = call ends without completing the intended speaking exercise.
"""

from analytics.integration import (
    complete_call_analytics,
    mark_first_response_analytics,
    start_call_analytics,
)
from analytics.models import (
    AnalyticsFilter,
    AnalyticsSummary,
    CallAnalyticsRecord,
    DashboardMetrics,
    RecentCall,
)
from analytics.repository import AnalyticsRepository, get_analytics_repository
from analytics.service import AnalyticsService, get_analytics_service

__all__ = [
    "AnalyticsFilter",
    "AnalyticsRepository",
    "AnalyticsService",
    "AnalyticsSummary",
    "CallAnalyticsRecord",
    "DashboardMetrics",
    "RecentCall",
    "complete_call_analytics",
    "get_analytics_repository",
    "get_analytics_service",
    "mark_first_response_analytics",
    "start_call_analytics",
]
