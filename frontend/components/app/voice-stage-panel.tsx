'use client';

import { Track } from 'livekit-client';
import { AnimatePresence, motion } from 'motion/react';
import { useTracks } from '@livekit/components-react';
import { AudioVisualizer } from '@/components/agents-ui/blocks/agent-session-view-01/components/audio-visualizer';
import { VoiceCore, VoiceFeedback, useVoice } from '@/components/voice';
import { cn } from '@/lib/shadcn/utils';

interface VoiceStagePanelProps {
  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  audioVisualizerColor?: `#${string}`;
  audioVisualizerColorShift?: number;
  audioVisualizerWaveLineWidth?: number;
  className?: string;
}

export function VoiceStagePanel({
  audioVisualizerType = 'wave',
  audioVisualizerColor,
  audioVisualizerColorShift = 0.25,
  audioVisualizerWaveLineWidth = 4,
  className,
}: VoiceStagePanelProps) {
  const { visual, phase } = useVoice();
  const [microphoneTrack] = useTracks([Track.Source.Microphone]);

  return (
    <div
      className={cn(
        'animate-in fade-in relative mx-auto flex w-full max-w-2xl flex-col items-center px-4 duration-500',
        className
      )}
    >
      <AnimatePresence mode="wait">
        <motion.div
          key={visual.label}
          initial={{ opacity: 0, y: 6, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -4, scale: 0.98 }}
          transition={{ duration: 0.22, ease: 'easeOut' }}
          className="mb-3.5 text-center"
        >
          <p className="text-foreground text-sm font-semibold tracking-wide sm:text-base">
            {visual.label}
          </p>
          <p className="text-muted-foreground mt-1 text-xs leading-relaxed sm:text-sm">
            {visual.meaning}
          </p>
        </motion.div>
      </AnimatePresence>

      <VoiceCore
        className={cn(
          'shadow-salora-md relative flex h-[156px] w-full items-center justify-center rounded-3xl border border-white/45 bg-white/55 px-3 backdrop-blur-xl sm:h-[188px] dark:border-white/10 dark:bg-white/5'
        )}
      >
        <AudioVisualizer
          isChatOpen={false}
          audioVisualizerType={audioVisualizerType}
          audioVisualizerColor={audioVisualizerColor}
          audioVisualizerColorShift={audioVisualizerColorShift}
          audioVisualizerWaveLineWidth={audioVisualizerWaveLineWidth}
          listeningAudioTrack={microphoneTrack}
          className="size-[240px] sm:size-[280px]"
        />
      </VoiceCore>
      <VoiceFeedback className="mt-3 justify-center" />
      <span className="sr-only">Voice phase {phase}</span>
    </div>
  );
}
