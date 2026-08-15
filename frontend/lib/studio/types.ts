export type StudioProjectKind =
  | 'project'
  | 'workspace'
  | 'folder'
  | 'asset'
  | 'document'
  | 'prompt'
  | 'conversation'
  | 'notebook'
  | 'workflow'
  | 'template';

export type StudioDocumentKind =
  | 'markdown'
  | 'rich_text'
  | 'whiteboard_ref'
  | 'code'
  | 'notes'
  | 'ai_output'
  | 'prompt'
  | 'research'
  | 'summary'
  | 'transcript_ref';

export type StudioWorkflowKind =
  | 'draft'
  | 'review'
  | 'improve'
  | 'translate'
  | 'explain'
  | 'summarize'
  | 'brainstorm'
  | 'generate'
  | 'analyze'
  | 'research';

export type StudioRecord = {
  id: string;
  title: string;
  kind: StudioProjectKind | StudioDocumentKind;
  owner: string;
  organization: string | null;
  permissions: string[];
  tags: string[];
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, string>;
};

export type PromptTemplate = {
  id: string;
  title: string;
  body: string;
  variables: string[];
  version: number;
};

export type StudioSnapshot = {
  projects: StudioRecord[];
  documents: StudioRecord[];
  workflows: StudioRecord[];
  prompts: PromptTemplate[];
  metrics: {
    projectCount: number;
    documentCount: number;
  };
};

export type StudioEventName =
  | 'ProjectCreated'
  | 'ProjectOpened'
  | 'DocumentUpdated'
  | 'WorkflowStarted'
  | 'WorkflowFinished'
  | 'PromptExecuted'
  | 'TemplateApplied'
  | 'AssetImported'
  | 'NotebookCreated';
