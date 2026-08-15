import { masteryFromSkill } from '@/lib/adaptive/mastery';
import { collectSignals, decide } from '@/lib/adaptive/policies';
import { buildPredictions } from '@/lib/adaptive/prediction';
import { buildRevisionQueue } from '@/lib/adaptive/revision';
import { adviseSpecialist } from '@/lib/adaptive/routing';
import type { AdaptiveSnapshot } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

export function buildAdaptiveSnapshot(intelligence: LearningIntelligence): AdaptiveSnapshot {
  const signals = collectSignals(intelligence);
  const { primary, alternatives } = decide(intelligence, signals);
  const mastery = intelligence.skills.map(masteryFromSkill);
  return {
    decision: primary,
    alternatives,
    mastery,
    revision: buildRevisionQueue(intelligence, mastery),
    specialist: adviseSpecialist(intelligence, primary),
    prediction: buildPredictions(intelligence, signals, mastery),
    signals,
  };
}
