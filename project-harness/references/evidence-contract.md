# Delivery Evidence Contract

Load this shared contract only when the selected operation produces or consumes the persistent `review` and `context-promotion` evidence defined here.

This file is the single authority for those artifacts' marker form, required semantic fields, tuple and digest bindings, and active-lineage rules. It does not decide acceptance, classify durable context, authorize a mutation, choose a transition, merge a Pull Request, or close an Issue. The producing phase reference owns those actions. `delivery` uses this contract only to validate independently re-read evidence and reconstruct the next bounded action.

This contract describes only the current artifact formats. Persistent artifacts from the v1 line are not read, interpreted, or migrated by this version. See `../MIGRATION.md` for the compatibility break.

## Apply the contract

- Resolve `${marker_namespace}` from the validated project-owned Harness configuration before producing or searching for a marker.
- Treat every fenced payload below as the exact field set and field order for a new artifact of that kind. Do not omit, rename, or add workflow-semantic fields without a separately approved versioned migration.
- Normalize and SHA-256 digest the whole Markdown comment, including any marker. A URL/digest pair always identifies that whole independently read comment, never an extracted YAML subtree.
- Require every populated `*_url` field that has a matching `*_sha256` field to be paired with it. Both are null or both are non-null.
- Bind all repeated Issue, product-PR, memory-PR, head, base, title, Body-digest, changed-file, and merge identities to the same independently read source tuple. Fail closed on drift or contradiction.
- Require the Issue and Pull Request transports to return the same verified authenticated actor record for the operation. Establish its `mutation_author_login` as the trusted workflow author; every artifact below must be authored by it.
- A phase result or hand-off is only a search hint, never mutation authority. A consumer must fetch and validate the original artifact under this contract before relying on it. The sole no-artifact exception is a `context-promotion` result with `reason: direct-no-promotion-all-no-write`: an ephemeral classification judgment that supports only the current `delivery` immediate closure gate. Immediately before closure, revalidate that classification and the complete absence of any promotion state or source-linked project-memory PR; after any re-entry, classify again.
- Accept only complete, exact, single-tip lineages. Ambiguity, drift, multiple active tips, or an unreadable artifact is `blocked`, never a pick-latest decision.

## Persist review evidence

### Review verdict

Write one complete append-only top-level product-PR comment for each review round:

~~~yaml
verdict: PASS | FAIL | BLOCKED
issue_url: URL
issue_body_sha256: SHA256
pr_url: URL
pr_title: TITLE
pr_body_sha256: SHA256
head_ref: BRANCH
head_sha: COMMIT
base_ref: develop
base_sha: COMMIT
review:
  - item: issue-scope | unit-tests | durable-memory-impact
    result: PASS | FAIL | BLOCKED
    evidence: COMMAND, OUTPUT, OR SOURCE
required_checks_known: true | false
return_stage: null | implementation | spec
blockers: []
~~~

- `issue-scope` PASS requires the complete final diff to stay inside the Issue `改动范围`, with every protected change matching an exact Issue `受保护改动` exception.
- `unit-tests` PASS requires the changed-code unit tests to pass against the exact current head, with `required_checks_known: true`. A successful required CI run bound to the exact current head may serve as the evidence; never reuse an old-head result.
- `durable-memory-impact` PASS with `evidence: all-five-none` requires each of the five Product PR rows to be exactly `无`, independently confirmed against the complete diff, Issue, and authority sources. A real candidate uses a factual evidence note instead of `无`.
- Authorize the merge path only on `verdict: PASS` with all three items PASS, `required_checks_known: true`, `return_stage: null`, and an empty `blockers` collection. Route `return_stage: implementation` for an implementation defect and `return_stage: spec` for a delivery-contract defect. A BLOCKED record is evidence of a stop, never success.

### Code-only admission

Admit a newly merged product delivery directly as code-only only when all of the following are independently established for one exact accepted product tuple:

- the Product PR Body contains the five required `持久项目记忆实际影响` rows—`decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, and `milestone_evidence`—exactly once and in contract order, and every row's `实际影响` value is exactly the literal `无`;
- the current review `verdict: PASS` record contains the durable-memory entry with `item: durable-memory-impact`, `result: PASS`, and `evidence: all-five-none`;
- complete source-PR comment and related-PR reads prove that no `context-promotion` marker, proposal artifact, confirmation, terminal callback, or source-linked project-memory PR exists; and
- the accepted diff, tests, Issue contract, and cited authority contain no durable-memory candidate that contradicts the five exact `无` claims.

This admission is a derived read-time gate, not a marker or a new persistent artifact. Fail closed when any row, review item, tuple binding, absence read, or factual check is missing or ambiguous; enter the `context-promotion` classification path instead.

## Persist Context Promotion evidence

### Promotion marker

Use this marker for every promotion-state callback below:

~~~text
<!-- ${marker_namespace}:context-promotion source-pr=456 source-head=COMMIT -->
~~~

The marker's product-PR number and source head must equal the callback payload and the current merged source tuple.

### Proposal artifact

Write one top-level source product-PR comment without a workflow marker:

~~~yaml
artifact_kind: context-promotion-proposal
artifact_schema_version: 2
revision: 1
issue_url: URL
issue_body_sha256: SHA256
source_pr_url: URL
source_pr_title: TITLE
source_pr_body_sha256: SHA256
source_head_ref: BRANCH
source_head_sha: COMMIT
source_merge_commit_sha: COMMIT
authority_base_sha: COMMIT
revises_artifact_url: null
revises_artifact_sha256: null
proposal:
  - id: CONTEXT-1
    action: add | update | supersede | no_write
    classification: decision | stable_rule | wiki_knowledge | stable_context | milestone_evidence | no_write
    destination: path | null
    exact_update: TEXT | null
    evidence:
      - source: URL_OR_PATH
        sha256: SHA256
    existing_authority:
      source: URL_OR_PATH | null
      sha256: SHA256 | null
      statement: TEXT | null
      conflict_or_duplication: TEXT
    omission_risk_or_no_write_reason: TEXT
memory_pr_url: URL | null
memory_pr_title: TITLE | null
memory_pr_body_sha256: SHA256 | null
memory_head_ref: BRANCH | null
memory_head_sha: COMMIT | null
memory_base_ref: develop | null
memory_base_sha: COMMIT | null
changed_files:
  - path: PATH
    status: added | modified | removed | renamed
    previous_path: PATH | null
    blob_sha: SHA | null
validation: []
~~~

For a first proposal, `revision: 1` and both `revises_artifact_*` fields are null. A user revision increments `revision`, binds the preceding whole artifact comment through both fields, and updates the same Draft project-memory PR in place rather than opening another.

For a write proposal, require the complete memory-PR tuple, non-empty exact sorted `changed_files`, and `authority_base_sha == memory_base_sha`. Every proposed conclusion and destination must equal the Draft project-memory PR Body and diff. List all five durable categories; give each `no_write` item an explicit category-specific reason. Every `validation` entry binds a command to the exact current memory head; never carry forward an old-head validation result.

### Awaiting-confirmation callback

Write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
outcome: awaiting-confirmation
revision: 1
issue_url: URL
issue_body_sha256: SHA256
source_pr_url: URL
source_pr_title: TITLE
source_pr_body_sha256: SHA256
source_head_ref: BRANCH
source_head_sha: COMMIT
source_merge_commit_sha: COMMIT
previous_comment_url: URL | null
previous_comment_sha256: SHA256 | null
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
memory_pr_url: URL | null
memory_pr_title: TITLE | null
memory_pr_body_sha256: SHA256 | null
memory_head_ref: BRANCH | null
memory_head_sha: COMMIT | null
memory_base_ref: develop | null
memory_base_sha: COMMIT | null
changed_files: []
~~~

For an initial proposal, `revision: 1` and both predecessor fields are null. A revised proposal increments `revision` and binds the superseded active `awaiting-confirmation` whole comment through `previous_comment_*`. For a write proposal the complete memory tuple is non-null; for an all-`no_write` revision the memory tuple and `changed_files` are null/empty. The proposal, source tuple, memory tuple, and changed files must match the independently read artifacts.

### Confirmed callback

After one current explicit source-bound approval re-entry, write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
outcome: confirmed
previous_comment_url: PROPOSAL_URL
previous_comment_sha256: PROPOSAL_SHA256
decision: approved
confirmed_revision: 1
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
memory_pr_url: URL | null
memory_pr_title: TITLE | null
memory_pr_body_sha256: SHA256 | null
memory_head_ref: BRANCH | null
memory_head_sha: COMMIT | null
memory_base_ref: develop | null
memory_base_sha: COMMIT | null
changed_files: []
~~~

`previous_comment_*` must bind the active `awaiting-confirmation` whole comment and `confirmed_revision` must equal its revision. Every evidence pair and tuple must equal the displayed proposal state and proposal artifact.

Only the current user's explicit proposal-bound confirmation re-entry may authorize a confirmation. Re-read the sole active `awaiting-confirmation` whole comment and require its URL/digest to equal the decision binding before writing. A bare reply, stale binding, existing comment, or prior invocation is insufficient; silence, timeout, or general delivery intent cannot authorize it.

### Memory-PR-merged terminal

After the guarded memory merge and its independent read-back, write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
outcome: memory-pr-merged
previous_comment_url: CONFIRMED_URL
previous_comment_sha256: CONFIRMED_SHA256
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
merge_commit_sha: COMMIT
changed_files: []
~~~

The predecessor must be the active `confirmed` callback; the memory tuple and merge identity must equal the transport-verified merge read-back.

### No-promotion terminal

When a user revision turns every proposal item into `no_write`, the confirmed lineage ends with one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
outcome: no-promotion
previous_comment_url: CONFIRMATION_URL
previous_comment_sha256: CONFIRMATION_SHA256
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
category_reasons: []
~~~

Require complete five-category reasons. A first-round all-`no_write` classification persists nothing at all; see the ephemeral exception in "Apply the contract".

## Validate the active lineage

- The active lineage is the revision chain of proposal artifacts plus their marker callbacks bound to one exact source tuple. The active tip is the latest callback of the latest revision.
- Require exactly one active tip. Multiple tips, a broken predecessor chain, unreadable digests, or tuple drift is `blocked`.
- A lineage that already has an `awaiting-confirmation`, `confirmed`, `memory-pr-merged`, or `no-promotion` callback in the current format resumes at that exact state; never restart classification over persisted state, and never use the code-only fast path to bypass it.
