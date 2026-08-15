'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BellIcon, MagnifyingGlassIcon } from '@phosphor-icons/react';
import { ThemeToggle } from '@/components/app/theme-toggle';
import { useOs } from '@/components/os/os-provider';
import { FloatingPanel, PageState } from '@/components/system';
import { Avatar } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { IconButton } from '@/components/ui/icon-button';
import { getActiveNavId, getNavItem, getPrimaryNav } from '@/lib/os-nav';
import { cn } from '@/lib/shadcn/utils';

export function OsTopBar() {
  const pathname = usePathname() ?? '/';
  const { brand, room, setCommandOpen } = useOs();
  const [notifyOpen, setNotifyOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const active = getActiveNavId(pathname);
  const context = getNavItem(active);
  const primary = getPrimaryNav();

  return (
    <header
      data-slot="os-top-bar"
      className={cn(
        'border-border/70 z-[var(--salora-z-header)] flex h-[var(--salora-shell-top)] items-center gap-3 border-b px-3 sm:px-5',
        room === 'hall'
          ? 'bg-background/55 absolute inset-x-0 top-0 backdrop-blur-md'
          : 'bg-background/90 sticky top-0 backdrop-blur-md'
      )}
    >
      <Link href="/" className="flex min-w-0 items-center gap-2.5">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={brand.logo}
          alt={`${brand.companyName} Logo`}
          className="block size-7 dark:hidden"
        />
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={brand.logoDark ?? brand.logo}
          alt={`${brand.companyName} Logo`}
          className="hidden size-7 dark:block"
        />
        <span className="text-foreground truncate text-sm font-semibold tracking-tight">
          {brand.companyName}
        </span>
      </Link>

      <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
        {primary.map((item) => (
          <Link
            key={item.id}
            href={item.href}
            className={cn(
              'rounded-[var(--salora-radius-pill)] px-3 py-1.5 text-sm transition-colors',
              active === item.id
                ? 'bg-foreground text-background'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground'
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>

      <p className="text-muted-foreground hidden font-mono text-[11px] font-bold tracking-[0.14em] uppercase xl:block">
        {room === 'hall' ? 'Hall · Voice' : (context?.label ?? 'Instrument')}
      </p>

      <div className="ml-auto flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="hidden min-h-[var(--salora-touch)] sm:inline-flex"
          onClick={() => setCommandOpen(true)}
        >
          <MagnifyingGlassIcon size={16} weight="bold" />
          Search
          <kbd className="text-muted-foreground ml-1 font-mono text-[10px]">⌘K</kbd>
        </Button>
        <IconButton
          type="button"
          variant="outline"
          className="sm:hidden"
          aria-label="Open search"
          onClick={() => setCommandOpen(true)}
        >
          <MagnifyingGlassIcon size={16} weight="bold" />
        </IconButton>

        <div className="relative">
          <IconButton
            type="button"
            variant="ghost"
            aria-label="Notifications"
            aria-expanded={notifyOpen}
            onClick={() => {
              setNotifyOpen((open) => !open);
              setProfileOpen(false);
            }}
          >
            <BellIcon size={16} weight="bold" />
          </IconButton>
          {notifyOpen ? (
            <FloatingPanel className="absolute top-12 right-0 z-[var(--salora-z-overlay)] w-72">
              <PageState kind="empty" title="No notifications" body="Alerts will land here." />
            </FloatingPanel>
          ) : null}
        </div>

        <div className="relative">
          <button
            type="button"
            className="rounded-[var(--salora-radius-pill)]"
            aria-label="Profile"
            aria-expanded={profileOpen}
            onClick={() => {
              setProfileOpen((open) => !open);
              setNotifyOpen(false);
            }}
          >
            <Avatar initials="S" alt="Guest profile" className="size-8" />
          </button>
          {profileOpen ? (
            <FloatingPanel className="absolute top-12 right-0 z-[var(--salora-z-overlay)] w-56">
              <p className="text-sm font-medium">Guest</p>
              <p className="text-muted-foreground mt-1 text-xs">
                Auth arrives later. Session stays local.
              </p>
            </FloatingPanel>
          ) : null}
        </div>

        <ThemeToggle className="w-auto shrink-0" />
      </div>
    </header>
  );
}
