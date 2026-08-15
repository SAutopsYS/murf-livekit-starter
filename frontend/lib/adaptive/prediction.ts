import type { AdaptivePrediction, AdaptiveSignals, MasteryRecord } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

export function buildPredictions(
  intelligence: LearningIntelligence,
  signals: AdaptiveSignals,
  mastery: MasteryRecord[]
): AdaptivePrediction {
  const completion = intelligence.metrics.participation
    ? Math.min(0.95, Math.max(0.05, intelligence.metrics.completionRate))
    : null;
  const reviewed = mastery.filter(
    (item) => item.level === 'needs_review' || item.level === 'regression'
  ).length;
  const dropOff =
    intelligence.metrics.participation === 0
      ? 0.4
      : Math.min(0.9, reviewed * 0.12 + (signals.recentFailures > 3 ? 0.2 : 0));

  return {
    completionProbability: completion,
    masteryForecast:
      reviewed > 0
        ? 'needs_review'
        : intelligence.metrics.completionRate >= 0.7
          ? 'confident'
          : 'emerging',
    dropOffRisk: dropOff,
    reviewNeed:
      reviewed > 0
        ? Math.min(1, reviewed / 8)
        : intelligence.profile.weaknesses.length
          ? 0.45
          : 0.1,
    recommendedPracticeMinutes: intelligence.phase === 'new' ? 8 : 12,
    expectedImprovement: completion == null ? null : Math.max(0.02, 0.15 - dropOff * 0.1),
    learningVelocity: signals.velocity,
    explanation:
      'Projected from instrument aggregates. Not a promise. Thin data stays low-confidence.',
  };
}
