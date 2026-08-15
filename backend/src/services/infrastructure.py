"""Hyperscale infrastructure. Architecture only. No Redis/Kafka/K8s install."""

from __future__ import annotations

from dataclasses import dataclass

from services.events import publish
from services.jobs import JOB_CATALOG


@dataclass(frozen=True)
class InfraComponent:
    name: str
    role: str
    implemented: bool


CATALOG: tuple[InfraComponent, ...] = (
    InfraComponent("redis", "cache + rate-limit store", False),
    InfraComponent("kafka", "event fan-out", False),
    InfraComponent("kubernetes", "container orchestration", False),
    InfraComponent("elastic", "log search", False),
    InfraComponent("object_storage", "exports + backups", False),
    InfraComponent("vector_db", "future search adapter", False),
    InfraComponent("gpu", "future local inference", False),
)


class InfrastructureService:
    def catalog(self) -> tuple[InfraComponent, ...]:
        return CATALOG

    def declare_queue(self) -> dict[str, object]:
        publish("QueueDeclared", jobs=len(JOB_CATALOG))
        return {"jobs": [spec.kind for spec in JOB_CATALOG], "broker": "none"}

    def warm_cache(self) -> dict[str, str]:
        publish("CacheWarmed")
        return {"status": "architected"}


class ClusterManager:
    def spec(self) -> dict[str, bool]:
        return {"kubernetes": False}


class CacheManager:
    def spec(self) -> dict[str, bool]:
        return {"redis": False}


class QueueManager:
    def spec(self) -> dict[str, bool]:
        return {"kafka": False}


class GPUManager:
    def spec(self) -> dict[str, bool]:
        return {"gpu": False}


class StorageManager:
    def spec(self) -> dict[str, bool]:
        return {"object_storage": False}


InfrastructureProvider = InfrastructureService
