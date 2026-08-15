"""Telephony health diagnostics and startup self-check.

No network calls. No outbound dialing. Structured verification only.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from telephony.config import TelephonyConfig
from telephony.metrics import TelephonyMetrics

logger = logging.getLogger("telephony.diagnostics")


@dataclass(frozen=True)
class DiagnosticResult:
    """One component health check result."""

    component: str
    healthy: bool
    message: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class TelephonyDiagnostics:
    """Verify telephony subsystem readiness without placing calls."""

    def __init__(
        self,
        config: TelephonyConfig,
        metrics: TelephonyMetrics | None = None,
        *,
        service_initialized: bool = True,
    ) -> None:
        self._config = config
        self._metrics = metrics
        self._service_initialized = service_initialized

    def run_checks(self) -> dict[str, Any]:
        """Run local readiness checks and return a structured report."""
        logger.info("Telephony diagnostics started")
        checks: list[DiagnosticResult] = []

        config_ok = self._config.is_valid
        checks.append(
            DiagnosticResult(
                component="configuration",
                healthy=config_ok,
                message="Loaded" if config_ok else "Missing LiveKit configuration",
            )
        )
        logger.info("Configuration verified")

        livekit_ok = self._config.livekit_ready
        checks.append(
            DiagnosticResult(
                component="livekit",
                healthy=livekit_ok,
                message="Configured" if livekit_ok else "LiveKit credentials missing",
            )
        )
        logger.info("Provider verified")

        checks.append(
            DiagnosticResult(
                component="provider",
                healthy=bool(livekit_ok),
                message=(
                    "Outbound trunk ready"
                    if self._config.outbound_ready
                    else (
                        "LiveKit ready; SIP trunk optional"
                        if livekit_ok
                        else "Provider not ready"
                    )
                ),
            )
        )

        checks.append(
            DiagnosticResult(
                component="service",
                healthy=self._service_initialized,
                message="Initialized"
                if self._service_initialized
                else "Not initialized",
            )
        )

        metrics_ok = self._metrics is not None
        checks.append(
            DiagnosticResult(
                component="metrics",
                healthy=metrics_ok,
                message="Available" if metrics_ok else "Unavailable",
            )
        )

        healthy = all(item.healthy for item in checks)
        logger.info("Diagnostics completed")
        return {
            "healthy": healthy,
            "checks": [item.as_dict() for item in checks],
        }
