'use client';

import { VoiceIndicators, useVoice } from '@/components/voice';
import { cn } from '@/lib/shadcn/utils';

export function ConnectingView({ ref, className, ...props }: React.ComponentProps<'div'>) {
  const { visual } = useVoice();
  const title = visual.hint ?? 'Connecting to your AI Tutor…';

  return (
    <div
      ref={ref}
      role="status"
      aria-live="polite"
      aria-label={title}
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_165/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.94_0.03_95/_0.35),_transparent_50%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.04_165/_0.4),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.22_0.03_145/_0.3),_transparent_50%)]"
      />

      <div className="animate-in fade-in zoom-in-95 surface-panel relative z-10 w-full max-w-md p-8 text-center duration-500 sm:p-10">
        <div className="mb-6 flex justify-center">
          <VoiceIndicators className="size-4" />
        </div>
        <h2 className="text-foreground text-xl font-semibold tracking-tight sm:text-2xl">
          {title}
        </h2>
        <p className="text-muted-foreground mt-3 text-sm leading-relaxed sm:text-base">
          {visual.meaning}
        </p>
      </div>
    </div>
  );
}
