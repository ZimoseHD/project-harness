# Context Promotion

After product integration, capture knowledge that will help future tasks.

Read the task, merged product changes, and relevant existing project memory. Consider decisions and their reasons, stable rules, domain knowledge, recurring context, or meaningful milestone evidence. These are prompts for judgment, not required categories or rows.

Promote only useful conclusions that are not already adequately recorded or easily learned from the code. Use the project's established memory locations and writing conventions. Avoid task logs, speculative rules, duplication, and unrelated edits.

If there is nothing useful to add, report that briefly and finish this phase without creating a branch, proposal, callback, or PR.

For useful updates, create or resume a memory branch from the integration branch, make focused documentation changes, and run the applicable documentation checks. Create or update a memory PR using [Hosting operations](hosting.md). Explain what knowledge changed, where, why it will remain useful, and the source task or PR.

Use the user's existing authorization as described in the Skill entrypoint. No proposal artifact, marker, decision packet, separate confirmation round, or terminal record is needed. Apply ordinary user revisions to the same work. If the user has asked to pause or review the changes before merge, honor that instruction.

A standalone `context-promotion` request ends with the memory PR and a summary, before merge. Under `delivery`, continue by merging the memory PR and closing the task. When resuming older work, use [Migration](../MIGRATION.md) to reuse actual changes and preserve historical records.
