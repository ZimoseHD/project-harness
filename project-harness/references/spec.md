# Spec

Turn the requirement and useful planning outcomes into an Issue that another agent can implement without the full conversation.

Read relevant code and existing task context, reusing authoritative evidence from planning and delegated investigation. Batch related searches and read bounded passages around known entries. Once material facts have suitable sources and conflicts are resolved, move to the user decisions that remain; do not keep changing keywords to rediscover the same facts or exhaust edge cases that would not change the plan. A failed query is not evidence of absence. If a plan is needed, form one with the host's planning capabilities. Bring established facts into clarification or grilling and investigate again only for a new material gap. Preserve necessary questions rather than replacing user decisions with guesses; there is no grilling transcript or plan-approval prerequisite.

Use the [Issue template](issue-template.md) as a writing aid. Explain the problem, desired result, change scope, decisions that affect implementation, and practical acceptance checks. Scale the detail to the task. Include compatibility or migration consequences when they matter, without a protected-surface checklist or special exception syntax.

Create the Issue or update the existing task's Issue using [Hosting operations](hosting.md). Resolve likely duplicates when useful and preserve still-relevant content. Keep the Issue aligned with the user's request and corrections. No exact heading order, digest, or decision-status field is required.

Return the Issue link and a short description of what is ready to implement. A standalone `spec` request ends here. When this phase is part of the full path selected for a raw request, continue with [Delivery](delivery.md).
