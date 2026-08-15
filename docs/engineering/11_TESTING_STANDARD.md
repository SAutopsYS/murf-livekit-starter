# 11 — Testing Standard

Every module that can break a learner must be testable without a child.

---

## Unit testing

**Backend:** `backend/tests/`. Pytest via `uv run python -m pytest`.  
Router, confidence, recovery, validators, sanitizers, scoring — no network.  
**Frontend:** when added, colocate or `frontend/**/*.test.ts`. Do not mock LiveKit with a fake second pipeline.

## Integration testing

Memory DB, analytics store, tool manager + local dataset.  
Use temp SQLite. No production files.  
Next API routes that `execFile` Python: keep the contract (JSON, no utterance).

## Voice testing

Manual: start session, barge-in Stop, drop and resume — no new hello.  
Do not commit recorded learner audio.  
Automated voice e2e stays sandbox and synthetic.

## Agent testing

Existing LLM-as-judge tests in `backend/tests/test_agent.py` are the pattern for prompt/tool behavior.  
Specialist: handoff, handback, fail-closed, one retry, disabled guests do not route.  
A new guest ships with these tests or it stays disabled.

## UI testing

Critical paths: welcome primary, connect, ended, theme toggle visible, analytics/enterprise load.  
Prefer role and name queries. No screenshot-only as the sole gate.

## Accessibility testing

Keyboard to primary and theme. Focus visible.  
New controls: label in the same PR.  
`prefers-reduced-motion` must not hide meaning.

## Performance testing

[12 Performance Standard](12_PERFORMANCE_STANDARD.md).  
p95 first useful audio is a product number — measure in staging, not by guessing.  
Do not load-test with real child data.

## Regression testing

Kernel suite (fail-closed, forget, privacy logs, no-restart) runs on every backend PR that touches those trees.  
Do not delete tests to go green.

## CI requirements

Wired in `.github/workflows/ci.yml` and `scripts/ci.ps1`:

- `uv run ruff check`  
- `uv run python -m pytest --ignore=tests/test_agent.py`  
- `pnpm exec tsc --noEmit`  
- `pnpm lint`  
- `pnpm test` (Vitest: platform, learning, adaptive, fabric)  
- fail if a memory/analytics store adds `transcript` / `utterance` columns  

`tests/test_agent.py` (LLM-as-judge) stays manual / secret-gated.  

## Coverage goals

Kernel modules (router, recovery, memory forget, sanitizer, validator): high — aim ≥ 80% on those packages.  
Do not chase 100% on `agent.py` wiring at the cost of honest tests.  
Coverage is not a reason to log speech “for assertions.”

See [05 Backend Constitution](05_BACKEND_CONSTITUTION.md), [08 Coding Standards](08_CODING_STANDARDS.md).
