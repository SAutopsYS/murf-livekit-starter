import type { VoiceMotionVerb, VoicePhase, VoiceVisualState } from '@/lib/voice/types';

const VISUAL: Record<VoicePhase, Omit<VoiceVisualState, 'phase'>> = {
  idle: {
    colorToken: 'var(--salora-pulse)',
    motionToken: 'rest',
    priority: 10,
    label: 'Ready',
    meaning: 'Tutor is present and waiting for a try.',
    hint: null,
  },
  connecting: {
    colorToken: 'var(--salora-warning)',
    motionToken: 'hold',
    priority: 80,
    label: 'Connecting',
    meaning: 'Joining the hall. Last good state is not lost.',
    hint: 'Connecting to your AI Tutor…',
  },
  connected: {
    colorToken: 'var(--salora-pulse)',
    motionToken: 'rest',
    priority: 20,
    label: 'Connected',
    meaning: 'The line is open.',
    hint: null,
  },
  listening: {
    colorToken: 'var(--salora-pulse)',
    motionToken: 'ripple',
    priority: 40,
    label: 'Listening',
    meaning: 'Energy follows the microphone.',
    hint: null,
  },
  thinking: {
    colorToken: 'var(--salora-warning)',
    motionToken: 'breathe',
    priority: 45,
    label: 'Thinking',
    meaning: 'Hold. Do not theater a brain.',
    hint: 'Preparing your lesson…',
  },
  speaking: {
    colorToken: 'var(--salora-info)',
    motionToken: 'glow',
    priority: 50,
    label: 'Speaking',
    meaning: 'Energy follows the tutor voice.',
    hint: null,
  },
  paused: {
    colorToken: 'var(--salora-border-strong)',
    motionToken: 'compress',
    priority: 55,
    label: 'Paused',
    meaning: 'The attempt is held. Resume is not restart.',
    hint: null,
  },
  routing: {
    colorToken: 'var(--salora-pulse)',
    motionToken: 'split',
    priority: 70,
    label: 'Routing',
    meaning: 'A named guest is taking the line. Same voice family.',
    hint: 'Handing off…',
  },
  returning: {
    colorToken: 'var(--salora-pulse)',
    motionToken: 'merge',
    priority: 65,
    label: 'Returning',
    meaning: 'Host is back. Same room. No origin burst.',
    hint: null,
  },
  muted: {
    colorToken: 'var(--salora-warning)',
    motionToken: 'still',
    priority: 60,
    label: 'Muted',
    meaning: 'Microphone is off. The hall is still here.',
    hint: 'Microphone muted',
  },
  disconnected: {
    colorToken: 'var(--muted-foreground)',
    motionToken: 'still',
    priority: 5,
    label: 'Ended',
    meaning: 'The session closed. Practice again is a new try.',
    hint: null,
  },
  offline: {
    colorToken: 'var(--salora-error)',
    motionToken: 'still',
    priority: 90,
    label: 'Offline',
    meaning: 'The network is gone. Last good state remains.',
    hint: 'You are offline',
  },
  error: {
    colorToken: 'var(--salora-error)',
    motionToken: 'still',
    priority: 95,
    label: 'Error',
    meaning: 'Fail-closed. High contrast. No shake.',
    hint: 'Something went wrong',
  },
};

export function getVoiceVisual(phase: VoicePhase): VoiceVisualState {
  return { phase, ...VISUAL[phase] };
}

export function isActiveVoiceMotion(verb: VoiceMotionVerb): boolean {
  return verb !== 'rest' && verb !== 'still' && verb !== 'hold';
}
