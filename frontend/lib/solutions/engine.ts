export const INDUSTRIES = [
  'school',
  'university',
  'coaching',
  'corporate',
  'government',
  'ngo',
  'healthcare_education',
] as const;

export type Industry = (typeof INDUSTRIES)[number];
