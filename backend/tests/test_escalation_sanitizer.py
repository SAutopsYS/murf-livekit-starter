"""Day 7 Phase 4: PII / sensitive-data sanitization."""

from __future__ import annotations

from typing import Any

import pytest

from escalation.notifier import EscalationNotifier
from escalation.repository import EscalationRepository
from escalation.sanitizer import EscalationSanitizer
from escalation.tools import create_escalation_request


@pytest.fixture()
def sanitizer() -> EscalationSanitizer:
    return EscalationSanitizer()


def test_normal_summary_remains_readable(sanitizer: EscalationSanitizer) -> None:
    text = "Learner requested help with past tense practice."
    assert sanitizer.sanitize_summary(text) == text


def test_otp_redacted(sanitizer: EscalationSanitizer) -> None:
    assert "[REDACTED]" in sanitizer.sanitize_summary("my OTP is 482913")
    assert "482913" not in sanitizer.sanitize_summary("my OTP is 482913")


def test_pin_redacted(sanitizer: EscalationSanitizer) -> None:
    assert "1234" not in sanitizer.sanitize_summary("my PIN is 1234")
    assert "[REDACTED]" in sanitizer.sanitize_summary("my PIN is 1234")


def test_password_redacted(sanitizer: EscalationSanitizer) -> None:
    result = sanitizer.sanitize_summary("password: hello123")
    assert "hello123" not in result
    assert "[REDACTED]" in result


def test_card_number_redacted(sanitizer: EscalationSanitizer) -> None:
    result = sanitizer.sanitize_summary("card number 4111 1111 1111 1111")
    assert "4111" not in result
    assert "[REDACTED]" in result


def test_long_numeric_identifier_redacted(sanitizer: EscalationSanitizer) -> None:
    result = sanitizer.sanitize_summary("account 123456789012")
    assert "123456789012" not in result
    assert "[REDACTED]" in result


def test_reference_id_and_fields_preserved(sanitizer: EscalationSanitizer) -> None:
    original = {
        "reference_id": "ESC-000001",
        "reason": "teacher_help",
        "summary": "Need help. OTP is 999888",
        "urgency": "medium",
        "language": "en",
        "status": "open",
        "transcript": "full conversation",
    }
    safe = sanitizer.sanitize_escalation(original)
    assert safe is not None
    assert safe["reference_id"] == "ESC-000001"
    assert safe["reason"] == "teacher_help"
    assert safe["urgency"] == "medium"
    assert safe["language"] == "en"
    assert safe["status"] == "open"
    assert "999888" not in safe["summary"]
    assert "transcript" not in safe
    assert set(safe.keys()) == {
        "reference_id",
        "reason",
        "summary",
        "urgency",
        "language",
        "status",
    }
    # Original object not modified.
    assert original["summary"] == "Need help. OTP is 999888"
    assert "transcript" in original


def test_notification_uses_sanitized_payload() -> None:
    captured: dict[str, Any] = {}

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url
        captured.update(payload)
        return True, 204

    notifier = EscalationNotifier(
        webhook_url="https://example.com/hook",
        poster=poster,
        sanitizer=EscalationSanitizer(),
    )
    notifier.send(
        {
            "reference_id": "ESC-000002",
            "reason": "learner_upset",
            "summary": "password: secret99",
            "urgency": "high",
            "language": "en",
            "status": "open",
        }
    )
    assert captured["reference_id"] == "ESC-000002"
    assert "secret99" not in captured["summary"]


def test_sanitization_failure_does_not_send_raw() -> None:
    class BrokenSanitizer(EscalationSanitizer):
        def sanitize_escalation(
            self, escalation: dict[str, Any]
        ) -> dict[str, Any] | None:
            del escalation
            return None

    calls: list[Any] = []

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        calls.append(payload)
        return True, 204

    notifier = EscalationNotifier(
        webhook_url="https://example.com/hook",
        poster=poster,
        sanitizer=BrokenSanitizer(),
    )
    result = notifier.send(
        {
            "reference_id": "ESC-000003",
            "reason": "teacher_help",
            "summary": "password: keep-secret",
            "urgency": "medium",
            "language": "en",
            "status": "open",
        }
    )
    assert result["notification"] == "unavailable"
    assert calls == []


def test_create_escalation_keeps_local_request_on_sanitize_failure() -> None:
    class BrokenSanitizer(EscalationSanitizer):
        def sanitize_escalation(
            self, escalation: dict[str, Any]
        ) -> dict[str, Any] | None:
            del escalation
            return None

    repo = EscalationRepository()
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need help.",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(
            webhook_url="https://example.com/hook",
            poster=lambda url, payload: (True, 204),
            sanitizer=BrokenSanitizer(),
        ),
    )
    assert result["notification"] == "unavailable"
    assert repo.get(result["reference_id"]) is not None
