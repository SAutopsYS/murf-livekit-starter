import type { MasteryLevel, MasteryRecord } from '@/lib/adaptive/types';
import type { Skill } from '@/lib/learning/types';

export function masteryFromSkill(skill: Skill): MasteryRecord {
  const practice = skill.practiceCount;
  const mastery = skill.mastery;
  const confidence = skill.confidence;

  let level: MasteryLevel = 'unknown';
  if (practice === 0 && mastery == null) level = 'unknown';
  else if (skill.trend === 'down') level = 'regression';
  else if (mastery != null && mastery >= 0.85 && (confidence ?? 0) >= 0.7) level = 'mastered';
  else if (mastery != null && mastery >= 0.65) level = 'confident';
  else if (practice >= 3) level = 'practicing';
  else if (practice >= 1) level = 'emerging';
  else level = 'learning';

  if (skill.trend === 'down' && practice > 0) level = 'needs_review';

  return {
    skillId: skill.id,
    level,
    score: mastery,
    evidence: `${practice} practices · trend ${skill.trend}`,
  };
}

export const MASTERY_LABEL: Record<MasteryLevel, string> = {
  unknown: 'Unknown',
  learning: 'Learning',
  emerging: 'Emerging',
  practicing: 'Practicing',
  confident: 'Confident',
  mastered: 'Mastered',
  forgotten: 'Forgotten',
  regression: 'Regression',
  needs_review: 'Needs review',
};
