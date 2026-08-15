# 39 — Governance & Compliance Platform

Wraps Phase 11 privacy + Phase 17 policies. No new auth. No new RBAC.

Frameworks: GDPR, COPPA, FERPA, SOC2, ISO27001, AI — pass when utterance columns are absent and consent-before-memory holds.

HIPAA is **architecture only** (`ok: false` until a dedicated review).

`GovernanceService.apply` requires `enterprise.admin`. Audit pack never includes speech.
