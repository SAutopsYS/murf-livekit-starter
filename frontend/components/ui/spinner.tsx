import { cn } from '@/lib/shadcn/utils';

function Spinner({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      role="status"
      aria-live="polite"
      data-slot="spinner"
      className={cn(
        'border-muted border-t-primary inline-block size-5 animate-spin rounded-full border-2',
        className
      )}
      {...props}
    >
      <span className="sr-only">Loading</span>
    </span>
  );
}

export { Spinner };
