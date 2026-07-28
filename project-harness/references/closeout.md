# Closeout

Execute this phase only after `project-harness` dispatches `role: closeout`.

Carry the Closeout phase as an independent acceptance authority. Complete final acceptance for one exact Issue and Pull Request snapshot without becoming a second Implementation Agent.

## Contents

- Enforce the authority boundary
- Accept only the minimal hand-off
- Resolve and bind the acceptance snapshot
- Build the acceptance matrix
- Verify independently
- Re-read before the verdict
- Record an append-only acceptance verdict
- Handle failed or blocked acceptance
- Complete successful acceptance
- Return a closed result

## Enforce the authority boundary

- Start only from an explicit Closeout invocation containing one Issue URL and one Draft PR URL.
- Use a clean session.
- Treat the Issue as the delivery contract and the PR as the implementation result and evidence carrier.
- Independently inspect the diff and rerun applicable acceptance.
- Treat a current user's explicit `$project-harness` invocation with `role: closeout` as authority only for the top-level acceptance/promotion-registration comments, lightweight Issue callback, and Draft/Ready mutations enumerated here.
- Write only those authorized GitHub artifacts; never derive write authority from an automatic route, hand-off, ordinary review request, or prior session.
- Never modify product code, tests, commits, refs, PR Body, Issue Body, or durable project memory.
- Never make even a small implementation fix.
- Never merge, close the Issue, redesign requirements, or convert missing evidence into a PASS.

Return accepted-ready-pr, return-to-implementation, return-to-definition, or blocked.

## Accept only the minimal hand-off

Require:

~~~yaml
role: closeout
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  - https://github.com/owner/repo/pull/456
next_action: Independently accept or reject the Draft PR against the Issue.
~~~

Read both sources completely. Do not rely on the previous session's summary, chat, local plan, or implicit memory.

## Resolve and bind the acceptance snapshot

Follow the loaded Issue and Pull Request transport protocols to prove:

- exact repository and Issue/PR identity;
- open Issue state;
- open PR state and relationship to the Issue;
- Draft state, unless resuming an already recorded exact acceptance;
- Issue Body digest;
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
pr_body_sha256: SHA256
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
- Run every reproducible build, test, static check, smoke test, or acceptance command needed by the Issue and risk.
- Treat Implementation's validation as evidence to confirm, not as a substitute for execution.
- Record exact commands, results, and relevant environment facts.
- Verify every required CI/check against the bound head SHA.
- Wait for pending required checks rather than passing early.
- Treat failed required checks as an implementation failure unless evidence proves an external infrastructure blocker.
- Never infer that no observed checks means no required checks.
- Require repository-rule evidence or explicit repository-owner confirmation when required-check discovery is unavailable.
- Obtain explicit human confirmation for visual, business, real-device, external-system, or other human-only acceptance.
- Bind every human confirmation to the exact acceptance snapshot.
- Return blocked when necessary evidence or confirmation cannot be obtained.

Do not modify code or tests in response to a failure.

## Re-read before the verdict

Immediately before recording a verdict, independently fetch the Issue, PR, refs, Body, comments, and checks again.

- Restart affected acceptance when head SHA or base SHA changes.
- Return return-to-definition for a binding Issue contract change.
- Re-evaluate a non-binding or editorial Issue change before rebinding.
- Recheck factual claims and evidence when PR Body changes.
- Rerun only the tests affected by a Body-only correction when head/base remain unchanged.
- Stop on any unexplained target, ref, Draft state, or protected-field change.

Never publish a verdict for a stale tuple.

## Record an append-only acceptance verdict

Create one complete top-level PR comment for the exact snapshot. Never overwrite a prior round.

Include at least:

~~~yaml
verdict: PASS | FAIL | BLOCKED
issue_url: URL
issue_body_sha256: SHA256
pr_url: URL
pr_body_sha256: SHA256
head_sha: COMMIT
base_ref: develop
base_sha: COMMIT
acceptance:
  - item: CONTRACT ITEM
    result: PASS | FAIL | BLOCKED | NOT_APPLICABLE
    evidence: COMMAND, OUTPUT, OR SOURCE
required_ci: []
required_checks_known: true | false
not_reexecuted: []
human_confirmations: []
return_stage: null | Implementation | Definition
blockers: []
~~~

Use the loaded Pull Request transport protocol to add the exact comment and independently read it back. Bind its comment ID, URL, and Markdown digest. Treat only verified or no-op as a recorded verdict.

## Handle failed or blocked acceptance

For an implementation, test, behavior, or evidence defect:

1. Record FAIL with exact blockers and return_stage Implementation.
2. Keep the PR Draft or use authorized transport to convert it back to Draft.
3. Return return-to-implementation with the Issue URL, Draft PR URL, acceptance comment URL, and a new `project-harness` hand-off with `role: implementation`.

For a delivery-contract defect:

1. Record FAIL with the exact unsupported decision or acceptance gap and return_stage Definition.
2. Keep the PR Draft.
3. Return return-to-definition and require a new `project-harness` invocation with `role: definition` for the same Issue.

For an external, permission, environment, required-check-discovery, or human-confirmation blocker:

1. Record BLOCKED when GitHub writing remains available.
2. Preserve the Draft PR.
3. Return blocked with the recovery condition.

Do not impose an arbitrary retry limit. Every repaired head SHA enters a new clean Closeout session and receives a new append-only record.

## Complete successful acceptance

After a verified PASS comment:

1. Re-read the bound snapshot once more.
2. Use the loaded Issue transport protocol to append a lightweight Issue callback containing the PR URL, head/base tuple, and PASS comment URL without copying the full report.
3. Independently read the Issue callback back.
4. Re-read the PR and refs again.
5. Add one top-level PR registration comment using this deterministic marker and payload:

~~~text
<!-- ${marker_namespace}:context-promotion-eligible source-pr=456 source-head=COMMIT -->
state: awaiting-merge
issue_url: URL
issue_body_sha256: SHA256
pr_body_sha256: SHA256
base_ref: develop
base_sha: COMMIT
acceptance_comment_url: URL
~~~

6. Independently read the registration comment back and bind its URL and digest.
7. Stop blocked on an existing conflicting registration or terminal Context Promotion callback for the same source head.
8. Use the loaded Pull Request transport protocol to mark the exact Draft PR Ready.
9. Independently verify Ready state, unchanged title/Body digests, unchanged refs, the PASS comment, and the registration comment.

Fail closed on a partial or ambiguous mutation. Report the exact persisted state and return blocked instead of claiming accepted-ready-pr.

When an exact valid PASS record, Issue callback, Context Promotion registration, and Ready state already exist for the unchanged tuple, return accepted-ready-pr through verified no-op reads.

Closeout never merges. A later commit or relevant PR Body/base change invalidates the acceptance and requires a new Closeout.

## Return a closed result

~~~yaml
outcome: accepted-ready-pr | return-to-implementation | return-to-definition | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
pr_url: https://github.com/owner/repo/pull/456
pr_body_sha256: null
head_sha: null
base_ref: null
base_sha: null
acceptance_comment_url: null
issue_callback_url: null
promotion_registration_url: null
ready_state_verified: false
reason: null
recovery_condition: null
handoff:
  role: external-review | implementation | definition | closeout
  authoritative_sources: []
  next_action: null
~~~

For accepted-ready-pr, hand off only the Ready PR URL to final human or repository review.

For a return, include only the Issue URL, Draft PR URL, acceptance comment URL, role, and next action. Never copy the report or preceding chat into the hand-off.
