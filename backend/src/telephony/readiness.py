"""Production readiness report for the telephony subsystem.

Aggregates configuration, diagnostics, metrics, and feature flags.
No networking. Never exposes secrets or SDK objects.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from telephony.config import TelephonyConfig
from telephony.diagnostics import TelephonyDiagnostics
from telephony.features import FeatureFlags
from telephony.metrics import TelephonyMetrics

logger = logging.getLogger("telephony.readiness")


@dataclass(frozen=True)
class ReadinessSummary:
    """High-level readiness summary counts."""

    overall_status: str
    timestamp: str
    checks_passed: int
    checks_failed: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class TelephonyReadinessReport:
    """Collect and aggregate telephony production readiness information."""

    def __init__(
        self,
        config: TelephonyConfig,
        metrics: TelephonyMetrics,
        feature_flags: FeatureFlags,
        *,
        service_initialized: bool = True,
        audit_available: bool = True,
        bootstrap_available: bool = True,
        learning_available: bool = True,
        evaluation_available: bool = True,
        outcome_available: bool = True,
    ) -> None:
        self._config = config
        self._metrics = metrics
        self._feature_flags = feature_flags
        self._service_initialized = service_initialized
        self._audit_available = audit_available
        self._bootstrap_available = bootstrap_available
        self._learning_available = learning_available
        self._evaluation_available = evaluation_available
        self._outcome_available = outcome_available

    def generate(self) -> dict[str, Any]:
        """Produce one structured production readiness report."""
        logger.info("Readiness report generation started")

        diagnostics = TelephonyDiagnostics(
            self._config,
            self._metrics,
            service_initialized=self._service_initialized,
        ).run_checks()

        components: dict[str, str] = {}
        passed = 0
        failed = 0

        def _mark(name: str, healthy: bool) -> None:
            nonlocal passed, failed
            components[name] = "healthy" if healthy else "unhealthy"
            if healthy:
                passed += 1
            else:
                failed += 1

        for check in diagnostics.get("checks", []):
            _mark(str(check["component"]), bool(check["healthy"]))

        _mark("audit", self._audit_available)
        _mark("bootstrap", self._bootstrap_available)
        _mark("learning", self._learning_available)
        _mark("evaluation", self._evaluation_available)
        _mark("outcome_handling", self._outcome_available)
        _mark("feature_flags", True)
        components["circuit_breaker"] = "not_configured"
        passed += 1

        overall = "ready" if failed == 0 and self._config.is_valid else "not_ready"
        summary = ReadinessSummary(
            overall_status=overall,
            timestamp=datetime.now(timezone.utc).isoformat(),
            checks_passed=passed,
            checks_failed=failed,
        )

        logger.info("Readiness checks completed")
        if overall == "ready":
            logger.info("Production readiness confirmed")

        return {
            "overall_status": summary.overall_status,
            "timestamp": summary.timestamp,
            "checks_passed": summary.checks_passed,
            "checks_failed": summary.checks_failed,
            "components": components,
            "sections": {
                "configuration": components.get("configuration", "unhealthy"),
                "provider": components.get("provider", "unhealthy"),
                "diagnostics": (
                    "healthy" if diagnostics.get("healthy") else "unhealthy"
                ),
                "metrics": components.get("metrics", "unhealthy"),
                "circuit_breaker": "not_configured",
                "feature_flags": self._feature_flags.snapshot(),
                "learning_integration": components.get("learning", "unhealthy"),
                "bootstrap": components.get("bootstrap", "unhealthy"),
                "evaluation": components.get("evaluation", "unhealthy"),
                "outcome_handling": components.get("outcome_handling", "unhealthy"),
            },
            "metrics": self._metrics.snapshot(),
            "diagnostics": diagnostics,
        }
