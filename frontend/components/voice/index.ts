export {
  VoiceProvider,
  useVoice,
  useVoiceActions,
  useVoiceEvent,
} from '@/components/voice/voice-provider';
export { VoiceCore } from '@/components/voice/voice-core';
export { VoiceOverlay } from '@/components/voice/voice-overlay';
export { VoiceFeedback } from '@/components/voice/voice-feedback';
export { VoiceIndicators } from '@/components/voice/voice-indicators';
export { VoiceLiveRegion } from '@/components/voice/voice-live-region';
export { deriveVoiceSnapshot, eventsForTransition } from '@/lib/voice/derive';
export { getVoiceVisual } from '@/lib/voice/visual-language';
export type {
  VoicePhase,
  SessionLifecycle,
  VoiceSnapshot,
  VoiceEvent,
  VoiceEventName,
  AgentTransfer,
  VoiceVisualState,
} from '@/lib/voice/types';
