"""Day 6 Bonus 2/3: telephony metrics and operational counters."""

from __future__ import annotations

import logging
import time
from typing import Any

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.features import clear_telephony_feature_flags
from telephony.metrics import TelephonyMetrics, reset_telephony_metrics
from telephony.service import TelephonyService


class _FakeDialer:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail

    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        del phone_number, room_name
        if self.fail:
            return {"error": True, "message": "Unable to place outbound call."}
        return {
            "status": "calling",
            "provider": "livekit",
            "call_id": "SCL_metrics_1",
            "purpose": purpose,
            "language": language,
            "room_name": "outbound-metrics",
            "participant_identity": "sip-outbound-metrics",
        }


@pytest.fixture(autouse=True)
def _reset(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
        "METRICS_ENABLED",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()


def test_metrics_initialize(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="telephony.metrics"):
        metrics = TelephonyMetrics()
    snap = metrics.snapshot()
    assert snap["calls_started"] == 0
    assert snap["average_call_duration_seconds"] == 0.0
    assert any("Telephony metrics initialized" in r.message for r in caplog.records)


def test_increment_and_snapshot() -> None:
    metrics = TelephonyMetrics()
    metrics.increment("calls_started")
    metrics.increment("bootstrap_generated")
    metrics.increment("unknown_metric")
    snap = metrics.snapshot()
    assert snap["calls_started"] == 1
    assert snap["bootstrap_generated"] == 1
    assert snap["outbound_attempts"] == 1
    assert snap["total_calls"] == 1


def test_reset_clears_counters() -> None:
    metrics = TelephonyMetrics()
    metrics.record_call_started()
    metrics.record_call_success()
    metrics.record_retry()
    metrics.reset()
    snap = metrics.snapshot()
    assert snap["calls_started"] == 0
    assert snap["calls_completed"] == 0
    assert snap["retry_recommended"] == 0


def test_call_duration_and_duplicate_end() -> None:
    metrics = TelephonyMetrics()
    metrics.record_call_start("c1")
    time.sleep(0.02)
    metrics.record_call_end("c1")
    metrics.record_call_end("c1")
    snap = metrics.snapshot()
    assert snap["average_call_duration_seconds"] >= 0.0
    assert metrics._duration_samples == 1


def test_service_integration_updates_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")
    metrics = TelephonyMetrics()
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(),
        metrics=metrics,
    )
    ok = service.place_call("9876543210", purpose="daily_practice")
    assert ok.get("error") is not True
    service.handle_call_outcome("busy")
    snap = service.get_metrics()
    assert snap["calls_started"] >= 1
    assert snap["calls_completed"] >= 1
    assert snap["bootstrap_generated"] >= 1
    assert snap["outcomes_processed"] >= 1
    assert snap["retry_recommended"] >= 1
    health = service.health()
    assert "metrics" in health
    assert health["metrics"]["outbound_success"] >= 1


def test_failed_call_increments_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")
    metrics = TelephonyMetrics()
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(fail=True),
        metrics=metrics,
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result["error"] is True
    assert metrics.snapshot()["calls_failed"] >= 1
