import { describe, expect, it } from 'vitest';
import { addElement, assistSpec, connect, emptyBoard } from '@/lib/whiteboard/engine';

describe('whiteboard engine', () => {
  it('uses fabric relationship kinds and no renderer', () => {
    let board = emptyBoard('Reasoning');
    board = addElement(board, 'knowledge_ref');
    board = addElement(board, 'document_ref');
    board = connect(board, board.elements[0].id, board.elements[1].id, 'belongs_to');
    expect(board.edges[0]?.kind).toBe('belongs_to');
    expect(assistSpec('generate_diagram').renderer).toBe('none');
  });
});
