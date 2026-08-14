"""Day 9 Bonus 2: specialist metadata, registry, and health."""

from __future__ import annotations

import logging

import pytest

from specialists.registry import (
    MATH_SPECIALIST_ID,
    SpecialistSpec,
    disable_specialist,
    discover_capabilities,
    enable_specialist,
    get_specialist,
    get_specialist_registry,
    list_active_specialists,
    list_disabled_specialists,
    register_specialist,
    reset_specialist_registry,
    unregister_specialist,
)
from specialists.router import SpecialistRouter
from specialists.schemas import RouteTarget


@pytest.fixture(autouse=True)
def _reset_registry() -> None:
    reset_specialist_registry()
    yield
    reset_specialist_registry()


def test_registry_operations() -> None:
    register_specialist(
        SpecialistSpec(
            specialist_id="temp_spec",
            name="Temp",
            track="learning_and_literacy",
            active=False,
            enabled=False,
        )
    )
    assert get_specialist("temp_spec") is not None
    assert unregister_specialist("temp_spec") is True
    assert get_specialist("temp_spec") is None


def test_enable_and_disable_specialist() -> None:
    assert disable_specialist(MATH_SPECIALIST_ID) is True
    assert get_specialist(MATH_SPECIALIST_ID)["enabled"] is False
    assert enable_specialist(MATH_SPECIALIST_ID) is True
    assert get_specialist(MATH_SPECIALIST_ID)["enabled"] is True


def test_active_and_disabled_listing() -> None:
    active = list_active_specialists()
    disabled = list_disabled_specialists()
    assert {item["specialist_id"] for item in active} == {MATH_SPECIALIST_ID}
    assert "english_specialist" in {item["specialist_id"] for item in disabled}


def test_metadata_validation() -> None:
    meta = get_specialist(MATH_SPECIALIST_ID)
    assert meta is not None
    assert meta["display_name"] == "Math Practice Specialist"
    assert meta["version"] == "1.0"
    assert "fractions" in meta["supported_topics"]
    assert "en" in meta["supported_languages"]
    assert meta["enabled"] is True


def test_health_status() -> None:
    registry = get_specialist_registry()
    assert registry.health(MATH_SPECIALIST_ID) == "READY"
    assert registry.set_health(MATH_SPECIALIST_ID, "BUSY") is True
    assert registry.health(MATH_SPECIALIST_ID) == "BUSY"
    assert registry.health("english_specialist") == "DISABLED"


def test_router_ignores_disabled_and_falls_back() -> None:
    disable_specialist(MATH_SPECIALIST_ID)
    result = SpecialistRouter().route("Let's practice multiplication")
    assert result["target"] == RouteTarget.MAIN_AGENT.value
    assert result["fallback_used"] is True


def test_capability_discovery() -> None:
    caps = discover_capabilities()
    assert caps["count"] == 1
    assert caps["specialists"][0]["specialist_id"] == MATH_SPECIALIST_ID
    assert "English Specialist" not in caps["message"]


def test_privacy_safe_registry_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        disable_specialist(MATH_SPECIALIST_ID)
        enable_specialist(MATH_SPECIALIST_ID)
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "Disable" in text
    assert "Enable" in text
    assert "password" not in text.lower()
