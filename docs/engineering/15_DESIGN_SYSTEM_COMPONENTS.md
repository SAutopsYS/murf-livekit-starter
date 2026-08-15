# 15 — Design System Components

Phase 2 visual operating system.  
Tokens: [07 Design System Bible](07_DESIGN_SYSTEM_BIBLE.md).  
Motion: [03 Motion Bible](03_MOTION_BIBLE.md).  
UX states: [02 UI/UX Bible](02_UI_UX_BIBLE.md).

Do not invent a second kit. Improve `components/ui`. Compose in `components/system`.  
OS chrome lives in `components/os`. Do not fork `agents-ui`.

---

## Decision: two layers

| Layer | Path | Job |
|---|---|---|
| Primitive | `frontend/components/ui/*` | One control. Variants, a11y, tokens |
| Composition | `frontend/components/system/*` | Rooms, states, instrument cards, motion |

If a primitive already exists, add a variant. Do not create `Button2`.

---

## Tokens (expanded, not replaced)

Source: `frontend/styles/tokens.css`.

| Family | Examples |
|---|---|
| Brand | `--salora-pulse`, `--salora-pulse-on`, `--salora-canvas`, `--salora-ink` |
| Semantic | `--salora-success`, `--salora-warning`, `--salora-error`, `--salora-info` |
| Surface | `--salora-surface-raised`, `--salora-surface-sunken` |
| Border | `--salora-border-subtle`, `--salora-border-strong` |
| Space | `--salora-space` … `--salora-space-7` (8pt kernel) |
| Radius | control `0.75rem`, cluster `1rem`, panel `1.5rem`, pill |
| Elevation | `--salora-shadow-sm/md/lg` |
| Blur / opacity | `--salora-blur-panel`, `--salora-opacity-panel` |
| Motion | short 180, medium 320, consequence 400; enter/exit/progress curves |
| Type | meta, body, primary, title |
| Breakpoints | sm 40rem, md 48rem, lg 64rem, xl 80rem |
| Z-index | base, sticky, header, overlay, toast |

Theme: same names in `.dark`. Pulse lightens for contrast.  
`prefers-reduced-motion` zeros duration tokens.

New screens: `bg-primary`, `text-muted-foreground`, `border-border`, `rounded-[var(--salora-radius-*)]`.  
No sky. No hardcoded hex in product UI.

---

## Primitives (`components/ui`)

| Component | Variants / notes | A11y |
|---|---|---|
| `Button` | default, destructive, outline, secondary, ghost, link, **hall** | focus ring, disabled |
| `IconButton` | wraps `Button` `size=icon` | label required via children/sr-only |
| `Card` | default, glass, sunken · padding none/sm/md/lg | article |
| `Badge` | default, pulse, success, warning, error | text, not color alone |
| `Input` / `NativeSelect` / `Textarea` / `FieldLabel` | token radius + ring | label association |
| `Select` | existing Radix | existing |
| `Dialog` | overlay + content | title, description, focus trap |
| `Drawer` | left/right on Dialog | same as dialog |
| `Tooltip` | existing | existing |
| `Tabs` | list / trigger / content | tab / tabpanel / aria-selected |
| `Accordion` | Collapsible | trigger + content |
| `Progress` | determinate only | value |
| `Spinner` | honest hold | role=status, sr-only |
| `Skeleton` | layout-shaped pulse | pair with aria-busy |
| `Alert` | default, destructive, warning, success | role=alert |
| `Avatar` | initials | role=img + alt |
| `Toaster` | sonner, token colors | existing |

Usage:

```tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

<Button variant="hall">Enter the hall</Button>
<Card variant="glass">…</Card>
```

---

## Compositions (`components/system`)

Import from `@/components/system`.

| Component | Use |
|---|---|
| `PageHeader` | eyebrow, title, description, actions |
| `SectionHeader` | in-page title |
| `PageState` | loading, empty, offline, no-results, permission, error, maintenance |
| `MetricSkeletonGrid` | instrument loading |
| `MetricCard` / `StatCard` | one number |
| `GlassCard` / `Panel` / `Widget` | instrument surfaces |
| `InsightCard` / `TimelineCard` / `MissionCard` | named instrument cards |
| `FloatingPanel` / `VoicePanel` | overlays / voice chrome (wrap, do not replace LiveKit) |
| `CommandItem` | palette rows |
| `ResponsiveGrid` / `BentoGrid` / `BentoCell` | 8pt grids |
| `AppShell` | page canvas |
| `InstrumentLayout` | analytics/enterprise chrome + toaster |
| `AnalyticsLayout` / `EnterpriseLayout` | width presets |
| `LearningLayout` | hall-centered (future wrap) |
| `SettingsLayout` / `WorkspaceLayout` | reserved shells — **do not implement Workspace here** |
| `DockLayout` / `FloatingLayout` | chrome positions |

Page states:

```tsx
<PageState kind="error" title="Analytics are temporarily unavailable." />
<PageState kind="empty" title="No calls recorded yet." />
<PageState kind="no-results" />
```

---

## Layouts

| Layout | Width | Room |
|---|---|---|
| Learning | full hall | `/` session |
| Analytics | `max-w-6xl` | `/analytics` |
| Enterprise | `max-w-7xl` | `/enterprise` |
| Settings / Workspace | instrument | Phase 3+ |

Root `app/layout.tsx` remains the application shell (mark, theme). Do not duplicate it.

---

## Motion primitives

CSS: `.motion-fade`, `.motion-rise`, `.motion-scale`, `.motion-slide`.  
JS (`motion/react`): `Fade`, `Rise`, `Scale`, `Slide`, `Reveal`, `Expand`, `Collapse`, `PageTransition`, `CardTransition`, `DialogTransition`, `ListAnimation`.

All read `useReducedMotion()`. Tokens already zero when reduced.

Verb must be nameable. No bounce. No shake on error.

---

## Icons

**New product UI: Phosphor only.**  
Weight bold on controls. Size 16 default, 20 on hall commitments. Pair icon with a word on commitments.

Do not rip Lucide from `agents-ui`, `select` chevrons, or `sonner`. That is kernel/shadcn debt, not a second system to expand.

Constants: `frontend/components/system/icons.ts`.

---

## Theming

`class="dark"` on `html`. `ThemeToggle` always visible.  
Light: ivory canvas, sage pulse. Dark: forest canvas, lifted pulse.  
Contrast: text uses `--foreground` / `--muted-foreground`. Destructive stays red. Pulse is not success.

---

## Migration

| Before | After |
|---|---|
| Analytics local `MetricCard` + sky shell | `MetricCard` + `AnalyticsLayout` + `PageHeader` |
| Enterprise `GlassCard` / `Metric` / `SkeletonGrid` | system cards + `EnterpriseLayout` |
| Hardcoded sky/slate | tokens / semantic Tailwind |
| Ad-hoc loading/error copy | `PageState` |

Voice welcome, session, LiveKit, Murf: untouched.

---

## Accessibility checklist

- Focus visible on every control (`ring` / `btn-premium`)
- Dialogs named
- Page states use `status` or `alert`
- Loading grids `aria-busy`
- Color never the only signal
- Reduced motion honored
- Theme control not hover-only
