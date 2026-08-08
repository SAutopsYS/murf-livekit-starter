"""LiveKit function tools for Learning & Literacy knowledge search."""

from __future__ import annotations

from typing import Any

from livekit.agents import RunContext, function_tool

from knowledge.search import search_knowledge


@function_tool()
async def search_learning_knowledge(
    context: RunContext,
    query: str,
) -> list[dict[str, Any]]:
    """Search the Learning & Literacy knowledge base.

    Returns structured matching entries. Returns an empty list when nothing
    matches. Does not generate spoken text and never fabricates information.

    Args:
        query: Learner question or topic about English learning.
    """
    del context
    results = search_knowledge(query)
    return [
        {
            "topic": entry["topic"],
            "title": entry["title"],
            "keywords": list(entry["keywords"]),
            "content": entry["content"],
        }
        for entry in results
    ]


KNOWLEDGE_TOOLS = [
    search_learning_knowledge,
]
