import { Button } from '@/components/ui/button';
import { cn } from '@/lib/shadcn/utils';

const FEATURES = [
  { emoji: '📖', label: 'Vocabulary' },
  { emoji: '🗣', label: 'Speaking Practice' },
  { emoji: '🎯', label: 'Grammar' },
  { emoji: '💬', label: 'Daily Conversation' },
] as const;

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
  className,
  ...props
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div
      ref={ref}
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6',
        className
      )}
      {...props}
    >
      {/* Soft ambient gradients */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_280/_0.55),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.93_0.05_230/_0.45),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.95_0.03_160/_0.35),_transparent_45%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.06_280/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.25_0.05_230/_0.4),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.22_0.04_160/_0.3),_transparent_45%)]"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -top-24 left-1/2 size-[28rem] -translate-x-1/2 rounded-full bg-primary/5 blur-3xl dark:bg-primary/10"
      />

      <section className="relative z-10 mx-auto flex w-full max-w-3xl flex-col items-center text-center">
        {/* Hero glass panel */}
        <div className="animate-in fade-in slide-in-from-bottom-4 fill-mode-both w-full rounded-3xl border border-white/40 bg-white/55 p-8 shadow-[0_20px_60px_-28px_rgba(15,23,42,0.35)] backdrop-blur-xl duration-700 dark:border-white/10 dark:bg-white/5 sm:p-12">
          <h1 className="animate-in fade-in slide-in-from-bottom-2 fill-mode-both text-foreground text-4xl font-semibold tracking-tight text-balance delay-100 duration-700 sm:text-5xl md:text-6xl">
            AI Voice Learning Tutor
          </h1>

          <div className="animate-in fade-in fill-mode-both mt-4 flex flex-wrap items-center justify-center gap-2 delay-150 duration-700">
            <span className="rounded-full border border-white/50 bg-white/55 px-3 py-1 text-[11px] font-medium tracking-wide text-foreground/80 shadow-sm backdrop-blur-md dark:border-white/10 dark:bg-white/10 sm:text-xs">
              Learning &amp; Literacy
            </span>
            <span className="rounded-full border border-white/50 bg-white/55 px-3 py-1 text-[11px] font-medium tracking-wide text-foreground/80 shadow-sm backdrop-blur-md dark:border-white/10 dark:bg-white/10 sm:text-xs">
              VoiceForBharat 2026
            </span>
          </div>

          <p className="animate-in fade-in fill-mode-both text-muted-foreground mx-auto mt-5 max-w-md text-base leading-relaxed text-pretty delay-200 duration-700 sm:text-lg">
            Practice Spoken English naturally.
            <br />
            Talk in Hindi, English or Hinglish.
          </p>

          {/* Feature cards */}
          <ul className="mt-10 grid w-full grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
            {FEATURES.map((feature, index) => (
              <li
                key={feature.label}
                className={cn(
                  'animate-in fade-in zoom-in-95 fill-mode-both group rounded-2xl border border-white/50 bg-white/60 px-3 py-4 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:scale-[1.03] hover:border-primary/20 hover:bg-white/80 hover:shadow-md dark:border-white/10 dark:bg-white/5 dark:hover:bg-white/10',
                  index === 0 && 'delay-300',
                  index === 1 && 'delay-400',
                  index === 2 && 'delay-500',
                  index === 3 && 'delay-[600ms]'
                )}
                style={{ animationDuration: '700ms' }}
              >
                <span className="mb-2 block text-2xl transition-transform duration-300 group-hover:scale-110">
                  {feature.emoji}
                </span>
                <span className="text-foreground text-xs font-medium tracking-wide sm:text-sm">
                  {feature.label}
                </span>
              </li>
            ))}
          </ul>

          <div className="animate-in fade-in slide-in-from-bottom-3 fill-mode-both mt-10 delay-[700ms] duration-700">
            <Button
              size="lg"
              onClick={onStartCall}
              className="h-14 min-w-[16rem] rounded-full px-10 text-sm font-bold tracking-[0.18em] uppercase shadow-[0_12px_40px_-12px_rgba(15,23,42,0.45)] transition-all duration-300 hover:-translate-y-0.5 hover:scale-[1.02] hover:shadow-[0_18px_44px_-12px_rgba(15,23,42,0.5)] active:scale-[0.98] sm:min-w-[18rem] sm:text-base"
            >
              {startButtonText}
            </Button>
          </div>
        </div>

        {/* Footer */}
        <footer className="animate-in fade-in fill-mode-both text-muted-foreground mt-10 space-y-1 text-center text-xs leading-relaxed delay-[800ms] duration-700 sm:text-sm">
          <p className="font-medium text-foreground/80">Built by Saloni Saini</p>
          <p>Powered by Murf Falcon</p>
        </footer>
      </section>
    </div>
  );
};
