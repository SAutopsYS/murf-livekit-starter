import { NextResponse } from 'next/server';
import { type PlatformSession, authorizeRequest } from '@/lib/platform/auth';
import { getPlatformConfig } from '@/lib/platform/config';
import { platformError, reportError } from '@/lib/platform/errors';
import { endSpan, log, recordMetric, startSpan } from '@/lib/platform/observability';
import type { Permission } from '@/lib/platform/rbac';
import { assertSameOrigin, audit, clientKey, rateLimit } from '@/lib/platform/security';

export async function platformRoute(
  req: Request,
  options: {
    permission?: Permission;
    rateLimit?: 'token' | 'api';
    csrf?: boolean;
    metric?: string;
  },
  handler: (ctx: { session: PlatformSession | null }) => Promise<Response>
): Promise<Response> {
  const config = getPlatformConfig();
  const span = startSpan(options.metric ?? 'api.request');
  const key = clientKey(req);

  if (options.csrf && !assertSameOrigin(req)) {
    const error = platformError('CSRF');
    recordMetric('api.error', 1, { code: error.code });
    endSpan(span, false);
    return NextResponse.json({ error: true, message: error.userMessage }, { status: error.status });
  }

  if (options.rateLimit) {
    const limit =
      options.rateLimit === 'token'
        ? config.security.tokenRatePerMinute
        : config.security.apiRatePerMinute;
    const limited = rateLimit(`${options.rateLimit}:${key}`, limit);
    if (!limited.ok) {
      const error = platformError('RATE_LIMITED');
      recordMetric('api.error', 1, { code: error.code });
      endSpan(span, false);
      return NextResponse.json(
        { error: true, message: error.userMessage },
        { status: error.status }
      );
    }
  }

  let session: PlatformSession | null = null;
  if (options.permission) {
    const gate = await authorizeRequest(req, options.permission, config);
    if (!gate.ok) {
      const error = platformError(gate.status === 401 ? 'AUTH_REQUIRED' : 'AUTH_FORBIDDEN');
      recordMetric('api.error', 1, { code: error.code });
      endSpan(span, false);
      return NextResponse.json(
        { error: true, message: error.userMessage },
        { status: error.status }
      );
    }
    session = gate.session;
  }

  try {
    const response = await handler({ session });
    const duration = endSpan(span, response.ok);
    recordMetric('api.request', 1, { route: options.metric ?? 'api' });
    recordMetric('api.latency_ms', duration, { route: options.metric ?? 'api' });
    log('info', 'api.request', {
      route: options.metric ?? 'api',
      status: response.status,
      duration_ms: duration,
      role: session?.role ?? 'none',
    });
    if (options.permission) {
      audit('api.access', { route: options.metric ?? 'api', role: session?.role ?? 'none' });
    }
    return response;
  } catch (error) {
    reportError(error, { route: options.metric ?? 'api' });
    endSpan(span, false);
    recordMetric('api.error', 1, { route: options.metric ?? 'api' });
    const mapped = platformError('NETWORK');
    return NextResponse.json(
      { error: true, message: mapped.userMessage },
      { status: mapped.status }
    );
  }
}
