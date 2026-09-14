# Review

Review the Product PR against the task and recommend the next step.

Read the Issue or task description, the complete relevant diff, and available test results. Identify the actual review base and target, including relevant uncommitted or new files; pass that scope to any reviewer instead of relying on a generic branch fallback. Use your own judgment about correctness, regressions, scope, compatibility, and whether the tests exercise the change. Consider whether any conclusion would help future work as durable project knowledge.

Start with review coverage suited to the changed modules, contract changes, runtime risk, and evidence gaps. A small change can use one focused review; a cross-module change may need distinct contract or failure-path checks. Add an angle only for a concrete uncovered risk or question. Honor explicit requests for comprehensive or high-intensity review while separating exploration scopes and retaining necessary independent verification. Review breadth does not require reducing model capability or skipping defect checks.

When using another review skill, check its expansion behavior and supported scope controls. Do not select a preset that launches broad or nested review merely because this is delivery. Pass the task scope, known findings, and applicable delegation limits; if the skill cannot honor them, choose a compatible review method or explain the conflict when the user explicitly requested that skill. Apply the entrypoint's coordination and waiting guidance throughout; a short final findings cap does not bound investigation cost.

Reuse applicable test results. Run additional checks when changes, missing coverage, or uncertainty justify them. Treat an unavailable check as a limitation to explain, not a missing Harness field to repair. Decide how any known failure affects the change and recommend a fix or next step accordingly.

Write concise findings and a recommendation on the PR through [Hosting operations](hosting.md). Identify concrete problems, their effects, and relevant files. When no actionable issue remains, say so and mark the PR Ready if appropriate. Draft/Ready is a collaboration aid, not a proof of acceptance.

Use ordinary prose. There is no required PASS artifact, fixed list of review items, checksum, or comment lineage. An edited PR description does not automatically trigger another review; assess substantive changes and review what needs attention.

A standalone review ends after reporting findings and the recommendation; leave implementation fixes and merge to the delivery work. Within `delivery`, use the findings to decide how to proceed. Review does not add requirements beyond the user's task.
