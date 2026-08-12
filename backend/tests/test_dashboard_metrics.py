"""Day 8 Phase 4: dashboard metrics service."""

from __future__ import annotations

from pathlib import Path

import pytest

from analytics.dashboard import DashboardAnalytics
from analytics.database import temporary_database
from analytics.models import DashboardMetrics
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService


@pytest.fixture()
def service(tmp_path: Path) -> AnalyticsService:
    with temporary_database(tmp_path / "analytics.db"):
        yield AnalyticsService(AnalyticsRepository())


def test_empty_and_mixed(service: AnalyticsService) -> None:
    empty = service.get_dashboard_metrics()
    assert isinstance(empty, DashboardMetrics)
    assert empty.to_dict() == {
        "total_calls": 0,
        "successful_calls": 0,
        "failed_calls": 0,
    }

    service.start_call("s1", "browser", "en-IN")
    service.start_call("f1", "browser", "en-IN")
    service.start_call("i1", "browser", "en-IN")
    service.complete_call("s1", "success")
    service.complete_call("f1", "failed")
    metrics = service.get_dashboard_metrics()
    assert isinstance(metrics, DashboardMetrics)
    assert metrics.total_calls == 3
    assert metrics.successful_calls == 1
    assert metrics.failed_calls == 1
    assert metrics.total_calls == (metrics.successful_calls + metrics.failed_calls + 1)


def test_only_success_or_failed(service: AnalyticsService) -> None:
    service.start_call("s", "browser", "en-IN")
    service.complete_call("s", "success")
    m = service.get_dashboard_metrics()
    assert m.successful_calls == 1 and m.failed_calls == 0

    service.start_call("f", "browser", "en-IN")
    service.complete_call("f", "failed")
    m2 = service.get_dashboard_metrics()
    assert m2.failed_calls == 1


def test_dashboard_helper_and_error(service: AnalyticsService) -> None:
    dash = DashboardAnalytics(service)
    assert dash.get_metrics()["total_calls"] == 0

    class Boom(AnalyticsRepository):
        def get_dashboard_metrics(self, filters=None):  # type: ignore[no-untyped-def]
            raise RuntimeError("fail")

    broken = AnalyticsService(Boom())
    result = broken.get_dashboard_metrics()
    assert result == {
        "error": True,
        "message": "Analytics data unavailable.",
    }


def test_no_sensitive_data(service: AnalyticsService) -> None:
    service.start_call("x", "browser", "en-IN")
    payload = DashboardAnalytics(service).get_metrics()
    for key in ("transcript", "phone_number", "learner_id", "password"):
        assert key not in payload
