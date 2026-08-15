import type { AnalyticsSummary } from '@/lib/analytics';
import type { EnterpriseSnapshot } from '@/lib/enterprise';
import { skillCatalog, skillIdForTopic } from '@/lib/learning/skills';
import { getLearningVisual } from '@/lib/learning/states';
import type {
  KnowledgeObject,
  LearnerProfile,
  LearningGoal,
  LearningInsight,
  LearningIntelligence,
  LearningMetrics,
  LearningPhase,
  LearningRecommendation,
  LearningTimelineEvent,
  Skill,
} from '@/lib/learning/types';

function asString(value: unknown, fallback = ''): string {
  return typeof value === 'string' ? value : fallback;
}

function asNumber(value: unknown, fallback = 0): number {
  return typeof value === 'number' && Number.isFinite(value) ? value : fallback;
}

function asStringList(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.map((item) => String(item)).filter(Boolean);
}

function pickPhase(metrics: LearningMetrics, insights: LearningInsight[]): LearningPhase {
  if (metrics.participation === 0) return 'new';
  if (insights.some((item) => item.kind === 'weakness' || item.kind === 'risk')) {
    return 'needs_review';
  }
  if (metrics.completionRate >= 1) return 'completed';
  if (metrics.practiceFrequency > 0) return 'active';
  return 'recommended';
}

function buildProfile(
  enterprise: EnterpriseSnapshot | null,
  metrics: LearningMetrics
): LearnerProfile {
  const parent = enterprise?.parent ?? {};
  const nodes = enterprise?.memory_graph?.nodes ?? [];
  const nodeMap = Object.fromEntries(
    nodes.map((node) => [asString(node.label || node.id), asString(node.value)])
  );

  const splitTopics = (raw: string) =>
    raw
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
  const weak = [...asStringList(parent.weak_areas), ...splitTopics(asString(nodeMap.weak_topics))];
  const strong = [
    ...asStringList(parent.strong_areas),
    ...splitTopics(asString(nodeMap.strong_topics)),
  ];

  return {
    learnerRef: 'aggregate',
    preferredLanguage: asString(nodeMap.preferred_language),
    currentLevel: asString(parent.difficulty || nodeMap.grade || 'beginner'),
    learningStyle: 'voice',
    strengths: strong.filter(Boolean),
    weaknesses: weak.filter(Boolean),
    interests: (Array.isArray(parent.upcoming_goals)
      ? asStringList(parent.upcoming_goals)
      : parent.upcoming_goals && typeof parent.upcoming_goals === 'object'
        ? Object.keys(parent.upcoming_goals)
        : []
    ).slice(0, 6),
    confidence: asString(parent.difficulty) || 'unset',
    consistency: metrics.consistency,
    motivation: null,
    attention: null,
    speakingSkill: metrics.speakingTimeSeconds,
    listeningSkill: null,
    readingSkill: null,
    writingSkill: null,
    problemSolving:
      typeof enterprise?.difficulty?.accuracy === 'number' ? enterprise.difficulty.accuracy : null,
    reasoning: null,
    progressScore: metrics.completionRate,
    grammarLevel: '',
    lastActivity: null,
    streak: asNumber(parent.learning_streak ?? enterprise?.journey?.streak),
    source: enterprise ? 'enterprise' : 'projected',
  };
}

function buildSkills(enterprise: EnterpriseSnapshot | null): Skill[] {
  const catalog = skillCatalog();
  const cells = enterprise?.heatmap?.cells ?? [];
  const byId = new Map(catalog.map((skill) => [skill.id, { ...skill }]));

  for (const cell of cells) {
    const topic = asString(cell.topic);
    const id = skillIdForTopic(topic);
    if (!id) continue;
    const current = byId.get(id) ?? byId.get('math');
    if (!current) continue;
    current.practiceCount = asNumber(cell.practice_count);
    current.mastery = typeof cell.completion === 'number' ? cell.completion : null;
    current.confidence = typeof cell.accuracy === 'number' ? cell.accuracy : null;
    current.trend = current.practiceCount > 0 ? 'up' : 'unknown';
    current.source = 'enterprise';
    byId.set(current.id, current);
  }

  return [...byId.values()];
}

function buildKnowledge(profile: LearnerProfile, skills: Skill[]): KnowledgeObject[] {
  const objects: KnowledgeObject[] = [];
  for (const topic of profile.interests) {
    objects.push({
      id: `topic:${topic}`,
      kind: 'topic',
      title: topic,
      summary: 'Projected from enterprise topic counts. Not a lesson store.',
      topic,
      relatedSkillIds: [skillIdForTopic(topic) ?? 'speaking'],
      source: 'projected',
    });
  }
  for (const skill of skills.filter((item) => item.practiceCount > 0).slice(0, 8)) {
    objects.push({
      id: `concept:${skill.id}`,
      kind: 'concept',
      title: skill.title,
      summary: skill.description,
      relatedSkillIds: [skill.id],
      source: skill.source,
    });
  }
  return objects;
}

function buildInsights(
  analytics: AnalyticsSummary | null,
  profile: LearnerProfile,
  metrics: LearningMetrics
): LearningInsight[] {
  const insights: LearningInsight[] = [];
  if (profile.strengths[0]) {
    insights.push({
      id: 'insight:strength',
      kind: 'strength',
      title: 'Strongest signal',
      body: profile.strengths[0],
      priority: 40,
      relatedSkillIds: [skillIdForTopic(profile.strengths[0]) ?? 'speaking'],
      source: 'projected',
    });
  }
  if (profile.weaknesses[0]) {
    insights.push({
      id: 'insight:weakness',
      kind: 'weakness',
      title: 'Needs review',
      body: profile.weaknesses[0],
      priority: 70,
      relatedSkillIds: [skillIdForTopic(profile.weaknesses[0]) ?? 'grammar'],
      source: 'projected',
    });
  }
  if (analytics?.insights?.summary_sentence) {
    insights.push({
      id: 'insight:ops',
      kind: 'trend',
      title: 'Practice line',
      body: analytics.insights.summary_sentence,
      priority: 30,
      relatedSkillIds: [],
      source: 'analytics',
    });
  }
  if (metrics.participation === 0) {
    insights.push({
      id: 'insight:new',
      kind: 'reminder',
      title: 'No calls yet',
      body: 'The hall is empty. The first try creates the profile.',
      priority: 20,
      relatedSkillIds: ['speaking'],
      source: 'projected',
    });
  }
  if (profile.streak > 0) {
    insights.push({
      id: 'insight:consistency',
      kind: 'improvement',
      title: 'Consistency',
      body: `Streak ${profile.streak}. Not a trophy. A habit.`,
      priority: 25,
      relatedSkillIds: ['speaking'],
      source: 'enterprise',
    });
  }
  return insights;
}

function buildRecommendations(
  profile: LearnerProfile,
  insights: LearningInsight[]
): LearningRecommendation[] {
  const recs: LearningRecommendation[] = [];
  if (profile.weaknesses[0]) {
    recs.push({
      id: 'rec:revision',
      kind: 'revision',
      title: `Revise ${profile.weaknesses[0]}`,
      reason: 'Weak area projected from enterprise heatmap / parent fields.',
      priority: 80,
      confidence: 0.4,
      relatedSkillIds: [skillIdForTopic(profile.weaknesses[0]) ?? 'grammar'],
      source: 'projected',
    });
  }
  recs.push({
    id: 'rec:conversation',
    kind: 'conversation',
    title: 'Return to the hall',
    reason: 'Voice is the live client. Scores stay conversation-scoped.',
    priority: 50,
    confidence: 0.9,
    relatedSkillIds: ['speaking'],
    source: 'projected',
  });
  if (insights.some((item) => item.kind === 'reminder')) {
    recs.push({
      id: 'rec:practice',
      kind: 'practice',
      title: 'Start a speaking try',
      reason: 'No completed calls in the current window.',
      priority: 60,
      confidence: 0.7,
      nextLevel: profile.currentLevel || 'beginner',
      relatedSkillIds: ['speaking'],
      source: 'projected',
    });
  }
  return recs;
}

function buildGoals(profile: LearnerProfile): LearningGoal[] {
  if (profile.interests.length === 0) return [];
  return profile.interests.slice(0, 3).map((topic, index) => ({
    id: `goal:${topic}`,
    horizon: 'weekly' as const,
    title: `Practice ${topic}`,
    status: 'open' as const,
    progress: 0,
    deadline: null,
    priority: 40 - index,
    recommendation: 'Conversation-only until a real goal store exists.',
    source: 'projected' as const,
  }));
}

function buildTimeline(
  analytics: AnalyticsSummary | null,
  enterprise: EnterpriseSnapshot | null
): LearningTimelineEvent[] {
  const events: LearningTimelineEvent[] = [];
  for (const call of analytics?.recent_calls ?? []) {
    events.push({
      id: `call:${call.call_id}`,
      kind: call.outcome === 'success' ? 'lesson_completed' : 'conversation',
      title: call.outcome === 'success' ? 'Practice completed' : 'Conversation',
      at: call.started_at,
      detail: call.channel,
      source: 'analytics',
    });
  }
  const steps = enterprise?.journey?.steps ?? [];
  steps.forEach((step, index) => {
    events.push({
      id: `journey:${index}`,
      kind: asString(step.status) === 'completed' ? 'lesson_completed' : 'practice',
      title: asString(step.topic, 'Practice'),
      at: asString(step.day) || null,
      source: 'enterprise',
    });
  });
  return events.slice(0, 24);
}

function buildMetrics(
  analytics: AnalyticsSummary | null,
  enterprise: EnterpriseSnapshot | null
): LearningMetrics {
  const voice = enterprise?.voice ?? {};
  const parent = enterprise?.parent ?? {};
  const total = analytics?.total_calls ?? 0;
  return {
    learningTimeSeconds:
      asNumber(analytics?.performance.average_call_duration_seconds) * Math.max(total, 1),
    speakingTimeSeconds:
      typeof voice.speaking_duration_seconds === 'number' ? voice.speaking_duration_seconds : null,
    completionRate:
      asNumber(parent.completion_percent) / 100 || asNumber(analytics?.success_rate) / 100,
    retention: null,
    confidence: null,
    consistency: asNumber(parent.learning_streak || enterprise?.journey?.streak) || null,
    responseQuality: null,
    latencyMs:
      typeof voice.average_response_latency_ms === 'number'
        ? voice.average_response_latency_ms
        : (analytics?.performance.average_first_response_ms ?? null),
    participation: total,
    practiceFrequency: asNumber(parent.weekly_practice),
    source: analytics ? 'analytics' : 'projected',
  };
}

export function buildLearningIntelligence(
  analytics: AnalyticsSummary | null,
  enterprise: EnterpriseSnapshot | null
): LearningIntelligence {
  const metrics = buildMetrics(analytics, enterprise);
  const profile = buildProfile(enterprise, metrics);
  const skills = buildSkills(enterprise);
  const knowledge = buildKnowledge(profile, skills);
  const insights = buildInsights(analytics, profile, metrics);
  const recommendations = buildRecommendations(profile, insights);
  const goals = buildGoals(profile);
  const timeline = buildTimeline(analytics, enterprise);
  const phase = pickPhase(metrics, insights);

  return {
    phase,
    visual: getLearningVisual(phase),
    profile,
    skills,
    knowledge,
    insights,
    recommendations,
    goals,
    timeline,
    metrics,
  };
}
