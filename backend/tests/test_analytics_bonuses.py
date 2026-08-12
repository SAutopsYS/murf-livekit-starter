"""Day 8 Bonuses 1-8: rates, history, filters, performance, insights, export."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from analytics.database import temporary_database
from analytics.models import AnalyticsReport, CallAnalyticsRecord
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService


@pytest.fixture()
def service(tmp_path: Path) -> AnalyticsService:
    with temporary_database(tmp_path / "analytics.db"):
        yield AnalyticsService(AnalyticsRepository())


def _seed(service: AnalyticsService) -> None:
    now = datetime.now(timezone.utc)
    repo = service._repository
    repo.create_call(
        CallAnalyticsRecord(
            call_id="c1",
            started_at=now - timedelta(minutes=10),
            ended_at=now - timedelta(minutes=8),
            channel="browser",
            language="en-IN",
            outcome="success",
            first_response_at=now - timedelta(minutes=9, seconds=50),
        )
    )
    repo.create_call(
        CallAnalyticsRecord(
            call_id="c2",
            started_at=now - timedelta(minutes=5),
            ended_at=now - timedelta(minutes=4),
            channel="browser",
            language="hi-IN",
            outcome="failed",
            failure_type="incomplete_exercise",
            first_response_at=now - timedelta(minutes=4, seconds=50),
        )
    )
    repo.create_call(
        CallAnalyticsRecord(
            call_id="c3",
            started_at=now - timedelta(days=10),
            ended_at=now - timedelta(days=10) + timedelta(minutes=2),
            channel="sip",
            language="en-IN",
            outcome="failed",
            failure_type="user_hangup",
        )
    )
    repo.create_call(
        CallAnalyticsRecord(
            call_id="c4",
            started_at=now,
            channel="browser",
            language="en-IN",
            outcome=None,
        )
    )


def test_bonus1_rates_and_categories(service: AnalyticsService) -> None:
    assert service.get_success_rate() == 0.0
    _seed(service)
    assert service.get_success_rate() == 33.3
    assert service.get_failure_rate() == 66.7
    assert abs(service.get_success_rate() + service.get_failure_rate() - 100.0) < 0.2
    cats = service._repository.get_failure_categories()
    assert cats["incomplete_exercise"] == 1
    assert cats["user_hangup"] == 1


def test_bonus2_recent_calls(service: AnalyticsService) -> None:
    assert service.get_recent_calls() == []
    _seed(service)
    recent = service.get_recent_calls(limit=2)
    assert isinstance(recent, list)
    assert len(recent) == 2
    assert recent[0].call_id == "c4"
    capped = service.get_recent_calls(limit=100)
    assert isinstance(capped, list)
    assert len(capped) <= 50
    assert capped[0].duration_seconds is None or capped[0].duration_seconds >= 0
    payload = capped[0].to_dict()
    assert "phone_number" not in payload
    assert "transcript" not in payload


def test_bonus3_filters(service: AnalyticsService) -> None:
    _seed(service)
    browser = service.build_filter(channel="browser")
    assert not isinstance(browser, dict) or not browser.get("error")
    summary = service.get_filtered_summary(browser)  # type: ignore[arg-type]
    assert not isinstance(summary, dict)
    assert summary.total_calls == 3
    assert summary.channel_breakdown.get("browser") == 3

    success = service.build_filter(outcome="success")
    s2 = service.get_filtered_summary(success)  # type: ignore[arg-type]
    assert not isinstance(s2, dict)
    assert s2.successful_calls == 1
    assert s2.failed_calls == 0

    invalid = service.build_filter(
        start_date=(date.today() + timedelta(days=1)).isoformat(),
        end_date=date.today().isoformat(),
        preset="custom",
    )
    assert isinstance(invalid, dict) and invalid["error"] is True

    week = service.build_filter(preset="last_7_days")
    s3 = service.get_filtered_summary(week)  # type: ignore[arg-type]
    assert not isinstance(s3, dict)
    assert s3.total_calls >= 3


def test_bonus5_performance(service: AnalyticsService) -> None:
    perf0 = service.get_performance_metrics()
    assert not isinstance(perf0, dict)
    assert perf0.average_call_duration_seconds == 0.0
    _seed(service)
    perf = service.get_performance_metrics()
    assert not isinstance(perf, dict)
    assert perf.average_call_duration_seconds > 0
    assert perf.average_first_response_ms > 0


def test_bonus6_language_channel(service: AnalyticsService) -> None:
    _seed(service)
    metrics = service.get_language_channel_metrics()
    assert not isinstance(metrics, dict)
    assert metrics.language_breakdown["en-IN"] >= 1
    assert metrics.channel_breakdown["browser"] >= 1


def test_bonus7_insights(service: AnalyticsService) -> None:
    insights0 = service.get_insights()
    assert not isinstance(insights0, dict)
    assert insights0.top_failure_category is None
    _seed(service)
    insights = service.get_insights()
    assert not isinstance(insights, dict)
    assert insights.top_channel in {"browser", "sip"}
    assert insights.top_language in {"en-IN", "hi-IN"}
    assert insights.top_failure_category in {
        "incomplete_exercise",
        "user_hangup",
    }


def test_bonus8_report_export(service: AnalyticsService) -> None:
    _seed(service)
    report = service.generate_report()
    assert isinstance(report, AnalyticsReport)
    payload = report.to_dict()
    assert payload["summary"]["total_calls"] == 4
    assert "recent_calls" in payload
    assert "phone_number" not in str(payload)
    assert "transcript" not in str(payload)

    filtered = service.build_filter(channel="sip")
    report2 = service.generate_report(filtered)  # type: ignore[arg-type]
    assert isinstance(report2, AnalyticsReport)
    assert report2.total_calls == 1


def test_filtered_summary_bundle(service: AnalyticsService) -> None:
    _seed(service)
    summary = service.get_filtered_summary()
    assert not isinstance(summary, dict)
    data = summary.to_dict()
    assert data["success_rate"] >= 0
    assert "insights" in data
    assert isinstance(data["recent_calls"], list)
