# Closeout

Execute this phase only after `project-harness` dispatches a standalone `role: closeout` or the current `delivery` coordinator delegates the Closeout phase under the root Skill's scoped envelope. Run the selected role as the Closeout Phase Owner; the exact public and delegated role name remains `closeout`.

Carry the Closeout phase as an independent acceptance authority. Complete final acceptance for one exact Issue and Pull Request snapshot without becoming a second Implementation Phase Owner.

## Contents

- Enforce the authority boundary
- Accept the public semantic input
- Resolve and bind the acceptance snapshot
- Enforce the final change scope
- Build the acceptance matrix
- Judge independently and verify proportionally
- Re-read before the verdict
- Record an append-only acceptance verdict
- Handle failed or blocked acceptance
- Complete successful acceptance
- Return a closed result

## Enforce the authority boundary

- Start only from one Issue URL and one Draft PR URL supplied by either a current explicit Closeout invocation or a host-provenance-bound delegation from the current explicit `delivery` invocation.
- Use a fresh isolated Phase Owner context with no Implementation conversation history.
- Apply the root Skill's fixed two-hop delegation topology. The Closeout Phase Owner may directly delegate narrow read-only verification and, when useful, one independent tuple-bound review; every Worker and Reviewer must remain mutation-free, must not delegate further, and must return only to this Owner.
- Keep the Closeout Phase Owner as the sole phase writer and sole producer of the acceptance verdict, Issue callback, eligibility registration, Ready-state mutation, and phase hand-off.
- Continue acceptance for the same bound snapshot in the same Phase Owner after a Worker failure or Reviewer FAIL. Replace the Owner only when a bound authoritative input or semantic target changes, the Owner explicitly terminates, or its context cannot be recovered.
- Treat the Issue as the delivery contract and the PR as the implementation result and evidence carrier.
- Independently inspect the diff and judge every acceptance item. Reuse trustworthy Implementation or CI evidence bound to the current head; rerun only missing, stale, ambiguous, failed-to-reproduce, or risk-sensitive items.
- Treat the current user message's exact host-valid `role: closeout` invocation and required semantic inputs under the root Skill's public-invocation adapter as authority only for the top-level acceptance/promotion-registration comments, lightweight Issue callback, and Draft/Ready mutations enumerated here. Under `delivery`, accept only the same mutations when the delegation envelope enumerates them and binds the current persistent sources.
- Write only those authorized GitHub artifacts; never derive write authority from host/model loading or automatic routing by itself, a serialized envelope, ordinary hand-off, ordinary review request, or prior run.
- Never modify product code, tests, commits, refs, PR Body, Issue Body, or durable project memory.
- Never make even a small implementation fix.
- Never merge, close the Issue, redesign requirements, or convert missing evidence into a PASS.

Return accepted-ready-pr, return-to-implementation, return-to-definition, or blocked.

## Accept the public semantic input

Apply the root Skill's public-invocation adapter. For a standalone entry, require an exact `role: closeout`, one Issue URL and one Draft product PR URL in the current user message. Treat those URLs as semantic sources whether they appear in prose or an optional structured carrier; do not require the caller to reproduce Implementation's hand-off envelope.

When delegated by `delivery`, also require the root Skill's compact schema-v3 envelope with `delegated_role: closeout`, the Implementation phase's persistent evidence URLs, typed evidence-comment URL/digest pairs, bound tuple, allowed mutations, and `next_action`. Do not require an Evidence Bundle, component identity map, or raw source payload. Dual-read a historical schema-v2 envelope with its Bundle and a schema-v1 envelope only through the root Skill's compatibility rules and complete fresh-read fallback; never emit or silently upgrade either legacy form.

Read both sources and every supplied evidence URL completely. Do not rely on the previous Phase Owner's summary, chat, local plan, or implicit memory.

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

## Enforce the final change scope

Independently read the exact compact `### 改动范围` subsection inside the Issue's binding `非目标与边界` section and compare it with the complete final product diff, not a file summary or the Implementation hand-off. For a current-format Issue, require one non-empty `普通业务改动` field and one non-empty `受保护改动` field in that subsection.

- For a new or open/unmerged lineage, require the compact scope to be present, unambiguous, and applicable. A historical open Issue or unmerged PR without it returns to Definition; Closeout must not retrofit the Issue or accept the missing contract from another source.
- Judge ordinary business changes against the Issue description and its `普通业务改动` field. Localized implementation and test changes may satisfy that ordinary scope, but neither source implicitly authorizes a protected surface.
- Apply the protected surfaces defined by the shared Issue contract. Require `受保护改动` to name every changed protected surface and state both the exact allowed change and its compatibility or migration boundary. The exact declaration `受保护改动：无` requires the final diff to contain no protected-surface change.
- Do not accept `实施计划`, the PR Body, an ADR or other durable source, repository convention, chat, or Implementation's explanation as additional mutation authority. Use them only as evidence about work already authorized by the Issue.
- When an out-of-scope edit is unnecessary and can be removed while still satisfying the existing contract, record the failure through the existing Acceptance verdict and return to Implementation with the exact offending area to remove. When completing the task genuinely requires broader ordinary scope or an unlisted protected change, or the authorization remains ambiguous, record the existing failure and return to Definition.
- For an exact already-merged recovery lineage, keep reconciliation read-only. Apply its existing legacy checks without requiring or writing a compact scope back into the Issue.

Do not add a scope-specific acceptance item, per-surface mapping table, callback, marker, schema field, or artifact. Express any scope failure only through the existing verdict, blocker, return-stage, reason, and evidence fields.

## Build the acceptance matrix

Extract each binding goal, boundary, confirmed decision, and acceptance check from the Issue. Treat the Issue implementation plan as non-binding.

Map every item to:

- executable verification;
- code/diff inspection;
- current-head Implementation or CI evidence eligible for reuse after source and relevance confirmation;
- required CI;
- human-only confirmation;
- not applicable with an explicit reason.

Do not add new delivery requirements during Closeout. Return return-to-definition when the existing contract cannot support a valid acceptance decision.

Also map the PR's `持久项目记忆实际影响` claims to the diff, tests, cited ADR/rule/wiki/memory sources, and repository state. Require exactly one factual row for each of `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`. Treat the exact literal `无` as the only no-impact value; require its evidence cell to be non-empty and non-placeholder. Treat `none`, `no_write`, `N/A`, a blank value, a missing row, vague language, single-task records claimed as durable knowledge, unsupported promotion promises, or omitted material effects as PR evidence defects.

Set the conservative promotion classification from this matrix:

- Set `promotion_required: false` only when all five actual-impact values are exactly `无` and independent diff/source inspection confirms every claim.
- Set `promotion_required: true` when any category has a concrete non-`无` impact, or when any row is missing, ambiguous, unsupported, or otherwise cannot be verified. A true value reports that the code-only fast path is unavailable; it does not convert defective evidence into acceptance.
- Set `code_only_verified: true` only for a final PASS whose five rows satisfy the verified all-`无` rule. Set it to false for every other PASS, FAIL, BLOCKED, or incomplete result.

## Judge independently and verify proportionally

- Inspect the complete diff and affected tests.
- Delegate bounded read-only verification only to direct Workers when separate context materially helps. Give each Worker an exact read set or acceptance-matrix slice and require evidence-bound results. Keep the Closeout Phase Owner accountable for the complete matrix and verdict; no Worker or Reviewer may edit code, write the verdict, mutate GitHub, delegate further, merge, close the Issue, or approve promotion.
- Reuse a validation result only when the PR, Implementation hand-off, commit status, or CI run identifies the exact command/check, successful result, final head SHA, and relevant environment; independently read that source and confirm that the check still covers the corresponding acceptance item and changed boundary.
- Do not rerun a current-head check merely to demonstrate phase independence. The Closeout Phase Owner's independence comes from its own source inspection, evidence-admissibility decision, acceptance mapping, and verdict.
- Rerun the narrow applicable command when evidence is missing, stale, ambiguous, tied to another head, or insufficient for the changed boundary. Also rerun risk-sensitive acceptance when failures would affect security, privacy, destructive data or migration behavior, external compatibility/protocols, difficult-to-reverse architecture, or a broad operational blast radius.
- Add broader builds, integration tests, static checks, smoke tests, or acceptance commands only when the Issue, changed boundary, repository rules, or risk requires them. Record exact commands, results, reused evidence sources, and relevant environment facts.
- Verify every required CI/check against the bound head SHA.
- Wait for pending required checks rather than passing early.
- Treat failed required checks as an implementation failure unless evidence proves an external infrastructure blocker.
- Never infer that no observed checks means no required checks.
- Require `required_checks_known: true` from the bound transport read before PASS. Repository-owner confirmation may help repair repository-rule discovery, but it cannot substitute for this machine-verifiable merge prerequisite; remain BLOCKED while the transport reports false.
- Never open the user decision gate in Closeout. For visual, business, real-device, external-system, or other human-only acceptance, accept only an already persisted explicit confirmation URL and digest bound to the exact acceptance snapshot.
- Return blocked when necessary evidence or a snapshot-bound human confirmation cannot be obtained. The `delivery` invocation is not blanket acceptance.

Do not modify code or tests in response to a failure.

## Re-read before the verdict

Immediately before recording a verdict, independently fetch the Issue, PR, refs, Body, comments, and checks again.

- Restart affected acceptance when head SHA or base SHA changes.
- Re-read the complete final diff and exact `### 改动范围`; rerun the scope judgment when either changes, and never publish a verdict for a diff that has not passed that judgment.
- Return return-to-definition for a binding Issue contract change.
- Re-evaluate a non-binding or editorial Issue change before rebinding.
- Recheck factual claims and evidence when the PR title or Body changes.
- Rerun only the tests affected by a Body-only correction when head/base remain unchanged.
- Stop on any unexplained target, ref, Draft state, or protected-field change.

Never publish a verdict for a stale tuple.

## Record an append-only acceptance verdict

Create one complete top-level PR comment for the exact snapshot. Never overwrite a prior round. Compose the exact **Acceptance verdict** artifact from `references/delivery-evidence-contract.md`; that shared contract is the only authority for its fields, values, tuple bindings, and success semantics.

For a verified all-five-`无` PASS, include this acceptance entry exactly once:

~~~yaml
  - item: durable-memory-impact
    result: PASS
    evidence: all-five-none
~~~

Do not emit `all-five-none` when any category is non-`无`, missing, ambiguous, unsupported, or contradicted by the diff. For a valid concrete durable-memory impact, record the checked category and evidence normally and keep `promotion_required: true` in the phase result.

Use the loaded Pull Request transport protocol to add the exact comment and independently read it back. Bind its comment ID, URL, and Markdown digest. Treat only verified or no-op as a recorded verdict.

## Handle failed or blocked acceptance

For an implementation, test, behavior, or evidence defect:

1. Record FAIL with exact blockers and return_stage Implementation.
2. Keep the PR Draft or use authorized transport to convert it back to Draft.
3. Return return-to-implementation with the Issue URL, Draft PR URL, acceptance comment URL, and `role: implementation`.
4. When delegated, let the coordinator re-read the FAIL and start a fresh repair Implementation Phase Owner automatically. A standalone caller receives the same persistent hand-off.

For a delivery-contract defect:

1. Record FAIL with the exact unsupported decision or acceptance gap and return_stage Definition.
2. Keep the PR Draft.
3. Return return-to-definition and require a new `project-harness` invocation with `role: definition` for the same Issue.

For an external, permission, environment, required-check-discovery, or human-confirmation blocker:

1. Record BLOCKED when GitHub writing remains available.
2. Preserve the Draft PR.
3. Return blocked with the recovery condition.

Do not impose an arbitrary retry limit. Every repaired head SHA changes the bound input, enters a new fresh Closeout Phase Owner, and receives a new append-only record. A failed Worker or Reviewer against the unchanged snapshot does not by itself justify replacing the current Owner.

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
code_only_verified: false
promotion_required: true
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

Always populate `code_only_verified` and `promotion_required` according to the five-category rule above. The coordinator may use the fast path only after independently re-reading the PASS comment and finding the exact `durable-memory-impact` / `PASS` / `all-five-none` entry on the unchanged accepted tuple; the ephemeral result fields alone never authorize skipping Context Promotion.

For standalone accepted-ready-pr, recommend `role: delivery` with those persistent URLs so the coordinator resumes at the product merge gate. Preserve `external-review` only for a caller intentionally using the legacy phase path.

For a return, include only the Issue URL, Draft PR URL, acceptance comment URL, role, evidence URLs, and next action. Never copy the report or preceding chat into the hand-off.
