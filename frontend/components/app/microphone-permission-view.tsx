import { WarningIcon } from '@phosphor-icons/react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/shadcn/utils';

interface MicrophonePermissionViewProps {
  onRetry: () => void;
  onBack?: () => void;
}

export function MicrophonePermissionView({
  onRetry,
  onBack,
  ref,
  className,
  ...props
}: React.ComponentProps<'div'> & MicrophonePermissionViewProps) {
  return (
    <div
      ref={ref}
      role="alertdialog"
      aria-labelledby="mic-permission-title"
      aria-describedby="mic-permission-description"
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.05_70/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom,_oklch(0.94_0.03_250/_0.35),_transparent_50%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.05_70/_0.4),_transparent_55%),radial-gradient(ellipse_at_bottom,_oklch(0.22_0.04_250/_0.3),_transparent_50%)]"
      />

      <div className="animate-in fade-in zoom-in-95 relative z-10 w-full max-w-md rounded-3xl border border-amber-500/20 bg-white/55 p-8 text-center shadow-[0_20px_60px_-28px_rgba(15,23,42,0.35)] backdrop-blur-xl duration-500 sm:p-10 dark:border-amber-400/20 dark:bg-white/5">
        <div
          aria-hidden
          className="mx-auto mb-5 flex size-14 items-center justify-center rounded-full border border-amber-500/20 bg-amber-500/10 text-2xl text-amber-600 dark:text-amber-300"
        >
          <WarningIcon weight="bold" className="size-7" />
        </div>

        <p aria-hidden className="mb-2 text-2xl">
          🎤
        </p>

        <h2
          id="mic-permission-title"
          className="text-foreground text-2xl font-semibold tracking-tight sm:text-3xl"
        >
          Microphone Access Required
        </h2>

        <div
          id="mic-permission-description"
          className="text-muted-foreground mx-auto mt-4 max-w-sm space-y-2 text-sm leading-relaxed sm:text-base"
        >
          <p>Allow microphone access to start practicing with your AI Voice Tutor.</p>
          <p>Please enable microphone permission in your browser settings and try again.</p>
        </div>

        <div className="mt-8 flex flex-col items-center gap-3">
          <Button
            size="lg"
            onClick={onRetry}
            className="h-12 min-w-[14rem] rounded-full px-8 text-sm font-bold tracking-[0.14em] uppercase focus-visible:ring-2 focus-visible:ring-offset-2 sm:h-14 sm:min-w-[16rem]"
          >
            Enable Microphone
          </Button>
          {onBack && (
            <Button
              variant="ghost"
              onClick={onBack}
              className="text-muted-foreground rounded-full focus-visible:ring-2"
            >
              Back to Ready
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
