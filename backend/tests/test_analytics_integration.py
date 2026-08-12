"""Day 8 Phase 3: lifecycle integration helpers."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from analytics.database import temporary_database
from analytics.integration import (
    complete_call_analytics,
    start_call_analytics,
)
from analytics.repository import AnalyticsRepository
from analytics.service import AnalyticsService
from telephony.service import TelephonyService


@pytest.fixture()
def service(tmp_path: Path) -> AnalyticsService:
    with temporary_database(tmp_path / "analytics.db"):
        yield AnalyticsService(AnalyticsRepository())


def test_browser_start_and_outcomes(service: AnalyticsService) -> None:
    started = start_call_analytics("room-1", "browser", "en-IN", service=service)
    assert started["status"] == "recorded"
    assert complete_call_analytics("room-1", "success", service=service)["outcome"] == (
        "success"
    )

    start_call_analytics("room-2", "browser", "en-IN", service=service)
    assert complete_call_analytics("room-2", "failed", service=service)["outcome"] == (
        "failed"
    )


def test_uuid_fallback_and_reuse(service: AnalyticsService) -> None:
    first = start_call_analytics(None, "browser", "en-IN", service=service)
    assert first["call_id"].startswith("call-")
    second = start_call_analytics("room-fixed", "browser", "en-IN", service=service)
    again = start_call_analytics("room-fixed", "browser", "en-IN", service=service)
    assert again["call_id"] == second["call_id"]


def test_analytics_failure_does_not_break_flow(service: AnalyticsService) -> None:
    class BoomRepo(AnalyticsRepository):
        def create_call(self, record):  # type: ignore[no-untyped-def]
            raise RuntimeError("db down")

    broken = AnalyticsService(BoomRepo())
    result = start_call_analytics("x", "browser", "en-IN", service=broken)
    assert result.get("error") is True
    # Caller continues.
    assert True


def test_outbound_start_and_completion(
    service: AnalyticsService, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeDialer:
        def place_outbound_call(self, **kwargs: Any) -> dict[str, Any]:
            return {
                "status": "calling",
                "call_id": "sip-call-1",
                "provider": "livekit",
            }

    telephony = TelephonyService(dialer=FakeDialer())  # type: ignore[arg-type]
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")
    from telephony.config import clear_telephony_config_cache, get_telephony_config
    from telephony.features import clear_telephony_feature_flags

    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    telephony = TelephonyService(
        config=get_telephony_config(force_reload=True),
        dialer=FakeDialer(),  # type: ignore[arg-type]
    )
    # Force analytics service used by integration to our temp service.
    monkeypatch.setattr(
        "analytics.integration.get_analytics_service",
        lambda: service,
    )
    result = telephony.place_call("+919876543210", "daily_practice", "en-IN")
    assert result.get("error") is not True
    assert service._repository.get_call("sip-call-1") is not None

    telephony._last_analytics_call_id = "sip-call-1"
    telephony._learning_session = SimpleNamespace(
        evaluate_practice=lambda **kwargs: {
            "score": 80,
            "recommendation": "continue",
        }
    )
    evaluated = telephony.evaluate_outbound_session("learner-1", "Hello there")
    assert evaluated.get("error") is not True
    assert service._repository.get_call("sip-call-1").outcome == "success"


def test_duplicate_completion_and_privacy(service: AnalyticsService) -> None:
    start_call_analytics("dup", "browser", "en-IN", service=service)
    complete_call_analytics("dup", "success", service=service)
    again = complete_call_analytics("dup", "failed", service=service)
    assert again["status"] == "already_completed"
    payload = service._repository.get_call("dup").to_dict()
    assert "transcript" not in payload
    summary = service.get_summary()
    assert summary["total_calls"] == 1
