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

export async function runEnterpriseCli(
  command: 'snapshot' | 'decide' | 'export' | 'search',
  options: {
    text?: string;
    format?: string;
    kind?: string;
    query?: string;
  } = {}
): Promise<Record<string, unknown>> {
  const args = ['-m', 'enterprise.cli', command];
  if (options.text) args.push('--text', options.text);
  if (options.format) args.push('--format', options.format);
  if (options.kind) args.push('--kind', options.kind);
  if (options.query) args.push('--query', options.query);

  const { stdout } = await execFileAsync(pythonExecutable(), args, {
    cwd: backendRoot(),
    env: {
      ...process.env,
      PYTHONPATH: path.join(backendRoot(), 'src'),
    },
    timeout: 20000,
    windowsHide: true,
  });

  const trimmed = stdout.trim();
  if (!trimmed) {
    return { error: true, message: 'Enterprise data unavailable.' };
  }
  return JSON.parse(trimmed) as Record<string, unknown>;
}
