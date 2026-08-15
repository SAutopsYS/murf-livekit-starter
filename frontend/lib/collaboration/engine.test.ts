import { describe, expect, it } from 'vitest';
import { emptyCollaboration, joinSession } from '@/lib/collaboration/engine';

describe('collaboration', () => {
  it('joins a studio session without a CRDT', () => {
    const snap = joinSession(emptyCollaboration(), 'studio', 'u1');
    expect(snap.crdt).toBe(false);
    expect(snap.sessionKind).toBe('studio');
    expect(snap.participants).toHaveLength(1);
  });
});
