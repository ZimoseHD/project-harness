# Definition

Execute this phase only after `project-harness` dispatches `role: definition`. Run the selected role as the Definition Phase Owner; the exact public role name remains `definition`.

Carry the Definition phase by turning an original requirement into the single GitHub Issue that a clean downstream Phase Owner can execute without access to the preceding conversation.

## Contents

- Enforce the boundary
- Accept the initial semantic input
- Delegate GitHub Issue operations
- Capture the request and run the preflight
- Clarify only blocking decisions
- Draft the Issue
- Bind and gate the exact draft
- Recheck and publish
- Hand off and stop

## Enforce the boundary

- Start with the original request and finish only after the reviewed Issue has been written, read back, and handed off by URL.
- Treat the explicit invocation as authorization to create or update the Issue after every gate passes. Do not request a final human publishing confirmation.
- Apply the root Skill's fixed two-hop delegation topology. The Definition Phase Owner may directly delegate narrow read-only work and each independent review round, but every Worker and Reviewer must remain mutation-free, must not delegate further, and must return only to this Owner.
- Keep the Definition Phase Owner as the sole phase writer and the sole producer of the persistent Issue and phase hand-off. A Worker or Reviewer cannot publish, edit, or hand work directly to the next phase.
- Continue the same semantic round in the same Phase Owner after a Worker failure or Reviewer FAIL. Replace the Owner only when a bound authoritative input or semantic target changes, the Owner explicitly terminates, or its context cannot be recovered.
- Do not implement product code, modify tests, create a Pull Request, or write durable project memory. Route a required pre-implementation durable-decision change to a new `project-harness` invocation with `role: context-authoring` after Issue publication.
- Keep drafts, decision packets, and review packets ephemeral. Persist task facts only in the GitHub Issue.
- Fail closed whenever a required decision, a risk-triggered independent Reviewer, GitHub write, or read-back verification is unavailable.

## Accept the initial semantic input

Apply the root Skill's public-invocation adapter. Require an exact `role: definition` and the raw or changed requirement in the current user message. For an initial Definition, accept an optional explicitly targeted Issue URL; when the user intends to update an existing contract, require that exact Issue target in the current message. Otherwise define a new task only after duplicate checks. Do not require the user to reproduce an upstream hand-off envelope or supply placeholder routing metadata.

## Use the internal GitHub transports

- Follow the loaded Issue transport protocol for repository resolution, Issue search and read, Body normalization and digesting, Issue create or update, and independent read-back verification. Do not duplicate its transport or consistency rules here.
- Follow the loaded Pull Request transport protocol only for the related Pull Request search and read evidence required by duplicate and completion checks.
- Supply the exact repository and target, the explicit publication authority from this Skill, the reviewed title and complete Body, the expected Body digest, and the fields that must remain unchanged.
- Retain responsibility for semantic duplicate classification, related Pull Request search, product decisions, risk classification, any required Reviewer gating, and publication timing.
- Accept only a `verified` or `no-op` transport outcome whose Issue identity, title, Body digest, and read-back evidence match the reviewed draft. Stop on `blocked`, `indeterminate`, or any mismatch.

## 1. Capture the request and run the preflight

1. Preserve a concise statement of the original problem, affected user, and desired outcome before discussing solutions.
2. Determine whether the invocation explicitly targets an existing Issue number or URL. Update an Issue only when explicitly targeted; never select one from similarity alone.
3. Establish the authoritative repository facts needed to define the delivery contract, including relevant code, tests, decisions, rules, and durable sources. Stop and report the missing evidence when a required fact cannot be established. Find discoverable facts instead of asking the user.
4. Follow the loaded Issue transport protocol to search open and closed Issues, and the loaded Pull Request transport protocol to search related Pull Requests separately, for duplicates, completed work, superseding tasks, and conflicting in-progress work. Compare the original problem, affected boundary, observable outcome, and acceptance effect rather than relying on titles or proposed implementations.
5. Classify candidates as `duplicate`, `overlapping`, `related`, or `distinct`. Stop and report candidate URLs whenever a duplicate or target ambiguity requires a user decision. Do not create or update anything.
6. Continue only when the target is explicit or the new task is distinct enough to create safely.

## 2. Clarify only blocking decisions

First classify whether the requirement is clear and low-risk from the current request and discoverable repository facts. Treat it as clear and low-risk only when the observable goal, boundaries, compatibility effect, and executable acceptance are unambiguous, and no unresolved choice affects data migration, security, an external contract, a difficult-to-reverse architecture decision, or a broad operational blast radius.

For a clear and low-risk requirement, ask no clarification question. Do not run `/grilling` merely to produce a decision transcript, confirm reversible implementation details, or restate facts that are already authoritative.

When one or more unresolved decisions can change the delivery contract, run the installed `/grilling` behavior only for those decisions. Ask one decision question at a time, wait for the answer, and include a recommended answer with its reason. Ask only about decisions that can change:

- user-observable behavior or compatibility;
- system boundaries and non-goals;
- data, failure, security, or operational semantics;
- difficult-to-reverse architecture choices;
- acceptance and validation outcomes.

Stop as soon as every remaining question can be delegated to the Implementation Phase Owner without changing any item above. Do not continue into implementation design or action. Treat a discoverable fact as an investigation task rather than a user question.

Handle uncertainty conservatively:

- Mark contract decisions as `confirmed` before publication.
- Use `assumed` only for reversible, low-risk implementation details that do not change the delivery contract; record the risk and reopening condition.
- Use `deferred` only for future or currently uncontrollable matters that do not block this task; record the reopening trigger.
- When the user skips a non-blocking question, record it as `deferred` and continue.
- When the user skips a contract-blocking question, stop Finalization without publishing.

Form an ephemeral Issue-ready decision packet containing the original request, refined goal, non-goals, relevant facts, any confirmed decisions and reasons, permitted assumptions or deferrals, and acceptance expectations. For the zero-question path, omit artificial decision rows instead of inventing choices to make the packet look complete.

Classify pre-implementation Context Authoring as `required` only when one settled decision satisfies every condition and belongs in a proposed ADR:

- it belongs to architecture, a domain model, a protocol/interface contract, a system boundary, or a project-level technology choice;
- it applies beyond the current Issue;
- another task must consume it before the current product PR merges;
- omission creates a concrete divergence, rework, correctness, safety, or compatibility risk.

Classify all other cases as `not-required`. Do not treat feature design, implementation plans, ordinary code choices, speculative alternatives, or post-merge reuse alone as sufficient.

## 3. Draft the Issue

Use the shared Issue contract loaded for this role as the exact Body structure.

Include:

- a concise original requirement and problem background, without copying the conversation;
- a verifiable goal and explicit non-goals;
- only the authoritative repository facts actually used;
- the durable-memory impact classification, four-condition evidence or explicit non-applicable reason, and non-binding post-merge candidates classified as `decision`, `stable_rule`, `wiki_knowledge`, `stable_context`, or `milestone_evidence`;
- decisions with choice, reason, and status;
- an implementation plan describing affected system areas, ordered stages, dependencies, stage outcomes, and required tests;
- executable acceptance checks that cover the goal and boundaries;

Treat the goal, non-goals, boundaries, confirmed decisions, constraints, and acceptance checks as the delivery contract. Treat the implementation plan as a non-binding starting prediction that the Implementation Phase Owner may revise without returning to Definition unless the revision changes the delivery contract.

Avoid prescribing class names, function structure, or ordinary code choices unless they are confirmed architecture constraints.

Do not promise future project-memory write-back. Record post-merge candidates only as non-binding review clues. Leave verified all-`无` fast-path eligibility to Closeout and any actual durable-write classification to Context Promotion after the product PR merges.

When updating an explicitly targeted Issue, treat its current Body as input and build one complete replacement Body. Preserve still-valid content, remove placeholders and explicitly superseded content, and leave comments, labels, assignees, milestones, and other metadata unchanged.

When creating a new Issue, set only the reviewed title and Body unless the original request or repository rules explicitly provide metadata. Do not infer labels, assignees, or milestones.

## 4. Bind and gate the exact draft

Follow the loaded Issue transport protocol to normalize the complete Body and calculate its SHA-256 digest. Bind the exact title and normalized Body to that digest. Treat any title or Body change as a new draft requiring a new digest and a new applicable draft gate.

For a clear and low-risk contract, have the Definition Phase Owner perform a deterministic completeness check against the original requirement, authoritative sources, and the exact Issue contract. Require complete headings, no placeholders, traceable facts, executable acceptance, and no contradiction or unresolved contract decision. This is the normal lean path and does not require an independent Reviewer.

Require an independent Reviewer when the contract is high-risk or material clarity remains difficult to establish after targeted clarification. Triggers include security or privacy behavior, destructive data or migration semantics, externally consumed compatibility or protocol changes, difficult-to-reverse architecture, a broad operational blast radius, human-only acceptance, or reasonable doubt that the draft faithfully closes a material ambiguity. Do not create a Reviewer merely because the task has multiple files, uses a new technology, or has a long implementation plan.

When review is required, have the Definition Phase Owner directly start one new clean, read-only Reviewer for each review round. Never replace required independent review with Owner self-review. Give the Reviewer only this structured packet:

- original requirement summary;
- confirmed decisions and reasons;
- exact Issue title and Body;
- Body digest;
- directly cited authoritative repository sources;
- the durable-memory impact classification and its gate evidence;
- duplicate-check evidence.

Do not give the Reviewer the complete grilling conversation or prior review discussions. Allow read-only verification of the packet and its cited authoritative sources. Forbid exploration unrelated to the review packet.

Constrain the Reviewer to pure review:

- forbid edits to the draft, repository, or GitHub;
- forbid further delegation or any hand-off outside the Definition Phase Owner;
- forbid alternative designs, repair actions, and non-blocking wording suggestions;
- require a structured, non-persistent `PASS` or `FAIL` verdict for the exact digest, returned only to the Definition Phase Owner;
- on `FAIL`, require only the violated criterion, evidence location, and impact for each blocker.

Require the Reviewer to check:

1. fidelity to the original request and confirmed grilling decisions;
2. observable goals and explicit non-goals or boundaries;
3. traceable authoritative repository facts, without treating `proposed` material as confirmed;
4. confirmation of every delivery-contract decision and valid use of `assumed` or `deferred`;
5. an actionable but implementation-agnostic plan covering the goal and required tests;
6. executable acceptance checks covering the goal and boundaries;
7. correct pre-implementation Context Authoring classification and separation of feature design from a durable architecture/technology decision;
8. absence of placeholders, contradictions, duplicates, target-Issue mismatch, and promised post-merge memory write-back.

Route a failed review according to the blocker:

- Fix drafting defects in the same Definition Phase Owner.
- Stop or return to the appropriate phase when required authoritative evidence remains unavailable.
- Return product decision gaps to targeted clarification, one question at a time.
- Stop on environmental or authority gaps.

After any correction on the reviewed path, calculate a new digest and let the same Definition Phase Owner directly start a new clean Reviewer. Allow at most three total review rounds. Stop without publishing when the third round fails. On the lean path, recalculate the digest and repeat the deterministic completeness check after every correction.

## 5. Recheck and publish

Immediately before publishing, repeat the semantic duplicate and target-state check. Stop if a new duplicate, conflict, completion, supersession, or target mismatch appears.

Use the loaded Issue transport protocol to publish only the exact title and Body that passed its applicable gate: either the deterministic clear-and-low-risk completeness check or a required independent Reviewer `PASS`:

- Create a new Issue only when no target was supplied and duplicate checks remain clear.
- Update the complete Body of the explicitly targeted Issue; update its title only when the reviewed draft intentionally changes it.
- Declare all unrelated Issue metadata as protected baseline fields.

Require the returned transport envelope to report `verified` or `no-op`, the expected Issue identity and title, the reviewed Body digest, protected-field preservation, and successful independent read-back. Any other outcome means Finalization is incomplete even if GitHub may have accepted part of the operation. Report the exact state and do not claim success.

## 6. Hand off and stop

After successful read-back verification, the Definition Phase Owner outputs one minimal hand-off:

- When pre-implementation Context Authoring is `required`, include the GitHub Issue URL, `role: context-authoring`, and the next action to invoke `project-harness` in a new clean session.
- When it is `not-required`, normally include the GitHub Issue URL, `role: delivery`, and the next action to start the automated Implementation → Closeout chain. State that a code-only result whose five durable-memory categories are all independently verified as `无` can complete without a Context Promotion confirmation round; if any category requires promotion, a proposal will be summarized at a turn boundary and requires the later explicit source-bound `delivery` re-entry supplied by that summary. Preserve `role: implementation` as an additive compatibility hand-off only when the caller explicitly chose the legacy phase-by-phase path.

Do not copy the Issue Body into the hand-off. Do not start implementation.

If Implementation later discovers a fact that changes the goal, boundaries, external behavior, difficult-to-reverse architecture, or acceptance contract, stop the delivery chain and hand the same Issue back to an explicit `role: definition`. Re-run the applicable gates, update and re-review the original Issue, and avoid creating a parallel task.
