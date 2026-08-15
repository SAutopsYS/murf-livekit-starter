import type {
  KnowledgeEdge,
  KnowledgeNode,
  KnowledgeRelationKind,
  KnowledgeSnapshot,
} from '@/lib/knowledge-fabric/types';

export type GraphNodeKind =
  | KnowledgeNode['type']
  | 'agent'
  | 'session'
  | 'project'
  | 'document'
  | 'whiteboard'
  | 'workflow';

export type GraphView = {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  focusId: string | null;
  breadcrumbs: string[];
  pins: string[];
  bookmarks: string[];
  zoom: number;
};

export type GraphQueryKind =
  | 'related'
  | 'similar'
  | 'learning_path'
  | 'weak'
  | 'strong'
  | 'history'
  | 'next'
  | 'by_skill'
  | 'by_topic'
  | 'by_confidence';

export type GraphQuery = {
  kind: GraphQueryKind;
  text?: string;
  limit?: number;
};

export type MemoryGraphSnapshot = {
  fabric: KnowledgeSnapshot;
  view: GraphView;
  source: 'knowledge-fabric';
};

export type { KnowledgeRelationKind };
