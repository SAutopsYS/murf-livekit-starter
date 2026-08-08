'use client';

import React from 'react';
import { Track } from 'livekit-client';
import { type MotionProps, motion } from 'motion/react';
import { useAgent, useSessionContext, useSessionMessages } from '@livekit/components-react';
import { AgentChatTranscript } from '@/components/agents-ui/agent-chat-transcript';
import {
  AgentControlBar,
  type AgentControlBarControls,
} from '@/components/agents-ui/agent-control-bar';
import { SessionStatusBadge } from '@/components/app/session-status-badge';
import { VoiceStagePanel } from '@/components/app/voice-stage-panel';
import { cn } from '@/lib/shadcn/utils';

const BOTTOM_VIEW_MOTION_PROPS: MotionProps = {
  variants: {
    visible: {
      opacity: 1,
      translateY: '0%',
    },
    hidden: {
      opacity: 0,
      translateY: '100%',
    },
  },
  initial: 'hidden',
  animate: 'visible',
  exit: 'hidden',
  transition: {
    duration: 0.3,
    delay: 0.5,
    ease: 'easeOut',
  },
};

interface FadeProps {
  top?: boolean;
  bottom?: boolean;
  className?: string;
}

export function Fade({ top = false, bottom = false, className }: FadeProps) {
  return (
    <div
      className={cn(
        'from-background pointer-events-none h-4 bg-linear-to-b to-transparent',
        top && 'bg-linear-to-b',
        bottom && 'bg-linear-to-t',
        className
      )}
    />
  );
}

export interface AgentSessionView_01Props {
  /**
   * Message shown above the controls before the first chat message is sent.
   *
   * @default 'Agent is listening, ask it a question'
   */
  preConnectMessage?: string;
  /**
   * Enables or disables the chat text input controls.
   *
   * @default true
   */
  supportsChatInput?: boolean;
  /**
   * Enables or disables camera controls in the bottom control bar.
   *
   * @default true
   */
  supportsVideoInput?: boolean;
  /**
   * Enables or disables screen sharing controls in the bottom control bar.
   *
   * @default true
   */
  supportsScreenShare?: boolean;
  /**
   * Shows a pre-connect buffer state with a shimmer message before messages appear.
   *
   * @default true
   */
  isPreConnectBufferEnabled?: boolean;

  /** Selects the visualizer style rendered in the main tile area. */
  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  /** Primary hex color used by supported audio visualizer variants. */
  audioVisualizerColor?: `#${string}`;
  /** Hue shift intensity used by certain visualizers. */
  audioVisualizerColorShift?: number;
  /** Number of bars to render when `audioVisualizerType` is `bar`. */
  audioVisualizerBarCount?: number;
  /** Number of rows in the visualizer when `audioVisualizerType` is `grid`. */
  audioVisualizerGridRowCount?: number;
  /** Number of columns in the visualizer when `audioVisualizerType` is `grid`. */
  audioVisualizerGridColumnCount?: number;
  /** Number of radial bars when `audioVisualizerType` is `radial`. */
  audioVisualizerRadialBarCount?: number;
  /** Base radius of the radial visualizer when `audioVisualizerType` is `radial`. */
  audioVisualizerRadialRadius?: number;
  /** Stroke width of the wave path when `audioVisualizerType` is `wave`. */
  audioVisualizerWaveLineWidth?: number;
  /** Called when microphone permission/device errors occur during the session. */
  onMicrophoneError?: (error: Error, source?: Track.Source) => void;
  /** Optional class name merged onto the outer `<section>` container. */
  className?: string;
}

const CUSTOM_SESSION_VIEW_PROP_KEYS = new Set<keyof AgentSessionView_01Props>([
  'preConnectMessage',
  'supportsChatInput',
  'supportsVideoInput',
  'supportsScreenShare',
  'isPreConnectBufferEnabled',
  'audioVisualizerType',
  'audioVisualizerColor',
  'audioVisualizerColorShift',
  'audioVisualizerBarCount',
  'audioVisualizerGridRowCount',
  'audioVisualizerGridColumnCount',
  'audioVisualizerRadialBarCount',
  'audioVisualizerRadialRadius',
  'audioVisualizerWaveLineWidth',
  'onMicrophoneError',
  'className',
]);

export function AgentSessionView_01({
  supportsChatInput = true,
  supportsVideoInput = true,
  supportsScreenShare = true,
  audioVisualizerColor,
  audioVisualizerColorShift,
  audioVisualizerWaveLineWidth,
  onMicrophoneError,
  ref,
  className,
  ...rest
}: React.ComponentProps<'section'> & AgentSessionView_01Props) {
  // Keep the public API, but never forward custom visualizer/session props to the DOM.
  const domProps = Object.fromEntries(
    Object.entries(rest).filter(
      ([key]) => !CUSTOM_SESSION_VIEW_PROP_KEYS.has(key as keyof AgentSessionView_01Props)
    )
  ) as React.ComponentProps<'section'>;

  const session = useSessionContext();
  const { messages } = useSessionMessages(session);
  const { state: agentState } = useAgent();

  // Transcript stays open for the whole session. Text input stays available;
  // the old chat-toggle control is hidden so the transcript is never tucked away.
  const controls: AgentControlBarControls = {
    leave: true,
    microphone: true,
    chat: false,
    camera: supportsVideoInput,
    screenShare: supportsScreenShare,
  };

  return (
    <section
      ref={ref}
      className={cn(
        'bg-background relative z-10 h-full w-full overflow-x-hidden overflow-y-hidden',
        className
      )}
      {...domProps}
    >
      <SessionStatusBadge />
      <Fade top className="absolute inset-x-4 top-0 z-10 h-28" />

      {/* Status → Voice stage → Transcript → Controls */}
      <div className="absolute inset-x-0 top-14 z-20 sm:top-16">
        <VoiceStagePanel
          audioVisualizerColor={audioVisualizerColor}
          audioVisualizerColorShift={audioVisualizerColorShift}
          audioVisualizerWaveLineWidth={audioVisualizerWaveLineWidth}
        />
      </div>

      {/* Transcript below the voice stage */}
      <div className="animate-in fade-in absolute inset-x-3 top-[300px] bottom-[150px] z-30 flex min-h-0 flex-col duration-500 sm:inset-x-6 sm:top-[340px] md:inset-x-12 md:bottom-[190px]">
        <AgentChatTranscript
          agentState={agentState}
          messages={messages}
          className="mx-auto h-full w-full max-w-2xl"
        />
      </div>

      {/* Bottom controls */}
      <motion.div
        {...BOTTOM_VIEW_MOTION_PROPS}
        className="absolute inset-x-3 bottom-0 z-50 md:inset-x-12"
      >
        <div className="bg-background relative mx-auto max-w-2xl pb-3 md:pb-12">
          <Fade bottom className="absolute inset-x-0 top-0 h-4 -translate-y-full" />
          <AgentControlBar
            variant="livekit"
            controls={controls}
            isChatOpen={supportsChatInput}
            isConnected={session.isConnected}
            onDisconnect={session.end}
            onDeviceError={({ source, error }) => {
              onMicrophoneError?.(error, source);
            }}
          />
        </div>
      </motion.div>
    </section>
  );
}
