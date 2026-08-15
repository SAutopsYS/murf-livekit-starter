import type { MembershipKind, OrganizationSnapshot, PolicyKind } from '@/lib/organization/types';
import type { Role } from '@/lib/platform/rbac';

export const MEMBER_TO_ROLE: Record<MembershipKind, Role> = {
  owner: 'enterprise_admin',
  administrator: 'enterprise_admin',
  manager: 'teacher',
  teacher: 'teacher',
  parent: 'parent',
  student: 'student',
  developer: 'developer',
  guest: 'guest',
  observer: 'guest',
};

export function emptyOrganization(): OrganizationSnapshot {
  return {
    organization: null,
    workspaces: [],
    members: [],
    isolation: 'none',
  };
}

export function createOrganization(name: string, owner: string): OrganizationSnapshot {
  const slug = name.toLowerCase().replace(/\s+/g, '-').slice(0, 48);
  const id = `org:${slug}`;
  return {
    organization: {
      id,
      name,
      slug,
      owner,
      kind: 'organization',
      plan: 'standard',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    workspaces: [
      {
        id: `ws:${slug}:enterprise`,
        organizationId: id,
        name: 'Enterprise',
        kind: 'enterprise',
        owner,
      },
    ],
    members: [{ subject: owner, membership: 'owner', role: 'enterprise_admin', status: 'active' }],
    isolation: 'organization',
  };
}

export function roleForMembership(kind: MembershipKind): Role {
  return MEMBER_TO_ROLE[kind];
}

export const POLICY_KINDS: PolicyKind[] = [
  'ai',
  'learning',
  'voice',
  'security',
  'retention',
  'marketplace',
  'plugin',
  'studio',
  'whiteboard',
];
