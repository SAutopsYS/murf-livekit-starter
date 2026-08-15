"""Workflow automation. One engine for Phase 22 and Phase 26. No visual editor."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Literal
from uuid import uuid4

from salora_platform.auth import Role, can
from services.events import publish
from services.jobs import job_for
from services.studio import WorkflowService

NodeKind = Literal[
    "trigger",
    "condition",
    "ai_action",
    "learning_action",
    "knowledge_action",
    "studio_action",
    "whiteboard_action",
    "marketplace_action",
    "notification",
    "approval",
    "delay",
    "webhook",
    "branch",
    "loop",
    "schedule",
    "api_call",
    "agent_execution",
    "document_update",
    "sdk_callback",
]
TriggerKind = Literal[
    "VoiceCompleted",
    "LearningFinished",
    "DocumentCreated",
    "WorkflowCompleted",
    "AgentFinished",
    "PluginInstalled",
    "ScheduleTriggered",
    "WebhookReceived",
    "APICalled",
    "OrganizationEvent",
]


@dataclass
class AutomationWorkflow:
    id: str
    owner: str
    organization: str | None
    permissions: tuple[str, ...]
    trigger: TriggerKind
    nodes: tuple[NodeKind, ...]
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: float = 0
    updated_at: float = 0


class TriggerService:
    KINDS: tuple[TriggerKind, ...] = (
        "VoiceCompleted",
        "LearningFinished",
        "DocumentCreated",
        "WorkflowCompleted",
        "AgentFinished",
        "PluginInstalled",
        "ScheduleTriggered",
        "WebhookReceived",
        "APICalled",
        "OrganizationEvent",
    )

    def fire(self, kind: TriggerKind) -> dict[str, str]:
        publish("TriggerFired", kind=kind)
        publish("TriggerActivated", kind=kind)
        return {"kind": kind, "status": "fired"}


class ActionService:
    def run(self, kind: NodeKind) -> dict[str, str]:
        publish("NodeExecuted", kind=kind)
        publish("ActionCompleted", kind=kind)
        return {"kind": kind, "status": "architected"}


class ConditionService:
    def evaluate(self, ok: bool) -> bool:
        return ok


class ApprovalService:
    def required(self, role: Role) -> bool:
        return can(role, "enterprise.admin")


class ScheduleService:
    def tick(self) -> dict[str, str]:
        publish("ScheduleTriggered")
        return {"status": "architected", "job": job_for("workflow_run").kind}


class ExecutionService:
    def __init__(self) -> None:
        self._studio = WorkflowService()

    def run(self, workflow: AutomationWorkflow) -> AutomationWorkflow:
        publish("WorkflowExecuted", id=workflow.id)
        self._studio.start("analyze", workflow.owner)
        publish("WorkflowCompleted", id=workflow.id)
        return workflow


class AutomationService:
    """Canonical automation engine. WorkflowAutomationService is this class."""

    def __init__(self) -> None:
        self.triggers = TriggerService()
        self.actions = ActionService()
        self.conditions = ConditionService()
        self.approvals = ApprovalService()
        self.schedules = ScheduleService()
        self.execution = ExecutionService()

    def create(
        self, owner: str, trigger: TriggerKind, organization: str | None = None
    ) -> AutomationWorkflow:
        stamp = time()
        record = AutomationWorkflow(
            id=f"wf_{uuid4().hex[:10]}",
            owner=owner,
            organization=organization,
            permissions=("studio.access",),
            trigger=trigger,
            nodes=("trigger", "condition", "ai_action"),
            created_at=stamp,
            updated_at=stamp,
        )
        publish("WorkflowCreated", id=record.id)
        return record

    def execute(self, workflow: AutomationWorkflow) -> AutomationWorkflow:
        self.triggers.fire(workflow.trigger)
        return self.execution.run(workflow)


WorkflowAutomationService = AutomationService
WorkflowExecutionService = ExecutionService
