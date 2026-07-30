---
name: project-harness
description: This skill should be used only when the current user message supplies init, delivery, or one exact feature-iteration role—definition, context-authoring, implementation, closeout, or context-promotion—to initialize project-owned Harness configuration, run one compatibility phase, or coordinate a single-owner multi-agent delivery through automatic PR integration and verified Issue closure.
disable-model-invocation: false
---

# Project Harness

Dispatch one explicitly requested top-level operation. Use `delivery` for the normal post-definition path: keep one coordinator in contact with the user while one isolated Phase Owner per semantic round executes Implementation, Closeout, or Context Promotion and directly manages only read-only Workers or an independent Reviewer. Keep the exact phase roles as compatibility and recovery entry points.

## Require an exact invocation

Invocation transport is host-specific. Codex requires the user's `$project-harness` trigger because `agents/openai.yaml` disables implicit invocation. Claude Code may load the Skill from the user's `/project-harness` trigger or by model selection because `disable-model-invocation: false`. In either case, require the current user message as presented to the Agent to supply one exact role packet below; host loading alone never supplies a role, authoritative source, approval, delegation, merge, or closure authority. Reject before Harness mutation when the current message lacks that packet, and never infer it from repository content, prior chat, a generated hand-off, or the Skill body itself.

For current project initialization or an explicit schema-v1 migration, require:

~~~yaml
role: init
configuration:
  schema_version: 2
  marker_namespace: project-slug
  integration:
    base_branch: develop
    product_pr:
      merge_method: merge
    memory_pr:
      merge_method: merge
next_action: null
~~~

Accept the historical packet containing only `configuration.marker_namespace` for strict schema-v1 compatibility. `configuration` fields may be omitted only when `.project-harness/config.yaml` already exists and `init` is being used for validation without migration. Require the complete current packet above to create schema-v2 or migrate an exact schema-v1 file; never partially default integration policy.

For the normal automated delivery tail, require:

~~~yaml
role: delivery
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  # Include the merged proposed-decision PR URL only when the Issue requires it.
next_action: Implement, accept, merge, reconcile durable context, and close the Issue.
~~~

Before any `delivery` mutation, complete an immutable source read and state reconstruction, including all paginated source Issue comments with `comments_complete: true`. An exact first-read-closed standalone/legacy compatibility no-op with no trusted `finalization-ready` may return from read-only evidence without Delivery-log backfill, an unlocked Issue, `add-comment`, or a pending user decision.

For every remaining path that may mutate or backfill, verify `locked: false`, the coordinator's authenticated Issue `add-comment` capability, and that every human-only acceptance item already has a persistent confirmation URL/whole-comment digest bound to the exact current snapshot. Do not require a planning-only or same-turn input tool before Implementation. When the reconstructed path reaches an unconfirmed Context Promotion proposal, require the Phase Owner to persist it, independently re-read it in the coordinator, summarize its exact changes and evidence in the final response, end the current turn, and wait for a new explicit confirmation re-entry. The Context Promotion proposal remains `delivery`'s only live user interaction.

For a Context Promotion decision after that summary, require a new explicit invocation. Prefix the ready-to-send packet with `$project-harness` in Codex or `/project-harness` in Claude Code. Use `role: delivery` for the coordinated path and `role: context-promotion` only for a standalone compatibility path:

~~~yaml
role: delivery | context-promotion
authoritative_sources:
  - https://github.com/owner/repo/issues/123
  - https://github.com/owner/repo/pull/456
user_decision:
  proposal_url: https://github.com/owner/repo/pull/456#issuecomment-789
  proposal_sha256: SHA256
  decision: approved | revise | pause
  modification_items: []
next_action: Re-read and continue the exact persisted Context Promotion proposal.
~~~

Require `modification_items` to be empty for `approved` and `pause` and non-empty for `revise`. Treat the proposal URL and whole-comment SHA-256 as claimed bindings only: independently re-read the sole active `awaiting-confirmation` tip and every bound source before accepting the decision. If a `user_decision` is supplied without one matching active tip, return blocked before mutation and never retain it for a later proposal. A bare reply, prior chat, or copied decision without a current exact role is not a Harness operation or approval. On Claude Code, model-selected loading may expose the Skill, but it cannot fill in a missing role packet or source-bound decision.

For a single compatibility or recovery phase, require:

~~~yaml
role: definition | context-authoring | implementation | closeout | context-promotion
authoritative_sources: []
next_action: null
~~~

Accept `definition` from a raw requirement or an explicitly targeted Issue. Require the exact authoritative URLs described by the selected operation for every later entry. A `delivery` re-entry may include exact related PR or callback URLs, but the coordinator must independently rediscover and verify their relationship rather than trusting the packet.

Reject a missing, ambiguous, aliased, or unknown role. Do not infer a public operation from repository state, URLs, prior chat, or a hand-off. Treat an internal phase dispatch from the current `delivery` coordinator as scoped delegation, not as an implicit public Skill invocation. Treat `external-review` as a stopping destination, not as an executable Harness role.

## Load one top-level operation

Select one row and read its operation reference completely, then read only the supporting references named in that row.

Internal GitHub transport protocols:

- **Issue transport:** `references/issue-transport.md`
- **Pull Request transport:** `references/pull-request-transport.md`

Shared artifact contracts:

- **Issue contract:** `references/issue-contract.md`
- **Product PR contract:** `references/product-pr-contract.md`
- **Delivery evidence contract:** `references/delivery-evidence-contract.md`
- **Delivery stage log contract:** `references/delivery-log-contract.md`

| Exact role | Operation reference | Supporting references | Authoritative input | Persistent success output | Success destination | Recovery or re-entry |
| --- | --- | --- | --- | --- | --- | --- |
| `init` | `references/init.md` | None | Exact project-owned marker namespace, or an existing valid Harness config | Created or read-back-verified `.project-harness/config.yaml` | `definition` or no further action | `init` after correcting a missing, invalid, or conflicting input |
| `definition` | `references/definition.md` | Issue transport; Pull Request transport; Issue contract | Raw or changed requirement; optional explicitly targeted Issue | Independently reviewed and read-back-verified Issue | `context-authoring` or `delivery` | `definition` when the contract later changes |
| `context-authoring` | `references/context-authoring.md` | Issue transport; Pull Request transport; Issue contract | Finalized Issue requiring the pre-implementation durable-decision gate | Verified existing decision source or Ready proposed-decision PR | `delivery` after the decision source is merged, or `external-review` | `definition`; `context-authoring` to resume blocked work or verify merge |
| `delivery` | `references/delivery.md` | Issue transport; Pull Request transport; Delivery evidence contract; Delivery stage log contract | Finalized Issue; merged decision source when required | Accepted product PR and any approved project-memory PR automatically merged into `develop`, required stage observations verified, terminal Context Promotion callback verified, and source Issue verified closed | No further action | `delivery` from persisted evidence; `init` for merge-policy migration; `definition` for a changed contract |
| `implementation` | `references/implementation.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Finalized Issue; merged decision source when required | Independently read-back-verified Draft product PR | `delivery` at Closeout, or `closeout` for legacy operation | `definition`; `implementation` to resume blocked work |
| `closeout` | `references/closeout.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Finalized Issue and Draft product PR | Accepted Ready product PR plus project-memory promotion eligibility | `delivery` at the product merge gate, or `external-review` for legacy operation | `implementation`, `definition`, or `closeout` to resume blocked/repaired work |
| `context-promotion` | `references/context-promotion.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Issue and eligible merged product PR | Confirmed `no-promotion` callback or Ready project-memory-only PR, plus the source Issue closure judgment | `delivery` for automatic integration, `external-review`, or no further action | `context-promotion` to resume blocked or legacy work; `definition` for a product-contract change |

`init`, `definition`, `context-authoring`, and the three compatibility phase roles stop at their selected operation boundary. They return a minimal hand-off and never load another operation in the same Agent.

For `delivery`, the coordinator loads `references/delivery.md`, the two transports, `references/delivery-evidence-contract.md`, and `references/delivery-log-contract.md` only. It must not load a phase reference or perform phase reasoning itself. The evidence contract lets it validate persistent artifact schemas and predecessor bindings only; it grants no phase behavior authority. For each semantic round, start one isolated Phase Owner and instruct that Owner to read exactly one phase reference plus the supporting references from its compatibility row above. Keep that Owner live while the bound inputs and target remain unchanged. The Owner returns the only phase hand-off; the coordinator verifies its referenced persistent evidence before dispatching the next phase.

## Delegate without expanding authority

A current explicit `role: delivery` invocation authorizes only the exact delivery tail for the supplied Issue. Before starting a Phase Owner, emit `delegation.schema_version: 2` in this ephemeral delegation envelope:

~~~yaml
delegation:
  schema_version: 2
  parent_role: delivery
  delegated_role: implementation | closeout | context-promotion
  authoritative_sources: []
  bound_snapshot:
    issue:
      url: null
      body_sha256: null
    product_pr:
      url: null
      title: null
      body_sha256: null
      head_ref: null
      head_sha: null
      base_ref: develop
      base_sha: null
    memory_pr:
      url: null
      title: null
      body_sha256: null
      head_ref: null
      head_sha: null
      base_ref: develop
      base_sha: null
    evidence_comments:
      - url: null
        body_sha256: null
  evidence_bundle:
    bundle_schema_version: 1
    scope: implementation | closeout | context-promotion
    semantic_round_key: null
    bundle_sha256: null
    provenance:
      authenticated_actor_login: null
      authenticated_actor_id: null
      mutation_author_login: null
      transport_family: null
    completeness:
      issue_body: false
      workflow_comments: false
      related_pr_search: false
      product_pr: false
      authority_sources: false
      memory_pr: false
      diff: false
      checks: false
    completeness_bindings:
      issue_body: []
      workflow_comments: []
      related_pr_search: []
      product_pr: []
      authority_sources: []
      memory_pr: []
      diff: []
      checks: []
    semantic_snapshot:
      round_binding:
        delegated_role: implementation | closeout | context-promotion
        bound_snapshot: {}
        persistent_evidence: []
        user_decision: {}
        allowed_mutations: {}
        next_action: null
      payload_identities: {}
    liveness_snapshot:
      payload_identities: {}
    payloads: []
  evidence_component_identities:
    issue_body:
      PAYLOAD-ID:
        locator: LOCATOR
        snapshot_class: semantic
        source_identity: content-sha256:SHA256
        content_sha256: SHA256
    workflow_comments: {}
    related_pr_search: {}
    product_pr: {}
    authority_sources: {}
    memory_pr: {}
    diff: {}
    checks: {}
  persistent_evidence_urls: []
  user_decision:
    proposal_url: null
    proposal_sha256: null
    decision: null
    modification_items: []
  allowed_mutations:
    repository: []
    issue_transport: []
    pull_request_transport: []
  next_action: null
~~~

- Treat the Evidence Bundle as an operation-local, transport-derived, digest-bound read cache, never as persistent evidence, workflow state, mutation authority, a Delivery observation, or project memory. Populate every payload with one stable ID, kind, locator, `snapshot_class: semantic | liveness`, normalized content, and its SHA-256 digest. Define `source_identity` exactly as `content-sha256:<content_sha256>`; do not accept an opaque caller-selected identity. Put the exact outer delegated role, bound semantic tuple/evidence identities, user-decision binding, allowed mutations, and `next_action` in `semantic_snapshot.round_binding`; derive `semantic_round_key` only from that stable binding's UTF-8 canonical JSON. Keep the extensible `semantic_snapshot.payload_identities` outside `round_binding`. Have `scripts/evidence_bundle.py` sort payloads and each completeness binding by payload ID, derive both snapshot classes' `payload_identities` maps from each payload's exact locator/snapshot-class/source-identity/content-digest tuple, then calculate `semantic_round_key` and `bundle_sha256`.
- Have the coordinator construct the initial Bundle from its immutable workflow reconstruction and include the complete normalized Issue/PR Bodies, requested comments, diff, check snapshot, and other payloads already read for the delegated scope. Let the Phase Owner add only phase-owned authority sources or newly produced PR evidence and derive a successor Bundle. Do not make the Owner download a complete payload again merely to establish independence.
- Require every Bundle to bind the verified authenticated actor, mutation author, selected transport family, semantic snapshot, liveness snapshot, and explicit completeness map. A true completeness field must have a non-empty `completeness_bindings` list whose payload IDs exist and whose normalized transport result proves the requested scope was completely represented, including a verified absence; a false field must bind no payload and is a structural cache miss. Before building the Bundle, have the producer run `derive_component_identities` over the original normalized transport-result manifest and place the result in the outer `evidence_component_identities`; do not derive the expected map from the Bundle being validated. Require each bound payload's locator/snapshot-class/source-identity/content-digest tuple to equal both its derived snapshot `payload_identities` entry and that outer map. Call `validate_bundle` with the exact `expected_scope`, outer-derived `expected_round_binding`, the component names required by the current consumer, and the outer map as `expected_component_identities`. A false, missing, unverifiable, unbound, wrong-scope, stale-round, class/identity-mismatched, or digest-mismatched required component requires a targeted fresh read or a blocked result, never permission to continue.
- When the Phase Owner adds authority, current-authority search, memory-PR, diff, check, or newly produced evidence payloads, derive the corresponding identities from those exact transport results and extend the outer map and successor Bundle together. Pass the complete successor map beside the Bundle to a Reviewer. This map is operation-local and excluded from `semantic_round_key`; a same-target extension does not create a new Owner. Never persist the map, Bundle, or raw payloads.
- Pass the same normalized Bundle payloads to a fresh Reviewer. Define review independence as an isolated, mutation-free judgment over exact raw evidence, not as a requirement to repeat evidence acquisition. Require the Reviewer to verify Bundle integrity locally and return `FAIL: incomplete-evidence-bundle` for a missing input; permit a targeted challenge read only when an exact source is incomplete, inconsistent, or requires a live gate.
- Use no time-to-live. Keep reusable semantic content valid only while its exact digest, immutable commit/blob binding, and semantic-round key remain unchanged. Put checks, mergeability, permissions, Issue/PR state, and repository merge-method capability in `liveness_snapshot`; a Bundle can report but never freeze them. Bind an active lineage or branch tip in `semantic_snapshot` whenever it is part of the delegated tuple, even if its current value is also probed live.
- Dual-read a delegated schema-v1 envelope only for compatibility. Because it has no Evidence Bundle, perform the existing complete independent reads and never infer cached content from its `bound_snapshot`. Emit only schema-v2 for a new dispatch. An unknown delegation or Bundle schema is blocked.
- Apply these exact verification layers without duplicating them in phase references:

| Layer | Purpose | Required behavior |
| --- | --- | --- |
| `L0 bundle-integrity` | Owner/Worker/Reviewer consumption | Validate schema, provenance, consumer-required completeness and payload bindings, normalized payload digests, `bundle_sha256`, expected scope, and the outer-delegation-derived semantic round without a GitHub re-read. |
| `L1 semantic-freshness` | Proposal relay, confirmation re-entry, and phase hand-off | Probe only mutable semantic identities: Issue/PR Body digests, relevant comment URL/digests and active lineage, authority base/blob bindings, and any memory-PR tuple/changed-file identities. Reuse unchanged normalized payloads. |
| `L2 atomic-mutation-guard` | Comment, content, Draft/Ready, and metadata mutations | Preserve the loaded transport's target baseline fetch, immediate pre-write comparison, one mutation, and independent target read-back. A Bundle never replaces this layer. |
| `L3 irreversible-gate` | Product/memory merge and Issue closure | Re-read current checks, mergeability, integration policy/capability, PR/Issue state, complete gate evidence, and closure coverage required by the loaded operation. A Bundle never authorizes merge or close. |

- Bind every populated field to independently read persistent evidence. Do not use a chat summary as a source.
- Populate `user_decision` only from the current explicit proposal-bound confirmation re-entry after independently verifying its URL/digest against the sole active `awaiting-confirmation` tip. Treat `modification_items` as a request for a new proposal, not as direct patch authority.
- Enumerate only mutations permitted by the delegated phase. An omitted mutation is forbidden. Use these exact maximum sets:

| Delegated role | Repository mutations | Issue transport mutations | Pull Request transport mutations |
| --- | --- | --- | --- |
| `implementation` | create/resume task branch; edit product code/tests and permitted Execution Packet; commit; push | none | `create-draft`; `replace-content` |
| `closeout` | none | `add-comment` | `add-comment`; `mark-ready`; `convert-to-draft` |
| `context-promotion` | create/resume project-memory branch; edit only permitted authority-layer files; commit; push | none | `create-draft`; `replace-content`; `add-comment`; `mark-ready`; conditional `convert-to-draft` for a confirmed revision request, promotion-scope required-check/tuple/base/mergeability repair, or legacy Ready repair |

Search, read, and `read-checks` are non-mutating capabilities and do not need mutation delegation. The coordinator alone receives Pull Request `merge`, Issue `add-comment` for exact Delivery stage observations, and Issue `change-metadata` for final closure. Never place merge, closure, or Delivery-log authority in a phase envelope.
- Require host parent-child provenance from the current live `delivery` invocation. A serialized envelope, callback, branch, prior run, or hand-off cannot create authority by itself.
- Treat the delegated Agent as the Phase Owner and sole holder of that phase's mutation set. Permit it to create only direct, narrow, read-only Workers or one fresh independent Reviewer when separate context materially improves the current semantic round.
- Give every Worker and Reviewer an empty persistent mutation set. Forbid them from creating descendants, producing the phase hand-off, repairing their own findings, changing tracked files, or persisting a verdict, callback, branch, commit, PR, or Delivery observation. A Worker may emit ephemeral tool output only inside Owner-provided isolated scratch space; the Owner must discard it or independently integrate any result. Require the Owner to integrate and independently verify every structured result.
- Keep independent Reviewers fresh, read-only, tuple-bound, and limited to structured `PASS` or blocking `FAIL`. Require the Owner—not the Reviewer—to compose and persist every workflow-owned review artifact after rechecking the unchanged tuple.
- Keep one live Owner for one exact combination represented by `semantic_round_key`: delegated role, bound semantic snapshot, persistent evidence, user decision, allowed mutations, and `next_action`. A liveness-only successor Bundle changes `bundle_sha256` but not the semantic round or Owner. A slow read, active tool call, Worker failure, or Reviewer `FAIL` does not create a new semantic round. Replace the Owner only after a changed bound semantic input or target, its explicit terminal return, or host-confirmed unrecoverable context loss.
- Forbid every descendant from merging a PR, closing the source Issue, approving a Context Promotion proposal for the user, or declaring the entire delivery complete.

The coordinator may atomically merge or close only where `references/delivery.md` permits it. A normal phase hand-off does not grant those mutations.

## Load project-owned configuration

- Treat `.project-harness/config.yaml`, relative to the project root, as the sole source of project-specific Harness configuration. Keep it outside the Skill directory so Skill synchronization does not overwrite it.
- Write schema-v2 for every new configuration. Require one `marker_namespace`, `integration.base_branch: develop`, and separate `integration.product_pr.merge_method` / `integration.memory_pr.merge_method` values from `merge`, `squash`, or `rebase`. The namespace must be a lowercase kebab-case ASCII slug of 1–63 characters matching `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Strictly dual-read an existing schema-v1 file containing only `schema_version: 1` and `marker_namespace`. Treat `develop` as its historical base and resolve one merge method only when the authoritative repository capability reports exactly one available method. When multiple methods remain, stop before the first lifecycle mutation and hand off to explicit `role: init` schema-v2 migration.
- Before any lifecycle operation, parse and validate the config with `scripts/config_guard.py`. If it is missing, invalid, unsupported, or ambiguous, fail closed and hand off to an explicit `role: init`; do not infer a namespace or merge policy from the directory, repository name, remote URL, Issue, prior callback, or enabled merge buttons.
- Resolve every `${marker_namespace}` token in the selected reference to the exact configured value before searching, comparing, producing, or verifying a marker. Never persist the token itself.
- Permit only an explicit schema-v1 to schema-v2 migration that preserves the exact namespace and supplies the complete integration policy. Once a callback containing the namespace has been persisted, `init` must not rename it.

## Enforce shared contracts

- Treat the Issue as the delivery contract and the product PR as implementation result and evidence. Store durable knowledge only in the single authoritative layer defined by the Harness document-placement contract and applicable repository rules.
- Pass only the delegation envelope, authoritative Issue/PR or exact durable-source URLs, phase-required evidence URLs, snapshot bindings, and `next_action` between Agents. Persist every successful stage boundary in GitHub before advancing.
- After each successful durable Delivery boundary and each persistently evidenced bounded attempt, follow the Delivery stage log contract to append and independently verify one source-Issue observation. Treat a current-invocation revision/pause/blocked confirmation-response observation as best-effort and non-coverage. Keep every observation audit-only: it summarizes authoritative artifacts but never replaces them, authorizes progress, or becomes a fourth workflow marker.
- Within a Harness operation, follow only the loaded internal Issue and Pull Request transport protocols for GitHub mutations, digest normalization, baseline protection, merge, and independent read-back. Do not invoke a separate GitHub transport Skill, mix in a generic PR workflow, or use a second authenticated transport.
- Require every loaded Issue/PR transport result in one operation to report the same verified authenticated actor login/ID and mutation-author login. Stop blocked on a mismatch or unverifiable identity.
- Accept only `verified` or `no-op` transport results; fail closed on partial, ambiguous, `blocked`, `indeterminate`, or mismatched results.
- Bind every decision or verdict to the fields required by its phase, including Issue Body digest, PR Body digest, head SHA, base ref/SHA, and comment URL/digest when applicable. Invalidate stale review, acceptance, promotion proposal, or user confirmation when a bound field changes.
- Let Context Promotion calculate its review tier only under that phase reference. A lower tier may narrow evidence breadth and local validation, but it never removes the fresh independent Reviewer, source-bound user confirmation, exact tuple/digest binding, required checks, merge gate, or closure gate.
- Treat a Context Promotion validation-impact artifact as retained local-validation evidence only. Never let it preserve an old tuple, Reviewer PASS, confirmation, mergeability result, or old-head required CI/check.
- Before completing an operation, establish every authoritative repository fact and durable source required by that operation. Stop and report missing evidence when a required fact cannot be established; never treat `proposed` material as verified behavior.
- Use the shared Issue contract as the only Issue Body schema. Use the shared Product PR contract only for the product PR handled by Implementation, Closeout, and Context Promotion. Build proposed-decision and project-memory-only PR Bodies from the selected phase reference instead. Do not look for or maintain `.github` copies of either contract.

## Bind repository policy and mutations

- Use `develop` as the product and project-memory integration base. Reserve `main` for the repository's release/hotfix flow.
- A current user message that explicitly invokes one exact compatibility phase supplies authority only for the mutations enumerated by that phase reference. It does not authorize merge or later phases.
- A current explicit `role: delivery` invocation supplies the coordinator's full, Issue-scoped automation authority and supplies descendants only the mutations enumerated in their delegation envelopes.
- Never infer a merge method from enabled repository buttons or ask the user to perform a normal Delivery merge. For schema-v2, require the `delivery` coordinator to use `integration.product_pr.merge_method` for the accepted product PR and `integration.memory_pr.merge_method` for the confirmed-and-reviewed project-memory PR. For schema-v1 compatibility, use the sole authoritatively available repository method for both. Before the first Delivery mutation, require the loaded transport to prove each selected method is currently available; otherwise return `role: init` for policy migration or blocked for unavailable capability.
- Perform both permitted merges automatically in the current explicit `delivery` invocation. For a new merge mutation, require mergeability to be affirmatively established as mergeable; unknown is not success. For exact already-merged schema-v2 recovery, additionally require the actual method to equal the configured method; schema-v1 recovery retains its strict historical policy check. Stop blocked when the applicable method, tuple, required checks, mergeability/provenance, or permission cannot be established, but never present manual merge as the normal recovery action.
- Do not open a user decision gate during Implementation or Closeout. If acceptance truly requires human-only evidence that is not already persisted and snapshot-bound, return blocked rather than creating a second interactive gate.
- Require explicit source-bound user confirmation only for the exact Context Promotion proposal. After persisting and re-reading `awaiting-confirmation`, summarize the proposal and finish the current turn without writing `confirmed`, marking a memory PR Ready, merging, or closing. Continue only from a new exact `delivery` or standalone `context-promotion` invocation whose `user_decision` names that active proposal URL/whole-comment digest. Never infer approval from timeout, silence, a bare reply, an earlier invocation, or general delivery intent.
- Under `delivery`, close the source Issue only after the exact accepted product PR is merged, the confirmed Context Promotion path is terminal, all callbacks are read-back verified, and closure-level stage-log coverage exists. After the Issue close mutation is independently read back, append the exact `issue-closed` observation without reopening the Issue, verify it remains closed/completed, and require completion-level coverage before returning completed. A current explicit standalone `context-promotion` follows its compatibility closure gate without Delivery observations.
- Do not use closing keywords. Do not infer merge or close authority from a hand-off, Ready state, acceptance verdict, branch protection, or repository write access.
- Omit `Co-Authored-By` from commits.

## Preserve persistent markers

Keep the configured namespace and these workflow-owned suffixes stable across Skill refactors:

| Marker template | Producer role | Consumer role |
| --- | --- | --- |
| `${marker_namespace}:context-authoring` | `context-authoring` | `implementation`; `delivery` |
| `${marker_namespace}:context-promotion-eligible` | `closeout` | `context-promotion`; `delivery` |
| `${marker_namespace}:context-promotion` | `context-promotion` | `context-promotion`; `delivery`; conflict checks in `closeout` |

Do not rename a marker after the first persisted callback unless a separately approved compatibility migration implements and verifies dual-read behavior.

The exact current and pre-schema-v2 eligibility payloads, schema-v2 promotion payloads, predecessor rules, tuple/digest bindings, and strict dual-read behavior live only in `references/delivery-evidence-contract.md`. Producers compose those artifacts from that shared contract; `delivery` uses it only to validate independently re-read evidence.

For both marker families, accept only the one active source-tuple-bound lineage that validates under the shared evidence contract. New writes use its current schemas. Historical unversioned artifacts remain eligible only for its strict dual-read and additive migration paths; malformed current-schema artifacts are never legacy. This root invariant does not redefine the contract's outcome enums, predecessor fields, or active-tip algorithm.

Delivery stage observations use the unmarked `record_kind: delivery-stage-observation` schema in `references/delivery-log-contract.md`. They are not marker callbacks, lifecycle state, authorization, acceptance, confirmation, or durable knowledge. Keep the three marker names above unchanged. Only the Delivery Coordinator writes observations; descendants and standalone phase roles never do.
