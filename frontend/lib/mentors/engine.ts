import { type AgentKind, type AgentManifest, buildAgentRuntime } from '@/lib/agent-runtime/engine';

const MENTORS: AgentKind[] = [
  'tutor',
  'math',
  'coding',
  'career',
  'interview',
  'language',
  'writing',
  'research',
];

export function listMentors(): AgentManifest[] {
  return buildAgentRuntime().agents.filter((item) => MENTORS.includes(item.kind));
}

export const MENTOR_POLICIES = {
  autonomous: false,
  router: 'specialist.router',
  voice: 'one_path',
} as const;

export const MentorEngine = { list: listMentors };
export const MentorRegistry = { list: listMentors };
