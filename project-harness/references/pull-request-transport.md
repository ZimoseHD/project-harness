# GitHub Pull Request Transport Protocol

Load this internal protocol only when the selected operation row in the root Skill names the Pull Request transport.

Execute Harness-authorized GitHub Pull Request operations without owning the workflow or meaning of the Pull Request. Never invoke this reference as a separate Skill.

## Keep the transport boundary

- Accept exact intent and payload from the selected Harness operation.
- Leave PR wording, Issue relationship classification, implementation status, acceptance verdicts, merge decisions, and durable project-memory selection to the caller.
- Operate on Pull Requests, their top-level conversation comments, their exact refs, and check evidence only.
- Prefer callable GitHub MCP or App operations in the current session. When no MCP/App GitHub operation is callable, fall back to the authenticated `gh` CLI as the single transport for the whole operation.
- Never use direct REST calls, browser automation, or a second authenticated transport.
- Never install a plugin, edit MCP configuration, switch identity, broaden permissions, create Git commits, push branches, enable auto-merge, close without merge, reopen, or delete a Pull Request. Support only the exact guarded merge operation defined below.
- Return blocked when a required capability or exact authority is unavailable.

## Resolve the repository and target

1. Prefer an explicit PR URL or owner/repo plus PR number.
2. Derive owner/repo from the workspace only when exactly one unambiguous GitHub remote exists.
3. Read metadata for the exact repository before trusting access.
4. Discover callable operations by capability rather than tool namespace. When requested for Delivery preflight or merge, report whether repository merge-method capability is known and return the exact sorted subset of `merge`, `squash`, and `rebase` currently available.
5. Require only the capabilities needed for the requested atomic operation and its independent read-back.
6. Use one authenticated GitHub transport for the entire operation.
7. Independently resolve the selected transport's authenticated actor login/ID and the login that its mutations will author. Return them as a verified identity record; return blocked when either identity is ambiguous.

Treat a successful login, global search, enabled connector, or local Git remote as insufficient proof of repository access.

## Require exact write authority

Allow a mutation only when the current explicit `project-harness` role authorizes that exact PR mutation. Require the selected operation to supply the exact repository, target, payload, expected baseline, and protected fields.

Allow `merge` only under a current explicit `delivery` invocation (product and memory kinds) or a current explicit `express` invocation (express kind). Do not treat repository write access, an implicit route, a prior hand-off, a general implementation request, an acceptance verdict, user confirmation alone, or Ready state as implicit authority for unrelated PR mutations.

## Support only atomic operations

| Operation | Required behavior |
| --- | --- |
| search | Search the exact repository and requested open/closed scope. Return normalized PR candidates without semantic classification. |
| read | Fetch the exact PR identity, title, Body, Draft/open/merged state, merge identity and verified merge provenance when requested, head ref/SHA, base ref/SHA, mergeability when available, repository merge-method capability when requested, requested top-level comments, and requested changed-file/unified-diff evidence. For each requested comment return identity, URL, author login, creation time, normalized Body digest, and Body when requested. |
| create-draft | Require exact title, complete Body, head ref, base ref, and explicit Draft intent. Never infer labels, reviewers, or other metadata. |
| replace-content | Require the exact PR and a complete replacement title and/or Body. Never patch a fuzzy section. |
| add-comment | Require exact Markdown comment text and explicit authority. |
| replace-comment | Require exact comment ID, complete replacement text, and explicit authority. |
| read-checks | Read combined commit status and applicable workflow runs for the exact head SHA. Report required-check knowledge separately from observed checks. |
| mark-ready | Change an exact open Draft PR to Ready only with explicit workflow authority. |
| convert-to-draft | Change an exact open Ready PR to Draft only with explicit workflow authority. |
| merge | Merge one exact open Ready PR only under a current explicit `delivery` or `express` invocation. Require expected title/Body digest, head ref/SHA, base ref/SHA, known successful required checks, affirmatively established mergeability, exact merge method from a validated Harness integration policy, current repository support for that method, and caller-supplied gate evidence URL/digest pairs. |

Reject auto-merge, close without merge, reopen, branch creation, commit creation, arbitrary ref updates, Issue mutations, inline code review, reviewer assignment, and semantic approval.

## Normalize Markdown deterministically

Use scripts/markdown_digest.py for every PR Body or top-level comment:

- convert CRLF and CR to LF;
- remove all trailing newlines;
- append exactly one trailing newline;
- calculate SHA-256 over normalized UTF-8 bytes.

Treat any title, Body, or comment change after review as a new artifact requiring a new digest and applicable review.

For a requested diff, return the complete transport-produced unified diff normalized to LF with exactly one trailing newline and calculate SHA-256 over those UTF-8 bytes. Return changed files sorted by path with status, previous path when renamed, additions, deletions, and blob SHA when available. Treat a truncated diff, missing changed file, or unstable digest as unavailable evidence rather than a complete read. Use `diff_sha256` only to detect drift within reads performed by the same selected transport; bind cross-run review and merge to exact head/base SHAs, Body digest, title, and changed-file/blob identities instead.

## Protect every mutation

Treat this section as the root Skill's `L2 atomic-mutation-guard`. A caller summary, hand-off, or cached semantic read cannot replace any target baseline, immediate pre-write comparison, mutation recovery, or independent read-back below.

1. Fetch the exact PR and the minimum comment/check state needed to prove identity and establish a baseline.
2. Normalize and digest every baseline Markdown field involved in the operation.
3. Compare desired state with the baseline. Return no-op after independent verification when every requested field already matches.
4. Fetch the target again immediately before an update.
5. Compare PR identity, state, Draft flag, head ref/SHA, base ref/SHA, requested content digests, and protected fields with the baseline.
6. Return blocked on any concurrent change. Require the caller to rebuild the complete payload from the new baseline.
7. Send one mutation containing only explicitly authorized fields.
8. Do not retry a timed-out, missing, or ambiguous mutation response.
9. Recover through read/search only when identity, expected digest, refs, and operation evidence prove the original mutation succeeded. Otherwise return indeterminate.
10. Perform a separate fetch through the same transport after every mutation.
11. Verify identity, every requested field, applicable digests, refs, Draft/Ready state, and every protected baseline field.
12. Return indeterminate for any mismatch or unexpected side effect, even if GitHub accepted part of the request.

For create-draft, search immediately before creation and never create when the caller has not resolved multiple or ambiguous active candidates.

## Guard an exact merge

Treat merge as an irreversible integration mutation, not as a convenience state change.

Treat this section as the root Skill's `L3 irreversible-gate`. No delegated carrier or cached read replaces or substitutes for this merge guard.

1. Require a current explicit `delivery` authority for the exact Issue lineage (product or memory kind), or a current explicit `express` authority for the exact express PR (express kind), plus a caller-selected `merge_method` resolved from a valid Harness integration policy: schema-v2 uses the configured product or project-memory method; schema-v1 compatibility uses the sole authoritatively available method. Never choose or substitute a method in the transport.
2. Require the exact expected PR title, normalized Body digest, Ready/open state, head ref/SHA, base ref `develop`, base SHA, successful required checks with `required_checks_known: true`, and `mergeable: true` or the selected transport's authoritative equivalent. Treat unknown mergeability as blocked, not as permission to attempt the irreversible mutation.
3. Require caller-supplied persistent gate evidence URL/digest pairs. For a product PR the pair identifies the `review` PASS verdict. For a project-memory PR the pairs identify the proposal artifact and the source-bound confirmation. An express merge carries an empty evidence set by definition. Return blocked when any required URL or normalized whole-comment digest is absent; leave semantic validation to the caller.
4. Set `merge_kind: product`, `merge_kind: memory`, or `merge_kind: express`; do not accept caller-defined evidence names. The deterministic guard fixes product evidence to `review-pass`, memory evidence to `proposal` and `confirmation`, and express evidence to the empty set.
5. Immediately before merge, obtain the PR/check snapshot, re-read repository merge-method capability, and independently re-read every evidence comment through the applicable loaded transport. Require `merge_methods_known: true` and the selected method to remain in `available_merge_methods`. Compare every expected field, protected field, evidence URL/digest, and protocol-owned evidence kind with the baseline. Return blocked on a missing/extra evidence kind, drift, unavailable configured method, Draft state, unknown or non-successful required checks, wrong base, closed-unmerged state, or mergeability other than affirmative true.
6. If the exact PR is already merged, independently verify non-Draft state, currently known and successful required checks for the exact head, the expected title/Body/head/base tuple, all protocol-owned evidence URL/digest pairs, the actual merge method as exactly `merge`, `squash`, or `rebase` and equal to the requested authoritative method, verified merge provenance, and a non-null merge commit identity. Return `no-op` only for an exact match; return blocked or indeterminate for a conflicting identity. This recovery proves the current persistent state conservatively; it does not claim that a fresh re-entry observed the checks at the historical merge instant.
7. Send one merge mutation. Do not retry a timeout or missing response.
8. Recover an ambiguous response only by independently fetching the exact PR and evidence, then proving `merged: true`, the expected tuple, all protocol-owned evidence pairs, and a non-null merge commit identity. Otherwise return `indeterminate`.
9. After a successful response, independently fetch the PR through the same transport and verify `state: closed`, `merged: true`, the expected title/Body/head/base lineage, preserved non-base protected fields, all gate evidence, and a non-null merge commit identity. Produce `merge_provenance` only from an authoritative merge event, verified commit provenance, or the mutation plus independent read-back; it must bind the guarded base SHA, guarded head SHA, merge commit SHA, evidence source, and `verified: true`. A caller-supplied or copied expected base is not provenance. If the transport exposes the live base branch tip after merge instead of the guarded pre-merge base SHA, use this verified record rather than comparing the advanced live tip as though it were unchanged.

Require every required check and required CI result from the exact current head. Never reuse or carry forward an old-head or previous-head required check, even when a validation-impact artifact retains local validation.

Never weaken a merge gate because branch protection would have rejected an unsafe request. Repository acceptance and Harness evidence remain separate requirements.

## Report check evidence conservatively

- Bind check reads to the exact head SHA.
- Return combined commit status and each observed status/workflow run.
- Distinguish success, failure, pending, missing, and unavailable capability.
- Normalize the applicable required subset separately as `required_checks`, mapping each unique required check name to exactly `success`, `failure`, `pending`, `missing`, or `unavailable`. An empty mapping is valid only when `required_checks_known: true` proves the authoritative required set is empty; in that case a raw combined status such as `pending` with zero legacy contexts remains diagnostic and does not invent a required-check blocker.
- Report required_checks_known as false when branch-protection or repository-rule requirements cannot be discovered.
- Never infer that no observed checks means no required checks.
- Let the selected `role: review` operation decide whether unavailable required-check knowledge blocks acceptance.

## Return the shared result envelope

Return exactly one outcome: verified, no-op, blocked, or indeterminate.

~~~yaml
outcome: verified | no-op | blocked | indeterminate
operation: search | read | create-draft | replace-content | add-comment | replace-comment | read-checks | mark-ready | convert-to-draft | merge
repository: owner/repo
pr_number: 123
url: https://github.com/owner/repo/pull/123
authenticated_actor:
  login: null
  id: null
  mutation_author_login: null
  verified: false
comment_id: null
snapshot:
  title: Example
  body: null
  body_sha256: null
  state: open
  is_draft: true
  merged: false
  merged_at: null
  merge_commit_sha: null
  merge_method: null
  merge_provenance:
    verified: false
    source: null
    guarded_base_sha: null
    guarded_head_sha: null
    merge_commit_sha: null
  head_ref: task/example
  head_sha: null
  base_ref: develop
  base_sha: null
  mergeable: null
  available_merge_methods: []
  merge_methods_known: null
  comment_ids: []
  comments:
    - id: null
      url: null
      author: null
      created_at: null
      body: null
      body_sha256: null
  changed_files:
    - path: null
      status: null
      previous_path: null
      additions: null
      deletions: null
      blob_sha: null
  diff: null
  diff_sha256: null
  checks: []
  required_checks:
    required-check-name: success | failure | pending | missing | unavailable
  required_checks_known: null
changed_fields: []
protected_fields_verified: []
before_body_sha256: null
after_body_sha256: null
before_comment_sha256: null
after_comment_sha256: null
read_back_verified: true | false | null
candidates: []
reason: null
~~~

Include the complete PR Body, comment Body, or unified diff only when requested by the caller. Always include its digest when it exists. For every requested comment, always include ID, URL, author, creation time, and digest so workflow authorship, immutable-baseline, predecessor, and legacy checks are executable. When changed-file or diff evidence is requested, always return the complete sorted file metadata and `diff_sha256`. Set `merge_methods_known: true` only after authoritative repository metadata establishes the complete available set; sort that set and reject unknown values. Treat only verified and no-op as success.

## Use the bundled verifier

Calculate a digest:

~~~bash
python3 scripts/markdown_digest.py path/to/body.md
~~~

Normalize content or verify an expected digest:

~~~bash
python3 scripts/markdown_digest.py --print-normalized
python3 scripts/markdown_digest.py --expect SHA256
~~~

Run the deterministic tests:

~~~bash
python3 scripts/test_markdown_digest.py
python3 scripts/test_transport_guard.py
~~~

scripts/transport_guard.py makes idempotent content comparison, protected-baseline conflict detection, unique-candidate selection, exact read-back, ambiguous-mutation recovery, and the pre-merge/ambiguous-merge decision executable without introducing another GitHub transport. Call `exact_merge_guard` with `merge_kind`, the exact expected tuple, expected and freshly read evidence URL/digest maps, checks, mergeability, and merge method. The function owns the exact product/memory evidence-name sets and supports a separately recorded `guarded_base_sha` when a post-merge API exposes an advanced live base tip. Treat its failure-path results as binding; never weaken them from a selected Harness operation.
