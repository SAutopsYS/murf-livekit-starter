import { getPlatformConfig, publicPlatformView } from '@/lib/platform/config';
import { getMetricsSnapshot, heartbeat } from '@/lib/platform/observability';

const startedAt = Date.now();

export function liveness() {
  heartbeat('frontend');
  return {
    status: 'ok' as const,
    service: 'salora-os',
    uptime_ms: Date.now() - startedAt,
  };
}

export function readiness() {
  const config = getPlatformConfig();
  const livekit = config.providers.livekit.configured;
  return {
    status: livekit ? ('ready' as const) : ('degraded' as const),
    service: 'salora-os',
    checks: {
      livekit,
      auth_secret: Boolean(config.auth.secret),
    },
    platform: publicPlatformView(config),
    metrics: getMetricsSnapshot().counts,
  };
}
