import { describe, expect, it } from 'vitest';
import { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
import { buildKnowledgeFabric } from '@/lib/knowledge-fabric/engine';
import { forgetNode, strengthenNode } from '@/lib/knowledge-fabric/lifecycle';
import { mayPersistLongTerm } from '@/lib/knowledge-fabric/policies';
import { retrieveKnowledge } from '@/lib/knowledge-fabric/retrieval';
import { buildLearningIntelligence } from '@/lib/learning/engine';

describe('knowledge fabric', () => {
  it('projects nodes without utterance fields', () => {
    const intel = buildLearningIntelligence(null, null);
    const adaptive = buildAdaptiveSnapshot(intel);
    const fabric = buildKnowledgeFabric(intel, adaptive);
    expect(fabric.nodes.length).toBeGreaterThan(0);
    const serialized = JSON.stringify(fabric);
    expect(serialized).not.toMatch(/utterance/);
    expect(mayPersistLongTerm(false, false)).toBe(false);
    expect(mayPersistLongTerm(true, true)).toBe(false);
  });

  it('retrieves and can forget a node', () => {
    const intel = buildLearningIntelligence(null, null);
    const adaptive = buildAdaptiveSnapshot(intel);
    const fabric = buildKnowledgeFabric(intel, adaptive);
    const hits = retrieveKnowledge(fabric, { text: fabric.nodes[0]?.title ?? 'skill' });
    expect(Array.isArray(hits)).toBe(true);
    const first = fabric.nodes[0];
    if (!first) return;
    const stronger = strengthenNode(fabric, first.id);
    const forgotten = forgetNode(stronger, first.id);
    expect(forgotten.nodes.some((node) => node.id === first.id)).toBe(false);
  });
});
