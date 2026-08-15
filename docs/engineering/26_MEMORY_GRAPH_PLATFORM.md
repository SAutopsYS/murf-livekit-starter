# 26 — Memory Graph Platform

Visualization and exploration of the **Knowledge Fabric**.  
This is not a new memory engine.

Law: [21 Knowledge Fabric](21_KNOWLEDGE_FABRIC.md). Enterprise `MemoryGraphService` stays the consented/aggregate projection.

---

## Memory Graph architecture

```
useKnowledgeFabric() / buildKnowledgeFabric()
            │
MemoryGraphProvider → buildMemoryGraph(fabric)
            │
queries use retrieveKnowledge()
            │
backend MemoryGraphService wraps knowledge.search + enterprise graph
```

`MemoryGraphProvider` takes a fabric snapshot. It never fetches. It never writes `memory.db`.

Do not mount on the hall.

---

## Graph model

Node, edge, cluster, collection, neighborhood, path, layer, snapshot, view.

View state: focus, breadcrumbs, pins, bookmarks, zoom. Architecture only — no force layout.

---

## Node model

Fabric types plus registry extras: agent, session, project, document, whiteboard, workflow. Extras are **references**, not a second store.

---

## Relationship explorer

Reuse `KnowledgeRelationKind`. No second relationship model.

---

## Query engine

related, similar, learning path, weak/strong, history, next, by skill/topic/confidence.

All queries call `retrieveKnowledge` or sort fabric fields. Backend `GraphQueryService` calls `search_knowledge`.

---

## Navigation

zoom, focus, breadcrumbs, history, pin, bookmarks, expand/collapse, path highlight — in `GraphView`. No 3D. No force-directed animation.

---

## Backend services

`services/memory_graph.py`: MemoryGraphService, KnowledgeExplorerService, GraphQueryService, RelationshipService, NodeService, ClusterService, BookmarkService, GraphExportService.

NodeService reads `enterprise.visualization.MemoryGraphService`. Write path does not exist.

---

## Event flow

GraphOpened, NodeSelected/Expanded/Collapsed, RelationshipFocused, GraphFiltered, GraphExported, BookmarkCreated, QueryExecuted, NavigationChanged.

---

## Performance

Lazy expansion, memoized view, snapshot cache, background index job spec (`graph_index`). Voice unaffected.

---

## Accessibility

Keyboard focus on `focusId`. Screen-reader summary = node title + relation count. High contrast and reduced motion when a renderer exists. ARIA graph roles belong to that future view, not a fake canvas here.

---

## Future

Whiteboard `knowledge_ref` and Studio documents appear as reference nodes. Marketplace does not get a private graph. SDK exports JSON through `GraphExportService` (architected).
