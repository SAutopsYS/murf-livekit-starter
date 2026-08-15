# Learning platform

Three projections. One Voice Pipeline. No second score store.

| Engine | Job | Authority |
| --- | --- | --- |
| Learning Engine | Profile, skills, insights, recommendations, timeline | Existing analytics + memory APIs |
| Adaptive Engine | Mastery, revision, routing *advice* | SpecialistRouter still routes |
| Knowledge Fabric | Nodes and relations over knowledge search | Same JSON search, no new DB |

## Learning Engine

Canonical: [19 Learning Intelligence](../engineering/19_LEARNING_INTELLIGENCE.md).  
`19_LEARNING_ENGINE.md` is a pointer to that file.

`buildLearningIntelligence` + `LearningProvider` project current APIs. Scores do not persist onto `User`.

## Adaptive Engine

Canonical: [20 Adaptive Learning Engine](../engineering/20_ADAPTIVE_LEARNING_ENGINE.md).

Frontend adaptive **advises**. Backend `AdaptiveService.decide` calls SpecialistRouter. Do not add a second router.

## Knowledge Fabric

Canonical: [21 Knowledge Fabric](../engineering/21_KNOWLEDGE_FABRIC.md).

Semantic memory, retrieval, lifecycle. Memory Graph explores the fabric. It does not write `memory.db`.

## Related

- [Search Platform](search-platform.md)
- [25 Learning Engine constitution](../salora/25-learning-engine.md)
