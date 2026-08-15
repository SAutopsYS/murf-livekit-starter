# 28 — Enterprise Cloud Platform

Multi-tenant operating layer. No new AI. No admin dashboard redesign.

---

## Organization architecture

`OrganizationProvider` + `TenantService`.

One engine. Studio, Whiteboard, Fabric, Learning, Marketplace, SDK all take `organization_id` on records already shaped for it.

---

## Tenant model

Kinds: tenant, organization, workspace, department, school, classroom, team, project, group, division.

Fields: id, name, slug, owner, plan, settings, metadata, timestamps.

---

## Membership

Kinds: owner, administrator, manager, teacher, parent, student, developer, guest, observer.

**Maps onto existing `Role`.** No second RBAC. Invitations, join, suspend, remove emit bus events.

---

## Workspace isolation

personal / organization / classroom / team / enterprise / shared.

No shared global document store. In-memory stores are process-local until SQL ports grow an `organization_id` column — without joining to `User` by identity for analytics.

---

## Policy engine

ai, learning, voice, security, retention, marketplace, plugin, studio, whiteboard.

Stored as `PolicyRecord`. Not hardcoded in `agent.py`.

---

## Billing

`BillingSpec` flags only: subscription, usage, quotas, seats, licenses, storage, AI credits, feature access. No gateway.

---

## Security

Tenant isolation via org id. Settings are not logged. Audit = event bus. Data residency and legal hold are architecture notes for a later compliance adapter.

Reuse Phase 11 `enterprise.admin`.

---

## Future

Global deploy = same images + org-scoped secrets. Enterprise marketplace = org-filtered catalog. Compliance dashboards consume events, not a speech lake.
