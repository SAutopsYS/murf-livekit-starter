'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BuildingsIcon, ChartBarIcon, DotsThreeIcon, HouseIcon } from '@phosphor-icons/react';
import { useOs } from '@/components/os/os-provider';
import { type OsNavId, getActiveNavId, getPrimaryNav } from '@/lib/os-nav';
import { cn } from '@/lib/shadcn/utils';

const ICONS: Partial<Record<OsNavId, typeof HouseIcon>> = {
  home: HouseIcon,
  analytics: ChartBarIcon,
  enterprise: BuildingsIcon,
};

export function OsBottomNav() {
  const pathname = usePathname() ?? '/';
  const { room, setCommandOpen } = useOs();
  const active = getActiveNavId(pathname);

  if (room === 'hall') return null;

  return (
    <nav
      data-slot="os-bottom-nav"
      aria-label="Primary mobile"
      className="border-border bg-background/95 supports-[backdrop-filter]:bg-background/80 fixed inset-x-0 bottom-0 z-[var(--salora-z-header)] flex h-[var(--salora-shell-dock)] items-stretch border-t px-2 backdrop-blur-md md:hidden"
    >
      {getPrimaryNav().map((item) => {
        const Icon = ICONS[item.id] ?? HouseIcon;
        const current = active === item.id;
        return (
          <Link
            key={item.id}
            href={item.href}
            className={cn(
              'flex min-h-[var(--salora-touch)] min-w-0 flex-1 flex-col items-center justify-center gap-1 text-[11px]',
              current ? 'text-foreground' : 'text-muted-foreground'
            )}
          >
            <Icon size={20} weight="bold" />
            {item.label}
          </Link>
        );
      })}
      <button
        type="button"
        className="text-muted-foreground flex min-h-[var(--salora-touch)] min-w-0 flex-1 flex-col items-center justify-center gap-1 text-[11px]"
        onClick={() => setCommandOpen(true)}
      >
        <DotsThreeIcon size={20} weight="bold" />
        More
      </button>
    </nav>
  );
}
