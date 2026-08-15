'use client';

import { useVoice } from '@/components/voice/voice-provider';
import { cn } from '@/lib/shadcn/utils';

export function VoiceFeedback({ className }: { className?: string }) {
  const { visual, muted, online, phase } = useVoice();

  return (
    <ul
      data-slot="voice-feedback"
      className={cn('text-muted-foreground flex flex-wrap gap-2 text-[11px]', className)}
    >
      <li>AI · {visual.label}</li>
      <li>Mic · {muted ? 'off' : 'on'}</li>
      <li>Net · {online ? 'online' : 'offline'}</li>
      <li className="sr-only">Phase {phase}</li>
    </ul>
  );
}
