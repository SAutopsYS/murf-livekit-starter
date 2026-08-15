# Frontend

SALORA OS web surface. Workspace Shell wraps the hall and instruments. The voice session stays on LiveKit.

Public guides: [../docs/guides/installation.md](../docs/guides/installation.md).

## Setup

```bash
cd frontend
pnpm install
cp .env.example .env.local
```

Required: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`. Optional: `AGENT_NAME=my-agent`.

```bash
pnpm dev
```

Open http://localhost:3000. The worker must be running. Frontend and backend do not call each other for audio. Both join LiveKit.

## Routes

| Path | Role |
| --- | --- |
| `/` | Hall. Voice only |
| `/analytics` | Call analytics instrument |
| `/enterprise` | Control Center |
| `/api/token` | LiveKit token |
| `/api/health` · `/api/ready` | Liveness / readiness |

Studio, Marketplace, Education, and mentors are libraries. They are not mounted on the hall.

## Brand

Tokens: `styles/tokens.css`. Name and pulse: `lib/brand.ts` and `app-config.ts` together.

Visualizer types in `app-config.ts`: `bar`, `grid`, `radial`, `wave`, `aura`.

## Test

```bash
pnpm exec tsc --noEmit
pnpm lint
pnpm test
```

## Layout

```text
frontend/
├── app/                 # Pages and API
├── components/os/       # Workspace Shell
├── components/app/      # Hall views
├── components/agents-ui/
├── lib/                 # Engines and platform
├── styles/
└── app-config.ts
```

## License

MIT. See [LICENSE](LICENSE).
