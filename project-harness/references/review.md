# Review

Execute this phase only after `project-harness` dispatches `role: review`, or a current `delivery` invocation runs the Review phase.

Carry the Review phase as the acceptance gate for one exact Issue and Draft Pull Request snapshot. Review verifies three things: the complete diff stays inside the Issue boundary, the unit tests pass against the current head, and the durable-memory impact claims hold. It never becomes a second implementation pass.

## Contents

- Enforce the authority boundary
- Accept the semantic input
- Bind the review snapshot
- Check the three review items
- Re-read before the verdict
- Record the append-only verdict
- Handle failure and success
- Return a phase result

## Enforce the authority boundary

- Start only from one Issue URL and one Draft product PR URL supplied by a current explicit `role: review` invocation or a current `delivery` invocation.
- Review with fresh eyes: judge the diff and evidence yourself rather than trusting the implementer's summary. Subagent use is unconstrained—spawn read-only verifiers whenever separate context materially helps, and integrate their results yourself.
- Treat that invocation as authority only for the top-level verdict comment and the Draft/Ready mutations enumerated here. Never derive write authority from host/model loading, automatic routing, an ordinary hand-off, an ordinary review request, or a prior run.
- Never modify product code, tests, commits, refs, PR Body, Issue Body, or durable project memory. Never make even a small implementation fix.
- Never merge, close the Issue, redesign requirements, or convert missing evidence into a PASS.

Return accepted-ready-pr, return-to-implementation, return-to-spec, or blocked.

## Accept the semantic input

Apply the root Skill's public-invocation adapter. Require an exact `role: review` (standalone) or a current `delivery` phase request, plus one Issue URL and one Draft product PR URL. Read both sources completely; do not rely on a prior phase's summary, chat, local plan, or implicit memory.

## Bind the review snapshot

Follow the loaded Issue and Pull Request transport protocols to prove:

- exact repository and Issue/PR identity;
- open Issue state;
- open Draft PR state and its relationship to the Issue;
- Issue Body digest, exact PR title, PR Body digest;
- head ref and head SHA, base ref `develop` and base SHA;
- current mergeability when available;
- required-check knowledge and observed required checks bound to the head SHA;
- top-level verdict and promotion callbacks already present.

Bind the exact tuple (Issue Body digest, PR title/Body digest, head ref/SHA, base ref/SHA). Stop blocked on target ambiguity, missing read-back, an unverifiable relationship, or unavailable evidence that prevents a safe verdict.

## Check the three review items

Judge exactly these items and record each in the verdict:

1. **`issue-scope`** — Independently read the exact compact `### 改动范围` subsection and compare it with the complete final product diff, not a file summary or the Implementation hand-off.
   - Require the compact scope to be present and unambiguous for a new or open/unmerged lineage; a lineage without it returns to `spec`.
   - Judge ordinary business changes against the Issue description and its `普通业务改动` field.
   - Require every changed protected surface to match one exact `受保护改动` exception with its compatibility or migration boundary. The exact declaration `受保护改动：无` requires the final diff to contain no protected-surface change.
   - Do not accept `实施计划`, the PR Body, an ADR, repository convention, chat, or Implementation's explanation as additional mutation authority.
   - When an out-of-scope edit is unnecessary and removable, FAIL with `return_stage: implementation` naming the offending area. When completion genuinely requires broader scope or an unlisted protected change, FAIL with `return_stage: spec`.
2. **`unit-tests`** — Require the changed-code unit tests to pass against the exact current head.
   - Reuse a validation result only when it identifies the exact command/check, successful result, and final head SHA or immutable CI run; independently read that source and confirm it still covers the changed boundary.
   - Do not rerun a current-head check merely to demonstrate independence. Rerun the narrow applicable command when evidence is missing, stale, ambiguous, tied to another head, or risk-sensitive (security, privacy, destructive data, external compatibility, difficult-to-reverse architecture).
   - Verify every required check against the bound head SHA. Wait for pending required checks rather than passing early. Never infer that no observed checks means no required checks.
   - Require `required_checks_known: true` from the bound transport read before PASS; remain BLOCKED while the transport reports false.
3. **`durable-memory-impact`** — Map the PR's `持久项目记忆实际影响` claims to the diff, tests, cited sources, and repository state.
   - Require exactly one factual row for each of `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`. The exact literal `无` is the only no-impact value; its evidence cell must be non-empty and non-placeholder.
   - Record `result: PASS` with `evidence: all-five-none` only when all five values are exactly `无` and your independent inspection confirms every claim. Otherwise record PASS with a factual evidence note naming the real candidate categories.
   - Treat `none`, `no_write`, `N/A`, a blank value, a missing row, or vague wording as an evidence defect (FAIL).

Do not add new delivery requirements during Review. When the existing contract cannot support a valid verdict, FAIL with `return_stage: spec`.

For visual, business, real-device, external-system, or other human-only acceptance, accept only an already persisted explicit confirmation URL and digest bound to the exact snapshot; otherwise return blocked.

## Re-read before the verdict

Immediately before recording a verdict, independently fetch the Issue, PR, refs, Body, comments, and checks again.

- Restart affected checks when head SHA or base SHA changes.
- Re-run the scope judgment when the Issue or diff changed; never publish a verdict for a diff that has not passed it.
- Return return-to-spec for a binding Issue contract change.
- Recheck factual claims when the PR title or Body changes.
- Stop on any unexplained target, ref, Draft state, or protected-field change.

Never publish a verdict for a stale tuple.

## Record the append-only verdict

Compose the exact **Review verdict** artifact from `references/evidence-contract.md`—that shared contract is the only authority for its fields, values, tuple bindings, and success semantics—and write it as one complete top-level PR comment for the exact snapshot. Never overwrite a prior round.

Use the loaded Pull Request transport protocol to add the exact comment and independently read it back. Bind its comment ID, URL, and Markdown digest. Treat only verified or no-op as a recorded verdict.

## Handle failure and success

For an implementation, test, behavior, or evidence defect:

1. Record FAIL with exact blockers and `return_stage: implementation`.
2. Keep the PR Draft or convert it back to Draft.
3. Return return-to-implementation with the Issue URL, Draft PR URL, and verdict comment URL.

For a delivery-contract defect:

1. Record FAIL with the exact unsupported decision or acceptance gap and `return_stage: spec`.
2. Keep the PR Draft.
3. Return return-to-spec for the same Issue.

For an external, permission, environment, required-check-discovery, or human-confirmation blocker, record BLOCKED when GitHub writing remains available, preserve the Draft PR, and return blocked with the recovery condition.

Impose no arbitrary retry limit. Every repaired head SHA changes the bound input and receives a new append-only verdict.

After a verified PASS whose payload has `required_checks_known: true`:

1. Re-read the bound snapshot once more.
2. Use the loaded Pull Request transport protocol to mark the exact Draft PR Ready.
3. Independently verify Ready state, unchanged title/Body digests, unchanged refs, and the verdict comment.

Fail closed on a partial or ambiguous mutation. Review never merges. A later title, commit, PR Body, or base change invalidates the verdict and requires a fresh review round; convert a stale accepted PR back to Draft before recording a new verdict.

## Return a phase result

~~~yaml
outcome: accepted-ready-pr | return-to-implementation | return-to-spec | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
pr_url: https://github.com/owner/repo/pull/456
pr_title: null
pr_body_sha256: null
head_ref: null
head_sha: null
base_ref: null
base_sha: null
verdict_comment_url: null
verdict_comment_sha256: null
ready_state_verified: false
code_only_verified: false
promotion_required: true
reason: null
recovery_condition: null
next_action: null
~~~

- Set `code_only_verified: true` only for a final PASS whose `durable-memory-impact` item carries `evidence: all-five-none`; set it to false for every other outcome.
- Set `promotion_required: true` whenever any durable-memory category has a concrete non-`无` impact or cannot be verified.
- `delivery` may use the code-only fast path only after independently re-reading the PASS verdict and finding the exact `durable-memory-impact` / `PASS` / `all-five-none` entry on the unchanged accepted tuple; these result fields alone never authorize skipping Context Promotion.
- For accepted-ready-pr, return to the current `delivery` invocation (or recommend `role: delivery` standalone) with the Issue URL, Ready PR URL, verdict comment URL, and bound tuple.
