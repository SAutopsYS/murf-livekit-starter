import type { ComponentProps } from 'react';
import { cn } from '@/lib/shadcn/utils';

function ResponsiveGrid({
  className,
  columns = 3,
  ...props
}: ComponentProps<'div'> & { columns?: 2 | 3 | 4 }) {
  return (
    <div
      data-slot="responsive-grid"
      className={cn(
        'grid gap-4',
        columns === 2 && 'sm:grid-cols-2',
        columns === 3 && 'sm:grid-cols-2 lg:grid-cols-3',
        columns === 4 && 'sm:grid-cols-2 lg:grid-cols-4',
        className
      )}
      {...props}
    />
  );
}

function BentoGrid({ className, ...props }: ComponentProps<'div'>) {
  return (
    <div
      data-slot="bento-grid"
      className={cn(
        'grid auto-rows-min grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-12',
        className
      )}
      {...props}
    />
  );
}

function BentoCell({
  className,
  span = 2,
  ...props
}: ComponentProps<'div'> & { span?: 2 | 3 | 4 | 6 | 8 | 12 }) {
  return (
    <div
      data-slot="bento-cell"
      className={cn(
        'col-span-1 sm:col-span-2',
        span === 2 && 'md:col-span-2 xl:col-span-2 2xl:col-span-3',
        span === 3 && 'md:col-span-3 xl:col-span-3 2xl:col-span-4',
        span === 4 && 'md:col-span-4 xl:col-span-4 2xl:col-span-6',
        span === 6 && 'md:col-span-6 xl:col-span-6 2xl:col-span-8',
        span === 8 && 'md:col-span-6 xl:col-span-8 2xl:col-span-8',
        span === 12 && 'md:col-span-6 xl:col-span-8 2xl:col-span-12',
        className
      )}
      {...props}
    />
  );
}

export { ResponsiveGrid, BentoGrid, BentoCell };
