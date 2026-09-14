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

- **Keep delegation bounded.** Give each subagent a question or change: scope and exclusions, known evidence, what to return, and when to stop. Carry applicable project tool-call budgets and checkpoint expectations into delegated work, including nested review workflows; do not create a second budget scheme. Return material gaps instead of silently expanding the assignment.
- **Keep coordination light.** Dispatch work, integrate checkpoints, deduplicate findings, resolve conflicts, verify key claims, and summarize. Once a scope is delegated, do not independently scan it again. Necessary overlap should name a distinct hypothesis or claim and the evidence needed to test it; independent verification is targeted work, not a second full investigation.
- **Wait for the right event.** When the host automatically notifies agent completion, yield through its supported mechanism or do unrelated useful work. Do not create Monitor jobs, poll output files, or issue repeated status requests to wait for agents. Without notifications, use the host's bounded wait facility. A quiet interval or wait timeout alone does not mean an agent failed or should be interrupted. External processes and CI may need polling: prefer native completion signals; otherwise fix the deadline once, bound each check, and handle success, failure, cancellation, and timeout distinctly. Never use tool calls merely to express status or organize reasoning, including pure `echo` commands.
- **Watch cumulative work.** Reuse existing budgets and checkpoints to report new findings, remaining questions, and usage so far, including coordination when available. Use host counters when exposed; estimates are not measured usage, and cumulative tokens are not current context length. If counters are unavailable, say so and use tool-call counts and observable context growth without inventing token totals. At a budget boundary, decide within existing authorization whether to narrow, take over, stop, or continue toward a named new evidence target; without such a target, close exploration. Respect explicit hard caps. Do not interrupt useful work merely because time passed, or add a user approval round for routine allocation.
- **Keep handoffs compact.** Return conclusions, relocatable evidence, remaining work, and still-relevant user decisions and constraints, not full logs, long diffs, or exploration history. Read supporting detail only to resolve a specific gap. When a growing context repeats searches or cycles through summaries, narrow the work and hand off a compact checkpoint to a fresh context if supported; do not have the same bloated context regenerate a full report.
- **Close completed work.** Once the requested outcome, necessary checks, and completion actions for the chosen path or standalone phase are satisfied, have the primary agent integrate existing results and finish. Do not reactivate finished agents merely to repeat or reformat their summaries. Repeat or broaden checks for a concrete change, failure, or unresolved concern; otherwise stop investigating. Report remaining limitations honestly.

See [Migration](MIGRATION.md) when resuming work started with an earlier Harness version.
