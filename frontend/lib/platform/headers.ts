/** Security headers only. Safe for next.config — no aliases, no env parse. */

export const SECURITY_HEADERS: Record<string, string> = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-DNS-Prefetch-Control': 'off',
  'Permissions-Policy': 'camera=(), microphone=(self), geolocation=(), payment=()',
  'X-Permitted-Cross-Domain-Policies': 'none',
};

export function productionSecurityHeaders(profile: string): Record<string, string> {
  if (profile !== 'production') return SECURITY_HEADERS;
  return {
    ...SECURITY_HEADERS,
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  };
}
