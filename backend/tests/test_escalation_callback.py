"""Day 7 Phase 7: outbound callback after escalation resolution."""

from __future__ import annotations

from typing import Any

import pytest

from escalation.callback import CALLBACK_PURPOSE, EscalationCallbackManager
from escalation.notifier import EscalationNotifier
from escalation.repository import EscalationRepository
from escalation.status import EscalationStatusManager
from escalation.tools import create_escalation_request, prepare_resolution_callback_data
from telephony.bootstrap import ConversationBootstrap
from telephony.caller import normalize_phone_number


class FakeTelephony:
    """Minimal TelephonyService stand-in for callback tests."""

    def __init__(self, *, fail: bool = False, invalid_phone: bool = False) -> None:
        self.fail = fail
        self.invalid_phone = invalid_phone
        self.calls: list[dict[str, Any]] = []

    def prepare_call(
        self,
        phone_number: str,
        purpose: str,
        language: str = "en-IN",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "phone_number": phone_number,
                "purpose": purpose,
                "language": language,
                "metadata": metadata or {},
            }
        )
        if self.fail:
            return {"error": True, "message": "Telephony configuration unavailable."}
        if self.invalid_phone:
            return {"error": True, "message": "Invalid phone number."}
        # Reuse real phone validation for eligibility checks.
        normalized = normalize_phone_number(phone_number)
        if isinstance(normalized, dict) and normalized.get("error"):
            return normalized
        return {
            "phone_number": str(normalized),
            "purpose": purpose,
            "language": language,
            "status": "prepared",
        }


@pytest.fixture()
def repo() -> EscalationRepository:
    return EscalationRepository()


def _resolved(repo: EscalationRepository) -> str:
    created = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )
    EscalationStatusManager(repo).update_status(created["reference_id"], "resolved")
    return created["reference_id"]


def test_resolved_with_consent_prepares_callback(repo: EscalationRepository) -> None:
    reference_id = _resolved(repo)
    telephony = FakeTelephony()
    result = prepare_resolution_callback_data(
        reference_id=reference_id,
        callback_consent=True,
        phone_number="+919876543210",
        language="en-IN",
        repository=repo,
        telephony=telephony,
    )
    assert result == {
        "status": "prepared",
        "reference_id": reference_id,
        "purpose": CALLBACK_PURPOSE,
        "callback": {"status": "prepared", "language": "en-IN"},
    }
    assert "phone_number" not in result
    assert "phone_number" not in result["callback"]
    assert telephony.calls[0]["purpose"] == "escalation_resolution"


@pytest.mark.parametrize("status", ["open", "in_progress"])
def test_unresolved_rejected(repo: EscalationRepository, status: str) -> None:
    created = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )
    if status == "in_progress":
        EscalationStatusManager(repo).update_status(
            created["reference_id"],
            "in_progress",
        )
    result = EscalationCallbackManager(
        repo, FakeTelephony()
    ).prepare_resolution_callback(
        reference_id=created["reference_id"],
        callback_consent=True,
        phone_number="+919876543210",
    )
    assert result == {"error": True, "message": "Callback unavailable."}


def test_missing_escalation_rejected(repo: EscalationRepository) -> None:
    result = EscalationCallbackManager(
        repo, FakeTelephony()
    ).prepare_resolution_callback(
        reference_id="ESC-999999",
        callback_consent=True,
        phone_number="+919876543210",
    )
    assert result["error"] is True


def test_consent_false_rejected(repo: EscalationRepository) -> None:
    reference_id = _resolved(repo)
    telephony = FakeTelephony()
    result = EscalationCallbackManager(repo, telephony).prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=False,
        phone_number="+919876543210",
    )
    assert result["error"] is True
    assert telephony.calls == []


def test_invalid_phone_rejected(repo: EscalationRepository) -> None:
    reference_id = _resolved(repo)
    result = EscalationCallbackManager(
        repo, FakeTelephony()
    ).prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=True,
        phone_number="not-a-phone",
    )
    assert result == {"error": True, "message": "Callback unavailable."}


def test_existing_phone_validation_reused() -> None:
    ok = normalize_phone_number("9876543210")
    bad = normalize_phone_number("abc")
    assert isinstance(ok, str)
    assert isinstance(bad, dict) and bad.get("error") is True


def test_hindi_language_and_bootstrap_script() -> None:
    intro = ConversationBootstrap().build_intro(
        learner_name=None,
        purpose="escalation_resolution",
        language="hi-IN",
    )
    assert intro["purpose"] == "escalation_resolution"
    assert "नमस्ते" in intro["intro"]
    assert "VoiceForBharat Tutor" in intro["intro"]
    assert "Namaste" not in intro["intro"]
    assert "resolved" not in intro["intro"].lower()

    en = ConversationBootstrap().build_intro(
        None,
        "escalation_resolution",
        "en-IN",
    )["intro"]
    assert "resolved support request" in en.lower()
    assert "stop" in en.lower()


def test_no_duplicate_callback_preparation(repo: EscalationRepository) -> None:
    reference_id = _resolved(repo)
    telephony = FakeTelephony()
    manager = EscalationCallbackManager(repo, telephony)
    first = manager.prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=True,
        phone_number="+919876543210",
    )
    second = manager.prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=True,
        phone_number="+919876543210",
    )
    assert first.get("status") == "prepared"
    assert second == {"error": True, "message": "Callback unavailable."}
    assert len(telephony.calls) == 1


def test_telephony_failure_structured_error(repo: EscalationRepository) -> None:
    reference_id = _resolved(repo)
    result = EscalationCallbackManager(
        repo,
        FakeTelephony(fail=True),
    ).prepare_resolution_callback(
        reference_id=reference_id,
        callback_consent=True,
        phone_number="+919876543210",
    )
    assert result == {"error": True, "message": "Callback unavailable."}
