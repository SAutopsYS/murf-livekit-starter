'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { buildWhiteboardSnapshot } from '@/lib/whiteboard/engine';
import type { WhiteboardSnapshot } from '@/lib/whiteboard/types';

const WhiteboardContext = createContext<WhiteboardSnapshot | null>(null);

export function useWhiteboard(): WhiteboardSnapshot {
  const ctx = useContext(WhiteboardContext);
  if (!ctx) throw new Error('useWhiteboard must be used inside WhiteboardProvider');
  return ctx;
}

export function WhiteboardProvider({
  snapshot,
  children,
}: {
  snapshot?: WhiteboardSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => snapshot ?? buildWhiteboardSnapshot(), [snapshot]);
  return <WhiteboardContext.Provider value={value}>{children}</WhiteboardContext.Provider>;
}
