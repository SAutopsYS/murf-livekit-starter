# Search Platform

One search. No second index.

Canonical: [32 Universal Search](../engineering/32_UNIVERSAL_SEARCH_PLATFORM.md).  
[38 Discovery](../engineering/38_SEARCH_PLATFORM.md) is an alias of 32.

## Behavior

`SearchService.search` fans out to:

- `knowledge.search` (JSON lessons)
- Marketplace catalog
- Agent Runtime manifests

Frontend `searchUniversal` uses the same sources. `DiscoveryService` delegates to `SearchService`.

Vector search, if added later, is an adapter on the same `SearchHit` contract. Do not stand up a second engine.

## Related

- [Knowledge Fabric](learning-platform.md)
- [Enterprise Platform](enterprise-platform.md)
