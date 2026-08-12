import { NextResponse } from 'next/server';
import { runAnalyticsCli } from '@/lib/analytics-backend';

export const revalidate = 0;

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const payload = await runAnalyticsCli('summary', {
      preset: searchParams.get('preset'),
      start_date: searchParams.get('start_date'),
      end_date: searchParams.get('end_date'),
      channel: searchParams.get('channel'),
      outcome: searchParams.get('outcome'),
    });

    if (payload.error) {
      return NextResponse.json(payload, { status: 503 });
    }
    return NextResponse.json(payload);
  } catch {
    return NextResponse.json(
      { error: true, message: 'Analytics are temporarily unavailable.' },
      { status: 503 }
    );
  }
}
