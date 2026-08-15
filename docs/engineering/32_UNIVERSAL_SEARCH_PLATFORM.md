# 32 — Universal Search Platform

One search layer. No second memory. No second graph.

Consumes `knowledge.search`, Knowledge Fabric `retrieveKnowledge`, marketplace catalog, agent runtime.

---

## Engine

`SearchService` / `SearchProvider`.

Modes: keyword, semantic (ranked fabric fields), hybrid, context, ai, filtered, organization.

Kinds: documents, knowledge, skills, projects, whiteboards, workflows, plugins, agents, learning, timeline, recommendations, organizations.

---

## Index

`IndexService.refresh()` emits `SearchIndexed`. Store stays the existing JSON/SQLite/projections. Job: `search_index`.

---

## Ranking / suggestions

Score sort. Suggestions are hit titles. No vector DB in this repo.

---

## Phase 27

`DiscoveryService` is an alias of `SearchService`. Do not add a second index.
