import { NextResponse } from 'next/server';
import { runEnterpriseCli } from '@/lib/enterprise-backend';

export const revalidate = 0;

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const command = (searchParams.get('command') || 'snapshot') as
      | 'snapshot'
      | 'decide'
      | 'search';
    const payload = await runEnterpriseCli(command, {
      text: searchParams.get('text') || undefined,
      query: searchParams.get('query') || undefined,
    });
    if (payload.error) {
      return NextResponse.json(payload, { status: 503 });
    }
    return NextResponse.json(payload);
  } catch {
    return NextResponse.json(
      { error: true, message: 'Enterprise data is temporarily unavailable.' },
      { status: 503 }
    );
  }
}
