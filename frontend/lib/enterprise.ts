export type EnterpriseSnapshot = Record<string, unknown> & {
  overview?: Record<string, unknown>;
  agents?: Array<Record<string, unknown>>;
  graph?: {
    nodes: Array<{ id: string; label: string; active: boolean }>;
    edges: Array<{ source: string; target: string }>;
  };
  timeline?: { items: Array<Record<string, unknown>>; count: number };
  decisions?: { decisions: Array<Record<string, unknown>>; count: number };
  memory_graph?: { nodes: Array<Record<string, unknown>> };
  journey?: { steps: Array<Record<string, unknown>>; streak: number };
  difficulty?: Record<string, unknown>;
  heatmap?: { cells: Array<Record<string, unknown>> };
  performance?: Record<string, unknown>;
  monitor?: { components: Record<string, { status: string; latency_ms: number }> };
  trace?: { nodes: Array<Record<string, unknown>> };
  replay?: { frames: Array<Record<string, unknown>>; speeds: number[] };
  voice?: Record<string, unknown>;
  report?: Record<string, unknown>;
  parent?: Record<string, unknown>;
  gamification?: Record<string, unknown>;
  teacher?: Record<string, unknown>;
  language?: { languages: Array<Record<string, unknown>> };
  ops?: Record<string, unknown>;
  notifications?: Array<Record<string, unknown>>;
  error?: boolean;
  message?: string;
};

export const ENTERPRISE_REFRESH_SECONDS = Number(
  process.env.NEXT_PUBLIC_ANALYTICS_REFRESH_INTERVAL_SECONDS || 30
);

export async function fetchEnterpriseSnapshot(): Promise<EnterpriseSnapshot> {
  const response = await fetch('/api/enterprise', { cache: 'no-store' });
  const data = (await response.json()) as EnterpriseSnapshot;
  if (!response.ok || data.error) {
    throw new Error(data.message || 'Enterprise data unavailable.');
  }
  return data;
}

export async function decideEnterpriseRoute(text: string): Promise<Record<string, unknown>> {
  const response = await fetch(`/api/enterprise?command=decide&text=${encodeURIComponent(text)}`, {
    cache: 'no-store',
  });
  return (await response.json()) as Record<string, unknown>;
}

export async function searchEnterprise(query: string): Promise<Record<string, unknown>> {
  const response = await fetch(
    `/api/enterprise?command=search&query=${encodeURIComponent(query)}`,
    {
      cache: 'no-store',
    }
  );
  return (await response.json()) as Record<string, unknown>;
}

export async function exportEnterprise(
  kind: string,
  format: 'json' | 'pdf'
): Promise<Record<string, unknown>> {
  const response = await fetch(
    `/api/enterprise/export?kind=${encodeURIComponent(kind)}&format=${format}`,
    { cache: 'no-store' }
  );
  return (await response.json()) as Record<string, unknown>;
}
