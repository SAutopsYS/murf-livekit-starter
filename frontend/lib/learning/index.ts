export { buildLearningIntelligence } from '@/lib/learning/engine';
export { adaptInstruments, mergeMemoryUser } from '@/lib/learning/adapters';
export { getLearningVisual } from '@/lib/learning/states';
export { skillCatalog, skillIdForTopic } from '@/lib/learning/skills';
export { eventsFromIntelligence, LEARNING_EVENT_LABEL } from '@/lib/learning/events';
export type {
  LearnerProfile,
  LearningIntelligence,
  LearningPhase,
  LearningInsight,
  LearningRecommendation,
  LearningGoal,
  LearningTimelineEvent,
  LearningMetrics,
  LearningEvent,
  Skill,
  KnowledgeObject,
} from '@/lib/learning/types';
export type { MemoryUserAdapter } from '@/lib/learning/adapters';
