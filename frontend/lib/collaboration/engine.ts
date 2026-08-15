export type PresenceState =
  | 'presence'
  | 'cursor'
  | 'selection'
  | 'activity'
  | 'focus'
  | 'typing'
  | 'voice'
  | 'status'
  | 'availability';

export type CollabRole =
  | 'owner'
  | 'admin'
  | 'editor'
  | 'reviewer'
  | 'commenter'
  | 'viewer'
  | 'observer'
  | 'ai_agent';

export type SessionKind = 'shared' | 'voice' | 'studio' | 'whiteboard' | 'learning' | 'enterprise';

export type PresenceRecord = {
  id: string;
  userId: string;
  sessionId: string;
  workspaceId: string;
  state: PresenceState;
  lastSeen: string;
};

export type CollaborationSnapshot = {
  sessionKind: SessionKind | null;
  participants: PresenceRecord[];
  sync: 'architected';
  crdt: false;
};

export function emptyCollaboration(): CollaborationSnapshot {
  return { sessionKind: null, participants: [], sync: 'architected', crdt: false };
}

export function joinSession(
  snapshot: CollaborationSnapshot,
  kind: SessionKind,
  userId: string
): CollaborationSnapshot {
  return {
    ...snapshot,
    sessionKind: kind,
    participants: [
      ...snapshot.participants,
      {
        id: `pres:${userId}`,
        userId,
        sessionId: `cs:${kind}`,
        workspaceId: 'local',
        state: 'presence',
        lastSeen: new Date().toISOString(),
      },
    ],
  };
}
