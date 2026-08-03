# Delivery

Execute this operation only after `project-harness` dispatches a current explicit `role: delivery` invocation.

Coordinate one finalized Issue through code implementation, proportional independent acceptance, guarded product integration, optional project-memory promotion, and verified Issue closure. Prefer the code-only path and add process only when the current evidence requires it.

## Contents

- Enforce the coordinator boundary
- Accept and preflight the delivery
- Reconstruct the next action
- Dispatch compact Phase Owners
- Run Implementation and Closeout
- Merge the accepted product PR
- Select code-only or Context Promotion
- Relay a real memory-write confirmation
- Merge approved project memory
- Close the source Issue
- Preserve recoverable failure state
- Return the delivery result
- Preserve compatibility

## Enforce the coordinator boundary

- Keep one Delivery Coordinator accountable for source reads, state reconstruction, compact phase dispatch, automatic merge gates, any required user confirmation relay, final closure, and the result.
- Do not implement product code, repair acceptance, issue a Closeout verdict, classify project memory, edit authority files, or review a phase's own work in the coordinator.
- Start one isolated Phase Owner for each Implementation, Closeout, required Context Promotion proposal/revision, or terminal-reconciliation semantic round.
- Keep the same Owner while its role, bound source tuple, evidence URL/digests, decision, mutation set, and target remain unchanged. Do not replace it for slow tools, liveness changes, Worker failure, or Reviewer FAIL.
- Permit only direct read-only Workers or a fresh independent Reviewer under the root Skill's fixed two-hop topology. Keep the Owner as the sole phase writer and hand-off producer.
- Re-read the exact persistent artifacts and mutable tuple fields needed by the next boundary. Do not reacquire complete unchanged payloads merely to prove independence.
- Perform product/memory merges and final Issue closure only in the coordinator through the loaded transports.
- Open a user decision gate only for an actual project-memory write proposal or an already-persisted legacy/current promotion state that requires it.
- Never write, backfill, repair, or require `delivery-stage-observation` comments. Treat historical observations as optional diagnostics only.

Return `completed`, `return-to-definition`, or `blocked`.

## Accept and preflight the delivery

Require one finalized Issue URL and any merged proposed-decision PR required by the Issue. Treat other supplied PR or callback URLs as search hints and independently prove their relationship.

For a confirmation re-entry, require the root Skill's exact `user_decision`. Reject malformed decision/item combinations before mutation. Reconstruct the active promotion state and require the claimed proposal URL/digest to equal the sole active `awaiting-confirmation` whole comment before using the decision.

Before the first mutation:

1. Read the Issue Body, state, lock state, exact marker-bearing workflow comments needed to classify the lineage, and related product/memory PRs. Request complete comment pagination only when candidate state is ambiguous, an atomic comment mutation response is ambiguous, or a legacy migration contract requires a first-read-complete baseline.
2. Parse `.project-harness/config.yaml` with `scripts/config_guard.py`. Bind schema, namespace, `develop` base, policy source, and configured methods.
3. Require repository metadata to prove the product merge method is available before product work that can lead to integration. Defer the memory-method capability check until a real memory write path exists.
4. Verify the Issue/PR transports expose the same authenticated actor and mutation-author identity for the mutations currently needed.
5. Inspect human-only acceptance items. Do not block code implementation merely because no product snapshot exists yet. Require exact snapshot-bound persistent human confirmation before Closeout can PASS that item.

For schema-v1 with multiple available merge methods, return `merge-policy-migration-required` before the first lifecycle mutation and hand off to `role: init`. For an unavailable configured method, return blocked rather than selecting another or asking for a manual merge.

Authorize only this Issue's phase mutations, configured PR merges, required write-proposal confirmation relay, and final explicit Issue closure. Do not extend authority to another Issue, unrelated branch, decision PR merge, `main`, release/hotfix work, or unspecified metadata.

## Reconstruct the next action

Recover from GitHub state rather than chat or Delivery logs:

1. Read the exact Issue and relevant workflow comments.
2. Search related open, closed-unmerged, and merged product and project-memory PRs.
3. Read only candidate PR Bodies, refs, required checks, merge identity/provenance, changed files, and evidence comments needed for the candidate state.
4. Validate Closeout and any existing Promotion artifacts under `references/delivery-evidence-contract.md`.
5. Require one unambiguous Issue/product lineage and trusted mutation author.

Use this priority order:

| Current exact state | Next action |
| --- | --- |
| Issue already closed and the selected code-only or promotion completion evidence still validates | Return completed through read-only `no-op` verification; never backfill logs |
| No product PR exists, or the product PR is still unmerged, and the Issue lacks a non-placeholder `### 改动范围` with both `普通业务改动` and `受保护改动` | Return `return-to-definition` for the one-time format migration before Implementation, Closeout, or merge; do not edit the Issue in Delivery |
| Any valid `awaiting-confirmation`, `confirmed`, `memory-pr-ready`, terminal, supersession, or legacy promotion state exists | Resume that exact promotion lineage; never select the new fast path |
| No product PR or one incomplete Draft product PR exists | Dispatch Implementation to create, resume, or repair it |
| This coordinator has accepted the unchanged current-run Implementation hand-off and no current Closeout verdict exists | Dispatch Closeout |
| Closeout FAIL targets Implementation | Dispatch a repair Implementation Owner for the changed repair target |
| Closeout FAIL targets Definition | Return `return-to-definition` without editing the Issue |
| Valid Closeout PASS exists but Issue callback, eligibility registration, or Ready state is incomplete | Dispatch Closeout reconciliation for only the missing idempotent steps |
| Accepted Ready product PR has tuple drift or a product-caused check/conflict failure | Restore Draft through Closeout and dispatch the required Closeout or Implementation repair round |
| Accepted Ready product PR has pending/unknown checks, unknown mergeability, or external infrastructure failure | Wait/re-read when supported, otherwise return blocked without changing the tuple |
| Accepted Ready product PR is unmerged | Enter the product merge gate |
| Exact accepted product PR is already merged | Verify the merge through the same product merge gate's `no-op` path, then select code-only or Context Promotion |
| Merged product PR satisfies the exact Lean code-only admission and no promotion state exists | Enter the code-only closure gate |
| Merged product PR does not satisfy code-only admission and no promotion state exists | Dispatch Context Promotion |
| Context Promotion returns direct first-round `no-promotion` | Enter closure without writing a promotion callback |
| Context Promotion returns `awaiting-confirmation` for a write | Summarize and end the turn for exact source-bound re-entry |
| Confirmed/reviewed Ready memory PR exists | Enter the memory merge gate |
| Current memory PR is merged but terminal reconciliation is absent | Verify merge through the memory gate, then dispatch Context Promotion reconciliation |
| Promotion path is terminal | Enter closure |

Do not select workflow state by comment recency. Validate exact tuple/digest and predecessor bindings for every existing lineage. Historical stage observations never choose or block the next action.

Treat the format-presence row above as Delivery's sole scope-related routing check. Verify only that the compact fields exist and are non-placeholder; never classify a change, map files, or add acceptance evidence here. Do not apply this migration row to an already-merged `no-op` recovery, and never use that legacy exception to authorize another product mutation.

## Dispatch compact Phase Owners

Before each new semantic-round dispatch:

1. Re-read only the mutable Issue/PR/comment identities used by that action.
2. Build the root Skill's complete `delegation.schema_version: 3` envelope.
3. Bind the applicable Issue, product PR, memory PR, and evidence comments; leave unrelated snapshot values null.
4. Include only necessary persistent evidence URLs.
5. Copy the role's maximum mutation set from the root Skill and remove mutations not needed by this attempt.
6. Set `next_action` to one phase outcome, never the remaining delivery plan.

Do not attach an Evidence Bundle, component identity map, complete comment inventory, full diff, full checks payload, or tool output. Require the Owner to read the exact sources through the loaded transport and fetch broader evidence only when its phase needs it.

Dual-read an older schema-v2 Evidence Bundle only for a live legacy dispatch and schema-v1 through its historical fresh-read fallback. Emit only schema-v3 for new work.

Dispatch:

| Role | Responsibility |
| --- | --- |
| `implementation` | Product branch, code/tests, commits, push, optional Execution Packet, Draft product PR |
| `closeout` | Independent proportional acceptance, append-only verdict/callbacks, code-only classification, Draft/Ready state |
| `context-promotion` | Only actual candidate classification, project-memory proposal/write, independent write review, confirmation/terminal reconciliation |

Forbid the coordinator from converting `blocked`, `indeterminate`, mismatched, or stale phase results into success.

## Run Implementation and Closeout

For Implementation:

1. Dispatch one Owner with the Issue, any required merged decision source, and an existing Draft PR plus exact FAIL comment when repairing.
2. Require `verified-draft-pr`, all selected risk-proportionate validation passing, no known unfinished contract item, and a complete Product PR Body.
3. Re-read the Issue and exact Draft PR title/Body/head/base tuple before accepting the hand-off.
4. Dispatch Closeout for the unchanged tuple. Do not write an intermediate Delivery observation.

For Closeout:

1. Dispatch one fresh independent Owner with the exact Issue and Draft PR.
2. Require complete diff inspection and an acceptance matrix. Permit reuse of exact current-head Implementation validation and current successful required CI when their scope is applicable; require re-execution only for missing, stale, contradicted, or risk-required checks.
3. Require one read-back-verified append-only verdict under the shared evidence contract.
4. On `return-to-implementation`, validate the persisted FAIL and dispatch a repair Owner. On `return-to-definition`, stop. On external/permission/environment/human-confirmation blockers, preserve state and stop.
5. On PASS, require the Issue callback, active eligibility registration, Ready state, unchanged tuple, current required-check knowledge, and successful required checks.
6. Re-read the Product PR's five fixed durable-memory rows and the PASS. Treat `code_only_verified: true` only when each impact is exactly `无` and the PASS contains the exact `durable-memory-impact` / `PASS` / `all-five-none` item. Otherwise require `promotion_required: true`.

Do not make Closeout rerun the entire Implementation validation suite merely to remain independent. Independence is judgment over the exact diff, contract, current-head evidence, and any checks selected because evidence or risk requires them.

## Merge the accepted product PR

Immediately before a new merge or already-merged recovery:

1. Re-read the Issue, product PR, refs, Body, Closeout PASS, Issue callback, active eligibility registration, required checks, and mergeability/state.
2. Require open Ready state for a new merge, base `develop`, unchanged accepted title/Body/head/base tuple, `required_checks_known: true`, every required check successful, and affirmative mergeability.
3. Require the eligibility registration to bind the same PASS, Issue callback, and accepted tuple.
4. Re-parse Harness config and repository capability; require the product method to equal the preflight binding and remain available.
5. Call the Pull Request transport's `merge` with the exact protected baseline and the three protocol-owned evidence pairs.
6. Independently read back merged state, accepted tuple, guarded base lineage, merge method/provenance, and non-null merge identity. Accept only `verified` or exact `no-op`.

Do not write a product-integration observation. If the tuple changes while open, invalidate acceptance and return to the affected phase. If an inconsistent tuple is already merged, return blocked.

## Select code-only or Context Promotion

After verified product integration, re-read the Product PR Body, exact Closeout PASS, active eligibility, the complete top-level source-PR comment set needed to prove absence of markerless as well as marker-bearing promotion artifacts, and the complete related memory-PR search.

Select `code-only` only when every **Lean code-only admission** rule in `references/delivery-evidence-contract.md` passes. Require all five rows exactly once with `实际影响: 无`, exact PASS evidence `durable-memory-impact` / `PASS` / `all-five-none`, unchanged source tuple, and verified absence of promotion state and related memory PR.

For `code-only`, skip Context Promotion and enter closure. Do not produce an empty branch, no-write proposal, Reviewer PASS, confirmation, terminal callback, Delivery log, finalization comment, or post-close comment.

When admission is false because any actual/possible durable conclusion exists, dispatch Context Promotion. When evidence is missing, malformed, contradictory, or ambiguous, block or repair the Product PR/Closeout evidence rather than assuming either path.

A first new Context Promotion round may return direct `no-promotion` after independently proving every candidate is code-discoverable, duplicate, or lacks recurring value. Accept this result without a proposal or user gate only when no promotion lineage existed at dispatch and the phase returns the unchanged source tuple. If any write remains, require the strict proposal path. If any promotion state already exists, continue the frozen lineage instead.

## Relay a real memory-write confirmation

For a write proposal, require Context Promotion to persist the exact proposal artifact, Draft memory PR, fresh independent Reviewer PASS, and `awaiting-confirmation` callback. Re-read those identities and the current source/authority/memory tuple before presenting them.

Summarize every proposed change, destination, authority effect, source evidence, changed path, validation result, Reviewer PASS, and proposal URL/whole-comment digest. Offer approve, pause, or exact revision. End the turn with `recovery_condition: awaiting-context-promotion-decision`; do not confirm, mark Ready, merge, or close in that turn.

On re-entry:

1. Reconstruct the sole active proposal and require exact URL/digest match.
2. Re-read source, eligibility, authority, proposal, Reviewer PASS, and memory tuple.
3. On exact approval, dispatch Context Promotion with the bound `user_decision` to persist `confirmed` and mark/reconcile the exact memory PR as required.
4. On revision, build a new proposal/review/callback and end the turn again.
5. On pause, leave the proposal and Draft PR unchanged and return blocked.

Never use raw free text as patch authority. Never require this gate for a new all-no-write classification.

## Merge approved project memory

For a confirmed write:

1. Require exact proposal artifact, Reviewer PASS, confirmation, `memory-pr-ready`, eligibility registration, and unchanged Ready memory PR tuple/diff.
2. Require current-head required checks known and successful, affirmative mergeability for a new merge, and the configured memory method still available.
3. Re-parse Harness config and re-read all four protocol-owned evidence pairs immediately before merge.
4. Merge through the Pull Request transport and independently verify method, provenance, guarded tuple, changed paths, and merge identity.
5. Dispatch one Context Promotion reconciliation Owner to persist and verify the exact `memory-pr-merged` terminal.

If a permitted memory-only defect or safe base repair changes the tuple, return it to Draft, create a new proposal/review, and obtain a later confirmation. Do not reuse old-head CI or an old confirmation. Block pending/unknown/external failures without changing the confirmed tuple.

## Close the source Issue

Enter closure through exactly one path:

- **code-only:** exact accepted product tuple verified merged; Lean admission still exact; no promotion state or related memory PR exists.
- **direct no-promotion:** exact accepted product tuple verified merged; the first new Context Promotion round returned direct no-promotion for the unchanged source; immediately before closure, that Context Promotion Owner revalidates the targeted classification and still returns no-write, and no promotion state/memory PR appeared.
- **memory promotion:** exact accepted product tuple verified merged; active confirmed project-memory tuple verified merged; exact current `memory-pr-merged` terminal validates.
- **frozen legacy/current terminal:** every predecessor, confirmation, terminal, merge, and migration rule in the shared evidence contract validates.

For every path:

1. Re-read the Issue Body/state, accepted product tuple and merge identity, required Closeout evidence, selected path evidence, related PR state, and config binding.
2. Require the Issue Body digest unchanged and no conflicting active PR or promotion state.
3. Follow the Issue transport to perform one `change-metadata` mutation setting `state: closed` and `state_reason: completed` while protecting all unrelated metadata.
4. Independently read the Issue back. Accept only `verified` or exact `no-op` with matching identity/digest and protected fields.

Do not require Delivery-log coverage, `finalization-ready`, an unlocked comment channel, or post-close `issue-closed` observation. Never reopen an Issue for audit repair.

## Preserve recoverable failure state

Before returning blocked:

- commit and push coherent phase work only where that phase authorizes it;
- persist required Closeout verdict or write proposal when the corresponding transport remains available;
- report exact Issue/PR/comment URLs, digests, head/base tuple, merge identities, validation, blocker, and recovery condition;
- leave the Issue open unless closure already independently verified it closed;
- never fabricate a transition from a phase return or historical Delivery observation.

Use transport recovery reads for ambiguous mutations and otherwise return blocked or indeterminate as specified by the transport.

## Return the delivery result

Return:

~~~yaml
outcome: completed | return-to-definition | blocked
delivery_path: code-only | direct-no-promotion | memory-promotion | legacy-promotion | null
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
acceptance_comment_url: null
acceptance_comment_sha256: null
issue_callback_url: null
issue_callback_sha256: null
eligibility_registration_url: null
eligibility_registration_sha256: null
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
stage_logs:
  observation_urls: []
  observation_count: 0
  coverage_level: null
  diagnostics: []
validation: []
reason: null
recovery_condition: null
handoff:
  role: init | definition | delivery | null
  authoritative_sources: []
  next_action: null
~~~

Return `completed` only with `issue_closure: closed` and `issue_state_verified: true`; never require `stage_logs.coverage_level`. Keep `stage_logs` only as a backward-compatible diagnostic view of already-existing trusted comments and never write or backfill them.

For `awaiting-context-promotion-decision`, require the active write proposal URL/digest and self-contained re-entry packet. For merge-policy migration, return `handoff.role: init` with the unchanged namespace and available method evidence. For other recoverable blockers, hand back to `delivery` only when the reported persistent state is sufficient for a later exact re-entry.

## Preserve compatibility

- Keep every public role and standalone phase stopping boundary.
- Emit compact delegation schema-v3. Dual-read schema-v2 Evidence Bundle and schema-v1 only for legacy in-flight dispatches.
- Keep Issue/Product PR headings, config schema, merge methods, transport envelopes, marker names, Closeout evidence, promotion callback schemas, whole-comment digest rules, and existing active-tip algorithms unchanged.
- Treat all historical Promotion states as binding recovery state. Do not convert an existing no-write proposal or legacy terminal to the new direct path.
- Treat historical Delivery observations as frozen, audit-only, read-only diagnostics. Do not backfill missing boundaries, build coverage manifests, write `finalization-ready` / `issue-closed`, require `closed-but-log-pending`, or block merge/closure/completion on logs.
- Permit an exact already-closed Issue to return completed after the selected current code-only or promotion evidence is re-read; never require historical log repair.
