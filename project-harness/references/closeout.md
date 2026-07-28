# Closeout

Execute this phase only after `project-harness` dispatches a standalone `role: closeout` or the current `delivery` coordinator delegates the Closeout phase under the root Skill's scoped envelope.

Carry the Closeout phase as an independent acceptance authority. Complete final acceptance for one exact Issue and Pull Request snapshot without becoming a second Implementation Agent.

## Contents

- Enforce the authority boundary
- Accept only the minimal persistent hand-off
- Resolve and bind the acceptance snapshot
- Build the acceptance matrix
- Verify independently
- Re-read before the verdict
- Record an append-only acceptance verdict
- Handle failed or blocked acceptance
- Complete successful acceptance
- Return a closed result

## Enforce the authority boundary

- Start only from one Issue URL and one Draft PR URL supplied by either a current explicit Closeout invocation or a host-provenance-bound delegation from the current explicit `delivery` invocation.
- Use a fresh isolated Agent context with no Implementation conversation history.
- Treat the Issue as the delivery contract and the PR as the implementation result and evidence carrier.
- Independently inspect the diff and rerun applicable acceptance.
- Treat a current user's explicit `$project-harness` invocation with `role: closeout` as authority only for the top-level acceptance/promotion-registration comments, lightweight Issue callback, and Draft/Ready mutations enumerated here. Under `delivery`, accept only the same mutations when the delegation envelope enumerates them and binds the current persistent sources.
- Write only those authorized GitHub artifacts; never derive write authority from an automatic route, serialized envelope, ordinary hand-off, ordinary review request, or prior run.
- Never modify product code, tests, commits, refs, PR Body, Issue Body, or durable project memory.
- Never make even a small implementation fix.
- Never merge, close the Issue, redesign requirements, or convert missing evidence into a PASS.

Return accepted-ready-pr, return-to-implementation, return-to-definition, or blocked.

## Accept only the minimal persistent hand-off

Require:

~~~yaml
role: closeout
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  - https://github.com/owner/repo/pull/456
next_action: Independently accept or reject the Draft PR against the Issue.
~~~

When delegated by `delivery`, also require the root Skill's envelope with `delegated_role: closeout` and the Implementation phase's persistent evidence URLs and bound tuple.

Read both sources and every supplied evidence URL completely. Do not rely on the previous Agent's summary, chat, local plan, or implicit memory.

## Resolve and bind the acceptance snapshot

Follow the loaded Issue and Pull Request transport protocols to prove:

- exact repository and Issue/PR identity;
- open Issue state;
- open PR state and relationship to the Issue;
- Draft state, unless resuming an already recorded exact acceptance;
- Issue Body digest;
- exact PR title;
- PR Body digest;
- head ref and head SHA;
- base ref and base SHA;
- current mergeability when available;
- combined commit status and workflow runs;
- required-check knowledge and observed required checks;
- top-level acceptance comments already present.
- top-level Context Promotion eligibility or terminal callbacks already present.

Bind this tuple:

~~~yaml
issue_body_sha256: SHA256
pr_title: TITLE
pr_body_sha256: SHA256
head_ref: BRANCH
head_sha: COMMIT
base_ref: develop
base_sha: COMMIT
~~~

Stop blocked on target ambiguity, missing read-back, an unverifiable relationship, or unavailable evidence that prevents a safe verdict.

## Build the acceptance matrix

Extract each binding goal, boundary, confirmed decision, and acceptance check from the Issue. Treat the Issue implementation plan as non-binding.

Map every item to:

- executable verification;
- code/diff inspection;
- existing evidence requiring independent confirmation;
- required CI;
- human-only confirmation;
- not applicable with an explicit reason.

Do not add new delivery requirements during Closeout. Return return-to-definition when the existing contract cannot support a valid acceptance decision.

Also map the PR's `持久项目记忆实际影响` claims to the diff, tests, cited ADR/rule/wiki/memory sources, and repository state. Require a factual result or explicit `none` for `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`. Treat single-task records claimed as durable knowledge, unsupported promotion promises, or omitted material effects as PR evidence defects rather than making the promotion decision here.

## Verify independently

- Inspect the complete diff and affected tests.
- Delegate bounded read-only verification to sub-agents or sub-subagents only when separate context materially helps. Keep the Closeout Agent accountable for the complete matrix and verdict; no descendant may edit code, write the verdict, merge, close the Issue, or approve promotion.
- Run every reproducible build, test, static check, smoke test, or acceptance command needed by the Issue and risk.
- Treat Implementation's validation as evidence to confirm, not as a substitute for execution.
- Record exact commands, results, and relevant environment facts.
- Verify every required CI/check against the bound head SHA.
- Wait for pending required checks rather than passing early.
- Treat failed required checks as an implementation failure unless evidence proves an external infrastructure blocker.
- Never infer that no observed checks means no required checks.
- Require `required_checks_known: true` from the bound transport read before PASS. Repository-owner confirmation may help repair repository-rule discovery, but it cannot substitute for this machine-verifiable merge prerequisite; remain BLOCKED while the transport reports false.
- Never call `request_user_input` in Closeout. For visual, business, real-device, external-system, or other human-only acceptance, accept only an already persisted explicit confirmation URL and digest bound to the exact acceptance snapshot.
- Return blocked when necessary evidence or a snapshot-bound human confirmation cannot be obtained. The `delivery` invocation is not blanket acceptance.

Do not modify code or tests in response to a failure.

## Re-read before the verdict

Immediately before recording a verdict, independently fetch the Issue, PR, refs, Body, comments, and checks again.

- Restart affected acceptance when head SHA or base SHA changes.
- Return return-to-definition for a binding Issue contract change.
- Re-evaluate a non-binding or editorial Issue change before rebinding.
- Recheck factual claims and evidence when the PR title or Body changes.
- Rerun only the tests affected by a Body-only correction when head/base remain unchanged.
- Stop on any unexplained target, ref, Draft state, or protected-field change.

Never publish a verdict for a stale tuple.

## Record an append-only acceptance verdict

Create one complete top-level PR comment for the exact snapshot. Never overwrite a prior round. Compose the exact **Acceptance verdict** artifact from `references/delivery-evidence-contract.md`; that shared contract is the only authority for its fields, values, tuple bindings, and success semantics.

Use the loaded Pull Request transport protocol to add the exact comment and independently read it back. Bind its comment ID, URL, and Markdown digest. Treat only verified or no-op as a recorded verdict.

## Handle failed or blocked acceptance

For an implementation, test, behavior, or evidence defect:

1. Record FAIL with exact blockers and return_stage Implementation.
2. Keep the PR Draft or use authorized transport to convert it back to Draft.
3. Return return-to-implementation with the Issue URL, Draft PR URL, acceptance comment URL, and `role: implementation`.
4. When delegated, let the coordinator re-read the FAIL and start a fresh repair Implementation Agent automatically. A standalone caller receives the same persistent hand-off.

For a delivery-contract defect:

1. Record FAIL with the exact unsupported decision or acceptance gap and return_stage Definition.
2. Keep the PR Draft.
3. Return return-to-definition and require a new `project-harness` invocation with `role: definition` for the same Issue.

For an external, permission, environment, required-check-discovery, or human-confirmation blocker:

1. Record BLOCKED when GitHub writing remains available.
2. Preserve the Draft PR.
3. Return blocked with the recovery condition.

Do not impose an arbitrary retry limit. Every repaired head SHA enters a new fresh Closeout Agent and receives a new append-only record.

## Complete successful acceptance

After a verified PASS comment whose payload has `required_checks_known: true`:

1. Bind the verified PASS comment URL and normalized Markdown digest, then re-read the bound snapshot once more.
2. Compose the exact **Product acceptance Issue callback** from `references/delivery-evidence-contract.md`, then use the loaded Issue transport protocol to append and independently read it back without copying the full report.

3. Bind the Issue callback URL and normalized Markdown digest.
4. Re-read the PR, refs, PASS comment, and Issue callback again.
5. Compose and add one top-level PR comment using the exact **Current eligibility registration** marker and payload from `references/delivery-evidence-contract.md`.

6. Independently read the registration comment back and bind its URL and digest.
7. Stop blocked on an ambiguous registration chain or incompatible in-progress/terminal Context Promotion callback for the same source head. Permit one same-head active schema-v2 predecessor only through the exact successor rule below, and one unversioned legacy predecessor only through the exact legacy migration.
8. Use the loaded Pull Request transport protocol to mark the exact Draft PR Ready.
9. Independently verify Ready state, unchanged title/Body digests, unchanged refs, the PASS comment, and the registration comment.

Fail closed on a partial or ambiguous mutation. Report the exact persisted state and return blocked instead of claiming accepted-ready-pr.

When an exact valid PASS record, Issue callback, Context Promotion registration, and Ready state already exist for the unchanged tuple and every stored comment digest matches, return accepted-ready-pr through verified no-op reads. When only a prefix of these successful steps exists, re-read its exact tuple/digests and complete the remaining steps idempotently; never restart acceptance solely because a later callback or Ready mutation was interrupted.

For an unmerged PR whose active schema-v2 registration is stale while the source head is unchanged, do not overwrite it or reuse its PASS. If the PR is Ready, convert it to Draft and verify that state. Run complete fresh Closeout against the current title/Body/head/base/check tuple, persist a new PASS and Issue callback, then append one schema-v2 registration with `previous_registration_url` / `previous_registration_sha256` bound to the exact active predecessor and both legacy alias fields null. Leave the old registration unchanged. Require one linear chain and define only its non-superseded tip as active before marking the newly accepted tuple Ready.

For an unmerged PR with exactly one historical unversioned eligibility registration matching the shared evidence contract's **Legacy eligibility registration**, do not treat the old lineage as current acceptance. Read and digest the old registration, PASS, and Issue callback. If the PR is Ready, convert it to Draft and verify that state. Run a complete fresh Closeout against the current title/Body/head/base/check tuple, persist a new PASS and Issue callback, and create the schema-v2 registration with both `previous_registration_*` and `supersedes_legacy_registration_*` pairs set to that exact predecessor. Require the two pairs to be equal. Allow only this one-to-one pair, leave the old comment unchanged, then mark the newly accepted tuple Ready. Any missing old source, multiple predecessor/successor, or current acceptance failure remains fail closed.

Closeout never merges. A later title, commit, PR Body, or base change invalidates the acceptance and requires a fresh Closeout. If the stale accepted PR is Ready, use the authorized transport to convert the exact PR to Draft and verify that state before recording a new verdict or returning to Implementation/Definition. Under `delivery`, return only an unchanged accepted tuple to the coordinator's product merge gate; do not hand off to an external Reviewer on the normal automated path.

## Return a closed result

~~~yaml
outcome: accepted-ready-pr | return-to-implementation | return-to-definition | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
pr_url: https://github.com/owner/repo/pull/456
pr_title: null
pr_body_sha256: null
head_ref: null
head_sha: null
base_ref: null
base_sha: null
acceptance_comment_url: null
acceptance_comment_sha256: null
issue_callback_url: null
issue_callback_sha256: null
eligibility_registration_url: null
eligibility_registration_sha256: null
promotion_registration_url: null
promotion_registration_sha256: null
ready_state_verified: false
reason: null
recovery_condition: null
handoff:
  role: delivery | external-review | implementation | definition | closeout
  recipient: delivery-coordinator | user
  authoritative_sources: []
  evidence_urls: []
  next_action: null
~~~

`promotion_registration_url` and `promotion_registration_sha256` are retained deprecated aliases for the compatibility result envelope and must equal the corresponding `eligibility_registration_*` fields whenever populated. New hand-offs and consumers use `eligibility_registration_url` / `eligibility_registration_sha256`.

For delegated accepted-ready-pr, set `recipient: delivery-coordinator`, `role: delivery`, and hand off the Issue URL, Ready PR URL, acceptance comment URL, Issue callback URL, eligibility registration URL, and bound tuple. The coordinator must re-read all of them before the product merge gate.

For standalone accepted-ready-pr, recommend `role: delivery` with those persistent URLs so the coordinator resumes at the product merge gate. Preserve `external-review` only for a caller intentionally using the legacy phase path.

For a return, include only the Issue URL, Draft PR URL, acceptance comment URL, role, evidence URLs, and next action. Never copy the report or preceding chat into the hand-off.
