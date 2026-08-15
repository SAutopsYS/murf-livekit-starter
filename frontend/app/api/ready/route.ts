import { NextResponse } from 'next/server';
import { readiness } from '@/lib/platform/health';

export const revalidate = 0;
export const dynamic = 'force-dynamic';

export async function GET() {
  const body = readiness();
  return NextResponse.json(body, {
    status: body.status === 'ready' ? 200 : 503,
    headers: { 'Cache-Control': 'no-store' },
  });
}
