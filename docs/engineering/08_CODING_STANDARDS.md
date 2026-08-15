# 08 — Coding Standards

Applies to every production file in this repository.

---

## TypeScript

- Strict. No `any` on new code. If a LiveKit type forces a cast, isolate it.  
- Prefer `type` for unions; `interface` for object shapes that may extend.  
- `app-config.ts` and `lib/brand.ts` stay the brand source.  
- `pnpm exec tsc --noEmit` must stay clean.

## Python

- 3.10+. `uv run` only. Never `pip install` for project deps.  
- Ruff: 88 columns, double quotes, space indent (`pyproject.toml`).  
- Type hints on public functions.  
- `uv run python -m pytest` — not bare `pytest`.

## React

- Server Components default. `"use client"` only when needed.  
- No new `useEffect` data fetching if a server component or existing route can do it.  
- Keys are stable ids, not array index, when the list can reorder.  
- Do not store utterances in React state beyond what LiveKit already shows in the live transcript UI.

## Naming

[14 Naming Convention](14_NAMING_CONVENTION.md). Honest names: `handoff` ≠ `reconnect`.

## Formatting

Frontend: project Prettier/ESLint (`pnpm lint`, `pnpm format:check`).  
Backend: `uv run ruff format` / `ruff check`.  
Do not fight the formatter.

## Comments

Why, not what. No commented-out graves.  
Constitutional constraints (no second pipeline, no transcript column) may be stated in one line at a dangerous call site.

## Imports

Frontend: `@/` alias. No deep imports into `agents-ui` internals from random features.  
Backend: package-relative within `src`. Dependency direction: tools do not import enterprise dashboards.

## Error handling

Structured. Speakable at the product edge.  
Python: typed errors in telephony/escalation style. Do not swallow.  
TS: do not `catch (e) {}` empty.  
No stack traces in the lesson UI.

## Logging

Event name + ids + error class.  
Forbidden: transcript, OTP, phone, API key, raw prompt body.

## Reusable code

Reuse `memory/`, `tools/`, `specialists/`, `components/ui`.  
Copy-paste of a service is a defect. Extract or import.

## Functions

One job. Side effects obvious.  
Tool functions stay validated through the manager.

## Classes

Services and repositories are classes. Agents extend LiveKit `Agent`.  
Do not add a God class in `agent.py`.

## Interfaces / enums

TS: enums for closed agent visualizer types already on `AppConfig`.  
Python: existing models/enums in specialists and analytics. New closed sets are enums or literals, not magic strings.

## Testing

[11 Testing Standard](11_TESTING_STANDARD.md).  
Tests live next to the contract: `backend/tests/`. Frontend tests when introduced follow the same privacy rules.

A PR that touches forget, fail-closed, or logs without tests is incomplete.
