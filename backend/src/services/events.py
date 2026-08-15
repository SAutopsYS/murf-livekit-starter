"""In-process event bus. Future modules subscribe. No speech fields."""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from salora_platform.observability import emit

EventHandler = Callable[["PlatformEvent"], None]

FORBIDDEN = re.compile(
    r"transcript|utterance|otp|phone|secret|password|token|api[_-]?key|prompt",
    re.I,
)

EVENT_NAMES = (
    "SessionStarted",
    "SessionEnded",
    "LearningUpdated",
    "KnowledgeUpdated",
    "AgentTransferred",
    "RecommendationCreated",
    "InsightCreated",
    "ProviderFailed",
    "ProviderRecovered",
    "MemoryMerged",
    "ProjectCreated",
    "ProjectOpened",
    "DocumentUpdated",
    "WorkflowStarted",
    "WorkflowFinished",
    "PromptExecuted",
    "TemplateApplied",
    "AssetImported",
    "NotebookCreated",
    "CanvasCreated",
    "CanvasOpened",
    "ElementAdded",
    "ElementUpdated",
    "ElementDeleted",
    "SelectionChanged",
    "ViewportChanged",
    "HistoryRecorded",
    "DiagramGenerated",
    "BoardExported",
    "GraphOpened",
    "NodeSelected",
    "NodeExpanded",
    "NodeCollapsed",
    "RelationshipFocused",
    "GraphFiltered",
    "GraphExported",
    "BookmarkCreated",
    "QueryExecuted",
    "NavigationChanged",
    "PluginInstalled",
    "PluginUpdated",
    "PluginRemoved",
    "PluginEnabled",
    "PluginDisabled",
    "MarketplaceOpened",
    "PackagePublished",
    "PackageDownloaded",
    "CapabilityGranted",
    "CapabilityRevoked",
    "OrganizationCreated",
    "WorkspaceCreated",
    "MemberInvited",
    "MemberJoined",
    "MemberRemoved",
    "RoleChanged",
    "PolicyUpdated",
    "WorkspaceArchived",
    "OrganizationDeleted",
    "WebhookDelivered",
    "IntegrationRegistered",
    "ApiTokenIssued",
    "SessionCreated",
    "ParticipantJoined",
    "ParticipantLeft",
    "CursorMoved",
    "CommentCreated",
    "CommentResolved",
    "VoiceJoined",
    "VoiceLeft",
    "WorkspaceShared",
    "PermissionsUpdated",
    "AgentRegistered",
    "AgentLoaded",
    "AgentStarted",
    "AgentCompleted",
    "AgentFailed",
    "AgentSuspended",
    "AgentInstalled",
    "AgentRemoved",
    "SearchStarted",
    "SearchCompleted",
    "SearchIndexed",
    "SearchExecuted",
    "SuggestionGenerated",
    "FiltersUpdated",
    "IndexUpdated",
    "WorkflowPaused",
    "WorkflowCompleted",
    "WorkflowCancelled",
    "WorkflowCreated",
    "WorkflowExecuted",
    "WorkflowFailed",
    "NodeExecuted",
    "TriggerFired",
    "TriggerActivated",
    "ActionCompleted",
    "ScheduleTriggered",
    "TaskCreated",
    "MeetingScheduled",
    "DocumentGenerated",
    "SummaryCreated",
    "EmailReceived",
    "DeviceRegistered",
    "SyncStarted",
    "SyncCompleted",
    "NotificationDelivered",
    "OfflineRecovered",
    "WindowOpened",
    "WorkspaceRestored",
    "FileImported",
    "FileExported",
    "UpdateAvailable",
    "PolicyApplied",
    "AuditGenerated",
    "ConsentGranted",
    "ComplianceChecked",
    "RegionAdded",
    "FailoverStarted",
    "BackupCompleted",
    "StudentJoined",
    "LessonCompleted",
    "AssignmentSubmitted",
    "ProgressUpdated",
    "ParentNotified",
    "MentorStarted",
    "MentorCompleted",
    "RecommendationGenerated",
    "GoalAchieved",
    "APIKeyIssued",
    "OAuthGranted",
    "ClientRegistered",
    "SolutionDeployed",
    "CacheWarmed",
    "QueueDeclared",
    "ExtensionVerified",
)


@dataclass(frozen=True)
class PlatformEvent:
    name: str
    at: float
    fields: dict[str, Any] = field(default_factory=dict)


_handlers: dict[str, list[EventHandler]] = {}
_history: list[PlatformEvent] = []
_MAX = 200


def subscribe(name: str, handler: EventHandler) -> None:
    _handlers.setdefault(name, []).append(handler)


def unsubscribe(name: str, handler: EventHandler) -> None:
    bucket = _handlers.get(name, [])
    if handler in bucket:
        bucket.remove(handler)


_EVENT_NAME_SET = frozenset(EVENT_NAMES)


def _clean_fields(fields: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in fields.items():
        if FORBIDDEN.search(key):
            continue
        if isinstance(value, str) and FORBIDDEN.search(value) and len(value) > 24:
            continue
        clean[key] = value
    return clean


def publish(name: str, **fields: Any) -> PlatformEvent:
    if name not in _EVENT_NAME_SET:
        emit("warning", "event.unknown", name=name)
    clean = _clean_fields(fields)
    event = PlatformEvent(name=name, at=time.time(), fields=clean)
    _history.append(event)
    if len(_history) > _MAX:
        del _history[: len(_history) - _MAX]
    emit("info", f"event.{name}", **{k: str(v)[:80] for k, v in clean.items()})
    for handler in list(_handlers.get(name, [])):
        handler(event)
    for handler in list(_handlers.get("*", [])):
        handler(event)
    return event


def recent_events(name: str | None = None) -> list[PlatformEvent]:
    if name is None:
        return list(_history)
    return [item for item in _history if item.name == name]


def reset_events() -> None:
    _handlers.clear()
    _history.clear()
