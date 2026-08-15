"""Production platform: config, RBAC, privacy logs, health."""

from __future__ import annotations

import json
import logging

import pytest

from salora_platform.auth import authorize, can, role_from_enterprise_ui
from salora_platform.config import clear_platform_config, get_platform_config
from salora_platform.errors import platform_error
from salora_platform.health import check_liveness, check_readiness, main
from salora_platform.observability import emit, reset_metrics
from salora_platform.security import PRIVACY_RULES, valid_date, valid_token


@pytest.fixture(autouse=True)
def _reset(monkeypatch: pytest.MonkeyPatch):
    clear_platform_config()
    reset_metrics()
    for key in (
        "SALORA_PROFILE",
        "AUTH_REQUIRED",
        "SALORA_AUTH_SECRET",
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "MURF_API_KEY",
        "DEEPGRAM_API_KEY",
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_platform_config()
    reset_metrics()


def test_config_defaults_to_development() -> None:
    config = get_platform_config(force_reload=True)
    assert config.profile == "development"
    assert config.auth_required is False
    assert config.livekit_ready is False


def test_config_reads_existing_env_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SALORA_PROFILE", "staging")
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("MURF_API_KEY", "murf")
    monkeypatch.setenv("DEEPGRAM_API_KEY", "dg")
    monkeypatch.setenv("GOOGLE_API_KEY", "g")
    config = get_platform_config(force_reload=True)
    assert config.profile == "staging"
    assert config.livekit_ready is True
    assert config.murf_ready is True
    assert config.llm_ready is True


def test_rbac_anonymous_voice_only() -> None:
    assert can("anonymous", "voice.session") is True
    assert can("anonymous", "analytics.read") is False
    assert can("enterprise_admin", "enterprise.admin") is True
    assert role_from_enterprise_ui("admin") == "enterprise_admin"


def test_authorize_open_when_auth_optional() -> None:
    allowed, status = authorize("guest", "analytics.read", auth_required=False)
    assert allowed is True
    assert status == 200
    allowed, status = authorize("guest", "analytics.read", auth_required=True)
    assert allowed is False
    assert status == 403


def test_privacy_rules_and_validation() -> None:
    assert PRIVACY_RULES["no_utterance_fields"] is True
    assert valid_token("7d") is True
    assert valid_token("bad token") is False
    assert valid_date("2026-08-15") is True
    assert valid_date("15/08/2026") is False


def test_emit_redacts_secrets(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="salora.platform")
    emit("info", "test", api_key="should-not-appear", route="analytics")
    joined = " ".join(record.message for record in caplog.records)
    assert "should-not-appear" not in joined
    assert "analytics" in joined or "test" in joined


def test_health_liveness_and_degraded_readiness() -> None:
    live = check_liveness()
    assert live["status"] == "ok"
    ready = check_readiness()
    assert ready["status"] == "degraded"
    assert main([]) == 0
    assert main(["--ready"]) == 1


def test_health_ready_when_providers_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("MURF_API_KEY", "murf")
    monkeypatch.setenv("DEEPGRAM_API_KEY", "dg")
    monkeypatch.setenv("GOOGLE_API_KEY", "g")
    clear_platform_config()
    payload = check_readiness()
    assert payload["status"] == "ready"
    assert json.loads(json.dumps(payload))["checks"]["livekit"] is True


def test_typed_errors() -> None:
    error = platform_error("AUTH_FORBIDDEN")
    assert error.status == 403
    assert error.retryable is False
