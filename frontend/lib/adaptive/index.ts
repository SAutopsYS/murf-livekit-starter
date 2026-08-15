export { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
export { masteryFromSkill, MASTERY_LABEL } from '@/lib/adaptive/mastery';
export { collectSignals, decide } from '@/lib/adaptive/policies';
export { buildRevisionQueue } from '@/lib/adaptive/revision';
export { buildPredictions } from '@/lib/adaptive/prediction';
export { adviseSpecialist } from '@/lib/adaptive/routing';
export type {
  AdaptiveAction,
  AdaptiveDecision,
  AdaptiveSnapshot,
  AdaptivePrediction,
  AdaptiveSignals,
  MasteryLevel,
  MasteryRecord,
  RevisionItem,
  SpecialistAdvice,
  SpecialistId,
} from '@/lib/adaptive/types';
