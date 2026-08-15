# SDK

Contracts for clients. No portal UI.

Canonical: [29 AI SDK](../engineering/29_AI_SDK_PLATFORM.md). Public wrap: [45 Public API](../engineering/45_PUBLIC_API_PLATFORM.md).

## Envelope

`ApiEnvelope` version `v1`. Breaking changes are a v2 envelope, not a kernel fork.

Tokens: `APITokenService`. Guest cannot issue keys. OAuth is architected, not a server.

## Adapters

Named, not implemented as extra runtimes. Mobile and desktop consume the same modules as the web SDK contracts.

## Events

`ApiTokenIssued`, `APIKeyIssued`, `OAuthGranted`, `ClientRegistered` go through the platform event bus.

## Related

- [api/backend.md](backend.md)
- [architecture/enterprise-platform.md](../architecture/enterprise-platform.md)
