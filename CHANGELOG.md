# Changelog

Recorded from `git log` on `origin/main` (Days 1–9) and the local working tree. Dates follow commit subjects, not a marketing calendar.

## Unreleased (local working tree)

Architecture freeze, Workspace Shell, `salora_platform`, service facades, public `docs/` tree, Day 10 showcase drafts.

- Event bus redacts forbidden keys **and** long forbidden values
- Voice continues if memory/analytics DB init fails
- Compose volume `salora-data` → `/app/data`
- Public docs index; constitutions stay in `docs/salora/`
- Unit suites last validated locally: backend 434 (judge skipped), frontend 25

Not on `origin/main` until this tree is committed and pushed.

## Day 9 — Enterprise multi-agent learning

- `SpecialistRouter`; Math guest on the same room and mouth
- One retry, then host; handback does not re-greet
- `/enterprise` Control Center
- Commits: `18d7b0d`, `967c414`

## Day 8 — Call analytics

- `analytics.db` (anonymous ops)
- `/analytics` dashboard and export without speech columns
- Commit: `b366bf3`

## Day 7 — Human-help escalation

- Consent, allow-listed reasons, sanitizer, reference IDs
- Optional webhook; do not claim a notify that was not sent
- Commit: `c53446e`

## Day 6 — Outbound telephony

- Separate SIP path. Browser Voice Pipeline unchanged
- Commit: `69c4a1e`

## Day 5 — Learning tools

- Exercises, deterministic scoring, recommendations
- Provider failover, cache, cooldown
- Commit: `5f96b6c`

## Day 4 — Memory and knowledge

- Consented SQLite profile, Forget Me
- JSON knowledge tool
- Commit: `5e9d8e5`

## Day 3 — Hall experience

- Session states, wave, practice suggestions
- Commits: `62032ab`, `ed1d7ac`

## Day 2 — Learning Tutor

- Personality, greeting, Hinglish, guardrails
- Commits: `d348190`, `7730ea0`

## Day 1 — Voice agent

- LiveKit + Murf Falcon end-to-end
- Commits: `3d58afb`, `2fa7b49`

Starter pins and model/voice updates sit under `09adf01` and `fb0feec`.
