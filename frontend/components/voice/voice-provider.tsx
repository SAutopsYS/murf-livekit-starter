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
import { ConnectionState } from 'livekit-client';
import { useAgent, useLocalParticipant, useSessionContext } from '@livekit/components-react';
import { deriveVoiceSnapshot, eventsForTransition } from '@/lib/voice/derive';
import type { AgentTransfer, VoiceEvent, VoiceSnapshot } from '@/lib/voice/types';

type VoiceListener = (event: VoiceEvent) => void;

type VoiceActions = {
  subscribe: (listener: VoiceListener) => () => void;
  reportAgentTransfer: (transfer: AgentTransfer) => void;
  clearAgentTransfer: () => void;
  setPaused: (paused: boolean) => void;
};

const VoiceSnapshotContext = createContext<VoiceSnapshot | null>(null);
const VoiceActionsContext = createContext<VoiceActions | null>(null);

export function useVoice(): VoiceSnapshot {
  const ctx = useContext(VoiceSnapshotContext);
  if (!ctx) throw new Error('useVoice must be used inside VoiceProvider');
  return ctx;
}

export function useVoiceActions(): VoiceActions {
  const ctx = useContext(VoiceActionsContext);
  if (!ctx) throw new Error('useVoiceActions must be used inside VoiceProvider');
  return ctx;
}

export function useVoiceEvent(listener: VoiceListener) {
  const { subscribe } = useVoiceActions();
  useEffect(() => subscribe(listener), [subscribe, listener]);
}

export function VoiceProvider({ children }: { children: ReactNode }) {
  const { connectionState, isConnected } = useSessionContext();
  const { state: agentState } = useAgent();
  const local = useLocalParticipant();
  const [online, setOnline] = useState(() =>
    typeof navigator === 'undefined' ? true : navigator.onLine
  );
  const [transfer, setTransfer] = useState<AgentTransfer | null>(null);
  const [paused, setPaused] = useState(false);
  const listeners = useRef(new Set<VoiceListener>());
  const lastPhase = useRef<VoiceSnapshot['phase'] | null>(null);

  const micEnabled = local.isMicrophoneEnabled ?? true;
  const failed = isConnected && agentState === 'failed';

  const snapshot = useMemo(
    () =>
      deriveVoiceSnapshot({
        connectionState: connectionState ?? ConnectionState.Disconnected,
        isConnected,
        agentState: String(agentState),
        micEnabled,
        online,
        transfer,
        paused,
        failed,
      }),
    [connectionState, isConnected, agentState, micEnabled, online, transfer, paused, failed]
  );

  const emit = useCallback((event: VoiceEvent) => {
    listeners.current.forEach((listener) => listener(event));
  }, []);

  useEffect(() => {
    const from = lastPhase.current;
    const to = snapshot.phase;
    if (from === to) return;
    lastPhase.current = to;
    const at = new Date().toISOString();
    for (const item of eventsForTransition(from, to)) {
      emit({ name: item.name, phase: to, at, detail: item.detail });
    }
  }, [snapshot.phase, emit]);

  useEffect(() => {
    const onOnline = () => setOnline(true);
    const onOffline = () => setOnline(false);
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    return () => {
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, []);

  const actions = useMemo<VoiceActions>(
    () => ({
      subscribe: (listener) => {
        listeners.current.add(listener);
        return () => {
          listeners.current.delete(listener);
        };
      },
      reportAgentTransfer: (next) => setTransfer(next),
      clearAgentTransfer: () => setTransfer(null),
      setPaused,
    }),
    []
  );

  return (
    <VoiceActionsContext.Provider value={actions}>
      <VoiceSnapshotContext.Provider value={snapshot}>{children}</VoiceSnapshotContext.Provider>
    </VoiceActionsContext.Provider>
  );
}
