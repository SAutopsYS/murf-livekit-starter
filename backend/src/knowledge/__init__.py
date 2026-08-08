"""Learning & Literacy knowledge base (JSON + keyword search)."""

from knowledge.search import search_knowledge
from knowledge.tools import KNOWLEDGE_TOOLS, search_learning_knowledge

__all__ = [
    "KNOWLEDGE_TOOLS",
    "search_knowledge",
    "search_learning_knowledge",
]
