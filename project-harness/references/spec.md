# Spec

Turn the requirement and useful planning outcomes into an Issue that another agent can implement without the full conversation.

Read relevant code and existing task context. If a plan is needed, form one with the host's planning capabilities. Clarify material product choices as needed; there is no grilling transcript or plan-approval prerequisite.

Use the [Issue template](issue-template.md) as a writing aid. Explain the problem, desired result, change scope, decisions that affect implementation, and practical acceptance checks. Scale the detail to the task. Include compatibility or migration consequences when they matter, without a protected-surface checklist or special exception syntax.

Create the Issue or update the existing task's Issue using [Hosting operations](hosting.md). Resolve likely duplicates when useful and preserve still-relevant content. Keep the Issue aligned with the user's request and corrections. No exact heading order, digest, or decision-status field is required.

Return the Issue link and a short description of what is ready to implement. A standalone `spec` request ends here. When this phase is part of the full path selected for a raw request, continue with [Delivery](delivery.md).
