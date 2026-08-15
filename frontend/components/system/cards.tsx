import type { ReactNode } from 'react';
import { Card, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/shadcn/utils';

function GlassCard({
  title,
  children,
  className,
}: {
  title?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Card variant="glass" className={className}>
      {title ? <CardTitle>{title}</CardTitle> : null}
      {children}
    </Card>
  );
}

function Panel({
  title,
  children,
  className,
}: {
  title?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Card variant="default" padding="lg" className={className}>
      {title ? <CardTitle>{title}</CardTitle> : null}
      {children}
    </Card>
  );
}

function Widget({
  title,
  children,
  className,
}: {
  title?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Card variant="sunken" className={className}>
      {title ? <CardTitle>{title}</CardTitle> : null}
      {children}
    </Card>
  );
}

function FloatingPanel({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <Card variant="glass" padding="sm" className={cn('shadow-salora-lg', className)}>
      {children}
    </Card>
  );
}

function VoicePanel({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <Card variant="glass" padding="lg" data-slot="voice-panel" className={className}>
      {children}
    </Card>
  );
}

function MissionCard({
  title,
  children,
  className,
}: {
  title: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Card variant="glass" data-slot="mission-card" className={className}>
      <CardTitle>{title}</CardTitle>
      {children}
    </Card>
  );
}

function InsightCard({
  title,
  children,
  className,
}: {
  title: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <Card variant="default" data-slot="insight-card" className={className}>
      <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
      <div className="mt-3">{children}</div>
    </Card>
  );
}

function TimelineCard({
  timestamp,
  title,
  children,
  className,
}: {
  timestamp?: string;
  title: string;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <li
      data-slot="timeline-card"
      className={cn(
        'border-border bg-card rounded-[var(--salora-radius-cluster)] border p-3',
        className
      )}
    >
      {timestamp ? <p className="text-muted-foreground text-xs">{timestamp}</p> : null}
      <p className="font-medium">{title}</p>
      {children}
    </li>
  );
}

export {
  GlassCard,
  Panel,
  Widget,
  FloatingPanel,
  VoicePanel,
  MissionCard,
  InsightCard,
  TimelineCard,
};
