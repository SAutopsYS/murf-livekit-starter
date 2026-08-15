'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import type { KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';
import { buildMemoryGraph } from '@/lib/memory-graph/engine';
import type { MemoryGraphSnapshot } from '@/lib/memory-graph/types';

const MemoryGraphContext = createContext<MemoryGraphSnapshot | null>(null);

export function useMemoryGraph(): MemoryGraphSnapshot {
  const ctx = useContext(MemoryGraphContext);
  if (!ctx) throw new Error('useMemoryGraph must be used inside MemoryGraphProvider');
  return ctx;
}

export function MemoryGraphProvider({
  fabric,
  children,
}: {
  fabric: KnowledgeSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => buildMemoryGraph(fabric), [fabric]);
  return <MemoryGraphContext.Provider value={value}>{children}</MemoryGraphContext.Provider>;
}
