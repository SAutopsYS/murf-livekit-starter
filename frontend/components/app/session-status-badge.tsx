'use client';

import { VoiceIndicators, useVoice } from '@/components/voice';
import { cn } from '@/lib/shadcn/utils';

export function SessionStatusBadge({ className }: { className?: string }) {
  const { visual } = useVoice();

  return (
    <div
      className={cn(
        'pointer-events-none absolute top-4 left-1/2 z-40 flex w-[min(100%-2rem,24rem)] -translate-x-1/2 flex-col items-center gap-1.5 sm:top-5',
        className
      )}
    >
      <div
        role="status"
        aria-live="polite"
        aria-label={`Session status: ${visual.label}${visual.hint ? `. ${visual.hint}` : ''}`}
        className="animate-in fade-in slide-in-from-top-2 text-foreground flex max-w-full items-center gap-1.5 rounded-full border border-white/55 bg-white/75 px-3 py-1.5 text-xs font-medium tracking-wide shadow-[0_10px_28px_-12px_rgba(15,23,42,0.32)] backdrop-blur-md duration-300 sm:gap-2 sm:px-3.5 sm:py-1.5 sm:text-sm dark:border-white/10 dark:bg-white/10"
      >
        <VoiceIndicators />
        <span className="truncate">{visual.label}</span>
      </div>

      {visual.hint ? (
        <p className="animate-in fade-in text-muted-foreground flex items-center gap-1.5 text-[11px] font-medium tracking-wide duration-300 sm:text-xs">
          <span
            aria-hidden
            className="border-muted-foreground/30 border-t-muted-foreground size-3 animate-spin rounded-full border-2"
          />
          <span>{visual.hint}</span>
        </p>
      ) : null}
    </div>
  );
}
