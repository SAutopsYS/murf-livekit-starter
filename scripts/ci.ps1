$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Set-Location "$root\backend"
uv run ruff check .
uv run python -m pytest -q --ignore=tests/test_agent.py

Set-Location "$root\frontend"
pnpm exec tsc --noEmit
pnpm lint
pnpm test
