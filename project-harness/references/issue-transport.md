# Issue Transport Protocol

Load this internal protocol only when the selected operation row in the root Skill names the Issue transport.

Execute Harness-authorized Issue operations on the consuming project's hosting platform without owning the workflow or meaning of the Issue. Never invoke this reference as a separate Skill.

## Keep the transport boundary

- Accept exact intent and payload from the selected Harness operation. Do not refine requirements, choose Issue wording, classify semantic duplicates, decide lifecycle transitions, or choose between Body and comments.
- Operate on Issues and Issue comments only. Exclude Pull Requests from search results and reject a Pull Request passed as an Issue target.
- Prefer a platform MCP or App operation callable in the current session. When no MCP/App operation for the platform is callable, fall back to the platform's official authenticated CLI as the single transport for the whole operation; never use direct REST calls, browser automation, or unverified transports.
- Never install a plugin, edit MCP configuration, switch accounts, request broader permissions, or repair authentication. Return `blocked` with the missing capability and evidence only when neither an MCP/App operation nor an authenticated official CLI session is callable.
- Do not write repository files, local caches, hand-off files, or local audit logs. The hosting platform holds the Issue state.
- Do not create probe Issues during ordinary work. Require a separate explicit user request for a smoke test, name its Issue clearly, and close it when the test completes.

## Resolve the target and transport

1. Use an explicit Issue URL or the repository identity plus Issue number when supplied.
2. When only `#number` is supplied, derive the repository identity only from one unambiguous remote on a supported hosting platform in the current workspace. Return `blocked` for no remote, multiple candidates, or a remote on an unsupported platform.
3. Discover callable platform operations by capability rather than tool namespace. Require repository metadata, Issue search and fetch, complete paginated comment enumeration when requested, the requested mutation, and an independent fetch after mutation.
4. Read metadata for the exact repository. Treat an enabled or connected status, successful login, and global search as insufficient proof of repository access.
5. Select one authenticated transport for the whole operation. Do not mutate through one integration and verify through another because identities and repository grants may differ.
6. Independently resolve the selected transport's authenticated actor login/ID and the login that its mutations will author. Return them as a verified identity record; return blocked when either identity is ambiguous.

## Require explicit write authority

Allow a write only when the current explicit `project-harness` role authorizes that exact mutation. Require the selected operation to supply the exact target and payload.

Allow final source Issue closure only to the current explicit `delivery` invocation after its loaded operation establishes every applicable closure gate. Do not turn read access, an implicit route, a prior hand-off, or a general task objective into write authority. Return `blocked` when the authority source is absent or broader than the requested mutation.

## Execute only atomic Issue operations

| Operation | Required behavior |
| --- | --- |
| Search | Search the exact repository and requested open/closed scope. Return raw normalized Issue candidates without semantic classification. Mark and exclude Pull Requests. |
| Read | Fetch the exact Issue and requested comments. Return identity, state, metadata, title, Body digest, and for every requested comment its ID, URL, author login, creation time, normalized Body digest, and Body when requested, without changing the platform. Enumerate every comment page and report completeness explicitly only when the caller requests a complete comment inventory for a concrete read or diagnostic purpose; never treat a truncated page as the full candidate set. |
| Create | Require an exact title and the caller's complete Body, if any. Apply only explicitly supplied labels, assignees, or milestone. Never infer metadata or semantic uniqueness. |
| Replace Issue content | Require the exact Issue identity and complete replacement title or Body. Do not perform fuzzy, section-based, or conversational edits. |
| Change metadata | Support explicit state/state reason, labels, assignees, and milestone mutations. Require an explicit mode for collection fields such as replace, add, or remove. Preserve omitted fields. |
| Add a comment | Require exact comment text and write authority. Do not decide that a workflow update belongs in a comment. |
| Replace a comment | Require the exact comment ID and complete replacement text. Do not edit a comment by fuzzy match. |

Do not support Projects, Issue types, dependencies, or Pull Request mutations until a real task expands this contract.

## Protect every mutation

Treat this section as the root Skill's `L2 atomic-mutation-guard`. A caller summary or cached read cannot replace the target baseline, immediate pre-write comparison, ambiguous-response recovery, or independent read-back.

1. Fetch the current Issue and the minimum fields needed to prove identity, establish the baseline, and verify preservation. For a comment update, fetch the exact comment as part of the baseline.
2. Normalize Markdown line endings to LF with exactly one trailing newline. Use `scripts/markdown_digest.py` to calculate the SHA-256 digest for an Issue Body or comment text.
3. Compare the desired state with the baseline. If all requested fields already match, skip the mutation and return `no-op` with the verified identity and digest.
4. For an update, fetch the target again immediately before writing. Compare its identity, relevant fields, and Body or comment digest with the baseline. Return `blocked` on any concurrent change; require the caller to rebuild the complete replacement.
5. Send one mutation containing only the explicitly authorized fields. Preserve every omitted field.
6. If the mutation response is missing, times out, or is otherwise ambiguous, do not retry. Recover through search or fetch only when Issue identity, title, expected digest, and operation evidence prove that the original mutation succeeded. For an authorized comment, enumerate all comment pages when needed to match the exact normalized whole Body/digest. Otherwise return `indeterminate`.
7. After a mutation response, perform a separate fetch through the same transport. Never reuse the mutation response as read-back evidence.
8. Verify the Issue or comment identity, every requested field, every protected baseline field, and applicable Markdown digests. Return `indeterminate` for unexpected side effects or a mismatch, even when the platform accepted the mutation.

Treat final Issue closure and its independent post-mutation state verification as the root Skill's `L3 irreversible-gate`. Immediately re-read the original workflow evidence required by the selected Harness operation. After closure verification, perform no unlock, reopen, or post-close comment mutation.

## Return the shared result envelope

Return a concise structured result with this shape. Use `null` or empty collections for fields that do not apply.

```yaml
outcome: verified | no-op | blocked | indeterminate
operation: search | read | create | replace-content | change-metadata | add-comment | replace-comment
repository: owner/repo
issue_number: 123
url: https://example.com/owner/repo/issues/123
authenticated_actor:
  login: null
  id: null
  mutation_author_login: null
  verified: false
comment_id: null
snapshot:
  title: Example Issue
  body: null
  body_sha256: null
  state: open
  state_reason: null
  locked: false
  labels: []
  assignees: []
  milestone: null
  comment_ids: []
  comments:
    - id: null
      url: null
      author: null
      created_at: null
      body: null
      body_sha256: null
  comments_complete: null
  comments_next_cursor: null
changed_fields: []
preserved_fields_verified: []
before_body_sha256: null
after_body_sha256: null
before_comment_sha256: null
after_comment_sha256: null
read_back_verified: true | false | null
candidates: []
reason: null
```

Populate `snapshot` with the fetched Issue state, state reason, lock state, and other requested fields for read operations and with the independently fetched final state for writes. Include the complete Issue Body or comment Body only when the caller requested it; always include its digest when it exists. For every requested comment, always include ID, URL, author, creation time, and digest so workflow authorship, immutable-baseline, diagnostic, and recovery checks are executable. Set `comments_complete: true` only after every requested page is fetched; expose an opaque next cursor while incomplete and never let the caller claim a complete inventory. Leave mutation-only before/after fields `null` for a pure read.

Do not turn this envelope into an Issue comment. Let the caller decide how to use it. Treat only `verified` and `no-op` as successful outcomes; never collapse `blocked` or `indeterminate` into success.

## Adapt the canonical contract to each hosting platform

The sections above are the only Issue-transport contract. This section names how each canonical capability lands on a supported hosting platform; it adds no operation, field, gate, or outcome. GitHub and GitLab are the supported hosting platforms; adding another extends this section and nothing else. The transport fallback chain is the same on every platform: prefer a callable platform MCP or App operation, then fall back to that platform's official authenticated CLI (`gh` on GitHub, `glab` on GitLab), and return `blocked` when neither is callable.

| Canonical concept | GitHub | GitLab |
| --- | --- | --- |
| Repository identity (`repository` value and URL) | `owner/repo`; `https://github.com/owner/repo/issues/N` | Full project path including nested groups; `https://<host>/<group>/<project>/-/issues/N` |
| Open state | `open` | `opened` — report `open` |
| Close with `state_reason: completed` | close reason `completed` | No close-reason field: perform the close, read back `state: closed`, and report `state_reason: completed` (GitLab has no not-planned distinction; closed is completed) |
| `locked` | Issue lock state | Issues have no lock concept: always report `false` |
| Pull Request exclusion in search | Issues and Pull Requests share one number space: filter Pull Requests from search results and reject one passed as an Issue target | Issues and merge requests are separate objects: the exclusion rule holds trivially |
| Comment anchor | `#issuecomment-<id>` | `#note_<id>` |
| Actor `login` / `id` | account login / id | username / id |
| Platform Issue template (forbidden by the Issue contract) | `.github/ISSUE_TEMPLATE` | `.gitlab/issue_templates` |

State normalization is a reporting rule: the envelope always carries the canonical values above, whatever raw state the platform returns. GitLab merge-request `discussion_locked` does not map to the Issue `locked` field.

## Use the digest utility

Read UTF-8 content from a file:

```bash
python3 scripts/markdown_digest.py path/to/body.md
```

Read standard input, emit normalized content, or verify an expected digest:

```bash
python3 scripts/markdown_digest.py
python3 scripts/markdown_digest.py --print-normalized
python3 scripts/markdown_digest.py --expect <sha256>
```
