export type VoicePhase =
  | 'idle'
  | 'connecting'
  | 'connected'
  | 'listening'
  | 'thinking'
  | 'speaking'
  | 'paused'
  | 'routing'
  | 'returning'
  | 'muted'
  | 'disconnected'
  | 'offline'
  | 'error';

export type SessionLifecycle =
  | 'disconnected'
  | 'connecting'
  | 'ready'
  | 'listening'
  | 'thinking'
  | 'speaking'
  | 'idle'
  | 'disconnecting'
  | 'offline';

export type VoiceMotionVerb =
  | 'rest'
  | 'hold'
  | 'breathe'
  | 'pulse'
  | 'glow'
  | 'expand'
  | 'compress'
  | 'ripple'
  | 'merge'
  | 'split'
  | 'still';

export type VoiceVisualState = {
  phase: VoicePhase;
  colorToken: string;
  motionToken: VoiceMotionVerb;
  priority: number;
  label: string;
  meaning: string;
  hint: string | null;
};

export type AgentTransfer = {
  source: string;
  destination: string;
  reason: string;
  confidence: number;
  durationMs: number;
  timestamp: string;
};

export type VoiceEventName =
  | 'SessionStarted'
  | 'SessionEnded'
  | 'ListeningStarted'
  | 'ListeningStopped'
  | 'ThinkingStarted'
  | 'ThinkingFinished'
  | 'SpeakingStarted'
  | 'SpeakingFinished'
  | 'MuteChanged'
  | 'AgentTransferred'
  | 'ReconnectStarted'
  | 'ReconnectFinished'
  | 'NetworkChanged'
  | 'PhaseChanged';

export type VoiceEvent = {
  name: VoiceEventName;
  phase: VoicePhase;
  at: string;
  detail?: Record<string, string | number | boolean>;
};

export type VoiceSnapshot = {
  phase: VoicePhase;
  lifecycle: SessionLifecycle;
  visual: VoiceVisualState;
  muted: boolean;
  online: boolean;
  agentState: string;
  transfer: AgentTransfer | null;
};
