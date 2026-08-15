export type OsNavStatus = 'live' | 'planned';
export type OsRoom = 'hall' | 'instrument';
export type OsNavId =
  | 'home'
  | 'workspace'
  | 'learning'
  | 'analytics'
  | 'enterprise'
  | 'settings'
  | 'studio'
  | 'marketplace'
  | 'developers';

export type OsNavItem = {
  id: OsNavId;
  label: string;
  href: string;
  status: OsNavStatus;
  /** Shown in top/bottom chrome. Command still lists the rest. */
  primary?: boolean;
  /** Same destination as another live item — command only. */
  alias?: boolean;
  hint: string;
};

export const OS_NAV: OsNavItem[] = [
  {
    id: 'home',
    label: 'Home',
    href: '/',
    status: 'live',
    primary: true,
    hint: 'Enter the hall',
  },
  {
    id: 'workspace',
    label: 'Workspace',
    href: '/',
    status: 'live',
    alias: true,
    hint: 'Voice lives in the workspace',
  },
  {
    id: 'learning',
    label: 'Learning',
    href: '/learning',
    status: 'planned',
    hint: 'Missions arrive in a later phase',
  },
  {
    id: 'analytics',
    label: 'Analytics',
    href: '/analytics',
    status: 'live',
    primary: true,
    hint: 'Privacy-safe call metrics',
  },
  {
    id: 'enterprise',
    label: 'Enterprise',
    href: '/enterprise',
    status: 'live',
    primary: true,
    hint: 'Control center',
  },
  {
    id: 'settings',
    label: 'Settings',
    href: '/settings',
    status: 'planned',
    hint: 'Preferences — not built yet',
  },
  {
    id: 'studio',
    label: 'Studio',
    href: '/studio',
    status: 'planned',
    hint: 'AI Studio — architecture ready, no editor yet',
  },
  {
    id: 'marketplace',
    label: 'Marketplace',
    href: '/marketplace',
    status: 'planned',
    hint: 'Plugin catalog — architecture ready, no storefront',
  },
  {
    id: 'developers',
    label: 'Developers',
    href: '/developers',
    status: 'planned',
    hint: 'SDK contracts — architecture ready, no portal UI',
  },
];

export function getPrimaryNav() {
  return OS_NAV.filter((item) => item.primary && !item.alias);
}

export function getCommandNav() {
  return OS_NAV;
}

export function getOsRoom(pathname: string): OsRoom {
  return pathname === '/' ? 'hall' : 'instrument';
}

export function getActiveNavId(pathname: string): OsNavId {
  if (pathname.startsWith('/analytics')) return 'analytics';
  if (pathname.startsWith('/enterprise')) return 'enterprise';
  if (pathname.startsWith('/learning')) return 'learning';
  if (pathname.startsWith('/settings')) return 'settings';
  if (pathname.startsWith('/studio')) return 'studio';
  if (pathname.startsWith('/marketplace')) return 'marketplace';
  if (pathname.startsWith('/developers')) return 'developers';
  return 'home';
}

export function getNavItem(id: OsNavId) {
  return OS_NAV.find((item) => item.id === id);
}
