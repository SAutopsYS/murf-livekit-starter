import type { OsCommand } from '@/lib/os-commands';

export function getStudioCommands(): OsCommand[] {
  return [
    {
      id: 'studio:open-project',
      label: 'Open Project',
      kind: 'ai',
      planned: true,
      keywords: 'studio project open',
    },
    {
      id: 'studio:search-project',
      label: 'Search Project',
      kind: 'search',
      planned: true,
      keywords: 'studio search project',
    },
    {
      id: 'studio:create-document',
      label: 'Create Document',
      kind: 'ai',
      planned: true,
      keywords: 'studio document create',
    },
    {
      id: 'studio:run-workflow',
      label: 'Run Workflow',
      kind: 'ai',
      planned: true,
      keywords: 'studio workflow',
    },
    {
      id: 'studio:open-prompt',
      label: 'Open Prompt',
      kind: 'ai',
      planned: true,
      keywords: 'studio prompt',
    },
    {
      id: 'studio:open-notebook',
      label: 'Open Notebook',
      kind: 'ai',
      planned: true,
      keywords: 'studio notebook',
    },
    {
      id: 'studio:search-assets',
      label: 'Search Assets',
      kind: 'search',
      planned: true,
      keywords: 'studio assets',
    },
  ];
}
