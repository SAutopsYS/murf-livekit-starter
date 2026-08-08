'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useTheme } from 'next-themes';
import { ConnectionState, Track } from 'livekit-client';
import { AnimatePresence, motion } from 'motion/react';
import { SessionEvent, useAgent, useChat, useSessionContext } from '@livekit/components-react';
import type { AppConfig } from '@/app-config';
import { AgentSessionView_01 } from '@/components/agents-ui/blocks/agent-session-view-01';
import { ConnectingView } from '@/components/app/connecting-view';
import { MicrophonePermissionView } from '@/components/app/microphone-permission-view';
import { SessionEndedView } from '@/components/app/session-ended-view';
import { WelcomeView } from '@/components/app/welcome-view';
import { isMicrophonePermissionError } from '@/lib/microphone-errors';

const MotionWelcomeView = motion.create(WelcomeView);
const MotionConnectingView = motion.create(ConnectingView);
const MotionSessionEndedView = motion.create(SessionEndedView);
const MotionMicrophonePermissionView = motion.create(MicrophonePermissionView);
const MotionSessionView = motion.create(AgentSessionView_01);

const VIEW_MOTION_PROPS = {
  variants: {
    visible: {
      opacity: 1,
    },
    hidden: {
      opacity: 0,
    },
  },
  initial: 'hidden',
  animate: 'visible',
  exit: 'hidden',
  transition: {
    duration: 0.4,
    ease: 'easeOut',
  },
};

type Screen = 'ready' | 'connecting' | 'session' | 'ended' | 'mic-error';

interface ViewControllerProps {
  appConfig: AppConfig;
}

export function ViewController({ appConfig }: ViewControllerProps) {
  const session = useSessionContext();
  const { isConnected, start, end, connectionState } = session;
  const { send } = useChat();
  const agent = useAgent();
  const { resolvedTheme } = useTheme();
  const [showEnded, setShowEnded] = useState(false);
  const [micDenied, setMicDenied] = useState(false);
  const [pendingPrompt, setPendingPrompt] = useState<string | null>(null);
  const hadConnectedRef = useRef(false);
  const promptSentRef = useRef(false);

  const handleMicrophoneError = useCallback(
    (error: Error, source?: Track.Source) => {
      if (!isMicrophonePermissionError(error, source)) {
        return;
      }
      setMicDenied(true);
      setPendingPrompt(null);
      promptSentRef.current = false;
      void end();
    },
    [end]
  );

  useEffect(() => {
    const onMediaError = (error: Error) => {
      handleMicrophoneError(error, Track.Source.Microphone);
    };

    session.internal.emitter.on(SessionEvent.MediaDevicesError, onMediaError);
    return () => {
      session.internal.emitter.off(SessionEvent.MediaDevicesError, onMediaError);
    };
  }, [session.internal.emitter, handleMicrophoneError]);

  useEffect(() => {
    if (isConnected) {
      hadConnectedRef.current = true;
      setShowEnded(false);
      setMicDenied(false);
      return;
    }

    if (hadConnectedRef.current && connectionState === ConnectionState.Disconnected && !micDenied) {
      setShowEnded(true);
      setPendingPrompt(null);
      promptSentRef.current = false;
    }
  }, [isConnected, connectionState, micDenied]);

  useEffect(() => {
    if (!isConnected || !pendingPrompt || promptSentRef.current) {
      return;
    }

    const state = String(agent.state);
    const agentReady =
      ('canListen' in agent && Boolean(agent.canListen)) ||
      state === 'idle' ||
      state === 'listening' ||
      state === 'thinking' ||
      state === 'speaking' ||
      state === 'pre-connect-buffering';

    if (!agentReady) {
      return;
    }

    promptSentRef.current = true;
    void send(pendingPrompt)
      .catch((error) => {
        console.error('Failed to send practice suggestion:', error);
        promptSentRef.current = false;
      })
      .finally(() => {
        setPendingPrompt(null);
      });
  }, [isConnected, pendingPrompt, agent, send]);

  const beginSession = useCallback(
    async (prompt?: string | null) => {
      setMicDenied(false);
      setShowEnded(false);
      promptSentRef.current = false;
      setPendingPrompt(prompt ?? null);

      try {
        await start();
      } catch (error) {
        if (isMicrophonePermissionError(error)) {
          setMicDenied(true);
          setPendingPrompt(null);
          promptSentRef.current = false;
          return;
        }
        throw error;
      }
    },
    [start]
  );

  const isConnecting = connectionState === ConnectionState.Connecting;

  let screen: Screen = 'ready';
  if (micDenied) {
    screen = 'mic-error';
  } else if (isConnected) {
    screen = 'session';
  } else if (isConnecting) {
    screen = 'connecting';
  } else if (showEnded) {
    screen = 'ended';
  }

  return (
    <AnimatePresence mode="wait">
      {screen === 'ready' && (
        <MotionWelcomeView
          key="welcome"
          {...VIEW_MOTION_PROPS}
          startButtonText={appConfig.startButtonText}
          onStartCall={() => {
            void beginSession(null);
          }}
          onPracticeSuggestion={(prompt) => {
            void beginSession(prompt);
          }}
        />
      )}

      {screen === 'connecting' && <MotionConnectingView key="connecting" {...VIEW_MOTION_PROPS} />}

      {screen === 'mic-error' && (
        <MotionMicrophonePermissionView
          key="mic-error"
          {...VIEW_MOTION_PROPS}
          onRetry={() => {
            void beginSession(null);
          }}
          onBack={() => {
            setMicDenied(false);
            setShowEnded(false);
            hadConnectedRef.current = false;
          }}
        />
      )}

      {screen === 'ended' && (
        <MotionSessionEndedView
          key="ended"
          {...VIEW_MOTION_PROPS}
          onPracticeAgain={() => {
            hadConnectedRef.current = false;
            void beginSession(null);
          }}
        />
      )}

      {screen === 'session' && (
        <MotionSessionView
          key="session-view"
          {...VIEW_MOTION_PROPS}
          supportsChatInput={appConfig.supportsChatInput}
          supportsVideoInput={appConfig.supportsVideoInput}
          supportsScreenShare={appConfig.supportsScreenShare}
          isPreConnectBufferEnabled={appConfig.isPreConnectBufferEnabled}
          audioVisualizerType={appConfig.audioVisualizerType}
          audioVisualizerColor={
            resolvedTheme === 'dark'
              ? appConfig.audioVisualizerColorDark
              : appConfig.audioVisualizerColor
          }
          audioVisualizerColorShift={appConfig.audioVisualizerColorShift}
          audioVisualizerBarCount={appConfig.audioVisualizerBarCount}
          audioVisualizerGridRowCount={appConfig.audioVisualizerGridRowCount}
          audioVisualizerGridColumnCount={appConfig.audioVisualizerGridColumnCount}
          audioVisualizerRadialBarCount={appConfig.audioVisualizerRadialBarCount}
          audioVisualizerRadialRadius={appConfig.audioVisualizerRadialRadius}
          audioVisualizerWaveLineWidth={appConfig.audioVisualizerWaveLineWidth}
          onMicrophoneError={handleMicrophoneError}
          className="fixed inset-0"
        />
      )}
    </AnimatePresence>
  );
}
