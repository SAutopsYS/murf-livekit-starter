export const SDK_MODULES = [
  'voice',
  'learning',
  'adaptive',
  'knowledge',
  'studio',
  'whiteboard',
  'memory_graph',
  'analytics',
  'enterprise',
  'marketplace',
  'agents',
] as const;

export type SdkModule = (typeof SDK_MODULES)[number];

export const INTEGRATION_ADAPTERS = [
  'google_workspace',
  'microsoft_365',
  'slack',
  'discord',
  'notion',
  'obsidian',
  'github',
  'gitlab',
  'jira',
  'canvas_lms',
  'moodle',
  'salesforce',
  'sap',
] as const;

export const WEBHOOK_EVENTS = [
  'LearningUpdated',
  'KnowledgeUpdated',
  'ProjectCreated',
  'CanvasCreated',
  'PluginInstalled',
  'OrganizationCreated',
  'RecommendationCreated',
  'AgentTransferred',
  'SessionEnded',
] as const;

export type SdkSnapshot = {
  version: 'v1';
  modules: readonly SdkModule[];
  adapters: readonly string[];
  webhooks: readonly string[];
  portalUi: false;
};

export function buildSdkSnapshot(): SdkSnapshot {
  return {
    version: 'v1',
    modules: SDK_MODULES,
    adapters: INTEGRATION_ADAPTERS,
    webhooks: WEBHOOK_EVENTS,
    portalUi: false,
  };
}
