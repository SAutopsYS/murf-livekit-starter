import type { LearningEvent, LearningEventName, LearningIntelligence } from '@/lib/learning/types';

export function eventsFromIntelligence(
  previous: LearningIntelligence | null,
  next: LearningIntelligence
): LearningEvent[] {
  const at = new Date().toISOString();
  if (!previous) {
    return [
      { name: 'ProfileUpdated', at },
      { name: 'TimelineUpdated', at, detail: { count: next.timeline.length } },
    ];
  }

  const events: LearningEvent[] = [];
  if (previous.insights.length !== next.insights.length) {
    events.push({ name: 'InsightCreated', at, detail: { count: next.insights.length } });
  }
  if (previous.recommendations.length !== next.recommendations.length) {
    events.push({
      name: 'RecommendationGenerated',
      at,
      detail: { count: next.recommendations.length },
    });
  }
  if (previous.goals.length !== next.goals.length) {
    events.push({ name: 'GoalCreated', at, detail: { count: next.goals.length } });
  }
  if (previous.timeline.length !== next.timeline.length) {
    events.push({ name: 'TimelineUpdated', at, detail: { count: next.timeline.length } });
  }
  if (previous.profile.streak !== next.profile.streak) {
    events.push({ name: 'SkillImproved', at, detail: { streak: next.profile.streak } });
  }
  if (previous.phase !== next.phase && next.phase === 'needs_review') {
    events.push({ name: 'ReviewRequested', at });
  }
  return events;
}

export const LEARNING_EVENT_LABEL: Record<LearningEventName, string> = {
  LessonStarted: 'Lesson started',
  LessonCompleted: 'Lesson completed',
  GoalCreated: 'Goal created',
  GoalUpdated: 'Goal updated',
  RecommendationGenerated: 'Recommendation generated',
  InsightCreated: 'Insight created',
  SkillImproved: 'Skill improved',
  ReviewRequested: 'Review requested',
  TimelineUpdated: 'Timeline updated',
  ConversationFinished: 'Conversation finished',
  ProfileUpdated: 'Profile updated',
};
