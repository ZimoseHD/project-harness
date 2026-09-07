# Delivery

Carry a task from its Issue through implementation, review, product integration, useful memory updates, and Issue closure.

Read the Issue and related PRs and inspect the working branch. Use actual changes, review findings, and merge state to work out what remains. Reuse completed work. Missing historical verdicts, callbacks, or configuration do not require a repair phase.

Follow the path:

1. Run [Implementation](implementation.md) to create or complete the code, tests, and Product PR.
2. Run [Review](review.md). Address actionable findings, then review the affected changes as needed.
3. Merge the Product PR using [Hosting operations](hosting.md) when the work is ready in your judgment and the requested delivery includes integration.
4. If the work produced useful durable knowledge, run [Context Promotion](context-promotion.md) and merge its memory PR. Otherwise proceed directly to closure.
5. Close the Issue when the requested work is complete and summarize the result.

Continue through these steps in the same invocation. Adjust the implementation plan and update the Issue when that helps keep the task accurate. Ask the user about material unresolved choices; there is no mandatory stage-confirmation round.

For recovery, resume from the real state:

- An incomplete Product PR needs implementation or fixes.
- A PR with unresolved review findings needs those findings addressed.
- A finished, unmerged Product PR needs integration.
- An already merged Product PR needs only any remaining memory work and closure.
- An existing memory PR needs its actual content assessed and completed, revised, or left aside according to the task. Avoid creating duplicate memory work.
- An already completed task needs a summary, not another merge or audit record.

The agent decides how much inspection is useful and which steps are already complete. No fixed evidence set or state machine controls this decision. For earlier Harness artifacts, follow [Migration](../MIGRATION.md).

Use normal platform Issue closure; an explicit close or an appropriate PR closing reference is fine. When memory work remains part of this delivery, prefer a plain Issue reference on the Product PR and close the Issue after that work. An intentional deferral can be noted in the summary without manufacturing a no-promotion record.

If tools, access, or another external dependency prevent progress, keep useful work and report the actual state and next action. Distinguish a queued merge from a completed one. Do not claim the Issue is closed until the available result establishes that it is.

Finish with the Issue and PR links, what changed, tests run, memory updates if any, and any remaining work. No structured result envelope is required.
