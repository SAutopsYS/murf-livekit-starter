"""AI Mentor suite. Every mentor is an Agent Runtime consumer. Router stays authority."""

from __future__ import annotations

from dataclasses import dataclass

from services.agent_runtime import AgentKind, AgentManifest, AgentRuntimeService
from services.events import publish

MENTOR_KINDS: tuple[AgentKind, ...] = (
    "tutor",
    "coding",
    "career",
    "interview",
    "language",
    "writing",
    "research",
    "math",
)


@dataclass(frozen=True)
class MentorSession:
    agent_id: str
    kind: AgentKind
    live: bool
    source: str


class MentorRegistry:
    def __init__(self) -> None:
        self._runtime = AgentRuntimeService()

    def list(self) -> list[AgentManifest]:
        return [
            item for item in self._runtime.registry.list() if item.kind in MENTOR_KINDS
        ]


class TutorService:
    def start(self) -> MentorSession:
        publish("MentorStarted", kind="tutor")
        return MentorSession("agent.tutor", "tutor", True, "agent.runtime")


class CodingMentorService:
    def start(self) -> MentorSession:
        return MentorSession("agent.coding", "coding", False, "agent.runtime")


class CareerService:
    def start(self) -> MentorSession:
        return MentorSession("agent.career", "career", False, "agent.runtime")


class LanguageService:
    def start(self) -> MentorSession:
        return MentorSession("agent.language", "language", False, "agent.runtime")


class ResearchService:
    def start(self) -> MentorSession:
        return MentorSession("agent.research", "research", False, "agent.runtime")


class MentorService:
    def __init__(self) -> None:
        self.registry = MentorRegistry()
        self.tutor = TutorService()
        self.coding = CodingMentorService()
        self.career = CareerService()
        self.language = LanguageService()
        self.research = ResearchService()
        self._runtime = AgentRuntimeService()

    def recommend(self, text: str) -> dict[str, object]:
        rec = self._runtime.execution.recommend(text)
        publish("RecommendationGenerated", target=str(rec.get("target")))
        publish("MentorCompleted", target=str(rec.get("target")))
        return rec


class MentorMetrics:
    def live(self) -> tuple[str, ...]:
        return ("tutor", "math")


class MentorPolicies:
    def spec(self) -> dict[str, object]:
        return {
            "autonomous": False,
            "router": "specialist.router",
            "voice": "one_path",
        }


MentorEngine = MentorService
MentorProvider = MentorService
