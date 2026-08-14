"""Enterprise orchestrator, graph, timeline, decisions, memory graph."""

from __future__ import annotations

import logging

from enterprise.journal import list_decisions, list_events, reset_journal
from enterprise.learning import DifficultyEngine, KnowledgeHeatmapService
from enterprise.orchestrator import AgentOrchestrator, reset_orchestrator
from enterprise.privacy import sanitize_payload
from enterprise.visualization import (
    DecisionService,
    ExecutionGraphService,
    MemoryGraphService,
    TimelineService,
)
from specialists.registry import reset_specialist_registry


def setup_function() -> None:
    reset_specialist_registry()
    reset_orchestrator()
    reset_journal()


def test_orchestrator_routes_math_with_confidence() -> None:
    decision = AgentOrchestrator().decide("Help me solve 24 x 18")
    assert decision["selected_agent"] == "math_specialist"
    assert decision["confidence"] >= 0.7
    assert decision["alternative"] == "tutor"
    assert "reason" in decision
    assert decision["status"] in {"routed", "fallback", "clarification"}


def test_orchestrator_fallback_for_science() -> None:
    decision = AgentOrchestrator().decide("What is photosynthesis?")
    assert decision["selected_agent"] == "tutor"
    assert decision["confidence"] < 0.4


def test_graph_and_timeline_from_real_events() -> None:
    AgentOrchestrator().decide("Let's practice multiplication")
    graph = ExecutionGraphService().build()
    assert any(node["id"] == "tutor" for node in graph["nodes"])
    assert graph["edges"]
    timeline = TimelineService().build()
    assert timeline["count"] >= 1
    assert timeline["items"][0]["timestamp"]


def test_decision_metadata_has_no_transcript() -> None:
    AgentOrchestrator().decide("fractions please. OTP 111222")
    payload = DecisionService().list_recent()
    blob = str(payload)
    assert "111222" not in blob
    assert "transcript" not in blob
    first = payload["decisions"][-1]
    assert "rejected" in first
    assert "intent" in first


def test_memory_graph_read_only() -> None:
    graph = MemoryGraphService().build()
    ids = {node["id"] for node in graph["nodes"]}
    assert "language" in ids
    assert "grade" in ids
    assert "transcript" not in str(graph)


def test_difficulty_is_deterministic() -> None:
    first = DifficultyEngine().evaluate(
        accuracy=0.9, completion_rate=0.8, current="medium"
    )
    second = DifficultyEngine().evaluate(
        accuracy=0.9, completion_rate=0.8, current="medium"
    )
    assert first == second
    assert first["difficulty"] == "hard"
    low = DifficultyEngine().evaluate(
        accuracy=0.2, completion_rate=0.2, current="medium"
    )
    assert low["difficulty"] == "easy"


def test_heatmap_uses_known_topics() -> None:
    heat = KnowledgeHeatmapService().build()
    topics = {cell["topic"] for cell in heat["cells"]}
    assert "fractions" in topics
    assert "geometry" in topics


def test_privacy_sanitize_drops_secrets() -> None:
    clean = sanitize_payload({"otp": "999", "phone": "999", "topic": "math"})
    assert "otp" not in clean
    assert clean["topic"] == "math"


def test_journal_privacy_logs(caplog: logging.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="specialists.events"):
        AgentOrchestrator().decide("password 12345 multiplication")
    text = " ".join(record.getMessage() for record in caplog.records)
    assert "12345" not in text
    assert list_events()
    assert list_decisions()
