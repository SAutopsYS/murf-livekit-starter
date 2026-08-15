# 07 — Design System Bible

Tokens and visual law as implemented in Phase 1 and expanded in Phase 2.  
Brand: [../salora/BRAND.md](../salora/BRAND.md).  
Philosophy: [../salora/06-design-system.md](../salora/06-design-system.md).  
Components: [15 Design System Components](15_DESIGN_SYSTEM_COMPONENTS.md).

Phase 2 extended **the same token set**. Do not invent a second one.

---

## Colors

| Token | Light | Dark | Use |
|---|---|---|---|
| Pulse | `#2F6F5E` | `#6FBF9A` | Primary, ring, wave, host |
| On-pulse | `#F7F4EE` | `#121410` | Text on pulse |
| Canvas | ivory `oklch(0.978 0.008 95)` | `oklch(0.155 0.016 145)` | Page |
| Destructive | existing oklch red | existing | Errors only |

`--primary` is mapped from `app-config` accent so LiveKit UI and buttons follow pulse.  
Semantic success/warning stay distinct. Pulse is not success and not error.  
New work: `bg-primary`, `text-primary`, `border-primary`. Do not add a new sky scale.

## Typography

- Sans: Public Sans → `--font-public-sans`  
- Mono: Commit Mono → status, uppercase labels  
- Roles: title, primary, body, meta  
- Regular body. Semibold titles. Bold rare. Light weights not for teaching text  

## Spacing

Kernel **8**. `--salora-space: 8px`. 4 only for optical icon/type correction.  
Tailwind spacing that is a multiple of 2 (8px) is preferred.

## Grid

8pt. Learner: one column of meaning. Suggestions: 1 col mobile, 2 col `sm+`.

## Radius

`--radius: 0.875rem`. Pills for primary commitments (`btn-premium`).  
Panels: `1.5rem` (`.surface-panel`).

## Icons

New product UI: Phosphor only. Pair with a word on commitments.  
No commenting mascot. Wave is presence.  
Do not rip Lucide from `agents-ui` or existing shadcn chevrons.

## Elevation / glass / shadows

`.surface-panel`: light glass, blur 24px, soft shadow. Dark: 5% white fill.  
Do not stack three blurs behind the wave.  
Glass is a panel material, not a personality.

## Motion tokens

```
--salora-duration-short: 180ms
--salora-duration-medium: 320ms
--salora-ease-enter: cubic-bezier(0.22, 1, 0.36, 1)
```

See [03 Motion Bible](03_MOTION_BIBLE.md).

## Dark mode / light mode

`class="dark"` on `html`. Same token names. Pulse lightens in dark for contrast.  
High contrast (future): same names, stronger border.

## Component variants

`components/ui/button` + `.btn-premium` for hall commitments.  
Do not create `Button2`. Variants are size/intent on the existing button.

## Design tokens (files)

| File | Role |
|---|---|
| `frontend/styles/tokens.css` | Brand, semantic, surface, space, radius, elevation, motion, type, z |
| `frontend/styles/globals.css` | Theme + utilities |
| `frontend/lib/brand.ts` | JS hex + copy |
| `frontend/app-config.ts` | Runtime accent + logos |

A raw magic number in a new screen is drift. [14 Naming](14_NAMING_CONVENTION.md) for token names.
