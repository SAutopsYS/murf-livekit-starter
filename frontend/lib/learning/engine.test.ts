import { describe, expect, it } from 'vitest';
import type { AnalyticsSummary } from '@/lib/analytics';
import { buildLearningIntelligence } from '@/lib/learning/engine';

const emptyAnalytics: AnalyticsSummary = {
  total_calls: 0,
  successful_calls: 0,
  failed_calls: 0,
  success_rate: 0,
  failure_rate: 0,
  failure_categories: {},
  recent_calls: [],
  performance: { average_call_duration_seconds: 0, average_first_response_ms: 0 },
  language_breakdown: {},
  channel_breakdown: {},
  insights: null,
};

describe('learning intelligence', () => {
  it('projects an empty window as a new learner without inventing scores', () => {
    const intel = buildLearningIntelligence(emptyAnalytics, null);
    expect(intel.phase).toBe('new');
    expect(intel.metrics.participation).toBe(0);
    expect(intel.profile.source).toBe('projected');
  });

  it('marks completed practice from analytics outcomes', () => {
    const intel = buildLearningIntelligence(
      {
        ...emptyAnalytics,
        total_calls: 2,
        successful_calls: 2,
        success_rate: 1,
        recent_calls: [
          {
            call_id: 'c1',
            started_at: '2026-08-01T00:00:00Z',
            ended_at: null,
            duration_seconds: 40,
            channel: 'browser',
            outcome: 'success',
            failure_type: null,
          },
        ],
      },
      null
    );
    expect(intel.timeline.length).toBeGreaterThan(0);
    expect(intel.recommendations.some((item) => item.kind === 'conversation')).toBe(true);
  });
});
