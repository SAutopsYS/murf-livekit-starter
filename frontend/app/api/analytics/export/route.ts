import { NextResponse } from 'next/server';
import { runAnalyticsCli } from '@/lib/analytics-backend';
import { platformRoute } from '@/lib/platform/http';
import { validateQueryToken } from '@/lib/platform/security';

export const revalidate = 0;

export async function GET(req: Request) {
  return platformRoute(
    req,
    { permission: 'analytics.export', rateLimit: 'api', metric: 'analytics.export' },
    async () => {
      const { searchParams } = new URL(req.url);
      const preset = searchParams.get('preset');
      const startDate = searchParams.get('start_date');
      const endDate = searchParams.get('end_date');
      const channel = searchParams.get('channel');
      const outcome = searchParams.get('outcome');

      if (
        !validateQueryToken(preset, 'preset') ||
        !validateQueryToken(startDate, 'date') ||
        !validateQueryToken(endDate, 'date') ||
        !validateQueryToken(channel, 'token') ||
        !validateQueryToken(outcome, 'token')
      ) {
        return NextResponse.json({ error: true, message: 'Invalid query.' }, { status: 400 });
      }

      const payload = await runAnalyticsCli('report', {
        preset,
        start_date: startDate,
        end_date: endDate,
        channel,
        outcome,
      });

      if (payload.error) {
        return NextResponse.json(
          { error: true, message: 'Unable to export analytics report.' },
          { status: 503 }
        );
      }
      return NextResponse.json(payload);
    }
  );
}
