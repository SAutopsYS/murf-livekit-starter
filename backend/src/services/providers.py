"""Provider registry. Live adapters wrap existing env. Future names are capabilities only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from salora_platform.config import PlatformConfig, get_platform_config
from salora_platform.observability import record_metric
from services.events import publish

ProviderName = Literal[
    "livekit",
    "murf",
    "deepgram",
    "google",
    "openai",
    "claude",
    "groq",
    "deepseek",
    "llama",
    "azure_openai",
    "bedrock",
    "vertex",
]

Capability = Literal["transport", "tts", "stt", "llm", "embeddings"]
HealthState = Literal["up", "down", "unknown", "disabled"]


@dataclass(frozen=True)
class ProviderAdapter:
    name: ProviderName
    capabilities: tuple[Capability, ...]
    live: bool
    configured: bool

    @property
    def health(self) -> HealthState:
        if not self.live:
            return "disabled"
        if self.configured:
            return "up"
        return "down"


@dataclass(frozen=True)
class ProviderMetrics:
    name: ProviderName
    health: HealthState
    calls: int
    failures: int


_LIVE: dict[ProviderName, tuple[Capability, ...]] = {
    "livekit": ("transport",),
    "murf": ("tts",),
    "deepgram": ("stt",),
    "google": ("llm",),
    "openai": ("llm", "embeddings"),
}

_FUTURE: dict[ProviderName, tuple[Capability, ...]] = {
    "claude": ("llm",),
    "groq": ("llm",),
    "deepseek": ("llm",),
    "llama": ("llm",),
    "azure_openai": ("llm", "embeddings"),
    "bedrock": ("llm",),
    "vertex": ("llm",),
}


class ProviderRegistry:
    """One registry. agent.py still constructs LiveKit/Murf plugins itself."""

    def __init__(self, config: PlatformConfig | None = None) -> None:
        self._config = config or get_platform_config()
        status = self._config.provider_status()
        self._adapters: dict[ProviderName, ProviderAdapter] = {}
        for name, caps in _LIVE.items():
            configured = bool(status.get(name, False))
            if name == "openai":
                configured = bool(self._config.openai_api_key)
            self._adapters[name] = ProviderAdapter(name, caps, True, configured)
        for name, caps in _FUTURE.items():
            self._adapters[name] = ProviderAdapter(name, caps, False, False)

    def get(self, name: ProviderName) -> ProviderAdapter:
        return self._adapters[name]

    def list_live(self) -> list[ProviderAdapter]:
        return [item for item in self._adapters.values() if item.live]

    def choose(self, capability: Capability) -> ProviderAdapter | None:
        live = [
            item
            for item in self._adapters.values()
            if item.live and item.configured and capability in item.capabilities
        ]
        return live[0] if live else None

    def mark_failed(self, name: ProviderName) -> None:
        record_metric("provider.failed")
        publish("ProviderFailed", provider=name)

    def mark_recovered(self, name: ProviderName) -> None:
        record_metric("provider.recovered")
        publish("ProviderRecovered", provider=name)

    def snapshot(self) -> list[ProviderMetrics]:
        return [
            ProviderMetrics(item.name, item.health, 0, 0)
            for item in self._adapters.values()
        ]


_registry: ProviderRegistry | None = None


def get_provider_registry(*, force_reload: bool = False) -> ProviderRegistry:
    global _registry
    if _registry is None or force_reload:
        _registry = ProviderRegistry()
    return _registry
