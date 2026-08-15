"""AI Studio services. Architecture + in-memory persistence. No editor."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import time
from typing import Literal
from uuid import uuid4

from salora_platform.auth import Role, can
from services.events import publish
from services.repositories import InMemoryDocumentStore

ProjectKind = Literal[
    "project",
    "workspace",
    "folder",
    "asset",
    "document",
    "prompt",
    "conversation",
    "notebook",
    "workflow",
    "template",
]
DocumentKind = Literal[
    "markdown",
    "rich_text",
    "whiteboard_ref",
    "code",
    "notes",
    "ai_output",
    "prompt",
    "research",
    "summary",
    "transcript_ref",
]
WorkflowKind = Literal[
    "draft",
    "review",
    "improve",
    "translate",
    "explain",
    "summarize",
    "brainstorm",
    "generate",
    "analyze",
    "research",
]


@dataclass
class StudioRecord:
    id: str
    title: str
    kind: str
    owner: str
    organization: str | None
    permissions: tuple[str, ...]
    tags: tuple[str, ...]
    created_at: float
    updated_at: float
    metadata: dict[str, str] = field(default_factory=dict)


def _now() -> float:
    return time()


def _from_row(raw: dict) -> StudioRecord:
    return StudioRecord(
        id=str(raw["id"]),
        title=str(raw["title"]),
        kind=str(raw["kind"]),
        owner=str(raw["owner"]),
        organization=raw.get("organization"),
        permissions=tuple(raw.get("permissions") or ()),
        tags=tuple(raw.get("tags") or ()),
        created_at=float(raw["created_at"]),
        updated_at=float(raw["updated_at"]),
        metadata=dict(raw.get("metadata") or {}),
    )


def _record(
    title: str, kind: str, owner: str, organization: str | None = None
) -> StudioRecord:
    stamp = _now()
    return StudioRecord(
        id=f"{kind}_{uuid4().hex[:10]}",
        title=title,
        kind=kind,
        owner=owner,
        organization=organization,
        permissions=("studio.access",),
        tags=(),
        created_at=stamp,
        updated_at=stamp,
    )


class ProjectService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()

    def create(
        self, title: str, owner: str, organization: str | None = None
    ) -> StudioRecord:
        record = _record(title, "project", owner, organization)
        self._store.put(record.id, asdict(record))
        publish("ProjectCreated", id=record.id)
        return record

    def get(self, project_id: str) -> StudioRecord | None:
        raw = self._store.get(project_id)
        return _from_row(raw) if raw else None

    def list(self) -> list[StudioRecord]:
        return [
            _from_row(row) for row in self._store.list() if row.get("kind") == "project"
        ]


class DocumentService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()

    def create(self, title: str, kind: DocumentKind, owner: str) -> StudioRecord:
        record = _record(title, kind, owner)
        self._store.put(record.id, asdict(record))
        publish("DocumentUpdated", id=record.id)
        return record


class WorkflowService:
    def start(self, kind: WorkflowKind, owner: str) -> StudioRecord:
        record = _record(kind, "workflow", owner)
        publish("WorkflowStarted", id=record.id, kind=kind)
        return record

    def finish(self, record: StudioRecord) -> StudioRecord:
        publish("WorkflowFinished", id=record.id)
        return record


class PromptService:
    def execute(self, template_id: str, owner: str) -> StudioRecord:
        record = _record(template_id, "prompt", owner)
        publish("PromptExecuted", id=record.id)
        return record


class AssetService:
    def import_asset(self, title: str, owner: str) -> StudioRecord:
        record = _record(title, "asset", owner)
        publish("AssetImported", id=record.id)
        return record


class NotebookService:
    def create(self, title: str, owner: str) -> StudioRecord:
        record = _record(title, "notebook", owner)
        publish("NotebookCreated", id=record.id)
        return record


class TemplateService:
    def apply(self, title: str, owner: str) -> StudioRecord:
        record = _record(title, "template", owner)
        publish("TemplateApplied", id=record.id)
        return record


class StudioService:
    def __init__(self) -> None:
        self.projects = ProjectService()
        self.documents = DocumentService()
        self.workflows = WorkflowService()
        self.prompts = PromptService()
        self.assets = AssetService()
        self.notebooks = NotebookService()
        self.templates = TemplateService()

    def may_access(self, role: Role) -> bool:
        return can(role, "studio.access")
