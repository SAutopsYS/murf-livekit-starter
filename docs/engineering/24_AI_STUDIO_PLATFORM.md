# 24 — AI Studio Platform

Studio is an **instrument**, not an app. It owns creation. Voice still owns the hall.

No editor, canvas, notebook UI, or workflow builder in this phase.

---

## Studio architecture

```
OsShell ⌘K
    │
StudioProvider  →  buildStudioSnapshot()
    │
StudioService (backend) → Project / Document / Workflow / Prompt / Asset / Notebook / Template
```

Frontend: `lib/studio/*`, `components/studio/studio-provider.tsx`.  
`autoload` is not a concept here — do not mount on the hall.

Commands reuse Phase 3 palette via `getStudioCommands()` (all `planned`).

---

## Project model

Kinds: project, workspace, folder, asset, document, prompt, conversation, notebook, workflow, template.

Fields: id, title, owner, organization, permissions, tags, createdAt, updatedAt, metadata.

---

## Document model

Kinds: markdown, rich text, whiteboard ref, code, notes, AI output, prompt, research, summary, transcript **reference** (never a stored utterance).

Knowledge Fabric may reference these ids. Do not duplicate storage.

---

## Workflow engine

Actions: draft, review, improve, translate, explain, summarize, brainstorm, generate, analyze, research.

`WorkflowService.start/finish` emits events. No generation UI.

---

## Prompt engine

Templates with variables, version, validation-by-shape. Default templates live in `lib/studio/engine.ts`. No hardcoded prompts in product UI.

---

## Backend services

`services/studio.py`: StudioService + child services. In-memory store until a table exists. RBAC: `studio.access`.

---

## Event flow

ProjectCreated, ProjectOpened, DocumentUpdated, WorkflowStarted/Finished, PromptExecuted, TemplateApplied, AssetImported, NotebookCreated.

Subscribe through `services.events`.

---

## Security

Reuse Phase 11 RBAC. Teacher / admin / operator hold `studio.access`. Ownership + organization on every record. Audit = event bus. Version history is a field on prompts (`version`). Sharing is permissions on the record — not a new ACL engine.

---

## Performance

Lazy snapshot build. Incremental in-memory writes. Autosave is an event name, not a timer on the hall. Voice latency unchanged.

---

## Accessibility

Keyboard-first commands (⌘K). Future editor must honor ARIA, focus, high contrast, `prefers-reduced-motion`. No canvas in this phase.

---

## Future

Whiteboard documents use `whiteboard_ref`. Marketplace templates plug into `TemplateService`. SDK uses `ApiEnvelope`.
