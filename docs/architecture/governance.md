# Governance

Privacy and policy wrap. Not a second auth stack.

Canonical: [39 Governance](../engineering/39_GOVERNANCE_PLATFORM.md).  
[48 Compliance](../engineering/48_COMPLIANCE_PLATFORM.md) is an alias of 39.

## Rules that do not move

- No utterance or transcript columns
- Consent before memory
- Anonymous voice is first-class
- HIPAA is not claimed (`ComplianceCheck` for HIPAA is `ok: False`)
- GDPR / COPPA / FERPA / SOC2 / ISO checks reuse `PRIVACY_RULES`

## AuthZ

One function: `can(role, permission)`. Frontend `lib/platform/rbac.ts` mirrors `salora_platform.auth`.

Roles include anonymous, guest, student, parent, teacher, enterprise_admin, developer, operator.

## Cloud and deploy

[40 Global Cloud](../engineering/40_GLOBAL_CLOUD_PLATFORM.md) and [47 Global Deployment](../engineering/47_GLOBAL_DEPLOYMENT_PLATFORM.md) are the same compose/region model. `GlobalDeploymentService = CloudService`.

## Related

- [13 Security Standard](../engineering/13_SECURITY_STANDARD.md)
- [16 Security & Privacy constitution](../salora/16-security-privacy.md)
- [guides/configuration.md](../guides/configuration.md)
