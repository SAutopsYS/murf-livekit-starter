'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import { type AgentRuntimeSnapshot, buildAgentRuntime } from '@/lib/agent-runtime/engine';

const AgentRuntimeContext = createContext<AgentRuntimeSnapshot | null>(null);

export function useAgentRuntime(): AgentRuntimeSnapshot {
  const ctx = useContext(AgentRuntimeContext);
  if (!ctx) throw new Error('useAgentRuntime must be used inside AgentRuntimeProvider');
  return ctx;
}

export function AgentRuntimeProvider({ children }: { children: ReactNode }) {
  const value = useMemo(() => buildAgentRuntime(), []);
  return <AgentRuntimeContext.Provider value={value}>{children}</AgentRuntimeContext.Provider>;
}
