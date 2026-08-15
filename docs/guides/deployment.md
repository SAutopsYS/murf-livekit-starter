# Deployment

Dev path: `start_app.ps1` / `start_app.sh`.  
Production-shaped path: Docker Compose. Do not invent a third orchestrator.

Canonical: [22 Production Platform](../engineering/22_PRODUCTION_PLATFORM.md).

## Compose

```bash
docker compose up --build
```

- Frontend: `:3000`
- Backend: LiveKit worker (no public HTTP)
- SQLite: volume `salora-data` → `/app/data`

Env files: `frontend/.env.local` and `backend/.env.local`. Root `.env` may set `SALORA_PROFILE` and `AUTH_REQUIRED`.

## Health

| Check | URL / command |
| --- | --- |
| Frontend liveness | `GET /api/health` |
| Frontend readiness | `GET /api/ready` (LiveKit env present) |
| Worker liveness | `uv run python -m salora_platform.health` |
| Worker readiness | `uv run python -m salora_platform.health --ready` |

## Profiles

`development` → `staging` → `production`. Keep `AUTH_REQUIRED=false` until identity is issued.

## Rollback

Previous image tag + previous env. Compose uses `restart: unless-stopped`. LiveKit rooms stick to the worker that accepted the job. Scale workers horizontally. Do not interrupt an in-flight room.

## CI

`.github/workflows/ci.yml`:

- Backend: `uv sync`, ruff, pytest (skips live LLM judge `test_agent.py`)
- Frontend: tsc, lint, vitest, production build
- Privacy: forbids utterance/transcript columns in memory and analytics

Local: `scripts/ci.ps1` or `scripts/ci.sh`.

## What is not in the image

Secrets. Real `.env.local`. Speech lakes. A second Voice Pipeline.
