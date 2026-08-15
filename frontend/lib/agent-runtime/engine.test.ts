import { describe, expect, it } from 'vitest';
import { buildAgentRuntime } from '@/lib/agent-runtime/engine';

describe('agent runtime', () => {
  it('hosts the tutor and defers routing', () => {
    const snap = buildAgentRuntime();
    expect(snap.routingAuthority).toBe('specialist.router');
    expect(snap.autonomousLoops).toBe(false);
    expect(snap.agents[0]?.kind).toBe('tutor');
  });
});
