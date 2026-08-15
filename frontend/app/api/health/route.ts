import { NextResponse } from 'next/server';
import { liveness } from '@/lib/platform/health';

export const revalidate = 0;
export const dynamic = 'force-dynamic';

export async function GET() {
  return NextResponse.json(liveness(), {
    headers: { 'Cache-Control': 'no-store' },
  });
}
