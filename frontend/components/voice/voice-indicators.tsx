'use client';

import { useVoice } from '@/components/voice/voice-provider';
import { cn } from '@/lib/shadcn/utils';

export function VoiceIndicators({ className }: { className?: string }) {
  const { visual, phase } = useVoice();

  return (
    <span
      aria-hidden
      data-slot="voice-indicator"
      data-phase={phase}
      data-motion={visual.motionToken}
      className={cn('voice-indicator inline-block size-3 rounded-full', className)}
      style={{ background: visual.colorToken }}
    />
  );
}
