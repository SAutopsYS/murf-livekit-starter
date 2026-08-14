"""Learning journey, adaptive difficulty, and knowledge heatmap."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

from analytics.models import AnalyticsFilter
from analytics.service import get_analytics_service
from enterprise.privacy import sanitize_payload
from memory.repository import list_users
from specialists.metrics import get_specialist_metrics

PRACTICE_LEVELS = ("beginner", "intermediate", "advanced")

DIFFICULTY_LEVELS = ("easy", "medium", "hard", "challenge", "olympiad")

TOPIC_KEYS = (
    "addition",
    "tables",
    "fractions",
    "decimals",
    "geometry",
    "multiplication",
    "percentages",
    "algebra",
)


def _day_label(iso: str | None, index: int) -> str:
    if not iso:
        return f"Session {index + 1}"
    try:
        parsed = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return f"Session {index + 1}"
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d")


class LearningJourneyService:
    def build(self, filters: AnalyticsFilter | None = None) -> dict[str, Any]:
        service = get_analytics_service()
        summary = service.get_filtered_summary(filters)
        payload = summary.to_dict() if hasattr(summary, "to_dict") else dict(summary)
        recent = list(payload.get("recent_calls") or [])
        steps: list[dict[str, Any]] = []
        users = [user for user in list_users() if user.consent]
        topics: list[str] = []
        for user in users:
            topics.extend(user.last_topics)
        for index, call in enumerate(recent):
            topic = topics[index] if index < len(topics) else "practice"
            outcome = call.get("outcome")
            status = "Completed" if outcome == "success" else "Needs Improvement"
            if outcome not in {"success", "failed"}:
                status = "In Progress"
            steps.append(
                {
                    "day": _day_label(call.get("started_at"), index),
                    "topic": topic,
                    "status": status,
                    "channel": call.get("channel") or "browser",
                }
            )
        successful = int(payload.get("successful_calls") or 0)
        streak = 0
        for call in reversed(recent):
            if call.get("outcome") == "success":
                streak += 1
            else:
                break
        return sanitize_payload(
            {
                "steps": steps,
                "streak": streak,
                "completed": successful,
                "total": int(payload.get("total_calls") or 0),
                "topic_progress": dict(Counter(topics)),
            }
        )


class DifficultyEngine:
    """Deterministic difficulty. Never mutates historical scores."""

    def evaluate(
        self,
        *,
        accuracy: float | None = None,
        completion_rate: float | None = None,
        response_time_ms: float | None = None,
        current: str = "medium",
    ) -> dict[str, Any]:
        metrics = get_specialist_metrics()
        handoffs = float(metrics.get("total_handoffs") or 0)
        success = float(metrics.get("successful_handoffs") or 0)
        derived_accuracy = (success / handoffs) if handoffs else None
        score = accuracy if accuracy is not None else derived_accuracy
        completion = completion_rate
        if completion is None:
            sessions = float(metrics.get("math_sessions") or 0)
            done = float(metrics.get("successful_math_sessions") or 0)
            completion = (done / sessions) if sessions else None
        level = current if current in DIFFICULTY_LEVELS else "medium"
        reason = "hold"
        if score is not None and score >= 0.85 and (completion or 0) >= 0.7:
            nxt = DIFFICULTY_LEVELS[
                min(DIFFICULTY_LEVELS.index(level) + 1, len(DIFFICULTY_LEVELS) - 1)
            ]
            if nxt != level:
                level = nxt
                reason = "advance_high_accuracy"
        elif score is not None and score < 0.45:
            nxt = DIFFICULTY_LEVELS[max(DIFFICULTY_LEVELS.index(level) - 1, 0)]
            if nxt != level:
                level = nxt
                reason = "reduce_low_accuracy"
        mapped = {
            "easy": PRACTICE_LEVELS[0],
            "medium": PRACTICE_LEVELS[1],
            "hard": PRACTICE_LEVELS[2],
            "challenge": PRACTICE_LEVELS[2],
            "olympiad": PRACTICE_LEVELS[2],
        }
        return {
            "difficulty": level,
            "practice_level": mapped[level],
            "reason": reason,
            "accuracy": round(score, 3) if score is not None else None,
            "completion_rate": round(completion, 3) if completion is not None else None,
            "response_time_ms": response_time_ms,
            "levels": list(DIFFICULTY_LEVELS),
        }


class KnowledgeHeatmapService:
    def build(self) -> dict[str, Any]:
        users = [user for user in list_users() if user.consent]
        counts: Counter[str] = Counter()
        for user in users:
            for topic in user.last_topics:
                key = topic.strip().lower().replace(" ", "_")
                if key in TOPIC_KEYS:
                    counts[key] += 1
                else:
                    for known in TOPIC_KEYS:
                        if known in key:
                            counts[known] += 1
        metrics = get_specialist_metrics()
        exercises = int(metrics.get("exercises_completed") or 0)
        if exercises and not counts:
            counts["multiplication"] = exercises
        cells = []
        maximum = max(counts.values()) if counts else 1
        for topic in TOPIC_KEYS:
            practice = counts.get(topic, 0)
            intensity = round(practice / maximum, 3) if maximum else 0.0
            cells.append(
                {
                    "topic": topic,
                    "practice_count": practice,
                    "accuracy": None,
                    "completion": practice,
                    "intensity": intensity,
                }
            )
        return {"cells": cells, "max_practice": maximum if counts else 0}
