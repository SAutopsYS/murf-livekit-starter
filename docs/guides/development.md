# Development

Reuse before rewrite. The Voice Pipeline stays in `backend/src/agent.py`.

## Tests

Backend (from `backend/`):

```bash
uv run python -m pytest -q --ignore=tests/test_agent.py
uv run ruff check .
uv run ruff format .
```

`tests/test_agent.py` is an LLM-as-judge suite. It needs LiveKit credentials and is skipped in CI.

Frontend (from `frontend/`):

```bash
pnpm exec tsc --noEmit
pnpm lint
pnpm test
```

## Git

See [09 Git Workflow](../engineering/09_GIT_WORKFLOW.md).

- `main` stays runnable
- `docs/<short>` for documentation-only work
- Do not commit `.env.local` or `scripts/node_modules`

## Brand in code

Change pulse or name in `frontend/lib/brand.ts` and `frontend/app-config.ts` together. Tokens: `frontend/styles/tokens.css`.

## Do not

- Add a second Voice Pipeline
- Add a second SpecialistRouter, Search Platform, or Automation Platform
- Store transcripts on dashboards
- Replace LiveKit or Murf Falcon
- Mount Studio, Marketplace, or Education on the hall

## Read first

1. [Architecture overview](../architecture/overview.md)
2. [Master Constitution](../salora/00-master-constitution.md)
3. [Engineering foundations](../engineering/foundations.md)
