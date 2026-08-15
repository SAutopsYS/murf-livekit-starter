import { OS_NAV, type OsNavItem } from '@/lib/os-nav';
import { getStudioCommands } from '@/lib/studio/commands';

function getPlatformCommands(): OsCommand[] {
  return [
    {
      id: 'marketplace:open',
      label: 'Open Marketplace',
      kind: 'search',
      planned: true,
      href: '/marketplace',
      keywords: 'marketplace plugins catalog',
    },
    {
      id: 'developers:sdk',
      label: 'SDK contracts',
      kind: 'settings',
      planned: true,
      href: '/developers',
      keywords: 'sdk api developer',
    },
  ];
}

export type OsCommandKind =
  | 'navigation'
  | 'action'
  | 'search'
  | 'ai'
  | 'agent'
  | 'settings'
  | 'shortcut';

export type OsCommand = {
  id: string;
  label: string;
  hint?: string;
  kind: OsCommandKind;
  keywords?: string;
  href?: string;
  planned?: boolean;
  run?: () => void;
};

export function navToCommand(item: OsNavItem): OsCommand {
  return {
    id: `nav:${item.id}`,
    label: item.label,
    hint: item.hint,
    kind: 'navigation',
    href: item.href,
    planned: item.status === 'planned',
    keywords: `${item.id} ${item.label} ${item.hint}`,
  };
}

export function getStaticCommands(): OsCommand[] {
  const nav = OS_NAV.map(navToCommand);
  const actions: OsCommand[] = [
    {
      id: 'action:search',
      label: 'Search',
      hint: '⌘K',
      kind: 'action',
      keywords: 'search find command palette',
    },
    {
      id: 'action:theme-dark',
      label: 'Theme: Dark',
      kind: 'action',
      keywords: 'dark night theme',
    },
    {
      id: 'action:theme-light',
      label: 'Theme: Light',
      kind: 'action',
      keywords: 'light day theme',
    },
    {
      id: 'action:theme-system',
      label: 'Theme: System',
      kind: 'action',
      keywords: 'system auto theme',
    },
    {
      id: 'ai:ask',
      label: 'Ask the tutor',
      hint: 'Future AI command',
      kind: 'ai',
      planned: true,
      keywords: 'ai ask tutor',
    },
    {
      id: 'agent:handoff',
      label: 'Handoff to specialist',
      hint: 'Future agent command',
      kind: 'agent',
      planned: true,
      keywords: 'agent specialist handoff',
    },
    {
      id: 'settings:account',
      label: 'Open account settings',
      kind: 'settings',
      planned: true,
      href: '/settings',
      keywords: 'settings account profile',
    },
    {
      id: 'shortcut:home',
      label: 'Go to hall',
      hint: 'G then H',
      kind: 'shortcut',
      href: '/',
      keywords: 'home hall workspace',
    },
  ];
  return [...nav, ...actions, ...getStudioCommands(), ...getPlatformCommands()];
}

export const COMMAND_KIND_LABEL: Record<OsCommandKind, string> = {
  navigation: 'Navigation',
  action: 'Quick actions',
  search: 'Search',
  ai: 'AI commands',
  agent: 'Agent commands',
  settings: 'Settings',
  shortcut: 'Shortcuts',
};
