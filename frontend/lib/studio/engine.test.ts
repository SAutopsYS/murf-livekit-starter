import { describe, expect, it } from 'vitest';
import { getStudioCommands } from '@/lib/studio/commands';
import { createDocument, createProject, emptyStudio, startWorkflow } from '@/lib/studio/engine';

describe('studio engine', () => {
  it('creates projects and documents without a UI editor', () => {
    let snap = emptyStudio();
    snap = createProject(snap, 'Unit 1');
    snap = createDocument(snap, 'Notes', 'notes');
    snap = startWorkflow(snap, 'summarize');
    expect(snap.metrics.projectCount).toBe(1);
    expect(snap.documents[0]?.kind).toBe('notes');
    expect(snap.workflows[0]?.title).toBe('summarize');
    expect(getStudioCommands().every((item) => item.planned)).toBe(true);
  });
});
