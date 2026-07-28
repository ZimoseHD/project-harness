# GitHub Pull Request Transport Protocol

Load this internal protocol only when the selected operation row in the root Skill names the Pull Request transport.

Execute Harness-authorized GitHub Pull Request operations without owning the workflow or meaning of the Pull Request. Never invoke this reference as a separate Skill.

## Keep the transport boundary

- Accept exact intent and payload from the selected Harness operation.
- Leave PR wording, Issue relationship classification, implementation status, acceptance verdicts, merge decisions, and durable project-memory selection to the caller.
- Operate on Pull Requests, their top-level conversation comments, their exact refs, and check evidence only.
- Prefer callable GitHub MCP or App operations in the current session. When no MCP/App GitHub operation is callable, fall back to the authenticated `gh` CLI as the single transport for the whole operation.
- Never use direct REST calls, browser automation, or a second authenticated transport.
- Never install a plugin, edit MCP configuration, switch identity, broaden permissions, create Git commits, push branches, merge, close, or delete a Pull Request.
- Return blocked when a required capability or exact authority is unavailable.

## Resolve the repository and target

1. Prefer an explicit PR URL or owner/repo plus PR number.
2. Derive owner/repo from the workspace only when exactly one unambiguous GitHub remote exists.
3. Read metadata for the exact repository before trusting access.
4. Discover callable operations by capability rather than tool namespace.
5. Require only the capabilities needed for the requested atomic operation and its independent read-back.
6. Use one authenticated GitHub transport for the entire operation.

Treat a successful login, global search, enabled connector, or local Git remote as insufficient proof of repository access.

## Require exact write authority

Allow a mutation only when the current explicit `project-harness` role authorizes that exact PR mutation and the selected operation supplies the exact repository, target, payload, expected baseline, and protected fields.

Do not treat repository write access, an implicit route, a prior hand-off, a general implementation request, or an acceptance verdict as implicit authority for unrelated PR mutations.

## Support only atomic operations

| Operation | Required behavior |
| --- | --- |
| search | Search the exact repository and requested open/closed scope. Return normalized PR candidates without semantic classification. |
| read | Fetch the exact PR identity, title, Body, Draft/open/merged state, merge identity, head ref/SHA, base ref/SHA, mergeability when available, and requested comments. |
| create-draft | Require exact title, complete Body, head ref, base ref, and explicit Draft intent. Never infer labels, reviewers, or other metadata. |
| replace-content | Require the exact PR and a complete replacement title and/or Body. Never patch a fuzzy section. |
| add-comment | Require exact Markdown comment text and explicit authority. |
| replace-comment | Require exact comment ID, complete replacement text, and explicit authority. |
| read-checks | Read combined commit status and applicable workflow runs for the exact head SHA. Report required-check knowledge separately from observed checks. |
| mark-ready | Change an exact open Draft PR to Ready only with explicit workflow authority. |
| convert-to-draft | Change an exact open Ready PR to Draft only with explicit workflow authority. |

Reject merge, auto-merge, close, reopen, branch creation, commit creation, ref updates, Issue mutations, inline code review, reviewer assignment, and semantic approval.

## Normalize Markdown deterministically

Use scripts/markdown_digest.py for every PR Body or top-level comment:

- convert CRLF and CR to LF;
- remove all trailing newlines;
- append exactly one trailing newline;
- calculate SHA-256 over normalized UTF-8 bytes.

Treat any title, Body, or comment change after review as a new artifact requiring a new digest and applicable review.

## Protect every mutation

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

## Report check evidence conservatively

- Bind check reads to the exact head SHA.
- Return combined commit status and each observed status/workflow run.
- Distinguish success, failure, pending, missing, and unavailable capability.
- Report required_checks_known as false when branch-protection or repository-rule requirements cannot be discovered.
- Never infer that no observed checks means no required checks.
- Let the selected `role: closeout` operation decide whether unavailable required-check knowledge blocks acceptance.

## Return the shared result envelope

Return exactly one outcome: verified, no-op, blocked, or indeterminate.

~~~yaml
outcome: verified | no-op | blocked | indeterminate
operation: search | read | create-draft | replace-content | add-comment | replace-comment | read-checks | mark-ready | convert-to-draft
repository: owner/repo
pr_number: 123
url: https://github.com/owner/repo/pull/123
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
  head_ref: task/example
  head_sha: null
  base_ref: develop
  base_sha: null
  mergeable: null
  comment_ids: []
  checks: []
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

Include the complete Body or comment only when requested by the caller. Always include its digest when it exists. Treat only verified and no-op as success.

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

scripts/transport_guard.py makes idempotent content comparison, protected-baseline conflict detection, unique-candidate selection, exact read-back, and ambiguous-mutation recovery executable without introducing another GitHub transport. Treat its failure-path results as binding; never weaken them from a selected Harness operation.
