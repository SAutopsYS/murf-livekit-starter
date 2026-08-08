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
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_280/_0.55),_transparent_55%),radial-gradient(ellipse_at_bottom_left,_oklch(0.95_0.03_160/_0.35),_transparent_45%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.06_280/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_left,_oklch(0.22_0.04_160/_0.3),_transparent_45%)]"
      />

      <div className="animate-in fade-in zoom-in-95 slide-in-from-bottom-4 relative z-10 w-full max-w-md rounded-3xl border border-white/40 bg-white/55 p-8 text-center shadow-[0_20px_60px_-28px_rgba(15,23,42,0.35)] backdrop-blur-xl duration-500 sm:p-10 dark:border-white/10 dark:bg-white/5">
        <p className="text-muted-foreground mb-3 font-mono text-[11px] font-bold tracking-[0.2em] uppercase">
          Learning &amp; Literacy
        </p>
        <h2 className="text-foreground text-3xl font-semibold tracking-tight sm:text-4xl">
          Session Ended
        </h2>
        <p aria-hidden className="mt-5 text-lg tracking-[0.2em]">
          ⭐⭐⭐⭐⭐
        </p>
        <p className="text-foreground mx-auto mt-3 max-w-sm text-base leading-relaxed font-medium">
          Great progress today!
        </p>
        <p className="text-muted-foreground mx-auto mt-2 max-w-sm text-sm leading-relaxed sm:text-base">
          Keep practicing for just 10 minutes every day to improve your English naturally.
        </p>
        <Button
          size="lg"
          onClick={onPracticeAgain}
          className="mt-8 h-14 min-w-[14rem] rounded-full px-10 text-sm font-bold tracking-[0.18em] uppercase shadow-[0_14px_44px_-12px_rgba(14,165,233,0.45)] transition-all duration-300 hover:-translate-y-0.5 hover:scale-[1.02] focus-visible:ring-4 focus-visible:ring-sky-400/40 focus-visible:ring-offset-2 active:scale-[0.98] sm:min-w-[16rem] sm:text-base"
        >
          Practice Again
        </Button>
      </div>
    </div>
  );
}
