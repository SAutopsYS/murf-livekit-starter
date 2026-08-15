"""Global cloud and edge. Wraps compose/health/profile. No new orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

from salora_platform.config import get_platform_config
from salora_platform.health import check_liveness, check_readiness
from services.events import publish
from services.jobs import job_for


@dataclass(frozen=True)
class RegionRecord:
    id: str
    name: str
    primary: bool


REGIONS: tuple[RegionRecord, ...] = (
    RegionRecord("local", "Local compose", True),
    RegionRecord("staging", "Staging", False),
    RegionRecord("production", "Production", False),
)


class RegionService:
    def list(self) -> tuple[RegionRecord, ...]:
        return REGIONS

    def add(self, region_id: str) -> dict[str, str]:
        publish("RegionAdded", id=region_id)
        return {"id": region_id, "status": "architected"}


class ClusterService:
    def snapshot(self) -> dict[str, object]:
        live = check_liveness()
        ready = check_readiness()
        return {"liveness": live["status"], "readiness": ready["status"]}


class DeploymentService:
    def strategy(self) -> dict[str, str]:
        profile = get_platform_config().profile
        return {
            "profile": profile,
            "images": "frontend+backend",
            "rollback": "previous_image_and_env",
            "zero_downtime": "frontend_replicas",
        }


class TrafficService:
    def failover(self) -> dict[str, str]:
        publish("FailoverStarted")
        return {"status": "architected"}


class BackupService:
    def run(self) -> dict[str, str]:
        spec = job_for("backup")
        publish("BackupCompleted", job=spec.kind)
        return {"job": spec.kind, "rule": "no_speech_lake"}


class CloudService:
    def __init__(self) -> None:
        self.regions = RegionService()
        self.clusters = ClusterService()
        self.deployments = DeploymentService()
        self.traffic = TrafficService()
        self.backups = BackupService()


GlobalDeploymentService = CloudService
GlobalProvider = CloudService
RegionEngine = RegionService
CDNEngine = TrafficService
EdgeEngine = TrafficService
EdgeService = TrafficService
FailoverEngine = TrafficService
