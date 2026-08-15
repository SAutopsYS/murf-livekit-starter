/**
 * Central RBAC. Roles, permissions, policies, feature gates.
 * UI selects are not authority. Routes call can() / authorizeRequest().
 */

export const ROLES = [
  'anonymous',
  'guest',
  'student',
  'parent',
  'teacher',
  'enterprise_admin',
  'developer',
  'operator',
] as const;

export type Role = (typeof ROLES)[number];

export const PERMISSIONS = [
  'voice.session',
  'analytics.read',
  'analytics.export',
  'enterprise.read',
  'enterprise.export',
  'enterprise.admin',
  'learning.read',
  'developer.sdk',
  'marketplace.browse',
  'studio.access',
  'whiteboard.access',
  'memory_graph.read',
] as const;

export type Permission = (typeof PERMISSIONS)[number];

export type FeatureGate =
  | 'analytics'
  | 'enterprise'
  | 'learning'
  | 'studio'
  | 'marketplace'
  | 'developers';

const ROLE_PERMISSIONS: Record<Role, readonly Permission[]> = {
  anonymous: ['voice.session'],
  guest: ['voice.session'],
  student: ['voice.session', 'learning.read'],
  parent: ['voice.session', 'learning.read', 'analytics.read', 'enterprise.read'],
  teacher: [
    'voice.session',
    'learning.read',
    'analytics.read',
    'analytics.export',
    'enterprise.read',
    'studio.access',
    'whiteboard.access',
    'memory_graph.read',
  ],
  enterprise_admin: [
    'voice.session',
    'learning.read',
    'analytics.read',
    'analytics.export',
    'enterprise.read',
    'enterprise.export',
    'enterprise.admin',
    'studio.access',
    'whiteboard.access',
    'memory_graph.read',
    'marketplace.browse',
  ],
  developer: [
    'voice.session',
    'analytics.read',
    'developer.sdk',
    'learning.read',
    'studio.access',
    'memory_graph.read',
    'marketplace.browse',
  ],
  operator: PERMISSIONS,
};

const FEATURE_PERMISSION: Record<FeatureGate, Permission | null> = {
  analytics: 'analytics.read',
  enterprise: 'enterprise.read',
  learning: 'learning.read',
  studio: 'studio.access',
  marketplace: 'marketplace.browse',
  developers: 'developer.sdk',
};

const ENTERPRISE_UI_ROLES: Record<string, Role> = {
  admin: 'enterprise_admin',
  teacher: 'teacher',
  parent: 'parent',
};

export function isRole(value: unknown): value is Role {
  return typeof value === 'string' && (ROLES as readonly string[]).includes(value);
}

export function roleFromEnterpriseUi(value: string | null | undefined): Role {
  if (!value) return 'guest';
  return ENTERPRISE_UI_ROLES[value] ?? (isRole(value) ? value : 'guest');
}

export function permissionsFor(role: Role): readonly Permission[] {
  return ROLE_PERMISSIONS[role];
}

export function can(role: Role, permission: Permission): boolean {
  return ROLE_PERMISSIONS[role].includes(permission);
}

export function canAny(role: Role, permissions: readonly Permission[]): boolean {
  return permissions.some((permission) => can(role, permission));
}

export function featureAllowed(
  role: Role,
  gate: FeatureGate,
  flags: Record<FeatureGate, boolean>
): boolean {
  if (!flags[gate]) return false;
  const permission = FEATURE_PERMISSION[gate];
  if (!permission) return true;
  return can(role, permission);
}

export type PolicyDecision = {
  allow: boolean;
  reason: string;
};

export function policyVoiceAnonymous(): PolicyDecision {
  return { allow: true, reason: 'Anonymous voice sessions are a first-class product path.' };
}

export function policyInstrumentRead(role: Role, permission: Permission): PolicyDecision {
  if (can(role, permission)) {
    return { allow: true, reason: 'Role holds the instrument permission.' };
  }
  return { allow: false, reason: 'Role cannot open this instrument.' };
}
