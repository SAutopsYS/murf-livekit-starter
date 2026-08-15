'use client';

import {
  type ReactNode,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { usePathname } from 'next/navigation';
import type { OsCommand } from '@/lib/os-commands';
import { type OsRoom, getOsRoom } from '@/lib/os-nav';

export type OsBrand = {
  companyName: string;
  logo: string;
  logoDark?: string;
};

type SearchHandler = (query: string) => Promise<OsCommand[]>;

type OsContextValue = {
  brand: OsBrand;
  room: OsRoom;
  commandOpen: boolean;
  setCommandOpen: (open: boolean) => void;
  extraCommands: OsCommand[];
  registerCommands: (commands: OsCommand[]) => () => void;
  searchHits: OsCommand[];
  setSearchHandler: (handler: SearchHandler | null) => void;
  runSearch: (query: string) => Promise<void>;
};

const OsContext = createContext<OsContextValue | null>(null);

export function useOs() {
  const ctx = useContext(OsContext);
  if (!ctx) throw new Error('useOs must be used inside OsProvider');
  return ctx;
}

export function OsProvider({ brand, children }: { brand: OsBrand; children: ReactNode }) {
  const pathname = usePathname() ?? '/';
  const room = getOsRoom(pathname);
  const [commandOpen, setCommandOpen] = useState(false);
  const [extraCommands, setExtraCommands] = useState<OsCommand[]>([]);
  const [searchHits, setSearchHits] = useState<OsCommand[]>([]);
  const searchRef = useRef<SearchHandler | null>(null);

  const registerCommands = useCallback((commands: OsCommand[]) => {
    setExtraCommands((prev) => [...prev, ...commands]);
    return () => {
      setExtraCommands((prev) =>
        prev.filter((item) => !commands.some((cmd) => cmd.id === item.id))
      );
    };
  }, []);

  const setSearchHandler = useCallback((handler: SearchHandler | null) => {
    searchRef.current = handler;
    if (!handler) setSearchHits([]);
  }, []);

  const runSearch = useCallback(async (query: string) => {
    if (!searchRef.current || query.trim().length < 2) {
      setSearchHits([]);
      return;
    }
    const hits = await searchRef.current(query);
    setSearchHits(hits);
  }, []);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setCommandOpen((open) => !open);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const value = useMemo(
    () => ({
      brand,
      room,
      commandOpen,
      setCommandOpen,
      extraCommands,
      registerCommands,
      searchHits,
      setSearchHandler,
      runSearch,
    }),
    [
      brand,
      room,
      commandOpen,
      extraCommands,
      registerCommands,
      searchHits,
      setSearchHandler,
      runSearch,
    ]
  );

  return <OsContext.Provider value={value}>{children}</OsContext.Provider>;
}
