'use client';

import { useAdaptive } from '@/components/adaptive/adaptive-provider';
import { InsightCard } from '@/components/system';
import { MASTERY_LABEL } from '@/lib/adaptive/mastery';

export function AdaptiveDecisionSummary() {
  const { decision, specialist, prediction } = useAdaptive();

  return (
    <InsightCard title="Adaptive decision">
      <p className="sr-only">{decision.explanation}</p>
      <p className="text-sm font-medium capitalize">{decision.action.replaceAll('_', ' ')}</p>
      <p className="text-muted-foreground mt-1 text-sm">{decision.reason}</p>
      <p className="text-muted-foreground mt-2 text-xs">
        Confidence {Math.round(decision.confidence * 100)}% · {specialist.specialist}
        {specialist.live ? '' : ' (planned)'}
      </p>
      <p className="text-muted-foreground mt-2 text-xs">
        Forecast {MASTERY_LABEL[prediction.masteryForecast]}. {prediction.explanation}
      </p>
    </InsightCard>
  );
}
