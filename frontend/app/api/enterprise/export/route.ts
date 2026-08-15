import { NextResponse } from 'next/server';
import { runEnterpriseCli } from '@/lib/enterprise-backend';
import { platformRoute } from '@/lib/platform/http';
import { validateQueryToken } from '@/lib/platform/security';

export const revalidate = 0;

export async function GET(req: Request) {
  return platformRoute(
    req,
    { permission: 'enterprise.export', rateLimit: 'api', metric: 'enterprise.export' },
    async () => {
      const { searchParams } = new URL(req.url);
      const kind = searchParams.get('kind') || 'report';
      const format = searchParams.get('format') || 'json';
      if (!validateQueryToken(kind, 'token') || !validateQueryToken(format, 'token')) {
        return NextResponse.json({ error: true, message: 'Invalid query.' }, { status: 400 });
      }
      const payload = await runEnterpriseCli('export', { kind, format });
      if (payload.error) {
        return NextResponse.json(payload, { status: 503 });
      }
      return NextResponse.json(payload);
    }
  );
}
