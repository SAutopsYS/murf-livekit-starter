export type PluginCapability =
  | 'voice'
  | 'learning'
  | 'adaptive'
  | 'knowledge'
  | 'studio'
  | 'whiteboard'
  | 'memory_graph'
  | 'analytics'
  | 'enterprise'
  | 'developer'
  | 'commands'
  | 'providers'
  | 'workflows'
  | 'agents';

export type PluginKind =
  | 'plugin'
  | 'extension'
  | 'package'
  | 'module'
  | 'command'
  | 'tool'
  | 'action'
  | 'provider'
  | 'integration'
  | 'workflow'
  | 'adapter';

export type PluginManifest = {
  id: string;
  name: string;
  version: string;
  author: string;
  publisher: string;
  license: string;
  permissions: string[];
  capabilities: PluginCapability[];
  dependencies: string[];
  entrypoint: string;
  icon: string;
  description: string;
  organization: string | null;
  kind: PluginKind;
  createdAt: string;
  updatedAt: string;
  signed: boolean;
  enabled: boolean;
};

export type SandboxPolicy = {
  permissionIsolation: true;
  capabilityIsolation: true;
  apiIsolation: true;
  storageIsolation: true;
  networkPolicy: 'deny_by_default';
  executionPolicy: 'no_arbitrary_code';
};

export type MarketplaceSnapshot = {
  catalog: PluginManifest[];
  installed: string[];
  sandbox: SandboxPolicy;
};
