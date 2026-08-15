export type MemoryLayer = 'working' | 'short_term' | 'long_term';

export type KnowledgeNodeType =
  | 'concept'
  | 'entity'
  | 'relationship'
  | 'evidence'
  | 'topic'
  | 'lesson'
  | 'rule'
  | 'observation'
  | 'correction'
  | 'question'
  | 'answer'
  | 'decision'
  | 'recommendation'
  | 'skill'
  | 'goal'
  | 'fact'
  | 'preference'
  | 'weakness'
  | 'strength'
  | 'context';

export type KnowledgeRelationKind =
  | 'depends_on'
  | 'related_to'
  | 'teaches'
  | 'corrects'
  | 'improves'
  | 'contradicts'
  | 'supports'
  | 'derived_from'
  | 'recommended_by'
  | 'belongs_to';

export type VerificationStatus = 'unverified' | 'projected' | 'consented' | 'verified';

export type KnowledgeNode = {
  id: string;
  type: KnowledgeNodeType;
  title: string;
  summary: string;
  confidence: number;
  importance: number;
  layer: MemoryLayer;
  source: string;
  createdAt: string;
  updatedAt: string;
  ttlSeconds: number | null;
  verification: VerificationStatus;
  references: string[];
};

export type KnowledgeEdge = {
  id: string;
  kind: KnowledgeRelationKind;
  from: string;
  to: string;
  confidence: number;
};

export type KnowledgeEventName =
  | 'KnowledgeCreated'
  | 'KnowledgeUpdated'
  | 'KnowledgeMerged'
  | 'MemoryStrengthened'
  | 'MemoryExpired'
  | 'RelationshipCreated'
  | 'RelationshipUpdated'
  | 'KnowledgeRetrieved'
  | 'KnowledgeVerified'
  | 'KnowledgeArchived';

export type KnowledgeEvent = {
  name: KnowledgeEventName;
  at: string;
  nodeId?: string;
};

export type RetrievalQuery = {
  text?: string;
  layer?: MemoryLayer;
  type?: KnowledgeNodeType;
  limit?: number;
};

export type KnowledgeSnapshot = {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  retrieved: KnowledgeNode[];
  metrics: {
    nodeCount: number;
    edgeCount: number;
    longTerm: number;
    working: number;
  };
};
