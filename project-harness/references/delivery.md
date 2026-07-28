# Delivery

Execute this top-level operation only after `project-harness` dispatches a current user's explicit `role: delivery`.

Coordinate one finalized Issue from Implementation through independent Closeout, exact product integration, user-confirmed Context Promotion, any required project-memory integration, and verified Issue closure. Keep each phase in a fresh Agent and make every transition recoverable from persistent GitHub evidence.

## Contents

- Enforce the coordinator boundary
- Accept the delivery input
- Reconstruct the persistent state
- Dispatch bounded phase Agents
- Run the Implementation and Closeout loop
- Merge the accepted product PR
- Relay the Context Promotion confirmation
- Merge approved project memory
- Persist Delivery stage observations
- Close the source Issue
- Preserve recoverable failure state
- Return the delivery result
- Preserve compatibility

## Enforce the coordinator boundary

- Keep one Delivery Coordinator accountable for dispatch, source re-read, transition validation, merge gates, structured user interaction, Delivery stage observations, terminal reconciliation, and the final result.
- Do not implement product code, repair a failed acceptance, issue an acceptance verdict, classify durable knowledge, edit project-memory files, or review a phase's own work in the coordinator.
- Start a fresh phase Agent for every Implementation attempt, Closeout round, Context Promotion proposal revision, and terminal reconciliation. Supply only the scoped delegation envelope from the root Skill and persistent source URLs.
- Let a phase Agent create sub-agents or sub-subagents under the shared narrowing and ownership rules. Never treat nested delegation as authority to cross a phase boundary.
- Consume a phase result only after independently re-reading every referenced Issue, PR, comment, ref, digest, and state through the loaded transports.
- Validate every Closeout and Context Promotion artifact against `references/delivery-evidence-contract.md`. Use that contract only for persistent schema, tuple/digest, predecessor, active-tip, and legacy dual-read checks; never use it to perform phase reasoning or produce a phase artifact.
- Never ask the user to create a new session for a normal transition. The coordinator consumes the persistent hand-off and creates the next isolated Agent itself.
- Never merge from a phase Agent. Perform the two permitted merge gates only in the coordinator through the loaded Pull Request transport.
- Never request user input outside the Context Promotion confirmation gate.
- Write Delivery stage observations only from the coordinator, after independently verifying the result they summarize. Never delegate this audit mutation or consume a log as phase evidence.

Return completed, return-to-definition, or blocked.

## Accept the delivery input

Require:

~~~yaml
role: delivery
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  # Include the merged proposed-decision PR URL only when the Issue requires it.
next_action: Implement, accept, merge, reconcile durable context, and close the Issue.
~~~

Accept exact related product PR, acceptance comment, promotion callback, or project-memory PR URLs on re-entry only as search hints. Re-read them and prove their relationship to the Issue before use. Reject chat summaries as delivery state or authority.

Before the first mutation, perform the immutable reads and workflow reconstruction in the next section. That read must include the complete source Issue and every paginated top-level comment with `comments_complete: true`.

If reconstruction proves the exact first-read-closed standalone/legacy compatibility no-op with no trusted `finalization-ready`, return completed from read-only evidence. This path performs no mutation or Delivery-log backfill and does not require an unlocked Issue, `add-comment`, or structured-input capability.

For every remaining path that may mutate or backfill, complete this state-aware preflight before the first mutation:

1. Require the source Issue to report `locked: false` and the same authenticated Issue transport to expose the coordinator's `add-comment` capability needed for Delivery observations. Do not unlock an Issue.
2. Inspect every acceptance item for visual, business, real-device, external-system, or other human-only evidence. Require each applicable item already to have a persistent explicit confirmation URL and whole-comment digest bound to the exact current acceptance snapshot. If no product snapshot exists yet, such a confirmation cannot be snapshot-bound.
3. When the reconstructed remaining path has not yet passed a valid source-bound structured confirmation or terminal and can reach the Context Promotion confirmation gate, verify that the top-level coordinator has a callable structured choice-and-free-text input capability. On Codex, it must be `request_user_input` in Plan mode. A fresh delivery must pass this check before its first Implementation mutation. A recovery after an already verified confirmation or terminal does not require the tool merely to reconcile, merge, log, or close.

Return blocked with `recovery_condition: unsupported-delivery-input` before Implementation and before any mutation when an applicable preflight check fails. In particular, do not begin a delivery whose human-only acceptance would require a later live question: the only live user interaction in `delivery` remains the Context Promotion confirmation gate.

Treat the explicit `delivery` invocation as authority, for this one Issue only, to:

- delegate the phase mutations enumerated by Implementation, Closeout, and Context Promotion;
- repair Implementation after a persisted Closeout FAIL;
- merge the exact accepted product PR into `develop`;
- relay one or more source-bound Context Promotion confirmation rounds;
- merge the exact user-confirmed and independently reviewed project-memory PR into `develop`;
- append exact read-back-verified Delivery stage observations to the source Issue;
- write terminal callbacks and close the source Issue after all terminal conditions hold.

Do not extend that authority to another Issue, unrelated branch, unspecified repository metadata, decision PR merge, release/hotfix work, `main`, or any mutation absent from this protocol.

## Reconstruct the persistent state

Before starting a phase:

1. Validate `.project-harness/config.yaml`.
2. Follow the loaded Issue transport to read the exact Issue, its state, complete Body digest, and workflow callbacks.
3. Follow the loaded Pull Request transport to search all related open, closed-unmerged, and merged product and project-memory PRs.
4. Re-read candidate PR Bodies, refs, comments, checks, merge identities, and marker payloads.
5. Validate every candidate Closeout and Context Promotion artifact, whole-comment digest, cross-artifact tuple, predecessor, and active tip under the loaded Delivery evidence contract. Treat the phase result as a search hint only.
6. Require the Issue and Pull Request transport envelopes to expose the same verified authenticated actor login/ID and `mutation_author_login`. Use only that mutation author as the trust root, not a marker or arbitrary comment author. Require the PASS, Issue callback, schema-v2 eligibility registration, and every schema-v2 promotion callback's transport-returned author to match it; apply the explicit legacy migration path when historical authorship differs.
7. Require one unambiguous source lineage. Stop on multiple active product PRs, conflicting callbacks, an untrusted callback author, an unverifiable Issue relationship, or a mixed-Issue branch.
8. Reconstruct the next state from authoritative artifacts, never from prior chat or a coordinator-local plan.
9. Only after workflow reconstruction, request a complete paginated read of all source-Issue Delivery observation candidates. Treat each exact observation binding—URL, normalized whole-comment digest, and schema-valid record—as audit coverage, never as input to steps 1–8.

Use this recovery matrix:

| Persisted exact state | Next coordinator action |
| --- | --- |
| No product PR, or any Draft product PR without a same-run Implementation hand-off already re-read and accepted by this coordinator | Dispatch Implementation to create, resume, or mechanically revalidate the Draft |
| This coordinator has just accepted a verified Implementation hand-off for the exact unchanged Draft tuple, with no current acceptance verdict | Dispatch Closeout |
| Current Closeout FAIL returning to Implementation | Dispatch a fresh repair Implementation Agent |
| Valid PASS comment with any missing Issue callback, eligibility registration, or Ready mutation | Dispatch a fresh Closeout reconciler to complete the remaining idempotent steps |
| Ready product PR whose accepted title/Body/head/base tuple drifted | Dispatch Closeout to convert it to Draft, append a fresh PASS/Issue callback and schema-v2 eligibility successor when the same head can be reaccepted, and otherwise select Implementation or Definition |
| Accepted Ready product PR whose required checks fail because of the product change | Dispatch Closeout to persist the failed current verdict and convert to Draft, then dispatch a fresh repair Implementation Agent |
| Accepted Ready product PR whose mergeability is false because of a repairable `develop` conflict | Dispatch Closeout to invalidate the stale PASS and convert to Draft, then dispatch a fresh Implementation Agent to rebase/repair; require a fresh Closeout round |
| Accepted Ready product PR whose required-check knowledge or mergeability is unknown, checks are pending, or failure is external infrastructure | Wait/re-read when the host supports it; otherwise return blocked with the exact recovery condition |
| Unmerged product PR with only an exact legacy eligibility registration | Dispatch Closeout to migrate through fresh current acceptance and one schema-v2 eligibility successor; do not merge the legacy lineage directly |
| Current Closeout PASS, Issue callback, eligibility registration, and Ready product PR | Enter the product merge gate |
| Current-format exact accepted product PR already merged into `develop`, with no terminal promotion state | Enter the product merge gate's already-merged `no-op` recovery; dispatch Context Promotion only after the transport verifies the complete current gate evidence, method, provenance, checks, and tuple |
| Historically merged product PR with an exact legacy eligibility lineage | Use only the explicit read-only legacy integration exception: verify every field the historical producer promised plus current merged head/base identity, allowed actual method, merge provenance, and known successful head checks; then dispatch Context Promotion with computed legacy comment digests and require schema-v2 proposal/review/confirmation migration before any new memory merge or Issue close |
| `awaiting-confirmation` promotion callback | Re-read and relay that exact proposal |
| `confirmed` no-write proposal without terminal callback | Dispatch Context Promotion terminal reconciliation |
| `confirmed` no-write proposal whose authority base or bound current-authority source drifted | Dispatch Context Promotion to invalidate the confirmation, rebuild/review the five-category proposal, and return to structured confirmation |
| `confirmed` project-memory proposal with a Draft PR | Dispatch Context Promotion to mark the exact reviewed tuple Ready and persist `memory-pr-ready` |
| Confirmed, reviewed, Ready project-memory PR without a valid `memory-pr-ready` callback | Dispatch a fresh Context Promotion reconciler; do not merge |
| Valid `memory-pr-ready` callback plus the unchanged confirmed/reviewed Ready project-memory PR | Enter the project-memory merge gate |
| Ready project-memory PR whose required checks fail because of a permitted context file or validation defect | Dispatch Context Promotion to convert it to Draft, repair within promotion scope, persist a new artifact and fresh review, and return to the same structured confirmation gate |
| Ready project-memory PR whose confirmed title/Body/head/base tuple drifted, base advanced, or mergeability is false because of a repairable promotion-scope conflict | Dispatch Context Promotion to convert it to Draft, rebase/repair within scope, persist a new artifact and fresh review, and return to structured confirmation; block when safe repair exceeds promotion authority |
| Ready project-memory PR whose checks or mergeability are pending/unknown, or checks fail only because of external infrastructure | Wait/re-read when supported; otherwise return blocked without changing the confirmed tuple |
| Exact unmerged legacy `memory-pr-ready` without a schema-v2 confirmation/migration callback | Dispatch Context Promotion to reconstruct, review, and confirm it before any merge |
| Current-format project-memory PR merged without a matching `memory-pr-merged` callback | Enter the project-memory merge gate's already-merged `no-op` recovery; dispatch a fresh Context Promotion reconciler only after the transport verifies the complete current gate evidence, method, provenance, checks, and tuple |
| Exact legacy terminal with an open Issue but no schema-v2 `legacy-reconciliation` confirmation | Dispatch Context Promotion to build, review, and confirm the migration proposal |
| Schema-v2 terminal, or exact legacy terminal plus its schema-v2 migration confirmation, with the Issue still open | Enter the Issue closure gate |
| Current-format terminal and independently verified closed Issue with completion-level schema-v1 Delivery observation coverage | Return completed as a verified no-op |
| Current-format terminal and independently verified closed Issue with a trusted schema-v1 `finalization-ready` but incomplete Delivery observation coverage | Keep the Issue closed; reconstruct any missing required boundary from original evidence, rebuild the stage manifest/finalization chain as needed, and append only the missing `issue-closed`; return blocked with `closed-but-log-pending` if comments are locked or forbidden |
| Exact terminal workflow and Issue already closed in the first immutable read, with no trusted `finalization-ready` | Return completed as a verified compatibility no-op without log backfill; require the full standalone/legacy workflow evidence, because absent logs alone never prove this exception |

When a Draft product PR has both incomplete implementation evidence and a stale Closeout FAIL, prefer Implementation. When a current PASS tuple differs from the current Issue Body, PR Body, head, base, or checks, invalidate it and dispatch the phase required by the changed field. A same-head reacceptance must append a schema-v2 eligibility successor bound to the former active registration URL/digest; consumers use only the sole non-superseded tip. Never select a state by comment recency alone; require its predecessor and tuple bindings.

The coordinator never decides whether a Draft PR satisfies the Product PR contract. After a clean coordinator re-entry, route an unaccepted Draft through Implementation even when it looks complete; the phase Agent may return an exact no-op verification. Only a verified phase hand-off accepted in the current coordinator run permits direct Closeout dispatch.

Every transition must already be reconstructible from GitHub:

- Implementation persists commits, the Draft product PR, and an Execution Packet when required by its phase.
- Closeout persists an append-only verdict, lightweight Issue callback, eligibility registration, and Ready state.
- Product integration persists the PR merge state and merge commit identity.
- Context Promotion persists proposal, confirmation, Ready/terminal callbacks, and any Draft or merged project-memory PR.
- Finalization persists the terminal callback and independently verified Issue state.
- The coordinator separately persists bounded Delivery observations on the source Issue after those authoritative results are verified.

Do not add another run marker or local coordinator checkpoint. Delivery observations use no workflow marker and are not a recovery authority. The existing Issue/PR identities, digests, refs, comments, and three stable marker families remain the workflow recovery index.

If an authoritative success boundary is complete but its observation is absent, append a reconstructed observation with unknown duration before advancing. Never rerun the underlying phase, merge, confirmation, close, or callback merely to obtain timing. If its exact stage-delta baseline is no longer persistent, set that modification domain to `unknown` instead of substituting a different net diff.

## Dispatch bounded phase Agents

Before every dispatch:

1. Re-read the current sources.
2. Capture the attempt's UTC display start and same-process monotonic start for later observation; do not persist a start checkpoint.
3. Build the root Skill's delegation envelope.
4. Bind the Issue, product PR, project-memory PR, and evidence-comment sub-snapshots that apply; leave unrelated sub-snapshots null.
5. Include only exact persistent evidence URLs needed by the phase.
6. Copy the delegated role's exact mutation set from the root Skill, remove any unnecessary mutation for this attempt, and never add another operation.
7. Set `next_action` to one phase outcome, never the full remaining delivery.

Dispatch these roles:

| Delegated role | Phase reference and supporting references | Permitted responsibility |
| --- | --- | --- |
| `implementation` | `references/implementation.md`; Issue transport; Pull Request transport; Issue contract; Product PR contract | Product branch, code/tests, commits, push, Execution Packet, Draft product PR |
| `closeout` | `references/closeout.md`; Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Independent acceptance, append-only verdict/callbacks, Draft/Ready state |
| `context-promotion` | `references/context-promotion.md`; Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Source-bound promotion proposal, project-memory-only branch/PR, independent review, proposal/terminal callbacks |

Forbid a phase Agent from loading `references/delivery.md` or another phase reference. Forbid the coordinator from converting a phase's blocked, indeterminate, or mismatched result into success.

## Run the Implementation and Closeout loop

For Implementation:

1. Dispatch a fresh Implementation Agent with the Issue URL, any required merged decision source, and an existing Draft PR plus the latest FAIL comment when repairing.
2. Require `verified-draft-pr`, a hand-off bound to the Draft PR tuple, all selected validation passing, and persistent evidence that no known acceptance item remains.
3. Re-read the Issue, Draft PR, refs, Body digest, and branch before accepting the hand-off.
4. Append and verify the Implementation attempt observation. For `verified-draft-pr`, require the `implementation-verified-draft` boundary and exact stage-delta change summary.
5. Dispatch Closeout only for the unchanged tuple and verified observation binding: comment URL, normalized whole-comment digest, and schema-valid record.

For Closeout:

1. Dispatch a fresh Closeout Agent with the Issue URL and exact Draft PR URL.
2. Require independent verification and one read-back-verified append-only verdict, then validate that original comment under the loaded Delivery evidence contract.
3. On `return-to-implementation`, require a persisted exact FAIL comment whose tuple and `return_stage: Implementation` validate under the shared evidence contract, and keep/restore Draft state before dispatching a fresh repair Implementation Agent.
4. On `return-to-definition`, stop without editing the Issue and return the exact contract defect.
5. On `blocked`, preserve all persistent state and stop.
6. Append and verify one Closeout round observation for every persisted verdict result.
7. On `accepted-ready-pr`, require the `closeout-accepted-ready` boundary, then re-read the exact PASS comment, Issue callback, active eligibility registration, Ready state, unchanged tuple, and current required-check evidence before entering the product merge gate.

Do not impose an arbitrary retry count. A repaired head always receives a fresh Closeout Agent. Stop only for a genuine external, permission, environment, contract, target-ambiguity, or unrecoverable-state condition.

Closeout must not call `request_user_input`. When the Issue includes a genuinely human-only acceptance item, require already persisted confirmation bound to the exact snapshot. If it is absent, return blocked; do not reinterpret the `delivery` invocation as blanket acceptance.

## Merge the accepted product PR

Immediately before merge or current-format already-merged recovery:

1. Re-read the Issue, product PR, refs, Body, PASS comment, Issue callback, eligibility registration, and checks.
2. For a new merge, require an open Ready PR targeting `develop`, the accepted exact title and head ref/SHA, unchanged Issue and PR Body digests, unchanged base SHA, known and successful required checks, and affirmatively established `mergeable: true` or the selected transport's authoritative equivalent. Unknown mergeability is blocked. For an already-merged recovery, require non-Draft state, the same accepted tuple and evidence, currently known successful required checks for the exact head, actual integration into `develop`, verified merge provenance, and the actual merge method; do not require post-merge mergeability.
3. Require the eligibility registration URL/digest pair to bind the same acceptance comment URL/digest, Issue callback URL/digest, and accepted tuple. Re-read each complete comment and compare its original whole-comment digest.
4. Establish one exact merge method from authoritative repository rules. Stop blocked when multiple methods remain possible without an authoritative choice.
5. Supply the exact baseline, protected fields, merge method, all three gate-evidence URL/digest pairs, and current `delivery` authority to the loaded Pull Request transport's `merge` operation. Use this same operation for current-format already-merged recovery and accept only its exact `no-op`.
6. Independently read the PR back through the same transport.
7. Require `merged: true`, base ref `develop`, the accepted title/Body/head tuple, the guarded base lineage, preserved non-base protected fields, and a non-null merge commit identity. Accept only `verified` or an exact-tuple `no-op`.

If the tuple changes while the PR remains open, invalidate acceptance and dispatch the affected phase again. If an inconsistent tuple was merged, return blocked and do not manufacture eligibility or acceptance evidence.

After verified product merge or exact current-format `no-op` recovery, append and verify the `product-merged` boundary observation with method, provenance, merge identity, and final product net-change evidence. Then re-read the Issue and dispatch a fresh Context Promotion Agent with only the Issue URL, merged product PR URL, eligibility registration URL/digest, acceptance comment URL/digest, Issue callback URL/digest, and bound source tuple.

The historical legacy integration row is a read-only compatibility exception because its producer did not persist the complete current tuple. It never authorizes or recovers a new merge mutation and must not be reported as a current-format transport `no-op`. Require the strict legacy source checks plus transport-verified current merge provenance, allowed actual method, merged head/base lineage, merge identity, and known successful head checks before entering the confirmation migration.

## Relay the Context Promotion confirmation

Require Context Promotion to finish source verification, persist an exact proposal artifact, build any exact Draft project-memory PR, run validation, persist a fresh read-only Reviewer PASS for either a write or no-write proposal, and persist one read-back-verified schema-v2 `outcome: awaiting-confirmation` callback before asking the user.

After re-reading that result, append and verify one `context-proposal-reviewed` boundary observation for the exact active revision. Record only proposal item identities/classifications/destinations and artifact URL/digest; never copy proposed prose.

Independently re-read the state callback, exact proposal artifact, Reviewer evidence, eligibility registration URL/digest, bound `develop` authority base, and every referenced evidence/current-authority source with its recorded digest. If any digest or tuple changed, dispatch a fresh Context Promotion revision instead of displaying or approving the stale artifact. Present the user with all proposal details from the artifact:

- every candidate conclusion;
- `add`, `update`, `supersede`, or `no_write` action;
- classification and exact authority-layer destination path;
- exact proposed context change or category-specific no-write reason;
- whether confirmation is merely source-confirming or an `explicit-user-decision`, and the exact authority effect that integration will create;
- source evidence, current authoritative statement, conflict/duplication result, and omission risk;
- any exact memory PR superseded by this revision, its Draft/non-active state, tuple, and reason;
- Reviewer PASS URL/digest for every proposal and, for a write, project-memory PR URL, changed paths, diff summary, Body/head/base tuple, and validation.

Immediately before displaying those details, capture a Context confirmation timing start. Then use `request_user_input` on Codex or the host's equivalent structured input tool. Ask one source-digest-bound question with:

- **Approve exact proposal (Recommended)** — approve only the displayed callback URL and digest;
- **Pause without integration** — preserve the Draft/proposal and leave the Issue open;
- the tool's free-text alternative for exact modification items.

Do not set an automatic resolution or default. Do not use an ordinary chat question as a fallback.

Handle the response:

- On exact approval, re-read the source, eligibility registration, authority base, every artifact evidence/current-authority source, artifact, Reviewer PASS, state callback, and any memory PR tuple. Populate the delegation envelope's host-provenance-bound `user_decision` with `decision: approved` only if every URL/digest still matches, then dispatch a fresh Context Promotion Agent to persist a `confirmed` callback and continue in that same phase invocation to the applicable `no-promotion`, `memory-pr-ready`, `memory-pr-merged`, or verified legacy-terminal result. `confirmed` alone is a recoverable interrupted state, not a successful phase result.
- On modification items, populate `user_decision` with `decision: revise`, the exact proposal URL/digest, and the structured response's `modification_items`, then dispatch a fresh Context Promotion Agent to validate them against the Issue, merged evidence, classification rules, and authority boundaries. Require a new Draft tuple or no-write assessment, fresh validation, a fresh Reviewer, and a new `awaiting-confirmation` callback. Present the new revision and ask again.
- On pause, unavailable structured-input capability, ambiguous response, or source drift, return blocked with the exact persisted proposal and recovery condition.
- On a requested change that alters the product contract or exceeds Context Promotion authority, return return-to-definition or blocked as the phase specifies. Do not treat free text as a hidden code or policy patch.

Any change to source identity, proposal content, classification, destination, changed paths, project-memory PR Body/head/base tuple, validation, or Reviewer verdict invalidates an earlier confirmation.

After the confirmation path produces a verified persistent result, append one Context confirmation observation. On approval, require the `context-confirmed` boundary bound to the schema-v2 confirmation callback. On revision, pause, or blocked input, best-effort write an attempt observation from the current live structured result with only the response kind and modification item count; never persist raw input or its digest. If interruption loses that result before logging, do not reconstruct it or block recovery on its absence. When revision work produces the next reviewed proposal, record that proposal in its own `context-proposal-reviewed` boundary.

This is the only interactive gate in `delivery`.

## Merge approved project memory

For an approved no-write proposal:

1. Require a read-back-verified `confirmed` callback bound to the current proposal.
2. Require the approval phase to write and verify the exact `no-promotion` terminal callback. Dispatch a fresh Context Promotion reconciler only when recovery finds an interrupted, already persisted `confirmed` tip.
3. Skip branch, commit, PR, and merge creation.
4. Append and verify the `context-no-promotion-terminal` boundary observation.

For an approved write proposal:

1. Require the `confirmed` callback, exact proposal artifact and Reviewer PASS, valid `memory-pr-ready` callback, and Context Promotion's verified Ready project-memory PR result. Bind and re-read the eligibility registration URL/digest and every predecessor URL/digest.
2. Re-read the source Issue/product PR, authority sources, proposal artifact/state and confirmation callbacks, memory PR title, complete changed files/diff, head ref/SHA, base ref/SHA, Body digest, checks, and Ready or merged state.
3. Require the diff to contain only the approved authority-layer paths and exact approved conclusions, the sorted changed-file/blob identities to match artifact/Reviewer/Ready evidence, and `authority_base_sha == memory_base_sha` for the active revision.
4. Require `required_checks_known: true` and every required check successful. For a new merge, also require affirmatively established mergeability. If a failed check proves a context-file or validation defect within Context Promotion authority, dispatch a fresh Context Promotion repair round: convert the exact Ready PR to Draft, repair it, persist a new artifact, obtain a fresh Reviewer PASS, and ask for structured confirmation again. If checks are pending/unknown or failure is external infrastructure, wait/re-read when supported or return blocked without mutating the tuple. For an already-merged recovery, require non-Draft state, verified merge provenance, actual integration into `develop`, and the actual allowed merge method; do not require post-merge mergeability.
5. Establish the repository-authoritative merge method.
6. Call the loaded Pull Request transport's `merge` operation with the exact confirmed/reviewed tuple, protected fields, and proposal-artifact, confirmation, Reviewer PASS, and memory-pr-ready URL/digest pairs. Use this same operation for current-format already-merged recovery and accept only its exact `no-op`.
7. Independently verify merge into `develop`, unchanged title/head/Body/paths and guarded base lineage, and a non-null merge commit identity.
8. Dispatch a fresh Context Promotion reconciler to append and verify the exact `memory-pr-merged` callback bound to the eligibility registration, proposal, confirmation, project-memory PR, Reviewer PASS, and merge identity.
9. Append and verify `memory-pr-merged` after the exact merge/no-op recovery, then append and verify `context-memory-terminal` after the reconciler callback. Record the measured span on only the action that owned it; do not duplicate elapsed time across both observations.

Never merge a Draft, unconfirmed, unreviewed, changed, check-failing, wrong-base, ambiguous, or unrelated project-memory PR.

After Context Promotion marks an approved project-memory PR Ready and persists its callback, append and verify the `memory-pr-ready` boundary before entering the merge gate.

## Persist Delivery stage observations

Follow `references/delivery-log-contract.md` as the only observation schema and aggregation source.

For every bounded phase Agent attempt, merge gate, confirmation round, reconciliation, and finalization gate:

1. Accept the underlying result only from original authoritative evidence.
2. Build one boundary observation for a successful durable boundary or one attempt observation for another persisted outcome. Give each live execution one UUIDv4 `attempt_id`; reuse it only for exact ambiguous-write recovery. Leave it null for a reconstructed/unknown-timing boundary.
3. Use `scripts/delivery_log.py` to validate the payload and calculate its transition key.
4. Read every source Issue comment page and require `comments_complete: true`.
5. Compare trusted exact candidates by normalized whole-comment digest and transition key.
6. Add the observation through the Issue transport only when an exact Body is absent.
7. Independently read the new or existing comment back and require the coordinator's verified mutation-author identity.

Do not block workflow merely because duplicate observations share one transition key. Do block advancement when a required successful-boundary observation is absent or cannot be independently verified; this does not invalidate or roll back the underlying workflow state. A persistently evidenced non-success attempt should be logged, but it never satisfies coverage. The live-only revision/pause/blocked confirmation attempt is best-effort and cannot block re-entry after its tool result is gone. On re-entry, recover workflow truth first, then backfill a missing successful boundary with `timing_quality: reconstructed` or `unknown` and null elapsed time.

Keep previews bounded and link full PR/artifact evidence. Never log raw user input, prompts, reasoning, chat, Reviewer prose, tool output, secrets, environment values, absolute local paths, or uncommitted content.

## Close the source Issue

Enter the closure gate only when all conditions hold:

- the exact Closeout-accepted product head is merged into `develop`;
- the PASS comment, Issue callback, and eligibility registration URL/digest pairs remain valid;
- the Issue Body digest remains the bound delivery contract;
- for a current-format lineage, the active terminal chain contains one exact non-invalidated schema-v2 `confirmed` callback and ends in either verified `no-promotion` or the exact approved project-memory PR verified merged with its `memory-pr-merged` callback;
- for a legacy lineage only, the sole active schema-v2 tip is the exact `legacy-reconciliation` confirmation bound to one verified legacy `no-promotion` or `memory-pr-merged` terminal; that legacy callback supplies terminal outcome evidence without creating a duplicate terminal;
- no conflicting active or terminal promotion state exists; an exact legacy `no-promotion` predecessor bound and superseded by the active schema-v2 write branch is audit evidence rather than a conflict, and any other open memory PR is an exact Draft proven superseded by the active artifact/state/comment chain.
- every required success boundary for the active no-write or project-memory path has one exact trusted observation binding—comment URL, normalized whole-comment digest, and schema-valid record—bound to the same authoritative evidence.
- the source Issue currently reports `locked: false`, and the selected Issue transport still exposes the same authenticated `add-comment` capability needed for the post-close observation; never unlock an Issue as part of Delivery.

Then:

1. Capture one UTC/monotonic closure-gate start, then re-read every source, terminal callback, and selected exact observation binding.
2. Build the exact 6/8-boundary stage coverage manifest from those URL/whole-comment-digest/record bindings and append/read back one `finalization-ready` boundary observation. Require `coverage(..., level="closure")` to prove 7/9 coverage.
3. Re-read every original workflow artifact and selected observation binding again. Treat URL, whole-comment digest, record, or source drift as invalidating only that readiness observation; rebuild coverage instead of using it as authority.
4. Follow the loaded Issue transport to perform one explicit `change-metadata` mutation setting `state: closed` and `state_reason: completed` on the exact source Issue.
5. Protect the Issue identity, title, Body digest, comments, and all unrelated metadata.
6. Independently read the Issue back through the same transport. Accept only `verified` or `no-op` with `state: closed`, `state_reason: completed`, matching identity/digest, preserved fields, and `read_back_verified: true`.
7. Append and independently verify one `issue-closed` boundary observation to the still-closed Issue. For this live fresh close, bind the same path kind, exact stage-manifest digest, and exact finalization observation, record `outcome: verified` plus the completed `change-metadata` mutation, and attach the one measured closure-gate span here; keep the preceding finalization observation reconstructed/null-timed to avoid double-counting. When recovering an Issue that was already closed at gate entry, use `outcome: no-op`, reconstructed/unknown timing, `change_quality.github: unknown`, an empty `github_mutations` list, and a non-null reason code; never report recovery duration as close duration or reconstruct a historical `change-metadata` mutation from current state.
8. For an ambiguous observation response, perform one complete exact comment search. If comments are locked, forbidden, or still indeterminate, keep the Issue closed and return blocked with `closed-but-log-pending`; never reopen or repeat the close mutation.
9. Re-read the Issue once more and require it to remain `closed`/`completed`, then require `coverage(..., level="completion")` to prove 8/10 coverage before returning completed.

Do not use a closing keyword or infer closure from either PR merge or from `finalization-ready`. The post-close observation is audit-only and cannot turn an open Issue into a completed delivery.

## Preserve recoverable failure state

Before returning blocked:

- ensure the latest coherent branch/PR work is committed and pushed when its phase authorizes that action;
- persist the latest phase verdict or promotion proposal when GitHub writing remains available;
- report exact Issue/PR/comment URLs, digests, head/base tuple, merge identities, current state, completed validation, blocker, and recovery condition;
- append an attempt observation when the bounded outcome and safe summary are persistently evidenced; never invent one from transient chat or uncommitted work;
- leave the Issue open unless the closure gate already completed and read-back proves it closed.

Do not claim a transition that exists only in an Agent return value. If a mutation response is ambiguous, use transport recovery reads and otherwise return blocked or indeterminate as specified by the transport.

## Return the delivery result

Return:

~~~yaml
outcome: completed | return-to-definition | blocked
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
  duplicate_transition_count: 0
  attempt_observations_by_stage: {}
  measured_elapsed_ms_by_stage: {}
  measured_elapsed_ms_total: 0
  unknown_timing_count: 0
  user_wait_ms_total: 0
  change_items_by_stage: {}
  unknown_change_domains_by_stage: {}
  final_product_net:
    files_changed: 0
    additions: 0
    deletions: 0
  final_memory_net:
    files_changed: 0
    additions: 0
    deletions: 0
  finalization_observation_url: null
  finalization_observation_sha256: null
  issue_closed_observation_url: null
  issue_closed_observation_sha256: null
  coverage_manifest_sha256: null
  coverage_level: null | manifest | closure | completion
  diagnostics: []
validation: []
reason: null
recovery_condition: null
handoff:
  role: definition | delivery | null
  authoritative_sources: []
  next_action: null
~~~

Return `completed` only with `issue_closure: closed`, `issue_state_verified: true`, and either current `coverage_level: completion` or the exact first-read-closed compatibility no-op exception with no trusted `finalization-ready`. For return-to-definition, preserve delivery artifacts and identify the exact changed or missing contract item. For blocked, set hand-off to `delivery` only when a later explicit re-entry can resume safely from the reported persistent state; `closed-but-log-pending` is such a recovery condition and never authorizes reopening.

Map phase fields without renaming their evidence: Context Promotion `proposal_artifact_*` becomes delivery `promotion_artifact_*`; `proposal_comment_*` becomes `promotion_proposal_*`; `confirmation_comment_*` becomes `promotion_confirmation_*`; and terminal `source_callback_*` becomes `promotion_terminal_*`. Copy both URL and digest and re-read the source before returning them.

Populate `stage_logs` only from complete paginated reads and exact observation bindings whose comment URL, normalized whole-comment digest, schema-valid record, and author are independently verified. Count attempts and measured spans by unique non-null `attempt_id`; do not count duplicate comments twice. Sum measured coordinator spans only, report reconstructed/unknown timing and change domains separately, and calculate final net file totals from the final product/memory PR diffs rather than retry previews.

## Preserve compatibility

- Keep `implementation`, `closeout`, and `context-promotion` callable as exact standalone phase roles. They retain their phase-scoped mutation authority and stop before merge.
- Keep all existing Issue and Product PR Body headings and digest rules unchanged.
- Keep the three existing marker names unchanged.
- Keep Delivery observations unmarked, audit-only, and additive. An exact standalone or legacy lineage already closed in the first immutable read with no trusted `finalization-ready` remains a completed compatibility no-op without backfill. Open lineages backfill required successful boundaries with unknown timing before finalization. A current Delivery-log schema-v1 lineage whose Issue closed after a trusted finalization but before `issue-closed` remains closed and reconstructs the missing observation chain only.
- Treat `delivery` and schema-v2 promotion callbacks as an additive protocol migration: existing exact phase invocations keep their old stopping boundaries, while callers opt into automatic orchestration only by explicitly selecting `role: delivery`.
- Dual-read existing Context Promotion callbacks under the strict legacy rules. Treat an exact standalone or legacy terminal workflow plus an Issue already closed in the first immutable read, with no trusted `finalization-ready`, as completed compatibility no-op evidence; missing logs alone never suffice without the complete workflow proof.
- When a legacy callback leaves the Issue open, reconstruct an exact schema-v2 proposal artifact, persist a fresh Reviewer PASS, and obtain structured confirmation before any new merge or close. For a legacy project-memory PR already merged before this protocol, confirm a `legacy-reconciliation` proposal and then persist the schema-v2 terminal without pretending the confirmation happened before that historical merge.
