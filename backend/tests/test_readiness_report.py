"""Day 6 Bonus 8: production telephony readiness report."""

from __future__ import annotations

import logging

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.features import (
    FeatureFlags,
    clear_telephony_feature_flags,
)
from telephony.metrics import TelephonyMetrics, reset_telephony_metrics
from telephony.readiness import TelephonyReadinessReport
from telephony.service import TelephonyService


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
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()


def test_report_generated_when_ready(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    config = get_telephony_config(force_reload=True)
    with caplog.at_level(logging.INFO, logger="telephony.readiness"):
        report = TelephonyReadinessReport(
            config,
            TelephonyMetrics(),
            FeatureFlags(),
        ).generate()
    assert report["overall_status"] == "ready"
    assert report["checks_failed"] == 0
    assert report["checks_passed"] >= 1
    assert report["components"]["configuration"] == "healthy"
    assert report["components"]["metrics"] == "healthy"
    assert report["components"]["bootstrap"] == "healthy"
    assert report["components"]["learning"] == "healthy"
    assert "secret" not in str(report).lower() or "api_secret" not in str(report)
    joined = " ".join(r.message for r in caplog.records)
    assert "Readiness report generation started" in joined
    assert "Readiness checks completed" in joined
    assert "Production readiness confirmed" in joined


def test_report_not_ready_without_config() -> None:
    report = TelephonyReadinessReport(
        get_telephony_config(force_reload=True),
        TelephonyMetrics(),
        FeatureFlags(),
    ).generate()
    assert report["overall_status"] == "not_ready"
    assert report["checks_failed"] >= 1


def test_service_generate_readiness_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    service = TelephonyService(get_telephony_config(force_reload=True))
    report = service.generate_readiness_report()
    assert report["overall_status"] == "ready"
    assert isinstance(report["metrics"], dict)
    assert isinstance(report["diagnostics"], dict)
