'use client';

import * as React from 'react';
import { Dialog as DialogPrimitive } from 'radix-ui';
import {
  Dialog,
  DialogClose,
  DialogOverlay,
  DialogPortal,
  DialogTrigger,
} from '@/components/ui/dialog';
import { cn } from '@/lib/shadcn/utils';

function Drawer({ ...props }: React.ComponentProps<typeof Dialog>) {
  return <Dialog data-slot="drawer" {...props} />;
}

function DrawerContent({
  className,
  side = 'right',
  children,
  ...props
}: React.ComponentProps<typeof DialogPrimitive.Content> & {
  side?: 'left' | 'right';
}) {
  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        data-slot="drawer-content"
        className={cn(
          'bg-card text-card-foreground data-[state=open]:animate-in data-[state=closed]:animate-out shadow-salora-lg fixed inset-y-0 z-[var(--salora-z-overlay)] flex h-full w-full max-w-md flex-col border p-6',
          side === 'right'
            ? 'data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right right-0'
            : 'data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left left-0',
          className
        )}
        {...props}
      >
        {children}
      </DialogPrimitive.Content>
    </DialogPortal>
  );
}

export { Drawer, DrawerContent, DialogTrigger as DrawerTrigger, DialogClose as DrawerClose };
