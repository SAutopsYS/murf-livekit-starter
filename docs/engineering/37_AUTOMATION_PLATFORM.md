# 37 — AI Automation Platform

Intelligent automation **is** [33](33_WORKFLOW_AUTOMATION_PLATFORM.md).

Public summary: [../architecture/automation-platform.md](../architecture/automation-platform.md).

Do not add a second runtime. `AutomationService.create/execute` + Trigger/Action/Schedule/Approval.

Security: `enterprise.admin` for approvals. Org id on the workflow. Capability checks via existing RBAC.

Performance: `workflow_run` job, retry from job spec, no in-process queue yet.
