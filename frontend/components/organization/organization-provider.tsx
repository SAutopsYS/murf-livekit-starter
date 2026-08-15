'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { emptyOrganization } from '@/lib/organization/engine';
import type { OrganizationSnapshot } from '@/lib/organization/types';

const OrganizationContext = createContext<OrganizationSnapshot | null>(null);

export function useOrganization(): OrganizationSnapshot {
  const ctx = useContext(OrganizationContext);
  if (!ctx) throw new Error('useOrganization must be used inside OrganizationProvider');
  return ctx;
}

export function OrganizationProvider({
  snapshot,
  children,
}: {
  snapshot?: OrganizationSnapshot;
  children: ReactNode;
}) {
  const value = useMemo(() => snapshot ?? emptyOrganization(), [snapshot]);
  return <OrganizationContext.Provider value={value}>{children}</OrganizationContext.Provider>;
}
