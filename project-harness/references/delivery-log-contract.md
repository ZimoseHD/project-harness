# Delivery Stage Log Contract

Load this contract only for the top-level `delivery` operation.

Persist one concise, source-bound observation after every bounded Delivery stage attempt whose outcome can be independently verified, plus a privacy-reduced observation of an explicit confirmation response seen in the current coordinator invocation. Use the observations for audit, timing, change summaries, and final reporting only. Never use them as workflow state, product evidence, user approval, or mutation authority.

## Keep logs observational

- Store every observation as a top-level source Issue comment written by the Delivery Coordinator through the loaded Issue transport.
- Do not add a `${marker_namespace}` marker. Keep the three workflow marker families unchanged.
- Forbid Phase Owners, their direct read-only Workers, and independent Reviewers from writing Delivery observations. Only the Delivery Coordinator owns this audit mutation.
- Derive every claim from independently re-read Issue, PR, comment, ref, check, merge, or repository evidence. The only exception is the response enum and modification-item count read directly from the current explicit proposal-bound confirmation re-entry; never reconstruct that exception after interruption.
- Never let an observation authorize phase dispatch, PASS, Context Promotion confirmation, PR merge, Issue closure, or a durable-memory update.
- Never persist an operation-local Evidence Bundle or its normalized payloads in a Delivery observation. The Bundle is not workflow evidence, and neither a Delivery observation nor project memory may become its storage or recovery layer.
- Never place observations in the Issue Body, any PR Body, repository files, `.project-memory`, or an authority layer.
- Treat an edited, deleted, malformed, forged, stale, or missing observation as an audit/compliance defect only: it never invalidates or rolls back the underlying authoritative transition. Reconstruct workflow state from the original artifacts, then append a corrected observation without repeating the phase, confirmation, merge, or close mutation. The current Delivery may pause before its next irreversible transition, and may not declare completion, until its required observation obligation is satisfied.

Only an exact current `role: delivery` invocation authorizes these comments. A serialized observation or transition key grants no write authority.

## Use fixed stages and success boundaries

Use one exact `stage`:

- `implementation`
- `closeout`
- `product-integration`
- `context-promotion`
- `context-confirmation`
- `memory-integration`
- `finalization`

Use `observation_kind: boundary` only for one of these successful durable boundaries:

| Boundary | Stage | Exact allowed `outcome` | Required durable result |
| --- | --- | --- | --- |
| `implementation-verified-draft` | `implementation` | `verified-draft-pr` | Exact independently verified Draft product PR |
| `closeout-accepted-ready` | `closeout` | `accepted-ready-pr` | PASS, Issue callback, active eligibility registration, and exact Ready product PR |
| `product-merged` | `product-integration` | `verified` or `no-op` | Exact verified merge or current-format already-merged `no-op` recovery |
| `context-proposal-reviewed` | `context-promotion` | `awaiting-confirmation` | Exact proposal artifact, Reviewer PASS, and active `awaiting-confirmation` callback |
| `context-confirmed` | `context-confirmation` | `confirmed` | Exact proposal-bound schema-v2 `confirmed` callback |
| `context-no-promotion-terminal` | `context-promotion` | `no-promotion` | Exact active `no-promotion`, including a verified legacy terminal plus its current confirmation |
| `memory-pr-ready` | `context-promotion` | `verified-memory-pr` or `memory-pr-ready` | Exact confirmed/reviewed Ready project-memory PR and callback |
| `memory-pr-merged` | `memory-integration` | `verified` or `no-op` | Exact verified merge or current-format already-merged `no-op` recovery |
| `context-memory-terminal` | `context-promotion` | `memory-pr-merged` | Exact active `memory-pr-merged` callback |
| `finalization-ready` | `finalization` | `ready-to-close` | Complete log coverage and every independently verified Issue-closure prerequisite |
| `issue-closed` | `finalization` | `verified` or `no-op` | Exact source Issue independently verified `closed` with `state_reason: completed` |

Use `observation_kind: attempt` with `boundary: null` after a bounded attempt ends in a persisted return, repair, revision, pause, blocked state, or indeterminate transport result. Use the original phase or transport outcome without renaming it. An attempt observation never satisfies successful-boundary coverage.

A changed binding, changed target, proposal revision, confirmation round, reconciler dispatch, or merge recovery is a new attempt. A narrow Worker replacement or re-review against an unchanged tuple inside the same live semantic-round Phase Owner remains part of that Owner attempt. Keep older observations as audit history; never choose active workflow state by observation time or attempt number.

## Write one exact schema

Write this semantic payload without a workflow marker:

~~~yaml
record_kind: delivery-stage-observation
log_schema_version: 1
observation_kind: boundary | attempt
transition_key: SHA256
attempt_id: 550e8400-e29b-41d4-a716-446655440000 | null
boundary: implementation-verified-draft | closeout-accepted-ready | product-merged | context-proposal-reviewed | context-confirmed | context-no-promotion-terminal | memory-pr-ready | memory-pr-merged | context-memory-terminal | finalization-ready | issue-closed | null
stage: implementation | closeout | product-integration | context-promotion | context-confirmation | memory-integration | finalization
activity: initial | repair | resume | revalidate | accept | reconcile | integrate | recover | propose | revise | confirm | finalize | closure-gate
attempt: 1
outcome: EXACT_PHASE_OR_TRANSPORT_OUTCOME
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: SHA256
observed_at: 2026-07-28T10:00:00.000Z
started_at: 2026-07-28T09:59:00.000Z | null
finished_at: 2026-07-28T10:00:00.000Z | null
elapsed_ms: 60000 | null
timing_scope: coordinator-wall
timing_quality: measured | reconstructed | unknown
user_wait_ms: 12000 | null
change_quality:
  repository: measured | reconstructed | unknown | not-applicable
  github: measured | reconstructed | unknown | not-applicable
  context: measured | reconstructed | unknown | not-applicable
input_snapshot: {}
output_snapshot: {}
change_summary:
  repository_changes: []
  github_mutations: []
  context_changes: []
  truncated: false
  omitted_count: 0
evidence:
  - kind: product-pr
    url: URL
    sha256: SHA256
raw_user_input_persisted: false
reason_code: null
~~~

Normalize and digest the entire Markdown comment. The whole-comment URL/digest pair is the observation identity; never digest only the extracted payload.

Require:

- `attempt` to be a positive display counter for the stage/activity; never use it as identity or authority;
- `attempt_id` to be one lowercase UUIDv4 for a live attempt, including its successful boundary; require it for every attempt observation and every measured boundary, and require null for a reconstructed or unknown-timing boundary;
- `activity` to be exactly one of the values enumerated in the schema;
- `input_snapshot` and `output_snapshot` to contain only exact tuple fields needed to explain that attempt;
- every evidence entry to contain a stable kind, URL, and normalized whole-artifact digest;
- `raw_user_input_persisted: false` exactly;
- `reason_code` to be null or a lowercase kebab-case diagnostic code;
- each `change_quality` domain to follow the modification-quality rules below;
- `boundary` to match the fixed stage table for a boundary observation and to be null for an attempt observation;
- unknown schema versions and malformed schema-v1 comments to remain invalid, never legacy.

## Calculate a deterministic transition key

Calculate `transition_key` as lowercase SHA-256 over UTF-8 canonical JSON with sorted keys, compact separators, and no ASCII escaping for exactly:

~~~json
{
  "log_schema_version": 1,
  "observation_kind": "boundary",
  "boundary": "implementation-verified-draft",
  "stage": "implementation",
  "issue_url": "URL",
  "issue_body_sha256": "SHA256",
  "input_snapshot": {},
  "output_snapshot": {},
  "evidence": []
}
~~~

Exclude activity, top-level outcome, attempt ID, timestamps, elapsed time, attempt number, change quality/preview, reason code, and the observation's own URL/digest. The canonical snapshots still bind an attempt's persisted `result_kind`. This makes initial `verified`, recovery `no-op`, and reconstructed observations of one exact durable state share a key without turning that key into workflow authority. Use `attempt_id`, not `transition_key`, to distinguish separate live executions.

Use `scripts/delivery_log.py` to calculate a constructed payload's transition key, then require `validate_new_observation` to return no errors before every new observation write. Use the backward-compatible `validate_observation` only when reading existing or historical records and evaluating successful-boundary coverage; calculating a transition key does not replace the new-write validator.

## Canonicalize snapshots and evidence

For a boundary observation, use only the exact snapshot keys below. Keep every listed key, using null only where shown. Use the same field names and value forms as the phase result or transport envelope; never invent a second tuple vocabulary.

| Boundary | Exact `input_snapshot` keys | Exact `output_snapshot` keys | Required evidence kinds |
| --- | --- | --- | --- |
| `implementation-verified-draft` | `base_ref`, `base_sha`, `prior_head_sha` (nullable) | `product_pr_url`, `product_pr_title`, `product_pr_body_sha256`, `head_ref`, `head_sha`, `base_ref`, `base_sha` | `product-pr` |
| `closeout-accepted-ready` | `product_pr_url`, `product_pr_title`, `product_pr_body_sha256`, `head_ref`, `head_sha`, `base_ref`, `base_sha` | `acceptance_comment_url`, `acceptance_comment_sha256`, `issue_callback_url`, `issue_callback_sha256`, `eligibility_registration_url`, `eligibility_registration_sha256`, `pr_state` | `product-pr`, `acceptance-comment`, `issue-callback`, `eligibility-registration` |
| `product-merged` | `product_pr_url`, `product_pr_title`, `product_pr_body_sha256`, `head_ref`, `head_sha`, `base_ref`, `base_sha`, `acceptance_comment_url`, `acceptance_comment_sha256`, `issue_callback_url`, `issue_callback_sha256`, `eligibility_registration_url`, `eligibility_registration_sha256` | `merge_method`, `merge_commit_sha`, `merged_head_sha`, `merged_base_ref` | `product-pr`, `acceptance-comment`, `issue-callback`, `eligibility-registration` |
| `context-proposal-reviewed` | `product_pr_url`, `source_head_sha`, `source_merge_commit_sha`, `eligibility_registration_url`, `eligibility_registration_sha256`, `authority_base_sha` | `proposal_artifact_url`, `proposal_artifact_sha256`, `proposal_comment_url`, `proposal_comment_sha256`, `review_url`, `review_sha256`, plus nullable `memory_pr_url`, `memory_pr_title`, `memory_pr_body_sha256`, `memory_head_ref`, `memory_head_sha`, `memory_base_ref`, `memory_base_sha` | `eligibility-registration`, `proposal-artifact`, `proposal-callback`, `review`, and `memory-pr` only for a write |
| `context-confirmed` | `proposal_artifact_url`, `proposal_artifact_sha256`, `proposal_comment_url`, `proposal_comment_sha256`, `review_url`, `review_sha256`, plus the same nullable memory PR tuple | `confirmation_comment_url`, `confirmation_comment_sha256`, `decision` | `proposal-artifact`, `proposal-callback`, `review`, `confirmation-callback` |
| `context-no-promotion-terminal` | `proposal_artifact_url`, `proposal_artifact_sha256`, `proposal_comment_url`, `proposal_comment_sha256`, `review_url`, `review_sha256`, `confirmation_comment_url`, `confirmation_comment_sha256` | `terminal_comment_url`, `terminal_comment_sha256`, `terminal_outcome` | `proposal-artifact`, `confirmation-callback`, `terminal-callback` |
| `memory-pr-ready` | `proposal_artifact_url`, `proposal_artifact_sha256`, `proposal_comment_url`, `proposal_comment_sha256`, `review_url`, `review_sha256`, `confirmation_comment_url`, `confirmation_comment_sha256` | `memory_pr_url`, `memory_pr_title`, `memory_pr_body_sha256`, `memory_head_ref`, `memory_head_sha`, `memory_base_ref`, `memory_base_sha`, `ready_comment_url`, `ready_comment_sha256` | `proposal-artifact`, `review`, `confirmation-callback`, `memory-pr`, `ready-callback` |
| `memory-pr-merged` | `memory_pr_url`, `memory_pr_title`, `memory_pr_body_sha256`, `memory_head_ref`, `memory_head_sha`, `memory_base_ref`, `memory_base_sha`, `ready_comment_url`, `ready_comment_sha256` | `merge_method`, `merge_commit_sha`, `merged_head_sha`, `merged_base_ref` | `memory-pr`, `ready-callback` |
| `context-memory-terminal` | `memory_pr_url`, `memory_pr_body_sha256`, `memory_head_sha`, `merge_method`, `merge_commit_sha`, `ready_comment_url`, `ready_comment_sha256` | `terminal_comment_url`, `terminal_comment_sha256`, `terminal_outcome` | `memory-pr`, `ready-callback`, `terminal-callback` |
| `finalization-ready` | `path_kind`, complete `coverage_manifest`, `coverage_manifest_sha256` | `ready` exactly true | One `stage-observation` entry for every selected manifest observation plus `terminal-callback` |
| `issue-closed` | `path_kind`, `coverage_manifest_sha256`, `finalization_observation_url`, `finalization_observation_sha256` | `state` exactly `closed`, `state_reason` exactly `completed` | `finalization-observation` |

An evidence entry's digest is the normalized whole Markdown digest defined by the artifact's contract. For a PR, use its complete Body digest and keep refs/state in the snapshot. Use exactly the listed evidence kinds: include `memory-pr` only when the proposal is a write, and repeat `stage-observation` once for every selected manifest comment. Other duplicate kinds or additional evidence kinds are invalid for a boundary; place non-identity diagnostics outside the observation instead. Sort evidence by `kind`, URL, and digest before hashing.

For `observation_kind: attempt`, use exactly:

~~~yaml
input_snapshot:
  target_boundary: null
  source_bindings: []
output_snapshot:
  result_kind: blocked
  result_url: null
  result_sha256: null
  response_kind: null
  modification_item_count: null
~~~

Set `target_boundary` when the attempt was working toward one fixed boundary. Populate `source_bindings` with sorted `{kind, url, sha256}` objects. Populate `result_url` and `result_sha256` together only for a persisted result. Populate `response_kind` and `modification_item_count` only for the current explicit confirmation-response exception; otherwise keep both null. Every new confirmation-response attempt must use `target_boundary: context-confirmed`, use only `revision-requested`, `paused`, or `blocked` with `response_kind == result_kind == outcome`, require `result_url: null` and `result_sha256: null`, and contain exactly one `source_bindings` item with `kind: proposal-callback` whose URL/digest is the independently matched active `awaiting-confirmation` whole comment. A new attempt may not use `result_kind` / `outcome: approved`; a new attempt with `revision-requested` or `paused` result/outcome may not omit its matching response kind and count. Set all three change-quality domains to `not-applicable`, keep every change list empty, use `truncated: false` / `omitted_count: 0`, and exclude the observation's own `add-comment`. A successful `approved` decision is represented only by the `context-confirmed` boundary; continue dual-reading valid historical attempt observations that used `response_kind: approved`. Keep the evidence list equal to the persistent source bindings represented by these snapshots.

Reuse the same `attempt_id` if ambiguous transport recovery finds that one attempted observation write produced more than one exact comment. Generate a new ID for a genuinely new live execution. Group aggregate attempt/timing statistics by `attempt_id`; repeated comments with the same ID do not add another attempt or duration. A null-ID reconstructed boundary contributes no attempt count or measured time.

## Measure time honestly

- Define elapsed time as the Delivery Coordinator's inclusive wall duration from immediately before dispatch/gate work to acceptance of the independently verified outcome.
- Include Phase Owner work, direct Worker/Reviewer work, validation, CI polling, transport calls, and external waiting inside that span.
- Never add parallel direct-child durations together.
- Use a monotonic clock for `elapsed_ms` inside one live coordinator run. Use normalized RFC 3339 UTC timestamps ending in `Z` only for display.
- Set `timing_quality: measured` only when the same live coordinator captured both ends. Require non-null start, finish, and non-negative integer elapsed time.
- Preserve non-null `user_wait_ms` only when reading a valid historical observation whose same-turn host actually measured that wait. The current split-turn confirmation flow must write `user_wait_ms: null`: only after the explicit re-entry arrives, start its monotonic span immediately after syntactically recognizing the current exact role and `user_decision` packet and before reconstructing or re-reading its bound state, then measure coordinator processing, never the interval between turns.
- When one live coordinator action produces more than one durable boundary before control returns, attach the measured span to exactly one observation and record the other boundary observations as reconstructed with null elapsed time. Never duplicate one measured span across boundary records.
- After interruption or clean re-entry, append a reconstructed observation only after original workflow evidence proves the outcome. Set `elapsed_ms: null` and `user_wait_ms: null`; never derive active duration from commit time, comment time, or model estimates.
- Use `timing_quality: reconstructed` when trustworthy persisted events supply `finished_at`, and optionally `started_at`, but the live monotonic span was not captured. Use `unknown` only when neither exact timestamp can be established.
- Never fabricate historical duration for legacy or already-completed work.

## Summarize modifications without copying them

Record only verified, persisted net changes for the bounded attempt:

Set each `change_quality` domain independently:

- `measured` only when the same live coordinator captured the exact before/after baseline and independently verified the resulting delta;
- `reconstructed` only when persistent before/after evidence can reproduce that domain's exact delta after re-entry;
- `unknown` when an exact delta cannot be recovered; require the corresponding preview list to be empty and a non-null reason code, and never interpret the empty list as no change;
- `not-applicable` when the bounded action could not mutate that domain; require the corresponding preview list to be empty.

Delivery observation `add-comment` mutations are intentionally excluded from all change summaries to avoid recursive log-of-log reporting. `truncated` and `omitted_count` describe only a known preview that exceeded the limit; they never disguise an unknown baseline.

### Repository changes

For Implementation or Context Promotion repository work, list a bounded preview sorted by path:

~~~yaml
- path: relative/path
  status: added | modified | removed | renamed
  previous_path: relative/old-path | null
  additions: 0 | null
  deletions: 0 | null
  before_blob_sha: SHA | null
  after_blob_sha: SHA | null
~~~

For Implementation, compare the dispatch branch head—or the bound `develop` base for a new branch—to the verified pushed result head. For Context Promotion, compare the prior memory head/base to the verified proposal result. Link the complete PR changed-file/diff evidence instead of copying a diff.

Do not sum retry deltas to report final delivery size. Calculate final product and memory totals from their final net PR diffs. If a repair's preceding head is no longer available from persistent GitHub evidence, set repository quality to `unknown`; do not substitute the final PR base diff for that attempt's stage delta.

### GitHub mutations

Record every mutation completed in the attempt:

~~~yaml
- operation: create-draft | replace-content | add-comment | mark-ready | convert-to-draft | merge | change-metadata
  target_url: URL
  before: concise-state | null
  after: concise-state
  result_url: URL
  result_sha256: SHA256 | null
~~~

Do not copy comment Bodies, test output, or tool traces.

### Context changes

Record only proposal identities:

~~~yaml
- item_id: CONTEXT-1
  action: add | update | supersede | no_write
  classification: decision | stable_rule | wiki_knowledge | stable_context | milestone_evidence | no_write
  destination: relative/path | null
  proposal_artifact_url: URL
  proposal_artifact_sha256: SHA256
~~~

Do not copy the exact proposed prose into the log; the reviewed proposal artifact remains its source.

Limit the combined preview lists to 100 entries. If more exist, set `truncated: true`, set the exact positive `omitted_count`, and include complete PR/artifact evidence. Otherwise require `truncated: false` and `omitted_count: 0`.

## Protect user and environment data

Never persist:

- raw confirmation replies or their digests, including legacy `request_user_input` modification text;
- prompts, chat summaries, reasoning, Reviewer prose, or conversation history;
- stdout/stderr, full tool traces, tokens, cookies, credentials, environment variables, or secrets;
- absolute local paths, local usernames, email addresses, or Agent display names;
- uncommitted content, complete code diffs, or test output.

For Context confirmation, map a proposal-bound top-level decision exactly: `approved` → the `context-confirmed` boundary's `decision: approved`, `revise` → attempt `response_kind: revision-requested`, and `pause` → attempt `response_kind: paused`. Use attempt `response_kind: blocked` only after the displayed proposal URL/digest has independently matched the sole active tip and later validation finds malformed decision/items, post-binding source drift, or an out-of-authority request. If no active tip exists or that proposal binding is missing, mismatched, or unreadable, return blocked without writing an observation or making any other mutation. For a permitted response attempt, record only the displayed proposal callback binding, response enum, and modification item count; keep both result fields null and report no repository, GitHub, or context changes. A later reviewed proposal has its own `context-proposal-reviewed` boundary and must never be back-linked as the earlier response attempt's result. Require count zero for `paused`, a positive count for `revision-requested`, and a non-negative count for `blocked`. A confirmation observation never substitutes for the schema-v2 `confirmed` callback. The current-invocation revision/pause/blocked attempt observation is best-effort and never part of boundary coverage: if interruption loses the response before the observation is written, do not reconstruct it and do not block later recovery on its absence.

Treat every Delivery observation as single-task chronology and always `no_write` during Context Promotion classification. Never promote a stage log into durable project memory.

## Deduplicate and backfill safely

At Delivery reconstruction, require the Issue transport to enumerate all source Issue comments completely, including pagination, and return `comments_complete: true`. Build one operation-local, author-verified observation inventory by filtering exact `record_kind`, schema, Issue URL/digest, and source evidence. Reuse that inventory for ordinary live observation writes in the same coordinator invocation and add each independently read-back new observation to it. Do not require full pagination before every observation comment.

A normal observation write uses the in-memory inventory and exact returned comment ID and does not need complete pagination. Ambiguous response recovery requires complete pagination; clean recovery without a complete current inventory requires complete pagination; final coverage requires complete pagination.

- Return `no-op` only when an existing whole comment exactly matches the desired normalized Body, and only when that candidate comes from a proven complete current inventory.
- Allow multiple valid observations with one transition key as harmless audit duplicates. Never choose workflow state by the newest duplicate.
- If a response is ambiguous, do not retry. Search/read the complete paginated candidate set and accept success only when exact Body/digest evidence proves the original comment exists.
- Require a new complete paginated inventory when a clean recovery/backfill does not retain a proven complete current inventory, when target/comment capability changed, or before manifest, closure, or completion coverage. A concurrent unseen duplicate during an ordinary live write is harmless audit duplication and is discovered by the next required complete inventory; it never authorizes workflow progress.
- Ignore an invalid or untrusted observation for coverage and report it as a log diagnostic. It cannot invalidate original phase evidence.
- If durable evidence proves a boundary completed but no valid observation exists, append a reconstructed observation with null elapsed time before advancing.
- If a stage failed without stable evidence, do not invent a historical attempt observation. The same rule applies to a confirmation response no longer present in the current explicit re-entry.
- If a prior log was deleted or edited, append a reconstructed replacement; never edit another observation.
- Never repeat a merge, confirmation, or closure mutation merely to create a missing log. After an Issue is closed, never reopen it to repair logging.

## Require three coverage levels

Before evaluating any coverage level, discard the operation-local write inventory and perform complete pagination for one current read. This final coverage read is always exhaustive. For a confirmed no-write path, require exact active observations for:

1. `implementation-verified-draft`
2. `closeout-accepted-ready`
3. `product-merged`
4. `context-proposal-reviewed`
5. `context-confirmed`
6. `context-no-promotion-terminal`

For a project-memory write path, require:

1. `implementation-verified-draft`
2. `closeout-accepted-ready`
3. `product-merged`
4. `context-proposal-reviewed`
5. `context-confirmed`
6. `memory-pr-ready`
7. `memory-pr-merged`
8. `context-memory-terminal`

These six or eight records are the `manifest` level. Select observations by exact authoritative tuple/evidence bindings, not comment recency. Require every selected whole-comment URL/digest to re-read unchanged and every selected author to equal the verified mutation author. When multiple trusted records bind the same required boundary and current tuple, select the lowest `(created_at, URL, whole-comment digest)` tuple; never select by attempt number or use the choice as workflow state.

Pass only this already author-verified, current-tuple-filtered set to `scripts/delivery_log.py` coverage checks, using one exact binding per selected comment:

~~~yaml
observation_url: URL
observation_sha256: SHA256
record:
  record_kind: delivery-stage-observation
  # Include the complete validated observation payload.
~~~

The URL and digest identify the normalized whole Issue comment represented by `record`. Bare records never satisfy any coverage level. The pure helper validates each record schema and makes the supplied comment identities executable; it cannot itself establish GitHub authorship, comment immutability, Body-to-record extraction, or workflow lineage and never confers trust on its inputs.

Build this exact stage coverage manifest, with entries in the path order above and every entry's evidence sorted by kind/URL/digest:

~~~yaml
manifest_schema_version: 1
path_kind: no-write | memory-write
issue_url: https://github.com/owner/repo/issues/123
issue_body_sha256: SHA256
entries:
  - boundary: implementation-verified-draft
    observation_url: URL
    observation_sha256: SHA256
    transition_key: SHA256
    evidence:
      - kind: product-pr
        url: URL
        sha256: SHA256
~~~

Calculate `coverage_manifest_sha256` over UTF-8 canonical JSON of this object with sorted keys, compact separators, and no ASCII escaping. The manifest never contains `finalization-ready` or `issue-closed`, so neither observation self-references.

Append and independently verify one `finalization-ready` boundary observation binding:

- the Issue Body digest;
- accepted product tuple and merge identity;
- active eligibility registration URL/digest;
- active proposal, confirmation, and terminal URL/digest;
- memory tuple and merge identity when applicable;
- the coverage manifest and its digest.

Immediately before Issue closure, re-read every original workflow artifact and selected observation. Drift makes the finalization observation historical only; rebuild coverage and append a new finalization observation. The manifest plus that exact observation is the `closure` level. The finalization observation records readiness but never authorizes closure.

Before closing, require the Issue to report `locked: false` and the same authenticated Issue transport to retain callable `add-comment`; never unlock it. Capture one live closure-gate span before the final re-read. When the Issue transport independently verifies `state: closed` and `state_reason: completed`, append and verify one `issue-closed` observation to the still-closed Issue. Bind the same path kind, exact stage-manifest digest, and exact finalization observation, and record the completed `change-metadata` mutation in `github_mutations`. Attach the measured closure-gate span only to `issue-closed`; use reconstructed/null timing for `finalization-ready` when both arise in one live action.

For a fresh close performed by this live coordinator, require `outcome: verified`, measured timing with a UUID attempt ID, and `change_quality.github: measured` for the exact completed `change-metadata`. For an Issue already closed when the current closure gate starts, require `outcome: no-op`, null attempt ID, reconstructed or unknown timing, `change_quality.github: unknown`, an empty `github_mutations` list, and a non-null reason code. Never report the recovery gate's duration as historical close duration or reconstruct a historical `change-metadata` mutation: the loaded Issue transport does not expose an authoritative close event or timeline.

The `manifest` level is 6/8 boundaries, the `closure` level is 7/9 after `finalization-ready`, and the `completion` level is 8/10 after `issue-closed`. Use `scripts/delivery_log.py` with the exact requested level. Require one unambiguous exact binding per selected boundary. At `closure`, require every manifest entry's boundary, comment URL/digest, transition key, and evidence to equal its selected binding. At `completion`, additionally require the Issue-closed input to name that exact finalization comment URL/digest and the same path kind, manifest digest, and Issue identity. A completion check therefore binds the stage manifest, then the finalization observation, then the Issue-closed observation; it does not build a self-referential completion manifest.

If the post-close comment is locked, forbidden, or indeterminate, keep the Issue closed and return `closed-but-log-pending` as the recovery condition. Never reopen it. For an ambiguous add-comment response, perform one complete exact Body/digest search before deciding whether the comment exists. After the comment is verified, independently re-read the Issue once more and require it to remain closed/completed.

An exact Issue already closed in the first immutable read remains a compatibility completed no-op without backfill when no trusted `finalization-ready` exists and the complete standalone or legacy workflow evidence proves terminal completion. Never infer this exception merely from absent or deleted log comments. A lineage with a trusted finalization that closes but lacks `issue-closed` is incomplete logging, not an open workflow state; keep it closed and reconstruct any missing boundary/manifest/finalization chain before repairing the closing observation.

## Return aggregate statistics

Aggregate only independently re-read valid observations:

~~~yaml
stage_logs:
  observation_urls: []
  observation_count: 0
  duplicate_transition_count: 0
  attempt_observations_by_stage: {}
  measured_elapsed_ms_by_stage: {}
  measured_elapsed_ms_total: 0
  unknown_timing_count: 0
  user_wait_ms_total: 0
  change_items_by_stage: {}
  unknown_change_domains_by_stage: {}
  final_product_net:
    files_changed: 0
    additions: 0
    deletions: 0
  final_memory_net:
    files_changed: 0
    additions: 0
    deletions: 0
  finalization_observation_url: null
  finalization_observation_sha256: null
  issue_closed_observation_url: null
  issue_closed_observation_sha256: null
  coverage_manifest_sha256: null
  coverage_level: null | manifest | closure | completion
  diagnostics: []
~~~

Count valid comment URLs in `observation_count`, and report comments beyond one per transition key in `duplicate_transition_count`. Count live executions and measured spans by unique non-null `attempt_id`, not by comment count or transition key. If records sharing one attempt ID disagree on elapsed/user-wait values, exclude that attempt from timing totals and add a diagnostic. Report reconstructed/unknown timing and change domains separately. Do not claim that summed spans equal elapsed calendar delivery time, and do not double-count retry file changes in final net totals.

## Preserve compatibility

- Treat this as additive schema version 1. Keep the three workflow markers and every existing callback schema unchanged.
- Continue accepting valid historical same-turn observations with measured `user_wait_ms`; every new split-turn confirmation writer uses null without changing the log schema or aggregate field.
- Existing open lineages may continue after reconstructing required successful-boundary observations with unknown timing.
- Exact standalone or legacy lineages already closed in the first immutable read with no trusted `finalization-ready` remain completed compatibility no-ops without backfill. A lineage with a trusted finalization requires `issue-closed` for completion but never reopens an Issue to obtain it.
- Unknown log schema versions, malformed schema-v1 observations, other authors, and duplicate comments never become legacy workflow evidence.
- Keep the log schema, stage/boundary enums, transition-key algorithm, timing semantics, preview limit, and coverage rules stable after publication. Change them only with an explicit compatibility migration and synchronized tests.
