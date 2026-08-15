import type { ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Spinner } from '@/components/ui/spinner';
import { cn } from '@/lib/shadcn/utils';

type PageStateKind =
  | 'loading'
  | 'empty'
  | 'offline'
  | 'no-results'
  | 'permission'
  | 'error'
  | 'maintenance';

const COPY: Record<PageStateKind, { title: string; body: string }> = {
  loading: { title: 'Loading', body: 'Fetching the latest state.' },
  empty: {
    title: 'Nothing here yet',
    body: 'This surface is empty. Take the first step when ready.',
  },
  offline: {
    title: 'You are offline',
    body: 'Reconnect to continue. Last good state stays on screen when available.',
  },
  'no-results': { title: 'No results', body: 'Nothing matches these filters.' },
  permission: { title: 'Permission denied', body: 'This role cannot open this surface.' },
  error: {
    title: 'Temporarily unavailable',
    body: 'Try again. Last good state remains when we have it.',
  },
  maintenance: {
    title: 'Under maintenance',
    body: 'This instrument is paused. The hall still works.',
  },
};

function PageState({
  kind,
  title,
  body,
  action,
  className,
}: {
  kind: PageStateKind;
  title?: string;
  body?: string;
  action?: ReactNode;
  className?: string;
}) {
  const copy = COPY[kind];
  const role = kind === 'error' || kind === 'offline' || kind === 'permission' ? 'alert' : 'status';

  return (
    <div
      role={role}
      data-slot="page-state"
      data-kind={kind}
      className={cn(
        'border-border bg-card text-card-foreground rounded-[var(--salora-radius-panel)] border p-8 text-center',
        className
      )}
    >
      {kind === 'loading' ? (
        <div className="mb-4 flex justify-center">
          <Spinner />
        </div>
      ) : null}
      <p className="text-lg font-semibold">{title ?? copy.title}</p>
      <p className="text-muted-foreground mt-2 text-sm">{body ?? copy.body}</p>
      {action ? <div className="mt-4 flex justify-center">{action}</div> : null}
    </div>
  );
}

function MetricSkeletonGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="grid gap-4 sm:grid-cols-3" aria-busy="true" aria-label="Loading metrics">
      {Array.from({ length: count }, (_, key) => (
        <Skeleton key={key} className="h-28" />
      ))}
    </div>
  );
}

function RetryAction({ onClick, label = 'Retry' }: { onClick: () => void; label?: string }) {
  return (
    <Button type="button" variant="outline" onClick={onClick}>
      {label}
    </Button>
  );
}

export { PageState, MetricSkeletonGrid, RetryAction };
export type { PageStateKind };
