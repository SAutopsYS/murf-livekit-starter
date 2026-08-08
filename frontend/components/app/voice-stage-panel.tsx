'use client';

import { Track } from 'livekit-client';
import { AnimatePresence, motion } from 'motion/react';
import { useAgent, useTracks } from '@livekit/components-react';
import { AudioVisualizer } from '@/components/agents-ui/blocks/agent-session-view-01/components/audio-visualizer';
import { cn } from '@/lib/shadcn/utils';

type StageCopy = {
  title: string;
  subtitle: string;
  tone: 'listening' | 'thinking' | 'speaking' | 'ready' | 'ended';
};

function getStageCopy(agentState: string): StageCopy {
  switch (agentState) {
    case 'listening':
      return {
        title: '🎤 Listening',
        subtitle: 'Speak naturally...',
        tone: 'listening',
      };
    case 'thinking':
      return {
        title: '🧠 Thinking',
        subtitle: 'Preparing a helpful response...',
        tone: 'thinking',
      };
    case 'speaking':
      return {
        title: '✨ AI Tutor Speaking',
        subtitle: 'Listen carefully.',
        tone: 'speaking',
      };
    case 'failed':
    case 'disconnected':
      return {
        title: 'Session Completed',
        subtitle: 'Thanks for practicing today.',
        tone: 'ended',
      };
    default:
      return {
        title: 'Ready to Practice',
        subtitle: 'Start speaking whenever you are ready.',
        tone: 'ready',
      };
  }
}

const TONE_CLASS: Record<StageCopy['tone'], string> = {
  listening: 'text-sky-600 dark:text-sky-300',
  thinking: 'text-violet-600 dark:text-violet-300',
  speaking: 'text-cyan-700 dark:text-cyan-300',
  ready: 'text-foreground/80',
  ended: 'text-muted-foreground',
};

const ORB_CLASS: Record<StageCopy['tone'], string> = {
  ready: 'bg-sky-400/50 shadow-[0_0_24px_rgba(14,165,233,0.35)]',
  listening: 'bg-sky-400 shadow-[0_0_28px_rgba(14,165,233,0.55)]',
  thinking: 'bg-violet-400 shadow-[0_0_24px_rgba(167,139,250,0.45)] animate-pulse',
  speaking: 'bg-cyan-400 shadow-[0_0_32px_rgba(34,211,238,0.6)] animate-pulse scale-110',
  ended: 'bg-slate-300/70 shadow-[0_0_16px_rgba(148,163,184,0.25)]',
};

interface VoiceStagePanelProps {
  audioVisualizerColor?: `#${string}`;
  audioVisualizerColorShift?: number;
  audioVisualizerWaveLineWidth?: number;
  className?: string;
}

export function VoiceStagePanel({
  audioVisualizerColor = '#0EA5E9',
  audioVisualizerColorShift = 0.25,
  audioVisualizerWaveLineWidth = 4,
  className,
}: VoiceStagePanelProps) {
  const { state: agentState } = useAgent();
  const [microphoneTrack] = useTracks([Track.Source.Microphone]);
  const stage = getStageCopy(agentState);

  return (
    <div
      className={cn(
        'animate-in fade-in relative mx-auto flex w-full max-w-2xl flex-col items-center px-4 duration-500',
        className
      )}
    >
      <AnimatePresence mode="wait">
        <motion.div
          key={stage.title}
          initial={{ opacity: 0, y: 6, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -4, scale: 0.98 }}
          transition={{ duration: 0.22, ease: 'easeOut' }}
          className="mb-3 text-center"
        >
          <p
            className={cn(
              'text-sm font-semibold tracking-wide sm:text-base',
              TONE_CLASS[stage.tone],
              stage.tone === 'thinking' && 'animate-pulse'
            )}
          >
            {stage.title}
          </p>
          <p className="text-muted-foreground mt-1 text-xs leading-relaxed sm:text-sm">
            {stage.subtitle}
          </p>
        </motion.div>
      </AnimatePresence>

      {/* Premium AI orb — Tailwind only */}
      <div
        aria-hidden
        className={cn(
          'mb-3 size-3 rounded-full transition-all duration-500 sm:size-3.5',
          ORB_CLASS[stage.tone]
        )}
      />

      <div
        className={cn(
          'relative flex h-[156px] w-full items-center justify-center overflow-hidden rounded-3xl border border-sky-200/40 bg-white/50 px-3 shadow-[0_16px_48px_-28px_rgba(14,165,233,0.45)] backdrop-blur-xl transition-shadow duration-300 sm:h-[188px] dark:border-sky-400/15 dark:bg-white/5',
          stage.tone === 'thinking' && 'shadow-violet-500/15',
          stage.tone === 'listening' && 'shadow-sky-500/20',
          stage.tone === 'speaking' && 'shadow-cyan-500/20'
        )}
      >
        <AudioVisualizer
          isChatOpen={false}
          audioVisualizerType="wave"
          audioVisualizerColor={audioVisualizerColor}
          audioVisualizerColorShift={audioVisualizerColorShift}
          audioVisualizerWaveLineWidth={audioVisualizerWaveLineWidth}
          listeningAudioTrack={microphoneTrack}
          className="size-[240px] sm:size-[280px]"
        />
      </div>
    </div>
  );
}
