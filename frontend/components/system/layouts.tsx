import type { ReactNode } from 'react';
import { cn } from '@/lib/shadcn/utils';

function AppShell({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="app-shell" className={cn('bg-background text-foreground min-h-svh', className)}>
      {children}
    </div>
  );
}

function InstrumentLayout({
  children,
  className,
  width = 'wide',
}: {
  children: ReactNode;
  className?: string;
  width?: 'wide' | 'xl';
}) {
  return (
    <AppShell>
      <main data-slot="instrument-layout" className={cn('px-4 py-6 sm:px-6 md:py-8', className)}>
        <div
          className={cn(
            'mx-auto flex w-full flex-col gap-8',
            width === 'xl' ? 'max-w-7xl' : 'max-w-6xl'
          )}
        >
          {children}
        </div>
      </main>
    </AppShell>
  );
}

function AnalyticsLayout({ children }: { children: ReactNode }) {
  return <InstrumentLayout width="wide">{children}</InstrumentLayout>;
}

function EnterpriseLayout({ children }: { children: ReactNode }) {
  return <InstrumentLayout width="xl">{children}</InstrumentLayout>;
}

function LearningLayout({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <AppShell>
      <main
        data-slot="learning-layout"
        className={cn('grid min-h-svh place-content-center', className)}
      >
        {children}
      </main>
    </AppShell>
  );
}

function SettingsLayout({ children }: { children: ReactNode }) {
  return <InstrumentLayout width="wide">{children}</InstrumentLayout>;
}

function WorkspaceLayout({ children }: { children: ReactNode }) {
  return <InstrumentLayout width="xl">{children}</InstrumentLayout>;
}

function DockLayout({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div
      data-slot="dock-layout"
      className={cn(
        'border-border bg-card/80 shadow-salora-md fixed bottom-3 left-1/2 z-[var(--salora-z-header)] flex -translate-x-1/2 items-center gap-2 rounded-[var(--salora-radius-pill)] border px-3 py-2 backdrop-blur-md',
        className
      )}
    >
      {children}
    </div>
  );
}

function FloatingLayout({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div
      data-slot="floating-layout"
      className={cn('pointer-events-none fixed inset-0 z-[var(--salora-z-sticky)]', className)}
    >
      <div className="pointer-events-auto">{children}</div>
    </div>
  );
}

export {
  AppShell,
  InstrumentLayout,
  AnalyticsLayout,
  EnterpriseLayout,
  LearningLayout,
  SettingsLayout,
  WorkspaceLayout,
  DockLayout,
  FloatingLayout,
};
