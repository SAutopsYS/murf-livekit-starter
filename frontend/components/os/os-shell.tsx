'use client';

import type { ReactNode } from 'react';
import { OsBottomNav } from '@/components/os/os-bottom-nav';
import { OsCommandPalette } from '@/components/os/os-command-palette';
import { type OsBrand, OsProvider, useOs } from '@/components/os/os-provider';
import { OsTopBar } from '@/components/os/os-top-bar';
import { OsWorkspace } from '@/components/os/os-workspace';
import { PlatformErrorBoundary } from '@/components/platform/error-boundary';
import { Toaster } from '@/components/ui/sonner';
import { cn } from '@/lib/shadcn/utils';

function OsShellFrame({ children }: { children: ReactNode }) {
  const { room } = useOs();

  return (
    <div
      data-slot="os-shell"
      data-room={room}
      className={cn(
        'bg-background text-foreground flex min-h-svh flex-col',
        room === 'hall' && 'relative'
      )}
    >
      <OsTopBar />
      <OsWorkspace className={cn(room === 'instrument' && 'pb-[var(--salora-shell-dock)] md:pb-0')}>
        <PlatformErrorBoundary>{children}</PlatformErrorBoundary>
      </OsWorkspace>
      <OsBottomNav />
      <OsCommandPalette />
      <Toaster position="top-center" />
    </div>
  );
}

export function OsShell({ brand, children }: { brand: OsBrand; children: ReactNode }) {
  return (
    <OsProvider brand={brand}>
      <OsShellFrame>{children}</OsShellFrame>
    </OsProvider>
  );
}
