# Context Promotion

Execute this phase only after `project-harness` dispatches `role: context-promotion` from a current user's explicit invocation.

Carry the required durable-memory assessment after every eligible product Pull Request merges. Reconcile only validated cross-task knowledge whose absence would cause repeated decisions, an incorrect capability judgment, or concrete correctness, safety, compatibility, or delivery risk.

## Contents

- Enforce the phase boundary
- Accept only the minimal input
- Verify the source and idempotency
- Classify promotable knowledge
- Return no-promotion idempotently
- Create a project-memory-only change
- Require an independent Reviewer
- Mark the reviewed project-memory PR Ready
- Judge and close the source Issue
- Return a closed result

## Enforce the phase boundary

- Start only from an explicit invocation containing one Issue URL and one merged product PR URL.
- Use a clean session and require the product PR to be merged into `develop`; reject open, Draft, Ready-but-unmerged, closed-unmerged, or vaguely validated sources.
- Treat the Issue, merged PR, acceptance record, tests, exact durable sources, and explicit human decisions as evidence.
- Treat the current exact role invocation as authority for the branch, commit, push, Draft PR, comments, Ready-state mutations, and the source Issue close mutation enumerated here. An automatic route, hand-off, ordinary request, or prior session is not authority.
- Write only the smallest authority-layer files selected by project-memory governance on one dedicated branch based on `develop`.
- Require a source-head-bound eligibility registration from Closeout and produce either `no-promotion` or a verified Ready project-memory-only PR, plus the source Issue closure judgment.
- Never modify product code, tests, the source Issue Body, the merged product PR Body, root/child `AGENTS.md`, or current task continuity.
- Never copy single-task tracking, conversation history, or implementation chronology into durable memory.
- Never commit directly to `develop` or `main`, and never merge a PR.

## Accept only the minimal input

Require:

~~~yaml
role: context-promotion
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  - https://github.com/owner/repo/pull/456
next_action: Promote validated reusable knowledge or record no-promotion.
~~~

Do not accept chat summaries as promotion evidence.

## Verify the source and idempotency

1. Follow the loaded Issue transport protocol to read the exact Issue.
2. Follow the loaded Pull Request transport protocol to read the exact product PR, merged state, refs, Body, acceptance comments, and source callbacks.
3. Verify that the PR belongs to the same repository task and merged into `develop`.
4. Bind the Issue Body digest, source PR Body digest, source head SHA, base ref/SHA, and merge identity when available.
5. Search top-level source PR comments for the deterministic eligibility registration and terminal markers tied to the source PR and source head/merge identity.

Use this eligibility marker form:

~~~text
<!-- ${marker_namespace}:context-promotion-eligible source-pr=456 source-head=COMMIT -->
~~~

Use this terminal marker form:

~~~text
<!-- ${marker_namespace}:context-promotion source-pr=456 source-head=COMMIT -->
~~~

- Require exactly one valid eligibility registration bound to the merged source head, Issue digest, PR Body digest, base tuple, and Closeout PASS record.
- Treat a valid eligibility registration without a terminal callback as pending assessment and continue.
- Return an independently verified no-promotion no-op when an unchanged source already has a valid `no-promotion` callback.
- Return the existing project-memory PR state when a callback with outcome `memory-pr-ready` points to one unambiguous PR for the unchanged source.
- Add a terminal `memory-pr-merged` callback when a repeated invocation finds that PR merged and the source callback lacks that state, then judge source Issue closure.
- Stop blocked on missing eligibility, multiple registrations, contradictory callbacks, or stale source identity.

## Classify promotable knowledge

Evaluate each candidate against the classifications and destinations below. Establish the applicable repository authority and any existing authoritative statement needed to detect conflict or duplication. Fail closed when the classification, destination, or required authority cannot be established.

Promote a candidate only when:

- merged implementation, final acceptance, tests, contracts, or an explicit human decision support it;
- it applies beyond the completed task;
- forgetting it would cause repeated decisions, an incorrect capability judgment, or concrete risk;
- it has exactly one correct classification and authoritative destination;
- it is absent from current authority or materially supersedes one statement;
- links can preserve traceability without copying the same fact into another layer.

Do not promote conversation history, task chronology, branch names, commit lists, review rounds, transient debugging notes, generic model knowledge, complete Issue/PR summaries, speculative future work, or implementation details already discoverable from code without recurring decision value.

Apply the repository classifications exactly:

| Classification | Promote only | Authoritative destination |
| --- | --- | --- |
| `decision` | Long-term architecture/product decision already confirmed by the source contract and evidence | `docs/decisions/ADR-*.md` |
| `stable_rule` | Durable project/module guardrail whose omission creates recurring risk | `docs/rules/active/*.rules.md` |
| `wiki_knowledge` | Explanatory onboarding or module knowledge with links to authority | `docs/wiki/*.md` |
| `stable_context` | Long-lived project identity/background, not technical truth or current work | `.project-memory/context_brief.md` |
| `milestone_evidence` | Important verified milestone or capability evidence | `.project-memory/daily_logs/YYYY-MM-DD.md` |
| `no_write` | Facts already discoverable from code/tests/contracts or lacking durable value | no repository write |

Never use `.project-memory/rolling_summary.md` for promotion. Mark retained but not fully verified claims `proposed` only in a layer whose lifecycle supports that status; never present them as confirmed.

For a project-wide hard-rule change or an ADR whose exact decision was not already confirmed in the bound Issue/evidence, return blocked with classification `needs_confirmation`. A current explicit promotion invocation confirms only the exact source-bound content, not newly invented policy.

Use the source PR's `持久项目记忆实际影响` table as a candidate index, not as promotion authority. Verify every category independently and inspect omitted categories when the diff or acceptance evidence exposes a material effect.

## Return no-promotion idempotently

When no candidate passes the threshold:

1. Compose a concise source PR callback containing the terminal marker, outcome `no-promotion`, evaluated source identity, category-by-category reasons, and eligibility registration URL.
2. Use the loaded Pull Request transport protocol to add the exact comment.
3. Independently read the comment and source PR back.
4. Verify the marker, comment digest, unchanged merged source identity, and absence of a conflicting callback.
5. Return `no-promotion` only for `verified` or `no-op` transport results.

Do not create an empty branch, commit, memory file, or PR merely to demonstrate activity.

## Create a project-memory-only change

When one or more candidates pass:

1. Synchronize `develop` after the product merge and bind its SHA.
2. Create or resume one dedicated project-memory branch associated with the source PR.
3. Preserve unrelated worktree changes.
4. Update the smallest correct authority-layer files and use links instead of copied facts.
5. Split a multi-layer update by classification; keep each fact in one authoritative destination.
6. Update a wiki link or active-rule route only when discovery would otherwise fail and the update protocol allows it.
7. Keep the diff limited to `docs/decisions/`, `docs/rules/active/`, `docs/wiki/`, `.project-memory/context_brief.md`, and `.project-memory/daily_logs/`.
8. Validate the actual changed paths against applicable repository rules, lifecycle metadata, links, status, terminology, discovery coverage, and single-source-of-truth behavior.
9. Run repository-required validation when active-rule metadata changes.
10. Commit and push the exact project-memory-only change; omit `Co-Authored-By`.
11. Create or update one Draft project-memory PR through the loaded Pull Request transport protocol, explicitly targeting `develop`.

The project-memory PR Body must include:

- source Issue and merged product PR links;
- source Issue/PR digests and source head/merge identity;
- each promoted conclusion, classification, destination, and evidence;
- any proposed decision confirmed, corrected, superseded, or left proposed, with supporting evidence;
- validation commands and results;
- confirmation that no product code, tests, current task state, or duplicate fact source is included.

Reference the source Issue in the project-memory PR Body with a plain `Refs`-style link so the memory reconciliation is bound into the Issue lifecycle. Never use a closing keyword as the closure mechanism: a `develop`-base merge does not fire it, and source Issue closure is the explicit judgment below.

## Require an independent Reviewer

After independent read-back, bind the Draft project-memory PR Body digest, head SHA, base ref `develop`, and base SHA. Start a new clean, read-only Reviewer for each review round and supply only exact source identities/evidence, the PR tuple and diff, and the authoritative sources used for classification.

Forbid edits, GitHub mutations, alternative designs, and non-blocking wording suggestions. Require the verdict to remain bound to the supplied tuple and cited authoritative evidence, and require `PASS` or blocking `FAIL` for the exact tuple. Check:

1. source traceability and merged/accepted evidence;
2. correct write classification and authority destination;
3. cross-task reuse, capability-judgment value, or concrete forgetting risk;
4. exclusion of single-task tracking, generic knowledge, and discoverable implementation trivia;
5. one fact in one authority layer with links instead of duplication;
6. correct accepted/proposed/superseded treatment;
7. compliance with applicable repository rules and required confirmation gates;
8. a project-memory-only diff and executable validation.

Fix blockers in the Promotion Agent, update the Draft PR, bind the new tuple, and use a new clean Reviewer. Continue until PASS or a genuine blocker; never let the Reviewer edit.

## Mark the reviewed project-memory PR Ready

After PASS:

1. Add an append-only PASS comment to the project-memory PR identifying the exact reviewed tuple and evidence.
2. Independently read the comment back.
3. Re-read the PR, refs, Body digest, and diff; stop if the reviewed tuple changed.
4. Use the loaded Pull Request transport protocol to mark the exact Draft PR Ready.
5. Independently verify Ready state and every bound field.
6. Add a source product PR callback containing the terminal marker, outcome `memory-pr-ready`, eligibility registration URL, and project-memory PR URL.
7. Independently read the source callback back.

Fail closed on partial or ambiguous mutations. Do not merge the project-memory PR.

## Judge and close the source Issue

Own the source Issue closure judgment; no other phase closes the source Issue.

- Judge closable only when durable-memory reconciliation is terminal for the unchanged source: an independently verified `no-promotion` callback exists, or the project-memory PR is independently verified merged.
- When the project-memory PR is Ready but unmerged, keep the Issue open and hand off closure to a repeated `context-promotion` invocation after that PR merges.
- When closable, close the source Issue through the loaded Issue transport protocol with an explicit state mutation, then independently read back the closed state; accept only `verified` or `no-op` transport results and fail closed otherwise.
- Never leave the Issue state ambiguous: record the closure outcome in the closed result.

## Return a closed result

~~~yaml
outcome: verified-memory-pr | no-promotion | blocked
issue_url: https://github.com/owner/repo/issues/123
source_pr_url: https://github.com/owner/repo/pull/456
source_head_sha: null
eligibility_registration_url: null
source_callback_url: null
memory_pr_url: null
memory_pr_body_sha256: null
memory_head_sha: null
ready_state_verified: false
memory_pr_merged: false
issue_closure: null | pending-memory-pr-merge | closed
issue_state_verified: false
promoted_sources: []
reason: null
recovery_condition: null
handoff:
  role: external-review | context-promotion
  authoritative_sources: []
  next_action: null
~~~

For `verified-memory-pr`, hand off only the Ready project-memory PR URL to final human or repository review and return `issue_closure: pending-memory-pr-merge` with the Issue left open. When a repeated invocation independently verifies that PR merged, persists `memory-pr-merged`, and closes the source Issue, return the verified source callback, `issue_closure: closed`, and no further action.

For `no-promotion`, reconciliation is terminal: close the source Issue in the same invocation and return the Issue URL, merged source PR URL, verified callback URL, `issue_closure: closed`, and no further action.

For blocked, preserve any Draft project-memory PR, leave the Issue state untouched, and report the exact state and recovery condition without claiming promotion or closure succeeded.
