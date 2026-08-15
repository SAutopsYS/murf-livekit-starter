# SALORA OS — Blog research (not the article)

Source of truth for the public technical post. Claims that could not be proven were left out of the article.

## Title options (not in the Medium body)

1. Building SALORA OS: one LiveKit room, one Murf mouth, and a hard no on a second pipeline *(selected)*
2. I kept one Voice Pipeline. Everything else had to consume it.
3. SALORA OS: a Hindi–English voice tutor that does not store what you said
4. From `agent.py` to an OS layer without adding a second TTS
5. What I actually shipped: Deepgram, Gemini, Murf Falcon, and two SQLite files that never join

## What it is

Voice-first learning hall. Browser + LiveKit Cloud + Python worker `my-agent`. Spoken identity: AI Voice Learning Tutor. Chrome: SALORA OS.

## Implemented

Hall voice; Deepgram nova-3 `multi`; Gemini 3.5 Flash Lite; Murf Falcon `Anisha`; `AGENT_TOOLS` (memory, knowledge, exercise, score, recommend, escalation, math handoff); two SQLite files; `/analytics`; `/enterprise`; `SpecialistRouter` (math live); `OsShell`; CI privacy grep; chat input on.

## Architected (not in the audio hop)

`AIOrchestrator`, `AgentRuntimeService`, Search/Automation facades, Learning/Adaptive/Fabric projections and providers (not mounted on the hall), Marketplace catalog (`may_execute` false), Studio/Whiteboard models.

## Planned (doc 41)

Identity + `AUTH_REQUIRED=true`, `JOB_CATALOG` queue, OTel, plugin signing, mobile/desktop of existing contracts.

## Current tests (15 August 2026)

| Check | Result |
| --- | --- |
| Pytest `--ignore=tests/test_agent.py` | 434 passed in 19.40s |
| Ruff | All checks passed |
| `tsc --noEmit` | exit 0 |
| Vitest | 25 passed / 17 files |
| ESLint `next lint` | exit 0, starter-kit warnings |
| `pnpm build` | not re-run this pass |

## Evidence

| Path | Status |
| --- | --- |
| `docs/assets/voice/hall-ready.png` | VERIFIED |
| `docs/assets/voice/hall-session.png` | VERIFIED (mic permission, not speaking) |
| `docs/assets/product/analytics.png` | VERIFIED (loading / zeros) |
| `docs/assets/product/enterprise.png` | VERIFIED (empty cards) |
| Listening/speaking PNG | CAPTURE REQUIRED |
| Latency number | Not benchmarked |
| Medium URL | CAPTURE REQUIRED (`BLOG_URL_HERE`) |

## Intentionally excluded

Millisecond TTS bake-off. HIPAA as a claimed certification. Teacher/parent pages. Autonomous loops. Kafka. “World’s first” as a product claim (the hall hero copy still says it; the article treats that as UI text). Cursor/AI-as-author. Day-by-day challenge diary. Shell `⌘K` as a Search Platform product. Video/screenshare flags in `app-config.ts` as shipped voice features. Math guest constructing its own `murf.TTS` (it stays in the same session). LearningProvider / AdaptiveProvider as hall UI. `pnpm build` as a current-run result.

## Key files

`backend/src/agent.py`, `specialists/router.py`, `specialists/recovery.py`, `specialists/handoff.py`, `memory/`, `analytics/`, `knowledge/`, `frontend/app/api/token/route.ts`, `frontend/app/page.tsx`.
