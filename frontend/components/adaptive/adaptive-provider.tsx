'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
import type { AdaptiveSnapshot } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

const AdaptiveContext = createContext<AdaptiveSnapshot | null>(null);

export function useAdaptive(): AdaptiveSnapshot {
  const ctx = useContext(AdaptiveContext);
  if (!ctx) throw new Error('useAdaptive must be used inside AdaptiveProvider');
  return ctx;
}

export function AdaptiveProvider({
  intelligence,
  children,
}: {
  intelligence: LearningIntelligence;
  children: ReactNode;
}) {
  const snapshot = useMemo(() => buildAdaptiveSnapshot(intelligence), [intelligence]);
  return <AdaptiveContext.Provider value={snapshot}>{children}</AdaptiveContext.Provider>;
}
