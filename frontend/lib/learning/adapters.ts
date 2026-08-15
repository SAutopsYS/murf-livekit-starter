import type { AnalyticsSummary } from '@/lib/analytics';
import type { EnterpriseSnapshot } from '@/lib/enterprise';
import { buildLearningIntelligence } from '@/lib/learning/engine';
import type { LearningIntelligence } from '@/lib/learning/types';

/** Project intelligence from live instrument APIs. Does not read memory.db. */
export function adaptInstruments(
  analytics: AnalyticsSummary | null,
  enterprise: EnterpriseSnapshot | null
): LearningIntelligence {
  return buildLearningIntelligence(analytics, enterprise);
}

/** Backend User fields we may map later. Do not invent a second profile table. */
export type MemoryUserAdapter = {
  user_id: string;
  language_preference: string;
  learning_level: string;
  grammar_level: string;
  speaking_confidence: string;
  common_mistakes: string[];
  last_topics: string[];
  last_interaction: string | null;
  consent: boolean;
};

export function mergeMemoryUser(
  intelligence: LearningIntelligence,
  user: MemoryUserAdapter | null
): LearningIntelligence {
  if (!user || !user.consent) return intelligence;
  return {
    ...intelligence,
    profile: {
      ...intelligence.profile,
      learnerRef: 'consented',
      preferredLanguage: user.language_preference || intelligence.profile.preferredLanguage,
      currentLevel: user.learning_level || intelligence.profile.currentLevel,
      grammarLevel: user.grammar_level,
      confidence: user.speaking_confidence || intelligence.profile.confidence,
      interests: user.last_topics.length ? user.last_topics : intelligence.profile.interests,
      lastActivity: user.last_interaction,
      source: 'memory',
    },
  };
}
