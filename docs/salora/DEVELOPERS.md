# Developer onboarding

This repo is a working voice learning product. Constitutions live in `docs/salora/`. How-to lives in `docs/guides/`. Code lives in `frontend/` and `backend/`.

## Run

See [../guides/installation.md](../guides/installation.md).

```bash
# backend
cd backend
uv sync
uv run python src/agent.py download-files   # first time
uv run python src/agent.py dev

# frontend
cd frontend
pnpm install
pnpm dev
```

Or `start_app.ps1` / `start_app.sh` from the root.

Copy `backend/.env.example` → `backend/.env.local` and `frontend/.env.example` → `frontend/.env.local`.

## Do not

- Add a second Voice Pipeline
- Store transcripts on dashboards
- Replace LiveKit or Murf Falcon
- Skip tests on forget, fail-closed, or privacy logs

## Read first

1. [Master Constitution](00-master-constitution.md)
2. [Architecture overview](../architecture/overview.md)
3. [Engineering foundations](../engineering/foundations.md)
4. [Brand](BRAND.md)
5. [Implementation plan](IMPLEMENTATION.md)

## Tests

See [../guides/development.md](../guides/development.md).

```bash
cd backend
uv run python -m pytest -q --ignore=tests/test_agent.py
```

```bash
cd frontend
pnpm lint
pnpm exec tsc --noEmit
pnpm test
```

## Brand in code

Change pulse or name in `frontend/lib/brand.ts` and `frontend/app-config.ts` together. CSS tokens are in `frontend/styles/tokens.css`.
