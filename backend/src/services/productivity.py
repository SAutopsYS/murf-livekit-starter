"""AI-native productivity. Wraps Studio documents/notebooks. No mail/calendar UI."""

from __future__ import annotations

from dataclasses import dataclass

from services.events import publish
from services.studio import DocumentService, NotebookService, StudioService


@dataclass(frozen=True)
class ProductivitySnapshot:
    notes: int
    tasks: int
    notebooks: int
    source: str


class TaskService:
    def create(self, title: str, owner: str) -> dict[str, str]:
        publish("TaskCreated", title=title[:40])
        return {"title": title, "owner": owner, "status": "open"}


class CalendarService:
    def spec(self) -> dict[str, bool]:
        return {"ui": False, "engine": True}


class MeetingService:
    def schedule(self, title: str) -> dict[str, str]:
        publish("MeetingScheduled", title=title[:40])
        return {"title": title, "status": "architected"}


class MailService:
    def spec(self) -> dict[str, bool]:
        return {"client": False, "engine": True}


class ResearchService:
    def summarize(self, title: str) -> dict[str, str]:
        publish("SummaryCreated", title=title[:40])
        return {"title": title, "kind": "ai_summary"}


class ProductivityService:
    def __init__(self) -> None:
        self.studio = StudioService()
        self.tasks = TaskService()
        self.calendar = CalendarService()
        self.meetings = MeetingService()
        self.mail = MailService()
        self.research = ResearchService()
        self.documents = DocumentService()
        self.notebooks = NotebookService()

    def snapshot(self, owner: str) -> ProductivitySnapshot:
        self.documents.create("Note", "notes", owner)
        self.notebooks.create("Research", owner)
        publish("DocumentGenerated", owner=owner)
        return ProductivitySnapshot(notes=1, tasks=0, notebooks=1, source="studio")
