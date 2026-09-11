---
name: project-harness
description: Guide code delivery through planning, an Issue, implementation, review, and useful memory updates, or use express for a small change. Use when the user invokes project-harness or asks for one of its delivery phases.
disable-model-invocation: false
---

# Project Harness

Follow a practical delivery workflow and use agent judgment to move the work forward. Harness v3 defines the paths, useful outputs, and where a standalone phase ends. It adds no validation gates, evidence protocol, or approval ceremony.

## Choose the path

Use the user's chosen path or phase. Otherwise choose a path from the task's size and uncertainty, explain the choice in one sentence, and proceed:

- **Full delivery:** plan → spec → autonomous delivery from the Issue. See [Delivery](references/delivery.md) for its reminders.
- **Express:** summarize scope → implement and test → lightweight PR → merge → summarize.

Plan with the host's native capabilities. Ask questions when their answers materially affect the work; use grilling when helpful or requested. Planning and path selection need no fixed confirmation round.

Keep the familiar phase names below. Accept ordinary language, existing conversation context, and optional `role: ...` inputs. Resolve Issue and PR references from supplied links, repository state, and the ongoing task; ask only when the intended target remains unclear. No structured role field or repeated URL is required.

For Codex, invoke with `$project-harness`; [agents/openai.yaml](agents/openai.yaml) keeps automatic loading disabled. Claude Code can load with `/project-harness` or model selection. Loading the Skill does not itself request work.

## Read the relevant operation

| Operation | Read | Output and stopping point when invoked alone |
| --- | --- | --- |
| `init` | [Init](references/init.md) | Optional project preferences; stop after setup |
| `spec` | [Spec](references/spec.md) | A concise Issue; stop with its link |
| `implementation` | [Implementation](references/implementation.md) | Code, tests, and a Draft Product PR; stop for review |
| `review` | [Review](references/review.md) | Findings and a recommendation on the Product PR; stop after review |
| `context-promotion` | [Context Promotion](references/context-promotion.md) | Useful memory changes in a PR, or a short no-update result; stop before merge |
| `delivery` | [Delivery](references/delivery.md) | Complete the Issue task autonomously within the requested scope |
| `express` | [Express](references/express.md) | Run the small-change path through merge and summary |

For a raw request selected for full delivery, complete planning and spec and continue through delivery. The standalone stopping points apply when the user asks for just that phase. Within `delivery`, choose the work arrangement freely; the other phase references are optional resources, and their standalone stopping points do not prescribe delivery sequencing.

## Work with the project

Use the request and its accepted corrections to guide scope. Keep the Issue useful as the shared task description and the PR useful as the record of changes and tests. Update them when the task evolves; their formatting does not confer or limit user authorization. Choose implementation details and task decomposition autonomously. Harness prescribes no subagent arrangement.

Test the changed behavior and review the actual diff. Use results to fix defects and explain limitations. Choose the necessary checks and whether to rerun them based on the changes; do not manufacture tests, fixed verdicts, or evidence records to advance a stage.

Use project conventions for branches and merge methods. If `.project-harness/config.yaml` exists, read relevant preferences as described in [Init](references/init.md). Configuration is optional. Use `develop` when it is the project's integration branch; otherwise use its established target or default branch. Work on a task branch and preserve other work.

Use the available hosting-platform tools as described in [Hosting operations](references/hosting.md). Agent judgment determines readiness and the next step. Harness adds no required-check discovery, mergeability proof, digest comparison, or repeated-read procedure. The hosting platform's own rules still apply.

Carry out the requested delivery, including its normal commits, PRs, merges, Issue closure, and useful memory updates, within the user's existing authorization and the host's permissions. Respect requests to stop at a phase, pause, or limit external writes. Ask for missing decisions or authorization when actually needed; no Harness-specific confirmation format or separate memory approval round is required.

Report what happened, relevant Issue/PR links, test results, and any unfinished work in plain language. Distinguish completed actions from attempted or pending ones. When tools fail or responses are unclear, investigate enough to decide how to continue without duplicating work or claiming an unobserved result.

## Bound effort and finish

Use these reminders across both paths and standalone phases. Apply them in ordinary task instructions, with detail proportional to the work.

- **Keep delegation small.** Give each subagent a bounded question or change: what to examine, what to return, and when to stop. Keep investigation within that scope and return a material gap for the primary agent to resolve instead of silently expanding the assignment.
- **Watch actual usage.** When using a budget, have the primary agent check host-provided usage counters at useful work boundaries and as the limit approaches; a subagent's estimate is not measured usage. Include coordination cost when available. At the limit, pause ongoing delegated work where the host supports it and decide whether to stop, narrow, take over, or continue within existing authorization before spending more. Make routine allocation decisions without repeatedly asking the user, while respecting explicit hard caps. If counters are unavailable, say so and use observable bounds such as tool calls or elapsed time without presenting them as token counts. Prefer host notifications or occasional checks over repeated polling and requests for status.
- **Keep handoffs compact.** When changing agents or contexts, pass conclusions, evidence locations, remaining work, and still-relevant user decisions and constraints. Use a fresh context when accumulated history gets in the way; avoid forwarding the whole transcript or replaying the investigation. Read supporting detail only when needed to resolve a specific gap.
- **Close completed work.** Once the requested outcome, necessary checks, and completion actions for the chosen path or standalone phase are satisfied, have the primary agent integrate existing results and finish. Do not reactivate finished agents merely to repeat or reformat their summaries. Repeat or broaden checks for a concrete change, failure, or unresolved concern; otherwise stop investigating. Report remaining limitations honestly.

See [Migration](MIGRATION.md) when resuming work started with an earlier Harness version.
