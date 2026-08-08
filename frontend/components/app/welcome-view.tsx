import { Button } from '@/components/ui/button';
import { cn } from '@/lib/shadcn/utils';

export const PRACTICE_SUGGESTIONS = [
  {
    emoji: '📖',
    title: 'Vocabulary Practice',
    description: 'Learn useful words and phrases for everyday English.',
    prompt:
      'Help me practice English vocabulary. Teach me 3 useful words and make me use them in sentences.',
  },
  {
    emoji: '🗣',
    title: 'Speaking Practice',
    description: 'Build confidence with short spoken conversations.',
    prompt: 'I want speaking practice. Start a simple spoken English conversation with me.',
  },
  {
    emoji: '🎯',
    title: 'Grammar Practice',
    description: 'Fix common mistakes with clear, simple explanations.',
    prompt:
      'Help me practice beginner English grammar. Explain one rule simply and give me an example to try.',
  },
  {
    emoji: '💬',
    title: 'Daily Conversation',
    description: 'Practice natural talk for school, work, and daily life.',
    prompt:
      'Let us practice daily conversation in English. Ask me about my day and help me reply naturally.',
  },
] as const;

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
  onPracticeSuggestion?: (prompt: string) => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  onPracticeSuggestion,
  ref,
  className,
  ...props
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div
      ref={ref}
      className={cn(
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-16 sm:px-6 sm:py-20',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_280/_0.55),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.93_0.05_230/_0.45),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.95_0.03_160/_0.35),_transparent_45%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.06_280/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.25_0.05_230/_0.4),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.22_0.04_160/_0.3),_transparent_45%)]"
      />
      <div
        aria-hidden
        className="bg-primary/5 dark:bg-primary/10 pointer-events-none absolute -top-24 left-1/2 size-[28rem] -translate-x-1/2 rounded-full blur-3xl"
      />

      <section className="relative z-10 mx-auto flex w-full max-w-3xl flex-col items-center text-center">
        {/* Hero */}
        <div className="animate-in fade-in slide-in-from-bottom-4 fill-mode-both w-full rounded-3xl border border-white/40 bg-white/55 p-8 shadow-[0_20px_60px_-28px_rgba(15,23,42,0.35)] backdrop-blur-xl duration-700 sm:p-12 dark:border-white/10 dark:bg-white/5">
          <p className="animate-in fade-in fill-mode-both text-muted-foreground mb-6 font-mono text-[11px] font-bold tracking-[0.22em] uppercase delay-75 duration-700">
            Ready to Practice
          </p>

          <h1 className="animate-in fade-in slide-in-from-bottom-2 fill-mode-both text-foreground text-4xl font-semibold tracking-tight text-balance delay-100 duration-700 sm:text-5xl md:text-6xl">
            AI Voice Learning Tutor
          </h1>

          <div className="animate-in fade-in fill-mode-both mt-5 flex flex-wrap items-center justify-center gap-2 delay-150 duration-700">
            <span className="text-foreground/80 rounded-full border border-white/50 bg-white/55 px-3 py-1 text-[11px] font-medium tracking-wide shadow-sm backdrop-blur-md sm:text-xs dark:border-white/10 dark:bg-white/10">
              Learning &amp; Literacy
            </span>
            <span className="text-foreground/80 rounded-full border border-white/50 bg-white/55 px-3 py-1 text-[11px] font-medium tracking-wide shadow-sm backdrop-blur-md sm:text-xs dark:border-white/10 dark:bg-white/10">
              VoiceForBharat 2026
            </span>
          </div>

          <p className="animate-in fade-in fill-mode-both text-muted-foreground mx-auto mt-6 max-w-md text-base leading-relaxed text-pretty delay-200 duration-700 sm:text-lg">
            Practice Spoken English naturally.
            <br />
            Talk in Hindi, English or Hinglish.
          </p>

          <div className="animate-in fade-in slide-in-from-bottom-3 fill-mode-both mt-10 flex flex-col items-center gap-3 delay-300 duration-700">
            <Button
              size="lg"
              onClick={onStartCall}
              className="h-14 min-w-[16rem] rounded-full px-10 text-sm font-bold tracking-[0.18em] uppercase shadow-[0_14px_44px_-12px_rgba(14,165,233,0.45)] transition-all duration-300 hover:-translate-y-0.5 hover:scale-[1.02] hover:shadow-[0_20px_48px_-12px_rgba(14,165,233,0.55)] focus-visible:ring-4 focus-visible:ring-sky-400/40 focus-visible:ring-offset-2 active:scale-[0.98] sm:min-w-[18rem] sm:text-base"
            >
              {startButtonText}
            </Button>
            <p className="text-muted-foreground text-[11px] font-medium tracking-wide sm:text-xs">
              Powered by Murf Falcon
            </p>
          </div>
        </div>

        {/* Quick Practice Suggestions */}
        <div className="animate-in fade-in fill-mode-both mt-8 w-full delay-500 duration-700 sm:mt-10">
          <p className="text-muted-foreground mb-4 text-xs font-medium tracking-wide uppercase sm:mb-5 sm:text-sm">
            Quick Practice Suggestions
          </p>
          <ul className="grid w-full grid-cols-1 gap-3.5 sm:grid-cols-2 sm:gap-4">
            {PRACTICE_SUGGESTIONS.map((suggestion, index) => (
              <li key={suggestion.title}>
                <button
                  type="button"
                  onClick={() =>
                    onPracticeSuggestion ? onPracticeSuggestion(suggestion.prompt) : onStartCall()
                  }
                  className={cn(
                    'group animate-in fade-in zoom-in-95 fill-mode-both focus-visible:ring-ring flex h-full w-full flex-col items-start rounded-2xl border border-white/50 bg-white/55 p-4 text-left shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1.5 hover:scale-[1.02] hover:border-sky-300/50 hover:bg-white/85 hover:shadow-[0_16px_36px_-18px_rgba(14,165,233,0.45)] focus-visible:ring-2 focus-visible:outline-none sm:p-5 dark:border-white/10 dark:bg-white/5 dark:hover:border-sky-400/30 dark:hover:bg-white/10',
                    index === 0 && 'delay-500',
                    index === 1 && 'delay-[550ms]',
                    index === 2 && 'delay-[600ms]',
                    index === 3 && 'delay-[650ms]'
                  )}
                >
                  <span className="mb-2.5 text-3xl transition-transform duration-300 group-hover:scale-110">
                    {suggestion.emoji}
                  </span>
                  <span className="text-foreground text-sm font-semibold tracking-wide sm:text-base">
                    {suggestion.title}
                  </span>
                  <span className="text-muted-foreground mt-1.5 text-xs leading-relaxed sm:text-sm">
                    {suggestion.description}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        <footer className="animate-in fade-in fill-mode-both text-muted-foreground mt-10 space-y-1 text-center text-xs leading-relaxed delay-700 duration-700 sm:text-sm">
          <p className="text-foreground/80 font-medium">Built by Saloni Saini</p>
          <p>Powered by Murf Falcon</p>
        </footer>
      </section>
    </div>
  );
};
