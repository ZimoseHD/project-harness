# Context Authoring

Execute this phase only after `project-harness` dispatches `role: context-authoring` from a current user's explicit invocation.

Carry the optional pre-implementation durable-decision gate. Persist only one settled cross-task architecture or technology decision that another task must consume before the source product Pull Request can merge.

## Contents

- Enforce the gate boundary
- Accept only the minimal hand-off
- Verify the source and gate
- Resolve authority and idempotency
- Create the smallest proposed ADR change
- Require an independent Reviewer
- Mark the reviewed decision PR Ready
- Return a closed result

## Enforce the gate boundary

- Start only from an explicit invocation containing one finalized open Issue URL.
- Use a clean session and treat the Issue as the decision source and delivery contract.
- Treat the current exact role invocation as authority for the branch, commit, push, Draft PR, comments, and Ready-state mutations enumerated here. A prior hand-off or implicit route is not authority.
- Write only one `docs/decisions/ADR-*.md` leaf on a dedicated branch based on `develop`.
- Mark every pre-implementation decision `status: proposed`.
- Produce a verified existing-decision result, a verified Ready proposed-decision PR, return-to-definition, or blocked.
- Never write active rules, wiki explanations, `.project-memory` state, product code, tests, or task-local tracking.
- Never replace verified current behavior with unverified future behavior without preserving their distinct applicability.
- Never modify the Issue Body, commit to `develop` or `main` directly, merge a PR, or start product implementation.

## Accept only the minimal hand-off

Require:

~~~yaml
role: context-authoring
authoritative_sources:
  - https://github.com/owner/repo/issues/123
next_action: Publish the required proposed decision before Implementation.
~~~

Reject chat summaries as decision authority.

## Verify the source and gate

1. Follow the loaded Issue transport protocol to read the exact open Issue, comments, identity, state, and normalized Body digest.
2. Establish the exact authoritative evidence cited by the Issue and required to validate the decision gate. Stop when required evidence or repository authority cannot be established.
3. Extract `持久项目记忆影响` and require `实现前 Context Authoring` to be `required`.
4. Verify all four conditions from the Issue:
   - the settled conclusion belongs to architecture, a domain model, a protocol/interface contract, a system boundary, or a project-level technology choice;
   - it applies beyond the source Issue;
   - another task must consume it before the source product PR merges;
   - omission creates concrete divergence, rework, correctness, safety, or compatibility risk.
5. Confirm the write classification is `decision` and the authoritative destination is `docs/decisions/`. Return return-to-definition when the gate is incomplete, contradictory, unresolved, unsupported, or classified into another layer. Do not repair the contract in this role.

Treat `proposed` as selected but not implementation-validated. Do not publish unresolved alternatives as a proposed decision.

## Resolve authority and idempotency

Compare the decision with the matching authoritative ADRs needed to select a new identifier, detect an existing decision, or verify one authoritative destination. Stop on unresolved identity, conflict, or destination ambiguity.

Use this deterministic Issue callback marker:

~~~text
<!-- ${marker_namespace}:context-authoring issue=123 issue-body=SHA256 -->
~~~

- Return `verified-existing-decision` when a merged ADR already contains the same source-bound proposed or accepted decision without conflict.
- Return the existing decision PR state when an unambiguous callback and PR exist for the unchanged Issue Body.
- Append a merged-status callback when a repeated invocation finds the decision PR merged and the source callback lacks that state.
- Stop blocked on multiple candidates, contradictory callbacks, identifier/destination ambiguity, or an overlapping unmerged decision change.

## Create the smallest proposed ADR change

1. Synchronize the `develop` integration base and bind its SHA.
2. Create or resume one dedicated decision branch associated with the source Issue.
3. Preserve unrelated worktree changes.
4. Add or update the smallest single-topic ADR under `docs/decisions/`.
5. Put the decision first, followed by applicability, rationale, rejected alternatives, consequences, evidence, source links, and related or superseded authority.
6. Keep the diff limited to `docs/decisions/` and keep technical facts in code/contracts/tests rather than duplicating them.
7. Validate frontmatter, `status: proposed`, links, terminology, authority, and single-source-of-truth behavior.
8. Commit and push the exact decision-only change; omit `Co-Authored-By`.
9. Create or update one Draft decision PR through the loaded Pull Request transport protocol, explicitly targeting `develop`.

Include in the decision PR Body:

- source Issue URL and Body digest;
- the exact settled decision and four-condition gate evidence;
- destination and authority rationale;
- confirmation that the decision remains proposed until implementation evidence supports promotion;
- validation commands and results;
- confirmation that no active rule, wiki explanation, project-memory state, product code, tests, or task tracking is included.

Do not use a closing keyword for the still-open product Issue.

## Require an independent Reviewer

Bind the Draft decision PR Body digest, head SHA, base ref `develop`, and base SHA after independent read-back. Start a new clean, read-only Reviewer for each review round and provide only the source Issue tuple, exact gate evidence, decision PR tuple and diff, and matching existing ADRs.

Require `PASS` or blocking `FAIL` for the exact tuple. Check:

1. traceability to one finalized Issue and unchanged Body digest;
2. satisfaction of all four pre-implementation gate conditions;
3. a settled architecture or technology decision rather than feature design or implementation planning;
4. correct `proposed` status and no claim of implemented behavior;
5. correct ADR placement and lifecycle metadata;
6. one authoritative destination without duplication or conflict;
7. a decision-only diff limited to `docs/decisions/` and executable validation.

Forbid edits, GitHub mutations, alternative designs, and non-blocking wording suggestions in the Reviewer. Require the verdict to remain bound to the supplied tuple and cited authoritative evidence. Fix blockers in the Authoring Agent, bind the new tuple, and start a new clean Reviewer.

## Mark the reviewed decision PR Ready

After PASS:

1. Add and independently verify an append-only PASS comment identifying the exact reviewed tuple.
2. Re-read the decision PR, refs, Body digest, and diff; stop if the tuple changed.
3. Use the loaded Pull Request transport protocol to mark the exact Draft PR Ready.
4. Independently verify Ready state and every bound field.
5. Add an Issue callback with the deterministic marker, outcome `decision-pr-ready`, PR URL, and bound head/base identity.
6. Independently read the Issue callback back.

Fail closed on partial or ambiguous mutations. Do not merge the decision PR.

## Return a closed result

~~~yaml
outcome: verified-existing-decision | verified-decision-pr | return-to-definition | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
issue_callback_url: null
decision_pr_url: null
decision_pr_body_sha256: null
decision_head_sha: null
ready_state_verified: false
decision_pr_merged: false
decision_sources: []
reason: null
recovery_condition: null
handoff:
  role: external-review | implementation | definition | context-authoring
  authoritative_sources: []
  next_action: null
~~~

For `verified-existing-decision`, hand off the Issue URL and exact merged ADR to a new `project-harness` session with `role: implementation`.

For `verified-decision-pr`, hand off only the Ready decision PR URL to external human or repository review. Start `role: implementation` only after a later explicit invocation independently verifies that PR merged into `develop`.

For return-to-definition, identify the exact gate or contract defect and require a new `project-harness` invocation with `role: definition` for the same Issue.

For blocked, preserve any Draft decision PR and report its exact state and recovery condition without claiming the gate completed.
