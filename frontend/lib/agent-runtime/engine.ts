export type AgentKind =
  | 'tutor'
  | 'math'
  | 'coding'
  | 'career'
  | 'interview'
  | 'language'
  | 'writing'
  | 'research'
  | 'planning'
  | 'creative'
  | 'enterprise'
  | 'custom';

export type AgentStatus =
  | 'registered'
  | 'loaded'
  | 'started'
  | 'busy'
  | 'waiting'
  | 'completed'
  | 'failed'
  | 'suspended'
  | 'disabled';

export type AgentManifest = {
  id: string;
  name: string;
  kind: AgentKind;
  status: AgentStatus;
  live: boolean;
  source: 'specialist.registry' | 'host';
};

export type AgentRuntimeSnapshot = {
  agents: AgentManifest[];
  autonomousLoops: false;
  routingAuthority: 'specialist.router';
};

export function buildAgentRuntime(): AgentRuntimeSnapshot {
  return {
    routingAuthority: 'specialist.router',
    autonomousLoops: false,
    agents: [
      {
        id: 'agent.tutor',
        name: 'Main Tutor',
        kind: 'tutor',
        status: 'started',
        live: true,
        source: 'host',
      },
      {
        id: 'agent.math_practice_specialist',
        name: 'Math Practice Specialist',
        kind: 'math',
        status: 'registered',
        live: true,
        source: 'specialist.registry',
      },
    ],
  };
}
