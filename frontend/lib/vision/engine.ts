export const V2_THEMES = [
  'autonomous_ai_teams',
  'distributed_agent_networks',
  'robotics',
  'iot',
  'cross_device',
  'ambient',
  'multimodal_workspace',
  'quantum_ready_conceptual',
] as const;

export const STABILITY_RULES = [
  'one_voice_path',
  'one_router',
  'one_search',
  'one_automation',
  'one_rbac',
  'no_utterance_column',
  'consume_do_not_rewrite',
] as const;

export const FutureRoadmap = {
  year1: 'identity, queue, studio instruments',
  year5: 'optional autonomous teams behind sandbox',
} as const;

export const EvolutionRegistry = V2_THEMES;
export const ArchitectureGuidelines = STABILITY_RULES;

export function visionSnapshot() {
  return { themes: V2_THEMES, rules: STABILITY_RULES, implementation: false as const };
}
