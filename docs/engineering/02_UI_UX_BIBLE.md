# 02 — UI/UX Bible

How SALORA surfaces must behave.  
Law: [../salora/03-experience-blueprint.md](../salora/03-experience-blueprint.md), [../salora/06-design-system.md](../salora/06-design-system.md).  
Tokens: [07 Design System Bible](07_DESIGN_SYSTEM_BIBLE.md).  
Motion: [03 Motion Bible](03_MOTION_BIBLE.md).

---

## Design philosophy

The interface is a room for a try. Premium minimalism. One pulse. Quiet canvas. Beauty is hierarchy, type, and true state — not ornament.

## User experience principles

- One primary per surface.
- Back is not restart.
- Stop is reachable (thumb on a phone).
- Hover is never the only path.
- Search and deep links confirm before replacing a live session.
- Theme control is visible (not hover-only).

## Interface principles

Learner surfaces: low density. Teacher/enterprise: higher density, still one primary.  
Brand pulse does not paint the whole screen.  
Voice presence (wave) is state, not a mascot.

## Information hierarchy

1. Where I am  
2. What to do now  
3. How to stop / go back  
4. Instruments (analytics, console)

Header: mark + name. Footer instruments do not steal the attempt.

## Layout philosophy

8pt grid. Content measure the eye can hold. Safe areas respected.  
Welcome, session, and ended are full-hall rooms. Analytics and enterprise are instrument rooms — they must not become the home of the learner.

## Interaction rules

A button’s label is the future act. After click, the world matches the label.  
Destructive acts use a dialog of consequence (forget, end, takeover).  
Toasts do not ask for decisions.

## Empty states

Name the surface. Why empty. First step as a real button. No fake charts. No shame.

## Error states

What happened. What to do. Last good state remains. No stack in the lesson. Voice errors short enough to say aloud.

## Loading states

Skeleton matching the layout that will arrive, or a short honest hold (connecting copy). No personality skit. No fake percent.

## Mobile experience

Attempt, stop, voice, back. Practice suggestions stack. Thumb reaches the primary. Theme toggle remains tappable.

## Desktop experience

Same rooms. More air. Instruments may sit as links, not as a second OS. Keyboard: every commitment reachable. See [04 Frontend Constitution](04_FRONTEND_CONSTITUTION.md).

## Accessibility rules

Labels on controls. Visible focus. Contrast on pulse and type. Meaning not color-only. Reduced motion: instant state, meaning remains. Dynamic type: two steps without hiding Stop. Captions when speech is essential and twins exist.

## Visual consistency

Tokens only (`styles/tokens.css`, `globals.css`). No raw sky hex on new work. Existing instrument pages may still carry challenge sky until Phase 2 migrates them — do not invent a third palette meanwhile.

## Storytelling through UI

The story is continuity: enter the hall → connect → practice → end → return.  
Do not tell a story of how smart the model is. Do not festival a success. Do not shame a miss.
