#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"

cd "$root/backend"
uv run ruff check .
uv run python -m pytest -q --ignore=tests/test_agent.py

cd "$root/frontend"
pnpm exec tsc --noEmit
pnpm lint
pnpm test
