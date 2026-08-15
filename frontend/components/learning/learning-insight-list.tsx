'use client';

import { useLearning } from '@/components/learning/learning-provider';
import { InsightCard } from '@/components/system';
import { getLearningVisual } from '@/lib/learning/states';

export function LearningInsightList() {
  const { insights, visual, recommendations } = useLearning();

  return (
    <div data-slot="learning-insights" className="grid gap-4">
      <p className="sr-only">
        Learning state {visual.label}. {visual.meaning}
      </p>
      {insights.map((insight) => (
        <InsightCard key={insight.id} title={insight.title}>
          <p className="text-muted-foreground text-sm">{insight.body}</p>
        </InsightCard>
      ))}
      {recommendations.slice(0, 2).map((item) => (
        <InsightCard key={item.id} title={item.title}>
          <p className="text-muted-foreground text-sm">{item.reason}</p>
        </InsightCard>
      ))}
    </div>
  );
}

export function LearningStateLabel() {
  const { phase } = useLearning();
  const visual = getLearningVisual(phase);
  return (
    <span role="status" aria-label={visual.meaning} className="text-muted-foreground text-sm">
      {visual.label}
    </span>
  );
}
