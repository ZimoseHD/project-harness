# Context Promotion

Execute this phase only after `project-harness` dispatches `role: context-promotion`, or a current `delivery` invocation runs the Context Promotion phase.

Carry the Context Promotion phase for one merged product PR: classify durable project-memory impact, and for an actual write drive one minimal project-memory PR through proposal, source-bound user confirmation, and guarded merge reconciliation.

## Contents

- Enforce the phase boundary
- Accept the semantic input
- Route existing lineage or classify fresh
- Classify promotable knowledge
- Build and persist the proposal
- Relay the confirmation gate
- Apply revisions
- Complete the confirmed outcome
- Return a phase result

## Enforce the phase boundary

- Start only from one Issue URL and one merged product PR URL supplied by a current explicit invocation or a current `delivery` phase request.
- Treat that invocation as authority to create or resume one project-memory branch, edit only the permitted authority files, commit, push, create or update one Draft project-memory PR, and write the promotion artifacts defined by `references/evidence-contract.md`.
- Subagent use is unconstrained; verify any delegated read yourself. There is no mandatory independent Reviewer: the source-bound user confirmation is the only approval gate for a durable write.
- Never modify product code, merge any PR, close the source Issue, or approve a proposal for the user.
- Never write active rules, wiki pages, or stable memory outside the exact proposal destinations.

## Accept the semantic input

Require the Issue URL and merged source product PR URL. For a confirmation, revision, or pause round, additionally require the root Skill's exact `user_decision` binding the sole active `awaiting-confirmation` whole comment by URL and digest. Reject a bare reply, stale binding, or ambiguous decision before any mutation.

## Route existing lineage or classify fresh

1. Re-read the Issue, merged source PR tuple and merge identity, the complete source-PR comment set, and related project-memory PRs.
2. When a current-format promotion lineage already exists—`awaiting-confirmation`, `confirmed`, `memory-pr-merged`, or `no-promotion`—resume that exact state under `references/evidence-contract.md`. Never restart classification over persisted state.
3. When the source tuple satisfies the evidence contract's code-only admission, return `direct-no-promotion` without persisting anything.
4. Otherwise classify fresh.

## Classify promotable knowledge

Judge each of the five categories—`decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, `milestone_evidence`—against the merged diff, tests, Issue contract, and existing authority sources:

- Promote only knowledge with recurring cross-task value that is not already code-discoverable or recorded.
- Give every `no_write` item an explicit category-specific reason.
- Check each candidate destination for conflict or duplication with existing authority content and record the finding.

When a first new round classifies every candidate as `no_write`, return `direct-no-promotion-all-no-write` as an ephemeral result: persist no proposal, no callback, no branch, and no PR. Immediately before any later closure relies on it, revalidate the classification and the continued absence of promotion state.

## Build and persist the proposal

For an actual write:

1. Create or resume one project-memory branch from `develop`; never work on `develop` or `main` directly.
2. Make the minimal authority-file edits that implement the proposal items—no product code, no unrelated memory.
3. Run the validation that the changed memory surface requires, bound to the exact current memory head. Always validate the current head; never carry forward an old-head result.
4. Create or update one Draft project-memory PR targeting `develop`, whose Body summarizes each proposed item, destination, and evidence.
5. Persist the exact **Proposal artifact** and the marker-bearing **`awaiting-confirmation`** callback from `references/evidence-contract.md` as top-level source product-PR comments, and independently read both back.

## Relay the confirmation gate

Return `awaiting-confirmation` with the proposal URL and whole-comment digest. Under `delivery`, the coordinator summarizes and ends the turn; a standalone invocation ends the same way. Never confirm, mark Ready, merge, or close in the proposal turn.

On a later exact source-bound re-entry:

- `approved` (empty `modification_items`): persist the **`confirmed`** callback bound to the active `awaiting-confirmation` comment, mark the exact memory PR Ready, and return `verified-memory-pr` with the bound tuple.
- `revise` (non-empty `modification_items`): apply the revision as below.
- `pause` (empty `modification_items`): persist nothing, leave the Draft PR and active proposal unchanged, and return blocked with the recovery condition.

Silence, timeout, general delivery intent, or an earlier invocation never authorizes a confirmation.

## Apply revisions

For an exact revision request:

1. Apply every modification item to the proposal and, when affected, to the same Draft memory PR in place.
2. Increment the proposal artifact `revision`, bind the superseded artifact through `revises_artifact_*`, and persist a new `awaiting-confirmation` revision bound through `previous_comment_*`.
3. Return `awaiting-confirmation` again with the new digest.

When a revision turns every item into `no_write`, still persist the revised artifact and callback; after an exact approval, complete the lineage with the **`no-promotion`** terminal instead of a memory PR.

## Complete the confirmed outcome

For a confirmed write, after the guarded memory merge performed by `delivery`:

1. Verify the merge read-back: merged state, exact tuple, merge method/provenance, non-null merge commit identity.
2. Persist the **`memory-pr-merged`** terminal bound to the active `confirmed` callback and the verified merge identity.

For a confirmed all-`no_write` lineage, persist the **`no-promotion`** terminal with complete five-category reasons.

After a terminal, report that the source Issue is ready for closure by the current `delivery` invocation.

## Return a phase result

~~~yaml
outcome: awaiting-confirmation | verified-memory-pr | memory-pr-merged | no-promotion | direct-no-promotion | return-to-spec | blocked
reason: null
issue_url: https://example.com/owner/repo/issues/123
source_pr_url: null
source_head_sha: null
proposal_artifact_url: null
proposal_artifact_sha256: null
proposal_comment_url: null
proposal_comment_sha256: null
confirmation_comment_url: null
confirmation_comment_sha256: null
terminal_comment_url: null
terminal_comment_sha256: null
memory_pr_url: null
memory_pr_title: null
memory_pr_body_sha256: null
memory_head_ref: null
memory_head_sha: null
memory_base_ref: null
memory_base_sha: null
memory_merge_commit_sha: null
changed_files: []
validation: []
recovery_condition: null
next_action: null
~~~

- `direct-no-promotion` with `reason: direct-no-promotion-all-no-write` is the ephemeral exception: bind the exact unchanged Issue and merged source tuple and persist nothing.
- `awaiting-confirmation` must carry the active proposal URL/digest so the user can re-enter with an exact source-bound decision.
- `verified-memory-pr` reports a confirmed Ready memory PR awaiting the `delivery` memory merge gate.
- `memory-pr-merged` / `no-promotion` report a terminal lineage ready for Issue closure.
- `return-to-spec` reports a contract defect discovered during classification; preserve all persisted state.
