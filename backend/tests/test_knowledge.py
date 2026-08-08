"""Day 4 Phase 8: knowledge base repository, search, and tool tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent import AGENT_TOOLS, SYSTEM_PROMPT
from knowledge.repository import clear_cache, get_all_entries, load_entries
from knowledge.search import search_knowledge
from knowledge.tools import KNOWLEDGE_TOOLS, search_learning_knowledge


@pytest.fixture(autouse=True)
def _reset_knowledge_cache():
    clear_cache()
    yield
    clear_cache()


def test_json_loads_and_cache_hit() -> None:
    first = load_entries()
    assert len(first) >= 6
    assert all("title" in entry and "content" in entry for entry in first)

    second = load_entries()
    assert second == first
    assert get_all_entries() == first


def test_search_returns_expected_entries() -> None:
    grammar = search_knowledge("present simple grammar")
    assert grammar
    assert any("Present Simple" in entry["title"] for entry in grammar)
    assert len(grammar) <= 3

    vocab = search_knowledge("vocabulary words")
    assert vocab
    assert any(entry["topic"] == "vocabulary" for entry in vocab)


def test_unknown_query_returns_empty_list() -> None:
    assert search_knowledge("quantum astrophysics calculus") == []
    assert search_knowledge("   ") == []


@pytest.mark.asyncio
async def test_search_tool_returns_structured_results() -> None:
    results = await search_learning_knowledge(object(), query="pronunciation tips")
    assert isinstance(results, list)
    assert results
    assert "content" in results[0]
    assert "title" in results[0]

    empty = await search_learning_knowledge(object(), query="mars rocket engines")
    assert empty == []


def test_knowledge_tool_registered() -> None:
    tool_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in KNOWLEDGE_TOOLS
    ]
    assert "search_learning_knowledge" in tool_names

    agent_tool_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in AGENT_TOOLS
    ]
    assert "search_learning_knowledge" in agent_tool_names
    assert "lookup_user" in agent_tool_names

    assert "Use the knowledge search tool first" in SYSTEM_PROMPT
    assert (
        Path(__file__).resolve().parents[1]
        / "src"
        / "knowledge"
        / "resources"
        / "english_basics.json"
    ).exists()
