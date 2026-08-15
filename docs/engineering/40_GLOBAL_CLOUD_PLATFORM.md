# 40 — Global Cloud & Edge Platform

Worldwide deploy without a new orchestrator.

Reuses `docker-compose`, `SALORA_PROFILE`, `/api/health`, `salora_platform.health`.

Regions: local, staging, production. Rollback = previous image + env. Backup job must not create a speech lake.

Failover and CDN are architected. Edge cache is a future adapter in front of Next, not a second frontend.
