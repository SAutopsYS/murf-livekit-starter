import type { LearningPhase, LearningVisualState } from '@/lib/learning/types';

const STATES: Record<LearningPhase, Omit<LearningVisualState, 'phase'>> = {
  new: {
    label: 'New',
    meaning: 'No practice recorded yet. The first try starts the profile.',
    priority: 10,
    colorToken: 'var(--salora-info)',
    iconToken: 'spark',
  },
  active: {
    label: 'Active',
    meaning: 'The learner is on the line or recently practiced.',
    priority: 40,
    colorToken: 'var(--salora-pulse)',
    iconToken: 'pulse',
  },
  practicing: {
    label: 'Practicing',
    meaning: 'An attempt is in progress.',
    priority: 50,
    colorToken: 'var(--salora-pulse)',
    iconToken: 'mic',
  },
  reviewing: {
    label: 'Reviewing',
    meaning: 'A concept should be seen again before new work.',
    priority: 45,
    colorToken: 'var(--salora-warning)',
    iconToken: 'repeat',
  },
  paused: {
    label: 'Paused',
    meaning: 'Held. Resume is not restart.',
    priority: 30,
    colorToken: 'var(--salora-border-strong)',
    iconToken: 'pause',
  },
  completed: {
    label: 'Completed',
    meaning: 'The intended exercise finished. Not a trophy.',
    priority: 20,
    colorToken: 'var(--salora-success)',
    iconToken: 'check',
  },
  needs_review: {
    label: 'Needs review',
    meaning: 'Weak or forgotten work. Dignity first.',
    priority: 60,
    colorToken: 'var(--salora-warning)',
    iconToken: 'flag',
  },
  recommended: {
    label: 'Recommended',
    meaning: 'A next try is named. Conversation-only until persisted.',
    priority: 35,
    colorToken: 'var(--salora-info)',
    iconToken: 'arrow',
  },
  archived: {
    label: 'Archived',
    meaning: 'No longer in the active path.',
    priority: 5,
    colorToken: 'var(--muted-foreground)',
    iconToken: 'archive',
  },
};

export function getLearningVisual(phase: LearningPhase): LearningVisualState {
  return { phase, ...STATES[phase] };
}
