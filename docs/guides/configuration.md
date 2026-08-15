# Configuration

Copy examples to `.env.local`. Placeholders only in git. Never paste live keys into docs.

## Backend (`backend/.env.local`)

| Variable | Required | Purpose |
| --- | --- | --- |
| `LIVEKIT_URL` | Yes | LiveKit Cloud WebSocket URL |
| `LIVEKIT_API_KEY` | Yes | LiveKit API key |
| `LIVEKIT_API_SECRET` | Yes | LiveKit API secret |
| `MURF_API_KEY` | Yes | Murf Falcon TTS |
| `DEEPGRAM_API_KEY` | Yes | Deepgram STT |
| `GOOGLE_API_KEY` | Yes | Gemini LLM |
| `EXERCISE_SOURCE` | No | `local` (default) or `api` |
| `EXERCISE_API_URL` | No | External exercise HTTP |
| `LIVEKIT_SIP_OUTBOUND_TRUNK_ID` | No | Outbound telephony |
| `TWILIO_*` | No | Optional SIP provider |
| `ESCALATION_WEBHOOK_URL` | No | Human-help webhook |
| `SALORA_PROFILE` | No | `development` / `staging` / `production` |
| `AUTH_REQUIRED` | No | Default `false`. Anonymous voice stays open |
| `SALORA_AUTH_SECRET` | No | JWT secret when auth is on |
| `FEATURE_*` | No | Instrument flags |

LiveKit Cloud helper:

```bash
lk cloud auth
lk app env -w -d backend/.env.local
```

## Frontend (`frontend/.env.local`)

| Variable | Required | Purpose |
| --- | --- | --- |
| `LIVEKIT_URL` | Yes | Same project as backend |
| `LIVEKIT_API_KEY` | Yes | Same as backend |
| `LIVEKIT_API_SECRET` | Yes | Same as backend |
| `AGENT_NAME` | No | Set `my-agent` for explicit dispatch |
| `AUTH_REQUIRED` | No | Default `false` |
| `SALORA_AUTH_SECRET` | No | Must match backend when auth is on |
| `RATE_LIMIT_TOKEN_PER_MIN` | No | Default 30 |
| `RATE_LIMIT_API_PER_MIN` | No | Default 120 |
| `FEATURE_ANALYTICS` | No | Default true |
| `FEATURE_ENTERPRISE` | No | Default true |
| `FEATURE_STUDIO` | No | Default false. Do not mount on the hall |
| `FEATURE_MARKETPLACE` | No | Default false |

## Privacy

- `.env` and `.env.local` are gitignored
- No transcripts in logs or dashboards
- Flip `AUTH_REQUIRED=true` only after a real roster exists

Related: [13 Security Standard](../engineering/13_SECURITY_STANDARD.md).
