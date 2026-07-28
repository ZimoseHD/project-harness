---
name: project-harness
description: Use only when explicitly invoked with init or one exact feature-iteration lifecycle role—definition, context-authoring, implementation, closeout, or context-promotion—to initialize project-owned Harness configuration or execute that phase from authoritative GitHub sources while preserving phase boundaries, independent read-back, repository authorization, durable-document conventions, and clean-session hand-offs.
disable-model-invocation: true
---

# Project Harness

Dispatch one explicitly requested operation—project initialization or one lifecycle phase—while keeping every other operation protocol unloaded. Treat this file as the shared index and contract; treat one selected operation reference plus its named supporting references as the complete executable protocol for the current invocation.

## Require an exact invocation

For project initialization, require:

~~~yaml
role: init
configuration:
  marker_namespace: project-slug
next_action: null
~~~

`configuration.marker_namespace` may be omitted only when `.project-harness/config.yaml` already exists and `init` is being used to validate it.

For a lifecycle phase, require:

~~~yaml
role: definition | context-authoring | implementation | closeout | context-promotion
authoritative_sources: []
next_action: null
~~~

Accept `definition` from a raw requirement or an explicitly targeted Issue. Require the exact authoritative URLs described by the selected phase for every later role.

Reject a missing, ambiguous, aliased, or unknown role. Do not infer an operation from repository state, URLs, prior chat, or a hand-off. Treat `external-review` as a stopping destination, not as an executable Harness role.

## Load exactly one operation

Select one row, read its operation reference completely, then read only the supporting references named in that row. Do not load any other operation, transport, or artifact-contract reference during the invocation.

Internal GitHub transport protocols:

- **Issue transport:** `references/issue-transport.md`
- **Pull Request transport:** `references/pull-request-transport.md`

Shared artifact contracts:

- **Issue contract:** `references/issue-contract.md`
- **Product PR contract:** `references/product-pr-contract.md`

| Exact role | Operation reference | Supporting references | Authoritative input | Persistent success output | Success destination | Recovery or re-entry |
| --- | --- | --- | --- | --- | --- | --- |
| `init` | `references/init.md` | None | Exact project-owned marker namespace, or an existing valid Harness config | Created or read-back-verified `.project-harness/config.yaml` | `definition` or no further action | `init` after correcting a missing, invalid, or conflicting input |
| `definition` | `references/definition.md` | Issue transport; Pull Request transport; Issue contract | Raw or changed requirement; optional explicitly targeted Issue | Independently reviewed and read-back-verified Issue | `context-authoring` or `implementation` | `definition` when the contract later changes |
| `context-authoring` | `references/context-authoring.md` | Issue transport; Pull Request transport; Issue contract | Finalized Issue requiring the pre-implementation durable-decision gate | Verified existing decision source or Ready proposed-decision PR | `implementation` after the decision source is merged, or `external-review` | `definition`; `context-authoring` to resume blocked work or verify merge |
| `implementation` | `references/implementation.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Finalized Issue; merged decision source when required | Independently read-back-verified Draft product PR | `closeout` | `definition`; `implementation` to resume blocked work |
| `closeout` | `references/closeout.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Finalized Issue and Draft product PR | Accepted Ready product PR plus project-memory promotion eligibility | `external-review` | `implementation`, `definition`, or `closeout` to resume blocked/repaired work |
| `context-promotion` | `references/context-promotion.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract | Issue and eligible merged product PR | Verified `no-promotion` callback or Ready project-memory-only PR, plus the source Issue closure judgment | `external-review` or no further action | `context-promotion` to resume blocked work, reconcile a merged project-memory PR, or execute a pending source Issue closure |

`init` is a setup operation, not a lifecycle phase. Stop at the selected operation boundary. Express a legal phase transition as a hand-off packet for a new clean session invoking `project-harness` with the next exact role; never continue by loading the next reference in the current session.

## Load project-owned configuration

- Treat `.project-harness/config.yaml`, relative to the project root, as the sole source of project-specific Harness configuration. Keep it outside the Skill directory so Skill synchronization does not overwrite it.
- Require `schema_version: 1` and one `marker_namespace` value. The namespace must be a lowercase kebab-case ASCII slug of 1–63 characters matching `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Before any lifecycle phase, read and validate the config. If it is missing, invalid, unsupported, or ambiguous, fail closed and hand off to an explicit `role: init`; do not infer a namespace from the directory, repository name, remote URL, Issue, or prior callback.
- Resolve every `${marker_namespace}` token in the selected phase reference to the exact configured value before searching, comparing, producing, or verifying a marker. Never persist the token itself.
- Once a callback containing the namespace has been persisted, `init` must not rename it. A namespace change requires a separately approved compatibility migration with verified dual-read behavior.

## Enforce shared contracts

- Use a clean session for every role after `definition` and for every independent Reviewer.
- Treat the Issue as the delivery contract and the product PR as implementation result and evidence. Store durable knowledge only in the single authoritative layer defined by the Harness document-placement contract and applicable repository rules.
- Pass only `role`, authoritative Issue/PR or exact durable-source URLs, phase-required evidence URLs such as an acceptance comment, and `next_action` across sessions. Do not depend on chat summaries or implicit memory.
- Within a Harness phase, follow only the loaded internal Issue and Pull Request transport protocols for GitHub mutations, digest normalization, baseline protection, and independent read-back. Do not invoke a separate GitHub transport Skill, mix in a generic PR workflow, or use a second authenticated transport.
- Accept only `verified` or `no-op` transport results; fail closed on partial, ambiguous, `blocked`, `indeterminate`, or mismatched results.
- Bind every decision or verdict to the fields required by its phase, including Issue Body digest, PR Body digest, head SHA, base ref/SHA, and comment URL/digest when applicable. Invalidate stale review or acceptance when a bound field changes.
- Before completing a phase, establish every authoritative repository fact and durable source required by that phase. Stop and report the missing evidence when a required fact cannot be established; never treat `proposed` material as verified behavior.
- Use the shared Issue contract as the only Issue Body schema. Use the shared Product PR contract only for the product PR handled by `implementation`, `closeout`, and `context-promotion`. Build proposed-decision and project-memory-only PR Bodies from the selected phase reference instead. Do not look for or maintain `.github` copies of either contract.

## Bind repository policy

- Use `develop` as the product and project-memory integration base. Reserve `main` for the repository's release/hotfix flow.
- A current user message that explicitly invokes `$project-harness` with one exact role supplies authority only for the mutations enumerated by that role reference. An automatic route, prior hand-off, ordinary feature request, or earlier session does not supply mutation authority.
- Never infer merge authority. Every role stops before merge, and commit messages must not contain `Co-Authored-By`.
- Map durable categories to the existing authority layers: decisions to `docs/decisions/`, stable rules to `docs/rules/active/`, explanations to `docs/wiki/`, continuity to `.project-memory/`, and technical facts to code/contracts/tests/configs.

## Preserve persistent markers

Keep the configured namespace and these workflow-owned suffixes stable across Skill refactors because GitHub callbacks and idempotency checks depend on them:

| Marker template | Producer role | Consumer role |
| --- | --- | --- |
| `${marker_namespace}:context-authoring` | `context-authoring` | `implementation` |
| `${marker_namespace}:context-promotion-eligible` | `closeout` | `context-promotion` |
| `${marker_namespace}:context-promotion` | `context-promotion` | `context-promotion`; conflict checks in `closeout` |

Do not rename a marker after the first persisted callback unless a separately approved compatibility migration implements and verifies dual-read behavior.
