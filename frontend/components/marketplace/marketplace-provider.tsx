'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { buildMarketplaceSnapshot } from '@/lib/marketplace/engine';
import type { MarketplaceSnapshot } from '@/lib/marketplace/types';

const MarketplaceContext = createContext<MarketplaceSnapshot | null>(null);

export function useMarketplace(): MarketplaceSnapshot {
  const ctx = useContext(MarketplaceContext);
  if (!ctx) throw new Error('useMarketplace must be used inside MarketplaceProvider');
  return ctx;
}

export function MarketplaceProvider({
  snapshot,
  children,
}: {
  snapshot?: MarketplaceSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => snapshot ?? buildMarketplaceSnapshot(), [snapshot]);
  return <MarketplaceContext.Provider value={value}>{children}</MarketplaceContext.Provider>;
}
