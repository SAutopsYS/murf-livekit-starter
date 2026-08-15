import type { AdaptiveDecision, SpecialistAdvice, SpecialistId } from '@/lib/adaptive/types';
import type { LearningIntelligence } from '@/lib/learning/types';

const LIVE: Record<SpecialistId, boolean> = {
  tutor: true,
  math: true,
  coding: false,
  career: false,
  interview: false,
  writing: false,
  language: false,
};

export function adviseSpecialist(
  intelligence: LearningIntelligence,
  decision: AdaptiveDecision
): SpecialistAdvice {
  const text = [
    ...intelligence.profile.weaknesses,
    ...intelligence.profile.interests,
    ...intelligence.profile.strengths,
  ]
    .join(' ')
    .toLowerCase();

  let specialist: SpecialistId = 'tutor';
  if (/\b(math|algebra|fraction|multiply|geometry|percent)\b/.test(text)) specialist = 'math';
  else if (/\b(code|coding|program)\b/.test(text)) specialist = 'coding';
  else if (/\b(career|job|resume)\b/.test(text)) specialist = 'career';
  else if (/\b(interview)\b/.test(text)) specialist = 'interview';
  else if (/\b(writ|essay|grammar)\b/.test(text)) specialist = 'writing';

  if (decision.action === 'recommend_human') {
    return {
      specialist: 'tutor',
      live: true,
      reason: 'Human recommended. Stay with the host until a person is present.',
      confidence: 0.9,
      urgency: 'high',
      expectedOutcome: 'Fail toward the tutor. Do not invent a second mouth.',
    };
  }

  const live = LIVE[specialist];
  return {
    specialist,
    live,
    reason: live
      ? specialist === 'math'
        ? 'Math request signal. Backend router remains the authority.'
        : 'Stay with the Main Tutor.'
      : `${specialist} is registered and disabled. Stay with the tutor.`,
    confidence: specialist === 'math' ? 0.55 : 0.8,
    urgency: specialist === 'math' ? 'medium' : 'low',
    expectedOutcome: live
      ? 'One voice family. Handback to host after the try.'
      : 'No guest yet. Host keeps the line.',
  };
}
