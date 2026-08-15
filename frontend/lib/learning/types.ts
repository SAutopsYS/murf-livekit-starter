export type LearningSource = 'memory' | 'analytics' | 'enterprise' | 'session' | 'projected';

export type LearningPhase =
  | 'new'
  | 'active'
  | 'practicing'
  | 'reviewing'
  | 'paused'
  | 'completed'
  | 'needs_review'
  | 'recommended'
  | 'archived';

export type SkillCategory =
  | 'speaking'
  | 'listening'
  | 'reading'
  | 'writing'
  | 'vocabulary'
  | 'grammar'
  | 'reasoning'
  | 'problem_solving'
  | 'math'
  | 'coding'
  | 'career'
  | 'interview';

export type KnowledgeKind =
  | 'concept'
  | 'topic'
  | 'lesson'
  | 'exercise'
  | 'question'
  | 'answer'
  | 'correction'
  | 'insight'
  | 'recommendation'
  | 'weakness'
  | 'strength'
  | 'mistake'
  | 'achievement'
  | 'revision';

export type InsightKind =
  | 'strength'
  | 'weakness'
  | 'recommendation'
  | 'prediction'
  | 'improvement'
  | 'reminder'
  | 'risk'
  | 'celebration'
  | 'trend';

export type RecommendationKind =
  | 'next_lesson'
  | 'revision'
  | 'practice'
  | 'conversation'
  | 'reading'
  | 'listening'
  | 'speaking'
  | 'vocabulary'
  | 'grammar'
  | 'math'
  | 'coding'
  | 'career'
  | 'interview'
  | 'quiz'
  | 'voice_exercise'
  | 'debate'
  | 'repeat_same_level'
  | 'continue_same_level'
  | 'advance_level';

export type GoalHorizon = 'daily' | 'weekly' | 'monthly' | 'skill' | 'conversation' | 'custom';

export type GoalStatus = 'open' | 'in_progress' | 'completed' | 'paused';

export type TimelineKind =
  | 'lesson_started'
  | 'lesson_completed'
  | 'conversation'
  | 'correction'
  | 'practice'
  | 'assessment'
  | 'recommendation'
  | 'goal_updated'
  | 'skill_improved'
  | 'agent_assisted'
  | 'mistake_fixed'
  | 'revision'
  | 'recommendation_applied';

export type LearningEventName =
  | 'LessonStarted'
  | 'LessonCompleted'
  | 'GoalCreated'
  | 'GoalUpdated'
  | 'RecommendationGenerated'
  | 'InsightCreated'
  | 'SkillImproved'
  | 'ReviewRequested'
  | 'TimelineUpdated'
  | 'ConversationFinished'
  | 'ProfileUpdated';

export type LearningVisualState = {
  phase: LearningPhase;
  label: string;
  meaning: string;
  priority: number;
  colorToken: string;
  iconToken: string;
};

export type Skill = {
  id: string;
  title: string;
  description: string;
  category: SkillCategory;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  mastery: number | null;
  confidence: number | null;
  practiceCount: number;
  lastPracticed: string | null;
  trend: 'up' | 'flat' | 'down' | 'unknown';
  relatedSkillIds: string[];
  dependencyIds: string[];
  source: LearningSource;
};

export type KnowledgeObject = {
  id: string;
  kind: KnowledgeKind;
  title: string;
  summary: string;
  topic?: string;
  relatedSkillIds: string[];
  source: LearningSource;
};

export type LearningInsight = {
  id: string;
  kind: InsightKind;
  title: string;
  body: string;
  priority: number;
  relatedSkillIds: string[];
  source: LearningSource;
};

export type LearningRecommendation = {
  id: string;
  kind: RecommendationKind;
  title: string;
  reason: string;
  priority: number;
  confidence: number | null;
  nextLevel?: string;
  relatedSkillIds: string[];
  source: LearningSource;
};

export type LearningGoal = {
  id: string;
  horizon: GoalHorizon;
  title: string;
  status: GoalStatus;
  progress: number;
  deadline: string | null;
  priority: number;
  recommendation: string | null;
  source: LearningSource;
};

export type LearningTimelineEvent = {
  id: string;
  kind: TimelineKind;
  title: string;
  at: string | null;
  detail?: string;
  source: LearningSource;
};

export type LearningMetrics = {
  learningTimeSeconds: number;
  speakingTimeSeconds: number | null;
  completionRate: number;
  retention: number | null;
  confidence: number | null;
  consistency: number | null;
  responseQuality: number | null;
  latencyMs: number | null;
  participation: number;
  practiceFrequency: number;
  source: LearningSource;
};

export type LearnerProfile = {
  learnerRef: string;
  preferredLanguage: string;
  currentLevel: string;
  learningStyle: string;
  strengths: string[];
  weaknesses: string[];
  interests: string[];
  confidence: string;
  consistency: number | null;
  motivation: string | null;
  attention: string | null;
  speakingSkill: number | null;
  listeningSkill: number | null;
  readingSkill: number | null;
  writingSkill: number | null;
  problemSolving: number | null;
  reasoning: number | null;
  progressScore: number | null;
  grammarLevel: string;
  lastActivity: string | null;
  streak: number;
  source: LearningSource;
};

export type LearningEvent = {
  name: LearningEventName;
  at: string;
  detail?: Record<string, string | number | boolean>;
};

export type LearningIntelligence = {
  phase: LearningPhase;
  visual: LearningVisualState;
  profile: LearnerProfile;
  skills: Skill[];
  knowledge: KnowledgeObject[];
  insights: LearningInsight[];
  recommendations: LearningRecommendation[];
  goals: LearningGoal[];
  timeline: LearningTimelineEvent[];
  metrics: LearningMetrics;
};
