import { cn } from '@/lib/shadcn/utils';

function Skeleton({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="skeleton"
      className={cn('bg-muted animate-pulse rounded-[var(--salora-radius-cluster)]', className)}
      {...props}
    />
  );
}

export { Skeleton };
