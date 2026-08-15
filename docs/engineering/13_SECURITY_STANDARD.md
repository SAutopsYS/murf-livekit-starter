# 13 — Security Standard

Protect learners before data.  
Law: [../salora/16-security-privacy.md](../salora/16-security-privacy.md), Master laws V–VII, X.

---

## Authentication

LiveKit tokens via `frontend/app/api/token/route.ts`.  
Platform session / JWT / refresh: [22 Production Platform](22_PRODUCTION_PLATFORM.md).  
Anonymous voice stays a first-class path. `AUTH_REQUIRED` defaults false.  
Auth session ≠ lesson visit.  
Future user accounts do not reset the host.  
No shared child logins as a workaround.

## Authorization

Server-side. UI is not the control.  
`can(role, permission)` in `frontend/lib/platform/rbac.ts` and `backend/src/salora_platform/auth.py`.  
Roles: `anonymous`, `guest`, `student`, `parent`, `teacher`, `enterprise_admin`, `developer`, `operator`.  
Enterprise UI `admin|teacher|parent` maps through `roleFromEnterpriseUi`.  
Guests cannot exceed host. Host cannot exceed consent.

## Secrets

Never in git. Never in traces. Never in README.  
`backend/.env.local`, `frontend/.env.local`.  
`.env.example` placeholders only.  
Rotate keys if they appear in a log or a screenshot.

## API keys

`LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `MURF_API_KEY`, `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`.  
Frontend must not embed API secrets. Token route stays server-side.

## Input validation

Tools go through `tools/validator.py` and the manager.  
Telephony and escalation sanitize PII (`escalation/sanitizer.py`).  
Never trust client-supplied “transcript” fields — they must not exist.

## Rate limiting

Edge (future) and provider health/cooldown (existing tools).  
A poller must not starve the attempt.  
No retry storm to Discord or SIP.

## Privacy

No transcript column. No utterance on analytics or enterprise exports.  
Consent-first memory. Forget Me completes.  
Hindi/English practice content is not a reason to keep a mouth.  
Research is not this repo’s default.

## Logging

Event names, route/agent ids, error class, latency.  
Forbidden: speech, OTP, phone, secrets, raw prompts.

## Encryption

TLS in transit (LiveKit Cloud, HTTPS).  
SQLite files are local process data — do not copy them into tickets.  
Device caches (future mobile): encrypted.  
Backups must not invent a speech lake.

## Compliance

DPA before a real school roster.  
Child extra review on features that touch minors.  
A demo does not waive residency or forget.  
If a feature needs a bedroom camera, it is refused.

## Security checklist (every PR)

- [ ] No new secret in the tree  
- [ ] No utterance-shaped field  
- [ ] Logs privacy-safe  
- [ ] Authz not only in the UI  
- [ ] Forget still possible if memory touched  
- [ ] `.env.example` updated with placeholders if a new key is required  
- [ ] Threat note if children, voice, export, or identity moved  

Sev-1: speech leak, secrets in the wild, systemic restart-the-person.  
See [09 Git Workflow](09_GIT_WORKFLOW.md) hotfix rules.
