"""Mobile and desktop clients. Same SDK contracts. No RN/Electron."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from services.events import publish
from services.jobs import job_for
from services.sdk import SDK_MODULES, SDKService

ClientKind = Literal["mobile", "desktop"]


@dataclass(frozen=True)
class ClientSession:
    kind: ClientKind
    offline: bool
    sync: str
    modules: tuple[str, ...]


class NotificationService:
    def deliver(self, kind: ClientKind) -> dict[str, str]:
        publish("NotificationDelivered", client=kind)
        return {"client": kind, "status": "architected"}


class DeviceService:
    def register(self, device_id: str) -> dict[str, str]:
        publish("DeviceRegistered", id=device_id)
        return {"id": device_id}


class SyncService:
    def run(self, kind: ClientKind) -> dict[str, str]:
        publish("SyncStarted", client=kind)
        job = job_for("mobile_sync" if kind == "mobile" else "desktop_sync")
        publish("SyncCompleted", client=kind, job=job.kind)
        return {"client": kind, "job": job.kind}


class OfflineService:
    def recover(self) -> dict[str, str]:
        publish("OfflineRecovered")
        return {"status": "architected"}


class WindowService:
    def open(self) -> dict[str, str]:
        publish("WindowOpened")
        return {"status": "architected"}


class FileService:
    def import_file(self) -> dict[str, str]:
        publish("FileImported")
        return {"status": "architected"}

    def export_file(self) -> dict[str, str]:
        publish("FileExported")
        return {"status": "architected"}


class UpdateService:
    def check(self) -> dict[str, str]:
        publish("UpdateAvailable")
        return {"status": "architected"}


class MobileService:
    def __init__(self) -> None:
        self.notifications = NotificationService()
        self.devices = DeviceService()
        self.sync = SyncService()
        self.offline = OfflineService()
        self.sdk = SDKService()

    def session(self) -> ClientSession:
        return ClientSession(
            "mobile", True, "background", tuple(m.module for m in SDK_MODULES)
        )


class DesktopService:
    def __init__(self) -> None:
        self.windows = WindowService()
        self.sync = SyncService()
        self.files = FileService()
        self.updates = UpdateService()
        self.sdk = SDKService()

    def session(self) -> ClientSession:
        return ClientSession(
            "desktop", True, "incremental", tuple(m.module for m in SDK_MODULES)
        )
