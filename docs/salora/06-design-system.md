# SALORA OS — Design System Constitution

Phase 3.

The Constitution defines values.  
The Operating Standards define execution.  
The Product Blueprint defines what exists.  
The Experience Blueprint defines how it should feel.  
The Language System defines every sentence.

This file defines how every interface is designed.

Not a Figma library.  
Not a component list.  
Not implementation.

A timeless design language. Valid when the glass, the engine, and the fashion change.

Design, frontend, motion, illustration, design-systems engineering, accessibility, and AI interface design follow this file.

If a visual decision cannot name a principle here, it is decoration. Decoration does not ship on the attempt.

---

# Volume I — Design Philosophy

The interface is a room for a try. It is not a poster of the company.

**Human-centered design**  
The body in the room is tired, young, old, on a bus, in a shared house, or in a classroom. We design for that body first. Our taste is second. A control the hand cannot find is not designed.

**Learning-first interfaces**  
During the try, the subject is the interface. Chrome recedes. Instruments wait. If a layout makes the lesson look like a dashboard, the layout is wrong.

**Calm technology**  
The OS asks for attention only when the next act needs it. One primary. No competing motion. No extra sound. Quiet is a designed material, not leftover space we failed to fill.

**Invisible complexity**  
Host, guest, routing, sync, and memory are allowed to be deep. The person meets one next act and a way back. If they must understand our architecture to tap, we have failed the surface.

**Focus over decoration**  
Beauty is hierarchy, type, space, and true state. Ornament that does not teach, route, or reassure is removed. A trend texture is not a reason.

**Trust through consistency**  
The same act looks and behaves the same tomorrow. Return does not restyle the host. Inconsistency is felt as a stranger. That is a continuity defect.

**Predictability**  
Where the primary sits, what Back does, what a destructive fill means — these do not wander by screen. Surprise after a click is forbidden. Surprise in layout is almost as bad.

**Emotional restraint**  
We do not perform delight on a miss. We do not festival a success. Color, motion, and illustration stay inside the climate of the Experience Blueprint. Restraint is how dignity is drawn.

**Accessibility-first**  
A labeled path, a keyboard path, a voice path, and a no-motion path exist in the same decision, not as a later coat. If only one path exists, the work is unfinished.

**Timeless aesthetics**  
We do not date the hall with a year of gradients, glass, or brutalism. Surfaces are quiet. Type is readable. Brand pulse is one note. Fashion is a guest. It does not renovate the kernel.

---

# Volume II — Visual Language

**Visual hierarchy**  
Every surface has one dominant. Then supporting. Then ambient. If two objects share dominance, neither is primary. Size, weight, position, and contrast create hierarchy. Color is a helper, never the only cue.

**Scale**  
Related objects share a scale family. A new size is a last resort. Scale jumps exist to mark a change of job (title vs body vs caption), not to decorate.

**Balance**  
Weight sits where the act sits. A heavy brand mark and a weak primary is inverted balance. Instruments do not outweigh the attempt on a learner surface.

**Rhythm**  
Repeat, then pause. Equal gaps between siblings. A pause (more space) before a new job. Rhythm is how the eye knows a list from a break.

**Contrast**  
Text on surface meets a contrast duty, not a mood. State (success, warning, error) meets a contrast duty in both themes. Low contrast as “elegance” is a fail.

**Alignment**  
One edge starts the reading. Ragged alignment is a decision, not a slide. Numbers that compare align by meaning (decimal, start of glyph), not by decoration.

**Density**  
Learner attempt: low density. Teacher and enterprise instruments: higher density, still one primary per view. Density is a property of the workspace, not a personal taste.

**White space**  
Absence is a decision. It groups, rests, and points. Filling space because a canvas looks empty is fear. Fear is not a layout rule.

**Reading flow**  
Locale start-edge to end-edge, top to bottom. Voice-first surfaces still have a visual reading order that matches the spoken order: where I am, what to do, how to stop.

**Information architecture (drawn)**  
Product Architecture Volume III is the map. This language only draws it: orientation, primary, secondary, back. We do not invent a second map in the pixels.

**Brand expression**  
One pulse color. One quiet mark. Presence of the host (orb, wave) is state, not a mascot commentary. Brand does not outrank the attempt. A splash that delays the first try is not expression. It is friction.

---

# Volume III — Layout System

## Grid

The spatial kernel is **8**. All spacing, padding, and sizing snap to 8, with 4 allowed only for optical correction of type and icons.

The grid is a habit of the hand, not a cage that forbids a needed exception. Exceptions are written.

## Columns

Learner attempt: one column of meaning. A second column is an instrument and must yield on small surfaces.

Teacher, parent, school, enterprise: start from a content column plus an optional list column. A third column is rare and never appears on the attempt.

Columns are for jobs, not for filling width.

## Rows

A row is one object or one toolbar of siblings. Mixed jobs in one row split.

## Containers

A container holds one cluster of meaning (see Card philosophy). Max measure for reading text is a line the eye can hold — not a full desktop bleed of prose.

The attempt container is centered in attention, not necessarily in pixels. Safe, reachable, obvious.

## Responsive layouts

We reflow. We do not hide the primary. We do not invent a new product at a new width.

Small: attempt + stop + back.  
Medium: attempt + one instrument.  
Large: attempt or job + instruments that still do not steal the primary.

## Safe areas

Home indicator, notch, status bar, keyboard, and gesture edges are not decorative margins. Commitments never sit in an unsafe thumb or chin zone.

Stop is reachable by the dominant thumb on a phone.

## Margins

Outer margin is a rest, not a brand stripe. It grows with the canvas so content does not glue to glass. It does not grow so much that the primary floats away from the hand.

## Padding

Padding is the breath inside a cluster. Equal padding means equal kinship. More padding before a new job. Tight padding in dense instruments, never in a destructive dialog.

## Breakpoints

Breakpoints are changes of job layout, not of identity. We name them by what the layout becomes (one-column attempt, list-and-detail, instrument-dense), not by a vendor’s device catalog.

A fold, a split view, or a desktop window uses the same names.

## Adaptive interfaces

Adapt to width, input (touch vs keyboard vs voice), and reduced motion / larger type. Adapt does not mean a different host, a different brand, or a different memory.

## Future devices

New aspect ratios inherit the grid, the one-primary rule, and safe reach. They do not inherit a requirement that the person learn a new spatial language to do yesterday’s attempt.

---

# Volume IV — Typography System

**Font philosophy**  
Type exists to be read and spoken. We choose families that stay clear at small sizes, in Devanagari and Latin and the next script we ship, on a cheap phone, in a bright yard.

Display novelty is not a teaching face. A second family is allowed for the brand mark only. A third family is a defect.

**Reading hierarchy**  
Title (where I am) → Primary (what to do) → Body (the subject) → Meta (state, time, quiet help).  
Skip a level only when the surface is a single act.

**Scale**  
A small, named scale. Each step has a job. We do not invent a size per screen. Dynamic Type multiplies the scale; it does not invent new roles.

**Weights**  
Regular for body. Medium or semibold for primary and titles. Bold is rare and never a whole paragraph. Light weights are not used for teaching text.

**Line height**  
Body needs air enough for the next line to be a new line, not a collision — especially in Devanagari and other combining scripts. Tight leading is allowed in dense instruments, not in the lesson.

**Paragraph spacing**  
Space between paragraphs is a pause in thought. Lists use rhythm, not extra ornament.

**Language support**  
Every shipped script is a first-class face, not a fallback accident. Line breaks follow the locale. We never force a script into a Latin measure that clips matras or stacked forms.

**Accessibility**  
Type can grow two steps without breaking hierarchy or covering Stop. Truncation is a last resort and never hides a commitment or a warning.

**Voice reading**  
Visible text that the host will say must be speakable (Language System). Layout must not require a paragraph the mouth cannot hold. Captions, if present, follow the same hierarchy.

**Dynamic Type**  
A first-class mode. Layout reflows. We do not freeze a design at the default size and call larger type “best effort.”

---

# Volume V — Color System

Color is meaning, then brand, then never fashion.

**Brand colors**  
One pulse. Used for the living primary and host presence. It does not paint entire surfaces. It does not become the only way to find the act.

**Semantic colors**  
State is a small closed set. Each state has a word and a second cue (icon, position, or pattern).

**Success**  
A completed fact. Quiet. Not a fireworks palette.

**Warning**  
A consequence ahead (overwrite, takeover, leave a live attempt). Must be readable before the tap.

**Error**  
What failed. High contrast. Paired with a next act. Never used as brand spice.

**Neutral**  
Type, borders, quiet icons. The mass of the product is neutral. If neutrals are fashionable gray-on-gray, contrast has already failed.

**Surface colors**  
A short stack: canvas, raised, overlay, sunken. Elevation is a token, not a new paint per team. Surfaces do not compete with the pulse.

**Dark mode**  
The same hierarchy, the same semantics, inverted canvas. Dark is not a dim wash that hides type. Pulse may lighten to keep contrast. We do not invent a second brand in the dark.

**High contrast**  
A first-class theme. Borders may thicken. Pulse may become a line as well as a fill. Meaning must survive.

**Accessibility**  
No meaning by color alone. Contrast is a ship gate. Color blindness is a default reviewer, not an edge case.

**Future displays**  
Wide gamut and HDR may enrich the pulse. They may not become required to see a warning. E-ink and limited palettes must still show hierarchy and state.

---

# Volume VI — Component Philosophy

Purpose. Behavior. Interaction. Not specs.

Operating Standards named why some objects exist. This volume is the interface law for each kind.

**Button**  
Purpose: commitment.  
Behavior: the world after click matches the label. Destructive fill is rare and confirmed.  
Interaction: press has a pressed state. Disabled explains itself or is not shown. Hover is never the only affordance.

**Text link**  
Purpose: go, without committing a consequence.  
Behavior: if consequence is real, it is a button.  
Interaction: underline or equivalent in high contrast. Not a fake button.

**Card**  
Purpose: one cluster of meaning.  
Behavior: one job; split if actions diverge.  
Interaction: the card’s primary is obvious; the whole card is not a nest of unlabeled taps.

**List**  
Purpose: same-kind objects the eye can scan.  
Behavior: one object per row.  
Interaction: row tap has one default. Extra actions are named, not hidden in a hover-only overflow.

**Navigation**  
Purpose: where I am, where I can go, how I go back.  
Behavior: few primaries. Nineteen siblings are an architecture fail drawn as chrome.  
Interaction: current place is named in words, not only a color pip.

**Input**  
Purpose: they put a fact.  
Behavior: label always visible. Error next to the field.  
Interaction: keyboard type matches the fact. Autofill does not steal a lesson answer.

**Search**  
Purpose: remember less.  
Behavior: results grouped by taxonomy. Confirm before leaving a live session.  
Interaction: query is editable. Empty says what to try.

**Command palette**  
Purpose: the same objects as search, for the keyboard.  
Behavior: same confirm rule.  
Interaction: not a second product.

**Modal / Dialog**  
Purpose: interrupt for a consequence (forget, end, pay, grant, takeover).  
Behavior: first sentence is the consequence. Safe cancel.  
Interaction: focus trapped. Escape is cancel. Never for marketing or a tour.

**Drawer / Sheet**  
Purpose: secondary instruments or a short list of next acts.  
Behavior: does not hide Stop on a learner attempt without a way to dismiss.  
Interaction: drag to dismiss is extra, not the only path.

**Table**  
Purpose: compare like objects.  
Behavior: on small surfaces, the same objects become cards. Not a new invention.  
Interaction: sort and filter are named. A cell is not a secret control.

**Chart**  
Purpose: a question with an answer.  
Behavior: empty is drawn. No fake series.  
Interaction: a value has a text equivalent. Color is not the only series cue.

**Timeline**  
Purpose: order of what happened.  
Behavior: events, not decoration. No utterance quotes.  
Interaction: a point opens a fact, not a tape.

**Badge**  
Purpose: state, with a word.  
Behavior: color helps. The word remains.  
Interaction: not tappable unless it is a filter, and then it is labeled as one.

**Avatar / orb / wave**  
Purpose: presence and voice state.  
Behavior: idle, listening, speaking, waiting, failed. Not a commenting mascot.  
Interaction: not required to start a lesson. Not a face capture.

**Progress**  
Purpose: how far in this set or this wait.  
Behavior: honest. No fake jump. Determinate when we know; indeterminate when we do not.  
Interaction: not a game bar that shames.

**Skeleton**  
Purpose: the shape of the truth that is coming.  
Behavior: matches the layout that will arrive.  
Interaction: not a spinner that hides a shift of the primary.

**Empty state**  
Purpose: teach the surface.  
Behavior: name, why empty, first step. No shame, no fake chart.  
Interaction: the first step is a real button.

**Error state**  
Purpose: a door.  
Behavior: what happened, what to do, last good state remains.  
Interaction: the act is reachable. Voice error is short enough to say.

**Toast**  
Purpose: confirmation that needs no decision.  
Behavior: if they must act, it is not a toast.  
Interaction: does not cover Stop. Does not speak over the tutor.

**Banner**  
Purpose: a standing condition (offline, failed guest).  
Behavior: dismissible unless safety.  
Interaction: one act, labeled.

**Tooltip**  
Purpose: last-resort help for a control that already deserved to exist.  
Behavior: if the control needs a tooltip to be understood, the control is wrong.  
Interaction: keyboard equivalent. Not hover-only meaning.

**Tabs**  
Purpose: siblings of one job.  
Behavior: if they are different products, they are navigation.  
Interaction: selected tab is a word, not only an underline color.

---

# Volume VII — Interaction System

**Touch**  
Targets that a thumb can hit. Stop in the safe reach. No essential hover. Pressed state exists.

**Mouse**  
Precision for instruments. Pointer is not required to learn. Cursor does not invent a second primary.

**Keyboard**  
Every commitment and every primary is reachable. Order follows meaning (where I am → act → back → instruments). Focus is visible. Shortcuts are documented in the palette, not secret.

**Voice**  
A first-class input. Stop, help, repeat, slower, go back, I need a human. Voice does not require a visual tour. Visual still exists for those who need it.

**Stylus**  
Optional for writing and diagrams. The same commitments remain without it unless the skill is handwriting.

**Gesture**  
Back, dismiss, pause only when the same acts exist as labeled controls. Gesture is never the only path. Accidental gesture must not end a lesson without confirm when the consequence is real.

**Spatial input**  
Pointing may select. It does not become required. Gaze is not a click unless the person chose it and can still Stop another way.

**Eye tracking**  
Optional, explicit, off by default. Never the price of a lesson. Never an analytics stare.

**Haptics**  
Rare. Confirm a commitment or a fail. Never a celebration pattern. Never a score. Respect system silence.

**Feedback**  
Pressed, focused, busy, done, failed — each has a visual state. Sound is the tutor, not a click pack. See Experience Blueprint for the words.

**Drag / drop**  
For arrangement of objects the person owns (order of a list they made). Not for the attempt itself. Drop targets are labeled. Cancel is obvious.

**Selection**  
Selected is a word or a checkbox plus a highlight, not color alone. Multi-select names the count and the next act.

**Multi-device continuity**  
A second device asks to take over. The UI of takeover is a dialog of consequence, not a silent steal. One live session. The attempt does not fork.

---

# Volume VIII — Motion System

Motion is a verb. If you cannot name the verb, delete the motion.

Allowed verbs: **arrive, leave, confirm, fail-closed, progress, takeover**.

**Arrival**  
The primary appears. Short. No bounce that mocks a child. No brand film.

**Exit**  
The thing that ended gets out of the way. The last good state remains.

**Transition**  
Place to place: the person should still know where they are. Crossfades that erase hierarchy are forbidden. Hierarchical move (push/pop) matches Back.

**Loading**  
Skeleton or a short spoken hold. Not a personality loop. Not a fake percentage.

**Progress**  
Determinate motion only when the proportion is true.

**Confirmation**  
A still change of state is enough. A short settle is allowed. Confetti is not a verb we use.

**Error**  
A still, high-contrast door. Shake is forbidden (shame, vestibular harm, no extra information).

**Spatial motion**  
In spatial canvases, objects move because the person moved or because a guest entered. They do not orbit to look alive.

**Reduced motion**  
A first-class path. Instant state change. Meaning remains. This is not a lesser product.

**Accessibility**  
No motion required to know state. No flashing. No parallax that costs a try.

**Timing / duration**  
As short as recognition allows. Longer only for a consequence the person must notice (takeover, forget). Teaching surfaces prefer shorter than instrument surfaces.

**Easing**  
Decelerate into rest. Do not overshoot on errors or on children. Linear is for determinate progress, not for arrival.

**Motion hierarchy**  
The primary may move. The brand mark may not compete. One motion at a time on the attempt. Background animation behind a try is a defect.

---

# Volume IX — Iconography & Illustration

**Icons**  
A closed, quiet set. One stroke language. Recognized before they are admired. Paired with a word on first use and on any commitment.

**Symbols**  
State symbols (error, offline, guest) are distinct in shape, not only in color.

**Illustrations**  
Rare. Allowed on a first empty to explain a room. Never a character that shames. Never a story that delays the act.

**Educational graphics**  
A diagram is a teaching object: one idea, labeled, high contrast, localizable. It is not a hero image.

**Diagrams**  
Align with the learning graph when they show prerequisites. They do not become a poster of the company.

**Empty states**  
Type does the teaching. An illustration, if present, does not replace the first button.

**Character usage**  
No persistent character that comments, teases, or “lives” on the home. The host is a voice and a state, not a cartoon roommate.

**AI presence**  
Orb or wave shows voice state. A guest is a named change of state, not a new creature. We do not draw a brain, a sparkle swarm, or a thinking theater.

**Accessibility**  
Icons have names. Illustrations are not the only instruction. Contrast on diagrams is a ship gate.

**Localization**  
No metaphor that fails in another script or culture (hand signs, animals, idioms). Left-right arrows follow locale direction. Text in images is forbidden; type sits outside the image.

---

# Volume X — Accessibility Design

Beyond a checklist. How the interface is built so more bodies can try.

**Visual**  
Hierarchy without color. Type that grows. Dark and high contrast as themes. Motion that can stop. Focus visible. Not a dim puzzle.

**Cognitive**  
One primary. Plain labels. Predictable Back. No traps. No timed surprise. Working memory: one clause on screen when the mouth is also holding a clause.

**Motor**  
Reachable commitments. Humane time. Gesture optional. Pointer optional. Voice optional. At least two ways to Stop.

**Hearing**  
Captions when speech is essential. Visual state when the wave is speaking. The OS is not sound-only and not sight-only.

**Reading levels**  
Short. Taxonomy nouns. Language System applies to every label.

**Dyslexia**  
Clear letterforms. Generous tracking only if it does not break scripts we ship. Avoid long fully-justified rivers. Do not force a “dyslexia font” as the only path; allow user type settings.

**Color blindness**  
Review every state pair. Pattern or word with color.

**Elderly users**  
Larger default reachable. No hover-only. No youth theater. Same dignity. Contrast first.

**Children**  
Targets they can hit. Consequences in the first sentence. No shame illustration. No dark pattern that looks like a game continue.

**Low-end devices**  
The attempt works without blur, video backgrounds, or heavy spatial scenes. Beauty that costs the try on a cheap phone is not beauty.

**Offline**  
A drawn, honest banner. Cached last lesson readable. No skeleton that never resolves.

**Low bandwidth**  
Shorter voice, still hierarchy, no fake richness. Images yield before type and Stop.

---

# Volume XI — Cross-Platform Design

One identity. One pulse. One host. One grid. Mode changes density and reach, not soul.

| Surface | Keep | Yield |
|---|---|---|
| Mobile | Attempt, stop, back, voice, thumb reach | Dense instruments |
| Tablet | Attempt plus one instrument | Enterprise density |
| Desktop | Full instruments for the role | Nothing Core needed on mobile |
| Web | Same OS | Native sensors as required |
| Foldables | Continuity across fold; no new hello | Two unrelated primaries |
| Wearables | Pause, next, stop, due glance | Teaching layouts |
| Vision | Optional point; large type in space | Required gaze or face |
| TV | Shared room; large type; no private memory edit | Personal forget flows |
| Automotive | Short, stoppable, glanceable | Deep practice |
| Voice-only | Full host path | Visual hierarchy |
| Future | Labeled path + host + grid | Any required new sensor |

A platform that cannot show a labeled Stop does not offer a guest.

---

# Volume XII — Design Review Handbook

Opinion is not a vote. The room answers. A single “we will make it accessible later” fails the review.

1. What is the primary action?
2. What is the secondary action?
3. What can disappear?
4. What distracts?
5. What teaches?
6. What reduces cognitive load?
7. What supports continuity?
8. What supports trust?
9. What supports accessibility?
10. What supports learning?
11. Would this work without animation?
12. Would this work with voice?
13. Would this work offline?
14. Would this work for a child?
15. Would this work for an elderly learner?
16. Is beauty serving function?
17. Is there one dominant?
18. Do two actions compete? If yes, fail.
19. Is Back not restart?
20. Is Stop reachable by thumb on a phone?
21. Is any control hover-only?
22. Is any meaning color-only?
23. Is focus visible?
24. Is the keyboard order the meaning order?
25. Does type grow two steps without hiding Stop?
26. Does dark mode keep hierarchy?
27. Does high contrast keep state?
28. Does reduced motion keep meaning?
29. Is the grid 8, or is the exception written?
30. Is density right for the workspace?
31. Is the attempt denser than a dashboard? If yes, fail.
32. Is brand pulse painting the whole surface?
33. Is a modal for consequence, not for a tour?
34. Is a toast asking for a decision? If yes, fail.
35. Does a card hold one job?
36. Does a table become the same objects on small glass?
37. Does a chart have a question and a text equivalent?
38. Is empty named, explained, and given a first step?
39. Is error a door with a next act?
40. Is the skeleton the shape of the truth?
41. Is progress honest?
42. Does motion have a named verb?
43. Is there more than one motion on the attempt?
44. Is there shake, bounce, or confetti?
45. Is sound anything but the tutor?
46. Is an icon paired with a word on a commitment?
47. Is there a commenting character?
48. Is AI drawn as theater (brains, sparkles, fake thought)?
49. Is a guest named visually as well as in language?
50. Does takeover use a consequence dialog?
51. Does a deep link confirm before replacing a live attempt?
52. Are safe areas respected?
53. Is the reading measure holdable?
54. Is Devanagari (or the shipped script) unclipped?
55. Is the font philosophy intact (no third family)?
56. Is light type used for teaching text? If yes, fail.
57. Does contrast meet duty on every state?
58. Would this work on a cheap phone?
59. Would this work on low bandwidth?
60. Would this work as a phone call with almost no UI?
61. If this screen vanished, is the attempt worse?
62. What Experience principle does this serve?
63. What Language rule does the copy obey?
64. What Architecture workspace is this?
65. Is this nineteen tabs?
66. Is Search confirming before it steals the session?
67. Can a teacher explain this screen in one breath?
68. Can a parent understand it without a legend?
69. Does enterprise density still have one primary?
70. Is fashion the reason for a color, a motion, or a face? If yes, fail.

The critique ends when the attempt is clearer, calmer, and more possible — or the work goes back.

---

# Volume XIII — Design Tokens Constitution

Tokens are the only way a value enters a surface. A raw magic number in a screen is drift.

Tokens name **meaning**, not a season. We do not ship `blue-sky-2026`. We ship `color.brand.pulse`.

## Color tokens

- `color.brand.pulse` / `color.brand.pulse-on` (ink on pulse)
- `color.semantic.success` / `warning` / `error` / `info`
- `color.neutral.fg` / `fg-muted` / `border` / `border-strong`
- `color.surface.canvas` / `raised` / `overlay` / `sunken`
- `color.state.focus` / `pressed` / `disabled`
- Theme overlays: `.light` `.dark` `.high-contrast` resolve the same names

## Typography tokens

- `type.family.text` / `type.family.mark` (mark only)
- `type.role.title` / `primary` / `body` / `meta`
- Each role: size, weight, line-height, letter as needed per script
- `type.scale.step` is the multiplier Dynamic Type uses

## Elevation tokens

- `elevation.0` (canvas) through a short stack
- Overlay elevation is for consequence, not for decoration
- Dark theme may use border more than shadow; the token still means “raised”

## Radius tokens

- A short set: control, cluster, full (pills for state, not for everything)
- Radius does not become a personality per team

## Border tokens

- `border.thin` / `strong`
- High contrast may resolve strong by default
- Hairline as fashion is not a token

## Motion tokens

- `motion.duration.short` / `medium` / `consequence`
- `motion.ease.enter` / `exit` / `progress`
- `motion.verb.arrive` / `leave` / `confirm` / `fail-closed` / `progress` / `takeover`
- Reduced motion resolves durations to instant

## Spacing tokens

- `space.1` = 4 (optical only)
- `space.2` = 8, then multiples of 8
- Named roles: `space.inset.cluster`, `space.inset.dialog`, `space.gutter.outer`, `space.stack.sibling`, `space.stack.section`

## Size tokens

- `size.control.min` (touch)
- `size.icon.sm` / `md` / `lg`
- `size.stop.reach` (thumb-safe)
- `size.measure.max` (reading width)

## Icon tokens

- `icon.stroke`
- `icon.size` bound to size tokens
- `icon.on-color` for pulse and semantic fills

## Theme tokens

- Theme is a resolution of the same names
- A new theme is a new resolution, not a new vocabulary
- Experimental themes cannot rename semantics

A token that exists only to satisfy a mock is deleted.  
A screen that bypasses tokens has failed review.

---

# Volume XIV — Future Interface Design

New computers do not earn a new soul.

**AI-first interfaces**  
The host is first. The pixels serve the next act and the voice state. We do not build a cockpit of models. We do not draw thinking.

**Spatial computing**  
The attempt is a stable place in space. Instruments orbit only if the person summoned them. A guest is a named arrival, not a creature in the corner. Gaze is not a click by default.

**Mixed reality**  
The world may be the diagram. Labels remain type, not burned into a texture. Privacy: no silent capture of the room.

**Ambient computing**  
A speaker in a kitchen is voice-only law: host, stop, no new hello, honest offline. Ambient is not always-listening theater.

**Wearables**  
Glance and control. No teaching layout. Haptics rare.

**Robotics**  
A body in the world is a guest of the host, not a new tutor brand. Motion of a robot is safety-first. Cute gait is not a lesson.

**Brain–computer interfaces**  
If they exist, they are an optional input like voice. Consent at need. They do not read a child for “engagement.” Stop must exist outside the BCI.

**Invisible interfaces**  
When the glass disappears, the labeled path still exists somewhere: a voice command, a hardware stop, a companion screen. Invisible is not unaccountable.

**Context-aware design**  
Context may change density (walking, driving, classroom). It may not change identity, license, or the host. Context is not an excuse to skip confirm on takeover, forget, or end.

The future is allowed to add a sense. It is not allowed to add a required confession, a required stare, or a required spectacle.

---

# Volume XV — Design Manifesto

Great educational design feels like a quiet table.

The problem is already hard. The room does not compete. The next act is obvious. The way back is obvious. The miss does not change the furniture. The success does not throw a parade. The voice and the type say the same thing. The person forgets the product and remembers the step.

That forgetting is the point.

Interfaces should disappear behind learning because the OS is not the subject. The attempt is the subject. When they remember our gradient and not the equation, we decorated a failure.

Consistency creates trust because the body learns our rooms the way it learns a house: the door is here, the light is here, the dangerous drawer is labeled. A house that rearranges itself every season is not taste. It is unrest. Unrest is the enemy of a tired learner.

Beauty exists to support understanding. Hierarchy is beautiful. A line length the eye can hold is beautiful. A contrast that an elder can read is beautiful. A motion that only confirms is beautiful. Beauty that costs a cheap phone, a Devanagari matra, or a color-blind warning is vanity in good type.

What must never change:

One primary.  
One pulse.  
One grid of eight.  
One host presence that is state, not a mascot.  
One way back that is not a restart.  
One Stop the hand can find.  
Meaning without color, without motion, without hover.  
Tokens instead of fashion.  
Restraint instead of festival.

Glass will thin. Rooms will become air. Models will speak in other throats.

If the table is still quiet, and the next try is still obvious, the design system has lived.

If the hall is loud and the person is lost, we have only kept a library of components.

Stay on the line. Draw less. Mean it.
