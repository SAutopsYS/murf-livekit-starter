'use client';

import { useKnowledgeFabric } from '@/components/knowledge-fabric/knowledge-fabric-provider';
import { InsightCard } from '@/components/system';

export function KnowledgeSummary() {
  const { metrics, retrieved } = useKnowledgeFabric();

  return (
    <InsightCard title="Knowledge fabric">
      <p className="sr-only">
        {metrics.nodeCount} knowledge objects. {metrics.edgeCount} relationships. No transcripts
        stored.
      </p>
      <p className="text-muted-foreground text-sm">
        {metrics.nodeCount} objects · {metrics.edgeCount} links · {metrics.longTerm} long-term
      </p>
      <ul className="mt-3 space-y-1 text-sm">
        {retrieved.slice(0, 5).map((node) => (
          <li key={node.id}>
            {node.title}
            <span className="text-muted-foreground"> · {node.type}</span>
          </li>
        ))}
      </ul>
    </InsightCard>
  );
}
