'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import type { AgentManifest } from '@/lib/agent-runtime/engine';
import { MENTOR_POLICIES, listMentors } from '@/lib/mentors/engine';

type MentorSnapshot = {
  mentors: AgentManifest[];
  policies: typeof MENTOR_POLICIES;
};

const MentorContext = createContext<MentorSnapshot | null>(null);

export function useMentors(): MentorSnapshot {
  const ctx = useContext(MentorContext);
  if (!ctx) throw new Error('useMentors must be used inside MentorProvider');
  return ctx;
}

export function MentorProvider({ children }: { children: ReactNode }) {
  const value = useMemo(() => ({ mentors: listMentors(), policies: MENTOR_POLICIES }), []);
  return <MentorContext.Provider value={value}>{children}</MentorContext.Provider>;
}
