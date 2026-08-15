"""Background job architecture. No queue implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

JobKind = Literal[
    "report_generation",
    "embeddings",
    "memory_consolidation",
    "analytics_aggregation",
    "notifications",
    "enterprise_export",
    "recommendation_refresh",
    "whiteboard_index",
    "graph_index",
    "search_index",
    "workflow_run",
    "mobile_sync",
    "desktop_sync",
    "backup",
]

JobStatus = Literal["queued", "running", "done", "failed", "cancelled"]


@dataclass(frozen=True)
class JobSpec:
    kind: JobKind
    name: str
    idempotent: bool
    max_attempts: int
    timeout_seconds: int


JOB_CATALOG: tuple[JobSpec, ...] = (
    JobSpec("report_generation", "Learning report", True, 2, 60),
    JobSpec("embeddings", "Knowledge embeddings", True, 3, 120),
    JobSpec("memory_consolidation", "Consented memory merge", True, 1, 30),
    JobSpec("analytics_aggregation", "Call rollup", True, 2, 45),
    JobSpec("notifications", "Enterprise notify", False, 3, 15),
    JobSpec("enterprise_export", "Control export", True, 2, 90),
    JobSpec("recommendation_refresh", "Adaptive refresh", True, 2, 20),
    JobSpec("whiteboard_index", "Canvas index", True, 2, 40),
    JobSpec("graph_index", "Memory graph index", True, 2, 40),
    JobSpec("search_index", "Universal search index", True, 2, 30),
    JobSpec("workflow_run", "Automation run", False, 2, 60),
    JobSpec("mobile_sync", "Mobile sync", True, 3, 20),
    JobSpec("desktop_sync", "Desktop sync", True, 3, 20),
    JobSpec("backup", "Region backup", True, 2, 120),
)


def job_for(kind: JobKind) -> JobSpec:
    for spec in JOB_CATALOG:
        if spec.kind == kind:
            return spec
    raise KeyError(kind)
