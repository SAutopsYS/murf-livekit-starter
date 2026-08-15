/**
 * Structured logs, metrics, traces. Privacy-safe. No speech, OTP, phone, secrets.
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export type MetricName =
  | 'voice.session.start'
  | 'voice.session.end'
  | 'voice.latency.connect_ms'
  | 'voice.latency.first_audio_ms'
  | 'api.request'
  | 'api.latency_ms'
  | 'api.error'
  | 'learning.projection'
  | 'adaptive.decision'
  | 'knowledge.retrieval'
  | 'agent.handoff'
  | 'agent.handback'
  | 'heartbeat';

export type TraceSpan = {
  name: string;
  startMs: number;
  endMs?: number;
  ok?: boolean;
};

const FORBIDDEN = /transcript|utterance|otp|phone|secret|password|token|api[_-]?key|prompt/i;

type LogFields = Record<string, unknown>;

type MetricPoint = {
  name: MetricName;
  value: number;
  at: number;
  tags?: Record<string, string>;
};

const metrics: MetricPoint[] = [];
const MAX_POINTS = 500;

function redact(fields: LogFields): LogFields {
  const clean: LogFields = {};
  for (const [key, value] of Object.entries(fields)) {
    if (FORBIDDEN.test(key)) continue;
    if (typeof value === 'string' && FORBIDDEN.test(value) && value.length > 24) continue;
    clean[key] = value;
  }
  return clean;
}

export function log(level: LogLevel, event: string, fields: LogFields = {}): void {
  const line = {
    ts: new Date().toISOString(),
    level,
    event,
    ...redact(fields),
  };
  const serialized = JSON.stringify(line);
  if (level === 'error') console.error(serialized);
  else if (level === 'warn') console.warn(serialized);
  else console.info(serialized);
}

export function recordMetric(name: MetricName, value = 1, tags?: Record<string, string>): void {
  metrics.push({ name, value, at: Date.now(), tags });
  if (metrics.length > MAX_POINTS) metrics.splice(0, metrics.length - MAX_POINTS);
}

export function getMetricsSnapshot(): {
  counts: Record<string, number>;
  last: MetricPoint[];
} {
  const counts: Record<string, number> = {};
  for (const point of metrics) {
    counts[point.name] = (counts[point.name] ?? 0) + point.value;
  }
  return { counts, last: metrics.slice(-50) };
}

export function resetMetrics(): void {
  metrics.length = 0;
}

export function startSpan(name: string): TraceSpan {
  return { name, startMs: Date.now() };
}

export function endSpan(span: TraceSpan, ok = true): number {
  span.endMs = Date.now();
  span.ok = ok;
  const duration = span.endMs - span.startMs;
  log('info', 'span.end', { span: span.name, duration_ms: duration, ok });
  return duration;
}

export function heartbeat(service: string): void {
  recordMetric('heartbeat', 1, { service });
  log('info', 'heartbeat', { service });
}
