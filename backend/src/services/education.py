"""Teacher / student / parent experience. Wraps existing dashboards. No new scores store."""

from __future__ import annotations

from dataclasses import dataclass

from enterprise.intelligence import ParentDashboardService
from enterprise.platform import TeacherConsoleService
from salora_platform.auth import Role, can
from services.events import publish
from services.intelligence import LearningService, LearningSnapshot
from services.tenants import TenantService, WorkspaceRecord


@dataclass(frozen=True)
class ExperienceSnapshot:
    role: Role
    learning: LearningSnapshot
    source: str


class StudentService:
    def snapshot(self) -> ExperienceSnapshot:
        learning = LearningService().snapshot()
        publish("ProgressUpdated", phase=learning.phase)
        return ExperienceSnapshot("student", learning, "learning.service")

    def join(self) -> None:
        publish("StudentJoined")


class TeacherService:
    def console(self) -> dict[str, object]:
        raw = TeacherConsoleService().build()
        return raw if isinstance(raw, dict) else {}


class ParentService:
    def dashboard(self) -> dict[str, object]:
        raw = ParentDashboardService().build()
        publish("ParentNotified")
        return raw if isinstance(raw, dict) else {}


class ClassroomService:
    def open(self, organization_id: str, owner: str) -> WorkspaceRecord:
        return TenantService().workspaces.create(
            organization_id, "Classroom", "classroom", owner
        )


class ProgressService:
    def from_learning(self) -> LearningSnapshot:
        snap = LearningService().snapshot()
        if snap.phase != "new":
            publish("LessonCompleted", phase=snap.phase)
        return snap


class AssignmentService:
    def submit(self, title: str) -> dict[str, str]:
        publish("AssignmentSubmitted", title=title[:40])
        return {"title": title, "status": "architected"}


class AttendanceService:
    def spec(self) -> dict[str, bool]:
        return {"ui": False, "engine": True}


class EducationService:
    def __init__(self) -> None:
        self.students = StudentService()
        self.teachers = TeacherService()
        self.parents = ParentService()
        self.classrooms = ClassroomService()
        self.progress = ProgressService()
        self.assignments = AssignmentService()
        self.attendance = AttendanceService()

    def for_role(self, role: Role) -> ExperienceSnapshot:
        if role == "parent" and can(role, "enterprise.read"):
            return ExperienceSnapshot(role, LearningService().snapshot(), "parent")
        if role == "teacher" and can(role, "studio.access"):
            return ExperienceSnapshot(role, LearningService().snapshot(), "teacher")
        return self.students.snapshot()


class ExperienceMetrics:
    def from_learning(self) -> LearningSnapshot:
        return LearningService().snapshot()


class ExperiencePolicies:
    def spec(self) -> dict[str, object]:
        return {
            "scores_persist": False,
            "source": "learning+enterprise",
            "lazy_dashboards": True,
            "cached_dashboards": "process-local",
            "streaming_analytics": "architected",
        }


ExperienceEngine = EducationService
StudentExperience = StudentService
TeacherExperience = TeacherService
ParentExperience = ParentService
