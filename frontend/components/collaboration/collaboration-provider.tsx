'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { type CollaborationSnapshot, emptyCollaboration } from '@/lib/collaboration/engine';

const CollaborationContext = createContext<CollaborationSnapshot | null>(null);

export function useCollaboration(): CollaborationSnapshot {
  const ctx = useContext(CollaborationContext);
  if (!ctx) throw new Error('useCollaboration must be used inside CollaborationProvider');
  return ctx;
}

export function CollaborationProvider({
  snapshot,
  children,
}: {
  snapshot?: CollaborationSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => snapshot ?? emptyCollaboration(), [snapshot]);
  return <CollaborationContext.Provider value={value}>{children}</CollaborationContext.Provider>;
}
