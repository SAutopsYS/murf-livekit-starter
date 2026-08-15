# 30 — Collaboration Platform

Many people and agents in one workspace. Not chat. Not video. Not a second voice path.

---

## Collaboration architecture

`CollaborationProvider` + `CollaborationService`.

Consumes Workspace Shell, Studio projects, Whiteboard sessions, org workspaces, RBAC, event bus.

Voice sessions stay LiveKit rooms. Collaboration sessions are metadata around them.

---

## Presence model

presence, cursor, selection, activity, focus, typing, voice, status, availability.

Fields: id, userId, sessionId, workspaceId, state, lastSeen, metadata.

---

## Session model

shared, voice, studio, whiteboard, learning, enterprise.

`SessionKind.voice` **references** a LiveKit room name. It does not mint a second token path.

---

## Synchronization

Architecture: incremental sync, conflict resolution, optimistic updates, session recovery, offline queue, presence sync.

`crdt: false`. No Yjs. No multiplayer canvas.

---

## Roles

owner, admin, editor, reviewer, commenter, viewer, observer, ai_agent.

Mapped onto existing permissions (`enterprise.admin`, `studio.access`, `learning.read`, `voice.session`).

---

## Notifications

mentions, share, comment reply, AI suggestion, workflow complete, learning recommendation, plugin update — kinds only.

---

## Accessibility

Future live regions for join/leave. Keyboard still owns ⌘K. Reduced motion when cursors exist. No cursor animation on the hall.

---

## Future

Live comments and multiplayer boards subscribe to this engine. They do not invent a second presence bus.
