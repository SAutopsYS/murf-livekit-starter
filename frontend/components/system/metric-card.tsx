import type { ComponentProps } from 'react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/shadcn/utils';

function MetricCard({
  label,
  value,
  emphasize = false,
  className,
}: {
  label: string;
  value: string | number | null | undefined;
  emphasize?: boolean;
  className?: string;
}) {
  const display = value ?? '—';
  return (
    <Card
      variant="glass"
      data-slot="metric-card"
      aria-label={`${label}: ${display}`}
      className={cn(emphasize && 'ring-primary/20 ring-1', className)}
    >
      <p className="text-muted-foreground text-sm">{label}</p>
      <p className="text-foreground mt-2 text-3xl font-semibold tracking-tight">{display}</p>
    </Card>
  );
}

function StatCard(props: ComponentProps<typeof MetricCard>) {
  return <MetricCard {...props} />;
}

export { MetricCard, StatCard };
