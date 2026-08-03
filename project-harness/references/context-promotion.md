# Context Promotion

Execute this phase only after `project-harness` dispatches a standalone `role: context-promotion` or the current `delivery` coordinator delegates the Context Promotion phase under the root Skill's scoped envelope. Run the selected role as the Context Promotion Phase Owner; the exact public and delegated role name remains `context-promotion`.

Assess durable context after an eligible product Pull Request merges. Enter the strict proposal/review/confirmation workflow only when at least one real durable-memory write remains or persisted promotion state must be resumed. A proven Lean code-only source normally skips this phase; if invoked, return direct `no-promotion`. For a first candidate round whose complete classification is all `no_write`, also return direct `no-promotion` without creating promotion artifacts or a cross-turn gate. Promote cross-task knowledge only when forgetting it would cause repeated decisions, an incorrect capability judgment, or concrete correctness, safety, compatibility, or delivery risk.

## Contents

- Enforce the phase boundary
- Accept the public semantic input
- Route Lean admission or existing lineage
- Acquire exact source evidence
- Verify the source and promotion state chain
- Classify promotable knowledge
- Calculate the review tier
- Build the exact proposal
- Revalidate an advanced base proportionally
- Persist the exact proposal artifact
- Require independent review
- Persist and relay the confirmation gate
- Apply modification requests and promotion-scope repairs
- Complete confirmed no-promotion
- Mark a confirmed project-memory PR Ready
- Reconcile a merged project-memory PR
- Judge source Issue closure
- Return a bound phase result

## Enforce the phase boundary

- Start only from one Issue URL and one merged product PR URL supplied by either a current explicit Context Promotion invocation or a host-provenance-bound delegation from the current explicit `delivery` invocation.
- Use a fresh isolated Phase Owner context and require the product PR to be merged into `develop`; reject open, Draft, Ready-but-unmerged, closed-unmerged, or vaguely validated sources.
- Apply the root Skill's fixed two-hop delegation topology. The Context Promotion Phase Owner may directly delegate narrow read-only evidence, authority, and validation work plus each independent review round; every Worker and Reviewer must remain mutation-free, must not delegate further, and must return only to this Owner.
- Keep the Context Promotion Phase Owner as the sole phase writer and sole producer of proposal artifacts, Reviewer PASS evidence, state callbacks, branch/PR mutations, and the phase hand-off.
- Continue the same semantic proposal or reconciliation round in the same Phase Owner after a Worker failure or Reviewer FAIL. Replace the Owner only when a bound authoritative input or semantic target changes, the Owner explicitly terminates, or its context cannot be recovered.
- Treat the Issue, merged PR, acceptance record, tests, exact durable sources, persisted promotion state, and explicit proposal-bound user decision as evidence.
- Treat a current standalone invocation as authority for the branch, commit, push, Draft project-memory PR, comments, Ready-state mutations, and source Issue close mutation enumerated here. Under `delivery`, accept only the mutations in the delegation envelope; the coordinator retains both PR merge operations and final Issue closure.
- Write only the smallest authority-layer files selected by project-memory governance on one dedicated branch based on `develop`.
- Require a source-head-bound eligibility registration. Produce a verified proposal before user confirmation only for a write candidate or a persisted lineage whose existing protocol requires proposal reconciliation.
- Never modify product code, tests, the source Issue Body, the merged product PR Body, root/child `AGENTS.md`, or current task continuity.
- Never copy single-task tracking, conversation history, or implementation chronology into durable memory.
- Treat every `record_kind: delivery-stage-observation` Issue comment as audit-only single-task chronology. Never use it as source evidence, current authority, confirmation, promotion input, closure authority, or a candidate for durable memory.
- Never commit directly to `develop` or `main`, never merge a PR, and never approve a proposal on the user's behalf.

Return awaiting-confirmation, verified-memory-pr, memory-pr-merged, no-promotion, return-to-definition, or blocked.

## Accept the public semantic input

Apply the root Skill's public-invocation adapter. For a standalone entry, require an exact `role: context-promotion`, one Issue URL and one merged product PR URL in the current user message. Treat those URLs as semantic sources whether they appear in prose or an optional structured carrier; do not require the caller to reproduce a generated hand-off envelope.

When delegated by `delivery`, require the root Skill's compact schema-v3 envelope with `delegated_role: context-promotion`. Depending on the current state, require separate bound product-PR and memory-PR snapshots plus exact acceptance, eligibility, proposal, confirmation, Reviewer PASS, or merge evidence comments. Dual-read schema-v2 with its already-carried legacy Bundle and schema-v1 through the fresh-read fallback only for an in-flight historical dispatch; never require or emit either form for new work. For any approval, revision, or pause confirmation round, require the host-provenance-bound `user_decision` fields derived from the current explicit `role: delivery` confirmation re-entry. For standalone, require those fields directly in the current explicit `role: context-promotion` re-entry. Verify their proposal URL/digest against the sole active state before use and apply the root Skill's layered freshness rules before relying on cached content.

Do not accept chat summaries or Delivery stage observations as promotion evidence. Treat modification text relayed from the current explicit source-bound confirmation response only as a request to build a new proposal, never as authority to patch files directly.

## Route Lean admission or existing lineage

Perform one complete source-PR comment read and related-PR search before selecting a path. Treat any current or legacy promotion callback, proposal artifact, Reviewer PASS, confirmation, Ready/terminal callback, supersession record, or source-linked project-memory PR as persisted promotion state.

Select exactly one route:

1. **Existing lineage:** when any persisted promotion state exists, reconstruct the complete active lineage and resume only the normal, repair, or legacy transition defined in `references/delivery-evidence-contract.md`. Never apply the Lean shortcut to an existing `awaiting-confirmation`, `confirmed`, Ready, terminal, orphaned proposal/review, memory-PR, or legacy lineage, even when the current PR Body now reports five `无` rows.
2. **Lean code-only:** when no persisted promotion state exists and the shared evidence contract's Lean code-only admission is fully proven, return `no-promotion` directly. Do not create a proposal artifact, Reviewer PASS, promotion-marker callback, branch, commit, project-memory PR, confirmation request, terminal callback, or Delivery observation. Under `delivery`, return `coordinator_action: close-issue`; standalone continues to the ordinary Issue closure mutation in this invocation.
3. **New candidate round:** when no persisted promotion state exists but at least one independently supported durable-memory candidate signal remains, classify it. If one or more write items remain, continue through the strict write proposal/review/source-bound-confirmation path below. If the complete five-category classification resolves to all `no_write`, return direct `no-promotion` with the same no-artifact/no-confirmation behavior as route 2, but identify the result as `direct-no-promotion-all-no-write` rather than claiming Lean admission.

For route 3 direct no-promotion, independently prove every candidate is code-discoverable, duplicate, or lacks recurring value; bind the unchanged source tuple; and reverify the complete absence of promotion state and source-linked memory PR. It does not require rewriting the accepted Product PR into the five-`无` code-only shape. Missing or ambiguous absence, source, classification, or authority evidence is blocked.

## Acquire exact source evidence

For every new schema-v3 delegation and every standalone entry, independently acquire the complete Issue, source PR, diff, checks, required workflow comments, related-PR search, and applicable authority sources through the loaded transports. A compact delegation tuple or hand-off is a binding/search hint, not a substitute for those reads. Before proposal relay, confirmation, Ready, terminal reconciliation, direct no-promotion result, or closure, apply `L1 semantic-freshness` to the exact mutable identities needed by that boundary. Fetch complete content again only for a changed, missing, challenged, or unverifiable binding. Keep transport-owned `L2 atomic-mutation-guard` reads and coordinator-owned `L3 irreversible-gate` reads unchanged.

Only when resuming a pre-Lean schema-v2 delegation that already carries an operation-local Evidence Bundle, validate and consume that Bundle under the frozen legacy v2 rules: independently derive its expected round binding and component identities from the outer envelope, require the applicable complete Issue/PR/diff/check/comment/authority/memory components, and never reconstruct expectations from the Bundle itself. Do not construct, extend, or require a Bundle for a new delegation. A delegated schema-v1 compatibility envelope and any missing, malformed, incomplete, or unverifiable legacy Bundle use complete fresh reads.

For a legacy Bundle, treat a semantic digest, authority blob, active lineage, memory tuple, or changed-file identity change as invalidating its affected cached payload. Treat checks, mergeability, permissions, or expected Draft/Ready/merged state changes as liveness changes unless repairing them changes content or the bound tuple. Do not restart classification for a liveness-only change.

## Verify the source and promotion state chain

1. Use complete loaded-Issue-transport evidence, or an unchanged payload from an already validated legacy Bundle, to establish the exact Issue.
2. Use complete loaded-Pull-Request-transport evidence, or an unchanged payload from an already validated legacy Bundle, to establish the exact product PR, merged state, refs, Body, acceptance comments, and source callbacks.
3. Verify that the PR belongs to the same repository task and that the accepted exact head merged into `develop`.
4. Bind the Issue Body digest, source PR title/Body digest, source head ref/SHA, accepted base ref/SHA, and merge identity.
5. Search top-level source PR comments for the deterministic eligibility registration and every Context Promotion state callback tied to the source PR and source head.

For a current-format eligibility lineage, whether delegated or standalone, also require non-Draft merged state, transport-verified merge provenance bound to the accepted head/base lineage, an actual merge method equal to the bound Harness integration policy (`integration.product_pr.merge_method` for schema-v2, or the sole authoritatively available method captured by schema-v1 compatibility preflight), and `required_checks_known: true` with every required check currently successful for the exact source head. Do not require post-merge mergeability. These are read-only source-admission checks; only the `delivery` coordinator may initiate or recover a current-format merge mutation.

Use the exact eligibility and promotion marker forms, artifact schemas, author rules, predecessor relationships, active-tip definition, and legacy dual-read gates in `references/delivery-evidence-contract.md`. Validate the current source against that shared contract before choosing any phase action; a marker match or phase hand-off is never enough.

Apply only the normal, repair, and legacy migration chains defined by the shared evidence contract. Re-evaluate all five durable categories for a new revision. An older confirmation or Ready branch explicitly invalidated by the active repair chain remains audit evidence and cannot authorize merge or closure.

An unmerged product PR with only a valid legacy eligibility lineage cannot enter the automatic product merge gate. Route it to a fresh Closeout round, which creates the one permitted schema-v2 successor after current acceptance. A product PR already merged under the historical protocol may use the independently verified legacy lineage only as evidence for the confirmation migrations defined below.

An exact legacy terminal with an already closed Issue is a completed no-op after every shared-contract check. When the Issue is open, reconstruct a complete schema-v2 proposal, persist a fresh Reviewer PASS, summarize it, and obtain a later explicit source-bound confirmation before any new merge or close. Apply the same rule to unmerged or already merged legacy `memory-pr-ready`. A malformed schema-v2 callback is never legacy.

## Classify promotable knowledge

Evaluate each candidate against the classifications and destinations below. Establish the applicable repository authority and existing authoritative statement needed to detect conflict or duplication. Fail closed when classification, destination, or authority cannot be established.

Promote a candidate only when:

- merged implementation, final acceptance, tests, contracts, or an explicit human decision support it;
- it applies beyond the completed task;
- forgetting it would cause repeated decisions, an incorrect capability judgment, or concrete risk;
- it has exactly one correct classification and authoritative destination;
- it is absent from current authority or materially supersedes one statement;
- links can preserve traceability without copying the same fact into another layer.

Do not promote conversation history, task chronology, branch names, commit lists, review rounds, transient debugging notes, generic model knowledge, complete Issue/PR summaries, speculative future work, or implementation details already discoverable from code without recurring decision value.

Classify Delivery stage observations as `no_write` without copying them into the proposal artifact. Their timing, attempt history, and change summaries are delivery telemetry, not milestone evidence or stable context.

Apply the repository classifications exactly:

| Classification | Promote only | Authoritative destination |
| --- | --- | --- |
| `decision` | Long-term architecture/product decision confirmed by the source contract, evidence, or the exact source-bound user confirmation | `docs/decisions/ADR-*.md` |
| `stable_rule` | Durable project/module guardrail whose omission creates recurring risk | `docs/rules/active/*.rules.md` |
| `wiki_knowledge` | Explanatory onboarding or module knowledge with links to authority | `docs/wiki/*.md` |
| `stable_context` | Long-lived project identity/background, not technical truth or current work | `.project-memory/context_brief.md` |
| `milestone_evidence` | Important verified milestone or capability evidence | `.project-memory/daily_logs/YYYY-MM-DD.md` |
| `no_write` | Facts already discoverable from code/tests/contracts or lacking durable value | no repository write |

Never use `.project-memory/rolling_summary.md` for promotion. Mark retained but not fully verified claims `proposed` only in a layer whose lifecycle supports that status; never present them as confirmed.

A project-wide hard-rule change or ADR whose exact decision was not already confirmed by bound evidence must keep its normal `stable_rule` or `decision` classification and set `confirmation_requirement: explicit-user-decision`, with consequences and the source gap explicit. Draft the exact final status/content that would become authoritative if merged; a Draft branch is not authority. User approval authorizes integration of that unchanged tuple, so confirmation must not require a post-approval content or lifecycle-status edit. A general `delivery` or standalone promotion invocation is not confirmation.

Use the source PR's `持久项目记忆实际影响` table as a candidate index, not as promotion authority. The exact five literal `无` values plus the bound Closeout acceptance item may establish Lean admission only under the shared evidence contract's complete gate. Any other value is a candidate signal, not automatic promotion. Verify every category independently and inspect omitted categories when the diff or acceptance exposes a material effect.

## Calculate the review tier

Calculate one deterministic tier per proposal item after its classification, action, destination, authority, and confirmation requirement are established. A higher tier changes evidence breadth and semantic review depth only; it never removes the fresh independent Reviewer, source-bound user confirmation, exact tuple/digest binding, required checks, merge gate, or closure gate.

Apply this base mapping:

| Tier | Item condition | Review purpose |
| --- | --- | --- |
| `r0-no-write` | A `no_write` item inside a write proposal, or a persisted lineage that must complete the historical no-write protocol | Prove complete category coverage and a supported omission/no-write reason. |
| `r1-documentary` | A write classified as `wiki_knowledge` or `milestone_evidence` | Verify explanatory fact accuracy, traceability, placement, links, daily-log structure, and absence of normative authority. |
| `r2-stable-context` | A write classified as `stable_context` | Verify long-lived project identity/background, lifecycle, conflict handling, and separation from technical truth or current work. |
| `r3-normative` | A write classified as `decision` or `stable_rule` | Verify normative authority, source gaps, consequences, compatibility/safety effects, lifecycle, and the full repository governance surface. |

In compact form, `r0-no-write` maps to `no_write`, `r1-documentary` maps to `wiki_knowledge` / `milestone_evidence`, `r2-stable-context` maps to `stable_context`, and `r3-normative` maps to `decision` / `stable_rule`.

Raise an item to at least `r2-stable-context` for `action: supersede`, a removed or renamed authority file, a prior memory-PR supersession, or an authority conflict that is being resolved. Raise the complete proposal to `r3-normative` for `confirmation_requirement: explicit-user-decision`, any legacy reconciliation or reassessment, an ADR/active-rule lifecycle or discovery-route change, or a higher repository-governance minimum. A classification of `no_write` with a write action is malformed.

Set `effective_review_tier` to the maximum item tier and every global escalation. For a mixed proposal, keep one proposal, one memory PR when applicable, one fresh Reviewer, and one confirmation gate; review each item with its own checklist and de-duplicate common evidence acquisition. Do not force unrelated documentary items through normative semantic analysis merely because another item is R3.

Fail closed when the tier cannot be calculated, a destination or authority is ambiguous, the proposed item IDs cannot map exactly to destinations/diff hunks, or repository governance requires an unknown review policy. Increasing the tier never substitutes for missing authority or evidence.

## Build the exact proposal

Build the proposal before presenting the turn-ending confirmation summary.

For every category, record:

- a stable item ID;
- action `add`, `update`, `supersede`, or `no_write`;
- classification;
- exact destination path or no destination;
- exact conclusion to add, change, or supersede;
- confirmation requirement `source-confirmed` or `explicit-user-decision`, and the authority effect of integration;
- source evidence URLs and bound digests;
- current authoritative source path/URL, digest, statement, and duplication/conflict result;
- concrete omission risk or category-specific no-write reason.

Synchronize and bind the current `develop` authority base before a write proposal or an existing-lineage repair. For a first new candidate round, when every category is `no_write`, stop here and return direct `no-promotion` under **Route Lean admission or existing lineage**; do not persist the assessment or continue to independent review. Only a persisted lineage whose historical protocol already requires a no-write proposal continues with a complete no-write assessment against that base.

When one or more items require a write:

1. Synchronize `develop` after the product merge and bind its SHA.
2. Create or resume one dedicated project-memory branch associated with the source PR.
3. Preserve unrelated worktree changes.
4. Update the smallest correct authority-layer files and use links instead of copied facts.
5. Split a multi-layer update by classification; keep each fact in one authoritative destination.
6. Update a wiki link or active-rule route only when discovery would otherwise fail and the repository update protocol allows it.
7. Keep the diff limited to `docs/decisions/`, `docs/rules/active/`, `docs/wiki/`, `.project-memory/context_brief.md`, and `.project-memory/daily_logs/`.
8. Validate applicable rules, lifecycle metadata, links, status, terminology, discovery coverage, and single-source-of-truth behavior.
9. Select validation proportionally to `effective_review_tier`. Do not run product Unit, Integration, or Coverage merely because an R1-only wiki/daily-log proposal exists. Run repository-required validation when active-rule metadata changes and obey every stricter repository rule.
10. Commit and push the exact project-memory-only change; omit `Co-Authored-By`.
11. Create or update one Draft project-memory PR through the loaded Pull Request transport, explicitly targeting `develop`.

The project-memory PR Body must include:

- source Issue and merged product PR links;
- source Issue/PR digests and source head/merge identity;
- each proposed conclusion, classification, destination, and evidence;
- any proposed decision confirmed, corrected, superseded, or left proposed;
- validation commands and results;
- confirmation that no product code, tests, current task state, or duplicate fact source is included.

Reference the source Issue with a plain `Refs`-style link. Never use a closing keyword.

## Revalidate an advanced base proportionally

Keep the exact current head/base tuple and final merge guard. When `develop` advances after a write proposal, separate tuple invalidation from validation invalidation instead of assuming that every prior local check is stale.

Before the first reusable validation, assign every selected validation a stable ID and a complete dependency-path set. Mark a validation global only when any repository change can affect it. Build an explicitly complete global-trigger-path inventory; treat dependency/lock files, toolchain and runtime configuration, test runners, Coverage configuration, CI workflows, generators, Harness/repository rules, and the validation inventory itself as global invalidation triggers. An incomplete global-trigger inventory forces `full`; an unknown completeness value is `blocked`.

On an advanced base:

1. Bind the prior proposal/Reviewer PASS URL/digest, prior and current head/base SHAs, complete prior and current changed-file/blob identities, and the prior persisted validation evidence.
2. Prove that the base relation is fast-forward and that the current base is an ancestor of the safely rebased current head. A non-fast-forward, unknown relation, unsafe/manual conflict, truncated diff, missing blob identity, or unavailable source is `blocked`.
3. Capture the complete non-truncated prior/current base-to-head promotion changed-file identities, including old/new paths and blobs. Derive both stable promotion-patch identities with `scripts/validation_impact.py::promotion_patch_sha256`; do not trust an opaque supplied digest or use cross-run `diff_sha256`.
4. Use `scripts/validation_impact.py` to intersect the complete base delta with every validation dependency path and the global trigger set.
5. Select exactly one impact mode:

| Impact mode | Required condition | Local validation action |
| --- | --- | --- |
| `reuse` | Equivalent promotion patch, complete dependency inventory, and no base-delta intersection | Reuse exact persisted local validation evidence and run only cheap tuple, path-allowlist, link, authority, and artifact checks. |
| `incremental` | Equivalent promotion patch and only a strict subset of validation IDs is affected | Re-run only the invalidated IDs plus the cheap checks. |
| `full` | Changed patch, global trigger, incomplete dependency inventory, or a change whose impact cannot be narrowed safely | Run the complete validation set required by the current review tier and repository rules. |
| `blocked` | Ancestry, tuple, diff/blob completeness, authority, or safe repair cannot be established | Reuse nothing and stop without changing confirmation or Ready state. |

Persist the exact markerless **Context Promotion validation-impact artifact** from `references/delivery-evidence-contract.md` for every reuse or incremental decision, and bind it into the new versioned Reviewer PASS. Keep retained evidence separate from `validation`: every ordinary `validation` entry still means a command actually executed for the current tuple.

A rebase changes the exact tuple and therefore still requires a successor proposal artifact, a fresh tier-appropriate Reviewer PASS, and a later source-bound confirmation under the current callback contract. The Reviewer verifies the impact decision and retained evidence without re-executing unaffected product tests.

The exact current head required CI is never reused. Before Ready/merge, still require `required_checks_known: true`, every required check successful for the exact current head, and the normal mergeability gate. A consuming repository may shorten that wait with a path-aware docs/memory required-check lane, but the Harness never waives, fabricates, or carries forward an old-head check.

For a legacy or current proposal whose prior validation lacks a valid validation-impact artifact and complete reusable evidence, use the old lineage full-validation fallback. Never reconstruct dependency scope from chat, command names, or an observation.

## Persist the exact proposal artifact

Before independent review, compose the exact **Proposal artifact** from `references/delivery-evidence-contract.md` and add it as one top-level source product PR comment without a workflow state marker.

Normalize, digest, add, and independently read the complete artifact comment back through the Pull Request transport. Its URL and whole-comment Markdown digest are the exact proposal identity; never calculate a digest from an extracted YAML subtree.

Apply the proposal artifact's shared cross-field rules. For a revision, create a new append-only artifact rather than editing the old one; a repair/rebase updates both base fields to the same new `develop` SHA.

When recovery finds one exact valid proposal artifact and its exact unchanged Draft project-memory PR, when applicable, but neither a Reviewer PASS nor an `awaiting-confirmation` callback for that proposal exists, reuse those persisted artifacts. Apply `L1 semantic-freshness` to the source, authority, artifact, complete PR tuple, changed-file identities, and validation bindings, and resume only the independent review step. Fetch the complete diff or content again whenever its bound identity changed or the exact normalized content is unavailable; an already validated legacy Bundle may supply only an unchanged cached payload. Do not repeat classification, rebuild the branch/PR, or create a duplicate proposal merely because the preceding Phase Owner ended after persisting the artifact. If the exact Reviewer PASS is already persisted but only the callback is absent, re-read and validate that PASS and let the Context Promotion Phase Owner complete only the callback step.

## Require independent review

For a no-write assessment that belongs to a persisted lineage, bind the complete proposal artifact URL/digest, source tuple, `effective_review_tier`, and exact normalized review inputs. The Context Promotion Phase Owner must directly start a fresh read-only Reviewer and require a structured, non-persistent PASS or blocking FAIL verdict for that exact review input. When a validated legacy Bundle supplied the review bytes, additionally require the ephemeral verdict's `consumed_bundle_sha256` to equal that same-round legacy Bundle. Bind the persisted PASS only to the contract's reconstructible semantic `review_input_sha256`, never to an operation-local cache digest. A first new all-`no_write` result never reaches this section.

For a write, use the independently read-back proposal artifact and Draft project-memory PR result to bind title/Body digest, head SHA, base ref `develop`, base SHA, complete changed files, and diff. The Context Promotion Phase Owner must directly start a fresh read-only Reviewer for each review round and supply the complete normalized source payloads, artifact URL/digest, PR tuple/diff, effective tier, item tiers, and any validation-impact URL/digest. Do not require that Reviewer to search GitHub or download the same complete inputs again.

Require every tier to check source traceability, exact tuple/digest integrity, item-to-destination/diff coverage, correct classification, cross-task value or concrete forgetting risk, exclusion of single-task tracking and generic/discoverable trivia, one fact in one authority layer, confirmation-gate correctness, and a project-memory-only diff or complete no-write assessment.

Apply the tier-specific depth:

- For `r0-no-write`, require all five durable categories, exact category-specific reasons, and evidence that no omitted reusable conclusion requires a write. Do not fetch a memory diff or run repository tests.
- For `r1-documentary`, inspect only the exact wiki/daily-log hunks, destination authority, cited sources, links, placement rules, and selected document validation. Do not re-read unrelated Issue/PR comments, re-inspect unrelated product diff, or re-run product Unit, Integration, or Coverage.
- For `r2-stable-context`, additionally inspect the complete affected stable-context authority, superseded statements, lifecycle, project identity/background consistency, and conflict/duplication search.
- For `r3-normative`, check the complete relevant Issue contract and accepted/merged source evidence, every affected ADR/rule authority, correct accepted/proposed/superseded treatment, applicable repository rules, source gap and consequences, compatibility/safety effects, executable validation, and the complete confirmation requirements.

For a validation-impact reuse or incremental result, require the Reviewer to validate ancestry, complete base delta, prior/current patch identities, dependency inventory, retained evidence pairs, executed validation, reason codes, and the rule that exact-current-head required CI remains outstanding. The Reviewer must not re-execute retained validation merely to remain independent.

Forbid edits, GitHub mutations, further delegation, alternative designs, and non-blocking wording suggestions in the Reviewer. Require the Reviewer to return its tuple-bound verdict only to the Context Promotion Phase Owner; the Reviewer must never persist its own PASS comment or callback. Fix blockers in the same Owner, bind a new tuple/digest when the proposal changes, and directly start a fresh Reviewer. Continue in that Owner until PASS or a genuine blocker.

For a no-write PASS in a persisted lineage that must finish the historical strict protocol, the Context Promotion Phase Owner composes the exact **Reviewer PASS for no-write** artifact in its versioned form from the Reviewer's returned verdict and `references/delivery-evidence-contract.md`, then adds and independently reads it back as one top-level source PR evidence comment without a workflow state marker.

Bind its comment URL and normalized Markdown digest. A clean re-entry must re-read this comment and the exact proposal artifact digest before relying on the PASS.

For a write, the Context Promotion Phase Owner composes the exact **Reviewer PASS for a write** artifact in its versioned form from the Reviewer's returned verdict and the shared evidence contract and adds it as an append-only comment to the Draft project-memory PR.

Require `changed_files` to be the exact sorted artifact/transport view and require every validation entry to reflect an executed check. Persist the effective tier, complete item coverage, review-input digest, and nullable validation-impact binding. Independently read the PASS comment back and bind its whole-comment URL/digest. Apply `L1 semantic-freshness` to the PR/ref/Body/changed-file identities and reuse the complete diff payload only on an exact match; invalidate PASS on any semantic change.

Dual-read an exact already persisted unversioned Reviewer PASS only under the shared evidence contract's `legacy-full` rules. Treat it as equivalent to `r3-normative`, never rewrite or downgrade it, and let an unchanged active lineage continue without repeat review. Every new PASS uses the versioned form.

## Persist and relay the confirmation gate

After Reviewer PASS, have the Context Promotion Phase Owner compose the exact **Awaiting-confirmation callback** from `references/delivery-evidence-contract.md` and add it as one source product PR comment with the unchanged promotion marker.

For a normal initial proposal, both predecessor fields and both legacy-evidence fields are null. For an initial closure-only `legacy-reconciliation` revision, `previous_comment_*` and `legacy_evidence_*` must both bind the exact legacy callback whole-comment URL/digest, `proposal_kind` is `legacy-reconciliation`, and the proposal preserves the old outcome. A first-state write that supersedes legacy `no-promotion` uses `proposal_kind: write`, `revision_reason: legacy-reassessment`, and the same two legacy pairs; this is the only non-null predecessor exception for an initial write proposal. For a user revision or promotion-scope repair, `previous_comment_*` binds the active superseded schema-v2 tip and the legacy-evidence fields remain unchanged only when the entire branch is a legacy migration.

Normalize, digest, add, and independently read the exact comment back through the Pull Request transport. The returned comment URL and digest are the proposal state identity. Do not persist raw conversation or user wording.

Require `eligibility_registration_url` / `eligibility_registration_sha256`, `proposal_artifact_url` / `proposal_artifact_sha256`, and `reviewer_pass_url` / `reviewer_pass_sha256` for every strict proposal path. This is the exact eligibility registration URL/digest, proposal artifact URL/digest, and Reviewer PASS URL/digest set. Bind the no-write evidence comment only for a persisted all-`no_write` lineage, or the project-memory PR PASS comment for a write proposal. For a write, require the state callback's `authority_base_sha` and `memory_base_sha` to be equal. Immediately before relay, apply `L1 semantic-freshness` to the complete artifact, eligibility registration, authority base, every evidence/current-authority source, and any memory tuple, and compare their recorded digests. Reuse an already validated legacy Bundle payload only when every identity matches; otherwise fetch the changed input and rebuild/re-review. Display exact details from the artifact rather than reconstructing user-visible content from the state callback.

When delegated, return that exact proposal to the `delivery` coordinator for a final, self-contained summary. When standalone, present the same complete details in the final response, including item/effective review tiers, any validation-impact and retained/re-executed validation summary, the proposal callback URL/whole-comment SHA-256, Reviewer PASS identity, any complete memory-PR tuple, and a ready-to-send explicit `role: context-promotion` re-entry packet, prefixed with `$project-harness` for Codex or `/project-harness` for Claude Code and using the root Skill's `user_decision` fields. In either case, end the proposal-producing turn with `awaiting-confirmation`. Do not call a same-turn input tool, write `confirmed`, mark a memory PR Ready, merge, close the Issue, or infer approval in that turn.

Offer exact approval, pause, and an exact modification-items path. Bind approval only to the displayed proposal comment URL/digest and, for a write, the exact Draft PR tuple. Silence or timeout leaves the active proposal unchanged and is not a response.

Never persist raw confirmation-response text, its digest, chat, prompt content, response metadata, or proposal identity into a Delivery observation. The stage-log schema is frozen read-only compatibility data; neither the coordinator nor this phase writes or backfills it.

On a later exact confirmation re-entry, first require the current `user_decision` proposal URL/digest to equal the sole active `awaiting-confirmation` whole comment. Reconstruct and completely enumerate the active promotion lineage, then apply `L1 semantic-freshness` to the Issue/product PR tuple, eligibility registration, authority base, every evidence/current-authority binding, proposal artifact/state, Reviewer PASS, and any memory PR tuple. Fetch complete content for a missing or changed binding; validate and reuse an existing legacy Bundle only when that resumed delegation already carries it. Compose the exact **Confirmed callback** from the shared evidence contract and add it as another source PR comment with the unchanged marker only for `decision: approved` and only when every URL, digest, ref, changed path, and validation result remains exact.

For `decision: revise`, do not write `confirmed`; continue through **Apply modification requests and promotion-scope repairs** and produce a new reviewed `awaiting-confirmation` revision. For `decision: pause`, make no phase mutation and return the existing `awaiting-confirmation` identities. Return blocked without a confirmation mutation for a malformed decision, stale proposal identity, or source drift that cannot safely produce a reviewed revision.

Require `proposal_kind` to equal the predecessor `awaiting-confirmation` callback. Whenever that proposal artifact includes a project-memory PR—normal write, unmerged legacy Ready, or historical merged-memory reconciliation—memory PR URL, title, Body digest, head ref/SHA, base ref/SHA, and changed files are all required and must equal the exact displayed/reviewed tuple. They are null only when the exact artifact contains no memory PR. Independently read the confirmation back and bind its URL/digest. Any eligibility registration, authority base/source, proposal, PR tuple, changed-file identity, validation, or Reviewer change invalidates it.

Do not return `confirmed` as a successful phase result. In the same confirmation-continuation phase invocation:

- continue an unchanged normal all-`no_write` proposal to schema-v2 `no-promotion`;
- continue an unchanged normal write proposal, including a write that supersedes legacy `no-promotion`, to schema-v2 `memory-pr-ready` and `verified-memory-pr`;
- for closure-only reconciliation of exact legacy `no-promotion` or `memory-pr-merged`, return that existing terminal plus the new confirmation as terminal evidence without duplicating it;
- for exact legacy `memory-pr-ready`, continue to the applicable migrated schema-v2 `memory-pr-ready` or `memory-pr-merged` state defined below.

If interruption leaves a verified `confirmed` callback as the persistent tip, return blocked with that recoverable state; a fresh Context Promotion reconciler resumes from it without requesting approval again.

## Apply modification requests and promotion-scope repairs

Treat modification items, repairable authority/current-source drift, or a repairable required-check, title/Body/head/base-tuple, advanced-base, or mergeability defect caused by permitted Context Promotion work as input to a new proposal revision. A source, tuple, rebase, conflict, or required-check repair is never covered by the old confirmation:

1. Apply `L1 semantic-freshness` to the source, current authority, prior proposal, and any Draft memory PR; reuse unchanged exact normalized payloads only when their identities still match.
2. Reject or route a requested change or repair that alters the product delivery contract or exceeds promotion authority. For authority/current-source drift, rebuild the complete five-category assessment against the new exact authority base. For failed checks or mergeability/base defects, independently distinguish a reproducible promotion-scope defect or safe rebase from pending, unknown, permission, unsafe conflict, or external-infrastructure failure; return blocked for the latter group without changing the tuple.
3. Reclassify every affected item and update the Draft project-memory PR or no-write assessment.
4. Re-run validation selected by the effective review tier. For an advanced base, apply **Revalidate an advanced base proportionally** and persist any required validation-impact artifact instead of automatically re-running every prior local test.
5. Persist a new complete proposal artifact bound to the preceding artifact URL/digest.
6. In the same Context Promotion Phase Owner, directly start a fresh independent Reviewer against the new artifact and, for a write, the new exact PR tuple/diff.
7. Persist a new `outcome: awaiting-confirmation` callback with an incremented revision and the superseded state callback as `previous_comment_url` / `previous_comment_sha256`. For a repair from a confirmed-only tip, populate `invalidates_confirmation_*` and leave `invalidates_ready_*` null. For a repair after Ready, populate both pairs. For an unconfirmed user revision all four invalidation fields remain null.
8. Return `awaiting-confirmation`; when delegated, let the coordinator summarize the new artifact and finish the turn, and when standalone, provide the same final summary and explicit re-entry packet directly before finishing the turn.

For an advanced-base repair, require the markerless validation-impact artifact for `reuse` or `incremental`; otherwise apply the old lineage full-validation fallback. The exact current head required CI is never reused, and no old-head check can satisfy Ready or merge.

If the existing project-memory PR is Ready, use the delegated conditional `convert-to-draft` mutation and verify Draft state before changing content or head. A confirmed no-write authority/source repair has no PR to convert and proceeds directly to a new artifact and review. Do not edit or replace prior proposal, review, or confirmation comments. A modified or repaired proposal requires a new artifact, review, state digest, and approval. Never loop a check failure by repeatedly changing content under an old confirmation.

When a revision changes a write proposal to all-`no_write`:

1. Convert the exact old memory PR to Draft when it is Ready.
2. Persist the old PR URL/title/Body digest, head ref/SHA, base ref/SHA, and a category-specific reason in the new artifact's `supersedes_memory_*` fields; set the new proposal/state `memory_pr_*` fields to null.
3. Add and read back one plain old-memory-PR comment binding the source PR, complete old tuple, new artifact URL/digest, and `state: superseded-by-context-promotion`. Bind that comment's whole-comment URL/digest.
4. Bind the same superseded tuple and `supersession_comment_*` pair in the new `awaiting-confirmation` callback. The old PR remains an open Draft because this transport does not close PRs, but it is non-active and must never be merged or reused. If a later revision returns to a write, create a new branch/Draft memory PR rather than reactivating the superseded one.

Allow the closure gate to ignore only an exact open Draft memory PR whose current complete tuple and supersession comment URL/digest still match this artifact/state/comment chain. Any Ready, drifted, unmarked, mismatched, or multiple active memory PR remains blocking.

## Complete confirmed no-promotion

Only for a persisted lineage that already has a read-back-verified `confirmed` callback for an all-`no_write` proposal, apply `L1 semantic-freshness` to the eligibility registration, authority base, every evidence/current-authority binding, artifact, Reviewer PASS, proposal state, and confirmation URL/digest. Reuse unchanged exact normalized payloads only on matching identities and continue only for an unchanged authority base/source set. A first new all-`no_write` result uses direct no-promotion and never writes this terminal:

1. Compose the exact **No-promotion terminal** from `references/delivery-evidence-contract.md` as a concise source PR callback with the unchanged marker.

2. Add the exact comment through the Pull Request transport.
3. Independently read the comment and source PR back.
4. Verify the marker, comment digest, unchanged merged source identity, valid predecessor, and absence of a conflicting callback.
5. Return the terminal state only for `verified` or `no-op`.

Do not create an empty branch, commit, memory file, or PR merely to demonstrate activity.

For an exact legacy `no-promotion` with an open Issue, do not enter the schema-v2 terminal write above only when the reconstructed and confirmed closure-only `legacy-reconciliation` proposal keeps every durable category `no_write` and all memory-PR fields null. Then return the existing legacy terminal plus the new confirmation as closure evidence. If reassessment or user modification yields a write, treat the old terminal as superseded evidence, follow the normal schema-v2 write/Ready/merge path, and require a new `memory-pr-merged` terminal before closure.

## Mark a confirmed project-memory PR Ready

Only after a read-back-verified `confirmed` callback for the exact write proposal:

1. Apply `L1 semantic-freshness` to the eligibility registration, authority base/sources, Draft project-memory PR, title, refs, Body digest, changed-file identities, Reviewer PASS, validation or validation-impact evidence, proposal artifact, state callback, and confirmation. Reuse a previously acquired complete diff only on an exact tuple/identity match.
2. Require the complete tuple and changed paths to remain exactly confirmed.
3. Use the loaded Pull Request transport to mark the exact Draft PR Ready.
4. Independently verify Ready state and every bound field.
5. Compose and add the normal exact **Memory-PR-ready callback** from the shared evidence contract with the unchanged marker.

6. Independently read the source callback back.

Populate `changed_files` with the exact sorted artifact/Reviewer identities for a write; it must not be empty when the diff is non-empty. Fail closed on partial or ambiguous mutations. Do not merge the project-memory PR.

When delegated, return the verified Ready tuple to the `delivery` coordinator's project-memory merge gate. A standalone role hands it to external review or a later `delivery` entry.

For an exact unmerged legacy `memory-pr-ready` whose project-memory PR remains Ready and whose Issue remains open, do not mark it Ready again. After every strict legacy check, build a `legacy-reconciliation` proposal artifact for the exact existing diff, persist a fresh Reviewer PASS, summarize and stop, obtain a later explicit source-bound confirmation, and re-read the unchanged eligibility, authority, source, artifact, review, confirmation, and memory-PR tuple. Then compose, append, and verify the shared evidence contract's `migration: confirmed-legacy-ready` variant of the **Memory-PR-ready callback**.

Populate `changed_files` with the exact sorted fresh-review identities. This migrated nonterminal may enter the coordinator's merge gate only for the unchanged Ready tuple. If the user requests a modification, or the tuple/base/check repair changes content, convert it to Draft first and follow the normal new-artifact, fresh-review, new-confirmation path instead.

## Reconcile a merged project-memory PR

After the `delivery` coordinator merges the exact confirmed project-memory PR, or recovery discovers that an external authority already merged it:

1. Apply `L1 semantic-freshness` to the source Issue/product PR, authority bindings, eligibility URL/digest, proposal artifact/state, confirmation, memory-pr-ready callback, project-memory PR, and Reviewer PASS, and live-read checks, actual merge method, verified merge provenance, and merge identity. Reuse unchanged normalized semantic payloads; consume an operation-local Bundle only when this is a resumed legacy-v2 delegation that already carried and validated one.
2. Require non-Draft merge into `develop`, the exact confirmed/reviewed title, head/base tuple, Body digest, unchanged approved paths/content, `required_checks_known: true` with every required check currently successful for the exact head, an actual merge method equal to the bound Harness integration policy (`integration.memory_pr.merge_method` for schema-v2, or the sole authoritatively available method captured by schema-v1 compatibility preflight), and transport-verified provenance bound to the guarded head/base and merge commit. Do not require post-merge mergeability. Apply these checks equally under delegated and standalone entry before writing `memory-pr-merged`.
3. Compose and add the normal exact **Memory-PR-merged terminal** from the shared evidence contract with the unchanged marker.

4. Populate `changed_files` from the exact Ready callback and independently read the callback and both PRs back.

Return terminal only for `verified` or `no-op`.

For an exact legacy `memory-pr-merged` with an open Issue, do not append another terminal. After the `legacy-reconciliation` proposal and confirmation are verified against the already merged diff, return the existing legacy terminal plus the new confirmation as closure evidence.

For an exact legacy `memory-pr-ready` whose project-memory PR is already merged and whose Issue remains open, first satisfy every strict legacy check, independently verify the integrated diff, transport-verified merge provenance, allowed actual merge method, current merge identity, and currently known successful required checks for the exact head, then build a schema-v2 `legacy-reconciliation` proposal artifact, persist a fresh Reviewer PASS, summarize and stop, and obtain a later explicit source-bound confirmation. This is a read-only historical-integration exception, not a current-format merge `no-op`. After confirmation, compose and append the shared evidence contract's `migration: confirmed-legacy-already-merged` variant of the **Memory-PR-merged terminal**.

Independently read back this callback. This path recognizes an integration that already happened; it does not fabricate historical confirmation and it cannot authorize any new merge.

## Judge source Issue closure

Own the durable-memory closure judgment; the mutation owner depends on the entry:

- Judge closable only when the exact Closeout-accepted product title/Body/head/base lineage is verified merged into `develop`; the PASS comment, Issue callback, and current or legacy eligibility registration URL/digest pairs all independently re-read as valid; the Issue contract digest is unchanged; and either the complete Lean code-only admission holds, a fresh first-round direct no-promotion classification is revalidated, a schema-v2 confirmed terminal path exists, or an exact legacy terminal is paired with a schema-v2 `legacy-reconciliation` confirmation for that same evidence.
- For Lean code-only closure, require a complete current read to prove no promotion state and no source-linked project-memory PR, then revalidate the exact five `无` rows and the exact Closeout acceptance triple `item: durable-memory-impact`, `result: PASS`, `evidence: all-five-none` immediately before closure. The absence itself is not a marker and does not become a callback. Any discovered promotion artifact disables this branch and must be resumed under its persisted lineage.
- For first-round direct no-promotion closure, re-run the targeted five-category classification against the unchanged source and authority immediately before closure; require every item still `no_write`, no promotion state or source-linked memory PR, and no new durable candidate. This ephemeral result does not become a marker or survive source/authority drift; a later recovery re-dispatches classification.
- Otherwise require the sole active promotion tip to be either a verified schema-v2 `no-promotion`; an exact approved/reviewed memory PR verified merged with a valid schema-v2 `memory-pr-merged` callback; or, only for the closure-only legacy migration, a schema-v2 `confirmed` callback with `proposal_kind: legacy-reconciliation` whose predecessor/evidence pairs bind one exact legacy `no-promotion` or `memory-pr-merged` terminal and whose proposal preserves that outcome. In that exception the legacy callback supplies terminal outcome evidence and the active schema-v2 confirmation supplies current closure authority; do not require or create a duplicate terminal. A schema-v2 write branch that binds and supersedes legacy no-promotion is closable only from its own active `memory-pr-merged` terminal; treat that exact predecessor legacy callback as superseded audit evidence, not as a conflicting active terminal. Reject any other untrusted author, superseded tip, conflicting active/terminal state, or unrelated memory PR; ignore only an exact open Draft proven non-active by the supersession chain defined above.
- Under `delivery`, return the applicable Lean admission or persisted terminal evidence to the coordinator. The delegated Context Promotion Phase Owner must not close the Issue.
- Under `delivery`, do not read, write, backfill, or judge legacy Delivery stage observations. Historical observations are optional diagnostics and never gate closure; the coordinator must still re-read the original workflow artifacts required by the selected path.
- Under a standalone Context Promotion invocation, re-read every source, PASS/callback/eligibility record, predecessor and terminal comment immediately before mutation. Then use one explicit Issue-transport `change-metadata` mutation with `state: closed` and `state_reason: completed`, and independently read back both exact fields and all protected Issue fields.
- Accept only `verified` or `no-op`; fail closed on ambiguity or protected-field mismatch.
- Never leave a successful result with an ambiguous Issue state.

## Return a bound phase result

~~~yaml
result_schema_version: 2
outcome: awaiting-confirmation | verified-memory-pr | memory-pr-merged | no-promotion | return-to-definition | blocked
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: null
source_pr_url: https://github.com/owner/repo/pull/456
source_pr_title: null
source_pr_body_sha256: null
source_head_ref: null
source_head_sha: null
source_merge_commit_sha: null
eligibility_registration_url: null
eligibility_registration_sha256: null
authority_base_sha: null
legacy_evidence_url: null
legacy_evidence_sha256: null
proposal_comment_url: null
proposal_comment_sha256: null
proposal_revision: null
proposal_artifact_url: null
proposal_artifact_sha256: null
reviewer_pass_url: null
reviewer_pass_sha256: null
confirmation_comment_url: null
confirmation_comment_sha256: null
source_callback_url: null
source_callback_sha256: null
memory_pr_url: null
memory_pr_title: null
memory_pr_body_sha256: null
memory_head_ref: null
memory_head_sha: null
memory_base_ref: null
memory_base_sha: null
changed_files: []
ready_state_verified: false
memory_pr_merged: false
memory_merge_commit_sha: null
issue_closure: null | pending-memory-pr-merge | closed
issue_state_verified: false
issue_state_reason: null | completed
coordinator_action: request-confirmation | merge-memory-pr | close-issue | null
promoted_sources: []
validation: []
reason: null
recovery_condition: null
handoff:
  role: delivery | external-review | context-promotion | definition
  recipient: delivery-coordinator | user
  authoritative_sources: []
  evidence_urls: []
  next_action: null
~~~

For delegated `awaiting-confirmation`, return the exact proposal artifact/state/review identities with `coordinator_action: request-confirmation`; include any validation-impact URL/digest in `handoff.evidence_urls` and its verified result in `validation`, and let the coordinator summarize them before ending its current turn. For standalone `awaiting-confirmation`, return the same identities with `coordinator_action: null`, leave `issue_closure: null`, and hand off to the user with the explicit `role: context-promotion` re-entry packet plus the current host trigger. For delegated `verified-memory-pr`, use `issue_closure: pending-memory-pr-merge` and `coordinator_action: merge-memory-pr`. For delegated no-promotion or memory-pr-merged, leave `issue_closure: null`, set `coordinator_action: close-issue`, and return the applicable Lean admission or persisted terminal evidence; only the coordinator may close.

For either no-artifact `no-promotion` route, leave all proposal, review, confirmation, source-callback, memory-PR, and changed-file fields null/empty. Set `reason: lean-code-only-all-five-none` only when the shared Lean admission holds; otherwise set `reason: direct-no-promotion-all-no-write`. Under `delivery`, set `coordinator_action: close-issue` and bind the acceptance, Issue callback, and eligibility URL/digest pairs in `handoff.evidence_urls`. This result is verified by its exact read-time gate and does not claim that a promotion terminal callback exists.

For a standalone no-promotion or reconciled memory-pr-merged result, close the Issue in the same invocation and require `issue_closure: closed` with `issue_state_verified: true`.

For standalone `verified-memory-pr`, preserve the legacy `issue_closure: pending-memory-pr-merge` meaning and leave the Issue open. Recommend a `role: delivery` entry to perform the exact merge, terminal reconciliation, and closure without requiring the user to invoke another phase manually. For blocked, preserve any Draft project-memory PR and proposal chain, leave `issue_closure: null`, and report the exact recovery condition.

For `return-to-definition`, leave every product and memory artifact unmerged, identify the exact requested product-contract change or unresolved authority decision, and return the source Issue plus `role: definition`. Under `delivery`, the coordinator stops and relays this typed result; it must not reinterpret it as a Context Promotion patch.
