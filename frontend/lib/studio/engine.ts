import type {
  PromptTemplate,
  StudioRecord,
  StudioSnapshot,
  StudioWorkflowKind,
} from '@/lib/studio/types';

function stamp(): string {
  return new Date().toISOString();
}

function record(kind: StudioRecord['kind'], title: string, owner = 'local'): StudioRecord {
  const at = stamp();
  return {
    id: `${kind}:${title.toLowerCase().replace(/\s+/g, '-')}`,
    title,
    kind,
    owner,
    organization: null,
    permissions: ['studio.access'],
    tags: [],
    createdAt: at,
    updatedAt: at,
    metadata: {},
  };
}

const DEFAULT_PROMPTS: PromptTemplate[] = [
  {
    id: 'prompt:explain',
    title: 'Explain',
    body: 'Explain {{topic}} at {{level}} without inventing a second voice.',
    variables: ['topic', 'level'],
    version: 1,
  },
  {
    id: 'prompt:summarize',
    title: 'Summarize',
    body: 'Summarize {{source}} for a {{audience}}. No utterance paste.',
    variables: ['source', 'audience'],
    version: 1,
  },
];

export function emptyStudio(): StudioSnapshot {
  return {
    projects: [],
    documents: [],
    workflows: [],
    prompts: DEFAULT_PROMPTS,
    metrics: { projectCount: 0, documentCount: 0 },
  };
}

export function createProject(snapshot: StudioSnapshot, title: string): StudioSnapshot {
  const project = record('project', title);
  const projects = [...snapshot.projects, project];
  return { ...snapshot, projects, metrics: { ...snapshot.metrics, projectCount: projects.length } };
}

export function createDocument(
  snapshot: StudioSnapshot,
  title: string,
  kind: StudioRecord['kind'] = 'notes'
): StudioSnapshot {
  const documents = [...snapshot.documents, record(kind, title)];
  return {
    ...snapshot,
    documents,
    metrics: { ...snapshot.metrics, documentCount: documents.length },
  };
}

export function startWorkflow(snapshot: StudioSnapshot, kind: StudioWorkflowKind): StudioSnapshot {
  return { ...snapshot, workflows: [...snapshot.workflows, record('workflow', kind)] };
}

export function applyTemplate(snapshot: StudioSnapshot, templateId: string): PromptTemplate | null {
  return snapshot.prompts.find((item) => item.id === templateId) ?? null;
}

export function buildStudioSnapshot(seed?: Partial<StudioSnapshot>): StudioSnapshot {
  const base = emptyStudio();
  return {
    ...base,
    ...seed,
    prompts: seed?.prompts ?? base.prompts,
    metrics: {
      projectCount: seed?.projects?.length ?? 0,
      documentCount: seed?.documents?.length ?? 0,
    },
  };
}
