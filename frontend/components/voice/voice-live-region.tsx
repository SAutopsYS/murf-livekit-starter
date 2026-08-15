'use client';

import { useVoice } from '@/components/voice/voice-provider';

export function VoiceLiveRegion() {
  const { visual, transfer } = useVoice();
  const text = transfer
    ? `${visual.label}. Routing from ${transfer.source} to ${transfer.destination}.`
    : `${visual.label}. ${visual.meaning}`;

  return (
    <div className="sr-only" role="status" aria-live="polite" aria-atomic="true">
      {text}
    </div>
  );
}
