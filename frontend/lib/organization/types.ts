import type { Role } from '@/lib/platform/rbac';

export type TenantKind =
  | 'tenant'
  | 'organization'
  | 'workspace'
  | 'department'
  | 'school'
  | 'classroom'
  | 'team'
  | 'project'
  | 'group'
  | 'division';

export type WorkspaceKind =
  | 'personal'
  | 'organization'
  | 'classroom'
  | 'team'
  | 'enterprise'
  | 'shared';

export type MembershipKind =
  | 'owner'
  | 'administrator'
  | 'manager'
  | 'teacher'
  | 'parent'
  | 'student'
  | 'developer'
  | 'guest'
  | 'observer';

export type PolicyKind =
  | 'ai'
  | 'learning'
  | 'voice'
  | 'security'
  | 'retention'
  | 'marketplace'
  | 'plugin'
  | 'studio'
  | 'whiteboard';

export type OrganizationRecord = {
  id: string;
  name: string;
  slug: string;
  owner: string;
  kind: TenantKind;
  plan: string;
  createdAt: string;
  updatedAt: string;
};

export type WorkspaceRecord = {
  id: string;
  organizationId: string;
  name: string;
  kind: WorkspaceKind;
  owner: string;
};

export type MembershipRecord = {
  subject: string;
  membership: MembershipKind;
  role: Role;
  status: 'invited' | 'active' | 'suspended' | 'removed';
};

export type OrganizationSnapshot = {
  organization: OrganizationRecord | null;
  workspaces: WorkspaceRecord[];
  members: MembershipRecord[];
  isolation: 'none' | 'personal' | 'organization';
};
