import type { AdaptiveSnapshot } from '@/lib/adaptive/types';
import { retrieveKnowledge } from '@/lib/knowledge-fabric/retrieval';
import type {
  KnowledgeEdge,
  KnowledgeNode,
  KnowledgeSnapshot,
  MemoryLayer,
  VerificationStatus,
} from '@/lib/knowledge-fabric/types';
import type { LearningIntelligence } from '@/lib/learning/types';

function now(): string {
  return new Date().toISOString();
}

function node(
  id: string,
  type: KnowledgeNode['type'],
  title: string,
  summary: string,
  extras?: Partial<KnowledgeNode>
): KnowledgeNode {
  const stamp = now();
  return {
    id,
    type,
    title,
    summary,
    confidence: extras?.confidence ?? 0.4,
    importance: extras?.importance ?? 0.5,
    layer: extras?.layer ?? 'short_term',
    source: extras?.source ?? 'projected',
    createdAt: extras?.createdAt ?? stamp,
    updatedAt: extras?.updatedAt ?? stamp,
    ttlSeconds: extras?.ttlSeconds ?? null,
    verification: extras?.verification ?? 'projected',
    references: extras?.references ?? [],
  };
}

function edge(
  kind: KnowledgeEdge['kind'],
  from: string,
  to: string,
  confidence = 0.5
): KnowledgeEdge {
  return { id: `${kind}:${from}:${to}`, kind, from, to, confidence };
}

function layerFor(verification: VerificationStatus): MemoryLayer {
  if (verification === 'consented' || verification === 'verified') return 'long_term';
  return 'short_term';
}

export function buildKnowledgeFabric(
  intelligence: LearningIntelligence,
  adaptive: AdaptiveSnapshot | null
): KnowledgeSnapshot {
  const nodes: KnowledgeNode[] = [];
  const edges: KnowledgeEdge[] = [];

  nodes.push(
    node(
      'profile:self',
      'entity',
      'Learner',
      `${intelligence.profile.currentLevel || 'unset'} · ${intelligence.profile.preferredLanguage || 'unset'}`,
      {
        layer: intelligence.profile.source === 'memory' ? 'long_term' : 'working',
        source: intelligence.profile.source,
        verification: intelligence.profile.source === 'memory' ? 'consented' : 'projected',
        importance: 0.9,
        confidence: 0.5,
      }
    )
  );

  for (const skill of intelligence.skills.filter(
    (item) => item.practiceCount > 0 || item.mastery != null
  )) {
    const id = `skill:${skill.id}`;
    nodes.push(
      node(id, 'skill', skill.title, skill.description, {
        layer: layerFor('projected'),
        source: skill.source,
        confidence: skill.confidence ?? 0.3,
        importance: Math.min(1, skill.practiceCount / 10),
        references: skill.relatedSkillIds,
      })
    );
    edges.push(edge('belongs_to', id, 'profile:self'));
  }

  for (const item of intelligence.knowledge) {
    const id = `know:${item.id}`;
    nodes.push(
      node(id, item.kind === 'topic' ? 'topic' : 'concept', item.title, item.summary, {
        source: item.source,
        references: item.relatedSkillIds,
      })
    );
    for (const skillId of item.relatedSkillIds) {
      edges.push(edge('related_to', id, `skill:${skillId}`));
    }
  }

  for (const weak of intelligence.profile.weaknesses) {
    const id = `weak:${weak}`;
    nodes.push(
      node(id, 'weakness', weak, 'Projected weakness. Not a transcript.', { importance: 0.8 })
    );
    edges.push(edge('belongs_to', id, 'profile:self'));
  }

  for (const strong of intelligence.profile.strengths) {
    const id = `strong:${strong}`;
    nodes.push(node(id, 'strength', strong, 'Projected strength.', { importance: 0.6 }));
    edges.push(edge('belongs_to', id, 'profile:self'));
  }

  for (const rec of intelligence.recommendations) {
    const id = `rec:${rec.id}`;
    nodes.push(
      node(id, 'recommendation', rec.title, rec.reason, {
        confidence: rec.confidence ?? 0.4,
        importance: rec.priority / 100,
      })
    );
    edges.push(edge('recommended_by', id, 'profile:self'));
  }

  for (const goal of intelligence.goals) {
    const id = `goal:${goal.id}`;
    nodes.push(
      node(id, 'goal', goal.title, goal.recommendation ?? 'Open goal', { importance: 0.55 })
    );
    edges.push(edge('belongs_to', id, 'profile:self'));
  }

  if (adaptive) {
    const id = `decision:${adaptive.decision.action}`;
    nodes.push(
      node(id, 'decision', adaptive.decision.action, adaptive.decision.explanation, {
        confidence: adaptive.decision.confidence,
        importance: adaptive.decision.priority / 100,
        layer: 'working',
        source: 'adaptive',
      })
    );
    edges.push(edge('derived_from', id, 'profile:self', adaptive.decision.confidence));
    if (adaptive.specialist.specialist !== 'tutor') {
      edges.push(edge('recommended_by', id, `skill:${adaptive.specialist.specialist}`));
    }
  }

  const retrieved = retrieveKnowledge({ nodes, edges }, { limit: 8 });
  return {
    nodes,
    edges,
    retrieved,
    metrics: {
      nodeCount: nodes.length,
      edgeCount: edges.length,
      longTerm: nodes.filter((item) => item.layer === 'long_term').length,
      working: nodes.filter((item) => item.layer === 'working').length,
    },
  };
}
