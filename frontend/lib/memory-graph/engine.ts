import { retrieveKnowledge } from '@/lib/knowledge-fabric/retrieval';
import type { KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';
import type { GraphQuery, GraphView, MemoryGraphSnapshot } from '@/lib/memory-graph/types';

export function viewFromFabric(fabric: KnowledgeSnapshot): GraphView {
  return {
    nodes: fabric.nodes,
    edges: fabric.edges,
    focusId: fabric.nodes[0]?.id ?? null,
    breadcrumbs: fabric.nodes[0] ? [fabric.nodes[0].id] : [],
    pins: [],
    bookmarks: [],
    zoom: 1,
  };
}

export function buildMemoryGraph(fabric: KnowledgeSnapshot): MemoryGraphSnapshot {
  return {
    fabric,
    view: viewFromFabric(fabric),
    source: 'knowledge-fabric',
  };
}

export function runGraphQuery(fabric: KnowledgeSnapshot, query: GraphQuery) {
  const limit = query.limit ?? 8;
  if (query.kind === 'strong') {
    return [...fabric.nodes].sort((a, b) => b.importance - a.importance).slice(0, limit);
  }
  if (query.kind === 'weak') {
    return [...fabric.nodes].sort((a, b) => a.confidence - b.confidence).slice(0, limit);
  }
  if (query.kind === 'by_confidence') {
    return fabric.nodes.filter((node) => node.confidence >= 0.6).slice(0, limit);
  }
  return retrieveKnowledge(fabric, { text: query.text, limit });
}

export function focusNode(snapshot: MemoryGraphSnapshot, id: string): MemoryGraphSnapshot {
  const exists = snapshot.fabric.nodes.some((node) => node.id === id);
  if (!exists) return snapshot;
  return {
    ...snapshot,
    view: {
      ...snapshot.view,
      focusId: id,
      breadcrumbs: [...snapshot.view.breadcrumbs, id].slice(-12),
    },
  };
}
