import type { KnowledgeRelationKind } from '@/lib/knowledge-fabric/types';
import type {
  WhiteboardAssistKind,
  WhiteboardElementKind,
  WhiteboardSnapshot,
} from '@/lib/whiteboard/types';

function stamp(): string {
  return new Date().toISOString();
}

export function emptyBoard(title = 'Untitled board'): WhiteboardSnapshot {
  const at = stamp();
  return {
    canvas: {
      id: 'canvas:local',
      title,
      owner: 'local',
      createdAt: at,
      updatedAt: at,
      layers: ['default'],
    },
    elements: [],
    edges: [],
    viewport: { x: 0, y: 0, zoom: 1 },
    selection: [],
  };
}

export function addElement(
  board: WhiteboardSnapshot,
  type: WhiteboardElementKind
): WhiteboardSnapshot {
  const at = stamp();
  const id = `el:${type}:${board.elements.length + 1}`;
  return {
    ...board,
    elements: [
      ...board.elements,
      {
        id,
        canvasId: board.canvas.id,
        type,
        bounds: { x: 0, y: 0, w: 160, h: 80 },
        owner: 'local',
        createdAt: at,
        updatedAt: at,
        metadata: {},
      },
    ],
  };
}

export function connect(
  board: WhiteboardSnapshot,
  from: string,
  to: string,
  kind: KnowledgeRelationKind = 'related_to'
): WhiteboardSnapshot {
  return {
    ...board,
    edges: [...board.edges, { id: `edge:${from}:${to}`, kind, from, to }],
  };
}

export function assistSpec(kind: WhiteboardAssistKind): {
  kind: WhiteboardAssistKind;
  renderer: 'none';
} {
  return { kind, renderer: 'none' };
}

export function buildWhiteboardSnapshot(title?: string): WhiteboardSnapshot {
  return emptyBoard(title);
}
