'use client';

import { ConnectionState } from 'livekit-client';
import { useAgent, useSessionContext } from '@livekit/components-react';
import { cn } from '@/lib/shadcn/utils';

type StatusLabel = 'Ready' | 'Connecting' | 'Listening' | 'Thinking' | 'Speaking' | 'Ended';

function getStatusLabel(agentState: string): StatusLabel {
  switch (agentState) {
    case 'listening':
      return 'Listening';
    case 'thinking':
      return 'Thinking';
    case 'speaking':
      return 'Speaking';
    case 'idle':
      return 'Ready';
    case 'failed':
    case 'disconnected':
      return 'Ended';
    case 'connecting':
    case 'pre-connect-buffering':
    case 'initializing':
    default:
      return 'Connecting';
  }
}

function getLoadingHint(
  connectionState: ConnectionState,
  agentState: string,
  isConnected: boolean
): string | null {
  if (connectionState === ConnectionState.Connecting) {
    return 'Connecting...';
  }

  if (!isConnected) {
    return null;
  }

  switch (agentState) {
    case 'connecting':
    case 'pre-connect-buffering':
      return 'Joining your AI Tutor...';
    case 'initializing':
    case 'thinking':
      return 'Preparing your lesson...';
    default:
      return null;
  }
}

const STATUS_META: Record<StatusLabel, { emoji: string; colorClass: string; emojiClass?: string }> =
  {
    Ready: {
      emoji: '🟢',
      colorClass: 'text-emerald-700 dark:text-emerald-300',
    },
    Connecting: {
      emoji: '🟡',
      colorClass: 'text-amber-700 dark:text-amber-300',
      emojiClass: 'animate-pulse',
    },
    Listening: {
      emoji: '🎤',
      colorClass: 'text-sky-700 dark:text-sky-300',
    },
    Thinking: {
      emoji: '🧠',
      colorClass: 'text-amber-700 dark:text-amber-300',
      emojiClass: 'animate-pulse',
    },
    Speaking: {
      emoji: '✨',
      colorClass: 'text-cyan-700 dark:text-cyan-300',
    },
    Ended: {
      emoji: '⚪',
      colorClass: 'text-muted-foreground',
    },
  };

export function SessionStatusBadge({ className }: { className?: string }) {
  const { state: agentState } = useAgent();
  const { connectionState, isConnected } = useSessionContext();
  const label = getStatusLabel(agentState);
  const meta = STATUS_META[label];
  const loadingHint = getLoadingHint(connectionState, String(agentState), isConnected);

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
        aria-label={`Session status: ${label}${loadingHint ? `. ${loadingHint}` : ''}`}
        className={cn(
          'animate-in fade-in slide-in-from-top-2 flex max-w-full items-center gap-1.5 rounded-full border border-white/55 bg-white/75 px-3 py-1.5 text-xs font-medium tracking-wide shadow-[0_10px_28px_-12px_rgba(15,23,42,0.32)] backdrop-blur-md duration-300 sm:gap-2 sm:px-3.5 sm:py-1.5 sm:text-sm dark:border-white/10 dark:bg-white/10',
          meta.colorClass
        )}
      >
        <span aria-hidden className={cn('text-[11px] leading-none sm:text-xs', meta.emojiClass)}>
          {meta.emoji}
        </span>
        <span className="truncate">{label}</span>
      </div>

      {loadingHint && (
        <p className="animate-in fade-in text-muted-foreground flex items-center gap-1.5 text-[11px] font-medium tracking-wide duration-300 sm:text-xs">
          <span
            aria-hidden
            className="border-muted-foreground/30 border-t-muted-foreground size-3 animate-spin rounded-full border-2"
          />
          <span>{loadingHint}</span>
        </p>
      )}
    </div>
  );
}
