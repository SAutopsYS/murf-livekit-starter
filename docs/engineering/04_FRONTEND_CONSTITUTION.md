# 04 — Frontend Constitution

Law for `frontend/`.  
Stack: Next.js App Router, React, TypeScript, Tailwind, LiveKit Agents UI, shadcn-based `components/ui`.

Do not replace the session provider, token route, or visualizer pipeline.

---

## Folder structure

```
frontend/
  app/                 # routes: /, /analytics, /enterprise, api/*
  components/
    app/               # product rooms (welcome, session, dashboards)
    agents-ui/         # LiveKit voice UI — treat as kernel
    enterprise/        # control center
    ui/                # reusable primitives
    system/            # layouts, page states, instrument cards, motion
    os/                # SALORA OS shell, nav, command, page frame
    voice/             # state machine, events, Living Core host
    learning/          # intelligence engine — do not mount on the hall
    adaptive/          # decision engine — consumes learning
    knowledge-fabric/  # semantic memory projection
    ai-elements/       # chat primitives
  hooks/
  lib/                 # brand.ts, utils, analytics, enterprise clients
  styles/              # tokens.css, globals.css
  public/              # salora-mark.svg, static
  app-config.ts        # brand + visualizer + agent name
```

New product UI goes in `components/app`, `components/ui`, or `components/system`.  
Do not fork `agents-ui` for cosmetics. Wrap or theme it.

Target monorepo (`apps/web`) is future. Law applies now. See [23 Implementation Foundation](../salora/23-implementation-foundation.md).

## Component architecture

- Server Components by default in `app/`.  
- Client only for LiveKit, theme, dashboards that poll.  
- One component, one job. Cards do not mix unrelated actions.  
- Reuse `components/ui/button` and existing views. Do not duplicate a second Button.

## Naming rules

See [14 Naming Convention](14_NAMING_CONVENTION.md).  
Files: `kebab-case.tsx`. Components: `PascalCase`. Hooks: `useThing`.

## Reusable components

Source of truth: `components/ui/*` primitives + `components/system/*` compositions.  
See [15 Design System Components](15_DESIGN_SYSTEM_COMPONENTS.md). Do not invent a parallel kit.

## Hooks

`hooks/` for shared behavior. LiveKit-specific hooks stay under `hooks/agents-ui/`.  
A hook does not fetch a transcript field that does not exist.

## Context

`ThemeProvider`, `AgentSessionProvider`, and `VoiceProvider` are the living contexts.  
`LearningProvider` is for instruments / future `/learning`. Do not mount it on the hall.  
Do not add a global utterance store. Do not remap `useAgent()` in leaf UI.

## State management

Server state from existing API routes (`/api/token`, `/api/analytics`, `/api/enterprise`).  
Session UI state stays local to the LiveKit tree.  
No Redux for the hall.

## Routing

| Route | Room |
|---|---|
| `/` | Hall — LiveKit session inside `OsShell` primary workspace |
| `/analytics` | Instrument |
| `/enterprise` | Instrument |

Nav registry: `frontend/lib/os-nav.ts`. Planned routes have no pages yet.  
New rooms are new routes. They do not swallow `/`.  
Deep link into a live session must confirm (when that lands).  
See [16 Workspace Architecture](16_WORKSPACE_ARCHITECTURE.md).

## Theme system

`next-themes` + class `dark`. Tokens in `styles/tokens.css` and `globals.css`.  
`getStyles(appConfig)` maps `accent` / `accentDark` to `--primary` and `--salora-pulse`.  
Toggle is always visible (`layout.tsx`).

## Accessibility

[02 UI/UX Bible](02_UI_UX_BIBLE.md). Keyboard path in the same PR as the control. `sr-only` for icon-only buttons (theme toggle already).

## Responsive rules

Mobile-first. `sm:` / `md:` for air and two-column suggestions.  
Stop and primary remain on one column.

## Performance rules

[12 Performance Standard](12_PERFORMANCE_STANDARD.md).  
Polling (analytics/enterprise) is single-flight and must pause when the document is hidden (keep this when touching those clients).

## Code splitting / lazy loading

Route-level split is enough for `/analytics` and `/enterprise`.  
Do not lazy-load the session kernel behind a flicker.

## Error boundaries

Route-level errors should be a door (what happened, what to do).  
Do not catch LiveKit disconnect and show a stack.

## Frontend review checklist

- [ ] Reused an existing component or said why not  
- [ ] Tokens, not raw sky hex (new work)  
- [ ] No hover-only meaning  
- [ ] Focus visible  
- [ ] Live session not restarted  
- [ ] No utterance in UI state  
- [ ] `pnpm exec tsc --noEmit` clean  
- [ ] Reduced-motion considered  
- [ ] Primary still obvious on a phone  

See [08 Coding Standards](08_CODING_STANDARDS.md).
