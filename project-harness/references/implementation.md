# Implementation

Execute this phase only after `project-harness` dispatches `role: implementation`, or a current `delivery` invocation runs the Implementation phase.

Carry the Implementation phase from one finalized Issue to one independently read-back Draft Pull Request.

## Contents

- Enforce the phase boundary
- Accept the semantic input
- Bind the Issue contract
- Enforce the authorized change scope
- Resolve one active branch and PR
- Plan autonomously
- Create an Execution Packet only when useful
- Implement and verify
- Build the complete Draft PR
- Preserve recoverable failure state
- Return a phase result

## Enforce the phase boundary

- Start only from an explicit Issue URL supplied by a current standalone `role: implementation` invocation or a current `delivery` invocation.
- Treat that invocation as authority to modify product code and tests, create or resume one task branch, commit, push, and create or update one Draft PR. Do not derive authority from host/model loading, automatic routing, an ordinary hand-off, an ordinary implementation request, or a prior run.
- Keep the Issue as the only delivery contract.
- Treat the Issue implementation plan as a non-binding starting prediction.
- Preserve model autonomy over exploration, code structure, task decomposition, commit cadence, debugging, and risk-proportionate test selection. Subagent use is unconstrained: spawn read-only explorers or verifiers whenever separate context materially helps, and integrate and verify their results yourself.
- Stop at verified-draft-pr, return-to-spec, or blocked.
- Never edit the Issue contract, mark a PR Ready, merge or close, write durable project memory, issue a review verdict, approve Context Promotion, or declare final delivery.

## Accept the semantic input

Apply the root Skill's public-invocation adapter. Require an exact `role: implementation` (standalone) or a current `delivery` phase request, plus one finalized Issue URL. Treat current-message URLs as semantic sources whether they appear in prose or an optional structured carrier.

For a repair round, require the existing Draft PR URL and the latest exact review FAIL comment URL. Re-read both completely; do not rely on anyone's summary of the failure.

Reject chat text that changes the goal, boundaries, external behavior, difficult-to-reverse architecture, or acceptance contract. Return return-to-spec instead of treating such text as a hidden requirement.

## Bind the Issue contract

1. Follow the loaded Issue transport protocol to resolve the exact repository and read the complete open Issue.
2. Normalize and bind the Issue Body digest.
3. Establish only the authoritative code, test, decision, rule, and durable-source evidence needed to implement the Issue contract safely. Stop when a required fact cannot be established.
4. Distinguish binding contract sections from the non-binding implementation plan.
5. Re-read the Issue before a successful hand-off; return return-to-spec for a change to a binding contract item.

Do not update the Issue from this phase.

## Enforce the authorized change scope

Before the first product-code or test mutation, read the exact compact `### 改动范围` subsection inside the Issue's binding `非目标与边界` section. For a current-format Issue, require one non-empty `普通业务改动` field and one non-empty `受保护改动` field in that subsection.

- For every new or open/unmerged lineage, require the compact scope to be present, unambiguous, and applicable to the requested change. A historical open Issue or Draft/Ready PR without it cannot continue under Implementation; return return-to-spec without making another product mutation.
- Treat the Issue description together with `普通业务改动` as the maximum ordinary change scope. It does not authorize a protected surface implicitly.
- Apply the protected surfaces defined by the shared Issue contract. Require `受保护改动` to name every applicable protected surface and state both the exact allowed change and its compatibility or migration boundary. The exact declaration `受保护改动：无` forbids every protected-surface change.
- Never derive a protected exception or wider ordinary scope from `实施计划`, a PR Body, an ADR or other durable source, repository conventions, chat, or an implementation convenience.
- Return return-to-spec immediately when the compact scope is missing, vague, internally inconsistent, contradicted by repository facts, or narrower than a mutation required to complete the contract. Omit an unnecessary planned edit that falls outside scope and continue.
- For an exact already-merged lineage reached only for recovery, keep the recovery read-only.

## Resolve one active branch and PR

Follow the loaded Pull Request transport protocol to search open and closed PRs related to the exact Issue.

- Create a dedicated task branch only when no active implementation PR or branch exists.
- Resume the exact head branch when one unambiguous active PR exists.
- Stop blocked when multiple candidates, branch ownership conflicts, or an ambiguous relationship prevents safe selection.
- Stop without implementation when the Issue is already completed by a merged PR.
- Never work directly on `develop` or `main`.
- Never mix another Issue's changes into the task branch.
- Preserve pre-existing user changes. Isolate safely or stop instead of overwriting, resetting, stashing, or reassigning them without authority.

## Plan autonomously

- Choose the smallest useful execution plan from the Issue and current repository state. For a simple localized task, proceed directly without manufacturing subplans, research packets, or delegation work.
- Keep implementation, integration, validation, PR, and phase hand-off responsibility in this phase.
- Spawn subagents only when they materially help, and verify every result before relying on it.

## Create an Execution Packet only when useful

Create task-local Markdown under `.project-memory/tasks/<task-id>.md` on the implementation branch when task length, multi-Agent execution, a review repair loop, or context pressure makes recovery materially safer and the repository update protocol permits it. Require it for a repair that cannot be reconstructed safely from the Draft PR and commits alone.

For every Execution Packet:

- identify the source Issue and bound digest;
- remain derived from, and subordinate to, the Issue;
- record only execution state needed by a later recovery;
- retain it when returning blocked with useful partial work;
- remove it from the final diff before verified-draft-pr.

Do not place task-local state in active rules, ADRs, wiki pages, or stable project memory.

## Implement and verify

- Implement the Issue completely, including necessary tests.
- Adjust the non-binding plan as repository facts require, and record material deviations for the PR.
- Run the smallest verification set that covers the Issue acceptance checks and the actual change risk. Prefer targeted tests and static checks for localized changes; add broader builds, integration tests, or smoke tests only when the changed boundary or repository rules require them.
- Continue through ordinary implementation and debugging failures.
- Checkpoint coherent progress to the task branch and incomplete Draft PR at risk-proportionate boundaries.
- Use blocked only for an external, permission, environment, target-ambiguity, or unrecoverable-state condition that prevents meaningful progress.
- Use return-to-spec when progress requires a changed delivery contract.

Before success, require:

- every binding contract item implemented;
- the complete final product diff independently compared with the Issue's exact `### 改动范围`, with every ordinary business change inside `普通业务改动` and every protected-surface change covered by one explicit exception including its compatibility or migration boundary; treat `受保护改动：无` as a verified absence requirement, remove any unnecessary out-of-scope edit and rerun the applicable checks, and return return-to-spec only when completion requires a broader contract or the required authority remains ambiguous;
- all risk-proportionate selected validation passing, with every reported command or check bound to the final head SHA;
- no known unfinished acceptance item;
- all intended changes committed and pushed;
- no task-local Execution Packet remaining in the final diff;
- the task branch based on the intended target and safely integrable;
- the Issue contract re-read and still applicable.

## Build the complete Draft PR

Use the shared Product PR contract loaded for this role as the exact Body structure and semantic minimum. Include:

- a plain `Refs`-style reference link to the Issue (closing keywords are forbidden; the authorized `delivery` owns explicit closure);
- user-observable result;
- main implementation scope;
- material plan deviations and reasons;
- exact validation commands/checks and results;
- known limitations and risks;
- factual durable-memory impact for `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`, using the exact value `无` with non-placeholder evidence when a category has no impact and a concrete impact statement otherwise;
- bound Issue Body digest;
- head SHA;
- base branch `develop` and its base SHA;
- an explicit statement that no known unfinished item remains.

Leave `Review` empty in the Body; the `review` phase writes its verdict as a top-level PR comment.

Use the loaded Pull Request transport protocol to create or replace the Draft PR, protect unrelated fields, normalize and bind the Body digest, and independently read the PR back. Treat only verified or no-op transport outcomes as success.

In every reported validation result, identify the exact command or check, its result, and the final head SHA or immutable CI run that produced it. This binding lets Review reuse current-head evidence without mechanically rerunning low-risk checks; stale, incomplete, or unbound evidence remains non-reusable.

## Preserve recoverable failure state

When returning blocked after valuable work:

- commit and push coherent changes when safe;
- create or update a clearly incomplete Draft PR when GitHub is available;
- retain useful Execution Packet state;
- report exact branch, head SHA, PR URL when present, dirty paths, completed checks, blocker, and recovery condition.

When GitHub is unavailable, report exact local branch, commit, and worktree state. Do not fabricate a verified PR.

## Return a phase result

Return one result only.

~~~yaml
outcome: verified-draft-pr | return-to-spec | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
repository: owner/repo
branch: null
head_ref: null
head_sha: null
pr_url: null
pr_title: null
pr_body_sha256: null
base_ref: null
base_sha: null
validation: []
reason: null
recovery_condition: null
next_action: null
~~~

For every populated result, require `branch == head_ref` and bind both to the independently read Draft PR head. Populate each `validation` entry with the command or check, result, bound `head_sha`, and an evidence URL when one exists. Keep the entry factual and compact; do not embed raw logs.

For verified-draft-pr, name `role: review` (phase-by-phase path) or return to the current `delivery` invocation with the Issue URL, Draft PR URL, and bound tuple.

For return-to-spec, identify the exact contract gap and evidence, preserve the branch/PR state, and return the same Issue URL with `role: spec`.

For blocked, do not claim successful Implementation or hand off to Review. Return only the exact persistent branch/PR state and recovery condition.
