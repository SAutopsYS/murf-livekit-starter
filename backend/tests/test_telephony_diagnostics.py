"""Day 6 Bonus 4: telephony health diagnostics."""

from __future__ import annotations

import logging

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.diagnostics import TelephonyDiagnostics
from telephony.features import clear_telephony_feature_flags
from telephony.metrics import TelephonyMetrics, reset_telephony_metrics
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
        "DIAGNOSTICS_ENABLED",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()


def test_diagnostics_succeed_with_valid_config(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    config = get_telephony_config(force_reload=True)
    metrics = TelephonyMetrics()
    with caplog.at_level(logging.INFO, logger="telephony.diagnostics"):
        report = TelephonyDiagnostics(config, metrics).run_checks()
    assert report["healthy"] is True
    components = {c["component"]: c for c in report["checks"]}
    assert components["configuration"]["healthy"] is True
    assert components["livekit"]["healthy"] is True
    assert components["metrics"]["healthy"] is True
    joined = " ".join(r.message for r in caplog.records)
    assert "Telephony diagnostics started" in joined
    assert "Configuration verified" in joined
    assert "Provider verified" in joined
    assert "Diagnostics completed" in joined


def test_missing_configuration_detected() -> None:
    config = get_telephony_config(force_reload=True)
    report = TelephonyDiagnostics(config, TelephonyMetrics()).run_checks()
    assert report["healthy"] is False
    assert any(
        c["component"] == "configuration" and c["healthy"] is False
        for c in report["checks"]
    )


def test_service_run_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    service = TelephonyService(get_telephony_config(force_reload=True))
    report = service.run_diagnostics()
    assert report["healthy"] is True
    assert "checks" in report
    assert "secret" not in str(report).lower() or "LIVEKIT_API_SECRET" not in str(
        report
    )
