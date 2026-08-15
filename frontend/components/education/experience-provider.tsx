'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { type ExperienceSnapshot, buildExperience } from '@/lib/education/engine';
import type { Role } from '@/lib/platform/rbac';

const ExperienceContext = createContext<ExperienceSnapshot | null>(null);

export function useExperience(): ExperienceSnapshot {
  const ctx = useContext(ExperienceContext);
  if (!ctx) throw new Error('useExperience must be used inside ExperienceProvider');
  return ctx;
}

export function ExperienceProvider({
  role = 'student',
  children,
}: {
  role?: Role;
  children: ReactNode;
}) {
  const value = useMemo(() => buildExperience(role), [role]);
  return <ExperienceContext.Provider value={value}>{children}</ExperienceContext.Provider>;
}
