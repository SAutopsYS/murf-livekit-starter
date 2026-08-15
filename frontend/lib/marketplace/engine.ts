import type { MarketplaceSnapshot, PluginManifest } from '@/lib/marketplace/types';

const SEED: PluginManifest[] = [
  {
    id: 'pkg.math-specialist',
    name: 'Math Practice Specialist',
    version: '1.0',
    author: 'SALORA',
    publisher: 'salora',
    license: 'MIT',
    permissions: ['voice.session'],
    capabilities: ['agents', 'learning', 'voice'],
    dependencies: ['specialists.router'],
    entrypoint: 'specialists.math_specialist',
    icon: 'function',
    description: 'Existing math guest. Catalog row only.',
    organization: null,
    kind: 'package',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-01T00:00:00Z',
    signed: true,
    enabled: true,
  },
  {
    id: 'pkg.analytics-export',
    name: 'Analytics JSON Export',
    version: '1.0',
    author: 'SALORA',
    publisher: 'salora',
    license: 'MIT',
    permissions: ['analytics.export'],
    capabilities: ['analytics'],
    dependencies: ['analytics.service'],
    entrypoint: 'analytics.service',
    icon: 'chart',
    description: 'Existing privacy-safe export.',
    organization: null,
    kind: 'adapter',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-01T00:00:00Z',
    signed: true,
    enabled: true,
  },
];

export function buildMarketplaceSnapshot(): MarketplaceSnapshot {
  return {
    catalog: SEED,
    installed: SEED.filter((item) => item.enabled).map((item) => item.id),
    sandbox: {
      permissionIsolation: true,
      capabilityIsolation: true,
      apiIsolation: true,
      storageIsolation: true,
      networkPolicy: 'deny_by_default',
      executionPolicy: 'no_arbitrary_code',
    },
  };
}

export function searchCatalog(snapshot: MarketplaceSnapshot, query: string): PluginManifest[] {
  const needle = query.trim().toLowerCase();
  if (!needle) return snapshot.catalog;
  return snapshot.catalog.filter(
    (item) => item.name.toLowerCase().includes(needle) || item.id.includes(needle)
  );
}

export function mayExecutePlugin(): boolean {
  return false;
}
