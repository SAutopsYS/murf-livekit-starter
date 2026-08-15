# SALORA OS — Evidence inventory

Official repo: https://github.com/SAutopsYS/SALORA-OS.git

**Not benchmarked in this validation run.**

Screenshots were taken from the running hall at http://127.0.0.1:3000 with system Chrome. No generated mock UI.

---

## Inventory

| File | Category | Feature | What it proves | Public-safe | Status |
| --- | --- | --- | --- | --- | --- |
| `docs/assets/voice/hall-ready.png` | Voice | Hall | Real home / Enter the hall | YES | **VERIFIED** |
| `docs/assets/voice/hall-session.png` | Voice | Session start | Real mic-permission view after Enter the hall | YES | **VERIFIED** (start state). Listening/speaking wave still **CAPTURE REQUIRED** (needs a human mic) |
| `docs/assets/product/analytics.png` | Product | `/analytics` | Real Voice Agent Analytics UI (empty/loading zeros) | YES | **VERIFIED** |
| `docs/assets/product/enterprise.png` | Product | `/enterprise` | Real Control Center + Role selector | YES | **VERIFIED** |
| `docs/architecture/diagrams.md` | Architecture | System / pipeline / agent / tools | Mermaid from the implementation | YES | **VERIFIED** |
| Root README §16–19 | Architecture | Structure | Text + Mermaid | YES | **VERIFIED** |
| Pytest / vitest / tsc / ruff | Testing | Suites | Commands in CI and README | YES | **VERIFIED** (no terminal PNG) |
| `frontend/public/salora-mark.svg` | Brand | Logo | Mark | YES | **VERIFIED** |

Live listening/speaking wave with Murf audio: **CAPTURE REQUIRED** (headless Chrome has no microphone; LiveKit session does not fully join).

Recordings / demo clips: **not found**.

---

## Security review of PNGs

Inspected before keeping:

- No API keys, tokens, passwords, LiveKit/Murf secrets, phone numbers, emails, or caller data.
- Analytics shows zeros / “Loading analytics,” not learner speech.
- Hall footer credits “Built by Saloni Saini” and Murf Falcon — public product copy, not a leaked secret.
- Next.js dev badge may appear on the mic-permission shot. Not a secret.

---

## Voice uniqueness (source)

One Voice Pipeline. One `SpecialistRouter`. One `ProviderRegistry`. Orchestrator is not imported from `agent.py`.
