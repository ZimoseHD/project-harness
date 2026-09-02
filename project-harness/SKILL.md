---
name: project-harness
description: This skill should be used only when the current user message supplies init, spec, implementation, review, context-promotion, delivery, or express—to initialize project-owned Harness configuration, write one grilled plan into a delivery Issue, run one phase, coordinate one guarded end-to-end delivery, or land one small agile change through a lightweight PR.
disable-model-invocation: false
---

# Project Harness

Deliver code through one of two paths. Path 1 turns a grilled, user-confirmed plan into an Issue contract, then implements, reviews, integrates, and closes it. Path 2 (`express`) lands a small low-risk change at conversational speed. The Harness defines phases, artifacts, and gates; how the work is decomposed—including any subagent use—is the agent's own judgment.

## Require an exact invocation or confirm a path

Require the current user message to supply exactly one recognized role and that role's semantic inputs. Codex requires the user's `$project-harness` trigger because `agents/openai.yaml` disables implicit invocation. Claude Code may load the Skill from `/project-harness` or by model selection because `disable-model-invocation: false`; loading alone never supplies a role, source, approval, merge, or closure authority.

When the current message is a raw requirement without an exact role, select the path together with the user: recommend path 1 or path 2 with a one-line rationale based on task size, risk, and whether a protected surface is involved, then wait for one explicit user confirmation. Path 1 continues with planning and `role: spec`; path 2 continues with `role: express`. Never infer a role, source, decision, configuration choice, approval, or mutation authority from repository state, prior chat, an absent hand-off, or the Skill body.

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

For path 1:

- `role: spec` requires the raw or changed requirement in the same message and a plan already stress-tested with the user through `grilling`-style questioning; accept an optional explicitly targeted Issue URL, and require that exact URL when updating an existing contract.
- `role: delivery` requires one explicit finalized Issue URL and coordinates implementation, review, guarded integration, optional promotion, and closure end to end.
- `role: implementation`, `role: review`, and `role: context-promotion` are exact single-phase entries for recovery or deliberate phase-by-phase control; each requires the sources named by its operation reference.

For an actual Context Promotion write proposal, or an already-persisted unconfirmed promotion lineage, require a later explicit source-bound decision re-entry:

~~~yaml
role: delivery | context-promotion
authoritative_sources:
  - https://example.com/owner/repo/issues/123
user_decision:
  proposal_url: https://example.com/owner/repo/pull/456#comment-789
  proposal_sha256: SHA256
  decision: approved | revise | pause
  modification_items: []
~~~

Require empty `modification_items` for `approved` and `pause`, and non-empty items for `revise`. Independently re-read the sole active `awaiting-confirmation` tip before accepting any decision. Reject a bare reply, stale binding, missing role, ambiguous decision, or unmatched proposal before mutation.

For path 2, require `role: express` and the oral requirement in the same message.

Reject missing, ambiguous, aliased, or unknown roles.

## Load one top-level operation

Read the selected operation reference completely, then read only the supporting references named in its row.

| Exact role | Operation reference | Supporting references | Verified success output | Normal destination |
| --- | --- | --- | --- | --- |
| `init` | `references/init.md` | None | Verified `.project-harness/config.yaml` | `spec` or stop |
| `spec` | `references/spec.md` | Issue transport; Pull Request transport; Issue contract | Read-back-verified Issue | `delivery` |
| `delivery` | `references/delivery.md` | Issue transport; Pull Request transport; Evidence contract | Accepted product PR merged, any confirmed memory PR merged, and Issue verified closed | Stop |
| `implementation` | `references/implementation.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Read-back-verified Draft product PR | `delivery` or `review` |
| `review` | `references/review.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Evidence contract | Accepted Ready product PR with verdict | `delivery` |
| `context-promotion` | `references/context-promotion.md` | Issue transport; Pull Request transport; Evidence contract | Direct no-promotion result, or confirmed Ready/merged project-memory result | `delivery` or stop |
| `express` | `references/express.md` | Pull Request transport | Merged lightweight PR | Stop |

Use `references/issue-transport.md` and `references/pull-request-transport.md` only as internal I/O protocols. Use `references/evidence-contract.md` as the only persistent Review/Promotion artifact schema.

## Use subagents freely

The Harness imposes no orchestration contract: no fixed topology, no phase-owner isolation, no delegation envelope, no per-phase mutation whitelist, no mandatory Worker or Reviewer. The agent running an invocation decides when a subagent materially helps, gives it whatever context serves the task, and integrates and verifies every delegated result itself. Phase artifacts, gates, and stop positions bind the invocation regardless of how the work was decomposed.

## Load project-owned configuration

- Treat `.project-harness/config.yaml` at the consuming project root as the only project-specific configuration source.
- Write schema-v2 for new configuration. Require one lowercase kebab-case `marker_namespace`, `integration.base_branch: develop`, and separate product/memory merge methods from `merge`, `squash`, or `rebase`.
- Dual-read schema-v1 with its historical `develop` base only when repository capability reports exactly one available method. Otherwise stop before the first lifecycle mutation and hand off to explicit `role: init` migration.
- Parse every lifecycle operation with `scripts/config_guard.py`. Fail closed on missing, invalid, unsupported, or ambiguous configuration.
- Resolve `${marker_namespace}` only from the validated config and never rename a namespace after a callback has been persisted.

## Keep the retained invariants

1. Treat the Issue as the delivery contract and the product PR as the implementation result and verification carrier. The Issue's `### 改动范围` block is the sole authority for what product code may change: the ordinary business area plus either the exact literal `受保护改动：无` or explicit exceptions for the protected surfaces defined only in `references/issue-contract.md`. Missing, broad, or ambiguous wording grants no permission. Express never touches a protected surface; it upgrades to path 1 instead.
2. Require atomic transport guards for every write: baseline read, immediate pre-write comparison for updates, one mutation, independent read-back, and exact Markdown digest where applicable. Accept only `verified` or `no-op`.
3. Before every merge, re-read the exact PR tuple, required checks with `required_checks_known: true`, affirmative mergeability, configured merge method, and the protocol-owned gate evidence: product merges bind `review-pass`; memory merges bind `proposal` and `confirmation`; an express merge carries an exactly empty evidence set. Base is always `develop`; `main` is reserved for release/hotfix work.
4. Do not use closing keywords. Close the source Issue with explicit `change-metadata` only after the selected path completes, then independently read back `state: closed` and `state_reason: completed`.
5. Require the split-turn source-bound user confirmation only for an actual project-memory write proposal. Never infer approval from silence, timeout, general delivery intent, or an earlier invocation.
6. Bind artifacts by whole-comment Markdown digest; never trust an extracted subtree, a chat summary, or a hand-off as mutation authority.
7. Select `code-only` only when the Product PR contains each of the five durable-memory rows exactly once, every `实际影响` value is exactly `无`, the review PASS contains `item: durable-memory-impact` with `result: PASS` and `evidence: all-five-none`, and no Context Promotion state or related project-memory PR exists. Fail closed into the promotion path otherwise.
8. Let only a current explicit `delivery` merge product and project-memory PRs and close the source Issue; let only a current explicit `express` merge its own lightweight PR. Never ask the user to perform a normal merge.
9. Omit `Co-Authored-By` from commits.

## Removed in v2

This major version deliberately breaks with the v1 line. The old contract-definition and acceptance roles were renamed to `spec` and `review`; the pre-implementation decision role was removed; and every orchestration contract—fixed delegation topology, delegation envelopes with their evidence carriers, persisted stage observations, promotion eligibility registrations, mandatory independent reviewers, and validation-reuse artifacts—was deleted together with all v1 persistent-evidence compatibility. See `MIGRATION.md` for the complete inventory and how to finish in-flight v1 work.
