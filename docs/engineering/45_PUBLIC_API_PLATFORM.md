# 45 — Public API Platform

Public surface **is** the SDK (`PublicAPIService` wraps `SDKService`).

OAuth 2.1 is architected. API keys reuse `developer.sdk`. Portal UI stays false.

Events: APIKeyIssued, OAuthGranted, ClientRegistered.
