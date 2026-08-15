'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { buildStudioSnapshot } from '@/lib/studio/engine';
import type { StudioSnapshot } from '@/lib/studio/types';

const StudioContext = createContext<StudioSnapshot | null>(null);

export function useStudio(): StudioSnapshot {
  const ctx = useContext(StudioContext);
  if (!ctx) throw new Error('useStudio must be used inside StudioProvider');
  return ctx;
}

export function StudioProvider({
  snapshot,
  children,
}: {
  snapshot?: StudioSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => snapshot ?? buildStudioSnapshot(), [snapshot]);
  return <StudioContext.Provider value={value}>{children}</StudioContext.Provider>;
}
