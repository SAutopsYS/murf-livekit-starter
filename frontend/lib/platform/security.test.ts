import { afterEach, describe, expect, it } from 'vitest';
import { ERROR_CATALOG } from '@/lib/platform/errors';
import { log, resetMetrics } from '@/lib/platform/observability';
import { rateLimit, resetRateLimits, validateQueryToken } from '@/lib/platform/security';

describe('security and errors', () => {
  afterEach(() => {
    resetRateLimits();
    resetMetrics();
  });

  it('validates query tokens and dates', () => {
    expect(validateQueryToken('7d', 'preset')).toBe(true);
    expect(validateQueryToken('2026-08-15', 'date')).toBe(true);
    expect(validateQueryToken('not a date', 'date')).toBe(false);
  });

  it('rate limits a key', () => {
    expect(rateLimit('t:1', 2).ok).toBe(true);
    expect(rateLimit('t:1', 2).ok).toBe(true);
    expect(rateLimit('t:1', 2).ok).toBe(false);
  });

  it('does not log secret-shaped fields', () => {
    const lines: string[] = [];
    const original = console.info;
    console.info = (value: string) => {
      lines.push(String(value));
    };
    log('info', 'test', { api_key: 'super-secret-value', route: 'health' });
    console.info = original;
    expect(lines.join(' ')).not.toContain('super-secret-value');
    expect(ERROR_CATALOG.RATE_LIMITED.status).toBe(429);
  });
});
