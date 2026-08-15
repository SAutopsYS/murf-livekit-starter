# Automation Platform

One workflow engine.

Canonical: [33 Workflow Automation](../engineering/33_WORKFLOW_AUTOMATION_PLATFORM.md).  
[37 Automation](../engineering/37_AUTOMATION_PLATFORM.md) is an alias of 33.

## Behavior

`AutomationService` (also exported as `WorkflowAutomationService`) creates and executes workflows. Triggers, actions, schedules, and approvals sit on that service.

Jobs use `JOB_CATALOG`. There is no Kafka or in-process queue yet. Do not add a second automation runtime.

Approvals use existing RBAC (`enterprise.admin`). Org id stays on the workflow.

## Related

- [Backend](backend.md)
- [Enterprise Platform](enterprise-platform.md)
