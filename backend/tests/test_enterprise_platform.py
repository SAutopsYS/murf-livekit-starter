"""Enterprise learning intelligence, reports, gamification, language, health."""

from __future__ import annotations

from enterprise.intelligence import (
    ExecutionTraceService,
    LearningReportService,
    ParentDashboardService,
    ReplayService,
    VoiceAnalyticsService,
    build_simple_pdf,
)
from enterprise.journal import reset_journal
from enterprise.learning import LearningJourneyService
from enterprise.monitor import AgentPerformanceService, HealthMonitorService
from enterprise.orchestrator import AgentOrchestrator, reset_orchestrator
from enterprise.platform import (
    ControlCenterService,
    GamificationService,
    LanguageRoutingService,
    TeacherConsoleService,
    reset_gamification,
)
from specialists.registry import reset_specialist_registry


def setup_function() -> None:
    reset_specialist_registry()
    reset_orchestrator()
    reset_journal()
    reset_gamification()


def test_journey_and_parent_are_structured() -> None:
    journey = LearningJourneyService().build()
    assert "steps" in journey
    assert "streak" in journey
    parent = ParentDashboardService().build()
    assert "learning_streak" in parent
    assert "phone" not in parent
    assert "transcript" not in parent


def test_trace_replay_voice() -> None:
    AgentOrchestrator().decide("Help me with fractions")
    trace = ExecutionTraceService().build()
    assert trace["count"] >= 1
    replay = ReplayService().build()
    assert "frames" in replay
    voice = VoiceAnalyticsService().build()
    assert "speaking_ratio" in voice
    assert "transcript" not in voice


def test_report_json_and_pdf() -> None:
    report = LearningReportService().export_json()
    assert report["title"] == "AI Learning Report"
    assert "generated_at" in report
    pdf = LearningReportService().export_pdf()
    assert pdf.startswith(b"%PDF-1.4")
    tiny = build_simple_pdf("Test", ["Hello"])
    assert b"Hello" in tiny


def test_gamification_no_duplicate_award() -> None:
    service = GamificationService()
    first = service.snapshot()
    second = service.snapshot()
    assert first["xp"] == second["xp"]
    assert second["awarded_this_snapshot"] == 0


def test_teacher_hashes_ids() -> None:
    console = TeacherConsoleService().build()
    assert "students" in console
    blob = str(console)
    assert "password" not in blob
    assert "otp" not in blob


def test_language_native_scripts() -> None:
    service = LanguageRoutingService()
    hindi = service.detect("नमस्ते गणित")
    assert hindi["language"] == "hi"
    assert hindi["script"] == "Devanagari"
    assert hindi["romanized"] is False
    english = service.detect("Hello there")
    assert english["language"] == "en"
    assert hindi["murf_voice"] == "Anisha"


def test_health_and_control_center() -> None:
    health = HealthMonitorService().snapshot()
    assert "tutor" in health["components"]
    assert "math_specialist" in health["components"]
    perf = AgentPerformanceService().snapshot()
    assert "successful_handoffs" in perf
    center = ControlCenterService().snapshot()
    assert "graph" in center
    assert "timeline" in center
    assert "gamification" in center
    assert "ops" in center
    assert "transcript" not in str(center)
