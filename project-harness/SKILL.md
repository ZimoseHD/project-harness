---
name: project-harness
description: This skill should be used only when the current user message supplies init, delivery, or one exact feature-iteration role—definition, context-authoring, implementation, closeout, or context-promotion—to initialize project-owned Harness configuration, define one feature, run one compatibility phase, or coordinate a lean code-first delivery through guarded PR integration and verified Issue closure.
disable-model-invocation: false
---

# Project Harness

Dispatch one explicitly requested operation. Prefer the lean `delivery` path after Definition: implement the contract, verify the product diff proportionally, merge the accepted product PR, skip Context Promotion when all five durable-memory categories are exactly `无`, and close the Issue after a final guarded read. Enter the source-bound Context Promotion confirmation flow only for an actual project-memory write or an already-persisted promotion lineage.

## Require an exact invocation

Require the current user message to supply exactly one recognized role and that role's semantic inputs. Codex requires the user's `$project-harness` trigger because `agents/openai.yaml` disables implicit invocation. Claude Code may load the Skill from `/project-harness` or by model selection because `disable-model-invocation: false`; loading alone never supplies a role, source, approval, delegation, merge, or closure authority.

Validate public invocations by semantic inputs rather than a generated hand-off shape. Accept `authoritative_sources` as an optional carrier for exact current-message URLs and `next_action` as optional non-authoritative description. Never fill a missing role, source, decision, configuration choice, approval, or mutation authority from repository state, prior chat, an absent hand-off, or the Skill body.

For project initialization or an explicit schema-v1 migration, require:

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
~~~

Accept the historical input containing only `configuration.marker_namespace` for schema-v1 compatibility. Permit omitted `configuration` fields only when `.project-harness/config.yaml` already exists and `init` is validating without migration. Never partially default schema-v2 integration policy.

For Definition, require `role: definition` and the raw or changed requirement in the same message. Accept an optional explicitly targeted Issue URL for an initial Definition; require that exact URL when updating an existing delivery contract.

For normal delivery, require `role: delivery` and one explicit finalized Issue URL. Accept related PR or callback URLs only as search hints. Read the Issue, relevant workflow comments, related PRs, current refs, and checks needed to reconstruct the next action. Do not enumerate every Issue comment page or construct an audit inventory unless an ambiguous workflow lineage, ambiguous comment mutation, or legacy recovery specifically requires it.

For one compatibility or recovery phase, require exactly one role and the sources named by that operation:

~~~yaml
role: context-authoring | implementation | closeout | context-promotion
~~~

For an actual Context Promotion write proposal, or an already-persisted unconfirmed promotion lineage, require a later explicit source-bound decision re-entry:

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

Require empty `modification_items` for `approved` and `pause`, and non-empty items for `revise`. Independently re-read the sole active `awaiting-confirmation` tip before accepting any decision. Reject a bare reply, stale binding, missing role, ambiguous decision, or unmatched proposal before mutation.

Reject missing, ambiguous, aliased, or unknown roles. Treat `external-review` as a stopping destination, not an executable role. Treat an internal dispatch from the current `delivery` coordinator as scoped delegation rather than a public invocation.

## Load one top-level operation

Read the selected operation reference completely, then read only the supporting references named in its row.

| Exact role | Operation reference | Supporting references | Verified success output | Normal destination |
| --- | --- | --- | --- | --- |
| `init` | `references/init.md` | None | Verified `.project-harness/config.yaml` | `definition` or stop |
| `definition` | `references/definition.md` | Issue transport; Pull Request transport; Issue contract | Read-back-verified Issue | `context-authoring` when required, otherwise `delivery` |
| `context-authoring` | `references/context-authoring.md` | Issue transport; Pull Request transport; Issue contract | Verified existing decision or Ready proposed-decision PR | `delivery` after the decision source merges, or `external-review` |
| `delivery` | `references/delivery.md` | Issue transport; Pull Request transport; Delivery evidence contract | Accepted product PR merged, any approved memory PR merged, and Issue verified closed | Stop |
| `implementation` | `references/implementation.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Read-back-verified Draft product PR | `delivery` or legacy `closeout` |
| `closeout` | `references/closeout.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Accepted Ready product PR and exact code-only/promotion classification | `delivery` or `external-review` |
| `context-promotion` | `references/context-promotion.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract | Direct no-promotion result, or confirmed Ready/merged project-memory result | `delivery`, `external-review`, or stop |

Use `references/issue-transport.md` and `references/pull-request-transport.md` only as internal I/O protocols. Use `references/delivery-evidence-contract.md` as the only persistent Closeout/Promotion artifact schema. Do not load `references/delivery-log-contract.md` during a new delivery; it is a frozen read-only reference for historical `delivery-stage-observation` comments.

Keep `init`, `definition`, `context-authoring`, and standalone compatibility phases at their selected operation boundary. For `delivery`, keep one coordinator in contact with the user and dispatch one isolated Phase Owner per Implementation, Closeout, or required Context Promotion semantic round. Do not load phase references or perform phase reasoning in the coordinator.

## Delegate compactly without expanding authority

Emit only delegation schema-v3 for a new phase dispatch:

~~~yaml
delegation:
  schema_version: 3
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
      - kind: null
        url: null
        body_sha256: null
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

Populate every schema-v3 field. Bind only the exact Issue/PR tuple and persistent evidence required by the delegated action. Have the Phase Owner read those exact sources through the loaded transports and challenge only missing, changed, or contradictory evidence. Do not copy complete Issue/PR Bodies, diffs, check payloads, comment inventories, Evidence Bundles, component identity maps, or raw tool output into a new delegation.

Treat one exact combination of delegated role, bound snapshot, evidence URL/digests, user decision, mutation set, and `next_action` as one semantic round. Keep the same live Owner while those bindings remain unchanged. A slow read, active tool, Worker failure, liveness change, or Reviewer FAIL does not by itself create another Owner.

Dual-read schema-v2 delegation only when recovering a live older dispatch. Validate its operation-local Evidence Bundle with `scripts/evidence_bundle.py` under the historical contract and never persist it. Dual-read schema-v1 through its historical complete-fresh-read fallback. Never emit schema-v1 or schema-v2 for a new dispatch, and never treat either legacy envelope as public mutation authority.

Enumerate only phase-permitted mutations:

| Delegated role | Repository mutations | Issue mutations | Pull Request mutations |
| --- | --- | --- | --- |
| `implementation` | create/resume task branch; edit product code/tests and permitted Execution Packet; commit; push | none | `create-draft`; `replace-content` |
| `closeout` | none | `add-comment` | `add-comment`; `mark-ready`; `convert-to-draft` |
| `context-promotion` | create/resume project-memory branch; edit permitted authority files; commit; push | none | `create-draft`; `replace-content`; `add-comment`; `mark-ready`; conditional `convert-to-draft` |

Keep merge and final Issue closure exclusively in the current `delivery` coordinator. A standalone `context-promotion` retains only its documented compatibility closure authority.

Keep each Phase Owner as the sole phase writer and hand-off producer. Permit only direct, narrow, read-only Workers or a fresh independent Reviewer when separate context materially improves the task. Give every Worker and Reviewer an empty persistent mutation set, forbid further delegation, and return results only to the Owner. Forbid every descendant from merging, closing the source Issue, approving for the user, or declaring the delivery complete.

## Load project-owned configuration

- Treat `.project-harness/config.yaml` at the consuming project root as the only project-specific configuration source.
- Write schema-v2 for new configuration. Require one lowercase kebab-case `marker_namespace`, `integration.base_branch: develop`, and separate product/memory merge methods from `merge`, `squash`, or `rebase`.
- Dual-read schema-v1 with its historical `develop` base only when repository capability reports exactly one available method. Otherwise stop before the first lifecycle mutation and hand off to explicit `role: init` migration.
- Parse every lifecycle operation with `scripts/config_guard.py`. Fail closed on missing, invalid, unsupported, or ambiguous configuration.
- Resolve `${marker_namespace}` only from the validated config and never rename a namespace after a callback has been persisted.

## Prefer code output and proportional verification

- Treat the Issue as the delivery contract and the product PR as the implementation result and verification carrier.
- Treat the Issue's `### 改动范围` block as the sole authority for what product code may change. Record the ordinary business area plus either the exact literal `受保护改动：无` or a short list of explicitly allowed exceptions for the protected surfaces defined only in `references/issue-contract.md`. Missing, broad, or ambiguous wording grants no permission.
- For a clear task with no protected change, write `受保护改动：无` without asking another question. When an exception is genuinely required, ask one decision at a time in plain language and state the current behavior, proposed change, affected callers or data, compatibility or migration consequence, and recommended answer. Do not turn the protected-surface list into a user-filled matrix.
- Before the first product edit and again against the complete final diff, require Implementation to stay inside that block. Return to Definition before mutation when an exception is absent or insufficient. Keep Closeout's independent full-diff comparison inside its existing review; do not create a separate scope artifact, per-file mapping, acceptance item, or extra phase.
- Ask only for decisions that would materially change goals, boundaries, external behavior, safety, compatibility, or acceptance. Discover repository facts instead of turning routine implementation choices into user gates.
- Run implementation validation proportional to the changed code, repository rules, and Issue acceptance checks.
- Keep Closeout independent, but reuse exact current-head Implementation evidence and successful required CI when their scope remains applicable. Re-execute only missing, stale, contradicted, or risk-required checks.
- Require atomic transport guards for every write: baseline read, immediate pre-write comparison for updates, one mutation, independent read-back, and exact Markdown digest where applicable.
- Before every merge, re-read the exact PR tuple, required checks, mergeability, configured merge method, and persistent gate evidence. Before closure, re-read the Issue, accepted/merged product tuple, applicable promotion state, and protected Issue fields.
- Accept only `verified` or `no-op`. Treat partial, ambiguous, mismatched, `blocked`, or `indeterminate` outcomes as non-success.

## Select the lean or promotion path

After Closeout succeeds, derive the path from independently read persistent evidence under `references/delivery-evidence-contract.md`:

- Select `code-only` only when the Product PR contains each of the five fixed durable-memory rows exactly once, every `实际影响` value is exactly `无`, the exact Closeout PASS contains `item: durable-memory-impact`, `result: PASS`, and `evidence: all-five-none`, and no Context Promotion state or related project-memory PR exists for the source tuple.
- Treat a missing row, non-`无` value, ambiguous evidence, tuple drift, conflicting callback, or related memory PR as promotion-required or blocked; never infer the fast path from a chat summary or phase return alone.
- On `code-only`, merge the accepted product PR through the normal guarded product merge, skip Context Promotion entirely, and close the Issue after the final closure guard. Do not write a proposal, Reviewer PASS, confirmation, no-promotion terminal, Delivery observation, finalization comment, or post-close comment.
- On an actual durable-memory candidate, dispatch Context Promotion. If a first new promotion round independently classifies every candidate as `no_write`, accept its direct no-promotion result without proposal persistence or user confirmation. If any write remains, require the strict proposal, independent Reviewer, source-bound user confirmation, guarded memory merge, and terminal reconciliation.
- When any valid historical or schema-v2 promotion state already exists, resume that exact lineage under its frozen rules. Never use the new fast path to bypass an existing `awaiting-confirmation`, `confirmed`, Ready, terminal, supersession, or legacy migration state.

Require the source-bound user confirmation only for an actual write proposal or a legacy lineage whose persisted protocol already requires it. Never infer approval from silence, timeout, general delivery intent, or an earlier invocation.

## Bind repository policy and mutations

- Use `develop` for product and project-memory integration. Reserve `main` for release/hotfix work.
- Let only the current explicit `delivery` coordinator merge the exact accepted product PR and any confirmed project-memory PR with the configured methods. Never ask the user to perform a normal Delivery merge.
- Require affirmative mergeability for a new merge and verified provenance, actual allowed method, exact tuple, and current required checks for already-merged recovery.
- Do not use closing keywords. Close the source Issue with explicit `change-metadata` only after the selected code-only or promotion path is complete, then independently read back `state: closed` and `state_reason: completed`.
- Do not require an unlocked Issue or `add-comment` capability solely for final closure; the lean path writes no post-close observation.
- Omit `Co-Authored-By` from commits.

## Preserve persistent compatibility

Keep these marker names unchanged:

| Marker template | Producer | Consumer |
| --- | --- | --- |
| `${marker_namespace}:context-authoring` | `context-authoring` | `implementation`; `delivery` |
| `${marker_namespace}:context-promotion-eligible` | `closeout` | `context-promotion`; `delivery` |
| `${marker_namespace}:context-promotion` | `context-promotion` | `context-promotion`; `delivery`; `closeout` conflict checks |

Keep existing Issue and Product PR headings, Markdown normalization, transport envelopes, Closeout evidence schemas, promotion callback schemas, marker payloads, and config schema stable. Read historical lineages under `references/delivery-evidence-contract.md`; never overwrite or reinterpret them.

Require the compact `### 改动范围` block before any new or still-unmerged product mutation. Return an older open lineage that lacks it to Definition for a one-time Issue update and fresh downstream binding. Permit an already-merged legacy lineage to finish read-only recovery or closure without rewriting history, but never use that exception for another product-code mutation.

Treat `record_kind: delivery-stage-observation` comments and `references/delivery-log-contract.md` as frozen legacy audit data. New operations must not write, backfill, repair, require, or use their coverage for phase dispatch, merge, closure, or completion. Historical comments never become workflow authority or project memory.
