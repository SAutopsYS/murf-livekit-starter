import { type VariantProps, cva } from 'class-variance-authority';
import { cn } from '@/lib/shadcn/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-[var(--salora-radius-pill)] border px-3 py-1 text-[11px] font-medium tracking-wide sm:text-xs',
  {
    variants: {
      variant: {
        default: 'border-border bg-secondary text-secondary-foreground',
        pulse: 'border-primary/20 bg-primary/10 text-foreground',
        success: 'border-transparent bg-salora-success/15 text-foreground',
        warning: 'border-transparent bg-salora-warning/20 text-foreground',
        error: 'border-transparent bg-salora-error/15 text-foreground',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

function Badge({
  className,
  variant,
  ...props
}: React.ComponentProps<'span'> & VariantProps<typeof badgeVariants>) {
  return (
    <span data-slot="badge" className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
