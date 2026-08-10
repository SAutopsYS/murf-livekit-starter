"""Day 5 Bonus 8: tool registry and capability discovery."""

from __future__ import annotations

from tools.registry import (
    get_tool,
    get_tool_registry,
    list_capabilities,
    list_categories,
    list_tools,
)


def test_registry_initializes_and_registers_learning_tools() -> None:
    registry = get_tool_registry()
    names = {tool["name"] for tool in registry.list_tools()}
    assert names == {
        "get_next_exercise",
        "score_spoken_answer",
        "recommend_next_practice",
    }


def test_metadata_retrieval() -> None:
    meta = get_tool("get_next_exercise")
    assert meta is not None
    assert meta["category"] == "exercise"
    assert meta["version"] == "1.0"
    assert "callable" not in meta


def test_category_and_capability_listing() -> None:
    categories = list_categories()
    capabilities = list_capabilities()
    assert "exercise" in categories
    assert "scoring" in categories
    assert "recommendation" in categories
    assert "exercise_lookup" in capabilities
    assert list_tools()
