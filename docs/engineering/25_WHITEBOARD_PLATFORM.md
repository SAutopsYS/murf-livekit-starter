# 25 — Whiteboard Platform

Visual reasoning workspace. Not a drawing app. Not a renderer in this phase.

---

## Whiteboard architecture

```
Studio document (whiteboard_ref)
        │
WhiteboardProvider → WhiteboardEngine
        │
WhiteboardService → Canvas / Element / Diagram / Selection / History / Import / Export
        │
Knowledge Fabric relation kinds (shared)
```

No infinite canvas, sticky UI, or mind-map view ships here.

---

## Canvas model

Canvas, layer, frame, group, element, connector, region, viewport, selection, snapshot.

Each object: id, type, bounds, metadata, owner, permissions, timestamps.

---

## Element model

text, sticky, shape, image, code, markdown, table, diagram, equation, AI block, voice block, knowledge ref, document ref, workflow ref.

Voice block is a **reference** to a session id — not a waveform clone.

---

## Relationship engine

**Same kinds as Knowledge Fabric:** depends_on, related_to, teaches, corrects, improves, contradicts, supports, derived_from, recommended_by, belongs_to.

Visual aliases (contains, connects_to, visualizes) map onto those kinds. No second graph.

---

## AI Assist

Specs only: generate diagram, explain, summarize board, create flow, expand idea, convert to notes/workflow, mind map, analyze structure.

`assistSpec()` returns `{ renderer: 'none' }`. Orchestrator may run later. No generation UI.

---

## Collaboration model

Roles: owner, editor, commenter, viewer. Presence, cursor, selection, awareness, conflict resolution are typed — not implemented. LiveKit data channels stay for voice, not for this canvas yet.

---

## Backend services

`services/whiteboard.py`. Events: CanvasCreated/Opened, Element*, SelectionChanged, ViewportChanged, HistoryRecorded, DiagramGenerated, BoardExported.

Import/export formats architected: markdown, PDF, PNG, SVG, JSON, Studio document, knowledge objects. Future adapters: Notion, Miro, Figma, Obsidian.

---

## Performance

Viewport virtualization, incremental render, lazy assets, history compression, undo/redo **architecture**. Do not load this engine on `/`.

---

## Accessibility

Future renderer: keyboard traversal, ARIA, screen-reader summary of selection, reduced motion, high contrast. Architecture records selection so AT can speak it later.

---

## Future

Memory Graph can project `knowledge_ref` elements. Studio opens a board as a document. Marketplace may ship templates. Still one relation catalog.
