# Release

v1 is frozen. v2 is vision only.

| # | Document | Role |
| --- | --- | --- |
| 41 | [SALORA OS v1.0](41_SALORA_OS_V1_RELEASE.md) | Architecture freeze |
| 51 | [v2 Vision](51_SALORA_OS_V2_VISION.md) | Roadmap. No implementation |

## What v1 locked

One Voice Pipeline. One SpecialistRouter. One Search Platform. One Automation Platform. One event bus. One RBAC. Separate `memory.db` and `analytics.db`.

## What comes next (consume, do not rewrite)

1. Identity and `AUTH_REQUIRED=true` after a roster exists
2. Studio editor / Whiteboard renderer / Graph view as instruments
3. Queue behind `JOB_CATALOG`
4. OTel exporter
5. Signed plugin crypto
6. Mobile and desktop implementations of existing contracts

Phase history: [salora/IMPLEMENTATION.md](../salora/IMPLEMENTATION.md).
