# Express

Execute this operation only after `project-harness` dispatches a current explicit `role: express` invocation, or the user confirmed the express path for the current request under the root Skill's path-selection protocol.

Carry one small, low-risk change from an oral requirement to a merged pull request at conversational speed: no Issue, no independent review phase, no Context Promotion flow.

## Contents

- Enforce the boundary
- Confirm the scope once
- Implement and test
- Open the lightweight PR
- Merge through the express gate
- Summarize

## Enforce the boundary

- Express serves ordinary business changes only. The protected surfaces defined by `references/issue-contract.md`—architecture or module boundaries, public APIs, DTOs or serialization, databases or migrations, message protocols, configuration formats, security or permissions, and core dependencies or frameworks—are absolutely forbidden here. The moment completing the request would touch one, stop before that mutation and tell the user the task must upgrade to path 1 (`role: spec`).
- Treat the current explicit invocation as authority to create one task branch, edit ordinary product code and tests, commit, push, create or update one PR, and merge it through the express gate below.
- Subagent use is unconstrained; verify any delegated read yourself.
- Never close or create Issues, never write durable project memory from this operation, and never work on `develop` or `main` directly.
- Fail closed: when required checks, mergeability, or the configured merge method cannot be established, return blocked rather than asking the user to merge manually.

## Confirm the scope once

1. Restate the requested change in one or two plain sentences: what changes, where, and the observable result.
2. State the path-2 trade-offs in one line: no Issue record, no independent review, no memory promotion.
3. Obtain the user's explicit confirmation once. When the user already confirmed the express path during path selection and the scope has not changed since, skip re-confirmation.
4. When the user cannot confirm, or the restated scope already shows a protected-surface change, stop and recommend path 1.

## Implement and test

- Create one task branch from `develop`. Preserve pre-existing user changes.
- Implement the confirmed scope completely—no more, no less.
- Write or update the unit tests that cover the changed behavior.
- Run the smallest verification set that covers the change: targeted unit tests first; broader checks only when the changed boundary or repository rules require them. Bind every reported result to the final head SHA.

## Open the lightweight PR

Create one PR targeting `develop` with this minimal Body (no five-category table, no Issue reference):

~~~markdown
## 需求

<一句话需求与用户确认的范围>

## 主要改动

- <实际改动>

## 验证证据

| 命令 / 检查 | 结果 |
| --- | --- |
| <可复现命令或检查> | <结果及关键证据，绑定最终 head SHA> |

## 已知限制与风险

- <限制或风险，或无>
~~~

Follow the loaded Pull Request transport protocol for creation, digest binding, and independent read-back. Mark the PR Ready once the Body and head are final.

## Merge through the express gate

Immediately before merge:

1. Re-read the PR title/Body digest, head ref/SHA, base ref `develop` and base SHA.
2. Require open non-Draft state, `required_checks_known: true` with every required check successful against the current head, affirmative mergeability, and the configured `product_pr` merge method still available in the repository.
3. Call the Pull Request transport's `merge` with `merge_kind: express`. The protocol-owned evidence set for express is exactly empty; do not invent evidence comments to fill it.
4. Independently read back merged state, exact tuple, merge method/provenance, and non-null merge commit identity. Accept only `verified` or exact `no-op`.

If the tuple drifts, the checks turn pending or fail, or mergeability becomes unknown, stop without merging and report the exact state.

## Summarize

Report:

~~~yaml
outcome: merged | upgraded-to-path-1 | blocked
pr_url: null
head_sha: null
merge_commit_sha: null
validation: []
memory_candidates: []
reason: null
~~~

- `memory_candidates` only suggests durable knowledge noticed during the work; Express never writes it. Offer to persist a candidate through a later `role: context-promotion` or a direct user request.
- For `upgraded-to-path-1`, name the protected surface that forced the upgrade and recommend `role: spec`.
