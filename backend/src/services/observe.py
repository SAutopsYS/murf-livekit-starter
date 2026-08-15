"""Per-service observability. Extends salora_platform metrics."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from salora_platform.observability import record_metric
from services.contracts import ServiceMetrics

T = TypeVar("T")

_last: dict[str, ServiceMetrics] = {}


def record_service(
    service: str,
    *,
    latency_ms: float,
    provider: str = "none",
    failures: int = 0,
    retries: int = 0,
    cache_hit: bool = False,
    token_usage: int = 0,
    cost_units: float = 0.0,
) -> ServiceMetrics:
    metrics = ServiceMetrics(
        service=service,
        latency_ms=latency_ms,
        failures=failures,
        retries=retries,
        cache_hit=cache_hit,
        provider=provider,
        token_usage=token_usage,
        cost_units=cost_units,
    )
    _last[service] = metrics
    record_metric(f"service.{service}.latency_ms", latency_ms)
    if failures:
        record_metric(f"service.{service}.failures", float(failures))
    return metrics


def last_metrics(service: str) -> ServiceMetrics | None:
    return _last.get(service)


def timed(
    service: str, provider: str = "none"
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def wrap(fn: Callable[..., T]) -> Callable[..., T]:
        def inner(*args: object, **kwargs: object) -> T:
            started = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                record_service(
                    service,
                    latency_ms=round((time.perf_counter() - started) * 1000, 2),
                    provider=provider,
                )

        return inner

    return wrap
