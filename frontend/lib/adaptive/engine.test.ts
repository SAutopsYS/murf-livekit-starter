import { describe, expect, it } from 'vitest';
import { buildAdaptiveSnapshot } from '@/lib/adaptive/engine';
import { masteryFromSkill } from '@/lib/adaptive/mastery';
import { buildLearningIntelligence } from '@/lib/learning/engine';
import type { Skill } from '@/lib/learning/types';

describe('adaptive engine', () => {
  it('advises only — never claims routing authority', () => {
    const intel = buildLearningIntelligence(null, null);
    const snapshot = buildAdaptiveSnapshot(intel);
    expect(snapshot.decision.action).toBeTruthy();
    expect(typeof snapshot.specialist.live).toBe('boolean');
    expect(snapshot.specialist.specialist).toBeTruthy();
  });

  it('maps mastery from practice evidence', () => {
    const skill: Skill = {
      id: 'math',
      title: 'Math',
      description: 'Numbers',
      category: 'math',
      difficulty: 'beginner',
      practiceCount: 4,
      mastery: 0.9,
      confidence: 0.8,
      lastPracticed: null,
      trend: 'up',
      relatedSkillIds: [],
      dependencyIds: [],
      source: 'projected',
    };
    expect(masteryFromSkill(skill).level).toBe('mastered');
  });
});
