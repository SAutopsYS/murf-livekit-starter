import type { KnowledgeNode, KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';

function touch(node: KnowledgeNode, patch: Partial<KnowledgeNode>): KnowledgeNode {
  return { ...node, ...patch, updatedAt: new Date().toISOString() };
}

export function strengthenNode(snapshot: KnowledgeSnapshot, id: string): KnowledgeSnapshot {
  return {
    ...snapshot,
    nodes: snapshot.nodes.map((node) =>
      node.id === id
        ? touch(node, {
            importance: Math.min(1, node.importance + 0.08),
            confidence: Math.min(1, node.confidence + 0.05),
          })
        : node
    ),
  };
}

export function weakenNode(snapshot: KnowledgeSnapshot, id: string): KnowledgeSnapshot {
  return {
    ...snapshot,
    nodes: snapshot.nodes.map((node) =>
      node.id === id
        ? touch(node, {
            importance: Math.max(0, node.importance - 0.08),
            confidence: Math.max(0, node.confidence - 0.05),
          })
        : node
    ),
  };
}

export function archiveNode(snapshot: KnowledgeSnapshot, id: string): KnowledgeSnapshot {
  return {
    ...snapshot,
    nodes: snapshot.nodes.map((node) =>
      node.id === id
        ? touch(node, { layer: 'long_term', importance: Math.max(0.1, node.importance * 0.5) })
        : node
    ),
  };
}

export function forgetNode(snapshot: KnowledgeSnapshot, id: string): KnowledgeSnapshot {
  return {
    ...snapshot,
    nodes: snapshot.nodes.filter((node) => node.id !== id),
    edges: snapshot.edges.filter((edge) => edge.from !== id && edge.to !== id),
  };
}

export function expireStale(snapshot: KnowledgeSnapshot, now = Date.now()): KnowledgeSnapshot {
  const keep = snapshot.nodes.filter((node) => {
    if (node.ttlSeconds == null) return true;
    const born = Date.parse(node.updatedAt);
    return Number.isNaN(born) || now - born < node.ttlSeconds * 1000;
  });
  const ids = new Set(keep.map((node) => node.id));
  return {
    ...snapshot,
    nodes: keep,
    edges: snapshot.edges.filter((edge) => ids.has(edge.from) && ids.has(edge.to)),
    metrics: {
      ...snapshot.metrics,
      nodeCount: keep.length,
    },
  };
}
