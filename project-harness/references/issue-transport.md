# GitHub Issue Transport Protocol

Load this internal protocol only when the selected operation row in the root Skill names the Issue transport.

Execute Harness-authorized GitHub Issue operations without owning the workflow or meaning of the Issue. Never invoke this reference as a separate Skill.

## Keep the transport boundary

- Accept exact intent and payload from the selected Harness operation. Do not refine requirements, choose Issue wording, classify semantic duplicates, decide lifecycle transitions, or choose between Body and comments.
- Operate on Issues and Issue comments only. Exclude Pull Requests from search results and reject a Pull Request passed as an Issue target.
- Prefer GitHub MCP or App operations callable in the current session. When no MCP/App GitHub operation is callable, fall back to the authenticated `gh` CLI as the single transport for the whole operation; never use direct REST calls, browser automation, or unverified transports.
- Never install a plugin, edit MCP configuration, switch accounts, request broader permissions, or repair authentication. Return `blocked` with the missing capability and evidence only when neither an MCP/App operation nor an authenticated `gh` session is callable.
- Do not write repository files, local caches, hand-off files, or local audit logs. GitHub holds the Issue state. Allow caller-owned source-Issue Delivery observation comments only when the current `delivery` operation supplies an exact payload authorized by the loaded Delivery stage log contract.
- Do not create probe Issues during ordinary work. Require a separate explicit user request for a smoke test, name its Issue clearly, and close it when the test completes.

## Resolve the target and transport

1. Use an explicit Issue URL or `owner/repo` plus Issue number when supplied.
2. When only `#number` is supplied, derive `owner/repo` only from one unambiguous GitHub remote in the current workspace. Return `blocked` for no remote, multiple candidates, or a non-GitHub remote.
3. Discover callable GitHub operations by capability rather than tool namespace. Require repository metadata, Issue search and fetch, complete paginated comment enumeration when requested, the requested mutation, and an independent fetch after mutation.
4. Read metadata for the exact repository. Treat an enabled or connected status, successful login, and global search as insufficient proof of repository access.
5. Select one authenticated transport for the whole operation. Do not mutate through one integration and verify through another because identities and repository grants may differ.
6. Independently resolve the selected transport's authenticated actor login/ID and the login that its mutations will author. Return them as a verified identity record; return blocked when either identity is ambiguous.

## Require explicit write authority

Allow a write only when the current explicit `project-harness` role authorizes that exact mutation, or when a current explicit `delivery` invocation supplies a host-provenance-bound delegation whose mutation whitelist includes it. Require the selected operation to supply the exact target and payload.

Allow the current `delivery` coordinator to add only exact Delivery stage observation comments produced under the loaded log contract. After independently verified closure, allow only the exact `issue-closed` observation to be added to that still-closed Issue; never reopen it, and independently verify the Issue remains `closed`/`completed` after comment read-back. Return `blocked` when the closed Issue is locked or comments are forbidden. Never accept such a payload from a Phase Owner, Worker, Reviewer, standalone compatibility role, serialized observation, or prior hand-off. The transport validates target/payload authority and read-back only; it does not decide whether a stage completed or whether log coverage is sufficient.

Allow final source Issue closure only to either the current `delivery` coordinator after its loaded operation establishes every terminal gate, or a current explicit standalone `role: context-promotion` invocation after that phase establishes its compatibility closure gate. Never accept final closure from a Phase Owner delegated by `delivery`, a Worker, a Reviewer, or any other descendant. Do not turn read access, an implicit route, a serialized delegation envelope, a prior hand-off, a stage observation, or a general task objective into write authority. Return `blocked` when the authority source is absent or broader than the requested mutation.

## Execute only atomic Issue operations

| Operation | Required behavior |
| --- | --- |
| Search | Search the exact repository and requested open/closed scope. Return raw normalized Issue candidates without semantic classification. Mark and exclude Pull Requests. |
| Read | Fetch the exact Issue and requested comments. Return identity, state, metadata, title, Body digest, and for every requested comment its ID, URL, author login, creation time, normalized Body digest, and Body when requested, without changing GitHub. When the caller requests a complete Delivery observation inventory, ambiguous-comment recovery, or coverage, enumerate every comment page and report completeness explicitly; never treat a truncated page as the full candidate set. An ordinary live observation add/read-back may use the caller's already proven complete operation-local inventory and fetch only the Issue baseline plus the exact returned comment. |
| Create | Require an exact title and the caller's complete Body, if any. Apply only explicitly supplied labels, assignees, or milestone. Never infer metadata or semantic uniqueness. |
| Replace Issue content | Require the exact Issue identity and complete replacement title or Body. Do not perform fuzzy, section-based, or conversational edits. |
| Change metadata | Support explicit state/state reason, labels, assignees, and milestone mutations. Require an explicit mode for collection fields such as replace, add, or remove. Preserve omitted fields. |
| Add a comment | Require exact comment text and write authority. Do not decide that a workflow update belongs in a comment. For an `issue-closed` observation, require the pre-write baseline itself to prove `closed`/`completed`, preserve that state, and never attempt to unlock or reopen the Issue. |
| Replace a comment | Require the exact comment ID and complete replacement text. Do not edit a comment by fuzzy match. |

Do not support Projects, Issue types, dependencies, or Pull Request mutations until a real task expands this contract.

## Protect every mutation

Treat this section as the root Skill's `L2 atomic-mutation-guard`. An operation-local Evidence Bundle cannot replace the target baseline, immediate pre-write comparison, ambiguous-response recovery, or independent read-back.

1. Fetch the current Issue and the minimum fields needed to prove identity, establish the baseline, and verify preservation. For a comment update, fetch the exact comment as part of the baseline.
2. Normalize Markdown line endings to LF with exactly one trailing newline. Use `scripts/markdown_digest.py` to calculate the SHA-256 digest for an Issue Body or comment text.
3. Compare the desired state with the baseline. If all requested fields already match, skip the mutation and return `no-op` with the verified identity and digest.
4. For an update, fetch the target again immediately before writing. Compare its identity, relevant fields, and Body or comment digest with the baseline. Return `blocked` on any concurrent change; require the caller to rebuild the complete replacement.
5. Send one mutation containing only the explicitly authorized fields. Preserve every omitted field.
6. If the mutation response is missing, times out, or is otherwise ambiguous, do not retry. Recover through search or fetch only when Issue identity, title, expected digest, and operation evidence prove that the original mutation succeeded. For an observation comment, enumerate all comment pages and match the exact normalized whole Body/digest. Otherwise return `indeterminate`.
7. After a mutation response, perform a separate fetch through the same transport. Never reuse the mutation response as read-back evidence.
8. Verify the Issue or comment identity, every requested field, every protected baseline field, and applicable Markdown digests. Return `indeterminate` for unexpected side effects or a mismatch, even when GitHub accepted the mutation.

For a new live Delivery observation, do not require the transport to enumerate unrelated comments when the current coordinator supplies a proven complete operation-local inventory and the desired Body is absent from it. Protect the Issue identity/title/Body/state baseline, add once, and read the exact returned comment by ID. This optimization grants no trust to the caller's inventory: ambiguous response recovery, recovery without that complete inventory, and every manifest/closure/completion coverage read still require complete pagination and transport-verified authorship.

A normal observation write therefore uses targeted Issue baseline protection plus exact comment ID read-back without complete pagination. Ambiguous response recovery, clean recovery without a complete current inventory, and final coverage each require complete pagination across all comment pages.

Treat final Issue closure and the post-close state verification as the root Skill's `L3 irreversible-gate`. A Bundle never authorizes closure or substitutes for the complete workflow and coverage evidence required by the selected Harness operation.

## Return the shared result envelope

Return a concise structured result with this shape. Use `null` or empty collections for fields that do not apply.

```yaml
outcome: verified | no-op | blocked | indeterminate
operation: search | read | create | replace-content | change-metadata | add-comment | replace-comment
repository: owner/repo
issue_number: 123
url: https://github.com/owner/repo/issues/123
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

Populate `snapshot` with the fetched Issue state, state reason, lock state, and other requested fields for read operations and with the independently fetched final state for writes. Include the complete Issue Body or comment Body only when the caller requested it; always include its digest when it exists. For every requested comment, always include ID, URL, author, creation time, and digest so workflow authorship, immutable-baseline, observation coverage, and recovery checks are executable. Set `comments_complete: true` only after every requested page is fetched; expose an opaque next cursor while incomplete and never let the caller claim complete coverage. Leave mutation-only before/after fields `null` for a pure read.

Do not turn this envelope into an Issue comment. Let the caller decide how to use it. Treat only `verified` and `no-op` as successful outcomes; never collapse `blocked` or `indeterminate` into success.

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
