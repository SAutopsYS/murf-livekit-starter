import { buildLearningIntelligence } from '@/lib/learning/engine';
import type { LearningIntelligence } from '@/lib/learning/types';
import type { Role } from '@/lib/platform/rbac';

export type ExperienceKind = 'student' | 'teacher' | 'parent' | 'classroom' | 'learning';

export type ExperienceSnapshot = {
  kind: ExperienceKind;
  role: Role;
  intelligence: LearningIntelligence;
  source: 'learning-engine';
};

export const EXPERIENCE_POLICIES = {
  scoresPersist: false,
  source: 'learning-engine',
  lazyDashboards: true,
  cachedDashboards: 'process-local',
  streamingAnalytics: 'architected',
} as const;

export function buildExperience(role: Role): ExperienceSnapshot {
  const kind: ExperienceKind =
    role === 'teacher' ? 'teacher' : role === 'parent' ? 'parent' : 'student';
  return {
    kind,
    role,
    intelligence: buildLearningIntelligence(null, null),
    source: 'learning-engine',
  };
}

export const ExperienceEngine = { build: buildExperience };
export const StudentExperience = { build: () => buildExperience('student') };
export const TeacherExperience = { build: () => buildExperience('teacher') };
export const ParentExperience = { build: () => buildExperience('parent') };
