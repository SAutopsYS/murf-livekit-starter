# 14 — Naming Convention

Honest names. A lie in a name becomes a lie in the product.

---

## Files

| Area | Pattern | Example |
|---|---|---|
| React component | `kebab-case.tsx` | `welcome-view.tsx` |
| Hook | `use-thing.ts` | `use-agent-audio-visualizer-wave.ts` |
| Python module | `snake_case.py` | `math_specialist.py` |
| Doc | `NN_TITLE.md` or existing salora slugs | `01_PRODUCT_BIBLE.md` |
| Token CSS | `tokens.css` | — |

No `utils2.ts`. No `new-agent-final.py`.

## Folders

kebab-case or existing package names (`specialists`, `agents-ui`).  
No `misc/`, `tmp/`, `new/`.

## Hooks

`use` + noun + optional qualifier: `useAgent`, `useDebug`.  
Do not name a hook `useTranscriptLogger`.

## Components

`PascalCase` export: `WelcomeView`, `ThemeToggle`.  
Filename remains kebab-case.

## Pages / routes

App Router folders: `analytics`, `enterprise`.  
Future: `workspace`, `learning` — not `dashboard2`.  
URL is a room name, not a team name.

## Functions

`snake_case` in Python, `camelCase` in TypeScript.  
Verbs: `forget_learner`, `fail_closed_to_host`, `search_learning_knowledge`.  
Forbidden: `processData`, `handleThing` without a noun.

## Variables

Same case as language.  
`isLive`, `resume_from_specialist`.  
Do not call a reconnect flag `isHandoff`.

## Types / interfaces

TS: `PascalCase`. `AppConfig`, `SandboxConfig`.  
No `IUser`.  
Python: `PascalCase` models.

## Enums

Closed sets. `ConnectionState` (LiveKit). New: `GuestId`, `LearningState`.  
Values: `math_practice`, not `MathSpecialistV2`.

## Events

Past tense, no body of speech: `GuestFailedClosed`, `ForgetCompleted`, `VisitResumed`.  
Never `UtteranceHeard`.

## AI agents

Registry id: `snake_case`. Host remains the default assistant.  
Guest: `math_practice` (live). Placeholders stay disabled and named for their subgraph.  
Do not name an agent `god_mode` or `new_tutor`.

## Tools

Function tool names: `snake_case`, verb+noun: `search_learning_knowledge`, `forget_me`.  
Registry keys match the callable name.

## Knowledge packs

`topic_or_locale` in the JSON repo. Stable ids.  
`equivalent-to` in data, not `hindi_copy_final`.

## Memory

Fields: licensed nouns (`preferred_language`, `display_name`).  
Never `raw_history`, `transcript`, `full_chat`.  
Forget is `forget`, not `soft_delete_maybe`.

## Brand strings

Product: `SALORA OS`. Company: `SALORA AI`.  
Code constants: `SALORA_BRAND` in `lib/brand.ts`.  
Do not introduce `SaloraApp`, `SALORA_V2`, or `MurfTutor` on new surfaces.

Cross-check: [08 Coding Standards](08_CODING_STANDARDS.md), [06 AI Architecture](06_AI_ARCHITECTURE_BIBLE.md).
