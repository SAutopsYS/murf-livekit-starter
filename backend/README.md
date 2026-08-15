# Backend

Python LiveKit worker for SALORA OS. One Voice Pipeline: Deepgram STT, Gemini, Murf Falcon TTS.

Public guides: [../docs/guides/installation.md](../docs/guides/installation.md). Architecture: [../docs/architecture/backend.md](../docs/architecture/backend.md).

## Pipeline

```text
User speaks → Deepgram STT → Gemini → Murf Falcon TTS → LiveKit → User hears
```

LiveKit carries audio. `src/agent.py` constructs the session. Services under `src/services/` wrap the worker. They do not replace it.

## Setup

```bash
cd backend
uv sync
cp .env.example .env.local
```

Required keys: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `MURF_API_KEY`, `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`. Table: [docs/guides/configuration.md](../docs/guides/configuration.md).

```bash
uv run python src/agent.py download-files
uv run python src/agent.py dev
```

Console (no frontend): `uv run python src/agent.py console`.  
Production: `uv run python src/agent.py start`.

## Configuration

Pipeline, prompt, and Murf voice live in [`src/agent.py`](src/agent.py). Default voice is `Anisha`. Browse voices: [Murf Voice Library](https://murf.ai/api/docs/voices-styles/voice-library).

The product prompt is the Learning Tutor. Do not paste a second customer-support agent into this worker.

## Testing

```bash
uv run python -m pytest -q --ignore=tests/test_agent.py
uv run ruff check .
```

`tests/test_agent.py` is an LLM-as-judge suite and needs LiveKit. CI skips it.

## Docker

```bash
docker build -t salora-agent .
docker run --env-file .env.local salora-agent
```

Compose from the repo root is the supported path: [docs/guides/deployment.md](../docs/guides/deployment.md).

## Layout

```text
backend/
├── src/agent.py
├── src/memory/            # memory.db
├── src/knowledge/         # JSON lessons
├── src/specialists/       # SpecialistRouter
├── src/services/          # Facades
├── src/salora_platform/   # Auth, RBAC, health
├── tests/
├── Dockerfile
└── pyproject.toml
```

## License

MIT. See [LICENSE](LICENSE).
