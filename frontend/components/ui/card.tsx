import * as React from 'react';
import { type VariantProps, cva } from 'class-variance-authority';
import { cn } from '@/lib/shadcn/utils';

const cardVariants = cva('text-card-foreground', {
  variants: {
    variant: {
      default:
        'bg-card border-border rounded-[var(--salora-radius-cluster)] border shadow-salora-sm',
      glass: 'surface-panel',
      sunken: 'bg-salora-sunken border-border rounded-[var(--salora-radius-cluster)] border',
    },
    padding: {
      none: '',
      sm: 'p-4',
      md: 'p-5',
      lg: 'p-8',
    },
  },
  defaultVariants: {
    variant: 'default',
    padding: 'md',
  },
});

function Card({
  className,
  variant,
  padding,
  ...props
}: React.ComponentProps<'article'> & VariantProps<typeof cardVariants>) {
  return (
    <article
      data-slot="card"
      className={cn(cardVariants({ variant, padding }), className)}
      {...props}
    />
  );
}

function CardTitle({ className, ...props }: React.ComponentProps<'h3'>) {
  return (
    <h3
      data-slot="card-title"
      className={cn(
        'text-muted-foreground mb-3 text-sm font-semibold tracking-wide uppercase',
        className
      )}
      {...props}
    />
  );
}

export { Card, CardTitle, cardVariants };
