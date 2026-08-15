"""AI service platform wraps existing modules. No second router or store."""

from __future__ import annotations

from salora_platform.config import clear_platform_config
from services.api import fail, ok, paginate
from services.events import publish, recent_events, reset_events, subscribe
from services.intelligence import (
    AdaptiveService,
    KnowledgeService,
    LearningService,
    VoiceService,
)
from services.jobs import job_for
from services.memory_graph import GraphQuery, MemoryGraphService
from services.orchestrator import AIOrchestrator
from services.providers import get_provider_registry
from services.studio import StudioService
from services.whiteboard import WhiteboardService


def setup_function() -> None:
    reset_events()
    clear_platform_config()


def test_voice_service_does_not_start_livekit() -> None:
    status = VoiceService().status()
    assert status.transport == "livekit"
    assert status.tts == "murf"
    assert status.stt == "deepgram"


def test_learning_and_knowledge_typed() -> None:
    learning = LearningService().snapshot()
    assert learning.source == "analytics+memory"
    assert learning.consented_profiles >= 0
    knowledge = KnowledgeService().search("english")
    assert knowledge.source == "knowledge.search"
    assert knowledge.count == len(knowledge.hits)


def test_adaptive_wraps_router() -> None:
    decision = AdaptiveService().decide("help me multiply fractions")
    assert decision.source == "specialist.router"
    assert decision.action in {"continue", "recommend_specialist"}


def test_provider_registry_future_disabled() -> None:
    registry = get_provider_registry(force_reload=True)
    assert registry.get("murf").live is True
    assert registry.get("claude").live is False
    assert registry.get("claude").health == "disabled"


def test_orchestrator_and_events() -> None:
    seen: list[str] = []
    subscribe("LearningUpdated", lambda event: seen.append(event.name))
    result = AIOrchestrator().run("learning")
    assert result.intent == "learning"
    assert result.ok is True
    assert "LearningUpdated" in seen or recent_events("LearningUpdated")


def test_api_contracts_and_jobs() -> None:
    envelope = ok({"phase": "new"})
    assert envelope.ok is True
    assert envelope.version == "v1"
    assert fail("X", "no", 400).ok is False
    page = paginate(list(range(5)), cursor=0, limit=2)
    assert len(page.items) == 2
    assert page.next_cursor == "2"
    assert job_for("embeddings").idempotent is True


def test_studio_whiteboard_graph_architecture() -> None:
    studio = StudioService()
    project = studio.projects.create("Demo", "teacher")
    assert project.kind == "project"
    assert studio.may_access("teacher") is True
    board = WhiteboardService()
    canvas = board.canvas.create("Board", "teacher")
    element = board.elements.add(canvas.id, "knowledge_ref", "teacher")
    assert element.canvas_id == canvas.id
    graph = MemoryGraphService()
    query = graph.queries.run(GraphQuery("english", limit=3))
    assert query.source == "knowledge.search"
    publish("GraphOpened")
    assert recent_events("GraphOpened")


def test_event_bus_redacts_forbidden_keys_and_long_values() -> None:
    publish("SearchStarted", transcript="should-drop", title="fractions")
    fields = recent_events("SearchStarted")[-1].fields
    assert "transcript" not in fields
    assert fields["title"] == "fractions"
    publish(
        "SearchStarted",
        body="this utterance contains a learner transcript dump",
    )
    assert "body" not in recent_events("SearchStarted")[-1].fields
