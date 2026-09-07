# Express

Deliver a small, clear change through implementation, tests, a lightweight PR, and merge.

Summarize the scope in one sentence and proceed from the user's request. There is no separate scope-confirmation round. Use a task branch from the project's integration branch and preserve existing work.

Implement the requested change and run appropriate tests. Review your diff as part of the work; express has no separate Issue or standalone review phase. Choose the depth of investigation from the actual change. If the task grows enough that a plan and Issue would help, explain the change of approach and use the full path. Touching an API, configuration, or another formerly protected surface does not by itself force an upgrade.

Commit and push, then create a lightweight PR with the result, main changes, tests, and relevant limitations. The [Product PR template](product-pr-template.md) can be shortened to fit; omit the Issue link when there is no Issue.

Merge using [Hosting operations](hosting.md) when the change is ready in your judgment and integration is within the user's request. Harness requires no evidence comments or merge-validation ceremony.

Report the PR link, outcome, and tests. Mention useful memory candidates in the summary; memory writing is outside this path. If requested, handle it as a subsequent memory task using the task or merged PR as its source, without requiring an Issue to be created first.
