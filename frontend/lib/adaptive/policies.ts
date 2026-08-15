import type { AdaptiveAction, AdaptiveDecision, AdaptiveSignals } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

export function collectSignals(intelligence: LearningIntelligence): AdaptiveSignals {
  const successes = intelligence.timeline.filter((item) => item.kind === 'lesson_completed').length;
  return {
    confidence: intelligence.metrics.confidence,
    consistency: intelligence.metrics.consistency,
    latencyMs: intelligence.metrics.latencyMs,
    responseQuality: intelligence.metrics.responseQuality,
    recentFailures: intelligence.metrics.participation - successes,
    recentSuccesses: successes,
    attention: intelligence.profile.attention,
    velocity:
      intelligence.metrics.practiceFrequency > 0
        ? intelligence.metrics.completionRate / Math.max(intelligence.metrics.practiceFrequency, 1)
        : null,
  };
}

function decision(
  action: AdaptiveAction,
  reason: string,
  explanation: string,
  confidence: number,
  priority: number,
  relatedSkillIds: string[]
): AdaptiveDecision {
  return {
    action,
    reason,
    explanation,
    confidence,
    priority,
    timestamp: new Date().toISOString(),
    relatedSkillIds,
  };
}

export function decide(
  intelligence: LearningIntelligence,
  signals: AdaptiveSignals
): { primary: AdaptiveDecision; alternatives: AdaptiveDecision[] } {
  const weak = intelligence.profile.weaknesses[0];
  const weakSkill = weak ? [weak.toLowerCase()] : ['speaking'];
  const candidates: AdaptiveDecision[] = [];

  if (intelligence.phase === 'new' || intelligence.metrics.participation === 0) {
    candidates.push(
      decision(
        'practice',
        'No completed tries yet',
        'Start in the hall. The first attempt creates the profile.',
        0.86,
        90,
        ['speaking']
      )
    );
  }

  if (intelligence.phase === 'needs_review' || weak) {
    candidates.push(
      decision(
        'revise',
        'Weak signal present',
        `Review ${weak || 'the last weak topic'} before adding new work.`,
        0.62,
        80,
        weakSkill
      )
    );
  }

  if (signals.recentFailures >= 3) {
    candidates.push(
      decision('simplify', 'Recent failures', 'Slow the climb. Same room. Smaller try.', 0.55, 75, [
        'speaking',
      ])
    );
  }

  if (intelligence.metrics.completionRate >= 0.7 && intelligence.profile.streak >= 3) {
    candidates.push(
      decision(
        'challenge',
        'Stable completion and streak',
        'A harder try is earned. Do not shame the last miss.',
        0.48,
        55,
        ['speaking']
      )
    );
    candidates.push(
      decision(
        'advance',
        'Ready to move a level',
        'Matches conversation-only advance_level. Does not write memory.',
        0.4,
        50,
        ['speaking']
      )
    );
  }

  if ((signals.latencyMs ?? 0) > 4000) {
    candidates.push(
      decision('pause', 'High response latency', 'Hold. Recovery is not a new hello.', 0.5, 60, [])
    );
  }

  if (intelligence.insights.some((item) => item.kind === 'risk')) {
    candidates.push(
      decision(
        'escalate',
        'Risk insight',
        'Recommend a human when dignity or safety is in question.',
        0.35,
        95,
        []
      )
    );
  }

  candidates.push(
    decision(
      'continue',
      'Default stay-on-tutor',
      'Keep the host. Fail toward the tutor.',
      0.7,
      40,
      ['speaking']
    )
  );

  const ranked = [...candidates].sort(
    (a, b) => b.priority - a.priority || b.confidence - a.confidence
  );
  return { primary: ranked[0], alternatives: ranked.slice(1, 4) };
}
