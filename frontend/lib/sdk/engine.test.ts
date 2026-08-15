import { describe, expect, it } from 'vitest';
import { buildSdkSnapshot } from '@/lib/sdk/engine';

describe('sdk', () => {
  it('exposes v1 modules without a portal UI', () => {
    const snap = buildSdkSnapshot();
    expect(snap.version).toBe('v1');
    expect(snap.modules).toContain('voice');
    expect(snap.portalUi).toBe(false);
    expect(snap.webhooks).toContain('LearningUpdated');
  });
});
