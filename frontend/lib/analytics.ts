export type AnalyticsFilters = {
  preset?: string;
  startDate?: string;
  endDate?: string;
  channel?: string;
  outcome?: string;
};

export type RecentCall = {
  call_id: string;
  started_at: string | null;
  ended_at: string | null;
  duration_seconds: number | null;
  channel: string;
  outcome: string | null;
  failure_type: string | null;
};

export type AnalyticsSummary = {
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
  success_rate: number;
  failure_rate: number;
  failure_categories: Record<string, number>;
  recent_calls: RecentCall[];
  performance: {
    average_call_duration_seconds: number;
    average_first_response_ms: number;
  };
  language_breakdown: Record<string, number>;
  channel_breakdown: Record<string, number>;
  insights: {
    total_calls: number;
    success_rate: number;
    average_call_duration_seconds: number;
    average_first_response_ms: number;
    top_failure_category: string | null;
    top_language: string | null;
    top_channel: string | null;
    summary_sentence: string;
  } | null;
  specialist_analytics?: {
    total_handoffs: number;
    successful_handoffs: number;
    failed_handoffs: number;
    recovery_count: number;
    average_routing_time_ms: number;
    average_specialist_session_duration_ms: number;
  };
  error?: boolean;
  message?: string;
};

export const ANALYTICS_REFRESH_INTERVAL_SECONDS = Number(
  process.env.NEXT_PUBLIC_ANALYTICS_REFRESH_INTERVAL_SECONDS ||
    process.env.ANALYTICS_REFRESH_INTERVAL_SECONDS ||
    30
);

export function buildAnalyticsQuery(filters: AnalyticsFilters): string {
  const params = new URLSearchParams();
  if (filters.preset) params.set('preset', filters.preset);
  if (filters.startDate) params.set('start_date', filters.startDate);
  if (filters.endDate) params.set('end_date', filters.endDate);
  if (filters.channel) params.set('channel', filters.channel);
  if (filters.outcome) params.set('outcome', filters.outcome);
  return params.toString();
}

export async function fetchAnalyticsSummary(
  filters: AnalyticsFilters = {}
): Promise<AnalyticsSummary> {
  const query = buildAnalyticsQuery(filters);
  const response = await fetch(`/api/analytics${query ? `?${query}` : ''}`, {
    method: 'GET',
    cache: 'no-store',
  });
  const data = (await response.json()) as AnalyticsSummary;
  if (!response.ok || data.error) {
    throw new Error(data.message || 'Analytics are temporarily unavailable.');
  }
  return data;
}

export async function exportAnalyticsReport(
  filters: AnalyticsFilters = {}
): Promise<Record<string, unknown>> {
  const query = buildAnalyticsQuery(filters);
  const response = await fetch(`/api/analytics/export${query ? `?${query}` : ''}`, {
    method: 'GET',
    cache: 'no-store',
  });
  const data = (await response.json()) as Record<string, unknown> & {
    error?: boolean;
    message?: string;
  };
  if (!response.ok || data.error) {
    throw new Error(data.message || 'Unable to export analytics report.');
  }
  return data;
}

export function formatDuration(seconds: number | null | undefined): string {
  if (seconds == null || Number.isNaN(seconds)) return '--:--';
  const total = Math.max(0, Math.round(seconds));
  const mins = Math.floor(total / 60);
  const secs = total % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

export function formatOutcome(outcome: string | null | undefined): string {
  if (outcome === 'success') return 'Successful';
  if (outcome === 'failed') return 'Failed';
  return 'Incomplete';
}
