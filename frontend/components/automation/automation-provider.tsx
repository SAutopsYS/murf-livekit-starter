'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { type AutomationWorkflow, createAutomation } from '@/lib/automation/engine';

const AutomationContext = createContext<AutomationWorkflow | null>(null);

export function useAutomation(): AutomationWorkflow {
  const ctx = useContext(AutomationContext);
  if (!ctx) throw new Error('useAutomation must be used inside AutomationProvider');
  return ctx;
}

export function AutomationProvider({ children }: { children: ReactNode }) {
  const value = useMemo(() => createAutomation('local', 'LearningFinished'), []);
  return <AutomationContext.Provider value={value}>{children}</AutomationContext.Provider>;
}
