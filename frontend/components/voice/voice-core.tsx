'use client';

import type { CSSProperties, ReactNode } from 'react';
import { VoiceOverlay } from '@/components/voice/voice-overlay';
import { useVoice } from '@/components/voice/voice-provider';
import { cn } from '@/lib/shadcn/utils';

export function VoiceCore({ children, className }: { children: ReactNode; className?: string }) {
  const { phase, visual } = useVoice();

  return (
    <div
      data-slot="voice-core"
      data-phase={phase}
      data-motion={visual.motionToken}
      className={cn('voice-core relative overflow-hidden', className)}
      style={{ '--voice-core-color': visual.colorToken } as CSSProperties}
    >
      <div aria-hidden className="voice-core-glow" />
      <div aria-hidden className="voice-core-ring" />
      <div className="relative z-[1]">{children}</div>
      <VoiceOverlay />
    </div>
  );
}
