'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { OsPage, OsPageActions, OsPageContent, OsPageHeader, useOs } from '@/components/os';
import {
  EnterpriseLayout,
  GlassCard,
  MetricCard,
  MetricSkeletonGrid,
  PageState,
  Rise,
  TimelineCard,
} from '@/components/system';
import { Button } from '@/components/ui/button';
import { NativeSelect } from '@/components/ui/input';
import {
  ENTERPRISE_REFRESH_SECONDS,
  type EnterpriseSnapshot,
  decideEnterpriseRoute,
  exportEnterprise,
  fetchEnterpriseSnapshot,
  searchEnterprise,
} from '@/lib/enterprise';
import type { OsCommand } from '@/lib/os-commands';

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

function Metric({ label, value }: { label: string; value: string | number | null | undefined }) {
  return <MetricCard label={label} value={value} />;
}

export function EnterpriseControlCenter() {
  const { setCommandOpen, registerCommands, setSearchHandler } = useOs();
  const [role, setRole] = useState<Role>('admin');
  const [section, setSection] = useState<Section>('overview');
  const [data, setData] = useState<EnterpriseSnapshot | null>(null);
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
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
    const timer = window.setInterval(
      () => {
        if (document.visibilityState === 'hidden') return;
        void load();
      },
      Math.max(5, ENTERPRISE_REFRESH_SECONDS) * 1000
    );
    return () => {
      mounted.current = false;
      window.clearInterval(timer);
    };
  }, [load]);

  const visibleSections = useMemo(
    () => SECTIONS.filter((item) => item.roles.includes(role)),
    [role]
  );

  useEffect(() => {
    const commands: OsCommand[] = visibleSections.map((item) => ({
      id: `enterprise:section:${item.id}`,
      label: item.label,
      hint: 'Control center',
      kind: 'navigation',
      keywords: `enterprise ${item.label} ${item.id}`,
      run: () => setSection(item.id),
    }));
    return registerCommands(commands);
  }, [visibleSections, registerCommands]);

  useEffect(() => {
    setSearchHandler(async (value) => {
      const result = (await searchEnterprise(value)) as {
        results?: Array<{ group: string; label: string }>;
      };
      return (result.results ?? []).map((hit) => ({
        id: `search:${hit.group}:${hit.label}`,
        label: `${hit.group}: ${hit.label}`,
        kind: 'search' as const,
      }));
    });
    return () => setSearchHandler(null);
  }, [setSearchHandler]);

  useEffect(() => {
    if (!playing) return;
    const frames = data?.replay?.frames ?? [];
    if (!frames.length) return;
    const timer = window.setInterval(() => {
      setReplayIndex((index) => (index + 1) % frames.length);
    }, 1200);
    return () => window.clearInterval(timer);
  }, [playing, data]);

  const timelineItems = useMemo(() => {
    const items = (data?.timeline?.items ?? []) as Array<Record<string, unknown>>;
    if (filterEvent === 'all') return items;
    return items.filter((item) => item.event === filterEvent);
  }, [data, filterEvent]);

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
    <EnterpriseLayout>
      <OsPage>
        <OsPageHeader
          eyebrow="SALORA OS · Control Center"
          title="Multi-Agent Learning Platform"
          actions={
            <OsPageActions>
              <label className="text-muted-foreground flex items-center gap-2 text-sm">
                Role
                <NativeSelect
                  className="h-8 w-auto"
                  value={role}
                  onChange={(event) => setRole(event.target.value as Role)}
                  aria-label="Role"
                >
                  <option value="admin">Admin</option>
                  <option value="teacher">Teacher</option>
                  <option value="parent">Parent</option>
                </NativeSelect>
              </label>
              <Button variant="hall" size="sm" onClick={() => void runMathRoute()}>
                Route math sample
              </Button>
              <Button variant="outline" size="sm" onClick={() => setCommandOpen(true)}>
                Search ⌘K
              </Button>
            </OsPageActions>
          }
        />
        <OsPageContent>
          {notice ? (
            <p
              role="status"
              className="bg-salora-success/15 rounded-[var(--salora-radius-cluster)] px-4 py-2 text-sm"
            >
              {notice}
            </p>
          ) : null}

          <nav className="flex gap-2 overflow-x-auto pb-1" aria-label="Enterprise sections">
            {visibleSections.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setSection(item.id)}
                className={`rounded-[var(--salora-radius-pill)] px-3 py-1.5 text-sm whitespace-nowrap transition-colors ${
                  section === item.id
                    ? 'bg-foreground text-background'
                    : 'bg-card text-muted-foreground hover:bg-accent'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {state === 'loading' && !data ? <MetricSkeletonGrid /> : null}
          {state === 'error' && !data ? (
            <PageState kind="error" title="Enterprise data is temporarily unavailable." />
          ) : null}

          {data ? (
            <Rise key={section} className="grid gap-4">
              {section === 'overview' ? (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <Metric label="Tutor" value={String(data.overview?.tutor ?? 'Healthy')} />
                  <Metric
                    label="Math Specialist"
                    value={String(data.overview?.math_specialist ?? '—')}
                  />
                  <Metric label="Tool Calls" value={Number(data.overview?.tool_calls ?? 0)} />
                  <Metric label="Notifications" value={(data.notifications ?? []).length} />
                </div>
              ) : null}

              {section === 'graph' ? (
                <GlassCard title="Live Agent Graph">
                  <div className="flex flex-wrap items-center gap-3 overflow-x-auto py-4">
                    {(data.graph?.nodes ?? []).map((node, index) => (
                      <div key={node.id} className="flex items-center gap-3">
                        <div className="border-primary/20 bg-primary/10 text-foreground rounded-[var(--salora-radius-cluster)] border px-4 py-3 text-sm font-medium">
                          {node.label}
                        </div>
                        {index < (data.graph?.nodes.length ?? 0) - 1 ? (
                          <span aria-hidden>→</span>
                        ) : null}
                      </div>
                    ))}
                  </div>
                </GlassCard>
              ) : null}

              {section === 'timeline' ? (
                <GlassCard title="Live Agent Timeline">
                  <label className="mb-3 block text-sm">
                    Filter
                    <NativeSelect
                      className="ml-2 inline-flex h-8 w-auto"
                      value={filterEvent}
                      onChange={(event) => setFilterEvent(event.target.value)}
                    >
                      <option value="all">All</option>
                      {timelineItems.map((item) => (
                        <option key={String(item.id)} value={String(item.event)}>
                          {String(item.event)}
                        </option>
                      ))}
                    </NativeSelect>
                  </label>
                  <ol className="space-y-3">
                    {timelineItems.map((item) => (
                      <TimelineCard
                        key={String(item.id)}
                        timestamp={String(item.timestamp)}
                        title={String(item.label)}
                      />
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
                      <p>
                        Rejected:{' '}
                        {Array.isArray(decision.rejected) ? decision.rejected.join(', ') : '—'}
                      </p>
                    </GlassCard>
                  ))}
                  {(data.decisions?.decisions ?? []).length === 0 ? (
                    <p>No routing decisions yet.</p>
                  ) : null}
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
                    <li
                      key={`${step.day}-${index}`}
                      className="border-border bg-card rounded-[var(--salora-radius-cluster)] border p-4"
                    >
                      <p className="text-muted-foreground text-xs">{String(step.day)}</p>
                      <p className="text-lg font-semibold">{String(step.topic)}</p>
                      <p>{String(step.status)}</p>
                    </li>
                  ))}
                  {(data.journey?.steps ?? []).length === 0 ? (
                    <p>No learning history yet.</p>
                  ) : null}
                  <p>Streak: {Number(data.journey?.streak ?? 0)}</p>
                </ol>
              ) : null}

              {section === 'difficulty' ? (
                <div className="grid gap-4 sm:grid-cols-3">
                  <Metric
                    label="Difficulty"
                    value={String(data.difficulty?.difficulty ?? 'medium')}
                  />
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
                      style={{
                        background: `rgba(14,165,233,${0.18 + Number(cell.intensity || 0) * 0.7})`,
                      }}
                    >
                      <p className="font-semibold capitalize">{String(cell.topic)}</p>
                      <p className="text-sm">{String(cell.practice_count)} sessions</p>
                    </div>
                  ))}
                </div>
              ) : null}

              {section === 'performance' ? (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <Metric
                    label="Successful Handoffs"
                    value={Number(data.performance?.successful_handoffs ?? 0)}
                  />
                  <Metric
                    label="Failed Handoffs"
                    value={Number(data.performance?.failed_handoffs ?? 0)}
                  />
                  <Metric
                    label="Exercises Generated"
                    value={Number(data.performance?.exercises_generated ?? 0)}
                  />
                  <Metric
                    label="Recommendations"
                    value={Number(data.performance?.learning_recommendations ?? 0)}
                  />
                </div>
              ) : null}

              {section === 'monitor' ? (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {Object.entries(data.monitor?.components ?? {}).map(([name, row]) => (
                    <GlassCard key={name} title={name.replaceAll('_', ' ')}>
                      <p>{row.status}</p>
                      <p className="text-muted-foreground text-sm">Latency {row.latency_ms} ms</p>
                    </GlassCard>
                  ))}
                </div>
              ) : null}

              {section === 'trace' ? (
                <ol className="space-y-2">
                  {(data.trace?.nodes ?? []).map((node, index) => (
                    <li
                      key={`${node.event}-${index}`}
                      className="border-border bg-card rounded-[var(--salora-radius-cluster)] border p-3"
                    >
                      <p className="text-muted-foreground text-xs">{String(node.timestamp)}</p>
                      <p>{String(node.label)}</p>
                      <p className="text-sm">
                        {String(node.service)} · {String(node.status)}
                      </p>
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
                    <Button type="button" size="sm" onClick={() => setPlaying(true)}>
                      Play
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setPlaying(false)}
                    >
                      Pause
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setReplayIndex((index) => Math.max(0, index - 1))}
                    >
                      Previous
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setReplayIndex((index) => index + 1)}
                    >
                      Next
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => setReplayIndex(0)}
                    >
                      Restart
                    </Button>
                  </div>
                </GlassCard>
              ) : null}

              {section === 'voice' ? (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <Metric
                    label="Speaking (s)"
                    value={Number(data.voice?.speaking_duration_seconds ?? 0)}
                  />
                  <Metric
                    label="Silence (s)"
                    value={Number(data.voice?.silence_duration_seconds ?? 0)}
                  />
                  <Metric
                    label="Latency (ms)"
                    value={Number(data.voice?.average_response_latency_ms ?? 0)}
                  />
                  <Metric label="Speaking ratio" value={Number(data.voice?.speaking_ratio ?? 0)} />
                </div>
              ) : null}

              {section === 'reports' ? (
                <GlassCard title="Report Download Center">
                  <div className="flex flex-wrap gap-2">
                    <Button type="button" size="sm" onClick={() => void onExport('report', 'json')}>
                      JSON report
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => void onExport('report', 'pdf')}
                    >
                      PDF report
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => void onExport('teacher', 'json')}
                    >
                      Teacher JSON
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      onClick={() => void onExport('health', 'pdf')}
                    >
                      Health PDF
                    </Button>
                  </div>
                </GlassCard>
              ) : null}

              {section === 'parent' ? (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <Metric
                    label="Weekly practice"
                    value={Number(data.parent?.weekly_practice ?? 0)}
                  />
                  <Metric label="Streak" value={Number(data.parent?.learning_streak ?? 0)} />
                  <Metric
                    label="Completion %"
                    value={Number(data.parent?.completion_percent ?? 0)}
                  />
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
                  <p className="text-muted-foreground mb-3 text-sm">
                    {Number(data.teacher?.count ?? 0)} consenting learners
                  </p>
                  <ul className="space-y-2">
                    {((data.teacher?.students as Array<Record<string, unknown>>) ?? []).map(
                      (student) => (
                        <li
                          key={String(student.learner_ref)}
                          className="border-border rounded-[var(--salora-radius-cluster)] border p-3"
                        >
                          <p>Ref {String(student.learner_ref)}</p>
                          <p className="text-muted-foreground text-sm">
                            {String(student.grade || 'unset')} ·{' '}
                            {String(student.language || 'unset')}
                          </p>
                        </li>
                      )
                    )}
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
            </Rise>
          ) : null}
        </OsPageContent>
      </OsPage>
    </EnterpriseLayout>
  );
}
