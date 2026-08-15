import type { MasteryRecord, RevisionItem } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

export function buildRevisionQueue(
  intelligence: LearningIntelligence,
  mastery: MasteryRecord[]
): RevisionItem[] {
  const items: RevisionItem[] = [];

  for (const weak of intelligence.profile.weaknesses.slice(0, 4)) {
    items.push({
      id: `rev:weak:${weak}`,
      skillId: weak.toLowerCase().replaceAll(' ', '_'),
      kind: 'weak',
      priority: 80,
      dueAt: null,
      reason: `Weak concept · ${weak}`,
    });
  }

  for (const record of mastery) {
    if (
      record.level === 'needs_review' ||
      record.level === 'regression' ||
      record.level === 'forgotten'
    ) {
      items.push({
        id: `rev:mastery:${record.skillId}`,
        skillId: record.skillId,
        kind: 'recommended',
        priority: 70,
        dueAt: null,
        reason: `Mastery ${record.level}`,
      });
    }
  }

  intelligence.recommendations
    .filter((item) => item.kind === 'revision')
    .forEach((item) => {
      items.push({
        id: `rev:rec:${item.id}`,
        skillId: item.relatedSkillIds[0] ?? 'speaking',
        kind: 'spaced',
        priority: item.priority,
        dueAt: null,
        reason: item.reason,
      });
    });

  return items.sort((a, b) => b.priority - a.priority).slice(0, 12);
}
