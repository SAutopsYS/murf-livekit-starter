"""Day 7 Phase 2: Discord/webhook escalation notifications."""

from __future__ import annotations

import logging
from typing import Any

import pytest

from escalation.notifier import EscalationNotifier
from escalation.repository import reset_escalation_repository
from escalation.tools import create_escalation_request


@pytest.fixture(autouse=True)
def _clean_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_escalation_repository()
    monkeypatch.delenv("ESCALATION_WEBHOOK_URL", raising=False)
    yield
    reset_escalation_repository()


def test_webhook_configuration_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ESCALATION_WEBHOOK_URL", "https://example.com/hook")
    notifier = EscalationNotifier()
    assert notifier.configured is True


def test_valid_notification_succeeds() -> None:
    calls: list[dict[str, Any]] = []

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        calls.append({"url": url, "payload": payload})
        return True, 204

    notifier = EscalationNotifier(
        webhook_url="https://example.com/hook",
        poster=poster,
    )
    result = notifier.send(
        {
            "reference_id": "ESC-000001",
            "reason": "teacher_help",
            "summary": "Learner requested help from a human teacher.",
            "urgency": "medium",
            "language": "en",
            "status": "open",
        }
    )
    assert result["notification"] == "delivered"
    assert len(calls) == 1
    assert set(calls[0]["payload"].keys()) == {
        "reference_id",
        "reason",
        "summary",
        "urgency",
        "language",
        "status",
    }


def test_missing_webhook_handled_gracefully() -> None:
    notifier = EscalationNotifier(webhook_url="")
    result = notifier.send(
        {
            "reference_id": "ESC-000001",
            "reason": "teacher_help",
            "summary": "Need help.",
            "urgency": "medium",
            "language": "en",
            "status": "open",
        }
    )
    assert result["notification"] == "unavailable"


def test_http_failure_handled_gracefully() -> None:
    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url, payload
        raise TimeoutError("network down")

    notifier = EscalationNotifier(
        webhook_url="https://example.com/hook",
        poster=poster,
    )
    result = notifier.send(
        {
            "reference_id": "ESC-000001",
            "reason": "teacher_help",
            "summary": "Need help.",
            "urgency": "medium",
            "language": "en",
            "status": "open",
        }
    )
    assert result["notification"] == "unavailable"


def test_payload_contains_only_approved_fields() -> None:
    captured: dict[str, Any] = {}

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url
        captured.update(payload)
        return True, 200

    notifier = EscalationNotifier(
        webhook_url="https://example.com/hook",
        poster=poster,
    )
    notifier.send(
        {
            "reference_id": "ESC-000001",
            "reason": "teacher_help",
            "summary": "Need help.",
            "urgency": "medium",
            "language": "en",
            "status": "open",
            "transcript": "should not send",
            "password": "secret",
        }
    )
    assert "transcript" not in captured
    assert "password" not in captured
    assert captured["reference_id"] == "ESC-000001"


def test_secrets_never_included_in_logs(caplog: pytest.LogCaptureFixture) -> None:
    webhook = "https://discord.com/api/webhooks/secret-token-123"

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url, payload
        return True, 204

    notifier = EscalationNotifier(webhook_url=webhook, poster=poster)
    with caplog.at_level(logging.INFO, logger="escalation.notifier"):
        notifier.send(
            {
                "reference_id": "ESC-000001",
                "reason": "teacher_help",
                "summary": "Need help.",
                "urgency": "medium",
                "language": "en",
                "status": "open",
            }
        )
    joined = " ".join(record.getMessage() for record in caplog.records)
    assert "secret-token-123" not in joined
    assert webhook not in joined


def test_escalation_remains_when_notification_fails() -> None:
    from escalation.repository import EscalationRepository

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url, payload
        return False, 500

    repo = EscalationRepository()
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help.",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(
            webhook_url="https://example.com/hook",
            poster=poster,
        ),
    )
    assert result["notification"] == "unavailable"
    assert result["status"] == "open"
    assert result["reference_id"].startswith("ESC-")
    fetched = repo.get(result["reference_id"])
    assert fetched is not None
    assert fetched.reference_id == result["reference_id"]
