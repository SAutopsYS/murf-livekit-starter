"""Day 7 Phase 3: escalation urgency levels."""

from __future__ import annotations

from typing import Any

import pytest

from escalation.models import determine_urgency
from escalation.notifier import EscalationNotifier
from escalation.repository import reset_escalation_repository
from escalation.tools import create_escalation_request


@pytest.fixture(autouse=True)
def _clean_repo() -> None:
    reset_escalation_repository()
    yield
    reset_escalation_repository()


@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        ("teacher_help", "medium"),
        ("learner_upset", "high"),
        ("urgent_teacher_help", "high"),
        ("emergency", "emergency"),
        ("unknown_reason", "medium"),
    ],
)
def test_determine_urgency_rules(reason: str, expected: str) -> None:
    assert determine_urgency(reason) == expected


def test_explicit_urgency_respected() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need help soon.",
        urgency="high",
        consent=True,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert result["urgency"] == "high"


def test_invalid_urgency_falls_back_to_medium_for_teacher_help() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need help.",
        urgency="not-a-level",
        consent=True,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert result["urgency"] == "medium"


def test_notification_and_response_include_urgency() -> None:
    captured: dict[str, Any] = {}

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url
        captured.update(payload)
        return True, 204

    result = create_escalation_request(
        reason="learner_upset",
        summary="Learner is upset and asked for a teacher.",
        consent=True,
        notifier=EscalationNotifier(
            webhook_url="https://example.com/hook",
            poster=poster,
        ),
    )
    assert result["urgency"] == "high"
    assert result["reason"] == "learner_upset"
    assert captured["urgency"] == "high"


def test_backward_compatible_without_urgency_arg() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help.",
        consent=True,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert result["urgency"] == "medium"
    assert result["status"] == "open"
