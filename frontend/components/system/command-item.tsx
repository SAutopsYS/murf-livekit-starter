import type { ComponentProps } from 'react';
import { cn } from '@/lib/shadcn/utils';

function CommandItem({ className, ...props }: ComponentProps<'button'>) {
  return (
    <button
      type="button"
      data-slot="command-item"
      className={cn(
        'hover:bg-accent w-full rounded-[var(--salora-radius-control)] px-3 py-2 text-left text-sm',
        className
      )}
      {...props}
    />
  );
}

export { CommandItem };
