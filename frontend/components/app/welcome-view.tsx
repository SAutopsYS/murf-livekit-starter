import Link from 'next/link';
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
        'relative flex min-h-svh w-full items-center justify-center overflow-hidden px-4 py-20 sm:px-6 sm:py-24',
        className
      )}
      {...props}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_oklch(0.92_0.04_165/_0.45),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.94_0.03_95/_0.35),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.96_0.02_150/_0.3),_transparent_45%)] dark:bg-[radial-gradient(ellipse_at_top,_oklch(0.28_0.04_165/_0.4),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_oklch(0.22_0.03_145/_0.3),_transparent_50%),radial-gradient(ellipse_at_bottom_left,_oklch(0.2_0.02_150/_0.28),_transparent_45%)]"
      />
      <div
        aria-hidden
        className="bg-primary/15 pointer-events-none absolute -top-28 left-1/2 size-[32rem] -translate-x-1/2 rounded-full blur-3xl"
      />

      <section className="relative z-10 mx-auto flex w-full max-w-3xl flex-col items-center text-center">
        <div className="animate-in fade-in slide-in-from-bottom-4 fill-mode-both surface-panel w-full p-8 duration-700 sm:p-12">
          <p className="animate-in fade-in fill-mode-both text-muted-foreground mb-5 font-mono text-[11px] font-bold tracking-[0.24em] uppercase delay-75 duration-700">
            SALORA OS
          </p>

          <h1 className="animate-in fade-in slide-in-from-bottom-2 fill-mode-both text-foreground text-4xl font-semibold tracking-[-0.03em] text-balance delay-100 duration-700 sm:text-5xl md:text-[3.5rem]">
            Learning that stays on the line.
          </h1>

          <div className="animate-in fade-in fill-mode-both mt-5 flex flex-wrap items-center justify-center gap-2 delay-150 duration-700">
            <span className="text-foreground/80 border-primary/20 bg-primary/10 rounded-full border px-3 py-1 text-[11px] font-medium tracking-wide shadow-sm backdrop-blur-md sm:text-xs">
              AI Learning OS
            </span>
            <span className="text-foreground/80 rounded-full border border-white/60 bg-white/70 px-3 py-1 text-[11px] font-medium tracking-wide shadow-sm backdrop-blur-md sm:text-xs dark:border-white/10 dark:bg-white/10">
              Hindi · English · Hinglish
            </span>
          </div>

          <p className="animate-in fade-in fill-mode-both text-muted-foreground mx-auto mt-6 max-w-md text-base leading-relaxed text-pretty delay-200 duration-700 sm:text-lg">
            The world&apos;s first AI Learning Operating System.
            <br />
            Speak. Practice. Return without starting over.
          </p>

          <div className="animate-in fade-in slide-in-from-bottom-3 fill-mode-both mt-10 flex flex-col items-center gap-3 delay-300 duration-700">
            <Button
              size="lg"
              onClick={onStartCall}
              className="btn-premium h-14 min-w-[16rem] px-10 text-sm font-bold tracking-[0.16em] uppercase sm:min-w-[18rem] sm:text-base"
            >
              {startButtonText}
            </Button>
            <p className="text-muted-foreground text-[11px] font-medium tracking-wide sm:text-xs">
              Voice by Murf Falcon · Transport by LiveKit
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Link
                href="/analytics"
                className="text-primary text-[11px] font-medium tracking-wide underline-offset-4 hover:underline sm:text-xs"
              >
                Analytics
              </Link>
              <Link
                href="/enterprise"
                className="text-primary text-[11px] font-medium tracking-wide underline-offset-4 hover:underline sm:text-xs"
              >
                Control Center
              </Link>
            </div>
          </div>
        </div>

        <div className="animate-in fade-in fill-mode-both mt-9 w-full delay-500 duration-700 sm:mt-11">
          <p className="text-muted-foreground mb-4 text-xs font-medium tracking-[0.14em] uppercase sm:mb-5 sm:text-sm">
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
                    'group animate-in fade-in zoom-in-95 fill-mode-both focus-visible:ring-ring hover:border-primary/35 dark:hover:border-primary/30 flex h-full w-full flex-col items-start rounded-2xl border border-white/55 bg-white/60 p-4 text-left shadow-[0_10px_30px_-20px_rgba(15,23,42,0.35)] backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:bg-white/90 hover:shadow-[0_18px_40px_-18px_color-mix(in_srgb,var(--salora-pulse)_40%,transparent)] focus-visible:ring-2 focus-visible:outline-none sm:p-5 dark:border-white/10 dark:bg-white/5 dark:hover:bg-white/10',
                    index === 0 && 'delay-500',
                    index === 1 && 'delay-[550ms]',
                    index === 2 && 'delay-[600ms]',
                    index === 3 && 'delay-[650ms]'
                  )}
                >
                  <span className="mb-2.5 text-2xl transition-transform duration-300 group-hover:scale-110 sm:text-3xl">
                    {suggestion.emoji}
                  </span>
                  <span className="text-foreground text-sm font-semibold tracking-tight sm:text-base">
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

        <footer className="animate-in fade-in fill-mode-both text-muted-foreground mt-11 space-y-1 text-center text-xs leading-relaxed delay-700 duration-700 sm:text-sm">
          <p className="text-foreground/80 font-medium">Built by Saloni Saini</p>
          <p>Powered by Murf Falcon</p>
        </footer>
      </section>
    </div>
  );
};
