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
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.93_0.05_230/_0.5),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.94_0.04_180/_0.35),_transparent_50%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.05_230/_0.4),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.24_0.04_190/_0.3),_transparent_50%)]"
      />

      <div className="animate-in fade-in zoom-in-95 surface-panel relative z-10 w-full max-w-md p-8 text-center duration-500 sm:p-10">
        <div
          aria-hidden
          className="mx-auto mb-6 size-11 animate-spin rounded-full border-2 border-sky-200/70 border-t-sky-500 dark:border-sky-400/20 dark:border-t-sky-300"
        />
        <h2 className="text-foreground text-xl font-semibold tracking-tight sm:text-2xl">
          {copy.title}
        </h2>
        <p className="text-muted-foreground mt-3 text-sm leading-relaxed sm:text-base">
          {copy.subtitle}
        </p>
        <p className="text-muted-foreground mt-5 text-xs font-medium tracking-wide">{copy.hint}</p>
      </div>
    </div>
  );
}
