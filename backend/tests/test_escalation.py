"""Day 7 Phase 1: human-help escalation foundation."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from escalation.models import EscalationRequest
from escalation.repository import EscalationRepository, reset_escalation_repository
from escalation.tools import create_escalation, create_escalation_request


@pytest.fixture(autouse=True)
def _clean_repo() -> None:
    reset_escalation_repository()
    yield
    reset_escalation_repository()


def _ctx() -> SimpleNamespace:
    return SimpleNamespace()


def test_teacher_help_escalation_created() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Learner requested help from a human teacher.",
        consent=True,
    )
    assert result.get("error") is not True
    assert result["reason"] == "teacher_help"
    assert result["status"] == "open"


def test_learner_upset_escalation_created() -> None:
    result = create_escalation_request(
        reason="learner_upset",
        summary="Learner is upset and asked for human help.",
        consent=True,
    )
    assert result.get("error") is not True
    assert result["reason"] == "learner_upset"
    assert result["status"] == "open"


def test_reference_id_generated() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help with grammar.",
        consent=True,
    )
    assert result["reference_id"].startswith("ESC-")
    assert len(result["reference_id"]) >= 10


def test_status_open_and_default_urgency() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help.",
        consent=True,
    )
    assert result["status"] == "open"
    assert result["urgency"] == "medium"


def test_structured_response_returned() -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher help.",
        consent=True,
    )
    assert "reference_id" in result
    assert "status" in result
    assert "message" in result
    assert result["message"] == "Human help request created."


def test_invalid_reason_handled_gracefully() -> None:
    result = create_escalation_request(
        reason="unknown_reason",
        summary="Something went wrong.",
        consent=True,
    )
    assert result == {
        "error": True,
        "message": "Unable to create human help request.",
    }


def test_repository_retrieve_and_list_open() -> None:
    repo = EscalationRepository()
    created = repo.create(
        reason="teacher_help",
        summary="Need help.",
        language="en",
    )
    fetched = repo.get(created.reference_id)
    assert fetched is not None
    assert fetched.reference_id == created.reference_id
    assert isinstance(fetched, EscalationRequest)

    open_items = repo.list_open()
    assert len(open_items) == 1
    assert open_items[0].reference_id == created.reference_id


@pytest.mark.asyncio
async def test_consent_granted_creates_escalation() -> None:
    result = await create_escalation(
        _ctx(),
        reason="teacher_help",
        summary="Learner asked for a teacher.",
        consent=True,
    )
    assert result.get("error") is not True
    assert result["reference_id"].startswith("ESC-")


@pytest.mark.asyncio
async def test_consent_denied_does_not_create() -> None:
    repo = reset_escalation_repository()
    result = await create_escalation(
        _ctx(),
        reason="teacher_help",
        summary="Learner asked for a teacher.",
        consent=False,
    )
    assert result["error"] is True
    assert repo.list_open() == []
