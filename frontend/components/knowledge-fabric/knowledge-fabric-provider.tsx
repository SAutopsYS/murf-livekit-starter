'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import type { AdaptiveSnapshot } from '@/lib/adaptive/types';
import { buildKnowledgeFabric } from '@/lib/knowledge-fabric/engine';
import type { KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';
import type { LearningIntelligence } from '@/lib/learning/types';

const FabricContext = createContext<KnowledgeSnapshot | null>(null);

export function useKnowledgeFabric(): KnowledgeSnapshot {
  const ctx = useContext(FabricContext);
  if (!ctx) throw new Error('useKnowledgeFabric must be used inside KnowledgeFabricProvider');
  return ctx;
}

export function KnowledgeFabricProvider({
  intelligence,
  adaptive = null,
  children,
}: {
  intelligence: LearningIntelligence;
  adaptive?: AdaptiveSnapshot | null;
  children: ReactNode;
}) {
  const snapshot = useMemo(
    () => buildKnowledgeFabric(intelligence, adaptive),
    [intelligence, adaptive]
  );
  return <FabricContext.Provider value={snapshot}>{children}</FabricContext.Provider>;
}
