import * as React from 'react';
import { cn } from '@/lib/shadcn/utils';

function Input({ className, type, ...props }: React.ComponentProps<'input'>) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        'border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex h-10 w-full rounded-[var(--salora-radius-control)] border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  );
}

function FieldLabel({ className, ...props }: React.ComponentProps<'label'>) {
  return (
    <label className={cn('text-muted-foreground text-sm font-medium', className)} {...props} />
  );
}

const fieldControlClassName =
  'border-input bg-background ring-offset-background focus-visible:ring-ring h-10 w-full rounded-[var(--salora-radius-control)] border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50';

function NativeSelect({ className, ...props }: React.ComponentProps<'select'>) {
  return (
    <select data-slot="native-select" className={cn(fieldControlClassName, className)} {...props} />
  );
}

export { Input, FieldLabel, NativeSelect, fieldControlClassName };
