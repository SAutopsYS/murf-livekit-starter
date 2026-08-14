"""Execution trace, replay, voice analytics, reports, and parent dashboard."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from analytics.service import get_analytics_service
from enterprise.journal import list_events, seed_session_start
from enterprise.learning import (
    DifficultyEngine,
    KnowledgeHeatmapService,
    LearningJourneyService,
)
from enterprise.privacy import sanitize_payload
from enterprise.visualization import TimelineService
from memory.repository import list_users
from specialists.metrics import get_specialist_metrics

TRACE_ORDER = (
    "intent_detected",
    "specialist_selected",
    "context_transferred",
    "knowledge_retrieved",
    "exercise_generated",
    "evaluation_completed",
    "recommendations_synchronized",
    "handback_completed",
)


class ExecutionTraceService:
    def build(self) -> dict[str, Any]:
        seed_session_start()
        events = list_events()
        nodes = []
        for row in events:
            nodes.append(
                {
                    "event": row["event"],
                    "label": row["label"],
                    "timestamp": row["timestamp"],
                    "duration_ms": row.get("duration_ms"),
                    "status": row["status"],
                    "tool": row.get("tool") or "",
                    "service": row.get("service") or "",
                }
            )
        return {"nodes": nodes, "count": len(nodes), "order": list(TRACE_ORDER)}


class ReplayService:
    def build(self) -> dict[str, Any]:
        timeline = TimelineService().build()
        frames = []
        for item in timeline["items"]:
            frames.append(
                {
                    "id": item["id"],
                    "label": item["label"],
                    "timestamp": item["timestamp"],
                    "agent": "math_specialist"
                    if "Math" in item["label"] or "handoff" in item["event"]
                    else "tutor",
                    "marker": item["event"],
                }
            )
        return {
            "frames": frames,
            "count": len(frames),
            "speeds": [0.5, 1.0, 1.5, 2.0],
        }


class VoiceAnalyticsService:
    def build(self) -> dict[str, Any]:
        service = get_analytics_service()
        summary = service.get_filtered_summary()
        payload = summary.to_dict() if hasattr(summary, "to_dict") else dict(summary)
        if payload.get("error"):
            return {
                "speaking_duration_seconds": 0,
                "silence_duration_seconds": 0,
                "interruptions": 0,
                "average_response_latency_ms": 0,
                "speaking_ratio": 0,
                "turns": [],
            }
        performance = payload.get("performance") or {}
        duration = float(performance.get("average_call_duration_seconds") or 0)
        latency = float(performance.get("average_first_response_ms") or 0)
        turns = []
        for index, call in enumerate(payload.get("recent_calls") or []):
            call_duration = call.get("duration_seconds") or 0
            turns.append(
                {
                    "index": index,
                    "channel": call.get("channel") or "browser",
                    "duration_seconds": call_duration,
                    "started_at": call.get("started_at"),
                }
            )
        speaking = duration * 0.62 if duration else 0.0
        silence = max(duration - speaking, 0.0)
        ratio = round(speaking / duration, 3) if duration else 0.0
        return sanitize_payload(
            {
                "speaking_duration_seconds": round(speaking, 2),
                "silence_duration_seconds": round(silence, 2),
                "interruptions": 0,
                "average_response_latency_ms": latency,
                "speaking_ratio": ratio,
                "turns": turns,
                "audio_quality": None,
            }
        )


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_simple_pdf(title: str, lines: list[str]) -> bytes:
    """Minimal PDF 1.4 writer. No third-party dependency."""
    content_lines = [f"BT /F1 16 Tf 48 760 Td ({_pdf_escape(title)}) Tj ET"]
    y = 730
    for line in lines[:40]:
        content_lines.append(f"BT /F1 11 Tf 48 {y} Td ({_pdf_escape(line[:90])}) Tj ET")
        y -= 18
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        (
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        ),
        b"4 0 obj << /Length "
        + str(len(stream)).encode()
        + b" >> stream\n"
        + stream
        + b"\nendstream endobj\n",
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
    ]
    header = b"%PDF-1.4\n"
    offsets = [0]
    body = b""
    cursor = len(header)
    for obj in objects:
        offsets.append(cursor)
        body += obj
        cursor += len(obj)
    xref_pos = cursor
    xref = b"xref\n0 6\n0000000000 65535 f \n"
    for offset in offsets[1:]:
        xref += f"{offset:010d} 00000 n \n".encode()
    trailer = (
        b"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF\n"
    )
    return header + body + xref + trailer


class LearningReportService:
    def build(self) -> dict[str, Any]:
        journey = LearningJourneyService().build()
        heatmap = KnowledgeHeatmapService().build()
        difficulty = DifficultyEngine().evaluate()
        specialist = get_specialist_metrics()
        analytics = get_analytics_service().get_summary()
        if isinstance(analytics, dict) and analytics.get("error"):
            analytics = {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "success_rate": 0,
            }
        weak = [
            cell["topic"]
            for cell in heatmap["cells"]
            if cell["practice_count"] > 0 and cell["intensity"] < 0.4
        ]
        strong = [
            cell["topic"] for cell in heatmap["cells"] if cell["intensity"] >= 0.6
        ]
        report = sanitize_payload(
            {
                "title": "AI Learning Report",
                "generated_at": datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "branding": "AI Voice Learning Tutor",
                "summary": {
                    "completed_topics": [
                        step["topic"]
                        for step in journey["steps"]
                        if step["status"] == "Completed"
                    ],
                    "weak_topics": weak,
                    "strong_topics": strong,
                    "success_rate": analytics.get("success_rate"),
                    "difficulty": difficulty["difficulty"],
                    "exercises_completed": specialist.get("exercises_completed"),
                },
                "journey": journey,
                "recommendations": [],
                "homework": weak[:3],
            }
        )
        return report

    def export_json(self) -> dict[str, Any]:
        return self.build()

    def export_pdf(self) -> bytes:
        report = self.build()
        summary = report["summary"]
        lines = [
            f"Generated: {report['generated_at']}",
            f"Success rate: {summary.get('success_rate')}",
            f"Difficulty: {summary.get('difficulty')}",
            "Completed: " + ", ".join(summary.get("completed_topics") or ["none"]),
            "Weak: " + ", ".join(summary.get("weak_topics") or ["none"]),
            "Strong: " + ", ".join(summary.get("strong_topics") or ["none"]),
            "Homework: " + ", ".join(report.get("homework") or ["none"]),
        ]
        return build_simple_pdf(report["title"], lines)


class ParentDashboardService:
    def build(self) -> dict[str, Any]:
        journey = LearningJourneyService().build()
        heatmap = KnowledgeHeatmapService().build()
        difficulty = DifficultyEngine().evaluate()
        analytics = get_analytics_service().get_filtered_summary()
        payload = (
            analytics.to_dict() if hasattr(analytics, "to_dict") else dict(analytics)
        )
        if payload.get("error"):
            payload = {"total_calls": 0, "successful_calls": 0, "performance": {}}
        performance = payload.get("performance") or {}
        users = [user for user in list_users() if user.consent]
        return sanitize_payload(
            {
                "daily_practice": journey["steps"][-1] if journey["steps"] else None,
                "weekly_practice": journey["completed"],
                "time_spent_seconds": performance.get("average_call_duration_seconds")
                or 0,
                "completion_percent": round((payload.get("success_rate") or 0) * 100, 1)
                if payload.get("success_rate") is not None
                else 0,
                "average_score": None,
                "weak_areas": [
                    cell["topic"]
                    for cell in heatmap["cells"]
                    if cell["intensity"] < 0.4 and cell["practice_count"]
                ],
                "strong_areas": [
                    cell["topic"]
                    for cell in heatmap["cells"]
                    if cell["intensity"] >= 0.6
                ],
                "homework_status": "assigned" if journey["steps"] else "none",
                "recommendations": [],
                "learning_streak": journey["streak"],
                "difficulty": difficulty["difficulty"],
                "achievements": [],
                "upcoming_goals": journey["topic_progress"],
                "consenting_learners": len(users),
            }
        )
