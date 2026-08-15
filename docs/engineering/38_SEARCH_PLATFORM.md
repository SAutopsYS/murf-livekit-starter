# 38 — Search & Universal Discovery

Discovery **is** [32](32_UNIVERSAL_SEARCH_PLATFORM.md). Canonical name: **Search Platform**.

Public summary: [../architecture/search-platform.md](../architecture/search-platform.md).

`DiscoveryService.search` delegates to `SearchService`. Frontend `searchUniversal` uses fabric retrieval + marketplace + agents.

Vector search is a future adapter on the same `SearchHit` contract. Do not stand up a second index.
