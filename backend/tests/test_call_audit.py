"""Day 6 Bonus 1: outbound call audit logger."""

from __future__ import annotations

import logging
from typing import Any

import pytest

from telephony.audit import CallAuditLogger, log_event, sanitize_metadata
from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.features import clear_telephony_feature_flags
from telephony.metrics import reset_telephony_metrics
from telephony.service import TelephonyService


class _FakeDialer:
    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        del phone_number, room_name
        return {
            "status": "calling",
            "provider": "livekit",
            "call_id": "SCL_audit_1",
            "purpose": purpose,
            "language": language,
            "room_name": "outbound-audit",
            "participant_identity": "sip-outbound-audit",
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
        "TELEPHONY_ENABLED",
        "OUTBOUND_CALLING_ENABLED",
        "AUDIT_ENABLED",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()


def test_logger_initializes(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="telephony.audit"):
        logger = CallAuditLogger()
    assert logger.enabled is True
    assert any("Call audit logger initialized" in r.message for r in caplog.records)


def test_supported_events_log(caplog: pytest.LogCaptureFixture) -> None:
    audit = CallAuditLogger()
    with caplog.at_level(logging.INFO, logger="telephony.audit"):
        audit.log_event("call_started", {"purpose": "daily_practice"})
        audit.log_event("bootstrap_completed")
        audit.log_event("evaluation_completed", {"status": "scored"})
        audit.log_event("not_a_real_event")
    messages = [r.message for r in caplog.records]
    assert any("Audit event: call_started" in m for m in messages)
    assert any("Audit event: bootstrap_completed" in m for m in messages)
    assert any("Audit event: evaluation_completed" in m for m in messages)
    assert not any("not_a_real_event" in m for m in messages)


def test_metadata_sanitized() -> None:
    clean = sanitize_metadata(
        {
            "purpose": "daily_practice",
            "status": "calling",
            "provider": "livekit",
            "phone_number": "+919876543210",
            "learner_id": "u1",
            "learner_name": "Asha",
            "spoken_answer": "hello",
            "transcript": "full",
            "token": "secret",
            "api_key": "key",
            "optional": None,
        }
    )
    assert clean == {
        "purpose": "daily_practice",
        "provider": "livekit",
        "status": "calling",
    }


def test_log_event_helper_ignores_sensitive(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.INFO, logger="telephony.audit"):
        log_event(
            "call_started",
            {"purpose": "daily_practice", "phone_number": "+100"},
        )
    joined = " ".join(r.message for r in caplog.records)
    assert "phone_number" not in joined
    assert "+100" not in joined
    assert "daily_practice" in joined


def test_service_integration_audits_lifecycle(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(),
    )
    with caplog.at_level(logging.INFO, logger="telephony.audit"):
        result = service.place_call("9876543210", purpose="daily_practice")
        service.handle_call_outcome("answered")
    assert result.get("error") is not True
    joined = " ".join(r.message for r in caplog.records)
    assert "Audit event: call_started" in joined
    assert "Audit event: bootstrap_completed" in joined
    assert "Audit event: call_completed" in joined
    assert "Audit event: outcome_processed" in joined
    assert "9876543210" not in joined
