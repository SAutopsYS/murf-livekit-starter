/**
 * Session + JWT + refresh. No login UI.
 * Anonymous voice remains first-class. SSO / OAuth / passkeys are typed providers.
 */
import { SignJWT, jwtVerify } from 'jose';
import { type PlatformConfig, getPlatformConfig } from '@/lib/platform/config';
import { type Permission, type Role, can, isRole } from '@/lib/platform/rbac';

export type AuthProviderKind = 'session' | 'jwt' | 'sso' | 'oauth' | 'passkey';

export type OrganizationRef = {
  id: string;
  name: string;
};

export type PlatformSession = {
  subject: string;
  role: Role;
  organization: OrganizationRef | null;
  provider: AuthProviderKind;
  anonymous: boolean;
  issuedAt: number;
  expiresAt: number;
};

export type TokenPair = {
  accessToken: string;
  refreshToken: string;
  session: PlatformSession;
};

export type FutureAuthProvider = {
  kind: AuthProviderKind;
  enabled: boolean;
  note: string;
};

const encoder = new TextEncoder();

export function futureAuthProviders(): FutureAuthProvider[] {
  return [
    { kind: 'session', enabled: true, note: 'Cookie session via SALORA_AUTH_SECRET.' },
    { kind: 'jwt', enabled: true, note: 'Bearer access token. 15m default.' },
    {
      kind: 'sso',
      enabled: false,
      note: 'Enterprise SSO plugs in as a provider. Not a second auth stack.',
    },
    { kind: 'oauth', enabled: false, note: 'OAuth identity maps onto Role + OrganizationRef.' },
    { kind: 'passkey', enabled: false, note: 'WebAuthn replaces password. Same session type.' },
  ];
}

export function anonymousSession(ttlSeconds = 900): PlatformSession {
  const issuedAt = Math.floor(Date.now() / 1000);
  return {
    subject: `anon_${issuedAt}`,
    role: 'anonymous',
    organization: null,
    provider: 'jwt',
    anonymous: true,
    issuedAt,
    expiresAt: issuedAt + ttlSeconds,
  };
}

export function guestSession(ttlSeconds = 900): PlatformSession {
  const issuedAt = Math.floor(Date.now() / 1000);
  return {
    subject: `guest_${issuedAt}`,
    role: 'guest',
    organization: null,
    provider: 'session',
    anonymous: false,
    issuedAt,
    expiresAt: issuedAt + ttlSeconds,
  };
}

function secretKey(config: PlatformConfig): Uint8Array | null {
  if (!config.auth.secret) return null;
  return encoder.encode(config.auth.secret);
}

export async function signAccessToken(
  session: PlatformSession,
  config: PlatformConfig = getPlatformConfig()
): Promise<string | null> {
  const key = secretKey(config);
  if (!key) return null;
  return new SignJWT({
    role: session.role,
    org: session.organization,
    anon: session.anonymous,
    provider: session.provider,
  })
    .setProtectedHeader({ alg: 'HS256', typ: 'JWT' })
    .setSubject(session.subject)
    .setIssuedAt(session.issuedAt)
    .setExpirationTime(session.expiresAt)
    .setIssuer('salora-os')
    .sign(key);
}

export async function signRefreshToken(
  session: PlatformSession,
  config: PlatformConfig = getPlatformConfig()
): Promise<string | null> {
  const key = secretKey(config);
  if (!key) return null;
  const exp = session.issuedAt + config.auth.refreshTtlSeconds;
  return new SignJWT({ typ: 'refresh', role: session.role, sub_session: session.subject })
    .setProtectedHeader({ alg: 'HS256', typ: 'JWT' })
    .setSubject(session.subject)
    .setIssuedAt(session.issuedAt)
    .setExpirationTime(exp)
    .setIssuer('salora-os')
    .sign(key);
}

export async function issueTokenPair(
  input: { role: Role; subject?: string; organization?: OrganizationRef | null },
  config: PlatformConfig = getPlatformConfig()
): Promise<TokenPair | null> {
  const issuedAt = Math.floor(Date.now() / 1000);
  const session: PlatformSession = {
    subject: input.subject ?? `user_${issuedAt}`,
    role: input.role,
    organization: input.organization ?? null,
    provider: 'jwt',
    anonymous: input.role === 'anonymous',
    issuedAt,
    expiresAt: issuedAt + config.auth.accessTtlSeconds,
  };
  const accessToken = await signAccessToken(session, config);
  const refreshToken = await signRefreshToken(session, config);
  if (!accessToken || !refreshToken) return null;
  return { accessToken, refreshToken, session };
}

export async function verifyAccessToken(
  token: string,
  config: PlatformConfig = getPlatformConfig()
): Promise<PlatformSession | null> {
  const key = secretKey(config);
  if (!key) return null;
  try {
    const { payload } = await jwtVerify(token, key, { issuer: 'salora-os' });
    if (payload.typ === 'refresh') return null;
    if (typeof payload.sub !== 'string' || !isRole(payload.role)) return null;
    return {
      subject: payload.sub,
      role: payload.role,
      organization: (payload.org as OrganizationRef | null) ?? null,
      provider: (payload.provider as AuthProviderKind) || 'jwt',
      anonymous: Boolean(payload.anon),
      issuedAt: typeof payload.iat === 'number' ? payload.iat : 0,
      expiresAt: typeof payload.exp === 'number' ? payload.exp : 0,
    };
  } catch {
    return null;
  }
}

export async function verifyRefreshToken(
  token: string,
  config: PlatformConfig = getPlatformConfig()
): Promise<PlatformSession | null> {
  const key = secretKey(config);
  if (!key) return null;
  try {
    const { payload } = await jwtVerify(token, key, { issuer: 'salora-os' });
    if (payload.typ !== 'refresh') return null;
    if (typeof payload.sub !== 'string' || !isRole(payload.role)) return null;
    return {
      subject: payload.sub,
      role: payload.role,
      organization: null,
      provider: 'jwt',
      anonymous: payload.role === 'anonymous',
      issuedAt: Math.floor(Date.now() / 1000),
      expiresAt: Math.floor(Date.now() / 1000) + config.auth.accessTtlSeconds,
    };
  } catch {
    return null;
  }
}

function readCookie(header: string | null, name: string): string | null {
  if (!header) return null;
  const parts = header.split(';');
  for (const part of parts) {
    const [key, ...rest] = part.trim().split('=');
    if (key === name) return decodeURIComponent(rest.join('='));
  }
  return null;
}

export async function resolveSession(
  req: Request,
  config: PlatformConfig = getPlatformConfig()
): Promise<PlatformSession | null> {
  const header = req.headers.get('authorization');
  const bearer = header?.startsWith('Bearer ') ? header.slice(7).trim() : '';
  if (bearer) {
    const fromBearer = await verifyAccessToken(bearer, config);
    if (fromBearer) return fromBearer;
  }
  const cookie = readCookie(req.headers.get('cookie'), config.auth.cookieName);
  if (cookie) {
    const fromCookie = await verifyAccessToken(cookie, config);
    if (fromCookie) return fromCookie;
  }
  return null;
}

export type AuthorizeResult =
  | { ok: true; session: PlatformSession }
  | { ok: false; status: 401 | 403; message: string };

const OPEN_WHEN_AUTH_OPTIONAL: readonly Permission[] = [
  'analytics.read',
  'analytics.export',
  'enterprise.read',
  'enterprise.export',
  'learning.read',
];

export async function authorizeRequest(
  req: Request,
  permission: Permission,
  config: PlatformConfig = getPlatformConfig()
): Promise<AuthorizeResult> {
  const resolved = await resolveSession(req, config);

  if (!config.auth.required) {
    const session = resolved ?? guestSession();
    if (OPEN_WHEN_AUTH_OPTIONAL.includes(permission) || can(session.role, permission)) {
      return { ok: true, session };
    }
  }

  if (!resolved) {
    return { ok: false, status: 401, message: 'Authentication required.' };
  }
  if (!can(resolved.role, permission)) {
    return { ok: false, status: 403, message: 'This role cannot use this instrument.' };
  }
  return { ok: true, session: resolved };
}
