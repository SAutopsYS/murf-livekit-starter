'use client';

import { useVoice } from '@/components/voice/voice-provider';
import { cn } from '@/lib/shadcn/utils';

const OVERLAY_PHASES = new Set(['connecting', 'routing', 'offline', 'muted', 'error']);

export function VoiceOverlay({ className }: { className?: string }) {
  const { visual, transfer, phase } = useVoice();
  if (!OVERLAY_PHASES.has(phase) || !visual.hint) return null;

  return (
    <div
      data-slot="voice-overlay"
      data-phase={phase}
      className={cn(
        'bg-background/70 pointer-events-none absolute inset-x-3 bottom-3 z-10 rounded-[var(--salora-radius-cluster)] border border-white/40 px-3 py-2 text-center text-xs font-medium backdrop-blur-md dark:border-white/10',
        className
      )}
    >
      {transfer && phase === 'routing'
        ? `${transfer.source} → ${transfer.destination}`
        : visual.hint}
    </div>
  );
}
