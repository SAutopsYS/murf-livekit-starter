/**
 * Typed errors, retry/fallback, recovery, reporting.
 * Does not replace useAgentErrors (LiveKit session failures stay there).
 */
import { log } from '@/lib/platform/observability';

export type ErrorDomain = 'user' | 'developer' | 'ai' | 'voice' | 'network' | 'auth' | 'config';

export type RecoveryAction = 'retry' | 'fallback' | 'reconnect' | 'none';

export type PlatformError = {
  code: string;
  domain: ErrorDomain;
  message: string;
  userMessage: string;
  retryable: boolean;
  recovery: RecoveryAction;
  status: number;
};

export const ERROR_CATALOG = {
  AUTH_REQUIRED: {
    code: 'AUTH_REQUIRED',
    domain: 'auth',
    message: 'Authentication required.',
    userMessage: 'Sign in to open this instrument.',
    retryable: false,
    recovery: 'none',
    status: 401,
  },
  AUTH_FORBIDDEN: {
    code: 'AUTH_FORBIDDEN',
    domain: 'auth',
    message: 'Role cannot use this instrument.',
    userMessage: 'This role cannot open this surface.',
    retryable: false,
    recovery: 'none',
    status: 403,
  },
  RATE_LIMITED: {
    code: 'RATE_LIMITED',
    domain: 'user',
    message: 'Rate limit exceeded.',
    userMessage: 'Too many requests. Wait a moment.',
    retryable: true,
    recovery: 'retry',
    status: 429,
  },
  CSRF: {
    code: 'CSRF',
    domain: 'auth',
    message: 'Origin is not allowed.',
    userMessage: 'This request was blocked.',
    retryable: false,
    recovery: 'none',
    status: 403,
  },
  CONFIG_MISSING: {
    code: 'CONFIG_MISSING',
    domain: 'config',
    message: 'Required configuration is missing.',
    userMessage: 'The hall cannot connect right now.',
    retryable: false,
    recovery: 'none',
    status: 500,
  },
  NETWORK: {
    code: 'NETWORK',
    domain: 'network',
    message: 'Upstream unavailable.',
    userMessage: 'Temporarily unavailable. Try again.',
    retryable: true,
    recovery: 'retry',
    status: 503,
  },
  VOICE_SESSION: {
    code: 'VOICE_SESSION',
    domain: 'voice',
    message: 'Voice session failed.',
    userMessage: 'The session ended. Rejoin the hall when ready.',
    retryable: true,
    recovery: 'reconnect',
    status: 503,
  },
  AI_FALLBACK: {
    code: 'AI_FALLBACK',
    domain: 'ai',
    message: 'Provider failed closed.',
    userMessage: 'The host stayed on the line. Try again.',
    retryable: true,
    recovery: 'fallback',
    status: 503,
  },
  DEVELOPER: {
    code: 'DEVELOPER',
    domain: 'developer',
    message: 'Unexpected application error.',
    userMessage: 'Something broke. The last good state stays when we have it.',
    retryable: true,
    recovery: 'retry',
    status: 500,
  },
} as const satisfies Record<string, PlatformError>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export function platformError(code: ErrorCode, override?: Partial<PlatformError>): PlatformError {
  return { ...ERROR_CATALOG[code], ...override };
}

export type RetryPolicy = {
  attempts: number;
  backoffMs: number;
  retryable: (error: unknown) => boolean;
};

export const API_RETRY: RetryPolicy = {
  attempts: 2,
  backoffMs: 250,
  retryable: (error) => {
    if (error && typeof error === 'object' && 'retryable' in error) {
      return Boolean((error as PlatformError).retryable);
    }
    return true;
  },
};

export async function withRetry<T>(
  run: () => Promise<T>,
  policy: RetryPolicy = API_RETRY
): Promise<T> {
  let last: unknown;
  for (let attempt = 1; attempt <= policy.attempts; attempt += 1) {
    try {
      return await run();
    } catch (error) {
      last = error;
      if (attempt >= policy.attempts || !policy.retryable(error)) throw error;
      await new Promise((resolve) => setTimeout(resolve, policy.backoffMs * attempt));
    }
  }
  throw last;
}

export function reportError(error: unknown, context: Record<string, string> = {}): void {
  const code =
    error && typeof error === 'object' && 'code' in error ? String(error.code) : 'DEVELOPER';
  const message = error instanceof Error ? error.message : 'unknown';
  log('error', 'platform.error', {
    code,
    class: error instanceof Error ? error.name : 'unknown',
    message: message.slice(0, 160),
    ...context,
  });
}
