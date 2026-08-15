'use client';

import * as React from 'react';
import { Progress as ProgressPrimitive } from 'radix-ui';
import { cn } from '@/lib/shadcn/utils';

function Progress({
  className,
  value,
  ...props
}: React.ComponentProps<typeof ProgressPrimitive.Root>) {
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      className={cn(
        'bg-muted relative h-2 w-full overflow-hidden rounded-[var(--salora-radius-pill)]',
        className
      )}
      value={value}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className="bg-primary h-full w-full flex-1 transition-transform"
        style={{
          transform: `translateX(-${100 - (value ?? 0)}%)`,
          transitionDuration: 'var(--salora-duration-medium)',
          transitionTimingFunction: 'var(--salora-ease-progress)',
        }}
      />
    </ProgressPrimitive.Root>
  );
}

export { Progress };
