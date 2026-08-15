import type { ReactNode } from 'react';
import { DockLayout, FloatingLayout } from '@/components/system';
import { cn } from '@/lib/shadcn/utils';

function OsPrimaryWorkspace({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="os-primary-workspace" className={cn('min-h-0 min-w-0 flex-1', className)}>
      {children}
    </div>
  );
}

function OsSecondaryPanel({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <aside
      data-slot="os-secondary-panel"
      className={cn('border-border hidden w-80 shrink-0 border-l xl:block', className)}
    >
      {children}
    </aside>
  );
}

function OsContextPanel({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <aside
      data-slot="os-context-panel"
      className={cn('border-border hidden w-72 shrink-0 border-l 2xl:block', className)}
    >
      {children}
    </aside>
  );
}

function OsWidgetRegion({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <section data-slot="os-widget-region" className={cn('min-w-0', className)}>
      {children}
    </section>
  );
}

function OsDockArea({ children, className }: { children: ReactNode; className?: string }) {
  return <DockLayout className={className}>{children}</DockLayout>;
}

function OsFloatingArea({ children, className }: { children: ReactNode; className?: string }) {
  return <FloatingLayout className={className}>{children}</FloatingLayout>;
}

function OsBottomSheet({
  open,
  children,
  className,
}: {
  open: boolean;
  children: ReactNode;
  className?: string;
}) {
  if (!open) return null;
  return (
    <div
      data-slot="os-bottom-sheet"
      className={cn(
        'border-border bg-card shadow-salora-lg fixed inset-x-0 bottom-0 z-[var(--salora-z-overlay)] rounded-t-[var(--salora-radius-panel)] border p-4 pb-[calc(var(--salora-shell-dock)+var(--salora-space-3))] md:hidden',
        className
      )}
    >
      {children}
    </div>
  );
}

function OsWorkspace({
  children,
  secondary,
  context,
  className,
}: {
  children: ReactNode;
  secondary?: ReactNode;
  context?: ReactNode;
  className?: string;
}) {
  return (
    <div data-slot="os-workspace" className={cn('flex min-h-0 min-w-0 flex-1', className)}>
      <OsPrimaryWorkspace>{children}</OsPrimaryWorkspace>
      {secondary}
      {context}
    </div>
  );
}

export {
  OsWorkspace,
  OsPrimaryWorkspace,
  OsSecondaryPanel,
  OsContextPanel,
  OsWidgetRegion,
  OsDockArea,
  OsFloatingArea,
  OsBottomSheet,
};
