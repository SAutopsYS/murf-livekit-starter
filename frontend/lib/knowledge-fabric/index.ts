export { buildKnowledgeFabric } from '@/lib/knowledge-fabric/engine';
export { retrieveKnowledge } from '@/lib/knowledge-fabric/retrieval';
export {
  strengthenNode,
  weakenNode,
  archiveNode,
  forgetNode,
  expireStale,
} from '@/lib/knowledge-fabric/lifecycle';
export { KNOWLEDGE_POLICIES, mayPersistLongTerm } from '@/lib/knowledge-fabric/policies';
export type {
  KnowledgeSnapshot,
  KnowledgeNode,
  KnowledgeEdge,
  KnowledgeNodeType,
  KnowledgeRelationKind,
  MemoryLayer,
  RetrievalQuery,
  KnowledgeEvent,
} from '@/lib/knowledge-fabric/types';
