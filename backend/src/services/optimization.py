"""Optimization hooks. Tune existing paths. No architecture change."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationPlan:
    voice_untouched: bool
    bundle: str
    cache: str
    providers: str
    memory: str
    gpu: str


class OptimizationService:
    def plan(self) -> OptimizationPlan:
        return OptimizationPlan(
            voice_untouched=True,
            bundle="route-split analytics/enterprise; hall stays light",
            cache="process-local metrics + search rank; Redis later",
            providers="ProviderRegistry.choose + orchestrator timeout",
            memory="SQLite process-local; no speech lake",
            gpu="none — inference stays with LiveKit/Gemini/Murf",
        )


OptimizationProvider = OptimizationService
PerformanceEngine = OptimizationService
CostEngine = OptimizationService
ModelRouterOptimizer = OptimizationService
CacheOptimizer = OptimizationService
