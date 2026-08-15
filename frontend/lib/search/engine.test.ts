import { describe, expect, it } from 'vitest';
import { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
import { buildKnowledgeFabric } from '@/lib/knowledge-fabric/engine';
import { buildLearningIntelligence } from '@/lib/learning/engine';
import { searchUniversal } from '@/lib/search/engine';

describe('universal search', () => {
  it('fans out to fabric and marketplace without a new store', () => {
    const fabric = buildKnowledgeFabric(
      buildLearningIntelligence(null, null),
      buildAdaptiveSnapshot(buildLearningIntelligence(null, null))
    );
    const hits = searchUniversal('skill', fabric, 'hybrid');
    expect(
      hits.some((item) => item.source === 'knowledge-fabric' || item.source === 'marketplace')
    ).toBe(true);
  });
});
