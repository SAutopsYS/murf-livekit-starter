import { afterEach, describe, expect, it } from 'vitest';
import {
  authorizeRequest,
  issueTokenPair,
  verifyAccessToken,
  verifyRefreshToken,
} from '@/lib/platform/auth';
import { clearPlatformConfigCache, getPlatformConfig } from '@/lib/platform/config';

describe('auth tokens', () => {
  afterEach(() => {
    delete process.env.SALORA_AUTH_SECRET;
    delete process.env.AUTH_REQUIRED;
    clearPlatformConfigCache();
  });

  it('issues and verifies access plus refresh when a secret exists', async () => {
    process.env.SALORA_AUTH_SECRET = 'test-secret-for-platform-jwt';
    clearPlatformConfigCache();
    const config = getPlatformConfig({ reload: true });
    const pair = await issueTokenPair({ role: 'teacher', subject: 't1' }, config);
    expect(pair).not.toBeNull();
    const access = await verifyAccessToken(pair!.accessToken, config);
    const refresh = await verifyRefreshToken(pair!.refreshToken, config);
    expect(access?.role).toBe('teacher');
    expect(refresh?.role).toBe('teacher');
  });

  it('allows instrument reads when AUTH_REQUIRED is off', async () => {
    process.env.AUTH_REQUIRED = 'false';
    clearPlatformConfigCache();
    const req = new Request('http://localhost/api/analytics');
    const gate = await authorizeRequest(req, 'analytics.read');
    expect(gate.ok).toBe(true);
  });
});
