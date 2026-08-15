'use client';

import { useMemo, useState } from 'react';
import { useTheme } from 'next-themes';
import { useRouter } from 'next/navigation';
import { Command } from 'cmdk';
import { toast } from 'sonner';
import { useOs } from '@/components/os/os-provider';
import { CommandItem } from '@/components/system';
import { Dialog, DialogContent, DialogDescription, DialogTitle } from '@/components/ui/dialog';
import {
  COMMAND_KIND_LABEL,
  type OsCommand,
  type OsCommandKind,
  getStaticCommands,
} from '@/lib/os-commands';

const KIND_ORDER: OsCommandKind[] = [
  'navigation',
  'action',
  'search',
  'shortcut',
  'settings',
  'ai',
  'agent',
];

export function OsCommandPalette() {
  const router = useRouter();
  const { setTheme } = useTheme();
  const { commandOpen, setCommandOpen, extraCommands, searchHits, runSearch } = useOs();
  const [query, setQuery] = useState('');

  const commands = useMemo(() => {
    const seen = new Set<string>();
    const merged: OsCommand[] = [];
    for (const item of [...getStaticCommands(), ...extraCommands, ...searchHits]) {
      if (seen.has(item.id)) continue;
      seen.add(item.id);
      merged.push(item);
    }
    return merged;
  }, [extraCommands, searchHits]);

  const grouped = useMemo(() => {
    const map = new Map<OsCommandKind, OsCommand[]>();
    for (const item of commands) {
      const list = map.get(item.kind) ?? [];
      list.push(item);
      map.set(item.kind, list);
    }
    return KIND_ORDER.filter((kind) => map.has(kind)).map((kind) => ({
      kind,
      items: map.get(kind) ?? [],
    }));
  }, [commands]);

  const run = (item: OsCommand) => {
    if (item.id === 'action:search') return;
    if (item.planned) {
      toast.message(`${item.label} is planned. Not built yet.`);
      setCommandOpen(false);
      return;
    }
    if (item.id === 'action:theme-dark') setTheme('dark');
    if (item.id === 'action:theme-light') setTheme('light');
    if (item.id === 'action:theme-system') setTheme('system');
    item.run?.();
    if (item.href) router.push(item.href);
    setCommandOpen(false);
    setQuery('');
  };

  return (
    <Dialog
      open={commandOpen}
      onOpenChange={(open) => {
        setCommandOpen(open);
        if (!open) {
          setQuery('');
          void runSearch('');
        }
      }}
    >
      <DialogContent className="top-[20%] translate-y-0 p-0 sm:max-w-xl">
        <DialogTitle className="sr-only">Command palette</DialogTitle>
        <DialogDescription className="sr-only">
          Navigate SALORA OS, run quick actions, or search.
        </DialogDescription>
        <Command label="SALORA OS commands" className="flex flex-col" shouldFilter>
          <Command.Input
            value={query}
            onValueChange={(value) => {
              setQuery(value);
              void runSearch(value);
            }}
            placeholder="Search pages, actions, agents…"
            className="border-border placeholder:text-muted-foreground w-full border-b bg-transparent px-4 py-3 text-sm outline-none"
          />
          <Command.List className="max-h-80 overflow-auto p-2">
            <Command.Empty className="text-muted-foreground px-3 py-6 text-center text-sm">
              No matching commands.
            </Command.Empty>
            {grouped.map((group) => (
              <Command.Group
                key={group.kind}
                heading={COMMAND_KIND_LABEL[group.kind]}
                className="text-muted-foreground [&_[cmdk-group-heading]]:px-3 [&_[cmdk-group-heading]]:py-2 [&_[cmdk-group-heading]]:text-[11px] [&_[cmdk-group-heading]]:font-bold [&_[cmdk-group-heading]]:tracking-[0.14em] [&_[cmdk-group-heading]]:uppercase"
              >
                {group.items.map((item) => (
                  <Command.Item
                    key={item.id}
                    value={`${item.label} ${item.keywords ?? ''} ${item.hint ?? ''}`}
                    onSelect={() => run(item)}
                    asChild
                  >
                    <CommandItem>
                      <span className="flex w-full items-center justify-between gap-3">
                        <span>{item.label}</span>
                        <span className="text-muted-foreground text-xs">
                          {item.planned ? 'Soon' : item.hint}
                        </span>
                      </span>
                    </CommandItem>
                  </Command.Item>
                ))}
              </Command.Group>
            ))}
          </Command.List>
        </Command>
      </DialogContent>
    </Dialog>
  );
}
