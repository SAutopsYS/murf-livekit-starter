'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Link from 'next/link';
import { motion, useReducedMotion } from 'motion/react';
import {
  ENTERPRISE_REFRESH_SECONDS,
  decideEnterpriseRoute,
  exportEnterprise,
  fetchEnterpriseSnapshot,
  searchEnterprise,
  type EnterpriseSnapshot,
} from '@/lib/enterprise';

type Role = 'admin' | 'teacher' | 'parent';
type Section =
  | 'overview'
  | 'graph'
  | 'timeline'
  | 'decisions'
  | 'memory'
  | 'journey'
  | 'difficulty'
  | 'heatmap'
  | 'performance'
  | 'monitor'
  | 'trace'
  | 'replay'
  | 'voice'
  | 'reports'
  | 'parent'
  | 'gamification'
  | 'teacher'
  | 'language'
  | 'ops';

const SECTIONS: Array<{ id: Section; label: string; roles: Role[] }> = [
  { id: 'overview', label: 'Overview', roles: ['admin', 'teacher', 'parent'] },
  { id: 'graph', label: 'Agent Graph', roles: ['admin'] },
  { id: 'timeline', label: 'Timeline', roles: ['admin'] },
  { id: 'decisions', label: 'Decisions', roles: ['admin'] },
  { id: 'memory', label: 'Memory Graph', roles: ['admin', 'teacher'] },
  { id: 'journey', label: 'Learning Journey', roles: ['admin', 'teacher', 'parent'] },
  { id: 'difficulty', label: 'Difficulty', roles: ['admin', 'teacher'] },
  { id: 'heatmap', label: 'Heatmap', roles: ['admin', 'teacher'] },
  { id: 'performance', label: 'AI Performance', roles: ['admin'] },
  { id: 'monitor', label: 'Live Monitor', roles: ['admin'] },
  { id: 'trace', label: 'Execution Trace', roles: ['admin'] },
  { id: 'replay', label: 'Session Replay', roles: ['admin'] },
  { id: 'voice', label: 'Voice Analytics', roles: ['admin'] },
  { id: 'reports', label: 'Reports', roles: ['admin', 'teacher', 'parent'] },
  { id: 'parent', label: 'Parent', roles: ['admin', 'parent'] },
  { id: 'gamification', label: 'Gamification', roles: ['admin', 'teacher', 'parent'] },
  { id: 'teacher', label: 'Teacher Console', roles: ['admin', 'teacher'] },
  { id: 'language', label: 'Languages', roles: ['admin'] },
  { id: 'ops', label: 'Production', roles: ['admin'] },
];

function GlassCard({
  title,
  children,
  className = '',
}: {
  title?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <article
      className={`rounded-2xl border border-white/40 bg-white/70 p-5 shadow-[0_8px_30px_rgb(15,23,42,0.06)] backdrop-blur-xl dark:border-white/10 dark:bg-slate-900/50 ${className}`}
    >
      {title ? <h3 className="mb-3 text-sm font-semibold tracking-wide text-slate-500 uppercase">{title}</h3> : null}
      {children}
    </article>
  );
}

function SkeletonGrid() {
  return (
    <div className="grid gap-4 sm:grid-cols-3" aria-busy="true" aria-label="Loading enterprise metrics">
      {[0, 1, 2, 3, 4, 5].map((key) => (
        <div
          key={key}
          className="h-28 animate-pulse rounded-2xl bg-gradient-to-r from-slate-200 via-slate-100 to-slate-200 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800"
        />
      ))}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number | null | undefined }) {
  return (
    <GlassCard>
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">{value ?? '—'}</p>
    </GlassCard>
  );
}

export function EnterpriseControlCenter() {
  const reduceMotion = useReducedMotion();
  const [role, setRole] = useState<Role>('admin');
  const [section, setSection] = useState<Section>('overview');
  const [data, setData] = useState<EnterpriseSnapshot | null>(null);
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [searchHits, setSearchHits] = useState<Array<{ group: string; label: string }>>([]);
  const [notice, setNotice] = useState<string | null>(null);
  const [replayIndex, setReplayIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [filterEvent, setFilterEvent] = useState('all');
  const inFlight = useRef(false);
  const mounted = useRef(true);

  const load = useCallback(async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    try {
      const snapshot = await fetchEnterpriseSnapshot();
      if (!mounted.current) return;
      setData(snapshot);
      setState('ready');
    } catch {
      if (!mounted.current) return;
      setState((prev) => (prev === 'ready' ? prev : 'error'));
    } finally {
      inFlight.current = false;
    }
  }, []);

  useEffect(() => {
    mounted.current = true;
    void load();
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'hidden') return;
      void load();
    }, Math.max(5, ENTERPRISE_REFRESH_SECONDS) * 1000);
    return () => {
      mounted.current = false;
      window.clearInterval(timer);
    };
  }, [load]);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setPaletteOpen((open) => !open);
      }
      if (event.key === 'Escape') setPaletteOpen(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  useEffect(() => {
    if (!playing) return;
    const frames = data?.replay?.frames ?? [];
    if (!frames.length) return;
    const timer = window.setInterval(() => {
      setReplayIndex((index) => (index + 1) % frames.length);
    }, 1200);
    return () => window.clearInterval(timer);
  }, [playing, data]);

  const visibleSections = useMemo(
    () => SECTIONS.filter((item) => item.roles.includes(role)),
    [role]
  );

  const timelineItems = useMemo(() => {
    const items = (data?.timeline?.items ?? []) as Array<Record<string, unknown>>;
    if (filterEvent === 'all') return items;
    return items.filter((item) => item.event === filterEvent);
  }, [data, filterEvent]);

  const onSearch = async (value: string) => {
    setQuery(value);
    if (value.trim().length < 2) {
      setSearchHits([]);
      return;
    }
    const result = (await searchEnterprise(value)) as { results?: Array<{ group: string; label: string }> };
    setSearchHits(result.results ?? []);
  };

  const onExport = async (kind: string, format: 'json' | 'pdf') => {
    const payload = await exportEnterprise(kind, format);
    if (format === 'pdf' && typeof payload.content_base64 === 'string') {
      const bytes = Uint8Array.from(atob(payload.content_base64), (char) => char.charCodeAt(0));
      const blob = new Blob([bytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = String(payload.filename || `${kind}.pdf`);
      link.click();
      URL.revokeObjectURL(url);
    } else {
      const blob = new Blob([JSON.stringify(payload.payload ?? payload, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${kind}.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
    setNotice('Export completed');
  };

  const runMathRoute = async () => {
    await decideEnterpriseRoute('Help me solve 24 x 18 multiplication');
    setNotice('Routing decision recorded');
    await load();
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(14,165,233,0.12),_transparent_36%),linear-gradient(180deg,#f8fafc,white)] px-4 pt-24 pb-16 dark:bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.12),_transparent_36%),linear-gradient(180deg,#0b1220,#0f172a)]">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold tracking-[0.16em] text-sky-600 uppercase">Enterprise Control Center</p>
            <h1 className="mt-1 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
              Multi-Agent Learning Platform
            </h1>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Link className="rounded-full border border-slate-200 bg-white/80 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-900" href="/">
              Voice
            </Link>
            <Link className="rounded-full border border-slate-200 bg-white/80 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-900" href="/analytics">
              Analytics
            </Link>
            <label className="text-sm text-slate-500">
              Role
              <select
                className="ml-2 rounded-lg border border-slate-200 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-900"
                value={role}
                onChange={(event) => setRole(event.target.value as Role)}
                aria-label="Role"
              >
                <option value="admin">Admin</option>
                <option value="teacher">Teacher</option>
                <option value="parent">Parent</option>
              </select>
            </label>
            <button
              type="button"
              className="rounded-full bg-sky-600 px-3 py-1.5 text-sm text-white"
              onClick={() => void runMathRoute()}
            >
              Route math sample
            </button>
            <button
              type="button"
              className="rounded-full border border-slate-200 px-3 py-1.5 text-sm dark:border-slate-700"
              onClick={() => setPaletteOpen(true)}
            >
              Search ⌘K
            </button>
          </div>
        </header>

        {notice ? (
          <p role="status" className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-800">
            {notice}
          </p>
        ) : null}

        <nav className="flex gap-2 overflow-x-auto pb-1" aria-label="Enterprise sections">
          {visibleSections.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setSection(item.id)}
              className={`rounded-full px-3 py-1.5 text-sm whitespace-nowrap transition ${
                section === item.id
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                  : 'bg-white/70 text-slate-600 dark:bg-slate-900/60 dark:text-slate-300'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {state === 'loading' && !data ? <SkeletonGrid /> : null}
        {state === 'error' && !data ? (
          <p role="alert" className="rounded-2xl border border-rose-200 bg-rose-50 p-8 text-center text-rose-800">
            Enterprise data is temporarily unavailable.
          </p>
        ) : null}

        {data ? (
          <motion.section
            key={section}
            initial={reduceMotion ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid gap-4"
          >
            {section === 'overview' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="Tutor" value={String(data.overview?.tutor ?? 'Healthy')} />
                <Metric label="Math Specialist" value={String(data.overview?.math_specialist ?? '—')} />
                <Metric label="Tool Calls" value={Number(data.overview?.tool_calls ?? 0)} />
                <Metric label="Notifications" value={(data.notifications ?? []).length} />
              </div>
            ) : null}

            {section === 'graph' ? (
              <GlassCard title="Live Agent Graph">
                <div className="flex flex-wrap items-center gap-3 overflow-x-auto py-4">
                  {(data.graph?.nodes ?? []).map((node, index) => (
                    <div key={node.id} className="flex items-center gap-3">
                      <div className="rounded-2xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm font-medium text-sky-900">
                        {node.label}
                      </div>
                      {index < (data.graph?.nodes.length ?? 0) - 1 ? <span aria-hidden>→</span> : null}
                    </div>
                  ))}
                </div>
              </GlassCard>
            ) : null}

            {section === 'timeline' ? (
              <GlassCard title="Live Agent Timeline">
                <label className="mb-3 block text-sm">
                  Filter
                  <select
                    className="ml-2 rounded-lg border px-2 py-1"
                    value={filterEvent}
                    onChange={(event) => setFilterEvent(event.target.value)}
                  >
                    <option value="all">All</option>
                    {timelineItems.map((item) => (
                      <option key={String(item.id)} value={String(item.event)}>
                        {String(item.event)}
                      </option>
                    ))}
                  </select>
                </label>
                <ol className="space-y-3">
                  {timelineItems.map((item) => (
                    <li key={String(item.id)} className="rounded-xl border border-slate-200/70 bg-white/60 p-3 dark:border-slate-700">
                      <p className="text-xs text-slate-500">{String(item.timestamp)}</p>
                      <p className="font-medium">{String(item.label)}</p>
                    </li>
                  ))}
                </ol>
              </GlassCard>
            ) : null}

            {section === 'decisions' ? (
              <div className="grid gap-3">
                {(data.decisions?.decisions ?? []).map((decision) => (
                  <GlassCard key={String(decision.id)} title={String(decision.selected_agent)}>
                    <p>Intent: {String(decision.intent || '—')}</p>
                    <p>Confidence: {Math.round(Number(decision.confidence || 0) * 100)}%</p>
                    <p>Reason: {String(decision.reason)}</p>
                    <p>Alternative: {String(decision.alternative)}</p>
                    <p>Rejected: {Array.isArray(decision.rejected) ? decision.rejected.join(', ') : '—'}</p>
                  </GlassCard>
                ))}
                {(data.decisions?.decisions ?? []).length === 0 ? <p>No routing decisions yet.</p> : null}
              </div>
            ) : null}

            {section === 'memory' ? (
              <div className="grid gap-3 sm:grid-cols-2">
                {(data.memory_graph?.nodes ?? []).map((node) => (
                  <GlassCard key={String(node.id)} title={String(node.label)}>
                    <p>{String(node.value)}</p>
                  </GlassCard>
                ))}
              </div>
            ) : null}

            {section === 'journey' ? (
              <ol className="space-y-3">
                {(data.journey?.steps ?? []).map((step, index) => (
                  <li key={`${step.day}-${index}`} className="rounded-2xl border bg-white/70 p-4 dark:bg-slate-900/50">
                    <p className="text-xs text-slate-500">{String(step.day)}</p>
                    <p className="text-lg font-semibold">{String(step.topic)}</p>
                    <p>{String(step.status)}</p>
                  </li>
                ))}
                {(data.journey?.steps ?? []).length === 0 ? <p>No learning history yet.</p> : null}
                <p>Streak: {Number(data.journey?.streak ?? 0)}</p>
              </ol>
            ) : null}

            {section === 'difficulty' ? (
              <div className="grid gap-4 sm:grid-cols-3">
                <Metric label="Difficulty" value={String(data.difficulty?.difficulty ?? 'medium')} />
                <Metric label="Accuracy" value={String(data.difficulty?.accuracy ?? '—')} />
                <Metric label="Reason" value={String(data.difficulty?.reason ?? 'hold')} />
              </div>
            ) : null}

            {section === 'heatmap' ? (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {(data.heatmap?.cells ?? []).map((cell) => (
                  <div
                    key={String(cell.topic)}
                    title={`Practice ${cell.practice_count}`}
                    className="rounded-2xl p-4 text-white"
                    style={{ background: `rgba(14,165,233,${0.18 + Number(cell.intensity || 0) * 0.7})` }}
                  >
                    <p className="font-semibold capitalize">{String(cell.topic)}</p>
                    <p className="text-sm">{String(cell.practice_count)} sessions</p>
                  </div>
                ))}
              </div>
            ) : null}

            {section === 'performance' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="Successful Handoffs" value={Number(data.performance?.successful_handoffs ?? 0)} />
                <Metric label="Failed Handoffs" value={Number(data.performance?.failed_handoffs ?? 0)} />
                <Metric label="Exercises Generated" value={Number(data.performance?.exercises_generated ?? 0)} />
                <Metric label="Recommendations" value={Number(data.performance?.learning_recommendations ?? 0)} />
              </div>
            ) : null}

            {section === 'monitor' ? (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {Object.entries(data.monitor?.components ?? {}).map(([name, row]) => (
                  <GlassCard key={name} title={name.replaceAll('_', ' ')}>
                    <p>{row.status}</p>
                    <p className="text-sm text-slate-500">Latency {row.latency_ms} ms</p>
                  </GlassCard>
                ))}
              </div>
            ) : null}

            {section === 'trace' ? (
              <ol className="space-y-2">
                {(data.trace?.nodes ?? []).map((node, index) => (
                  <li key={`${node.event}-${index}`} className="rounded-xl border bg-white/70 p-3 dark:bg-slate-900/40">
                    <p className="text-xs text-slate-500">{String(node.timestamp)}</p>
                    <p>{String(node.label)}</p>
                    <p className="text-sm">{String(node.service)} · {String(node.status)}</p>
                  </li>
                ))}
              </ol>
            ) : null}

            {section === 'replay' ? (
              <GlassCard title="Smart Session Replay">
                <p className="mb-3 text-lg font-medium">
                  {String((data.replay?.frames ?? [])[replayIndex]?.label || 'No frames yet')}
                </p>
                <div className="flex flex-wrap gap-2">
                  <button type="button" className="rounded-lg bg-slate-900 px-3 py-1 text-white" onClick={() => setPlaying(true)}>
                    Play
                  </button>
                  <button type="button" className="rounded-lg border px-3 py-1" onClick={() => setPlaying(false)}>
                    Pause
                  </button>
                  <button
                    type="button"
                    className="rounded-lg border px-3 py-1"
                    onClick={() => setReplayIndex((index) => Math.max(0, index - 1))}
                  >
                    Previous
                  </button>
                  <button
                    type="button"
                    className="rounded-lg border px-3 py-1"
                    onClick={() => setReplayIndex((index) => index + 1)}
                  >
                    Next
                  </button>
                  <button type="button" className="rounded-lg border px-3 py-1" onClick={() => setReplayIndex(0)}>
                    Restart
                  </button>
                </div>
              </GlassCard>
            ) : null}

            {section === 'voice' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="Speaking (s)" value={Number(data.voice?.speaking_duration_seconds ?? 0)} />
                <Metric label="Silence (s)" value={Number(data.voice?.silence_duration_seconds ?? 0)} />
                <Metric label="Latency (ms)" value={Number(data.voice?.average_response_latency_ms ?? 0)} />
                <Metric label="Speaking ratio" value={Number(data.voice?.speaking_ratio ?? 0)} />
              </div>
            ) : null}

            {section === 'reports' ? (
              <GlassCard title="Report Download Center">
                <div className="flex flex-wrap gap-2">
                  <button type="button" className="rounded-lg bg-sky-600 px-3 py-2 text-white" onClick={() => void onExport('report', 'json')}>
                    JSON report
                  </button>
                  <button type="button" className="rounded-lg border px-3 py-2" onClick={() => void onExport('report', 'pdf')}>
                    PDF report
                  </button>
                  <button type="button" className="rounded-lg border px-3 py-2" onClick={() => void onExport('teacher', 'json')}>
                    Teacher JSON
                  </button>
                  <button type="button" className="rounded-lg border px-3 py-2" onClick={() => void onExport('health', 'pdf')}>
                    Health PDF
                  </button>
                </div>
              </GlassCard>
            ) : null}

            {section === 'parent' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="Weekly practice" value={Number(data.parent?.weekly_practice ?? 0)} />
                <Metric label="Streak" value={Number(data.parent?.learning_streak ?? 0)} />
                <Metric label="Completion %" value={Number(data.parent?.completion_percent ?? 0)} />
                <Metric label="Difficulty" value={String(data.parent?.difficulty ?? '—')} />
              </div>
            ) : null}

            {section === 'gamification' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="XP" value={Number(data.gamification?.xp ?? 0)} />
                <Metric label="Level" value={String(data.gamification?.level ?? 'Beginner')} />
                <Metric label="Coins" value={Number(data.gamification?.coins ?? 0)} />
                <Metric label="Stars" value={Number(data.gamification?.stars ?? 0)} />
              </div>
            ) : null}

            {section === 'teacher' ? (
              <GlassCard title="Students">
                <p className="mb-3 text-sm text-slate-500">{Number(data.teacher?.count ?? 0)} consenting learners</p>
                <ul className="space-y-2">
                  {((data.teacher?.students as Array<Record<string, unknown>>) ?? []).map((student) => (
                    <li key={String(student.learner_ref)} className="rounded-xl border p-3">
                      <p>Ref {String(student.learner_ref)}</p>
                      <p className="text-sm text-slate-500">
                        {String(student.grade || 'unset')} · {String(student.language || 'unset')}
                      </p>
                    </li>
                  ))}
                </ul>
              </GlassCard>
            ) : null}

            {section === 'language' ? (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {(data.language?.languages ?? []).map((lang) => (
                  <GlassCard key={String(lang.code)} title={String(lang.name)}>
                    <p>Script: {String(lang.script)}</p>
                    <p>Murf voice: {String(lang.voice)}</p>
                  </GlassCard>
                ))}
              </div>
            ) : null}

            {section === 'ops' ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <Metric label="Health score" value={Number(data.ops?.health_score ?? 0)} />
                <Metric label="Status" value={String(data.ops?.status ?? '—')} />
                <Metric label="Sessions" value={Number(data.ops?.session_count ?? 0)} />
                <Metric label="Retries" value={Number(data.ops?.retries ?? 0)} />
              </div>
            ) : null}
          </motion.section>
        ) : null}

        {paletteOpen ? (
          <div className="fixed inset-0 z-50 flex items-start justify-center bg-slate-950/40 p-6 backdrop-blur-sm" role="dialog" aria-label="Command palette">
            <div className="w-full max-w-xl rounded-2xl border bg-white p-4 shadow-2xl dark:bg-slate-900">
              <input
                autoFocus
                className="w-full rounded-xl border px-3 py-2"
                placeholder="Search agents, topics, pages"
                value={query}
                onChange={(event) => void onSearch(event.target.value)}
                aria-label="Global search"
              />
              <ul className="mt-3 max-h-64 overflow-auto">
                {visibleSections
                  .filter((item) => item.label.toLowerCase().includes(query.toLowerCase()))
                  .map((item) => (
                    <li key={item.id}>
                      <button
                        type="button"
                        className="w-full rounded-lg px-3 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800"
                        onClick={() => {
                          setSection(item.id);
                          setPaletteOpen(false);
                        }}
                      >
                        {item.label}
                      </button>
                    </li>
                  ))}
                {searchHits.map((hit) => (
                  <li key={`${hit.group}-${hit.label}`} className="px-3 py-2 text-sm text-slate-500">
                    {hit.group}: {hit.label}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : null}
      </div>
    </main>
  );
}
