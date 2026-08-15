import type { KnowledgeRelationKind } from '@/lib/knowledge-fabric/types';

export type WhiteboardElementKind =
  | 'text'
  | 'sticky'
  | 'shape'
  | 'image'
  | 'code'
  | 'markdown'
  | 'table'
  | 'diagram'
  | 'equation'
  | 'ai_block'
  | 'voice_block'
  | 'knowledge_ref'
  | 'document_ref'
  | 'workflow_ref';

export type WhiteboardRelationKind = KnowledgeRelationKind;

export type CanvasObject = {
  id: string;
  title: string;
  owner: string;
  createdAt: string;
  updatedAt: string;
  layers: string[];
};

export type WhiteboardElement = {
  id: string;
  canvasId: string;
  type: WhiteboardElementKind;
  bounds: { x: number; y: number; w: number; h: number };
  owner: string;
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, string>;
};

export type WhiteboardEdge = {
  id: string;
  kind: WhiteboardRelationKind;
  from: string;
  to: string;
};

export type ViewportState = {
  x: number;
  y: number;
  zoom: number;
};

export type WhiteboardSnapshot = {
  canvas: CanvasObject;
  elements: WhiteboardElement[];
  edges: WhiteboardEdge[];
  viewport: ViewportState;
  selection: string[];
};

export type WhiteboardAssistKind =
  | 'generate_diagram'
  | 'explain_diagram'
  | 'summarize_board'
  | 'create_flow'
  | 'expand_idea'
  | 'convert_to_notes'
  | 'convert_to_workflow'
  | 'create_mind_map'
  | 'analyze_structure';

export type CollabRole = 'owner' | 'editor' | 'commenter' | 'viewer';
