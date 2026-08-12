'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import Link from 'next/link';
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

function MetricCard({
  label,
  value,
  emphasize = false,
}: {
  label: string;
  value: string | number;
  emphasize?: boolean;
}) {
  return (
    <article
      className={`rounded-2xl border border-slate-200/80 bg-white/90 p-5 shadow-sm ${
        emphasize ? 'ring-1 ring-sky-200' : ''
      }`}
      aria-label={`${label}: ${value}`}
    >
      <h3 className="text-sm font-medium text-slate-500">{label}</h3>
      <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">{value}</p>
    </article>
  );
}

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
    <main className="min-h-screen bg-gradient-to-b from-sky-50 via-white to-slate-50 text-slate-900">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-medium text-sky-700">VoiceForBharat · Day 8</p>
            <h1 className="mt-1 text-3xl font-semibold tracking-tight sm:text-4xl">
              Voice Agent Analytics
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-600">
              Privacy-safe aggregate metrics from real Learning &amp; Literacy calls.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/"
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Back to Tutor
            </Link>
            <button
              type="button"
              onClick={() => void load(filters, { soft: true })}
              className="rounded-full bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700"
            >
              Refresh
            </button>
            <button
              type="button"
              onClick={() => void onExport()}
              className="rounded-full border border-sky-200 bg-sky-50 px-4 py-2 text-sm font-medium text-sky-800 hover:bg-sky-100"
            >
              Export Report
            </button>
          </div>
        </header>

        <section
          aria-label="Analytics filters"
          className="grid gap-3 rounded-2xl border border-slate-200 bg-white/80 p-4 sm:grid-cols-2 lg:grid-cols-5"
        >
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium text-slate-600">Date</span>
            <select
              className="rounded-lg border border-slate-200 bg-white px-3 py-2"
              value={draft.preset || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, preset: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="today">Today</option>
              <option value="last_7_days">Last 7 Days</option>
              <option value="last_30_days">Last 30 Days</option>
            </select>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium text-slate-600">Channel</span>
            <select
              className="rounded-lg border border-slate-200 bg-white px-3 py-2"
              value={draft.channel || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, channel: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="browser">Browser</option>
              <option value="sip">SIP</option>
            </select>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium text-slate-600">Outcome</span>
            <select
              className="rounded-lg border border-slate-200 bg-white px-3 py-2"
              value={draft.outcome || 'all'}
              onChange={(event) => setDraft((prev) => ({ ...prev, outcome: event.target.value }))}
            >
              <option value="all">All</option>
              <option value="success">Successful</option>
              <option value="failed">Failed</option>
              <option value="incomplete">Incomplete</option>
            </select>
          </label>
          <div className="flex items-end gap-2 lg:col-span-2">
            <button
              type="button"
              onClick={applyFilters}
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white"
            >
              Apply
            </button>
            <button
              type="button"
              onClick={resetFilters}
              className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700"
            >
              Reset Filters
            </button>
          </div>
        </section>

        <div
          className="flex flex-wrap items-center gap-3 text-sm text-slate-500"
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
          {refreshWarning ? <span className="text-amber-700">{refreshWarning}</span> : null}
          {exportError ? <span className="text-rose-700">{exportError}</span> : null}
        </div>

        {state === 'loading' && !summary ? (
          <p className="rounded-2xl border border-dashed border-slate-300 bg-white/70 p-8 text-center text-slate-600">
            Loading analytics…
          </p>
        ) : null}

        {state === 'error' ? (
          <p
            role="alert"
            className="rounded-2xl border border-rose-200 bg-rose-50 p-8 text-center text-rose-800"
          >
            Analytics are temporarily unavailable.
          </p>
        ) : null}

        {state !== 'error' ? (
          <>
            {state === 'empty' ? (
              <p className="rounded-2xl border border-slate-200 bg-white/80 p-4 text-sm text-slate-600">
                No calls recorded yet.
              </p>
            ) : null}
            {state === 'ready' && metrics.total_calls === 0 ? (
              <p className="rounded-2xl border border-slate-200 bg-white/80 p-4 text-sm text-slate-600">
                No calls match these filters.
              </p>
            ) : null}

            <section aria-label="Core call metrics" className="grid gap-4 sm:grid-cols-3">
              <MetricCard label="Total Calls" value={metrics.total_calls} emphasize />
              <MetricCard label="Successful Calls" value={metrics.successful_calls} emphasize />
              <MetricCard label="Failed Calls" value={metrics.failed_calls} emphasize />
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
              <p className="text-sm text-slate-500">No completed calls yet.</p>
            ) : null}

            <section
              aria-label="Failure analysis"
              className="rounded-2xl border border-slate-200 bg-white/90 p-5"
            >
              <h2 className="text-lg font-semibold">Failure Analysis</h2>
              {Object.keys(metrics.failure_categories).length === 0 ? (
                <p className="mt-3 text-sm text-slate-500">No failure categories yet.</p>
              ) : (
                <ul className="mt-3 space-y-2">
                  {Object.entries(metrics.failure_categories).map(([key, count]) => (
                    <li
                      key={key}
                      className="flex items-center justify-between text-sm text-slate-700"
                    >
                      <span>{labelize(key)}</span>
                      <span className="font-semibold">{count}</span>
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section
              aria-label="Performance"
              className="grid gap-4 rounded-2xl border border-slate-200 bg-white/90 p-5 sm:grid-cols-2"
            >
              <div>
                <h2 className="text-lg font-semibold">Performance</h2>
                <dl className="mt-4 space-y-3 text-sm">
                  <div className="flex justify-between gap-4">
                    <dt className="text-slate-500">Average Call Duration</dt>
                    <dd className="font-semibold">
                      {formatDuration(metrics.performance.average_call_duration_seconds)}
                    </dd>
                  </div>
                  <div className="flex justify-between gap-4">
                    <dt className="text-slate-500">Average First Response</dt>
                    <dd className="font-semibold">
                      {Math.round(metrics.performance.average_first_response_ms)} ms
                    </dd>
                  </div>
                </dl>
              </div>
              <div>
                <h2 className="text-lg font-semibold">Performance Insights</h2>
                <p className="mt-3 text-sm text-slate-600">
                  {metrics.insights?.summary_sentence ||
                    'No completed calls are available for analysis.'}
                </p>
                <dl className="mt-4 space-y-2 text-sm">
                  <div className="flex justify-between gap-4">
                    <dt className="text-slate-500">Top Failure</dt>
                    <dd className="font-medium">
                      {labelize(metrics.insights?.top_failure_category)}
                    </dd>
                  </div>
                  <div className="flex justify-between gap-4">
                    <dt className="text-slate-500">Top Language</dt>
                    <dd className="font-medium">{metrics.insights?.top_language || 'Unknown'}</dd>
                  </div>
                  <div className="flex justify-between gap-4">
                    <dt className="text-slate-500">Top Channel</dt>
                    <dd className="font-medium">{labelize(metrics.insights?.top_channel)}</dd>
                  </div>
                </dl>
              </div>
            </section>

            <section className="grid gap-4 lg:grid-cols-2">
              <div className="rounded-2xl border border-slate-200 bg-white/90 p-5">
                <h2 className="text-lg font-semibold">Language Distribution</h2>
                {Object.keys(metrics.language_breakdown).length === 0 ? (
                  <p className="mt-3 text-sm text-slate-500">No language data available.</p>
                ) : (
                  <ul className="mt-3 space-y-2 text-sm">
                    {Object.entries(metrics.language_breakdown).map(([lang, count]) => (
                      <li key={lang} className="flex justify-between">
                        <span>{lang}</span>
                        <span className="font-semibold">{count}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <div className="rounded-2xl border border-slate-200 bg-white/90 p-5">
                <h2 className="text-lg font-semibold">Call Channels</h2>
                {Object.keys(metrics.channel_breakdown).length === 0 ? (
                  <p className="mt-3 text-sm text-slate-500">No channel data available.</p>
                ) : (
                  <ul className="mt-3 space-y-2 text-sm">
                    {Object.entries(metrics.channel_breakdown).map(([channel, count]) => (
                      <li key={channel} className="flex justify-between">
                        <span>{labelize(channel)}</span>
                        <span className="font-semibold">{count}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </section>

            <section
              aria-label="Recent calls"
              className="rounded-2xl border border-slate-200 bg-white/90 p-5"
            >
              <h2 className="text-lg font-semibold">Recent Calls</h2>
              {state === 'loading' && !summary ? (
                <p className="mt-3 text-sm text-slate-500">Loading recent calls…</p>
              ) : metrics.recent_calls.length === 0 ? (
                <p className="mt-3 text-sm text-slate-500">No calls recorded yet.</p>
              ) : (
                <ul className="mt-4 divide-y divide-slate-100">
                  {metrics.recent_calls.map((call) => (
                    <li
                      key={call.call_id}
                      className="flex flex-wrap items-center justify-between gap-2 py-3 text-sm"
                    >
                      <span className="text-slate-700">
                        {formatRelativeDay(call.started_at)} · {labelize(call.channel)} ·{' '}
                        {formatDuration(call.duration_seconds)} · {formatOutcome(call.outcome)}
                        {call.failure_type ? ` · ${labelize(call.failure_type)}` : ''}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
