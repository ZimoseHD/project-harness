# Delivery Evidence Contract

Load this shared contract only when the selected operation produces or consumes the persistent Closeout and Context Promotion evidence defined here.

This file is the single authority for those artifacts' marker forms, required semantic fields, tuple and digest bindings, predecessor relationships, active-tip rules, and legacy dual-read rules. It does not decide acceptance, classify durable context, authorize a mutation, choose a transition, merge a Pull Request, or close an Issue. The producing phase reference owns those actions. The `delivery` coordinator may use this contract only to validate independently re-read evidence and reconstruct the next bounded action.

## Apply the contract

- Resolve `${marker_namespace}` from the validated project-owned Harness configuration before producing or searching for a marker.
- Treat every fenced payload below as the exact field set and field order for a new artifact of that kind. Do not omit, rename, or add workflow-semantic fields without a separately approved versioned migration.
- Normalize and SHA-256 digest the whole Markdown comment, including any marker. A URL/digest pair always identifies that whole independently read comment, never an extracted YAML subtree.
- Require every populated `*_url` field that has a matching `*_sha256` field to be paired with it. Both are null or both are non-null unless one exact legacy rule below says that a digest is computed during the current read.
- Bind all repeated Issue, product-PR, memory-PR, head, base, title, Body-digest, changed-file, authority-base, and merge identities to the same independently read source tuple. Fail closed on drift or contradiction.
- Require the Issue and Pull Request transports to return the same verified authenticated actor record for the operation. Establish its `mutation_author_login` as the trusted workflow author; a marker or arbitrary matching comment cannot establish trust.
- For a current-format lineage, require the Closeout PASS, Issue callback, schema-v2 eligibility registration, and every schema-v2 promotion callback's transport-returned author login to equal the trusted workflow author. Apply only the explicit legacy migration rules below when historical authorship differs.
- A phase result or hand-off is only a search hint. A consumer must fetch and validate the original artifact under this contract before relying on it.
- An operation-local Evidence Bundle is a non-persistent, non-authoritative optimization defined by the root Skill. It may carry exact normalized artifact content between the current coordinator, Owner, and Reviewer, but it does not authorize a transition or replace the live artifact, active-lineage, mutation, merge, or closure checks required here.
- Treat each Context Promotion artifact named **Reviewer PASS** as persistent evidence of an independent Reviewer's returned, tuple-bound read-only verdict. The Reviewer never writes that GitHub comment: the Context Promotion Phase Owner is its producer, composes it from the returned verdict and exact independently read tuple, persists it through the loaded Pull Request transport, and verifies the read-back. This ownership clarification does not change any artifact field, author rule, digest, predecessor, or schema below.

## Persist Closeout evidence

### Acceptance verdict

Write one complete append-only top-level product-PR comment for each acceptance snapshot:

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

Require `verdict: PASS`, `required_checks_known: true`, no failed or blocked acceptance item, `return_stage: null`, and an empty `blockers` collection before the record can authorize the successful Closeout evidence below. Require `return_stage: Implementation` for an implementation defect and `return_stage: Definition` for a delivery-contract defect. A BLOCKED record is evidence of a stop, never success.

### Product acceptance Issue callback

After a valid PASS, write one lightweight source-Issue callback:

~~~yaml
callback: product-acceptance-pass
pr_url: URL
pr_title: TITLE
pr_body_sha256: SHA256
head_ref: BRANCH
head_sha: COMMIT
base_ref: develop
base_sha: COMMIT
acceptance_comment_url: URL
acceptance_comment_sha256: SHA256
~~~

The callback tuple must equal the PASS tuple, and `acceptance_comment_*` must bind that exact whole PASS comment.

### Current eligibility registration

Write one top-level product-PR comment containing the marker and payload:

~~~text
<!-- ${marker_namespace}:context-promotion-eligible source-pr=456 source-head=COMMIT -->
schema_version: 2
state: awaiting-merge
issue_url: URL
issue_body_sha256: SHA256
pr_title: TITLE
pr_body_sha256: SHA256
head_ref: BRANCH
head_sha: COMMIT
base_ref: develop
base_sha: COMMIT
acceptance_comment_url: URL
acceptance_comment_sha256: SHA256
issue_callback_url: URL
issue_callback_sha256: SHA256
previous_registration_url: null
previous_registration_sha256: null
supersedes_legacy_registration_url: null
supersedes_legacy_registration_sha256: null
~~~

The marker's product-PR number and source head must equal the payload and current product-PR tuple. The Issue/PR/head/base fields must equal the PASS and Issue callback. The acceptance and Issue-callback pairs must bind those exact whole comments.

For the first current registration, both predecessor pairs are null. For a same-head schema-v2 successor, `previous_registration_*` binds the preceding active registration and both legacy alias fields are null. For the sole permitted legacy upgrade, both `previous_registration_*` and `supersedes_legacy_registration_*` bind the same exact unversioned predecessor URL/digest. No other predecessor shape is valid.

### Legacy eligibility registration

The pre-schema-v2 Closeout producer persisted this exact legacy eligibility semantic minimum:

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

Dual-read this unversioned form only when it was present in the first immutable read baseline and its marker, source head, Issue/PR digests, base tuple, linked historical PASS, and one matching historical Issue callback are independently verified. Read and digest each whole comment now. Do not require the old payload to contain source title, acceptance-comment digest, Issue-callback URL/digest, or required-check knowledge that its producer never wrote.

An unmerged product PR must pass a fresh Closeout and receive exactly one schema-v2 eligibility successor bound to the legacy URL/digest before `delivery` may merge it. For an already merged historical product PR, Context Promotion may use the verified legacy lineage only as evidence for the schema-v2 confirmation migration below.

## Persist Context Promotion evidence

### Promotion marker

Use this unchanged marker for every schema-v2 proposal-state, confirmation, Ready, and terminal callback:

~~~text
<!-- ${marker_namespace}:context-promotion source-pr=456 source-head=COMMIT -->
~~~

The marker's product-PR number and source head must equal the callback and the current merged source tuple.

### Proposal artifact

Before independent review, write one top-level source product-PR comment without a workflow marker:

~~~yaml
artifact_kind: context-promotion-proposal
artifact_schema_version: 1
revision: 1
issue_url: URL
issue_body_sha256: SHA256
source_pr_url: URL
source_pr_title: TITLE
source_pr_body_sha256: SHA256
source_head_ref: BRANCH
source_head_sha: COMMIT
source_merge_commit_sha: COMMIT
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
authority_base_sha: COMMIT
revises_artifact_url: null
revises_artifact_sha256: null
legacy_evidence_url: null
legacy_evidence_sha256: null
supersedes_memory_pr_url: null
supersedes_memory_pr_title: null
supersedes_memory_pr_body_sha256: null
supersedes_memory_head_ref: null
supersedes_memory_head_sha: null
supersedes_memory_base_ref: null
supersedes_memory_base_sha: null
supersedes_memory_reason: null
proposal:
  - id: CONTEXT-1
    action: add | update | supersede | no_write
    classification: decision | stable_rule | wiki_knowledge | stable_context | milestone_evidence | no_write
    destination: path | null
    exact_update: TEXT | null
    confirmation_requirement: source-confirmed | explicit-user-decision
    integration_authority_effect: TEXT | null
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
changed_paths: []
changed_files:
  - path: PATH
    status: added | modified | removed | renamed
    previous_path: PATH | null
    blob_sha: SHA | null
diff_summary: []
validation: []
~~~

For a first proposal, `revision: 1` and both `revises_artifact_*` fields are null. A revision increments `revision` and binds the preceding whole artifact comment through both fields.

For a write, require the complete memory-PR tuple, non-empty exact sorted `changed_files`, a `changed_paths` compatibility view equal to those paths, and `authority_base_sha == memory_base_sha`. Every proposed conclusion and destination must equal the Draft project-memory PR Body and diff. For a deletion, the exact head/base tuple plus path/status identifies the removed base blob.

For no-write, require all five durable categories with explicit category-specific reasons, all memory-PR fields null, and both changed-file collections empty. A legacy migration must populate `legacy_evidence_*`; an artifact that supersedes a memory PR must populate every `supersedes_memory_*` field.

### Context Promotion validation-impact artifact

After an advanced-base assessment selects `reuse` or `incremental`, have the Context Promotion Phase Owner write one append-only Draft project-memory-PR comment without a workflow marker:

~~~yaml
artifact_kind: context-promotion-validation-impact
artifact_schema_version: 1
issue_url: URL
source_pr_url: URL
memory_pr_url: URL
prior_proposal_artifact_url: URL
prior_proposal_artifact_sha256: SHA256
prior_reviewer_pass_url: URL
prior_reviewer_pass_sha256: SHA256
prior_head_sha: COMMIT
prior_base_sha: COMMIT
current_head_sha: COMMIT
current_base_sha: COMMIT
base_relation: fast-forward
current_base_is_head_ancestor: true
base_delta:
  complete: true
  truncated: false
  files:
    - status: added | modified | removed | renamed
      old_path: PATH | null
      new_path: PATH | null
      old_blob_sha: SHA | null
      new_blob_sha: SHA | null
prior_promotion_patch:
  complete: true
  truncated: false
  files:
    - status: added | modified | removed | renamed
      old_path: PATH | null
      new_path: PATH | null
      old_blob_sha: SHA | null
      new_blob_sha: SHA | null
current_promotion_patch:
  complete: true
  truncated: false
  files:
    - status: added | modified | removed | renamed
      old_path: PATH | null
      new_path: PATH | null
      old_blob_sha: SHA | null
      new_blob_sha: SHA | null
prior_promotion_patch_sha256: SHA256
current_promotion_patch_sha256: SHA256
validation_inventory_complete: true
validation_inventory:
  - id: VALIDATION-ID
    dependency_paths: []
    global: false
validation_inventory_sha256: SHA256
global_trigger_paths_complete: true
global_trigger_paths: []
impact_input_sha256: SHA256
impact_mode: reuse | incremental
invalidated_validation_ids: []
retained_validation:
  - id: VALIDATION-ID
    prior_evidence_url: URL
    prior_evidence_sha256: SHA256
    reason: TEXT
executed_validation:
  - id: VALIDATION-ID
    command: COMMAND
    result: PASS
    evidence: OUTPUT_OR_URL
reason_codes: []
final_ci_gate:
  policy: exact-current-head
  reuse_allowed: false
~~~

Require the prior pairs to bind the exact preceding proposal and versioned or legacy Reviewer PASS. Require a complete fast-forward base delta, exact current-base ancestry, complete changed-file/blob identities, and a deterministic `impact_input_sha256` returned by `scripts/validation_impact.py`. Persist both complete non-truncated base-to-head promotion-patch record sets. Derive each promotion-patch digest with `promotion_patch_sha256`: validate the exact five-field changed-file identities; sort by `(status, old_path-or-empty, new_path-or-empty, old_blob_sha-or-empty, new_blob_sha-or-empty)`; hash UTF-8 canonical JSON containing `complete: true`, `truncated: false`, and those sorted records. Never accept a caller-supplied opaque digest that does not reproduce from the displayed records. Calculate `validation_inventory_sha256` over the exact displayed inventory using UTF-8 canonical JSON with sorted keys, compact separators, and no ASCII escaping. Require the validation inventory and global-trigger-path inventory to be explicitly complete. Require the patch records/digests, inventory/digest, delta, global-trigger completeness/list, and every other helper input to reproduce `impact_input_sha256`. Require the two derived promotion-patch digests to be equal for `reuse` or `incremental`.

Require `impact_mode`, `invalidated_validation_ids`, `reason_codes`, and the retained ID set to equal the helper result exactly. Require unique IDs and require the validation-inventory IDs to equal the disjoint union of retained-validation IDs and executed-validation IDs. The executed-validation IDs must equal the helper's invalidated IDs. For `reuse`, both invalidated and executed lists are empty; require at least one exact retained-validation pair when reusable local validation existed. For `incremental`, require one passing current execution for every invalidated ID and retain every unaffected ID. Every retained pair must bind a whole persistent evidence comment that recorded the prior passing execution; chat, tool output, a Delivery observation, or an uncommitted result is invalid.

Normalize, add, and independently read this complete comment back through the Pull Request transport. Its URL and whole-comment digest are the validation-impact identity. Copy the helper's `input_sha256` result exactly into `impact_input_sha256`. Keep the existing Proposal artifact schema-v1 `validation` item shape unchanged; it continues to contain only current executed command/result/evidence records. Require the versioned Reviewer PASS to bind the exact validation-impact URL/digest pair and to repeat exactly the successor proposal's current executed-validation records. The awaiting-confirmation callback binds that PASS transitively through its unchanged Reviewer PASS pair. The impact artifact is evidence only and never a workflow marker, active tip, confirmation, required-check result, merge permission, or Delivery observation.

Do not persist this success artifact for a helper result of `full` or `blocked`. Run the required current validation for `full`; stop for `blocked`. An old lineage without this artifact, a malformed current artifact, incomplete dependency inventory, unknown helper schema, or mismatched URL/digest uses the old lineage full-validation fallback and never silently reuses local validation. The exact current head required CI is never reused, regardless of this artifact.

### Context Promotion canonical review input

Before dispatching a fresh Reviewer, build this exact ephemeral manifest. It is not a comment, marker, callback, Delivery observation, or recovery artifact:

~~~yaml
review_input_schema_version: 1
review_policy_version: 1
review_kind: context-promotion-no-write | context-promotion-write
effective_review_tier: r0-no-write | r1-documentary | r2-stable-context | r3-normative
reviewed_items:
  - id: CONTEXT-1
    tier: r0-no-write | r1-documentary | r2-stable-context | r3-normative
source:
  issue_url: URL
  issue_body_sha256: SHA256
  source_pr_url: URL
  source_pr_title: TITLE
  source_pr_body_sha256: SHA256
  source_head_ref: BRANCH
  source_head_sha: COMMIT
  source_merge_commit_sha: COMMIT
eligibility:
  url: URL
  sha256: SHA256
proposal:
  url: URL
  sha256: SHA256
memory:
  url: URL
  title: TITLE
  body_sha256: SHA256
  head_ref: BRANCH
  head_sha: COMMIT
  base_ref: develop
  base_sha: COMMIT
changed_files:
  - path: PATH
    status: added | modified | removed | renamed
    previous_path: PATH | null
    blob_sha: SHA | null
validation_impact:
  url: URL
  sha256: SHA256
executed_validation:
  - command: COMMAND
    result: PASS
    evidence: OUTPUT_OR_URL
~~~

For `context-promotion-no-write`, require `memory: null`, `changed_files: []`, and `validation_impact: null`. For a write, require the complete memory tuple and non-empty changed files; the impact pair remains nullable. Require exact keys and no extras. Sort reviewed items by ID, changed files by `(path, status, previous_path-or-empty, blob_sha-or-empty)`, and executed validation by `(command, result, evidence)`.

Use `scripts/context_review_input.py` to validate and canonicalize this object and calculate `review_input_sha256` over UTF-8 JSON with sorted keys, compact separators, and no ASCII escaping. Every field is recoverable from the versioned PASS plus its exact proposal/eligibility/current-source references; do not include operation-local payload IDs, aggregate search/comment snapshots, Bundle content digests, unified-diff digests, liveness fields, or the Bundle container digest. The Reviewer and Owner must calculate the same persistent digest. The Reviewer separately returns the ephemeral `consumed_bundle_sha256` so the same Owner can prove that the reviewed raw bytes and exact diff came from its current Bundle; never persist that Bundle digest or use it for later recovery.

### Reviewer PASS for no-write

After the independent Reviewer returns a tuple-bound read-only PASS, have the Context Promotion Phase Owner write one top-level source product-PR evidence comment without a workflow marker:

~~~yaml
review_schema_version: 1
review_policy_version: 1
review_kind: context-promotion-no-write
verdict: PASS
effective_review_tier: r0-no-write | r1-documentary | r2-stable-context | r3-normative
review_input_sha256: SHA256
issue_body_sha256: SHA256
source_pr_body_sha256: SHA256
source_head_ref: BRANCH
source_head_sha: COMMIT
source_merge_commit_sha: COMMIT
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
reviewed_items:
  - id: CONTEXT-1
    tier: r0-no-write | r1-documentary | r2-stable-context | r3-normative
    result: PASS
validation_impact_url: null
validation_impact_sha256: null
category_results: []
~~~

The source tuple and eligibility pair must equal the artifact, and the proposal pair must bind that exact whole artifact comment. Require the complete five-category review result, exact proposal item coverage, and an effective tier equal to the maximum calculated by the phase. A no-write PASS cannot bind a validation-impact artifact.

### Reviewer PASS for a write

After the independent Reviewer returns a tuple-bound read-only PASS, have the Context Promotion Phase Owner write one append-only Draft project-memory-PR comment:

~~~yaml
review_schema_version: 1
review_policy_version: 1
review_kind: context-promotion-write
verdict: PASS
effective_review_tier: r1-documentary | r2-stable-context | r3-normative
review_input_sha256: SHA256
issue_url: URL
issue_body_sha256: SHA256
source_pr_url: URL
source_pr_title: TITLE
source_pr_body_sha256: SHA256
source_head_ref: BRANCH
source_head_sha: COMMIT
source_merge_commit_sha: COMMIT
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
changed_files:
  - path: PATH
    status: added | modified | removed | renamed
    previous_path: PATH | null
    blob_sha: SHA | null
reviewed_items:
  - id: CONTEXT-1
    tier: r0-no-write | r1-documentary | r2-stable-context | r3-normative
    result: PASS
validation_impact_url: URL | null
validation_impact_sha256: SHA256 | null
validation:
  - command: COMMAND
    result: PASS
    evidence: OUTPUT_OR_URL
~~~

Require the source, eligibility, artifact, memory-PR, and changed-file identities to equal the exact proposal and transport reads. `changed_files` is sorted and exact. Require `reviewed_items` to cover every proposal item exactly once with its calculated tier and require `effective_review_tier` to equal their maximum plus every global escalation. Every validation entry represents an executed passing check and must equal the Proposal artifact's executed-validation records exactly. Populate the validation-impact pair only for an exact independently read current artifact; both fields are null otherwise. When non-null, its `executed_validation` records must also equal the subset it identifies as invalidated and executed for this tuple. Any PR, tuple, diff, executed validation, impact artifact, or semantic review-input change invalidates this PASS.

Require `review_input_sha256` to equal the exact **Context Promotion canonical review input** helper result. The ephemeral Reviewer returns this digest plus `consumed_bundle_sha256`; the Context Promotion Phase Owner must require the latter to equal its current same-round Bundle, recompute the persistent semantic review-input digest, and persist only `review_input_sha256`. Later recovery rebuilds that digest from persistent artifacts and immutable semantic source identities, never from a historical Bundle.

Dual-read an already persisted unversioned Reviewer PASS only when it has exactly the former field set for its `review_kind`, all existing tuple/digest/validation/category rules pass, and no `review_schema_version` field is present. Define that exact historical field set as the corresponding current fenced form after removing only `review_schema_version`, `review_policy_version`, `effective_review_tier`, `review_input_sha256`, `reviewed_items`, `validation_impact_url`, and `validation_impact_sha256`; retain every other field and order shown. Treat that record as `legacy-full`, semantically equivalent to `r3-normative`; do not rewrite or downgrade it. New review writes always use the versioned form. A record declaring `review_schema_version: 1` or `review_policy_version: 1` but omitting or mismatching any required tier, item, digest, or impact field is malformed current evidence, never an unversioned legacy PASS.

### Awaiting-confirmation callback

Write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
schema_version: 2
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
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
authority_base_sha: COMMIT
previous_comment_url: URL | null
previous_comment_sha256: SHA256 | null
proposal_kind: write | no-write | legacy-reconciliation
revision_reason: initial | user-modification | promotion-scope-repair | legacy-reconciliation | legacy-reassessment
proposal_artifact_url: URL
proposal_artifact_sha256: SHA256
legacy_evidence_url: URL | null
legacy_evidence_sha256: SHA256 | null
supersedes_memory_pr_url: URL | null
supersedes_memory_pr_title: TITLE | null
supersedes_memory_pr_body_sha256: SHA256 | null
supersedes_memory_head_ref: BRANCH | null
supersedes_memory_head_sha: COMMIT | null
supersedes_memory_base_ref: develop | null
supersedes_memory_base_sha: COMMIT | null
supersedes_memory_reason: TEXT | null
supersession_comment_url: URL | null
supersession_comment_sha256: SHA256 | null
invalidates_confirmation_url: URL | null
invalidates_confirmation_sha256: SHA256 | null
invalidates_ready_url: URL | null
invalidates_ready_sha256: SHA256 | null
memory_pr_url: URL | null
memory_pr_title: TITLE | null
memory_pr_body_sha256: SHA256 | null
memory_head_ref: BRANCH | null
memory_head_sha: COMMIT | null
memory_base_ref: develop | null
memory_base_sha: COMMIT | null
changed_files: []
reviewer_result: PASS
reviewer_pass_url: URL
reviewer_pass_sha256: SHA256
~~~

For a normal initial proposal, predecessor, legacy-evidence, supersession, and invalidation pairs are null. For an initial closure-only legacy reconciliation, `previous_comment_*` and `legacy_evidence_*` both bind the exact legacy callback, `proposal_kind: legacy-reconciliation`, and `revision_reason: legacy-reconciliation`. A first-state write that supersedes legacy `no-promotion` uses `proposal_kind: write`, `revision_reason: legacy-reassessment`, and those same two equal legacy pairs.

For a user revision or promotion-scope repair, `previous_comment_*` binds the active superseded schema-v2 tip. A user revision may supersede only an unconfirmed proposal and leaves all invalidation pairs null. A repair from a confirmed tip populates `invalidates_confirmation_*`; a repair from a Ready tip also populates `invalidates_ready_*`. A branch retaining legacy evidence keeps its exact legacy pair unchanged.

The proposal, review, eligibility, authority base, source tuple, memory tuple, and changed files must match the independently read artifacts. For a new proposal, require the exact versioned Reviewer PASS, its computed tier/item coverage, and any bound validation-impact artifact. Continue an unchanged historical lineage with one exact `legacy-full` PASS only under its dual-read rules. For a write, the complete memory tuple is non-null and `authority_base_sha == memory_base_sha`. For no-write, the memory tuple and changed files are null/empty.

### Confirmed callback

After one current explicit source-bound approval re-entry, write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
schema_version: 2
outcome: confirmed
previous_comment_url: PROPOSAL_URL
previous_comment_sha256: PROPOSAL_SHA256
decision: approved
confirmed_revision: 1
proposal_kind: write | no-write | legacy-reconciliation
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
reviewer_pass_url: REVIEW_URL
reviewer_pass_sha256: REVIEW_SHA256
eligibility_registration_url: ELIGIBILITY_URL
eligibility_registration_sha256: ELIGIBILITY_SHA256
authority_base_sha: COMMIT
memory_pr_url: URL | null
memory_pr_title: TITLE | null
memory_pr_body_sha256: SHA256 | null
memory_head_ref: BRANCH | null
memory_head_sha: COMMIT | null
memory_base_ref: develop | null
memory_base_sha: COMMIT | null
changed_files: []
~~~

`previous_comment_*` must bind the active `awaiting-confirmation` whole comment, `confirmed_revision` must equal its revision, and `proposal_kind` must equal it. Every evidence pair and tuple must equal the displayed proposal state and proposal artifact. Whenever that artifact includes a project-memory PR, every memory field and `changed_files` entry is required and exact; otherwise all are null/empty.

Only the current user's explicit proposal-bound confirmation re-entry may authorize creation of a confirmation. Under `delivery`, require the host-provenance-bound `user_decision` derived from the current exact `role: delivery` invocation; standalone requires the same fields in the current exact `role: context-promotion` invocation. Re-read the sole active `awaiting-confirmation` whole comment and require its URL/digest to equal that decision before writing. A stored or relayed packet cannot authorize confirmation by itself. Without current host parent-child provenance and independent re-read, a bare reply, existing comment, or prior invocation is insufficient; silence, timeout, or general delivery intent cannot authorize it.

### No-promotion terminal

Write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
schema_version: 2
outcome: no-promotion
previous_comment_url: CONFIRMATION_URL
previous_comment_sha256: CONFIRMATION_SHA256
proposal_comment_url: PROPOSAL_URL
proposal_comment_sha256: PROPOSAL_SHA256
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
authority_base_sha: COMMIT
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
reviewer_pass_url: REVIEW_URL
reviewer_pass_sha256: REVIEW_SHA256
category_reasons: []
~~~

The predecessor must be the active confirmed all-`no_write` proposal. Require complete five-category reasons, no memory PR, and exact confirmation, proposal-state, eligibility, artifact, review, and authority-base bindings.

### Memory-PR-ready callback

For a normal confirmed write, write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
schema_version: 2
outcome: memory-pr-ready
previous_comment_url: CONFIRMATION_URL
previous_comment_sha256: CONFIRMATION_SHA256
proposal_comment_url: PROPOSAL_URL
proposal_comment_sha256: PROPOSAL_SHA256
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
authority_base_sha: COMMIT
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
changed_files: []
reviewer_pass_url: URL
reviewer_pass_sha256: SHA256
~~~

For an exact unmerged legacy `memory-pr-ready` that has undergone current review and confirmation, use this migration variant:

~~~yaml
schema_version: 2
outcome: memory-pr-ready
migration: confirmed-legacy-ready
previous_comment_url: CONFIRMATION_URL
previous_comment_sha256: CONFIRMATION_SHA256
proposal_comment_url: PROPOSAL_URL
proposal_comment_sha256: PROPOSAL_SHA256
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
legacy_evidence_url: LEGACY_CALLBACK_URL
legacy_evidence_sha256: LEGACY_CALLBACK_SHA256
authority_base_sha: COMMIT
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
changed_files: []
reviewer_pass_url: URL
reviewer_pass_sha256: SHA256
~~~

Require an exact Ready project-memory PR and exact confirmation, proposal-state, eligibility, artifact, review, authority-base, title/Body/head/base, and sorted changed-file bindings. A migrated callback additionally binds the exact legacy evidence and authorizes only the unchanged historical Ready tuple.

### Memory-PR-merged terminal

After the exact current-format project-memory PR is independently verified merged, write one top-level source product-PR comment containing the promotion marker and payload:

~~~yaml
schema_version: 2
outcome: memory-pr-merged
previous_comment_url: MEMORY_READY_URL
previous_comment_sha256: MEMORY_READY_SHA256
proposal_comment_url: PROPOSAL_URL
proposal_comment_sha256: PROPOSAL_SHA256
confirmation_comment_url: CONFIRMATION_URL
confirmation_comment_sha256: CONFIRMATION_SHA256
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
authority_base_sha: COMMIT
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
changed_files: []
memory_merge_commit_sha: COMMIT
reviewer_pass_url: URL
reviewer_pass_sha256: SHA256
~~~

For an exact legacy `memory-pr-ready` whose linked project-memory PR had already merged before schema v2, use this migration variant after current reconstruction, review, and confirmation:

~~~yaml
schema_version: 2
outcome: memory-pr-merged
migration: confirmed-legacy-already-merged
previous_comment_url: CONFIRMATION_URL
previous_comment_sha256: CONFIRMATION_SHA256
eligibility_registration_url: URL
eligibility_registration_sha256: SHA256
legacy_evidence_url: LEGACY_CALLBACK_URL
legacy_evidence_sha256: LEGACY_CALLBACK_SHA256
authority_base_sha: COMMIT
proposal_comment_url: PROPOSAL_URL
proposal_comment_sha256: PROPOSAL_SHA256
proposal_artifact_url: ARTIFACT_URL
proposal_artifact_sha256: ARTIFACT_SHA256
confirmation_comment_url: CONFIRMATION_URL
confirmation_comment_sha256: CONFIRMATION_SHA256
memory_pr_url: URL
memory_pr_title: TITLE
memory_pr_body_sha256: SHA256
memory_head_ref: BRANCH
memory_head_sha: COMMIT
memory_base_ref: develop
memory_base_sha: COMMIT
changed_files: []
memory_merge_commit_sha: COMMIT
reviewer_pass_url: URL
reviewer_pass_sha256: SHA256
~~~

For a normal terminal, the predecessor must bind the active `memory-pr-ready`. For the historical already-merged migration, it binds the active migration confirmation and the legacy pair binds the old Ready callback. In both cases require the exact confirmed/reviewed memory tuple and changed files, non-Draft merge into `develop`, current merge identity, an allowed actual merge method, transport-verified merge provenance, `required_checks_known: true`, and every required check successful for the exact head.

## Validate active lineages

### Eligibility lineage

- Resolve schema-v2 eligibility comments as one append-only predecessor chain per exact product PR and source head.
- Require exactly one reachable, non-superseded active registration URL/digest pair. Historical registrations are audit evidence and cannot authorize merge or promotion.
- A same-head successor must bind the preceding whole comment through `previous_registration_*`. A first schema-v2 successor may bind one unversioned predecessor only when its generic predecessor pair and legacy alias pair are equal.
- Require the active registration to bind the current Issue digest, source PR title/Body digest, head/base tuple, Closeout PASS, and Issue callback.
- Stop on missing links, cycles, multiple active tips, multiple legacy predecessors/successors, tuple drift, or untrusted authorship.

### Promotion lineage

- Require `schema_version: 2` on every new workflow callback.
- Permit the normal chains `awaiting-confirmation` → `confirmed` → `no-promotion` and `awaiting-confirmation` → `confirmed` → `memory-pr-ready` → `memory-pr-merged`.
- Permit a higher-revision `awaiting-confirmation` to supersede an unconfirmed proposal through its predecessor pair.
- Permit a promotion-scope repair from an active `confirmed` or `memory-pr-ready` tip only when the new `awaiting-confirmation` callback binds that tip, binds the new artifact/review, and populates the required invalidation pairs. The invalidated older branch cannot authorize merge or closure.
- Permit the explicit legacy migration chains defined in this contract. Do not invent another transition.
- Define the active tip as the sole reachable, non-superseded end of the valid predecessor chain. `awaiting-confirmation`, `confirmed`, and `memory-pr-ready` are recoverable nonterminal states. Only `no-promotion` and `memory-pr-merged` are current-format terminal states.
- Return an existing valid state through verified reads rather than duplicating it.
- Stop on a missing predecessor/digest, cycle, untrusted author, multiple active or unsuperseded confirmed revisions, contradictory terminal, stale source identity, ambiguous active memory PR, or any cross-field mismatch.

## Dual-read legacy promotion callbacks

Dual-read an unversioned legacy `${marker_namespace}:context-promotion` callback only when every applicable check passes:

- the callback and linked legacy eligibility registration were present in the first immutable read baseline of the current explicit invocation, before any current-run mutation;
- both unchanged markers bind the exact merged product-PR number and source head, and the callback author login exactly matches the legacy eligibility registration comment's author login;
- `outcome` is exactly `no-promotion`, `memory-pr-ready`, or `memory-pr-merged`, and the callback identifies the legacy eligibility registration URL; compute and bind both whole-comment digests during the current read rather than requiring the historical payload to contain them;
- the historical PASS binds the same Issue URL/digest, product-PR URL/Body digest, head/base tuple, and `verdict: PASS`;
- exactly one historical Issue callback has the matching PR URL, head/base tuple, and PASS URL;
- legacy `no-promotion` conflicts with no project-memory PR; reconstruct the complete five-category assessment rather than requiring absent historical category fields;
- legacy `memory-pr-ready` identifies one exact Ready or merged project-memory PR with a persisted historical Reviewer PASS bound to its then-current Body/head/base tuple;
- legacy `memory-pr-merged` identifies that project-memory PR and independently verifies integration into `develop`, current merge identity, allowed actual merge method, transport-verified merge provenance, and currently known successful required checks;
- no conflicting legacy or schema-v2 state exists except one exact source-bound migration branch defined below.

Treat a callback that declares `schema_version: 2` but omits a required field, predecessor, or digest as malformed schema v2, never as legacy.

An exact legacy terminal with an already closed Issue is a completed compatibility no-op after all independent verification. When the Issue remains open, reconstruct and persist the complete source-bound proposal artifact and fresh Reviewer PASS, summarize and stop, then obtain a later current explicit source-bound confirmation re-entry before any new merge or close:

- closure-only legacy `no-promotion` or `memory-pr-merged` uses `awaiting-confirmation` with `proposal_kind: legacy-reconciliation`, preserves the exact terminal outcome, and then appends `confirmed`; the historical terminal remains outcome evidence and no duplicate terminal is written;
- if reassessment of legacy `no-promotion` finds a write, use `proposal_kind: write`, `revision_reason: legacy-reassessment`, bind the legacy callback through both predecessor/evidence pairs, and require the normal Ready → coordinator merge → current `memory-pr-merged` path;
- unmerged legacy `memory-pr-ready` uses `legacy-reconciliation` confirmation and then the `migration: confirmed-legacy-ready` Ready callback before any coordinator merge;
- legacy `memory-pr-ready` whose memory PR was already merged uses `legacy-reconciliation` confirmation and then the `migration: confirmed-legacy-already-merged` terminal. This recognizes historical integration and cannot authorize a new merge.

For a legacy migration, establish the first schema-v2 `awaiting-confirmation` comment's transport-returned author as the current trusted workflow author and require every successor to equal it. If safe provenance cannot be established, stop blocked.

## Preserve compatibility

- Keep all callback field names, enum values, marker forms, schema versions, and digest algorithms above stable. Treat the versioned Reviewer PASS and markerless validation-impact artifact as the explicit additive migration defined here, not as permission to extend another fenced schema silently.
- Continue dual-reading an exact unversioned Reviewer PASS as `legacy-full`, equivalent to `r3-normative`; never rewrite, upgrade, or downgrade it, and never require its historical producer to have written tier, review-input, item-coverage, or validation-impact fields. New PASS writes use only `review_schema_version: 1`.
- Treat validation-impact evidence as optional only for old/full-validation paths. Reuse or incremental validation requires the exact current artifact; its absence never weakens validation or required CI.
- Keep the unversioned eligibility and promotion dual-read paths. Never reinterpret malformed schema v2 as legacy or require a historical field that its producer did not promise.
- Keep standalone `closeout` and `context-promotion` entries able to produce and consume the same artifacts. They retain their phase-scoped authority and stopping rules; this contract grants no coordinator authority to them.
- Keep `delivery` a read/validation consumer of these schemas. It cannot produce a phase verdict, proposal, review, confirmation, Ready callback, or terminal callback.
