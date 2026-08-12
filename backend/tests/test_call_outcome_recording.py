"""Day 8 Phase 2: call start/outcome recording."""

from __future__ import annotations

from pathlib import Path

import pytest

from analytics.database import temporary_database
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService


@pytest.fixture()
def service(tmp_path: Path) -> AnalyticsService:
    with temporary_database(tmp_path / "analytics.db"):
        yield AnalyticsService(AnalyticsRepository())


def test_start_creates_record(service: AnalyticsService) -> None:
    result = service.start_call("call-100", "browser", "hi-IN")
    assert result["status"] == "recorded"
    stored = service._repository.get_call("call-100")
    assert stored is not None
    assert stored.language == "hi-IN"
    assert stored.outcome is None


@pytest.mark.parametrize(
    ("call_id", "channel", "language"),
    [("", "browser", "en"), ("c", "", "en"), ("c", "browser", "")],
)
def test_start_validation(
    service: AnalyticsService, call_id: str, channel: str, language: str
) -> None:
    assert service.start_call(call_id, channel, language)["error"] is True


def test_complete_success_and_failed(service: AnalyticsService) -> None:
    service.start_call("s1", "browser", "en-IN")
    service.start_call("f1", "sip", "en-IN")
    assert service.complete_call("s1", "success") == {
        "status": "completed",
        "outcome": "success",
    }
    assert service.complete_call("f1", "failed")["outcome"] == "failed"
    assert service._repository.get_call("s1").ended_at is not None


def test_invalid_and_unknown(service: AnalyticsService) -> None:
    service.start_call("u1", "browser", "en-IN")
    assert service.complete_call("u1", "weird")["error"] is True
    assert service.complete_call("missing", "success") == {
        "error": True,
        "message": "Call record unavailable.",
    }


def test_duplicate_completion_safe(service: AnalyticsService) -> None:
    service.start_call("d1", "browser", "en-IN")
    service.complete_call("d1", "success")
    again = service.complete_call("d1", "failed")
    assert again == {"status": "already_completed", "outcome": "success"}
    assert service._repository.get_call("d1").outcome == "success"


def test_summary_updates(service: AnalyticsService) -> None:
    service.start_call("a", "browser", "en-IN")
    service.complete_call("a", "success")
    summary = service.get_summary()
    assert summary["total_calls"] == 1
    assert summary["successful_calls"] == 1


def test_no_sensitive_fields(service: AnalyticsService) -> None:
    service.start_call("safe", "browser", "en-IN")
    service.complete_call("safe", "failed", failure_type="user_hangup")
    data = service._repository.get_call("safe").to_dict()
    assert "phone_number" not in data
    assert "transcript" not in data
    assert data["failure_type"] == "user_hangup"
