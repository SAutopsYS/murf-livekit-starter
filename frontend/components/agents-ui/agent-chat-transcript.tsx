'use client';

import { type ComponentProps, memo, useMemo } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { type AgentState, type ReceivedMessage } from '@livekit/components-react';
import { GraduationCapIcon, UserIcon } from '@phosphor-icons/react';
import { AgentChatIndicator } from '@/components/agents-ui/agent-chat-indicator';
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import { MessageResponse } from '@/components/ai-elements/message';
import { cn } from '@/lib/shadcn/utils';

export interface AgentChatTranscriptProps extends ComponentProps<'div'> {
  agentState?: AgentState;
  messages?: ReceivedMessage[];
  className?: string;
}

const TranscriptMessage = memo(function TranscriptMessage({
  id,
  timestamp,
  message,
  isUser,
  locale,
}: {
  id: string;
  timestamp: number;
  message: string;
  isUser: boolean;
  locale: string;
}) {
  const timeLabel = useMemo(
    () =>
      new Date(timestamp).toLocaleTimeString(locale, {
        hour: 'numeric',
        minute: '2-digit',
      }),
    [timestamp, locale]
  );

  return (
    <motion.div
      key={id}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={cn('flex w-full gap-2.5', isUser ? 'flex-row-reverse' : 'flex-row')}
    >
      <div
        className={cn(
          'mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-full border shadow-sm backdrop-blur-md',
          isUser
            ? 'border-sky-300/40 bg-sky-500/10 text-sky-700 dark:text-sky-300'
            : 'text-foreground border-white/40 bg-white/55 dark:border-white/10 dark:bg-white/10'
        )}
      >
        {isUser ? (
          <UserIcon weight="bold" aria-hidden className="size-4" />
        ) : (
          <GraduationCapIcon weight="bold" aria-hidden className="size-4" />
        )}
      </div>

      <div className={cn('flex max-w-[70%] flex-col gap-1', isUser && 'items-end')}>
        <div
          className={cn(
            'rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm',
            isUser
              ? 'rounded-br-md bg-linear-to-br from-sky-500 to-cyan-500 text-white shadow-sky-500/20'
              : 'text-foreground rounded-bl-md border border-white/45 bg-white/60 shadow-[0_8px_24px_-16px_rgba(15,23,42,0.35)] backdrop-blur-md dark:border-white/10 dark:bg-white/10'
          )}
        >
          <MessageResponse className="[&_*]:text-inherit">{message}</MessageResponse>
        </div>
        <span className="text-muted-foreground px-1 text-[10px] tracking-wide">{timeLabel}</span>
      </div>
    </motion.div>
  );
});

function ThinkingRow() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 4 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className="flex w-full items-center gap-2"
    >
      <div className="flex size-8 shrink-0 items-center justify-center rounded-full border border-white/40 bg-white/50 shadow-sm backdrop-blur-md dark:border-white/10 dark:bg-white/10">
        <GraduationCapIcon weight="bold" className="size-4" />
      </div>
      <div className="flex items-center gap-2 rounded-2xl rounded-bl-md border border-white/40 bg-white/55 px-4 py-3 text-sm shadow-sm backdrop-blur-md dark:border-white/10 dark:bg-white/10">
        <AgentChatIndicator size="sm" />
        <span className="text-muted-foreground">AI Tutor is thinking...</span>
      </div>
    </motion.div>
  );
}

/**
 * Live chat transcript for the voice session.
 * Uses LiveKit session messages; always intended to stay visible during a call.
 */
export function AgentChatTranscript({
  agentState,
  messages = [],
  className,
  ...props
}: AgentChatTranscriptProps) {
  const locale = useMemo(
    () => (typeof navigator !== 'undefined' ? navigator.language : 'en-US'),
    []
  );

  return (
    <div
      className={cn(
        'flex h-full min-h-0 flex-col overflow-hidden rounded-3xl border border-white/40 bg-white/45 shadow-[0_16px_48px_-24px_rgba(15,23,42,0.35)] backdrop-blur-xl dark:border-white/10 dark:bg-white/5',
        className
      )}
      {...props}
    >
      <div className="border-border/40 text-muted-foreground border-b px-4 py-2.5 text-center text-[11px] font-medium tracking-wide uppercase">
        Live Transcript
      </div>

      <Conversation className="min-h-0 flex-1" aria-label="Conversation transcript">
        <ConversationContent className="gap-5 p-3.5 sm:gap-6 sm:p-5">
          {messages.length === 0 && agentState !== 'thinking' && (
            <div className="animate-in fade-in flex flex-1 flex-col items-center justify-center px-4 py-10 text-center duration-500">
              <p aria-hidden className="mb-2 text-2xl">
                👋
              </p>
              <p className="text-foreground text-sm font-medium sm:text-base">
                Start speaking whenever you&apos;re ready.
              </p>
              <p className="text-muted-foreground mt-1 text-xs sm:text-sm">
                Your conversation will appear here.
              </p>
            </div>
          )}

          {messages.map((receivedMessage) => {
            const { id, timestamp, from, message } = receivedMessage;
            return (
              <TranscriptMessage
                key={id}
                id={id}
                timestamp={timestamp}
                message={message}
                isUser={Boolean(from?.isLocal)}
                locale={locale}
              />
            );
          })}

          <AnimatePresence mode="wait">
            {agentState === 'thinking' && <ThinkingRow key="thinking" />}
          </AnimatePresence>
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>
    </div>
  );
}
