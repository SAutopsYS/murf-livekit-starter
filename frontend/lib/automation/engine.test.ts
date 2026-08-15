import { describe, expect, it } from 'vitest';
import { createAutomation } from '@/lib/automation/engine';
import { buildCloud } from '@/lib/cloud/engine';
import { buildDesktop } from '@/lib/desktop/engine';
import { checkCompliance } from '@/lib/governance/engine';
import { buildMobile } from '@/lib/mobile/engine';
import { buildProductivity } from '@/lib/productivity/engine';

describe('os v1 consumers', () => {
  it('keeps one automation shape and no client UIs', () => {
    expect(createAutomation('t', 'VoiceCompleted').nodes[0]).toBe('trigger');
    expect(buildProductivity().mailClient).toBe(false);
    expect(buildMobile().nativeUi).toBe(false);
    expect(buildDesktop().electron).toBe(false);
    expect(checkCompliance('GDPR').ok).toBe(true);
    expect(checkCompliance('HIPAA').ok).toBe(false);
    expect(buildCloud().speechLake).toBe(false);
  });
});
