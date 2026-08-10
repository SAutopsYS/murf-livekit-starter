import { Button } from '@/components/ui/button';
import { cn } from '@/lib/shadcn/utils';

interface SessionEndedViewProps {
  onPracticeAgain: () => void;
}

export function SessionEndedView({
  onPracticeAgain,
  ref,
  className,
  ...props
}: React.ComponentProps<'div'> & SessionEndedViewProps) {
  return (
    <div
      ref={ref}
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.93_0.05_230/_0.5),_transparent_55%),radial-gradient(ellipse_at_bottom_left,_oklch(0.95_0.03_180/_0.35),_transparent_45%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.05_230/_0.4),_transparent_55%),radial-gradient(ellipse_at_bottom_left,_oklch(0.22_0.04_190/_0.3),_transparent_45%)]"
      />

      <div className="animate-in fade-in zoom-in-95 slide-in-from-bottom-4 surface-panel relative z-10 w-full max-w-md p-8 text-center duration-500 sm:p-10">
        <p className="text-muted-foreground mb-3 font-mono text-[11px] font-bold tracking-[0.2em] uppercase">
          Learning &amp; Literacy
        </p>
        <h2 className="text-foreground text-3xl font-semibold tracking-tight sm:text-4xl">
          Session Ended
        </h2>
        <div
          aria-hidden
          className="mx-auto mt-6 flex size-14 items-center justify-center rounded-full border border-sky-200/60 bg-sky-50 text-sky-600 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300"
        >
          <span className="text-xl">★</span>
        </div>
        <p className="text-foreground mx-auto mt-4 max-w-sm text-base leading-relaxed font-medium">
          Great progress today!
        </p>
        <p className="text-muted-foreground mx-auto mt-2 max-w-sm text-sm leading-relaxed sm:text-base">
          Keep practicing for just 10 minutes every day to improve your English naturally.
        </p>
        <Button
          size="lg"
          onClick={onPracticeAgain}
          className="btn-premium mt-8 h-14 min-w-[14rem] px-10 text-sm font-bold tracking-[0.16em] uppercase sm:min-w-[16rem] sm:text-base"
        >
          Practice Again
        </Button>
      </div>
    </div>
  );
}
