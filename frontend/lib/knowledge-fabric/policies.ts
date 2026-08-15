export const KNOWLEDGE_POLICIES = {
  noUtterances: true,
  requireConsentForLongTerm: true,
  defaultTtlSeconds: null as number | null,
  minConfidenceToVerify: 0.8,
  conflict: 'keep_higher_confidence' as const,
  privacy: 'aggregate_until_consented' as const,
} as const;

export function mayPersistLongTerm(consented: boolean, containsUtterance: boolean): boolean {
  if (containsUtterance) return false;
  if (KNOWLEDGE_POLICIES.requireConsentForLongTerm && !consented) return false;
  return true;
}
