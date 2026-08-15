import { describe, expect, it } from 'vitest';
import {
  can,
  featureAllowed,
  permissionsFor,
  policyVoiceAnonymous,
  roleFromEnterpriseUi,
} from '@/lib/platform/rbac';

describe('RBAC', () => {
  it('keeps anonymous voice first-class and blocks instruments', () => {
    expect(can('anonymous', 'voice.session')).toBe(true);
    expect(can('anonymous', 'analytics.read')).toBe(false);
    expect(policyVoiceAnonymous().allow).toBe(true);
  });

  it('maps enterprise UI roles without a second matrix', () => {
    expect(roleFromEnterpriseUi('admin')).toBe('enterprise_admin');
    expect(roleFromEnterpriseUi('teacher')).toBe('teacher');
    expect(can('enterprise_admin', 'enterprise.admin')).toBe(true);
    expect(can('parent', 'analytics.export')).toBe(false);
  });

  it('gates future studio and marketplace', () => {
    const flags = {
      analytics: true,
      enterprise: true,
      learning: true,
      studio: false,
      marketplace: false,
      developers: false,
    };
    expect(featureAllowed('operator', 'studio', flags)).toBe(false);
    expect(permissionsFor('developer')).toContain('developer.sdk');
  });
});
