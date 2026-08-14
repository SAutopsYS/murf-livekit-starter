"""Day 9 Bonus 5: specialist performance analytics."""

from __future__ import annotations

from pathlib import Path

import pytest

from analytics.dashboard import DashboardAnalytics
from analytics.database import temporary_database
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService
from specialists.handoff import execute_handback, execute_handoff
from specialists.metrics import get_specialist_metrics, reset_specialist_metrics
from specialists.registry import reset_specialist_registry
from specialists.router import SpecialistRouter
from specialists.schemas import SpecialistContext


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_specialist_registry()
    reset_specialist_metrics()
    yield
    reset_specialist_registry()
    reset_specialist_metrics()


def test_successful_and_failed_and_recovery_metrics() -> None:
    execute_handoff(user_text="Let's practice multiplication", language="en")
    execute_handback(
        reason="solved",
        problem_solved=True,
        current_context=SpecialistContext(language="en"),
    )

    def _boom(_ctx: SpecialistContext) -> object:
        raise RuntimeError("down")

    execute_handoff(
        user_text="Help me with fractions",
        language="en",
        specialist_factory=_boom,
    )
    snap = get_specialist_metrics()
    assert snap["successful_handoffs"] == 1
    assert snap["failed_handoffs"] == 1
    assert snap["recovery_count"] == 1
    assert snap["successful_handbacks"] == 1
    assert snap["retry_count"] == 1


def test_routing_timing_and_usage() -> None:
    SpecialistRouter().route("Let's practice multiplication")
    snap = get_specialist_metrics()
    assert snap["average_routing_time_ms"] >= 0
    execute_handoff(user_text="Can you teach fractions?", language="en")
    usage = get_specialist_metrics()
    assert usage["math_sessions"] == 1


def test_dashboard_api_response_and_zero_metrics(tmp_path: Path) -> None:
    with temporary_database(tmp_path / "analytics.db"):
        dash = DashboardAnalytics(AnalyticsService(AnalyticsRepository()))
        payload = dash.get_summary()
        specialist = payload["specialist_analytics"]
        assert specialist["total_handoffs"] == 0
        assert specialist["successful_handoffs"] == 0
        assert "learner" not in str(specialist).lower()
        assert "transcript" not in specialist
        execute_handoff(user_text="Let's practice multiplication")
        again = dash.get_summary()["specialist_analytics"]
        assert again["successful_handoffs"] == 1


def test_privacy_and_aggregates_only() -> None:
    execute_handoff(user_text="Let's practice multiplication")
    execute_handoff(user_text="Help me with percentages")
    snap = get_specialist_metrics()
    blob = str(snap)
    assert "multiplication" not in blob
    assert "percentages" not in blob
    assert snap["total_handoffs"] == 2
