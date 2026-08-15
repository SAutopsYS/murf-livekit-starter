# AGENTS.md

Monorepo for SALORA OS: a voice learning product on LiveKit Agents and Murf Falcon TTS.

Public docs: [docs/README.md](docs/README.md). Do not add a second Voice Pipeline, SpecialistRouter, Search Platform, or Automation Platform.

## Repository structure

```text
├── backend/                 # Python worker
│   ├── src/agent.py         # Voice Pipeline
│   └── tests/               # pytest (CI skips live LLM judge)
├── frontend/                # Next.js hall + instruments
│   ├── app/
│   ├── components/
│   └── app-config.ts
├── docs/                    # Architecture, guides, archive
├── start_app.sh
└── start_app.ps1
```

## Backend

### Tech stack

- Python 3.10+ with uv
- LiveKit Agents SDK (`livekit-agents ~1.4`)
- Murf Falcon (`livekit-murf`)
- Deepgram Nova-3
- Google Gemini
- Silero VAD + LiveKit turn detector

### Key file: `backend/src/agent.py`

- `SYSTEM_PROMPT`: Learning Tutor behavior
- `Assistant`: tools via `@function_tool`
- `my_agent()`: STT → LLM → TTS and LiveKit connect
- `prewarm()`: Silero VAD

### Running the backend

```bash
cd backend
uv sync
uv run python src/agent.py download-files
uv run python src/agent.py dev
uv run python src/agent.py console
```

### Environment variables

Copy `backend/.env.example` to `backend/.env.local`. Required: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `MURF_API_KEY`, `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`.

### Code style

```bash
uv run ruff check .
uv run ruff format .
```

88 char line, double quotes, space indent.

### Testing

```bash
uv run python -m pytest -q --ignore=tests/test_agent.py
```

`tests/test_agent.py` is LLM-as-judge and needs LiveKit. CI skips it. When changing the prompt or tools, add tests first.

Always `uv sync` / `uv run`. Never `pip install`.

## Frontend

### Tech stack

Next.js, TypeScript, pnpm, LiveKit Agents UI, Tailwind.

### Key files

- `frontend/app-config.ts` and `frontend/lib/brand.ts`
- `frontend/app/page.tsx` (hall)
- `frontend/app/api/token/route.ts`
- `frontend/components/os/` (Workspace Shell)
- `frontend/components/app/` (hall views)

### Running the frontend

```bash
cd frontend
pnpm install
pnpm dev
```

### Environment variables

Copy `frontend/.env.example` to `frontend/.env.local`. Required: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`. Optional: `AGENT_NAME=my-agent`.

### Linting

```bash
pnpm lint
pnpm exec tsc --noEmit
pnpm test
```

## Common tasks

### Change what the agent does

Edit `SYSTEM_PROMPT` in `backend/src/agent.py`. Keep the Learning Tutor. Do not paste a second product prompt as a second pipeline.

### Change the voice

Edit `voice` in `murf.TTS(...)` in `agent.py`. Library: https://murf.ai/api/docs/voices-styles/voice-library

### Add a tool

Add a method on `Assistant` with `@function_tool`. Import `function_tool` and `RunContext` from `livekit.agents`.

### Switch the LLM

Replace `llm=google.LLM(...)`. For OpenAI: `livekit-agents[openai]`, `OPENAI_API_KEY`, `openai.LLM(...)`. Same Voice Pipeline.

### Change frontend branding

`frontend/lib/brand.ts` and `frontend/app-config.ts` together. Tokens: `frontend/styles/tokens.css`.

## Documentation

- [docs/README.md](docs/README.md)
- [docs/guides/installation.md](docs/guides/installation.md)
- [docs/architecture/overview.md](docs/architecture/overview.md)
- Murf Falcon: https://murf.ai/api/docs/text-to-speech/streaming
- LiveKit Agents: https://docs.livekit.io/agents
- Deepgram: https://developers.deepgram.com
