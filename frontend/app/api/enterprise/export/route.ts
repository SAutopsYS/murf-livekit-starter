import { NextResponse } from 'next/server';
import { runEnterpriseCli } from '@/lib/enterprise-backend';

export const revalidate = 0;

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const payload = await runEnterpriseCli('export', {
      kind: searchParams.get('kind') || 'report',
      format: searchParams.get('format') || 'json',
    });
    if (payload.error) {
      return NextResponse.json(payload, { status: 503 });
    }
    return NextResponse.json(payload);
  } catch {
    return NextResponse.json(
      { error: true, message: 'Export is temporarily unavailable.' },
      { status: 503 }
    );
  }
}
