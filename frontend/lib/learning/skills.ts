import type { Skill, SkillCategory } from '@/lib/learning/types';

type SkillSeed = Pick<
  Skill,
  'id' | 'title' | 'description' | 'category' | 'relatedSkillIds' | 'dependencyIds'
>;

const SEEDS: SkillSeed[] = [
  {
    id: 'speaking',
    title: 'Speaking',
    description: 'Produce language on the line.',
    category: 'speaking',
    relatedSkillIds: ['listening', 'vocabulary', 'grammar'],
    dependencyIds: [],
  },
  {
    id: 'listening',
    title: 'Listening',
    description: 'Hear and hold the tutor turn.',
    category: 'listening',
    relatedSkillIds: ['speaking'],
    dependencyIds: [],
  },
  {
    id: 'reading',
    title: 'Reading',
    description: 'Decode written language.',
    category: 'reading',
    relatedSkillIds: ['vocabulary'],
    dependencyIds: [],
  },
  {
    id: 'writing',
    title: 'Writing',
    description: 'Produce written language.',
    category: 'writing',
    relatedSkillIds: ['grammar'],
    dependencyIds: [],
  },
  {
    id: 'vocabulary',
    title: 'Vocabulary',
    description: 'Words that stay available.',
    category: 'vocabulary',
    relatedSkillIds: ['speaking', 'reading'],
    dependencyIds: [],
  },
  {
    id: 'grammar',
    title: 'Grammar',
    description: 'Form that keeps meaning clear.',
    category: 'grammar',
    relatedSkillIds: ['writing', 'speaking'],
    dependencyIds: [],
  },
  {
    id: 'reasoning',
    title: 'Reasoning',
    description: 'Explain why an answer holds.',
    category: 'reasoning',
    relatedSkillIds: ['problem_solving'],
    dependencyIds: [],
  },
  {
    id: 'problem_solving',
    title: 'Problem solving',
    description: 'Choose a method and finish.',
    category: 'problem_solving',
    relatedSkillIds: ['math', 'reasoning'],
    dependencyIds: [],
  },
  {
    id: 'math',
    title: 'Math practice',
    description: 'Guest specialist. Same voice family.',
    category: 'math',
    relatedSkillIds: ['problem_solving'],
    dependencyIds: [],
  },
  {
    id: 'coding',
    title: 'Coding',
    description: 'Future guest. Registered, not live.',
    category: 'coding',
    relatedSkillIds: ['reasoning'],
    dependencyIds: [],
  },
  {
    id: 'career',
    title: 'Career',
    description: 'Future guest. Registered, not live.',
    category: 'career',
    relatedSkillIds: ['speaking'],
    dependencyIds: [],
  },
  {
    id: 'interview',
    title: 'Interview',
    description: 'Future guest. Registered, not live.',
    category: 'interview',
    relatedSkillIds: ['speaking', 'career'],
    dependencyIds: ['speaking'],
  },
];

const MATH_TOPICS = [
  'addition',
  'tables',
  'fractions',
  'decimals',
  'geometry',
  'multiplication',
  'percentages',
  'algebra',
] as const;

export function emptySkill(seed: SkillSeed): Skill {
  return {
    ...seed,
    difficulty: 'beginner',
    mastery: null,
    confidence: null,
    practiceCount: 0,
    lastPracticed: null,
    trend: 'unknown',
    source: 'projected',
  };
}

export function skillCatalog(): Skill[] {
  const mathChildren: Skill[] = MATH_TOPICS.map((topic) =>
    emptySkill({
      id: `math:${topic}`,
      title: topic.replace(/^\w/, (char) => char.toUpperCase()),
      description: `Math topic · ${topic}`,
      category: 'math',
      relatedSkillIds: ['math', 'problem_solving'],
      dependencyIds: ['math'],
    })
  );
  return [...SEEDS.map(emptySkill), ...mathChildren];
}

export function skillIdForTopic(topic: string): string | null {
  const key = topic.trim().toLowerCase().replaceAll(' ', '_');
  if (MATH_TOPICS.includes(key as (typeof MATH_TOPICS)[number])) return `math:${key}`;
  const direct = SEEDS.find((seed) => seed.id === key || seed.category === (key as SkillCategory));
  return direct?.id ?? null;
}
