'use client';

import {
  type ReactNode,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { type AnalyticsSummary, fetchAnalyticsSummary } from '@/lib/analytics';
import { type EnterpriseSnapshot, fetchEnterpriseSnapshot } from '@/lib/enterprise';
import { adaptInstruments } from '@/lib/learning/adapters';
import { eventsFromIntelligence } from '@/lib/learning/events';
import type { LearningEvent, LearningIntelligence } from '@/lib/learning/types';

type LearningListener = (event: LearningEvent) => void;

type LearningActions = {
  subscribe: (listener: LearningListener) => () => void;
  refresh: () => Promise<void>;
};

const SnapshotContext = createContext<LearningIntelligence | null>(null);
const ActionsContext = createContext<LearningActions | null>(null);

export function useLearning(): LearningIntelligence {
  const ctx = useContext(SnapshotContext);
  if (!ctx) throw new Error('useLearning must be used inside LearningProvider');
  return ctx;
}

export function useLearningActions(): LearningActions {
  const ctx = useContext(ActionsContext);
  if (!ctx) throw new Error('useLearningActions must be used inside LearningProvider');
  return ctx;
}

export function LearningProvider({
  children,
  autoload = false,
  analytics: analyticsProp = null,
  enterprise: enterpriseProp = null,
}: {
  children: ReactNode;
  /** Do not enable on the hall. Voice latency stays first. */
  autoload?: boolean;
  analytics?: AnalyticsSummary | null;
  enterprise?: EnterpriseSnapshot | null;
}) {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(analyticsProp);
  const [enterprise, setEnterprise] = useState<EnterpriseSnapshot | null>(enterpriseProp);
  const previous = useRef<LearningIntelligence | null>(null);
  const listeners = useRef(new Set<LearningListener>());

  const intelligence = useMemo(
    () => adaptInstruments(analytics, enterprise),
    [analytics, enterprise]
  );

  useEffect(() => {
    const nextEvents = eventsFromIntelligence(previous.current, intelligence);
    previous.current = intelligence;
    const emit = (event: LearningEvent) => {
      listeners.current.forEach((listener) => listener(event));
    };
    nextEvents.forEach(emit);
  }, [intelligence]);

  const refresh = useCallback(async () => {
    const [nextAnalytics, nextEnterprise] = await Promise.all([
      fetchAnalyticsSummary().catch(() => null),
      fetchEnterpriseSnapshot().catch(() => null),
    ]);
    setAnalytics(nextAnalytics);
    setEnterprise(nextEnterprise);
  }, []);

  useEffect(() => {
    if (!autoload) return;
    void refresh();
  }, [autoload, refresh]);

  const actions = useMemo<LearningActions>(
    () => ({
      subscribe: (listener) => {
        listeners.current.add(listener);
        return () => {
          listeners.current.delete(listener);
        };
      },
      refresh,
    }),
    [refresh]
  );

  return (
    <ActionsContext.Provider value={actions}>
      <SnapshotContext.Provider value={intelligence}>{children}</SnapshotContext.Provider>
    </ActionsContext.Provider>
  );
}
