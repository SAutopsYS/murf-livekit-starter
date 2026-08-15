# 16 — Workspace Architecture

Phase 3: SALORA OS shell.  
The hall is one application inside the OS.  
LiveKit session is not replaced. Murf is not touched.

Design system: [15 Design System Components](15_DESIGN_SYSTEM_COMPONENTS.md).  
Frontend law: [04 Frontend Constitution](04_FRONTEND_CONSTITUTION.md).

---

## Decision

One shell. One nav registry. One command catalog.  
Pages do not draw their own product chrome.  
Future modules plug into regions. They do not fork the frame.

---

## Shell architecture

`OsShell` in `frontend/components/os/` wraps every route from `app/layout.tsx`.

```
OsShell
  OsTopBar          mark, primary nav, context, search, notices, profile, theme
  OsWorkspace
    OsPrimaryWorkspace   route children (voice / analytics / enterprise)
    OsSecondaryPanel     reserved
    OsContextPanel       reserved
  OsBottomNav       instrument + mobile only
  OsCommandPalette  ⌘K
```

### Rooms

| Room | Path | Chrome |
|---|---|---|
| `hall` | `/` | Top bar overlays the session. No bottom nav. Voice controls stay free. |
| `instrument` | everything else | Top bar in flow. Bottom nav on small screens. |

Do not add a third room without naming why the first two fail.

### Shell tokens

`--salora-shell-top` 56px · `--salora-shell-dock` 64px · `--salora-touch` 44px.

---

## Navigation architecture

Source: `frontend/lib/os-nav.ts`.

| id | href | Status | Chrome |
|---|---|---|---|
| home | `/` | live | primary |
| workspace | `/` | live | command alias — same hall |
| learning | `/learning` | planned | command only |
| analytics | `/analytics` | live | primary |
| enterprise | `/enterprise` | live | primary |
| settings | `/settings` | planned | command only |
| studio | `/studio` | planned | command only |
| marketplace | `/marketplace` | planned | command only |
| developers | `/developers` | planned | command only |

Planned items do not get pages. Command says “Soon”.  
Do not implement Studio, Marketplace, or Learning here.

Primary nav is the only product nav. Pages must not ship a second Home/Analytics/Enterprise row.

---

## Workspace regions

| Region | Component | Now |
|---|---|---|
| Primary | `OsPrimaryWorkspace` | LiveKit App, or instrument page |
| Secondary | `OsSecondaryPanel` | Hidden until a module needs a rail |
| Context | `OsContextPanel` | Hidden until a module needs inspector |
| Widget | `OsWidgetRegion` | Slot for bento cells |
| Dock | `OsDockArea` | Reuses `DockLayout` |
| Floating | `OsFloatingArea` | Reuses `FloatingLayout` |
| Bottom sheet | `OsBottomSheet` | Mobile overflow |

Voice session renders in Primary. `AgentSessionView` stays `fixed inset-0`. Hall chrome overlays. Do not change the visualizer.

---

## Page framework

Every instrument page:

```
OsPage
  OsPageHeader      (PageHeader)
  OsPageToolbar
  OsPageContent
    states / widgets
  OsPageFooter
```

Actions live in `OsPageActions`. Navigation does not.

---

## Command system

`frontend/lib/os-commands.ts` + `OsCommandPalette`.

Kinds: navigation, action, search, ai, agent, settings, shortcut.  
AI / agent / settings entries are stubs (`planned: true`).

Enterprise **registers** section jumps and search hits. It does not own a second palette.

⌘K / Ctrl+K is global (`OsProvider`).

---

## Layout rules

- One `OsShell`. No page-level product header.
- `InstrumentLayout` is a **measure** (max-width + padding). Not a second shell.
- Hall children may be full viewport. Instruments use `OsPage` + 8pt gap.
- Bento: 1 / 2 / 6 / 8 / 12 columns from mobile → ultrawide.

---

## Responsive rules

- Mobile first. Touch target `--salora-touch`.
- Hall: no dock. Session controls keep the thumb zone.
- Instruments: bottom nav (Home, Analytics, Enterprise, More).
- Desktop: primary links in the top bar. Search labeled.
- Theme lives in the top bar. Not a floating pill over the wave.

---

## Widget rules

Widgets are `Card` / `MetricCard` / `InsightCard` inside `BentoGrid`.  
They rearrange by column count. They do not invent a second grid system.

---

## Future expansion

1. Add a row to `OS_NAV` (`live` only when the route exists).
2. Put the page in Primary. Use `OsPage`.
3. Register commands from the page. Do not fork ⌘K.
4. Open Secondary / Context only when the module has a real inspector.
5. Phase 4 may animate the **existing** wave. It must not replace the shell.

Auth, profile, and notifications are placeholders. Do not fake a user graph.
