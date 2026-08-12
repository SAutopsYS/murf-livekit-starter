import { execFile } from 'node:child_process';
import path from 'node:path';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

function backendRoot(): string {
  return path.resolve(process.cwd(), '..', 'backend');
}

function pythonExecutable(): string {
  const root = backendRoot();
  if (process.platform === 'win32') {
    return path.join(root, '.venv', 'Scripts', 'python.exe');
  }
  return path.join(root, '.venv', 'bin', 'python');
}

export type AnalyticsQuery = {
  preset?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  channel?: string | null;
  outcome?: string | null;
};

export async function runAnalyticsCli(
  command: 'summary' | 'report' | 'metrics',
  query: AnalyticsQuery = {}
): Promise<Record<string, unknown>> {
  const args = ['-m', 'analytics.cli', command];
  if (query.preset) args.push('--preset', query.preset);
  if (query.start_date) args.push('--start-date', query.start_date);
  if (query.end_date) args.push('--end-date', query.end_date);
  if (query.channel) args.push('--channel', query.channel);
  if (query.outcome) args.push('--outcome', query.outcome);

  const { stdout } = await execFileAsync(pythonExecutable(), args, {
    cwd: backendRoot(),
    env: {
      ...process.env,
      PYTHONPATH: path.join(backendRoot(), 'src'),
    },
    timeout: 15000,
    windowsHide: true,
  });

  const trimmed = stdout.trim();
  if (!trimmed) {
    return { error: true, message: 'Analytics data unavailable.' };
  }
  return JSON.parse(trimmed) as Record<string, unknown>;
}
