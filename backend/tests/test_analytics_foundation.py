"""Day 8 Phase 1: analytics architecture foundation."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from analytics.database import temporary_database
from analytics.models import CallAnalyticsRecord
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService


@pytest.fixture()
def service(tmp_path: Path) -> AnalyticsService:
    with temporary_database(tmp_path / "analytics.db"):
        yield AnalyticsService(AnalyticsRepository())


def test_valid_analytics_record(service: AnalyticsService) -> None:
    result = service.record_call("call-1", "browser", "en-IN")
    assert result == {"status": "recorded", "call_id": "call-1"}
    stored = service._repository.get_call("call-1")
    assert isinstance(stored, CallAnalyticsRecord)
    assert stored.outcome is None


@pytest.mark.parametrize(
    ("call_id", "channel", "language"),
    [
        ("", "browser", "en-IN"),
        ("call-x", "", "en-IN"),
        ("call-x", "browser", ""),
    ],
)
def test_invalid_required_fields(
    service: AnalyticsService,
    call_id: str,
    channel: str,
    language: str,
) -> None:
    result = service.record_call(call_id, channel, language)
    assert result["error"] is True


def test_invalid_outcome(service: AnalyticsService) -> None:
    result = service.record_call("call-2", "browser", "en-IN", outcome="maybe")
    assert result["error"] is True


def test_successful_and_failed_outcomes(service: AnalyticsService) -> None:
    service.start_call("ok-1", "browser", "en-IN")
    service.start_call("bad-1", "browser", "en-IN")
    assert service.complete_call("ok-1", "success")["outcome"] == "success"
    assert service.complete_call("bad-1", "failed")["outcome"] == "failed"


def test_summary_calculation(service: AnalyticsService) -> None:
    service.start_call("a", "browser", "en-IN")
    service.start_call("b", "browser", "en-IN")
    service.complete_call("a", "success")
    service.complete_call("b", "failed")
    summary = service.get_summary()
    assert summary["total_calls"] == 2
    assert summary["successful_calls"] == 1
    assert summary["failed_calls"] == 1


def test_empty_dataset_summary(service: AnalyticsService) -> None:
    summary = service.get_summary()
    assert summary == {
        "total_calls": 0,
        "successful_calls": 0,
        "failed_calls": 0,
        "success_rate": 0.0,
        "failure_rate": 0.0,
    }


def test_sensitive_fields_not_stored(service: AnalyticsService) -> None:
    service.record_call("safe-1", "browser", "en-IN")
    payload = service._repository.get_call("safe-1").to_dict()
    for banned in (
        "transcript",
        "spoken_answer",
        "phone_number",
        "password",
        "otp",
        "pin",
    ):
        assert banned not in payload
    assert "started_at" in payload
    assert isinstance(
        datetime.fromisoformat(payload["started_at"].replace("Z", "+00:00")),
        datetime,
    )
    assert payload["started_at"].endswith("Z") or "+" in payload["started_at"]
    assert datetime.now(timezone.utc)
