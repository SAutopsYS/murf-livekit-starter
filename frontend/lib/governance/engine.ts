import { PRIVACY_RULES } from '@/lib/platform/security';

export type Framework = 'GDPR' | 'COPPA' | 'FERPA' | 'SOC2' | 'ISO27001' | 'HIPAA' | 'AI';

export function checkCompliance(framework: Framework): { framework: Framework; ok: boolean } {
  const base = PRIVACY_RULES.noUtteranceFields && PRIVACY_RULES.consentBeforeMemory;
  return { framework, ok: framework === 'HIPAA' ? false : base };
}
