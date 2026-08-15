# 10 — README Standard

How README files are written in this repository.

Root README is the public front door. Package READMEs (`frontend/`, `backend/`) are how to run that package.

---

## Structure (required order)

Root README is the public front door. Use this order:

1. Name and one-line promise
2. Vision
3. Features
4. Architecture overview (short; link [architecture/overview.md](../architecture/overview.md))
5. Technology stack
6. Folder structure
7. Quick start
8. Installation (or link [guides/installation.md](../guides/installation.md))
9. Environment variables (or link [guides/configuration.md](../guides/configuration.md))
10. Running
11. Testing
12. Documentation index
13. Contributing — [09 Git Workflow](09_GIT_WORKFLOW.md)
14. License

Challenge history lives in [VOICEFORBHARAT.md](../salora/VOICEFORBHARAT.md). It must not bury how to run.

Package READMEs (`frontend/`, `backend/`) stay how-to-run for that package.

## Screenshots

Optional. If used: current SALORA hall, not a mock. Alt text. No child faces. No transcript of a real learner.

## Architecture

Prefer a small pipeline block:

```text
User speaks → Deepgram STT → Gemini → Murf Falcon TTS → LiveKit → User hears
```

Link [06 AI Architecture Bible](06_AI_ARCHITECTURE_BIBLE.md). Do not paste the entire specialist graph into every README.

## Setup

Copy-pasteable. Windows and Unix if both scripts exist (`start_app.ps1`, `start_app.sh`).  
`uv sync` / `uv run`. `pnpm install` / `pnpm dev`.  
First-time `download-files` called out.

## Security

`.env` / `.env.local` gitignored.  
`.env.example` placeholders only.  
Say: no transcripts in logs or dashboards.

## Environment variables

Table: name, required, purpose.  
`LIVEKIT_*`, `MURF_API_KEY`, `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`, optional `AGENT_NAME`.  
Never paste a live key into README.

## Contributing

Point to engineering foundation and Master Constitution.  
“Reuse before rewrite.”

## Roadmap

Milestones, not press. Phase 2 = design system on existing UI. Voice kernel stays.

## Style

Complete sentences. No decorative dash separators as section rules.  
Caveman-tight is fine. Marketing fluff is not.  
Do not claim “world’s first” in a package README without the product name next to it — once at the root is enough.
