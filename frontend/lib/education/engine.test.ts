import { describe, expect, it } from 'vitest';
import { EXPERIENCE_POLICIES, buildExperience } from '@/lib/education/engine';
import { listMentors } from '@/lib/mentors/engine';
import { INDUSTRIES } from '@/lib/solutions/engine';
import { STABILITY_RULES, V2_THEMES } from '@/lib/vision/engine';

describe('experience and vision', () => {
  it('projects learning for teacher and lists runtime mentors', () => {
    const exp = buildExperience('teacher');
    expect(exp.kind).toBe('teacher');
    expect(exp.source).toBe('learning-engine');
    expect(EXPERIENCE_POLICIES.scoresPersist).toBe(false);
    expect(listMentors().some((item) => item.kind === 'tutor')).toBe(true);
    expect(INDUSTRIES).toContain('school');
    expect(STABILITY_RULES).toContain('one_voice_path');
    expect(V2_THEMES).toContain('autonomous_ai_teams');
  });
});
