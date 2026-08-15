import type { ComponentProps, ReactNode } from 'react';
import { PageHeader, SectionHeader } from '@/components/system';
import { cn } from '@/lib/shadcn/utils';

function OsPage({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="os-page" className={cn('flex flex-col gap-6 sm:gap-8', className)}>
      {children}
    </div>
  );
}

function OsPageToolbar({
  children,
  className,
  ...props
}: {
  children: ReactNode;
  className?: string;
} & ComponentProps<'div'>) {
  return (
    <div
      data-slot="os-page-toolbar"
      className={cn(
        'border-border bg-card flex flex-wrap items-end gap-3 rounded-[var(--salora-radius-cluster)] border p-4',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

function OsPageContent({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="os-page-content" className={cn('flex flex-col gap-6', className)}>
      {children}
    </div>
  );
}

function OsPageWidgets({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="os-page-widgets" className={cn('min-w-0', className)}>
      {children}
    </div>
  );
}

function OsPageActions({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div data-slot="os-page-actions" className={cn('flex flex-wrap items-center gap-2', className)}>
      {children}
    </div>
  );
}

function OsPageFooter({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <footer
      data-slot="os-page-footer"
      className={cn('text-muted-foreground border-border border-t pt-4 text-sm', className)}
    >
      {children}
    </footer>
  );
}

export {
  OsPage,
  PageHeader as OsPageHeader,
  SectionHeader as OsPageSection,
  OsPageToolbar,
  OsPageContent,
  OsPageWidgets,
  OsPageActions,
  OsPageFooter,
};
