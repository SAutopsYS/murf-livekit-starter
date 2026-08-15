import { describe, expect, it } from 'vitest';
import { createOrganization, roleForMembership } from '@/lib/organization/engine';

describe('organization', () => {
  it('maps membership onto existing RBAC', () => {
    const snap = createOrganization('North School', 'admin');
    expect(snap.isolation).toBe('organization');
    expect(snap.members[0]?.role).toBe('enterprise_admin');
    expect(roleForMembership('teacher')).toBe('teacher');
    expect(roleForMembership('observer')).toBe('guest');
  });
});
