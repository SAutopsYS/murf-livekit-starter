import { buildAgentRuntime } from '@/lib/agent-runtime/engine';
import { retrieveKnowledge } from '@/lib/knowledge-fabric/retrieval';
import type { KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';
import { buildMarketplaceSnapshot } from '@/lib/marketplace/engine';

export type SearchKind = 'document' | 'knowledge' | 'plugin' | 'agent' | 'project' | 'organization';

export type SearchMode = 'keyword' | 'semantic' | 'hybrid' | 'filtered';

export type SearchHit = {
  kind: SearchKind;
  id: string;
  title: string;
  score: number;
  source: string;
};

export function searchUniversal(
  query: string,
  fabric: KnowledgeSnapshot | null,
  mode: SearchMode = 'hybrid'
): SearchHit[] {
  const hits: SearchHit[] = [];
  if (fabric) {
    for (const node of retrieveKnowledge(fabric, { text: query, limit: 6 })) {
      hits.push({
        kind: 'knowledge',
        id: node.id,
        title: node.title,
        score: node.importance,
        source: 'knowledge-fabric',
      });
    }
  }
  if (mode === 'hybrid' || mode === 'filtered') {
    for (const plugin of buildMarketplaceSnapshot().catalog) {
      if (!query || plugin.name.toLowerCase().includes(query.toLowerCase())) {
        hits.push({
          kind: 'plugin',
          id: plugin.id,
          title: plugin.name,
          score: 1,
          source: 'marketplace',
        });
      }
    }
    for (const agent of buildAgentRuntime().agents) {
      if (!query || agent.name.toLowerCase().includes(query.toLowerCase())) {
        hits.push({
          kind: 'agent',
          id: agent.id,
          title: agent.name,
          score: agent.live ? 2 : 0.4,
          source: 'agent-runtime',
        });
      }
    }
  }
  return hits.sort((a, b) => b.score - a.score);
}
