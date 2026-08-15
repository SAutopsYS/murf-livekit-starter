import { describe, expect, it } from 'vitest';
import { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
import { buildKnowledgeFabric } from '@/lib/knowledge-fabric/engine';
import { buildLearningIntelligence } from '@/lib/learning/engine';
import { buildMemoryGraph, focusNode, runGraphQuery } from '@/lib/memory-graph/engine';

describe('memory graph', () => {
  it('projects the fabric and never invents a second memory', () => {
    const intel = buildLearningIntelligence(null, null);
    const fabric = buildKnowledgeFabric(intel, buildAdaptiveSnapshot(intel));
    const graph = buildMemoryGraph(fabric);
    expect(graph.source).toBe('knowledge-fabric');
    expect(graph.view.nodes).toBe(fabric.nodes);
    const focused = focusNode(graph, fabric.nodes[0].id);
    expect(focused.view.focusId).toBe(fabric.nodes[0].id);
    const strong = runGraphQuery(fabric, { kind: 'strong', limit: 3 });
    expect(strong.length).toBeLessThanOrEqual(3);
  });
});
