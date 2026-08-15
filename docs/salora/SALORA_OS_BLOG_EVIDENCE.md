# SALORA OS — Blog evidence map

Current test run: 15 August 2026. `pnpm build` was not re-run in this pass.

| Blog section | Repository evidence | Evidence file | Verified |
| --- | --- | --- | --- |
| Hall / Enter the hall | `frontend/app/page.tsx`, `welcome-view.tsx` | `docs/assets/voice/hall-ready.png` | **VERIFIED** |
| Mic permission after start | Session views | `docs/assets/voice/hall-session.png` | **VERIFIED** (not speaking) |
| Listening / speaking wave | LiveKit session + wave | — | **CAPTURE REQUIRED** |
| Analytics | `frontend/app/analytics` | `docs/assets/product/analytics.png` | **VERIFIED** (loading / zeros) |
| Enterprise / RBAC UI | `frontend/app/enterprise` | `docs/assets/product/enterprise.png` | **VERIFIED** (empty cards) |
| Voice pipeline | `backend/src/agent.py` `my_agent` | blog Mermaid | **VERIFIED** |
| OS architecture diagram | hall + worker + dashed facades | blog Mermaid | **VERIFIED** |
| Specialist routing | `specialists/router.py`, `recovery.py` | blog Mermaid | **VERIFIED** |
| Tool calling | `AGENT_TOOLS` in `agent.py` | blog Mermaid | **VERIFIED** |
| Math handoff | `specialists/handoff.py` | tests | **VERIFIED** |
| Orchestrator not in audio | no import in `agent.py` | source | **VERIFIED** |
| Learning tools | `get_next_exercise`, `score_spoken_answer`, `recommend_next_practice` | `backend/src` tools | **VERIFIED** |
| Learning / Adaptive engines | `frontend/lib/learning`, `frontend/lib/adaptive` | providers not on hall | **VERIFIED** architected |
| Knowledge JSON | `knowledge/resources/english_basics.json` | tool | **VERIFIED** |
| Knowledge Fabric | `frontend/lib/knowledge-fabric` | not on audio hop | **VERIFIED** architected |
| Pytest 434 | `uv run python -m pytest -q --ignore=tests/test_agent.py` | this run | **VERIFIED** |
| Vitest 25 | `pnpm test` | this run | **VERIFIED** |
| tsc | `pnpm exec tsc --noEmit` exit 0 | this run | **VERIFIED** |
| Ruff | `uv run ruff check .` | this run | **VERIFIED** |
| ESLint | `pnpm lint` exit 0 + warnings | this run | **VERIFIED** |
| Latency ms | — | — | Not benchmarked |
| Windows standalone EPERM | `next.config.ts` `output: 'standalone'` | prior report, not re-run | Prior observation |
| GitHub | official remote | https://github.com/SAutopsYS/SALORA-OS.git | **VERIFIED** URL |
| LinkedIn profile | provided | https://www.linkedin.com/in/saloni-saini-aa7133252/ | Link only |
| Medium URL | — | `BLOG_URL_HERE` | **CAPTURE REQUIRED** |
