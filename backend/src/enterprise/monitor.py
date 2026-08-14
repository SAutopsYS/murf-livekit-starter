"""Agent performance, live health, and production operations."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from analytics.database import get_database_path as analytics_db_path
from analytics.service import get_analytics_service
from enterprise.privacy import sanitize_payload
from memory.database import get_database_path as memory_db_path
from specialists.metrics import get_specialist_metrics
from specialists.registry import get_specialist_registry
from tools.metrics import get_tool_metrics


def _configured(name: str) -> bool:
    value = os.getenv(name, "").strip()
    return bool(value) and not value.startswith("your_")


def _file_status(path: Path) -> str:
    if path.exists():
        return "Healthy"
    if path.parent.exists():
        return "Idle"
    return "Disconnected"


def _latency(metrics: dict[str, Any], key: str) -> float:
    value = metrics.get(key)
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


class AgentPerformanceService:
    def snapshot(self) -> dict[str, Any]:
        specialist = get_specialist_metrics()
        tools = get_tool_metrics()
        analytics = get_analytics_service().get_summary()
        summary = (
            analytics.to_dict() if hasattr(analytics, "to_dict") else dict(analytics)
        )
        tool_calls = sum(int(row.get("calls") or 0) for row in tools.values())
        memory_hits = int((tools.get("memory_tool") or {}).get("calls") or 0)
        knowledge_hits = int((tools.get("knowledge_tool") or {}).get("calls") or 0)
        exercises_generated = int((tools.get("exercise_tool") or {}).get("calls") or 0)
        exercises_evaluated = int((tools.get("score_tool") or {}).get("calls") or 0)
        recommendations = int(
            (tools.get("recommendation_tool") or {}).get("calls") or 0
        )
        return sanitize_payload(
            {
                "tutor_accuracy": None,
                "math_specialist_accuracy": specialist.get("recovery_success_rate"),
                "average_response_time_ms": specialist.get("average_routing_time_ms"),
                "average_thinking_time_ms": specialist.get("average_handoff_time_ms"),
                "tool_calls": tool_calls,
                "memory_hits": memory_hits,
                "knowledge_hits": knowledge_hits,
                "successful_handoffs": specialist.get("successful_handoffs"),
                "failed_handoffs": specialist.get("failed_handoffs"),
                "exercises_generated": exercises_generated,
                "exercises_evaluated": exercises_evaluated,
                "learning_recommendations": recommendations,
                "calls": {
                    "total": summary.get("total_calls"),
                    "successful": summary.get("successful_calls"),
                    "failed": summary.get("failed_calls"),
                },
                "tools": tools,
                "specialist": specialist,
            }
        )


class HealthMonitorService:
    def snapshot(self) -> dict[str, Any]:
        registry = get_specialist_registry()
        specialist = get_specialist_metrics()
        math_health = registry.health("math_practice_specialist")
        components = {
            "tutor": {
                "status": "Healthy",
                "latency_ms": _latency(specialist, "average_routing_time_ms"),
            },
            "math_specialist": {
                "status": "Healthy" if math_health == "READY" else math_health.title(),
                "latency_ms": _latency(specialist, "average_handoff_time_ms"),
            },
            "memory": {"status": _file_status(memory_db_path()), "latency_ms": 0},
            "knowledge": {"status": "Healthy", "latency_ms": 0},
            "analytics": {"status": _file_status(analytics_db_path()), "latency_ms": 0},
            "learning_tools": {"status": "Healthy", "latency_ms": 0},
            "livekit": {
                "status": "Healthy" if _configured("LIVEKIT_URL") else "Disconnected",
                "latency_ms": 0,
            },
            "murf_falcon": {
                "status": "Healthy" if _configured("MURF_API_KEY") else "Disconnected",
                "latency_ms": 0,
            },
            "sqlite": {"status": "Healthy", "latency_ms": 0},
            "api": {"status": "Healthy", "latency_ms": 0},
            "websocket": {"status": "Idle", "latency_ms": 0},
        }
        return {
            "components": components,
            "retry_count": specialist.get("retry_count"),
            "heartbeat": "ok",
        }


class ProductionMonitoringService:
    def snapshot(self) -> dict[str, Any]:
        health = HealthMonitorService().snapshot()
        specialist = get_specialist_metrics()
        try:
            disk = shutil.disk_usage(Path.cwd())
            disk_payload = {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
            }
        except OSError:
            disk_payload = {"total": 0, "used": 0, "free": 0}
        critical = sum(
            1
            for row in health["components"].values()
            if row["status"] in {"Disconnected", "Error", "ERROR"}
        )
        score = max(0, 100 - critical * 15)
        status = "Healthy"
        if score < 70:
            status = "Warning"
        if score < 40:
            status = "Critical"
        return sanitize_payload(
            {
                "health_score": score,
                "status": status,
                "disk": disk_payload,
                "cpu": None,
                "memory": None,
                "redis": "unavailable",
                "session_count": int(specialist.get("math_sessions") or 0),
                "latency_ms": specialist.get("average_routing_time_ms"),
                "retries": specialist.get("retry_count"),
                "failures": specialist.get("failed_handoffs"),
                "components": health["components"],
            }
        )
