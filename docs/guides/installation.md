# Installation and setup

Run the hall on your machine. Frontend and backend do not stream audio to each other. Both join [LiveKit Cloud](https://cloud.livekit.io/).

If something fails after first run, use [troubleshooting.md](troubleshooting.md).

## Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| Python | 3.10+ (CI uses 3.12) | Worker |
| [uv](https://docs.astral.sh/uv/) | current | Backend deps. Do not use `pip install` |
| Node.js | 18+ (CI uses 22) | Next.js |
| [pnpm](https://pnpm.io/) | current | Frontend deps |
| LiveKit Cloud project | — | Room + agent dispatch |
| API keys | — | Murf, Deepgram, Google Gemini |

Optional: [LiveKit CLI](https://docs.livekit.io/home/cli) (`lk`) to write LiveKit env files. Optional: Docker + Compose for the shaped deploy path.

## 1. Clone

```bash
git clone https://github.com/SAutopsYS/SALORA-OS.git
cd SALORA-OS
```

Use your fork URL if you forked.

## 2. Environment files

```bash
cp backend/.env.example backend/.env.local
cp frontend/.env.example frontend/.env.local
```

Do not commit `.env.local`. Root `.env.example` only sets compose profile flags (`SALORA_PROFILE`, `AUTH_REQUIRED`). Secrets stay in the package files.

Full table: [configuration.md](configuration.md).

## 3. API keys

Placeholders only in git. Fill real values locally.

| Variable | Where | Get it |
| --- | --- | --- |
| `LIVEKIT_URL` | backend + frontend | [LiveKit Cloud](https://cloud.livekit.io/) → project → Settings |
| `LIVEKIT_API_KEY` | both | same |
| `LIVEKIT_API_SECRET` | both | same |
| `MURF_API_KEY` | backend | [Murf API dashboard](https://murf.ai/api/dashboard) |
| `DEEPGRAM_API_KEY` | backend | [Deepgram](https://deepgram.com) |
| `GOOGLE_API_KEY` | backend | [Google AI Studio](https://aistudio.google.com/apikey) |

Frontend optional: `AGENT_NAME=my-agent` for explicit dispatch.

LiveKit helper:

```bash
lk cloud auth
lk app env -w -d backend/.env.local
```

Copy the same three LiveKit values into `frontend/.env.local`.

`AUTH_REQUIRED` defaults to `false`. Leave it there so anonymous voice works.

Optional later: `ESCALATION_WEBHOOK_URL`, `LIVEKIT_SIP_OUTBOUND_TRUNK_ID`, Twilio vars. The hall talks without them.

## 4. Backend

```bash
cd backend
uv sync
uv run python src/agent.py download-files
```

`download-files` pulls Silero VAD and the LiveKit turn detector. First time only.

Start the worker:

```bash
uv run python src/agent.py dev
```

Wait until you see a registered worker and `agent_name: my-agent`.

Other modes:

| Mode | Command |
| --- | --- |
| Reload (dev) | `uv run python src/agent.py dev` |
| Production process | `uv run python src/agent.py start` |
| Console, no UI | `uv run python src/agent.py console` |

## 5. Frontend

Second terminal:

```bash
cd frontend
pnpm install
pnpm dev
```

Open http://localhost:3000.

## 6. One-command start

Windows:

```powershell
.\start_app.ps1
```

macOS / Linux:

```bash
chmod +x start_app.sh
./start_app.sh
```

`start_app.ps1` opens separate windows for worker and web. If `livekit-server` is missing, it uses your `LIVEKIT_URL` (Cloud). That is the usual path.

## 7. Voice setup

1. Worker is registered (`my-agent`).
2. Browser is on http://localhost:3000.
3. Click **Enter the hall**.
4. Allow the microphone. If the browser denied it, use the retry view.
5. Speak. You should hear Murf Falcon (`Anisha`).

Chat input is also on (`supportsChatInput: true`). Voice is the practice, not the only wire.

Hindi in the Windows terminal: the worker forces UTF-8 on stdout. If a log still shows `?`, that is the console, not a second TTS.

## 8. Verify the install

| Check | Expect |
| --- | --- |
| Worker log | registered, `agent_name: my-agent` |
| http://localhost:3000 | Hall, Enter the hall |
| `GET /api/health` | liveness |
| `GET /api/ready` | 200 if LiveKit env is present; 503 if missing |
| Speak a greeting | Spoken reply |
| `/analytics` | Dashboard (empty until a call completes) |
| `/enterprise` | Control Center |

Worker health from the backend tree:

```bash
uv run python -m salora_platform.health
uv run python -m salora_platform.health --ready
```

## 9. Tests

Backend:

```bash
cd backend
uv run python -m pytest -q --ignore=tests/test_agent.py
uv run ruff check .
```

Frontend:

```bash
cd frontend
pnpm exec tsc --noEmit
pnpm lint
pnpm test
```

Repo wrappers: `scripts/ci.sh` / `scripts/ci.ps1`.

`tests/test_agent.py` needs live LiveKit and an LLM judge. CI skips it.

## 10. Docker

```bash
docker compose up --build
```

- Web: `:3000`
- Worker: LiveKit job (no public HTTP)
- SQLite: volume `salora-data` → `/app/data`

Need `backend/.env.local` and `frontend/.env.local` on the host. Details: [deployment.md](deployment.md).

## 11. Debugging

| Symptom | First look |
| --- | --- |
| Worker never registers | LiveKit values, `download-files`, wait for `my-agent` |
| Page loads, no voice | Worker running? Same LiveKit project both sides? Mic allowed? `/api/ready` |
| 503 on `/api/ready` | Missing `LIVEKIT_*` in frontend env |
| Hindi garbled in terminal | Windows cp1252 — worker already sets UTF-8 |
| Empty analytics | No completed call yet. Not a hall mount bug |
| Docker lost memory | Volume removed. Recreate is expected to wipe if you deleted `salora-data` |
| `test_agent.py` fails locally | Ignore it unless you meant to run the live judge |

More: [troubleshooting.md](troubleshooting.md).

## 12. Common errors

**`Missing required command: uv` / `pnpm`** — install them; `start_app.ps1` exits if they are absent.

**Gemini / Murf / Deepgram auth errors in the worker** — key missing or wrong file. Keys belong in `backend/.env.local`, not the frontend file (except LiveKit).

**Two different LiveKit projects** — token mints for project A, worker registered on project B. Rooms never meet.

**`AUTH_REQUIRED=true` with no roster** — instruments and token path expect identity that this demo does not issue. Leave it false until [41](../engineering/41_SALORA_OS_V1_RELEASE.md) identity work exists.

Next: [configuration.md](configuration.md) · [development.md](development.md) · [troubleshooting.md](troubleshooting.md)
