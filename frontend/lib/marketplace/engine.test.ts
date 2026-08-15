import { describe, expect, it } from 'vitest';
import {
  buildMarketplaceSnapshot,
  mayExecutePlugin,
  searchCatalog,
} from '@/lib/marketplace/engine';

describe('marketplace', () => {
  it('catalogs existing specialists and never executes', () => {
    const snap = buildMarketplaceSnapshot();
    expect(snap.catalog.some((item) => item.id === 'pkg.math-specialist')).toBe(true);
    expect(mayExecutePlugin()).toBe(false);
    expect(searchCatalog(snap, 'math').length).toBe(1);
    expect(snap.sandbox.executionPolicy).toBe('no_arbitrary_code');
  });
});
