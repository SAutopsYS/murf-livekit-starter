/**
 * Headers, CORS, CSRF origin check, rate limit, validation, audit, privacy.
 */
import { getPlatformConfig } from '@/lib/platform/config';
import { log } from '@/lib/platform/observability';

export { SECURITY_HEADERS, productionSecurityHeaders } from '@/lib/platform/headers';

export function assertSameOrigin(req: Request): boolean {
  const origin = req.headers.get('origin');
  if (!origin) return true;
  const config = getPlatformConfig();
  if (config.security.allowedOrigins.includes(origin)) return true;
  try {
    return new URL(origin).origin === new URL(req.url).origin;
  } catch {
    return false;
  }
}

export function clientKey(req: Request): string {
  const forwarded = req.headers.get('x-forwarded-for');
  if (forwarded) return forwarded.split(',')[0]?.trim() || 'unknown';
  return req.headers.get('x-real-ip') || 'local';
}

type Bucket = { count: number; resetAt: number };
const buckets = new Map<string, Bucket>();

export function rateLimit(
  key: string,
  limit: number,
  windowMs = 60_000
): { ok: boolean; remaining: number } {
  const now = Date.now();
  const current = buckets.get(key);
  if (!current || current.resetAt <= now) {
    buckets.set(key, { count: 1, resetAt: now + windowMs });
    return { ok: true, remaining: limit - 1 };
  }
  current.count += 1;
  const remaining = Math.max(0, limit - current.count);
  return { ok: current.count <= limit, remaining };
}

export function resetRateLimits(): void {
  buckets.clear();
}

const SAFE_PRESET = /^(7d|14d|30d|90d|all)?$/;
const SAFE_DATE = /^\d{4}-\d{2}-\d{2}$/;
const SAFE_TOKEN = /^[a-z0-9_-]{0,64}$/i;

export function validateQueryToken(
  value: string | null,
  kind: 'preset' | 'date' | 'token'
): boolean {
  if (value == null || value === '') return true;
  if (kind === 'preset') return SAFE_PRESET.test(value);
  if (kind === 'date') return SAFE_DATE.test(value);
  return SAFE_TOKEN.test(value);
}

export function audit(event: string, fields: Record<string, unknown>): void {
  log('info', `audit.${event}`, fields);
}

export const PRIVACY_RULES = {
  noUtteranceFields: true,
  noTranscriptLogs: true,
  consentBeforeMemory: true,
  forgetMustComplete: true,
  analyticsAnonymous: true,
} as const;
