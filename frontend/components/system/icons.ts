/**
 * Icon law for new SALORA UI.
 *
 * System: Phosphor (`@phosphor-icons/react`).
 * Weight: bold for controls, regular for meta.
 * Size: 16 default, 20 for hall commitments.
 * Always pair a commitment icon with a word.
 *
 * Do not rip Lucide from `components/agents-ui` or shadcn primitives
 * that already import it (select chevrons, sonner). New product UI
 * uses Phosphor only.
 */
export const ICON_SYSTEM = 'phosphor' as const;
export const ICON_WEIGHT_CONTROL = 'bold' as const;
export const ICON_SIZE_DEFAULT = 16;
export const ICON_SIZE_COMMITMENT = 20;
