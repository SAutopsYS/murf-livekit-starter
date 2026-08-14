"""Graph, timeline, decisions, and memory graph from real journal events."""

from __future__ import annotations

from typing import Any

from enterprise.journal import list_decisions, list_events, seed_session_start
from enterprise.privacy import sanitize_payload
from memory.repository import get_user_by_id, list_users
from specialists.metrics import get_specialist_metrics

GRAPH_ORDER = (
    ("user", "User"),
    ("tutor", "Tutor"),
    ("math_specialist", "Math Specialist"),
    ("exercise_generator", "Exercise Generator"),
    ("evaluation", "Evaluation"),
    ("analytics", "Analytics"),
)


def _event_to_node(event: str) -> str | None:
    mapping = {
        "tutor_started": "tutor",
        "routing_decision": "tutor",
        "specialist_selected": "math_specialist",
        "handoff_started": "math_specialist",
        "handoff_completed": "math_specialist",
        "exercise_generated": "exercise_generator",
        "evaluation_completed": "evaluation",
        "exercise_completed": "evaluation",
        "handback_completed": "tutor",
        "analytics_recorded": "analytics",
        "recommendations_synchronized": "tutor",
    }
    return mapping.get(event)


class ExecutionGraphService:
    def build(self) -> dict[str, Any]:
        seed_session_start()
        events = list_events()
        seen: set[str] = {"user", "tutor"}
        for row in events:
            node = _event_to_node(str(row["event"]))
            if node:
                seen.add(node)
        metrics = get_specialist_metrics()
        if metrics.get("successful_handoffs"):
            seen.update({"math_specialist", "exercise_generator", "evaluation"})
        if metrics.get("successful_handbacks"):
            seen.add("tutor")
        nodes = [
            {
                "id": node_id,
                "label": label,
                "active": node_id in seen,
            }
            for node_id, label in GRAPH_ORDER
            if node_id in seen or node_id in {"user", "tutor"}
        ]
        edges: list[dict[str, str]] = []
        active_ids = [node["id"] for node in nodes]
        for index in range(len(active_ids) - 1):
            edges.append(
                {
                    "source": active_ids[index],
                    "target": active_ids[index + 1],
                }
            )
        stamps = {
            row["event"]: row["timestamp"] for row in events if row.get("timestamp")
        }
        return {
            "nodes": nodes,
            "edges": edges,
            "timestamps": stamps,
            "event_count": len(events),
        }


class TimelineService:
    def build(
        self,
        *,
        event: str | None = None,
        sort: str = "asc",
    ) -> dict[str, Any]:
        seed_session_start()
        rows = list_events(event=event)
        items: list[dict[str, Any]] = []
        previous_ts: str | None = None
        for row in rows:
            duration_ms = row.get("duration_ms")
            items.append(
                {
                    "id": row["id"],
                    "event": row["event"],
                    "label": row["label"],
                    "timestamp": row["timestamp"],
                    "duration_ms": duration_ms,
                    "status": row["status"],
                    "service": row["service"],
                    "previous": previous_ts,
                }
            )
            previous_ts = str(row["timestamp"])
        if sort == "desc":
            items = list(reversed(items))
        return {"items": items, "count": len(items)}


class DecisionService:
    def list_recent(self, limit: int = 40) -> dict[str, Any]:
        items = list_decisions(limit)
        return {"decisions": items, "count": len(items)}


class MemoryGraphService:
    """Read-only memory projection. Never writes."""

    def build(self, user_id: str | None = None) -> dict[str, Any]:
        user = get_user_by_id(user_id) if user_id else None
        if user is None or not user.consent:
            users = [item for item in list_users() if item.consent]
            topics: list[str] = []
            languages: list[str] = []
            levels: list[str] = []
            for item in users:
                topics.extend(item.last_topics)
                if item.language_preference:
                    languages.append(item.language_preference)
                if item.learning_level:
                    levels.append(item.learning_level)
            payload = {
                "mode": "aggregate",
                "learner_count": len(users),
                "preferred_language": languages[0] if languages else "",
                "grade": levels[0] if levels else "",
                "weak_topics": topics[-3:],
                "strong_topics": topics[:3],
                "last_exercise": topics[-1] if topics else "",
                "learning_speed": "unknown",
                "completion_rate": 0.0,
                "recommendations": [],
            }
        else:
            payload = {
                "mode": "learner",
                "preferred_language": user.language_preference,
                "grade": user.learning_level,
                "weak_topics": user.common_mistakes[:5],
                "strong_topics": user.last_topics[:5],
                "last_exercise": user.last_topics[-1] if user.last_topics else "",
                "learning_speed": user.speaking_confidence or "unknown",
                "completion_rate": 0.0,
                "recommendations": [],
            }
        nodes = [
            {"id": "learner", "label": "Learner", "value": payload["mode"]},
            {
                "id": "language",
                "label": "Preferred Language",
                "value": payload["preferred_language"] or "unset",
            },
            {"id": "grade", "label": "Grade", "value": payload["grade"] or "unset"},
            {
                "id": "weak",
                "label": "Weak Topics",
                "value": ", ".join(payload["weak_topics"]) or "none",
            },
            {
                "id": "strong",
                "label": "Strong Topics",
                "value": ", ".join(payload["strong_topics"]) or "none",
            },
            {
                "id": "last",
                "label": "Last Exercise",
                "value": payload["last_exercise"] or "none",
            },
            {
                "id": "speed",
                "label": "Learning Speed",
                "value": payload["learning_speed"],
            },
            {
                "id": "completion",
                "label": "Completion Rate",
                "value": payload["completion_rate"],
            },
            {
                "id": "recs",
                "label": "Recommendations",
                "value": ", ".join(payload["recommendations"]) or "none",
            },
        ]
        return sanitize_payload({"root": "learner", "nodes": nodes, "data": payload})
