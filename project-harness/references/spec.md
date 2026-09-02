# Spec

Execute this phase only after `project-harness` dispatches `role: spec`.

Carry the Spec phase by turning a grilled, user-confirmed plan into the single delivery Issue that downstream phases can execute without access to the preceding conversation.

## Contents

- Enforce the boundary
- Require a grilled and confirmed plan
- Accept the initial semantic input
- Use the internal transports
- 1. Run the preflight
- 2. Draft the Issue
- 3. Bind and check the exact draft
- 4. Recheck and publish
- 5. Hand off and stop

## Enforce the boundary

- Start with the confirmed plan and finish only after the Issue has been written, read back, and handed off by URL.
- Treat the explicit invocation as authorization to create or update the Issue after every gate passes. Do not request a final human publishing confirmation.
- Subagent use is unconstrained: spawn read-only explorers or a fresh-eyes reviewer whenever separate context materially helps, and integrate their results yourself. The Harness fixes no topology, delegation envelope, or review-round count.
- Do not implement product code, modify tests, create a Pull Request, or write durable project memory.
- Keep drafts and decision notes ephemeral. Persist task facts only in the delivery Issue.
- Fail closed whenever a required decision, platform write, or read-back verification is unavailable.

## Require a grilled and confirmed plan

The Spec phase writes the delivery contract; the decisions inside it must already be settled with the user.

- Require the current conversation to contain a plan that was stress-tested through persistent `grilling`-style questioning and explicitly confirmed by the user. Grilling means asking one pointed question at a time about goals, boundaries, failure semantics, compatibility, and acceptance—challenging vague answers until every material decision is stable—never a batch questionnaire.
- When the user invokes `spec` without such a confirmed plan, do not draft yet. First plan with the host's native planning capability, grill every material decision, obtain an explicit confirmation of the final plan, and only then continue this phase.
- Record the confirmed outcomes in the Issue's `已确认决策` table. A decision that materially changed during grilling appears with its final choice, reason, and `confirmed` status.
- For a clear and low-risk requirement whose plan is already confirmed, ask no further clarification question. Describe the allowed ordinary business change and write exactly `受保护改动：无`. Do not re-run grilling merely to produce a transcript, confirm reversible implementation details, or restate facts that are already authoritative.
- When a repository fact discovered during drafting newly reveals a contract-blocking decision, ask one decision at a time in plain language: state the current behavior, the proposed choice, who or what is affected, any compatibility or migration consequence, and the recommended choice. Do not bundle decisions.

Write every confirmed protected-change answer as one exact exception under the Issue's `受保护改动` field. Do not publish while a required exception remains unresolved, ambiguous, or broader than the user's decision. Protected changes absent from those explicit exceptions remain forbidden even when they appear useful to the proposed implementation.

Handle uncertainty conservatively:

- Mark contract decisions as `confirmed` before publication.
- Use `assumed` only for reversible, low-risk implementation details that do not change the delivery contract; record the risk and reopening condition.
- Use `deferred` only for future or currently uncontrollable matters that do not block this task; record the reopening trigger.
- When the user skips a contract-blocking question, stop without publishing.

## Accept the initial semantic input

Apply the root Skill's public-invocation adapter. Require an exact `role: spec` and the raw or changed requirement in the current user message. For an initial Spec, accept an optional explicitly targeted Issue URL; when the user intends to update an existing contract, require that exact Issue target in the current message. Otherwise define a new task only after duplicate checks.

## Use the internal transports

- Follow the loaded Issue transport protocol for repository resolution, Issue search and read, Body normalization and digesting, Issue create or update, and independent read-back verification. Do not duplicate its transport or consistency rules here.
- Follow the loaded Pull Request transport protocol only for the related Pull Request search and read evidence required by duplicate and completion checks.
- Retain responsibility for semantic duplicate classification, product decisions, and publication timing.
- Accept only a `verified` or `no-op` transport outcome whose Issue identity, title, Body digest, and read-back evidence match the checked draft. Stop on `blocked`, `indeterminate`, or any mismatch.

## 1. Run the preflight

1. Preserve a concise statement of the original problem, affected user, and desired outcome.
2. Update an Issue only when explicitly targeted; never select one from similarity alone.
3. Establish the authoritative repository facts needed to define the delivery contract, including relevant code, tests, decisions, rules, and durable sources. Find discoverable facts instead of asking the user. Stop and report the missing evidence when a required fact cannot be established.
4. Search open and closed Issues, and related Pull Requests separately, for duplicates, completed work, superseding tasks, and conflicting in-progress work. Compare the original problem, affected boundary, observable outcome, and acceptance effect rather than titles or proposed implementations.
5. Classify candidates as `duplicate`, `overlapping`, `related`, or `distinct`. Stop and report candidate URLs whenever a duplicate or target ambiguity requires a user decision.
6. Continue only when the target is explicit or the new task is distinct enough to create safely.

## 2. Draft the Issue

Use the shared Issue contract loaded for this role as the exact Body structure. Include:

- a concise original requirement and problem background, without copying the conversation;
- a verifiable goal and explicit non-goals;
- the compact `改动范围`: allowed ordinary business areas plus exactly `受保护改动：无` or only the specifically confirmed protected exceptions;
- only the authoritative repository facts actually used;
- non-binding post-merge durable-memory candidates classified as `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, or `milestone_evidence`;
- decisions with choice, reason, and status;
- an implementation plan describing affected system areas, ordered stages, dependencies, stage outcomes, and required tests;
- executable acceptance checks that cover the goal and boundaries.

Treat the goal, non-goals, boundaries, `改动范围`, confirmed decisions, constraints, and acceptance checks as the delivery contract. Treat the implementation plan as a non-binding starting prediction that Implementation may revise without returning to `spec` unless the revision changes the delivery contract. Never use the plan to imply permission for an unlisted protected change.

Avoid prescribing class names, function structure, or ordinary code choices unless they are confirmed architecture constraints. Do not promise future project-memory write-back; record post-merge candidates only as non-binding clues for `context-promotion`.

When updating an explicitly targeted Issue, build one complete replacement Body: preserve still-valid content, remove placeholders and superseded content, and leave comments, labels, assignees, milestones, and other metadata unchanged. When an open legacy task has no merged product Pull Request and is returned for a missing `改动范围`, add the compact subsection and rebind the complete Body. Do not rewrite an Issue solely to migrate this format after its product Pull Request has merged.

When creating a new Issue, set only the checked title and Body. Do not infer labels, assignees, or milestones.

## 3. Bind and check the exact draft

Follow the loaded Issue transport protocol to normalize the complete Body and calculate its SHA-256 digest. Treat any title or Body change as a new draft requiring a new digest and a new check.

Perform a deterministic completeness check against the confirmed plan, authoritative sources, and the exact Issue contract. Require complete headings, a non-placeholder compact `改动范围`, no placeholders, traceable facts, executable acceptance, and no contradiction, unresolved contract decision, or implied protected permission.

For a high-risk contract—security or privacy behavior, destructive data or migration semantics, externally consumed compatibility changes, difficult-to-reverse architecture, or a broad operational blast radius—a fresh-eyes review is recommended: start one clean read-only subagent against the exact draft digest and integrate its verdict before publishing. The choice and the accountability remain yours.

## 4. Recheck and publish

Immediately before publishing, repeat the semantic duplicate and target-state check. Stop if a new duplicate, conflict, completion, supersession, or target mismatch appears.

Use the loaded Issue transport protocol to publish only the exact title and Body that passed the check. Declare all unrelated Issue metadata as protected baseline fields.

Require the returned transport envelope to report `verified` or `no-op`, the expected Issue identity and title, the checked Body digest, protected-field preservation, and successful independent read-back. Any other outcome means the phase is incomplete even if the platform may have accepted part of the operation. Report the exact state and do not claim success.

## 5. Hand off and stop

After successful read-back verification, output one minimal hand-off:

- the read-back-verified Issue URL;
- `role: delivery` as the normal next action, noting that a code-only result whose five durable-memory categories are all verified `无` completes without a Context Promotion confirmation round, while any actual promotion candidate requires a later explicit source-bound re-entry;
- `role: implementation` only when the caller explicitly chose the phase-by-phase path.

Do not copy the Issue Body into the hand-off. Do not start implementation.

If Implementation or Review later discovers a fact that changes the goal, boundaries, external behavior, difficult-to-reverse architecture, acceptance contract, or requires any protected change not explicitly allowed by `改动范围`, the delivery chain stops and hands the same Issue back to an explicit `role: spec`. Re-run the gates above, update the original Issue, and avoid creating a parallel task.
