# SALORA OS — Showcase pack

Public-review notes. VoiceForBharat submission artifacts stay in `DAY10_BLOG.md` and `DAY10_LINKEDIN.md`. Nothing here invents a feature.

**Implemented** — hall, worker, or instrument.  
**Architected** — facade or contract; not the live audio path.  
**Planned** — [41 SALORA OS v1](../engineering/41_SALORA_OS_V1_RELEASE.md) only.

---

## 1. Repository improvement report

### What was already solid

- Monorepo split (`backend/`, `frontend/`, `docs/`) matches how the product runs: two processes, one LiveKit room.
- `AGENTS.md` and package READMEs tell an agent (or a human) where the mouth lives.
- `.env.example` files use placeholders. `.env.*` is gitignored except examples.
- CI: ruff, pytest (judge skipped), tsc, lint, vitest, production build, privacy grep.
- Compose volume `salora-data` persists SQLite.

### What was confusing (and what we did)

| Finding | Action |
| --- | --- |
| Root README was accurate but thin on limitations, roadmap, contact | Rewrote [README.md](../../README.md) |
| No `CONTRIBUTING.md` / `CHANGELOG.md` | Added both from existing law + `git log` |
| Setup lived in a short install page | Expanded [guides/installation.md](../guides/installation.md) |
| Diagrams were scattered in Day 10 drafts | Canonical [architecture/diagrams.md](../architecture/diagrams.md) |
| `scripts/node_modules` (Playwright leftover) | Documented in `scripts/README.md`; gitignored |
| No screenshots in `docs/assets/` | Left empty on purpose. Capture list below |
| 51 numbered engineering files | Kept. Public index already in [docs/README.md](../README.md) |
| GitHub identity | Official remote is `https://github.com/SAutopsYS/SALORA-OS.git` |
| LICENSE copyright Murf Inc | Unchanged. README states starter vs product work |
| OS layer largely uncommitted vs `origin/main` Day 9 | Called out. Push is a human step |

### Do not delete

`docs/engineering/01`–`51` and `docs/salora/00`–`25` stay. Discoverability is the index, not a purge.

### Still messy (accepted)

- Local folder may still be named `Amurf-livekit-starter`. Public GitHub is `SALORA-OS`.
- `scripts/package.json` still lists Playwright. Not a product suite.
- `frontend/app-config.ts` pageDescription may still say “world’s first.” Copy leftover. Not a pipeline bug.
- `__pycache__` / pytest caches can appear locally. Backend gitignore covers the usual ones.

---

## 2. Documentation improvement report

### Before

Public map existed (`docs/README.md`). Day 10 lived as four drafts (brief, intro, features, architecture, journey). Install guide stopped at “open localhost.” No contribution file. No changelog. Diagrams only inside a draft chapter.

### After

| Document | Change |
| --- | --- |
| Root README | Production sections: capabilities, limits, roadmap, contact |
| `docs/guides/installation.md` | Clone → keys → verify → debug |
| `docs/architecture/diagrams.md` | All Mermaid maps |
| `docs/salora/DAY10_BLOG.md` | Combined post |
| `docs/salora/DAY10_LINKEDIN.md` | Copy-ready post |
| `CONTRIBUTING.md` / `CHANGELOG.md` | Process + recorded days |
| Indexes | This file + blog + diagrams linked |

### Status labels

Every public page should keep three words: **Implemented / Architected / Planned**. Drafts already used them. The final blog and README do too.

### Not rewritten

Constitutions and numbered engineering files. They are law and archive. Guides point at them.

---

## 3. Production README

Canonical file: [../../README.md](../../README.md).

---

## 4. Setup guide

Canonical file: [../guides/installation.md](../guides/installation.md).

---

## 5. Evidence checklist

### Exists in the repo (use these)

| Evidence | Where |
| --- | --- |
| Voice Pipeline construction | `backend/src/agent.py` (`my_agent`, TTS/STT/LLM kwargs) |
| Token mint | `frontend/app/api/token/route.ts` |
| Hall route | `frontend/app/page.tsx` |
| Memory schema | `backend/src/memory/repository.py` |
| Analytics schema (no speech) | `backend/src/analytics/repository.py` |
| Specialist retry | `backend/src/specialists/recovery.py` |
| Event redact | `backend/src/services/events.py` |
| Env placeholders | `backend/.env.example`, `frontend/.env.example` |
| CI + privacy job | `.github/workflows/ci.yml` |
| Compose volume | `docker-compose.yml` |
| Day history | `git log`; [VOICEFORBHARAT.md](VOICEFORBHARAT.md); [CHANGELOG.md](../../CHANGELOG.md) |
| Architecture prose | [overview.md](../architecture/overview.md) |
| Mermaid | [diagrams.md](../architecture/diagrams.md) |
| Test inventory | `backend/tests/*`, `frontend` vitest |
| Validation counts | Last local pass: 434 / 25 (re-run before you submit) |
| Brand marks | `frontend/public/salora-mark.svg` (logo, not a hall screenshot) |

### Does not exist — capture before you publish

Do not invent images. Suggested files for [../assets/](../assets/README.md):

| File | What to show | Rules |
| --- | --- | --- |
| `hall-ready.png` | Hall, Enter the hall | Current UI. No child faces |
| `hall-session.png` | Wave + listening/speaking | No real-learner transcript overlay |
| `analytics.png` | `/analytics` after a **your** test call | Export must show no speech |
| `enterprise.png` | `/enterprise` | Same |
| `worker-registered.png` | Terminal: `agent_name: my-agent` | Redact keys if any line leaked |
| `pytest.png` | `434 passed` (or current count) | Fresh run |

### Terminal output you may quote

```text
uv run python src/agent.py dev
# wait for registered worker, agent_name: my-agent
```

```text
uv run python -m pytest -q --ignore=tests/test_agent.py
```

```text
pnpm test
```

Do not paste live API keys. Do not paste a real learner utterance.

### Code snippets safe to quote

- `murf.TTS(voice="Anisha", ...)` and `deepgram.STT(model="nova-3", language="multi")` from `agent.py`
- Pipeline ASCII from the README
- `AUTH_REQUIRED` default false from config docs
- Privacy CI grep from `.github/workflows/ci.yml`

---

## 6. Mermaid diagrams

Canonical file: [../architecture/diagrams.md](../architecture/diagrams.md).

Includes: overall, voice, agent, knowledge, search, automation, event bus, auth, RBAC, enterprise isolation, repo structure.

---

## 7. Final blog

Canonical file: [DAY10_BLOG.md](DAY10_BLOG.md).

Draft chapters remain as VoiceForBharat sources: `DAY10_INTRODUCTION.md`, `DAY10_FEATURES.md`, `DAY10_ARCHITECTURE.md`. Journey: [SALORA_OS_ENGINEERING_JOURNEY.md](SALORA_OS_ENGINEERING_JOURNEY.md).

---

## 8. LinkedIn post

Canonical file: [DAY10_LINKEDIN.md](DAY10_LINKEDIN.md).

Required lines included: Murf Falcon product line, “10 Days of Voice Agents – VoiceForBharat Edition”, #VoiceForBharat, Murf AI tag, repo CTA. No invented latency number.

---

## 9. Submission checklist

Human steps. Docs cannot tick “published” for you.

| Item | State | Notes |
| --- | --- | --- |
| Blog written | Done in-repo | [DAY10_BLOG.md](DAY10_BLOG.md). Still need to paste to the contest / Medium / Hashnode if required |
| Repository public | **You** | Remote exists. Confirm GitHub visibility. Commit/push local OS + docs first |
| README polished | Done | [README.md](../../README.md) |
| Architecture diagrams | Done | Mermaid. Export PNG only if the form wants images |
| Screenshots added | **You** | None in `docs/assets/` yet |
| Code snippets verified | Done | Match `agent.py` / token route / schemas |
| API keys removed | Done | Examples are placeholders. Do not commit `.env.local` |
| `.env` ignored | Done | Root + package gitignores |
| Tests passing | **Re-run** | Last recorded 434 / 25. Run `scripts/ci.sh` before submit |
| Documentation complete | Done for showcase | Indexes updated |
| LinkedIn post ready | Done in-repo | [DAY10_LINKEDIN.md](DAY10_LINKEDIN.md). Not posted |
| Submission form ready | **You** | Use facts from the blog + this checklist |

### Form copy (safe)

- **Name:** SALORA OS / AI Voice Learning Tutor
- **Track:** Learning & Literacy
- **TTS:** Murf Falcon (`Anisha`)
- **Transport:** LiveKit Agents
- **Repo:** https://github.com/SAutopsYS/SALORA-OS
- **One sentence:** A voice tutor that practices with you in Hindi and English, remembers only with consent, and never stores what you said.

---

## 10. Final Day 10 readiness report

### Ready

- Voice path is one `AgentSession`. Docs and diagrams match that.
- Implemented vs architected vs planned is labeled in README, blog, and diagrams.
- Privacy story matches schema + CI.
- Setup guide matches `uv` / `pnpm` / Compose / `start_app.*`.
- LinkedIn copy does not invent a benchmark.
- No `TODO`/`FIXME` in `backend/src`. Future list is doc 41.

### Blockers for a public form (not code)

1. **Commit and push** the local OS layer and docs. `origin/main` last commit is still Day 9.
2. **Confirm the GitHub repo is public.**
3. **Capture screenshots** of the current hall. Do not use starter mocks.
4. **Re-run CI locally** and paste current counts if they changed.
5. **Publish the blog** to whatever URL the form asks for.
6. **Post LinkedIn** and tag Murf AI.

### Quality review (this pass)

| Check | Result |
| --- | --- |
| Grammar / tone | Human engineer voice in blog and LinkedIn |
| Architecture consistency | Voice diagrams exclude orchestrator hop |
| Feature verification | Hall features match `AGENT_TOOLS` + Day 9 routes |
| Secrets | No live keys in docs |
| Duplicate systems | Still forbidden in CONTRIBUTING / AGENTS.md |
| Broken image refs | None added (no PNGs to break) |
| LICENSE | Still Murf Inc MIT — stated, not silently changed |

### Score (honest)

| Surface | Readiness | Why not 100 |
| --- | --- | --- |
| Code kernel (Days 1–9) | High | Live judge and soak not in CI |
| Local OS + docs | High if you push | Uncommitted vs origin |
| Public showcase | Medium until you capture media and publish | Screenshots, push, form, LinkedIn |

Ship the hall. Then tick the human boxes.
