# 27 — Marketplace Platform

Extension layer of SALORA OS. Not an app store. Not a payment system.

Law: [22](22_PRODUCTION_PLATFORM.md), [23](23_BACKEND_PLATFORM.md). Plugins consume services. They do not open `agent.py`.

---

## Plugin architecture

`PluginEngine` / `MarketplaceService` is the only extension runtime.

Manifest fields: id, name, version, author, publisher, license, permissions, capabilities, dependencies, entrypoint, icon, description, organization, timestamps.

Kinds: plugin, extension, package, module, command, tool, action, provider, integration, workflow, adapter.

Seed catalog points at **existing** modules (`math_practice_specialist`, analytics export). Install records an event. `SandboxService.may_execute()` is **false**.

---

## Capability model

Declared capabilities: voice, learning, adaptive, knowledge, studio, whiteboard, memory_graph, analytics, enterprise, developer, commands, providers, workflows, agents.

Mapped onto Phase 11 permissions. No plugin calls a service except through contracts.

---

## Sandbox

Architecture: permission / capability / API / storage isolation, deny-by-default network, resource quotas, no arbitrary code, lifecycle hooks (install/enable/disable/remove).

Signature verification is a `signed` flag on the manifest. Trust policy = RBAC + signed + org scope.

---

## Marketplace engine

Catalog, search, install, update, ratings (field later), metrics. No storefront UI. No billing.

Frontend: `MarketplaceProvider` — do not mount on the hall. ⌘K `marketplace:open` is planned.

---

## Events

PluginInstalled/Updated/Removed/Enabled/Disabled, MarketplaceOpened, PackagePublished/Downloaded, CapabilityGranted/Revoked.

Same bus as [23](23_BACKEND_PLATFORM.md).

---

## Future

SDK packages, enterprise private catalogs, agent marketplace — same manifests. A payment rail is a later adapter, not a core rewrite.
