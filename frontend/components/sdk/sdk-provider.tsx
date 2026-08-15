'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { type SdkSnapshot, buildSdkSnapshot } from '@/lib/sdk/engine';

const SdkContext = createContext<SdkSnapshot | null>(null);

export function useSdk(): SdkSnapshot {
  const ctx = useContext(SdkContext);
  if (!ctx) throw new Error('useSdk must be used inside SdkProvider');
  return ctx;
}

export function SdkProvider({ children }: { children: ReactNode }) {
  const value = useMemo(() => buildSdkSnapshot(), []);
  return <SdkContext.Provider value={value}>{children}</SdkContext.Provider>;
}
