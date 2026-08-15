# Contributing

Reuse before rewrite. The Voice Pipeline stays in `backend/src/agent.py`.

## Before you change code

1. Read [docs/architecture/overview.md](docs/architecture/overview.md).
2. Read [docs/guides/development.md](docs/guides/development.md).
3. If the change touches product law, read [docs/salora/00-master-constitution.md](docs/salora/00-master-constitution.md).

## Do not

- Add a second Voice Pipeline, SpecialistRouter, Search Platform, or Automation Platform
- Store transcripts, utterances, or OTPs in `memory.db` or `analytics.db`
- Join those two databases by learner identity
- Mount Studio, Marketplace, or Education on the hall
- Enable marketplace `may_execute` or autonomous agent loops
- Commit `.env.local`, live keys, or `scripts/node_modules`

## Setup

Follow [docs/guides/installation.md](docs/guides/installation.md).

## Checks

```bash
cd backend
uv run ruff check .
uv run python -m pytest -q --ignore=tests/test_agent.py
```

```bash
cd frontend
pnpm exec tsc --noEmit
pnpm lint
pnpm test
```

Or from the repo root: `scripts/ci.sh` / `scripts/ci.ps1`.

`tests/test_agent.py` needs LiveKit and an LLM judge. CI skips it. Do not require it for a docs or facade change.

## Pull requests

- Keep `main` runnable
- One concern per PR when you can
- Label what is implemented vs architected vs planned
- Git process: [docs/engineering/09_GIT_WORKFLOW.md](docs/engineering/09_GIT_WORKFLOW.md)

## License

MIT. See [LICENSE](LICENSE). Starter copyright remains Murf Inc.
