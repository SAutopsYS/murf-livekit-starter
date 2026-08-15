"""Memory Graph services. Knowledge Fabric / enterprise graph stay source of truth."""

from __future__ import annotations

from dataclasses import dataclass

from knowledge.search import search_knowledge
from services.events import publish
from services.intelligence import GraphProjectionService


@dataclass(frozen=True)
class GraphQuery:
    text: str
    limit: int = 8


@dataclass(frozen=True)
class GraphQueryResult:
    titles: tuple[str, ...]
    count: int
    source: str


class NodeService:
    def from_enterprise(self) -> dict[str, object]:
        return GraphProjectionService().build()


class RelationshipService:
    """Reuse Knowledge Fabric kinds. No second model."""

    KINDS = (
        "depends_on",
        "related_to",
        "teaches",
        "corrects",
        "improves",
        "contradicts",
        "supports",
        "derived_from",
        "recommended_by",
        "belongs_to",
    )


class GraphQueryService:
    def run(self, query: GraphQuery) -> GraphQueryResult:
        rows = (
            search_knowledge(query.text, limit=query.limit)
            if query.text.strip()
            else []
        )
        titles = tuple(row["title"] for row in rows)
        publish("QueryExecuted", count=len(titles))
        return GraphQueryResult(
            titles=titles, count=len(titles), source="knowledge.search"
        )


class ClusterService:
    def empty(self) -> dict[str, int]:
        return {"clusters": 0}


class BookmarkService:
    def create(self, node_id: str) -> dict[str, str]:
        publish("BookmarkCreated", id=node_id)
        return {"id": node_id}


class GraphExportService:
    def export(self, fmt: str) -> dict[str, str]:
        publish("GraphExported", format=fmt)
        return {"format": fmt, "status": "architected"}


class KnowledgeExplorerService:
    def open(self) -> dict[str, str]:
        publish("GraphOpened")
        return {"status": "open", "source": "knowledge-fabric"}


class MemoryGraphService:
    def __init__(self) -> None:
        self.nodes = NodeService()
        self.relationships = RelationshipService()
        self.queries = GraphQueryService()
        self.clusters = ClusterService()
        self.bookmarks = BookmarkService()
        self.exports = GraphExportService()
        self.explorer = KnowledgeExplorerService()
