import { ConnectionState } from 'livekit-client';
import type { AgentTransfer, SessionLifecycle, VoicePhase, VoiceSnapshot } from '@/lib/voice/types';
import { getVoiceVisual } from '@/lib/voice/visual-language';

export type VoiceDeriveInput = {
  connectionState: ConnectionState;
  isConnected: boolean;
  agentState: string;
  micEnabled: boolean;
  online: boolean;
  transfer: AgentTransfer | null;
  paused: boolean;
  failed: boolean;
};

function pickPhase(input: VoiceDeriveInput): VoicePhase {
  if (!input.online) return 'offline';
  if (input.failed || input.agentState === 'failed') return 'error';
  if (input.connectionState === ConnectionState.Connecting) return 'connecting';
  if (!input.isConnected) return 'disconnected';
  if (input.paused) return 'paused';
  if (input.transfer) return 'routing';
  if (!input.micEnabled) return 'muted';

  switch (input.agentState) {
    case 'listening':
      return 'listening';
    case 'thinking':
      return 'thinking';
    case 'speaking':
      return 'speaking';
    case 'connecting':
    case 'pre-connect-buffering':
    case 'initializing':
      return 'connecting';
    case 'disconnected':
      return 'disconnected';
    case 'idle':
    default:
      return 'idle';
  }
}

function pickLifecycle(phase: VoicePhase, input: VoiceDeriveInput): SessionLifecycle {
  if (phase === 'offline') return 'offline';
  if (phase === 'connecting') return 'connecting';
  if (phase === 'disconnected' || phase === 'error') return 'disconnected';
  if (phase === 'listening') return 'listening';
  if (phase === 'thinking') return 'thinking';
  if (phase === 'speaking') return 'speaking';
  if (input.isConnected && phase === 'idle') return 'ready';
  if (input.isConnected) return 'idle';
  return 'disconnected';
}

export function deriveVoiceSnapshot(input: VoiceDeriveInput): VoiceSnapshot {
  const phase = pickPhase(input);
  return {
    phase,
    lifecycle: pickLifecycle(phase, input),
    visual: getVoiceVisual(phase),
    muted: !input.micEnabled && input.isConnected,
    online: input.online,
    agentState: input.agentState,
    transfer: input.transfer,
  };
}

export function eventsForTransition(
  from: VoicePhase | null,
  to: VoicePhase
): Array<{
  name: import('@/lib/voice/types').VoiceEventName;
  detail?: Record<string, string | number | boolean>;
}> {
  if (from === to) return [];
  const events: Array<{
    name: import('@/lib/voice/types').VoiceEventName;
    detail?: Record<string, string | number | boolean>;
  }> = [{ name: 'PhaseChanged', detail: { from: from ?? 'none', to } }];

  if (to === 'connecting' && from !== 'connecting') events.push({ name: 'ReconnectStarted' });
  if (from === 'connecting' && to !== 'connecting' && to !== 'disconnected' && to !== 'error') {
    events.push({ name: 'ReconnectFinished' });
    events.push({ name: 'SessionStarted' });
  }
  if (to === 'listening') events.push({ name: 'ListeningStarted' });
  if (from === 'listening' && to !== 'listening') events.push({ name: 'ListeningStopped' });
  if (to === 'thinking') events.push({ name: 'ThinkingStarted' });
  if (from === 'thinking' && to !== 'thinking') events.push({ name: 'ThinkingFinished' });
  if (to === 'speaking') events.push({ name: 'SpeakingStarted' });
  if (from === 'speaking' && to !== 'speaking') events.push({ name: 'SpeakingFinished' });
  if (to === 'muted' || from === 'muted') events.push({ name: 'MuteChanged' });
  if (to === 'offline' || from === 'offline') events.push({ name: 'NetworkChanged' });
  if (to === 'disconnected' || to === 'error') events.push({ name: 'SessionEnded' });
  if (to === 'routing') events.push({ name: 'AgentTransferred' });

  return events;
}
