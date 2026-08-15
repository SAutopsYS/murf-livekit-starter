"""Liveness and readiness for containers and CI. Does not start the agent."""

from __future__ import annotations

import json
import sys

from salora_platform.config import get_platform_config
from salora_platform.observability import heartbeat, metric_snapshot


def check_liveness() -> dict[str, object]:
    heartbeat("backend")
    return {"status": "ok", "service": "salora-agent"}


def check_readiness() -> dict[str, object]:
    config = get_platform_config()
    checks = {
        "livekit": config.livekit_ready,
        "murf": config.murf_ready,
        "stt": config.stt_ready,
        "llm": config.llm_ready,
    }
    ready = all(checks.values())
    return {
        "status": "ready" if ready else "degraded",
        "service": "salora-agent",
        "profile": config.profile,
        "checks": checks,
        "providers": config.provider_status(),
        "metrics": metric_snapshot(),
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    payload = check_readiness() if "--ready" in args else check_liveness()
    print(json.dumps(payload))
    if payload["status"] in {"ok", "ready", "degraded"}:
        # Degraded is a running worker missing optional keys — still alive.
        return 0 if payload["status"] != "degraded" or "--ready" not in args else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
