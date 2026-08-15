import { cn } from '@/lib/shadcn/utils';

function Avatar({
  initials,
  alt,
  className,
}: {
  initials: string;
  alt: string;
  className?: string;
}) {
  return (
    <span
      role="img"
      aria-label={alt}
      data-slot="avatar"
      className={cn(
        'bg-primary/15 text-foreground inline-flex size-9 items-center justify-center rounded-[var(--salora-radius-pill)] text-xs font-semibold',
        className
      )}
    >
      {initials.slice(0, 2).toUpperCase()}
    </span>
  );
}

export { Avatar };
