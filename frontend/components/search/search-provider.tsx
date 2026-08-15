'use client';

import { type ReactNode, createContext, useContext, useMemo } from 'react';
import type { KnowledgeSnapshot } from '@/lib/knowledge-fabric/types';
import { type SearchHit, searchUniversal } from '@/lib/search/engine';

const SearchContext = createContext<SearchHit[] | null>(null);

export function useSearch(): SearchHit[] {
  const ctx = useContext(SearchContext);
  if (!ctx) throw new Error('useSearch must be used inside SearchProvider');
  return ctx;
}

export function SearchProvider({
  query,
  fabric,
  children,
}: {
  query: string;
  fabric: KnowledgeSnapshot | null;
  children: ReactNode;
}) {
  const value = useMemo(() => searchUniversal(query, fabric), [query, fabric]);
  return <SearchContext.Provider value={value}>{children}</SearchContext.Provider>;
}
