# Implementation

Execute this phase only after `project-harness` dispatches a standalone `role: implementation` or the current `delivery` coordinator delegates the Implementation phase under the root Skill's scoped envelope.

Carry the Implementation phase from one finalized Issue to one independently read-back Draft Pull Request.

## Contents

- Enforce the phase boundary
- Accept only the minimal input
- Bind the Issue contract
- Verify the pre-implementation durable-decision gate
- Resolve one active branch and PR
- Plan and delegate autonomously
- Create an Execution Packet only when useful
- Implement and verify
- Build the complete Draft PR
- Preserve recoverable failure state
- Return a persistent phase result

## Enforce the phase boundary

- Start only from an explicit Issue URL and either a current standalone Implementation invocation or a host-provenance-bound delegation from the current explicit `delivery` invocation.
- Treat a current user's explicit `$project-harness` invocation with `role: implementation` as authority to modify product code and tests, create or resume one task branch, commit, push, and create or update one Draft PR. Under `delivery`, accept only the same mutations when the delegation envelope enumerates them and binds the current persistent sources. Do not derive authority from an automatic route, serialized envelope, ordinary hand-off, ordinary implementation request, or prior run.
- Keep the Issue as the only delivery contract.
- Treat the Issue implementation plan as a non-binding starting prediction.
- Preserve model autonomy over exploration, code structure, task decomposition, sub-agents, commit cadence, debugging, and risk-proportionate test selection.
- Keep one Primary Implementation Agent accountable for the branch, integration, validation, and PR.
- Verify any required pre-implementation durable-decision result before modifying product code.
- Stop at verified-draft-pr, return-to-definition, or blocked and return control to the coordinator when delegated.
- Never edit the Issue contract, mark a PR Ready, merge or close, write durable project memory, issue a Closeout verdict, approve Context Promotion, or declare final delivery.

## Accept only the minimal input

Require:

~~~yaml
role: implementation
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  # Include the merged proposed-decision PR URL only when the Issue requires it.
next_action: Implement the Issue and produce a verified Draft PR.
~~~

When delegated by `delivery`, also require the root Skill's envelope with `delegated_role: implementation`. For a repair, require the existing Draft PR URL and latest exact Closeout FAIL comment URL in `authoritative_sources` or `persistent_evidence_urls`. Re-read both completely; do not rely on the coordinator's explanation of the failure.

Reject chat text that changes the goal, boundaries, external behavior, difficult-to-reverse architecture, or acceptance contract. Return return-to-definition instead of treating such text as a hidden requirement.

## Bind the Issue contract

1. Follow the loaded Issue transport protocol to resolve the exact repository and read the complete open Issue.
2. Normalize and bind the Issue Body digest.
3. Establish the authoritative code, test, decision, rule, and durable-source evidence required to implement the Issue contract. Stop when a required fact cannot be established.
4. Distinguish binding contract sections from the non-binding implementation plan.
5. Re-read the Issue before successful hand-off.
6. Compare any changed Body with the bound version.
7. Return return-to-definition for a change to a binding contract item.
8. Rebind and record a purely editorial or non-binding-plan change only when it cannot affect delivery.

Do not update the Issue from this Skill.

## Verify the pre-implementation durable-decision gate

Read the Issue's `持久项目记忆影响` section before modifying product code.

- For `not-required`, continue without a decision source.
- For `required`, follow the loaded Issue transport protocol to read the source Issue callbacks and the loaded Pull Request transport protocol to resolve the one referenced decision PR.
- Require the decision PR to belong to the exact Issue Body digest, be merged into `develop`, contain only the required `docs/decisions/` change, and have an independently verified authoring PASS record.
- Treat only the exact merged ADR leaves referenced by that PR as decision authority. Treat `proposed` as selected but not yet implementation-validated.
- Stop blocked when the required decision PR is Ready but unmerged or when GitHub state is temporarily unavailable.
- Return return-to-definition when the Issue declares `required` without a settled decision, valid callback, unique target, or satisfiable gate.
- Stop on conflicting or multiple authoring callbacks instead of selecting one.

## Resolve one active branch and PR

Follow the loaded Pull Request transport protocol to search open and closed PRs related to the exact Issue.

- Create a dedicated task branch only when no active implementation PR or branch exists.
- Resume the exact head branch when one unambiguous active PR exists.
- Stop blocked when multiple candidates, branch ownership conflicts, or an ambiguous relationship prevents safe selection.
- Stop without implementation when the Issue is already completed by a merged PR.
- Never work directly on `develop` or `main`.
- Never mix another Issue's changes into the task branch.
- Preserve pre-existing user changes. Isolate safely or stop instead of overwriting, resetting, stashing, or reassigning them without authority.

Leave branch naming to the Primary Agent.

## Plan and delegate autonomously

- Choose the smallest useful execution plan from the Issue and current repository state.
- Keep core implementation, integration, validation, PR, and phase hand-off responsibility in the Primary Agent.
- Delegate to sub-agents or sub-subagents only when separate context spaces materially help exploration, independent research, bounded implementation, or verification.
- Set explicit write ownership before allowing parallel writers.
- Integrate and verify every sub-agent result before relying on it.
- Narrow every nested delegation from this phase's allowed mutations. Keep Reviewers read-only and prevent descendants from merging, closing the Issue, approving promotion, or declaring delivery complete.
- Never let an ordinary implementation descendant cross the phase boundary. Only the Primary Implementation Agent may return the verified phase hand-off to the `delivery` coordinator or standalone caller.

Do not require a fixed Agent count, role roster, DAG, or work-package format.

## Create an Execution Packet only when useful

Create task-local Markdown under `.project-memory/tasks/<task-id>.md` on the implementation branch when task length, multi-Agent execution, nested delegation, a Closeout repair loop, or context pressure makes recovery materially safer and the repository update protocol permits it. Require it for nested parallel writers or a repair that cannot be reconstructed safely from the Draft PR and commits alone.

Possible derived artifacts include a task board, append-only progress log, current hand-off, or context map. Do not require any fixed file set.

For every Execution Packet:

- identify the source Issue and bound digest;
- remain derived from, and subordinate to, the Issue;
- avoid copying the complete contract;
- record only execution state needed by a fresh Implementation Agent;
- retain it when returning blocked with useful partial work;
- remove it from the final diff before verified-draft-pr.

Do not place task-local state in active rules, ADRs, wiki pages, or stable project memory.

## Implement and verify

- Implement the Issue completely, including necessary tests.
- Adjust the non-binding plan as repository facts require.
- Record material plan deviations and their reasons for the PR.
- Run verification proportional to risk and the Issue acceptance checks.
- Continue through ordinary implementation and debugging failures.
- Under `delivery`, checkpoint coherent progress to the task branch and incomplete Draft PR at risk-proportionate boundaries. Do not leave valuable multi-Agent or repair-loop state only in a worktree or Agent context.
- Use blocked only for an external, permission, environment, target-ambiguity, or unrecoverable-state condition that prevents meaningful progress.
- Use return-to-definition when progress requires a changed delivery contract.

Before success, require:

- every binding contract item implemented;
- all selected validation passing;
- no known unfinished acceptance item;
- all intended changes committed and pushed;
- no task-local Execution Packet remaining in the final diff;
- the task branch based on the intended target and safely integrable;
- the Issue contract re-read and still applicable;
- every required pre-implementation decision gate independently verified against the merged ADR source.

## Build the complete Draft PR

Use the shared Product PR contract loaded for this role as the exact Body structure and semantic minimum. Include:

- a plain `Refs`-style reference link to the Issue (closing keywords are forbidden; Context Promotion owns the closure judgment and the authorized entry performs the explicit mutation);
- user-observable result;
- main implementation scope;
- material plan deviations and reasons;
- exact validation commands/checks and results;
- known limitations and risks;
- factual durable-memory impact for `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`, with evidence or an explicit `none` for each category;
- bound Issue Body digest;
- head SHA;
- base branch `develop` and its base SHA;
- an explicit statement that no known unfinished item remains.

Keep Closeout's independent verdict out of the PR Body.

Use the loaded Pull Request transport protocol to:

1. create the exact PR as Draft or replace the complete Body of the one active PR;
2. protect title, refs, Draft state, and unrelated fields;
3. normalize and bind the PR Body digest;
4. independently read the PR back;
5. bind and verify Issue linkage, exact title, Body digest, Draft state, head ref/SHA, and base ref/SHA.

Treat only verified or no-op transport outcomes as success.

## Preserve recoverable failure state

When returning blocked after valuable work:

- commit and push coherent changes when safe;
- create or update a clearly incomplete Draft PR when GitHub is available;
- retain useful Execution Packet state;
- report exact branch, head SHA, PR URL when present, dirty paths, completed checks, blocker, and recovery condition.

When GitHub is unavailable, report exact local branch, commit, and worktree state. Do not fabricate a verified PR.

## Return a persistent phase result

Return one result only.

~~~yaml
outcome: verified-draft-pr | return-to-definition | blocked
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
decision_sources: []
reason: null
recovery_condition: null
handoff:
  role: delivery | closeout | definition | implementation
  recipient: delivery-coordinator | user
  authoritative_sources: []
  evidence_urls: []
  next_action: null
~~~

For delegated verified-draft-pr, set `recipient: delivery-coordinator`, `role: closeout`, and include only the Issue URL and Draft PR URL plus the bound tuple evidence. The coordinator must re-read them before starting a fresh Closeout Agent.

For every populated result, require `branch == head_ref` and bind both to the independently read Draft PR head.

For standalone verified-draft-pr, recommend `role: delivery` with the Issue and Draft PR URLs so the coordinator resumes at Closeout without requiring the user to invoke each later phase. Preserve `role: closeout` only for a caller intentionally using the legacy phase path.

For return-to-definition, identify the exact contract gap and evidence, preserve the branch/PR state, and return the same Issue URL with `role: definition`. A `delivery` coordinator stops instead of editing the contract.

For blocked, do not claim successful Implementation or hand off to Closeout. Return control to the coordinator only with the exact persistent branch/PR state and recovery condition.
