# Delivery

Execute this operation only after `project-harness` dispatches a current explicit `role: delivery` invocation.

Coordinate one finalized Issue through implementation, review, guarded product integration, optional project-memory promotion, and verified Issue closure. Prefer the code-only path and add process only when the current evidence requires it.

## Contents

- Enforce the coordinator boundary
- Accept and preflight the delivery
- Reconstruct the next action
- Run Implementation and Review
- Merge the accepted product PR
- Select code-only or Context Promotion
- Relay a real memory-write confirmation
- Merge approved project memory
- Close the source Issue
- Preserve recoverable failure state
- Return the delivery result

## Enforce the coordinator boundary

- Stay accountable for source reads, state reconstruction, phase sequencing, automatic merge gates, any required user confirmation relay, final closure, and the result.
- Run each phase by loading its reference and following it—directly or through subagents at your discretion. The Harness fixes no topology, delegation envelope, or phase-owner isolation; the phase artifacts and gates below are unchanged regardless of how the work is decomposed.
- Re-read the exact persistent artifacts and mutable tuple fields needed by the next boundary. Do not reacquire complete unchanged payloads merely to prove independence.
- Perform product/memory merges and final Issue closure only through the loaded transports under this invocation's authority.
- Open a user decision gate only for an actual project-memory write proposal or an already-persisted current-format promotion state that requires it.
- Never convert a `blocked`, `indeterminate`, mismatched, or stale phase result into success.

Return `completed`, `return-to-spec`, or `blocked`.

## Accept and preflight the delivery

Require one finalized Issue URL. Treat other supplied PR or callback URLs as search hints and independently prove their relationship.

For a confirmation re-entry, require the root Skill's exact `user_decision`. Reject malformed decision/item combinations before mutation. Reconstruct the active promotion state and require the claimed proposal URL/digest to equal the sole active `awaiting-confirmation` whole comment before using the decision.

Before the first mutation:

1. Read the Issue Body, state, exact marker-bearing workflow comments needed to classify the lineage, and related product/memory PRs. Request complete comment pagination only when candidate state or an atomic comment mutation response is ambiguous.
2. Parse `.project-harness/config.yaml` with `scripts/config_guard.py`. Bind schema, namespace, `develop` base, policy source, and configured methods.
3. Require repository metadata to prove the product merge method is available before product work that can lead to integration. Defer the memory-method capability check until a real memory write path exists.
4. Verify the Issue/PR transports expose the same authenticated actor and mutation-author identity for the mutations currently needed.
5. Inspect human-only acceptance items. Do not block code implementation merely because no product snapshot exists yet; require exact snapshot-bound persistent human confirmation before Review can PASS that item.

For schema-v1 with multiple available merge methods, return `merge-policy-migration-required` before the first lifecycle mutation and hand off to `role: init`. For an unavailable configured method, return blocked rather than selecting another or asking for a manual merge.

Authorize only this Issue's phase mutations, configured PR merges, the required write-proposal confirmation relay, and final explicit Issue closure. Do not extend authority to another Issue, unrelated branch, `main`, release/hotfix work, or unspecified metadata.

## Reconstruct the next action

Recover from GitHub state rather than chat:

1. Read the exact Issue and relevant workflow comments.
2. Search related open, closed-unmerged, and merged product and project-memory PRs.
3. Read only candidate PR Bodies, refs, required checks, merge identity/provenance, changed files, and evidence comments needed for the candidate state.
4. Validate Review verdicts and any existing Promotion artifacts under `references/evidence-contract.md`.
5. Require one unambiguous Issue/product lineage and trusted mutation author.

Use this priority order:

| Current exact state | Next action |
| --- | --- |
| Issue already closed and the selected code-only or promotion completion evidence still validates | Return completed through read-only `no-op` verification |
| No product PR exists, or the product PR is still unmerged, and the Issue lacks a non-placeholder `### 改动范围` with both `普通业务改动` and `受保护改动` | Return `return-to-spec` for the one-time format migration; do not edit the Issue in Delivery |
| Any current-format `awaiting-confirmation`, `confirmed`, or terminal promotion state exists | Resume that exact promotion lineage; never select the fast path |
| No product PR or one incomplete Draft product PR exists | Run Implementation to create, resume, or repair it |
| No current-format review verdict exists for the current Draft tuple | Run Review |
| Review FAIL targets Implementation | Run a repair Implementation round for the changed repair target |
| Review FAIL targets Spec | Return `return-to-spec` without editing the Issue |
| Review PASS exists but Ready state is incomplete | Complete the idempotent Ready step |
| Accepted Ready product PR has tuple drift or a product-caused check/conflict failure | Restore Draft and run the required Review or Implementation repair round |
| Accepted Ready product PR has pending/unknown checks, unknown mergeability, or external infrastructure failure | Wait/re-read when supported, otherwise return blocked without changing the tuple |
| Accepted Ready product PR is unmerged | Enter the product merge gate |
| Exact accepted product PR is already merged | Verify the merge through the same product merge gate's `no-op` path, then select code-only or Context Promotion |
| Merged product PR satisfies the exact code-only admission and no promotion state exists | Enter the code-only closure gate |
| Merged product PR does not satisfy code-only admission and no promotion state exists | Run Context Promotion |
| Context Promotion returns direct first-round `no-promotion` | Enter closure without writing a promotion callback |
| Context Promotion returns `awaiting-confirmation` for a write | Summarize and end the turn for exact source-bound re-entry |
| Confirmed Ready memory PR exists | Enter the memory merge gate |
| Current memory PR is merged but the terminal is absent | Verify merge through the memory gate, then persist the terminal |
| Promotion path is terminal | Enter closure |

Do not select workflow state by comment recency. Validate exact tuple/digest and predecessor bindings for every existing lineage.

Treat the format-presence row above as Delivery's sole scope-related routing check. Verify only that the compact fields exist and are non-placeholder; never classify a change, map files, or add acceptance evidence here. Do not apply this migration row to an already-merged `no-op` recovery, and never use that exception to authorize another product mutation.

## Run Implementation and Review

For Implementation:

1. Run the phase with the Issue and, when repairing, the existing Draft PR plus exact FAIL verdict comment.
2. Require `verified-draft-pr`, all selected risk-proportionate validation passing, no known unfinished contract item, and a complete Product PR Body.
3. Re-read the Issue and exact Draft PR title/Body/head/base tuple before accepting the result.

For Review:

1. Run the phase with the exact Issue and Draft PR.
2. Require the three review items judged against the complete diff and current-head evidence. Permit reuse of exact current-head Implementation validation and current successful required CI when their scope is applicable; require re-execution only for missing, stale, contradicted, or risk-required checks.
3. Require one read-back-verified append-only verdict under the shared evidence contract.
4. On `return-to-implementation`, validate the persisted FAIL and run a repair round. On `return-to-spec`, stop. On external/permission/environment/human-confirmation blockers, preserve state and stop.
5. On PASS, require Ready state, unchanged tuple, current required-check knowledge, and successful required checks.
6. Re-read the Product PR's five fixed durable-memory rows and the PASS. Treat `code_only_verified: true` only when each impact is exactly `无` and the PASS contains the exact `durable-memory-impact` / `PASS` / `all-five-none` item. Otherwise require `promotion_required: true`.

## Merge the accepted product PR

Immediately before a new merge or already-merged recovery:

1. Re-read the Issue, product PR, refs, Body, the review PASS, required checks, and mergeability/state.
2. Require open Ready state for a new merge, base `develop`, unchanged accepted title/Body/head/base tuple, `required_checks_known: true`, every required check successful, and affirmative mergeability.
3. Re-parse Harness config and repository capability; require the product method to equal the preflight binding and remain available.
4. Call the Pull Request transport's `merge` with the exact protected baseline and the protocol-owned `review-pass` evidence pair.
5. Independently read back merged state, accepted tuple, guarded base lineage, merge method/provenance, and non-null merge identity. Accept only `verified` or exact `no-op`.

If the tuple changes while open, invalidate acceptance and return to the affected phase. If an inconsistent tuple is already merged, return blocked.

## Select code-only or Context Promotion

After verified product integration, re-read the Product PR Body, the exact review PASS, the complete top-level source-PR comment set needed to prove absence of promotion artifacts, and the complete related memory-PR search.

Select `code-only` only when every **Code-only admission** rule in `references/evidence-contract.md` passes: all five rows exactly once with `实际影响: 无`, exact PASS evidence `durable-memory-impact` / `PASS` / `all-five-none`, unchanged source tuple, and verified absence of promotion state and related memory PR.

For `code-only`, skip Context Promotion and enter closure. Do not produce an empty branch, no-write proposal, confirmation, terminal callback, finalization comment, or post-close comment.

When admission is false because any actual/possible durable conclusion exists, run Context Promotion. When evidence is missing, malformed, contradictory, or ambiguous, block or repair the Product PR/Review evidence rather than assuming either path.

A first new Context Promotion round may return direct `no-promotion` after independently proving every candidate is code-discoverable, duplicate, or lacks recurring value. Accept this result without a proposal or user gate only when no promotion lineage existed and the phase returns the unchanged source tuple. If any write remains, require the proposal path. If any promotion state already exists, resume that lineage instead.

## Relay a real memory-write confirmation

For a write proposal, require Context Promotion to persist the exact proposal artifact, Draft memory PR, and `awaiting-confirmation` callback. Re-read those identities and the current source/authority/memory tuple before presenting them.

Summarize every proposed change, destination, authority effect, source evidence, changed path, validation result, and proposal URL/whole-comment digest. Offer approve, pause, or exact revision. End the turn with `recovery_condition: awaiting-context-promotion-decision`; do not confirm, mark Ready, merge, or close in that turn.

On re-entry:

1. Reconstruct the sole active proposal and require exact URL/digest match.
2. Re-read source, authority, proposal, and memory tuple.
3. On exact approval, run Context Promotion with the bound `user_decision` to persist `confirmed` and mark the exact memory PR Ready.
4. On revision, persist a new proposal revision and `awaiting-confirmation`, then end the turn again.
5. On pause, leave the proposal and Draft PR unchanged and return blocked.

Never use raw free text as patch authority. Never require this gate for a new all-no-write classification.

## Merge approved project memory

For a confirmed write:

1. Require the exact proposal artifact, confirmation, and unchanged Ready memory PR tuple/diff.
2. Require current-head required checks known and successful, affirmative mergeability for a new merge, and the configured memory method still available.
3. Re-parse Harness config and re-read the protocol-owned `proposal` and `confirmation` evidence pairs immediately before merge.
4. Merge through the Pull Request transport and independently verify method, provenance, guarded tuple, changed paths, and merge identity.
5. Persist and verify the exact `memory-pr-merged` terminal.

If a permitted memory-only defect or safe base repair changes the tuple, return it to Draft, persist a new proposal revision, and obtain a later confirmation. Do not reuse old-head CI or an old confirmation. Block pending/unknown/external failures without changing the confirmed tuple.

## Close the source Issue

Enter closure through exactly one path:

- **code-only:** exact accepted product tuple verified merged; code-only admission still exact; no promotion state or related memory PR exists.
- **direct no-promotion:** exact accepted product tuple verified merged; the first new Context Promotion round returned direct no-promotion for the unchanged source; immediately before closure, revalidate that classification still returns no-write and no promotion state/memory PR appeared.
- **memory promotion:** exact accepted product tuple verified merged; active confirmed project-memory tuple verified merged; exact current `memory-pr-merged` terminal validates.
- **confirmed no-promotion:** a revised all-`no_write` proposal reached the exact `no-promotion` terminal.

For every path:

1. Re-read the Issue Body/state, accepted product tuple and merge identity, required review evidence, selected path evidence, related PR state, and config binding.
2. Require the Issue Body digest unchanged and no conflicting active PR or promotion state.
3. Follow the Issue transport to perform one `change-metadata` mutation setting `state: closed` and `state_reason: completed` while protecting all unrelated metadata.
4. Independently read the Issue back. Accept only `verified` or exact `no-op` with matching identity/digest and protected fields.

Do not require an unlocked comment channel or any post-close comment. Never reopen an Issue for audit repair.

## Preserve recoverable failure state

Before returning blocked:

- commit and push coherent phase work only where that phase authorizes it;
- persist the required review verdict or write proposal when the corresponding transport remains available;
- report exact Issue/PR/comment URLs, digests, head/base tuple, merge identities, validation, blocker, and recovery condition;
- leave the Issue open unless closure already independently verified it closed;
- never fabricate a transition from a phase return.

Use transport recovery reads for ambiguous mutations and otherwise return blocked or indeterminate as specified by the transport.

## Return the delivery result

Return:

~~~yaml
outcome: completed | return-to-spec | blocked
delivery_path: code-only | direct-no-promotion | memory-promotion | confirmed-no-promotion | null
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
product_pr_url: null
product_pr_title: null
product_pr_body_sha256: null
product_head_ref: null
product_head_sha: null
product_base_ref: null
product_base_sha: null
product_merge_commit_sha: null
review_verdict_url: null
review_verdict_sha256: null
code_only_verified: false
promotion_required: null
promotion_artifact_url: null
promotion_artifact_sha256: null
promotion_proposal_url: null
promotion_proposal_sha256: null
promotion_confirmation_url: null
promotion_confirmation_sha256: null
promotion_terminal_url: null
promotion_terminal_sha256: null
promotion_terminal_outcome: null
memory_pr_url: null
memory_pr_title: null
memory_pr_body_sha256: null
memory_head_ref: null
memory_head_sha: null
memory_base_ref: null
memory_base_sha: null
memory_merge_commit_sha: null
issue_closure: open | closed
issue_state_verified: false
issue_state_reason: null | completed
validation: []
reason: null
recovery_condition: null
next_action: null
~~~

Return `completed` only with `issue_closure: closed` and `issue_state_verified: true`. For `awaiting-context-promotion-decision`, require the active write proposal URL/digest and self-contained re-entry packet. For merge-policy migration, name `role: init` with the unchanged namespace and available method evidence. For other recoverable blockers, hand back to `delivery` only when the reported persistent state is sufficient for a later exact re-entry.
