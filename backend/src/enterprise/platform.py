"""Gamification, teacher console, language routing, and control center."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from analytics.service import get_analytics_service
from enterprise.intelligence import (
    ExecutionTraceService,
    LearningReportService,
    ParentDashboardService,
    ReplayService,
    VoiceAnalyticsService,
)
from enterprise.journal import list_notifications
from enterprise.learning import (
    DifficultyEngine,
    KnowledgeHeatmapService,
    LearningJourneyService,
)
from enterprise.monitor import (
    AgentPerformanceService,
    HealthMonitorService,
    ProductionMonitoringService,
)
from enterprise.orchestrator import FUTURE_PLACEHOLDERS, TUTOR_ID, get_orchestrator
from enterprise.privacy import sanitize_payload
from enterprise.visualization import (
    DecisionService,
    ExecutionGraphService,
    MemoryGraphService,
    TimelineService,
)
from memory.repository import list_users
from specialists.metrics import get_specialist_metrics

LEVELS = (
    (0, "Beginner"),
    (50, "Explorer"),
    (120, "Scholar"),
    (220, "Master"),
    (360, "Champion"),
    (520, "Legend"),
)

LANGUAGE_SCRIPTS = {
    "en": ("English", "Latin", "Anisha"),
    "hi": ("Hindi", "Devanagari", "Anisha"),
    "gu": ("Gujarati", "Gujarati", "Anisha"),
    "mr": ("Marathi", "Devanagari", "Anisha"),
    "ta": ("Tamil", "Tamil", "Anisha"),
    "te": ("Telugu", "Telugu", "Anisha"),
    "kn": ("Kannada", "Kannada", "Anisha"),
    "ml": ("Malayalam", "Malayalam", "Anisha"),
    "pa": ("Punjabi", "Gurmukhi", "Anisha"),
    "bn": ("Bengali", "Bengali", "Anisha"),
}

_SCRIPT_RANGES = (
    ("hi", (0x0900, 0x097F)),
    ("gu", (0x0A80, 0x0AFF)),
    ("pa", (0x0A00, 0x0A7F)),
    ("ta", (0x0B80, 0x0BFF)),
    ("te", (0x0C00, 0x0C7F)),
    ("kn", (0x0C80, 0x0CFF)),
    ("ml", (0x0D00, 0x0D7F)),
    ("bn", (0x0980, 0x09FF)),
)

_AWARDED: set[str] = set()


def reset_gamification() -> None:
    _AWARDED.clear()


def _hash_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:10]


def _level_for_xp(xp: int) -> str:
    label = LEVELS[0][1]
    for threshold, name in LEVELS:
        if xp >= threshold:
            label = name
    return label


class GamificationService:
    def snapshot(self) -> dict[str, Any]:
        specialist = get_specialist_metrics()
        analytics = get_analytics_service().get_summary()
        if isinstance(analytics, dict) and analytics.get("error"):
            analytics = {"successful_calls": 0, "total_calls": 0}
        exercises = int(specialist.get("exercises_completed") or 0)
        successes = int(analytics.get("successful_calls") or 0)
        handoffs = int(specialist.get("successful_handoffs") or 0)
        key = f"xp:{exercises}:{successes}:{handoffs}"
        xp = exercises * 15 + successes * 10 + handoffs * 5
        if key in _AWARDED:
            awarded = 0
        else:
            _AWARDED.add(key)
            awarded = xp
        journey = LearningJourneyService().build()
        badges = []
        if successes:
            badges.append("First Practice")
        if journey["streak"] >= 3:
            badges.append("Streak Starter")
        if exercises:
            badges.append("Problem Solver")
        return sanitize_payload(
            {
                "xp": xp,
                "awarded_this_snapshot": awarded,
                "coins": successes * 2,
                "stars": min(exercises, 5),
                "level": _level_for_xp(xp),
                "streak_daily": journey["streak"],
                "badges": badges,
                "missions": [
                    {"id": "complete_exercise", "done": exercises > 0},
                    {"id": "daily_practice", "done": successes > 0},
                ],
                "leaderboard": [],
            }
        )


class TeacherConsoleService:
    def build(self) -> dict[str, Any]:
        users = [user for user in list_users() if user.consent]
        heatmap = KnowledgeHeatmapService().build()
        journey = LearningJourneyService().build()
        students = []
        for user in users:
            students.append(
                {
                    "learner_ref": _hash_id(user.user_id),
                    "grade": user.learning_level or "",
                    "language": user.language_preference or "",
                    "topics": user.last_topics[:5],
                    "last_seen": user.last_interaction,
                }
            )
        weak = [
            cell["topic"]
            for cell in heatmap["cells"]
            if cell["practice_count"] and cell["intensity"] < 0.4
        ]
        return sanitize_payload(
            {
                "students": students,
                "count": len(students),
                "weak_topics": weak,
                "strong_topics": [
                    cell["topic"]
                    for cell in heatmap["cells"]
                    if cell["intensity"] >= 0.6
                ],
                "completion": journey["completed"],
                "alerts": [],
                "heatmap": heatmap,
            }
        )


class LanguageRoutingService:
    """Detect language and recommend existing Murf voice. No new pipeline."""

    def detect(self, text: str) -> dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            return self.describe("en")
        counts: dict[str, int] = {}
        for char in text:
            code = ord(char)
            for lang, (start, end) in _SCRIPT_RANGES:
                if start <= code <= end:
                    counts[lang] = counts.get(lang, 0) + 1
        if counts:
            lang = max(counts, key=counts.get)
            return self.describe(lang)
        lowered = text.lower()
        if re.search(r"[\u0900-\u097F]", text):
            return self.describe("hi")
        if any(word in lowered for word in ("namaste", "hindi", "devanagari")):
            return self.describe("hi")
        return self.describe("en")

    def describe(self, language: str) -> dict[str, Any]:
        code = language if language in LANGUAGE_SCRIPTS else "en"
        name, script, voice = LANGUAGE_SCRIPTS[code]
        return {
            "language": code,
            "display_name": name,
            "script": script,
            "murf_voice": voice,
            "romanized": False,
            "supported": list(LANGUAGE_SCRIPTS),
        }

    def catalog(self) -> dict[str, Any]:
        return {
            "languages": [
                {
                    "code": code,
                    "name": meta[0],
                    "script": meta[1],
                    "voice": meta[2],
                }
                for code, meta in LANGUAGE_SCRIPTS.items()
            ]
        }


class ControlCenterService:
    def snapshot(self) -> dict[str, Any]:
        orchestrator = get_orchestrator()
        performance = AgentPerformanceService().snapshot()
        health = HealthMonitorService().snapshot()
        ops = ProductionMonitoringService().snapshot()
        journey = LearningJourneyService().build()
        heatmap = KnowledgeHeatmapService().build()
        return sanitize_payload(
            {
                "overview": {
                    "tutor": "Healthy",
                    "math_specialist": health["components"]["math_specialist"][
                        "status"
                    ],
                    "future_specialists": list(FUTURE_PLACEHOLDERS),
                    "active_agent": TUTOR_ID,
                    "success_rate": performance["calls"].get("successful"),
                    "failure_rate": performance["calls"].get("failed"),
                    "tool_calls": performance["tool_calls"],
                    "memory_hits": performance["memory_hits"],
                    "knowledge_hits": performance["knowledge_hits"],
                    "top_weak_topic": next(
                        (
                            cell["topic"]
                            for cell in heatmap["cells"]
                            if cell["practice_count"] and cell["intensity"] < 0.4
                        ),
                        None,
                    ),
                    "top_strong_topic": next(
                        (
                            cell["topic"]
                            for cell in heatmap["cells"]
                            if cell["intensity"] >= 0.6
                        ),
                        None,
                    ),
                },
                "agents": orchestrator.list_agents(),
                "graph": ExecutionGraphService().build(),
                "timeline": TimelineService().build(),
                "decisions": DecisionService().list_recent(),
                "memory_graph": MemoryGraphService().build(),
                "journey": journey,
                "difficulty": DifficultyEngine().evaluate(),
                "heatmap": heatmap,
                "performance": performance,
                "monitor": health,
                "trace": ExecutionTraceService().build(),
                "replay": ReplayService().build(),
                "voice": VoiceAnalyticsService().build(),
                "report": LearningReportService().build(),
                "parent": ParentDashboardService().build(),
                "gamification": GamificationService().snapshot(),
                "teacher": TeacherConsoleService().build(),
                "language": LanguageRoutingService().catalog(),
                "ops": ops,
                "notifications": list_notifications(),
            }
        )
