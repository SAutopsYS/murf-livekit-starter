"""Whiteboard services. Architecture only. No renderer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import time
from typing import Literal
from uuid import uuid4

from services.events import publish
from services.repositories import InMemoryDocumentStore

ElementKind = Literal[
    "text",
    "sticky",
    "shape",
    "image",
    "code",
    "markdown",
    "table",
    "diagram",
    "equation",
    "ai_block",
    "voice_block",
    "knowledge_ref",
    "document_ref",
    "workflow_ref",
]

# Same kinds as Knowledge Fabric. No second relationship system.
RelationKind = Literal[
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
]


@dataclass
class CanvasRecord:
    id: str
    title: str
    owner: str
    created_at: float
    updated_at: float
    layers: tuple[str, ...] = ("default",)
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ElementRecord:
    id: str
    canvas_id: str
    type: ElementKind
    bounds: tuple[float, float, float, float]
    owner: str
    created_at: float
    updated_at: float
    metadata: dict[str, str] = field(default_factory=dict)


class CanvasService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()

    def create(self, title: str, owner: str) -> CanvasRecord:
        stamp = time()
        record = CanvasRecord(
            id=f"canvas_{uuid4().hex[:10]}",
            title=title,
            owner=owner,
            created_at=stamp,
            updated_at=stamp,
        )
        self._store.put(record.id, asdict(record))
        publish("CanvasCreated", id=record.id)
        return record

    def get(self, canvas_id: str) -> CanvasRecord | None:
        raw = self._store.get(canvas_id)
        if not raw:
            return None
        return CanvasRecord(
            id=str(raw["id"]),
            title=str(raw["title"]),
            owner=str(raw["owner"]),
            created_at=float(raw["created_at"]),
            updated_at=float(raw["updated_at"]),
            layers=tuple(raw.get("layers") or ("default",)),
            metadata=dict(raw.get("metadata") or {}),
        )


class ElementService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()

    def add(self, canvas_id: str, kind: ElementKind, owner: str) -> ElementRecord:
        stamp = time()
        record = ElementRecord(
            id=f"el_{uuid4().hex[:10]}",
            canvas_id=canvas_id,
            type=kind,
            bounds=(0, 0, 160, 80),
            owner=owner,
            created_at=stamp,
            updated_at=stamp,
        )
        self._store.put(record.id, asdict(record))
        publish("ElementAdded", id=record.id, canvas=canvas_id)
        return record


class DiagramService:
    def generate_spec(self, canvas_id: str) -> dict[str, str]:
        publish("DiagramGenerated", canvas=canvas_id)
        return {"canvas_id": canvas_id, "status": "architected", "renderer": "none"}


class SelectionService:
    def select(self, element_id: str) -> dict[str, str]:
        publish("SelectionChanged", id=element_id)
        return {"selected": element_id}


class HistoryService:
    def record(self, canvas_id: str, action: str) -> dict[str, str]:
        publish("HistoryRecorded", canvas=canvas_id, action=action)
        return {"canvas_id": canvas_id, "action": action}


class ExportService:
    def export(self, canvas_id: str, fmt: str) -> dict[str, str]:
        publish("BoardExported", canvas=canvas_id, format=fmt)
        return {"canvas_id": canvas_id, "format": fmt, "status": "architected"}


class ImportService:
    def import_spec(self, fmt: str) -> dict[str, str]:
        return {"format": fmt, "status": "architected"}


class WhiteboardService:
    def __init__(self) -> None:
        store = InMemoryDocumentStore()
        self.canvas = CanvasService(store)
        self.elements = ElementService(store)
        self.diagrams = DiagramService()
        self.selection = SelectionService()
        self.history = HistoryService()
        self.exports = ExportService()
        self.imports = ImportService()
