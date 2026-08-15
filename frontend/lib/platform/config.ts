/**
 * Typed platform configuration. Single env parse for the Next process.
 * Branding stays in app-config.ts. Telephony flags stay in the Python worker.
 */

export type EnvironmentProfile = 'development' | 'staging' | 'production';

export type ProviderName = 'livekit' | 'murf' | 'deepgram' | 'google' | 'openai';

export type FeatureFlags = {
  analytics: boolean;
  enterprise: boolean;
  learning: boolean;
  studio: boolean;
  marketplace: boolean;
  developers: boolean;
};

export type PlatformConfig = {
  profile: EnvironmentProfile;
  auth: {
    required: boolean;
    secret: string;
    accessTtlSeconds: number;
    refreshTtlSeconds: number;
    cookieName: string;
    refreshCookieName: string;
  };
  livekit: {
    url: string;
    apiKey: string;
    apiSecret: string;
    agentName: string;
  };
  flags: FeatureFlags;
  security: {
    allowedOrigins: string[];
    tokenRatePerMinute: number;
    apiRatePerMinute: number;
  };
  providers: Record<ProviderName, { configured: boolean }>;
};

const PROFILES: readonly EnvironmentProfile[] = ['development', 'staging', 'production'];

function read(name: string, fallback = ''): string {
  const value = process.env[name];
  return typeof value === 'string' ? value.trim() : fallback;
}

function readBool(name: string, fallback: boolean): boolean {
  const raw = read(name);
  if (!raw) return fallback;
  return !['0', 'false', 'no', 'off'].includes(raw.toLowerCase());
}

function readInt(name: string, fallback: number): number {
  const parsed = Number(read(name));
  return Number.isFinite(parsed) && parsed > 0 ? Math.floor(parsed) : fallback;
}

function readProfile(): EnvironmentProfile {
  const explicit = read('SALORA_PROFILE') as EnvironmentProfile;
  if (PROFILES.includes(explicit)) return explicit;
  if (process.env.NODE_ENV === 'production') return 'production';
  return 'development';
}

function parseOrigins(raw: string): string[] {
  return raw
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

let cached: PlatformConfig | null = null;

export function getPlatformConfig(options?: { reload?: boolean }): PlatformConfig {
  if (cached && !options?.reload) return cached;

  const profile = readProfile();
  const livekitUrl = read('LIVEKIT_URL');
  const livekitKey = read('LIVEKIT_API_KEY');
  const livekitSecret = read('LIVEKIT_API_SECRET');

  cached = {
    profile,
    auth: {
      required: readBool('AUTH_REQUIRED', false),
      secret: read('SALORA_AUTH_SECRET') || read('SESSION_SECRET'),
      accessTtlSeconds: readInt('AUTH_ACCESS_TTL_SECONDS', 900),
      refreshTtlSeconds: readInt('AUTH_REFRESH_TTL_SECONDS', 60 * 60 * 24 * 14),
      cookieName: read('AUTH_COOKIE_NAME', 'salora_session'),
      refreshCookieName: read('AUTH_REFRESH_COOKIE_NAME', 'salora_refresh'),
    },
    livekit: {
      url: livekitUrl,
      apiKey: livekitKey,
      apiSecret: livekitSecret,
      agentName: read('AGENT_NAME'),
    },
    flags: {
      analytics: readBool('FEATURE_ANALYTICS', true),
      enterprise: readBool('FEATURE_ENTERPRISE', true),
      learning: readBool('FEATURE_LEARNING', true),
      studio: readBool('FEATURE_STUDIO', false),
      marketplace: readBool('FEATURE_MARKETPLACE', false),
      developers: readBool('FEATURE_DEVELOPERS', false),
    },
    security: {
      allowedOrigins: parseOrigins(read('ALLOWED_ORIGINS')),
      tokenRatePerMinute: readInt('RATE_LIMIT_TOKEN_PER_MIN', 30),
      apiRatePerMinute: readInt('RATE_LIMIT_API_PER_MIN', 120),
    },
    providers: {
      livekit: { configured: Boolean(livekitUrl && livekitKey && livekitSecret) },
      murf: { configured: Boolean(read('MURF_API_KEY')) },
      deepgram: { configured: Boolean(read('DEEPGRAM_API_KEY')) },
      google: { configured: Boolean(read('GOOGLE_API_KEY')) },
      openai: { configured: Boolean(read('OPENAI_API_KEY')) },
    },
  };
  return cached;
}

export function clearPlatformConfigCache(): void {
  cached = null;
}

export function publicPlatformView(config: PlatformConfig = getPlatformConfig()) {
  return {
    profile: config.profile,
    flags: config.flags,
    authRequired: config.auth.required,
    providers: Object.fromEntries(
      Object.entries(config.providers).map(([name, value]) => [name, value.configured])
    ) as Record<ProviderName, boolean>,
    livekitConfigured: config.providers.livekit.configured,
  };
}
