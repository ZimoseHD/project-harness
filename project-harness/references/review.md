# Review

Review the Product PR against the task and recommend the next step.

Read the Issue or task description, the complete relevant diff, and available test results. Use your own judgment about correctness, regressions, scope, compatibility, and whether the tests exercise the change. Consider whether any conclusion would help future work as durable project knowledge.

Reuse applicable test results. Run additional checks when changes, missing coverage, or uncertainty justify them. Treat an unavailable check as a limitation to explain, not a missing Harness field to repair. Decide how any known failure affects the change and recommend a fix or next step accordingly.

Write concise findings and a recommendation on the PR through [Hosting operations](hosting.md). Identify concrete problems, their effects, and relevant files. When no actionable issue remains, say so and mark the PR Ready if appropriate. Draft/Ready is a collaboration aid, not a proof of acceptance.

Use ordinary prose. There is no required PASS artifact, fixed list of review items, checksum, or comment lineage. An edited PR description does not automatically trigger another review; assess substantive changes and review what needs attention.

A standalone review ends after reporting findings and the recommendation; leave implementation fixes and merge to the delivery work. Under `delivery`, address findings and continue. Review does not add requirements beyond the user's task.
