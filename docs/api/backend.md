# Backend HTTP and health

The Python worker is not a public REST server. Browser HTTP lives on Next.js. The worker exposes health as a module.

## Next.js routes

| Route | Purpose | Notes |
| --- | --- | --- |
| `POST /api/token` | LiveKit room token | CSRF + rate limit. Anonymous voice by design |
| `GET /api/health` | Liveness | Used by Compose |
| `GET /api/ready` | Readiness | 503 if LiveKit env missing |
| `GET /api/analytics` | Dashboard summary | `analytics.read` when auth is on |
| `GET /api/analytics/export` | Privacy-safe export | `analytics.export` |
| `GET /api/enterprise` | Control Center payload | `enterprise.read` |
| `GET /api/enterprise/export` | Enterprise export | `enterprise.export` |

Routes wrap `platformRoute` (RBAC, rate limit, metrics). They exec existing Python CLIs. They do not reimplement analytics.

## Worker health

```bash
cd backend
uv run python -m salora_platform.health
uv run python -m salora_platform.health --ready
```

`--ready` exits non-zero when LiveKit / Murf / STT / LLM keys are missing.

## Service envelopes

Internal services return `ApiEnvelope` v1 (`ok`, `fail`, `paginate`). See [sdk.md](sdk.md).

## Related

- [29 AI SDK](../engineering/29_AI_SDK_PLATFORM.md)
- [22 Production Platform](../engineering/22_PRODUCTION_PLATFORM.md)
