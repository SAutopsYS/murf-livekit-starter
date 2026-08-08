'use client';

import { ConnectionState } from 'livekit-client';
import { useAgent, useSessionContext } from '@livekit/components-react';
import { cn } from '@/lib/shadcn/utils';

function getConnectingCopy(connectionState: ConnectionState, agentState: string) {
  if (connectionState === ConnectionState.Connecting) {
    return {
      title: 'Connecting to your AI Tutor...',
      subtitle: 'Please wait a moment.',
      hint: 'Connecting...',
    };
  }

  if (
    agentState === 'connecting' ||
    agentState === 'pre-connect-buffering' ||
    agentState === 'initializing'
  ) {
    return {
      title: 'Joining your AI Tutor...',
      subtitle: 'Setting up your practice session.',
      hint: 'Joining your AI Tutor...',
    };
  }

  return {
    title: 'Preparing your lesson...',
    subtitle: 'Almost ready to practice.',
    hint: 'Preparing your lesson...',
  };
}

export function ConnectingView({ ref, className, ...props }: React.ComponentProps<'div'>) {
  const { connectionState } = useSessionContext();
  const { state: agentState } = useAgent();
  const copy = getConnectingCopy(connectionState, String(agentState));

  return (
    <div
      ref={ref}
      role="status"
      aria-live="polite"
      aria-label={copy.hint}
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_280/_0.55),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.93_0.05_230/_0.45),_transparent_50%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.06_280/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.25_0.05_230/_0.4),_transparent_50%)]"
      />

      <div className="animate-in fade-in zoom-in-95 relative z-10 w-full max-w-md rounded-3xl border border-white/40 bg-white/55 p-8 text-center shadow-[0_20px_60px_-28px_rgba(15,23,42,0.35)] backdrop-blur-xl duration-500 sm:p-10 dark:border-white/10 dark:bg-white/5">
        <div
          aria-hidden
          className="border-foreground/15 border-t-foreground mx-auto mb-6 size-10 animate-spin rounded-full border-2"
        />
        <h2 className="text-foreground text-xl font-semibold tracking-tight sm:text-2xl">
          {copy.title}
        </h2>
        <p className="text-muted-foreground mt-3 text-sm leading-relaxed sm:text-base">
          {copy.subtitle}
        </p>
        <p className="text-muted-foreground mt-4 text-xs font-medium tracking-wide">{copy.hint}</p>
      </div>
    </div>
  );
}
