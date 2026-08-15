# 29 — AI SDK Platform

Stable contracts over existing services. Developers integrate. They do not fork the kernel.

---

## SDK architecture

`SDKService` / `SdkProvider`.

Modules: Voice, Learning, Adaptive, Knowledge, Studio, Whiteboard, Memory Graph, Analytics, Enterprise, Marketplace, Agents.

Each module returns `ApiEnvelope[T]` from [23](23_BACKEND_PLATFORM.md). Never a SQLite row.

---

## API Gateway

`GatewayService` documents version (`v1`), JWT + API key, existing rate limits, `/api/health`.

Does **not** replace `/api/token`, `/api/analytics`, `/api/enterprise`.

---

## Integration framework

Adapters only: Google Workspace, Microsoft 365, Slack, Discord, Notion, Obsidian, GitHub, GitLab, Jira, Canvas LMS, Moodle, Salesforce, SAP.

No implementations.

---

## Webhooks

Reuse platform events: LearningUpdated, KnowledgeUpdated, ProjectCreated, CanvasCreated, PluginInstalled, OrganizationCreated, RecommendationCreated, AgentTransferred, SessionEnded.

Delivery is architected (`WebhookDelivered`). Batching is a flag.

---

## Developer portal

Spec only: API keys, OAuth clients, service accounts, downloads, webhooks, usage, docs, samples. `portalUi: false`.

---

## Security

`developer.sdk` to issue tokens. Guest cannot. JWT from Phase 11. Secret rotation architected. Tenant id on the token record.

---

## Versioning

`API_VERSION = v1`. Additive fields only. A breaking change is a `v2` envelope, not a rewrite of services.

---

## Future

Mobile / desktop SDKs consume the same modules. Public APIs stay envelopes. OAuth 2.1 is a provider on `PlatformSession`, not a second auth stack.
