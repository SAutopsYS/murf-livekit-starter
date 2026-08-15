"""Collaboration platform. Presence and sessions. No CRDT, no second voice."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal
from uuid import uuid4

from salora_platform.auth import Role, can
from services.events import publish

PresenceState = Literal[
    "presence",
    "cursor",
    "selection",
    "activity",
    "focus",
    "typing",
    "voice",
    "status",
    "availability",
]
CollabRole = Literal[
    "owner",
    "admin",
    "editor",
    "reviewer",
    "commenter",
    "viewer",
    "observer",
    "ai_agent",
]
SessionKind = Literal[
    "shared",
    "voice",
    "studio",
    "whiteboard",
    "learning",
    "enterprise",
]

COLLAB_TO_PERMISSION: dict[CollabRole, str] = {
    "owner": "enterprise.admin",
    "admin": "enterprise.admin",
    "editor": "studio.access",
    "reviewer": "studio.access",
    "commenter": "learning.read",
    "viewer": "learning.read",
    "observer": "learning.read",
    "ai_agent": "voice.session",
}


@dataclass
class PresenceRecord:
    id: str
    user_id: str
    session_id: str
    workspace_id: str
    state: PresenceState
    last_seen: float
    metadata: dict[str, str]


@dataclass
class CollaborationSession:
    id: str
    kind: SessionKind
    workspace_id: str
    organization_id: str | None
    owner: str
    created_at: float


class PresenceService:
    def heartbeat(
        self, user_id: str, session_id: str, workspace_id: str
    ) -> PresenceRecord:
        record = PresenceRecord(
            id=f"pres_{uuid4().hex[:8]}",
            user_id=user_id,
            session_id=session_id,
            workspace_id=workspace_id,
            state="presence",
            last_seen=time(),
            metadata={},
        )
        return record


class SessionService:
    def create(
        self, kind: SessionKind, workspace_id: str, owner: str
    ) -> CollaborationSession:
        record = CollaborationSession(
            id=f"cs_{uuid4().hex[:10]}",
            kind=kind,
            workspace_id=workspace_id,
            organization_id=None,
            owner=owner,
            created_at=time(),
        )
        publish("SessionCreated", id=record.id, kind=kind)
        return record


class ParticipantService:
    def join(self, session_id: str, user_id: str) -> dict[str, str]:
        publish("ParticipantJoined", session=session_id, user=user_id)
        return {"session_id": session_id, "user_id": user_id, "status": "joined"}

    def leave(self, session_id: str, user_id: str) -> None:
        publish("ParticipantLeft", session=session_id, user=user_id)


class CommentService:
    def create(self, session_id: str) -> dict[str, str]:
        publish("CommentCreated", session=session_id)
        return {"session_id": session_id, "status": "architected"}

    def resolve(self, session_id: str) -> None:
        publish("CommentResolved", session=session_id)


class NotificationService:
    def kinds(self) -> tuple[str, ...]:
        return (
            "mention",
            "shared_workspace",
            "comment_reply",
            "ai_suggestion",
            "workflow_complete",
            "learning_recommendation",
            "plugin_update",
        )


class AwarenessService:
    def cursor(self, session_id: str) -> None:
        publish("CursorMoved", session=session_id)


class ActivityService:
    def share(self, workspace_id: str) -> None:
        publish("WorkspaceShared", workspace=workspace_id)


class CollaborationService:
    def __init__(self) -> None:
        self.presence = PresenceService()
        self.sessions = SessionService()
        self.participants = ParticipantService()
        self.comments = CommentService()
        self.notifications = NotificationService()
        self.awareness = AwarenessService()
        self.activity = ActivityService()

    def may_join(self, role: Role, collab: CollabRole) -> bool:
        permission = COLLAB_TO_PERMISSION[collab]
        return can(role, permission)  # type: ignore[arg-type]
