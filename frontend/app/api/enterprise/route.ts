import { NextResponse } from 'next/server';
import { runEnterpriseCli } from '@/lib/enterprise-backend';
import { platformRoute } from '@/lib/platform/http';
import { validateQueryToken } from '@/lib/platform/security';

export const revalidate = 0;

export async function GET(req: Request) {
  return platformRoute(
    req,
    { permission: 'enterprise.read', rateLimit: 'api', metric: 'enterprise.snapshot' },
    async () => {
      const { searchParams } = new URL(req.url);
      const command = searchParams.get('command') || 'snapshot';
      if (command !== 'snapshot' && command !== 'decide' && command !== 'search') {
        return NextResponse.json({ error: true, message: 'Invalid command.' }, { status: 400 });
      }
      const text = searchParams.get('text');
      const query = searchParams.get('query');
      if (!validateQueryToken(command, 'token')) {
        return NextResponse.json({ error: true, message: 'Invalid query.' }, { status: 400 });
      }

      const payload = await runEnterpriseCli(command, {
        text: text || undefined,
        query: query || undefined,
      });
      if (payload.error) {
        return NextResponse.json(payload, { status: 503 });
      }
      return NextResponse.json(payload);
    }
  );
}
