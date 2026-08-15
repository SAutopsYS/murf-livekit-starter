'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  OsPage,
  OsPageActions,
  OsPageContent,
  OsPageFooter,
  OsPageHeader,
  OsPageToolbar,
} from '@/components/os';
import { AnalyticsLayout, InsightCard, MetricCard, PageState } from '@/components/system';
import { Button } from '@/components/ui/button';
import { NativeSelect } from '@/components/ui/input';
import {
  ANALYTICS_REFRESH_INTERVAL_SECONDS,
  type AnalyticsFilters,
  type AnalyticsSummary,
  exportAnalyticsReport,
  fetchAnalyticsSummary,
  formatDuration,
  formatOutcome,
} from '@/lib/analytics';

type LoadState = 'loading' | 'ready' | 'error' | 'empty';

const DEFAULT_FILTERS: AnalyticsFilters = {
  preset: 'all',
  channel: 'all',
  outcome: 'all',
};

function formatRelativeDay(iso: string | null): string {
  if (!iso) return 'Unknown';
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return 'Unknown';
  const today = new Date();
  const startToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const startThat = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const diffDays = Math.round((startToday.getTime() - startThat.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  return date.toLocaleDateString();
}

function labelize(value: string | null | undefined): string {
  if (!value) return 'Unknown';
  return value.replaceAll('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase());
}

export function AnalyticsDashboard() {
  const [filters, setFilters] = useState<AnalyticsFilters>(DEFAULT_FILTERS);
  const [draft, setDraft] = useState<AnalyticsFilters>(DEFAULT_FILTERS);
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [state, setState] = useState<LoadState>('loading');
  const [refreshWarning, setRefreshWarning] = useState<string | null>(null);
  const [exportError, setExportError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const inFlight = useRef(false);
  const mounted = useRef(true);

  const load = useCallback(
    async (nextFilters: AnalyticsFilters, { soft = false }: { soft?: boolean } = {}) => {
      if (inFlight.current) return;
      inFlight.current = true;
      if (!soft) {
        setState((prev) => (prev === 'ready' ? prev : 'loading'));
        setRefreshWarning(null);
      }
      try {
        const data = await fetchAnalyticsSummary(nextFilters);
        if (!mounted.current) return;
        setSummary(data);
        setLastUpdated(new Date());
        setRefreshWarning(null);
        const empty = data.total_calls === 0;
        setState(empty ? 'empty' : 'ready');
      } catch {
        if (!mounted.current) return;
        if (summary) {
          setRefreshWarning('Unable to refresh analytics.');
        } else {
          setState('error');
        }
      } finally {
        inFlight.current = false;
      }
    },
    [summary]
  );

  const filtersRef = useRef(filters);
  const loadRef = useRef(load);
  filtersRef.current = filters;
  loadRef.current = load;

  useEffect(() => {
    mounted.current = true;
    void load(filters);
    return () => {
      mounted.current = false;
    };
  }, [filters, load]);

  useEffect(() => {
    const intervalMs = Math.max(5, ANALYTICS_REFRESH_INTERVAL_SECONDS) * 1000;
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'hidden') return;
      void loadRef.current(filtersRef.current, { soft: true });
    }, intervalMs);
    const onVisibility = () => {
      if (document.visibilityState === 'visible') {
        void loadRef.current(filtersRef.current, { soft: true });
      }
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, []);

  const applyFilters = () => setFilters(draft);
  const resetFilters = () => {
    setDraft(DEFAULT_FILTERS);
    setFilters(DEFAULT_FILTERS);
  };

  const onExport = async () => {
    setExportError(null);
    try {
      const report = await exportAnalyticsReport(filters);
      const blob = new Blob([JSON.stringify(report, null, 2)], {
        type: 'application/json',
      });
      const stamp = new Date().toISOString().slice(0, 10);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `voice-agent-analytics-${stamp}.json`;
      anchor.click();
      URL.revokeObjectURL(url);
    } catch {
      setExportError('Unable to export analytics report.');
    }
  };

  const metrics = summary ?? {
    total_calls: 0,
    successful_calls: 0,
    failed_calls: 0,
    success_rate: 0,
    failure_rate: 0,
    failure_categories: {},
    recent_calls: [],
    performance: {
      average_call_duration_seconds: 0,
      average_first_response_ms: 0,
    },
    language_breakdown: {},
    channel_breakdown: {},
    insights: null,
  };

  const completed = metrics.successful_calls + metrics.failed_calls;
  const showZeroRates = completed === 0;

  return (
    <AnalyticsLayout>
      <OsPage>
        <OsPageHeader
          eyebrow="SALORA OS · Analytics"
          title="Voice Agent Analytics"
          description="Privacy-safe aggregate metrics from real Learning & Literacy calls."
          actions={
            <OsPageActions>
              <Button variant="hall" size="sm" onClick={() => void load(filters, { soft: true })}>
                Refresh
              </Button>
              <Button variant="outline" size="sm" onClick={() => void onExport()}>
                Export Report
              </Button>
            </OsPageActions>
          }
        />

        <OsPageToolbar
          aria-label="Analytics filters"
          className="grid sm:grid-cols-2 lg:grid-cols-5"
        >
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-muted-foreground font-medium">Date</span>
            <NativeSelect
              value={draft.preset || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, preset: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="today">Today</option>
              <option value="last_7_days">Last 7 Days</option>
              <option value="last_30_days">Last 30 Days</option>
            </NativeSelect>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-muted-foreground font-medium">Channel</span>
            <NativeSelect
              value={draft.channel || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, channel: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="browser">Browser</option>
              <option value="sip">SIP</option>
            </NativeSelect>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-muted-foreground font-medium">Outcome</span>
            <NativeSelect
              value={draft.outcome || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, outcome: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="success">Successful</option>
              <option value="failed">Failed</option>
              <option value="incomplete">Incomplete</option>
            </NativeSelect>
          </label>
          <div className="flex items-end gap-2 lg:col-span-2">
            <Button type="button" onClick={applyFilters}>
              Apply
            </Button>
            <Button type="button" variant="outline" onClick={resetFilters}>
              Reset Filters
            </Button>
          </div>
        </OsPageToolbar>

        <OsPageContent>
          <div
            className="text-muted-foreground flex flex-wrap items-center gap-3 text-sm"
            aria-live="polite"
          >
            {lastUpdated ? (
              <span>
                Last updated:{' '}
                {lastUpdated.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}
              </span>
            ) : (
              <span>Updated just now</span>
            )}
            {refreshWarning ? <span className="text-salora-warning">{refreshWarning}</span> : null}
            {exportError ? <span className="text-salora-error">{exportError}</span> : null}
          </div>

          {state === 'loading' && !summary ? (
            <PageState kind="loading" title="Loading analytics" />
          ) : null}

          {state === 'error' ? (
            <PageState kind="error" title="Analytics are temporarily unavailable." />
          ) : null}

          {state !== 'error' ? (
            <>
              {state === 'empty' ? <PageState kind="empty" title="No calls recorded yet." /> : null}
              {state === 'ready' && metrics.total_calls === 0 ? (
                <PageState kind="no-results" title="No calls match these filters." />
              ) : null}

              <section aria-label="Core call metrics" className="grid gap-4 sm:grid-cols-3">
                <MetricCard label="Total Calls" value={metrics.total_calls} emphasize />
                <MetricCard label="Successful Calls" value={metrics.successful_calls} emphasize />
                <MetricCard label="Failed Calls" value={metrics.failed_calls} emphasize />
              </section>

              <section aria-label="Specialist Analytics" className="grid gap-4 sm:grid-cols-3">
                <MetricCard
                  label="Total Handoffs"
                  value={metrics.specialist_analytics?.total_handoffs ?? 0}
                />
                <MetricCard
                  label="Successful Handoffs"
                  value={metrics.specialist_analytics?.successful_handoffs ?? 0}
                />
                <MetricCard
                  label="Failed Handoffs"
                  value={metrics.specialist_analytics?.failed_handoffs ?? 0}
                />
                <MetricCard
                  label="Recovery Count"
                  value={metrics.specialist_analytics?.recovery_count ?? 0}
                />
                <MetricCard
                  label="Average Routing Time"
                  value={`${metrics.specialist_analytics?.average_routing_time_ms ?? 0} ms`}
                />
                <MetricCard
                  label="Average Specialist Session Duration"
                  value={`${metrics.specialist_analytics?.average_specialist_session_duration_ms ?? 0} ms`}
                />
              </section>

              <section aria-label="Success and failure rates" className="grid gap-4 sm:grid-cols-2">
                <MetricCard
                  label="Success Rate"
                  value={showZeroRates ? '0%' : `${metrics.success_rate}%`}
                />
                <MetricCard
                  label="Failure Rate"
                  value={showZeroRates ? '0%' : `${metrics.failure_rate}%`}
                />
              </section>
              {showZeroRates ? (
                <p className="text-muted-foreground text-sm">No completed calls yet.</p>
              ) : null}

              <InsightCard title="Failure Analysis">
                {Object.keys(metrics.failure_categories).length === 0 ? (
                  <p className="text-muted-foreground text-sm">No failure categories yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {Object.entries(metrics.failure_categories).map(([key, count]) => (
                      <li
                        key={key}
                        className="text-foreground flex items-center justify-between text-sm"
                      >
                        <span>{labelize(key)}</span>
                        <span className="font-semibold">{count}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </InsightCard>

              <section aria-label="Performance" className="grid gap-4 sm:grid-cols-2">
                <InsightCard title="Performance">
                  <dl className="space-y-3 text-sm">
                    <div className="flex justify-between gap-4">
                      <dt className="text-muted-foreground">Average Call Duration</dt>
                      <dd className="font-semibold">
                        {formatDuration(metrics.performance.average_call_duration_seconds)}
                      </dd>
                    </div>
                    <div className="flex justify-between gap-4">
                      <dt className="text-muted-foreground">Average First Response</dt>
                      <dd className="font-semibold">
                        {Math.round(metrics.performance.average_first_response_ms)} ms
                      </dd>
                    </div>
                  </dl>
                </InsightCard>
                <InsightCard title="Performance Insights">
                  <p className="text-muted-foreground text-sm">
                    {metrics.insights?.summary_sentence ||
                      'No completed calls are available for analysis.'}
                  </p>
                  <dl className="mt-4 space-y-2 text-sm">
                    <div className="flex justify-between gap-4">
                      <dt className="text-muted-foreground">Top Failure</dt>
                      <dd className="font-medium">
                        {labelize(metrics.insights?.top_failure_category)}
                      </dd>
                    </div>
                    <div className="flex justify-between gap-4">
                      <dt className="text-muted-foreground">Top Language</dt>
                      <dd className="font-medium">{metrics.insights?.top_language || 'Unknown'}</dd>
                    </div>
                    <div className="flex justify-between gap-4">
                      <dt className="text-muted-foreground">Top Channel</dt>
                      <dd className="font-medium">{labelize(metrics.insights?.top_channel)}</dd>
                    </div>
                  </dl>
                </InsightCard>
              </section>

              <section className="grid gap-4 lg:grid-cols-2">
                <InsightCard title="Language Distribution">
                  {Object.keys(metrics.language_breakdown).length === 0 ? (
                    <p className="text-muted-foreground text-sm">No language data available.</p>
                  ) : (
                    <ul className="space-y-2 text-sm">
                      {Object.entries(metrics.language_breakdown).map(([lang, count]) => (
                        <li key={lang} className="flex justify-between">
                          <span>{lang}</span>
                          <span className="font-semibold">{count}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </InsightCard>
                <InsightCard title="Call Channels">
                  {Object.keys(metrics.channel_breakdown).length === 0 ? (
                    <p className="text-muted-foreground text-sm">No channel data available.</p>
                  ) : (
                    <ul className="space-y-2 text-sm">
                      {Object.entries(metrics.channel_breakdown).map(([channel, count]) => (
                        <li key={channel} className="flex justify-between">
                          <span>{labelize(channel)}</span>
                          <span className="font-semibold">{count}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </InsightCard>
              </section>

              <InsightCard title="Recent Calls">
                {state === 'loading' && !summary ? (
                  <p className="text-muted-foreground text-sm">Loading recent calls…</p>
                ) : metrics.recent_calls.length === 0 ? (
                  <p className="text-muted-foreground text-sm">No calls recorded yet.</p>
                ) : (
                  <ul className="divide-border mt-1 divide-y">
                    {metrics.recent_calls.map((call) => (
                      <li
                        key={call.call_id}
                        className="flex flex-wrap items-center justify-between gap-2 py-3 text-sm"
                      >
                        <span className="text-foreground">
                          {formatRelativeDay(call.started_at)} · {labelize(call.channel)} ·{' '}
                          {formatDuration(call.duration_seconds)} · {formatOutcome(call.outcome)}
                          {call.failure_type ? ` · ${labelize(call.failure_type)}` : ''}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </InsightCard>
            </>
          ) : null}
        </OsPageContent>
        <OsPageFooter>Privacy-safe aggregates. No transcripts. No tape.</OsPageFooter>
      </OsPage>
    </AnalyticsLayout>
  );
}
