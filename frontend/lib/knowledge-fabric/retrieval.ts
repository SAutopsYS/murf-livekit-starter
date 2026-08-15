import type { KnowledgeEdge, KnowledgeNode, RetrievalQuery } from '@/lib/knowledge-fabric/types';

function tokens(text: string): string[] {
  return text.toLowerCase().match(/[a-z0-9]{3,}/g) ?? [];
}

export function retrieveKnowledge(
  graph: { nodes: KnowledgeNode[]; edges: KnowledgeEdge[] },
  query: RetrievalQuery = {}
): KnowledgeNode[] {
  const limit = query.limit ?? 8;
  const asked = query.text ? tokens(query.text) : [];

  const scored = graph.nodes
    .filter((node) => (query.layer ? node.layer === query.layer : true))
    .filter((node) => (query.type ? node.type === query.type : true))
    .map((node) => {
      const hay = `${node.title} ${node.summary}`.toLowerCase();
      let score = node.importance + node.confidence * 0.3;
      for (const token of asked) {
        if (hay.includes(token)) score += 2;
      }
      if (node.layer === 'working') score += 0.2;
      if (node.layer === 'long_term') score += 0.4;
      return { node, score };
    })
    .sort((a, b) => b.score - a.score);

  return scored.slice(0, limit).map((item) => item.node);
}
