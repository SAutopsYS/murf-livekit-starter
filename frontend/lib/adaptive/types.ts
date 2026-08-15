export type AdaptiveAction =
  | 'continue'
  | 'pause'
  | 'repeat'
  | 'revise'
  | 'challenge'
  | 'advance'
  | 'escalate'
  | 'simplify'
  | 'practice'
  | 'assess'
  | 'review'
  | 'recommend_specialist'
  | 'recommend_human';

export type MasteryLevel =
  | 'unknown'
  | 'learning'
  | 'emerging'
  | 'practicing'
  | 'confident'
  | 'mastered'
  | 'forgotten'
  | 'regression'
  | 'needs_review';

export type SpecialistId =
  | 'tutor'
  | 'math'
  | 'coding'
  | 'career'
  | 'interview'
  | 'writing'
  | 'language';

export type AdaptiveDecision = {
  action: AdaptiveAction;
  reason: string;
  confidence: number;
  priority: number;
  explanation: string;
  timestamp: string;
  relatedSkillIds: string[];
};

export type MasteryRecord = {
  skillId: string;
  level: MasteryLevel;
  score: number | null;
  evidence: string;
};

export type RevisionItem = {
  id: string;
  skillId: string;
  kind: 'spaced' | 'weak' | 'missed' | 'queue' | 'recommended';
  priority: number;
  dueAt: string | null;
  reason: string;
};

export type SpecialistAdvice = {
  specialist: SpecialistId;
  live: boolean;
  reason: string;
  confidence: number;
  urgency: 'low' | 'medium' | 'high';
  expectedOutcome: string;
};

export type AdaptivePrediction = {
  completionProbability: number | null;
  masteryForecast: MasteryLevel;
  dropOffRisk: number | null;
  reviewNeed: number | null;
  recommendedPracticeMinutes: number | null;
  expectedImprovement: number | null;
  learningVelocity: number | null;
  explanation: string;
};

export type AdaptiveSignals = {
  confidence: number | null;
  consistency: number | null;
  latencyMs: number | null;
  responseQuality: number | null;
  recentFailures: number;
  recentSuccesses: number;
  attention: string | null;
  velocity: number | null;
};

export type AdaptiveSnapshot = {
  decision: AdaptiveDecision;
  alternatives: AdaptiveDecision[];
  mastery: MasteryRecord[];
  revision: RevisionItem[];
  specialist: SpecialistAdvice;
  prediction: AdaptivePrediction;
  signals: AdaptiveSignals;
};
