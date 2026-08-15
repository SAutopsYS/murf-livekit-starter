'use client';

import * as React from 'react';
import { Collapsible as CollapsiblePrimitive } from 'radix-ui';
import { cn } from '@/lib/shadcn/utils';

function Accordion({
  className,
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.Root>) {
  return (
    <CollapsiblePrimitive.Root
      data-slot="accordion"
      className={cn('border-border rounded-[var(--salora-radius-cluster)] border', className)}
      {...props}
    />
  );
}

function AccordionTrigger({
  className,
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.Trigger>) {
  return (
    <CollapsiblePrimitive.Trigger
      data-slot="accordion-trigger"
      className={cn(
        'hover:bg-accent flex w-full items-center justify-between px-4 py-3 text-left text-sm font-medium transition-colors',
        className
      )}
      {...props}
    />
  );
}

function AccordionContent({
  className,
  ...props
}: React.ComponentProps<typeof CollapsiblePrimitive.Content>) {
  return (
    <CollapsiblePrimitive.Content
      data-slot="accordion-content"
      className={cn(
        'data-[state=closed]:animate-out data-[state=open]:animate-in overflow-hidden px-4 pb-4 text-sm',
        className
      )}
      {...props}
    />
  );
}

export { Accordion, AccordionTrigger, AccordionContent };
