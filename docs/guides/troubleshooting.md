# Troubleshooting

## Worker never registers

- Confirm `backend/.env.local` LiveKit values match the Cloud project
- Wait for `registered worker` / `agent_name: my-agent`
- Run `uv run python src/agent.py download-files` once

## Frontend connects, no voice

- Backend must be running in `dev` or `start`
- `LIVEKIT_*` must match on both sides
- Allow microphone. Use the retry view if the browser denied it
- Check `GET /api/ready` — missing LiveKit env returns 503

## Hindi looks garbled in the terminal

Windows consoles default to cp1252. The worker reconfigures stdout to UTF-8. If a log still breaks, that is a console encoding issue, not a second TTS.

## Analytics or enterprise empty

Those instruments read `analytics.db` and consented memory. A new clone has no calls yet. They are not mounted on the hall.

## `AUTH_REQUIRED` surprises

Default is `false` so anonymous voice works. Instruments stay open. Set `true` only with a roster and matching `SALORA_AUTH_SECRET` on frontend and backend.

## Docker loses learner data

Compose mounts `salora-data` to `/app/data`. If you removed the volume, SQLite is gone. That is expected.

## Tests fail on `test_agent.py`

CI ignores that file. It needs live LiveKit and an LLM judge. Run the rest with `--ignore=tests/test_agent.py`.

## Still stuck

- [configuration.md](configuration.md)
- [Voice Pipeline](../architecture/voice-platform.md)
- [13 Security Standard](../engineering/13_SECURITY_STANDARD.md)
