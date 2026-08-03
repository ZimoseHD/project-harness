# Legacy Delivery Stage Log Contract

Load this contract only to read and diagnose `delivery-stage-observation` comments that were persisted by the pre-Lean Delivery protocol. Schema v1 is frozen compatibility data. A new `delivery`, any resumed `delivery`, and every standalone phase role must not write, replace, repair, backfill, or require a Delivery stage observation.

Historical observations can explain timing and past mutation summaries. They are never workflow state, product evidence, user approval, mutation authority, recovery authority, merge evidence, closure evidence, or durable project knowledge. Their presence, absence, validity, completeness, or coverage cannot gate phase dispatch, Pull Request merge, Issue closure, successful completion, or a no-op recovery.

## Keep logs observational

- Recognize a valid legacy observation only as a top-level source Issue comment with `record_kind: delivery-stage-observation` and `log_schema_version: 1`.
- Do not add a `${marker_namespace}` marker. Keep the three workflow marker families unchanged.
- Forbid the Delivery Coordinator, Phase Owners, direct read-only Workers, independent Reviewers, and standalone compatibility roles from creating or changing a Delivery observation. No current role owns this retired audit mutation.
- Never let an observation authorize phase dispatch, PASS, Context Promotion confirmation, PR merge, Issue closure, or a durable-memory update.
- Treat an edited, deleted, malformed, forged, stale, duplicate, or missing observation as a diagnostic condition only. Reconstruct workflow truth from the original Issue, PR, check, verdict, callback, merge, and state artifacts without repairing the log.
- Never persist raw user input, an Evidence Bundle, chat, reasoning, tool output, secrets, absolute local paths, or complete diffs while diagnosing historical records.
- Treat every historical stage observation as single-task chronology and therefore `no_write` during Context Promotion classification.

Only read these comments when they materially help a requested diagnosis or historical report. Do not enumerate all Issue comments merely to prove log absence or coverage.

## Use fixed stages and success boundaries

The following table is the frozen schema-v1 boundary vocabulary. It describes old records only and grants no current write authority:

| Boundary | Stage | Exact historical `outcome` | Historical durable result |
| --- | --- | --- | --- |
| `implementation-verified-draft` | `implementation` | `verified-draft-pr` | Exact independently verified Draft product PR |
| `closeout-accepted-ready` | `closeout` | `accepted-ready-pr` | PASS, Issue callback, active eligibility registration, and exact Ready product PR |
| `product-merged` | `product-integration` | `verified` or `no-op` | Exact verified merge or current-format already-merged `no-op` recovery |
| `context-proposal-reviewed` | `context-promotion` | `awaiting-confirmation` | Exact proposal artifact, Reviewer PASS, and active `awaiting-confirmation` callback |
| `context-confirmed` | `context-confirmation` | `confirmed` | Exact proposal-bound schema-v2 `confirmed` callback |
| `context-no-promotion-terminal` | `context-promotion` | `no-promotion` | Exact active historical `no-promotion` terminal |
| `memory-pr-ready` | `context-promotion` | `verified-memory-pr` or `memory-pr-ready` | Exact confirmed/reviewed Ready project-memory PR and callback |
| `memory-pr-merged` | `memory-integration` | `verified` or `no-op` | Exact verified merge or current-format already-merged `no-op` recovery |
| `context-memory-terminal` | `context-promotion` | `memory-pr-merged` | Exact active `memory-pr-merged` callback |
| `finalization-ready` | `finalization` | `ready-to-close` | Historical log coverage and Issue-closure prerequisites recorded by the old protocol |
| `issue-closed` | `finalization` | `verified` or `no-op` | Historical source Issue close observation |

The frozen `stage` values are `implementation`, `closeout`, `product-integration`, `context-promotion`, `context-confirmation`, `memory-integration`, and `finalization`. The frozen `activity` values are `initial`, `repair`, `resume`, `revalidate`, `accept`, `reconcile`, `integrate`, `recover`, `propose`, `revise`, `confirm`, `finalize`, and `closure-gate`.

## Write one exact schema

This historical heading and payload preserve the schema-v1 compatibility surface. Do not interpret the word “Write” as current mutation authority and do not produce a new instance.

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

When reading a legacy record, require its exact schema-v1 keys and enum values, a positive `attempt`, paired evidence URL/digest values, `raw_user_input_persisted: false`, and a null or lowercase kebab-case `reason_code`. Unknown schema versions and malformed schema-v1 comments are invalid diagnostics, never another legacy format.

## Calculate a deterministic transition key

Validate the frozen `transition_key` as lowercase SHA-256 over UTF-8 canonical JSON with sorted keys, compact separators, and no ASCII escaping for exactly these fields:

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

Exclude activity, top-level outcome, attempt ID, timestamps, elapsed time, attempt number, change quality/preview, reason code, and the observation's own URL/digest. Use `attempt_id`, not `transition_key`, to distinguish separate historical live executions. A valid transition key deduplicates diagnostics only; it does not prove the referenced workflow transition.

Use `scripts/delivery_log.py::validate_observation` only to dual-read a historical record. Do not call `validate_new_observation` to prepare a write, do not synthesize a missing transition key, and do not use the helper's coverage result as a workflow gate.

## Canonicalize snapshots and evidence

Preserve the old snapshot vocabulary while validating historical records:

| Boundary | Frozen `input_snapshot` identity | Frozen `output_snapshot` identity | Frozen evidence kinds |
| --- | --- | --- | --- |
| `implementation-verified-draft` | product base and nullable prior head | exact Draft product-PR tuple | `product-pr` |
| `closeout-accepted-ready` | exact product-PR tuple | acceptance, Issue callback, eligibility, Ready state | `product-pr`, `acceptance-comment`, `issue-callback`, `eligibility-registration` |
| `product-merged` | accepted product tuple and three gate-evidence pairs | merge method and merge identity | `product-pr`, `acceptance-comment`, `issue-callback`, `eligibility-registration` |
| `context-proposal-reviewed` | source merge, eligibility, authority base | proposal, review, nullable memory tuple | eligibility/proposal/review and optional `memory-pr` |
| `context-confirmed` | proposal, review, nullable memory tuple | confirmation and approved decision | proposal/review/confirmation |
| `context-no-promotion-terminal` | proposal, review, confirmation | terminal identity/outcome | proposal/confirmation/terminal |
| `memory-pr-ready` | proposal, review, confirmation | exact Ready memory tuple/callback | proposal/review/confirmation/memory/Ready |
| `memory-pr-merged` | exact Ready memory tuple/callback | merge method and identity | memory PR/Ready callback |
| `context-memory-terminal` | merged memory identity and Ready callback | terminal identity/outcome | memory/Ready/terminal |
| `finalization-ready` | path kind and coverage manifest | `ready: true` | selected stage observations and terminal callback |
| `issue-closed` | path kind, manifest, finalization observation | `closed` / `completed` | finalization observation |

Validate an old `observation_kind: attempt` against its frozen shape:

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

Require exact persistent evidence URL/whole-comment-digest bindings before reporting a historical claim. An observation's copied tuple or summary cannot substitute for reading the referenced artifact when current truth matters.

## Read without repair or backfill

1. Fetch only the comments needed by the requested diagnosis. Request complete pagination when—and only when—the diagnosis explicitly needs a complete historical inventory.
2. Normalize and digest the whole Markdown comment, validate schema v1, verify Issue identity and author when available, and separately read any original evidence needed for the report.
3. Group exact duplicates by whole-comment identity and group repeated live attempts by non-null `attempt_id`. Report conflicts as diagnostics instead of selecting workflow truth by timestamp, attempt number, or transition key.
4. Never add a reconstructed observation, replace an edited comment, retry an old ambiguous write, create `finalization-ready`, create `issue-closed`, or reopen a closed Issue.
5. Continue the current workflow from authoritative evidence regardless of legacy-log gaps. Do not pause before a merge or close to repair, complete, or enumerate observations.

## Interpret timing and changes conservatively

- Accept `timing_quality: measured` only with a non-null historical start, finish, non-negative elapsed value, and one consistent non-null UUIDv4 attempt ID. Never reconstruct elapsed time from GitHub timestamps.
- Keep reconstructed and unknown timing separate from measured timing. Do not claim summed coordinator spans equal calendar delivery time.
- Treat `user_wait_ms` as valid only for a historically valid same-turn record; never derive it from the interval between turns.
- Read repository, GitHub, and context change previews as bounded historical summaries, not diffs or mutation proof. Respect the frozen 100-entry combined preview limit and quality labels.
- Exclude invalid, conflicting, secret-bearing, raw-input-bearing, or absolute-local-path-bearing records from aggregates and report a diagnostic.

## Require three coverage levels

The old helper names `manifest`, `closure`, and `completion` are retained solely so historical reports can interpret already-persisted `finalization-ready` and `issue-closed` records. A current operation must not require, build, backfill, or pass any of these coverage levels.

Historically, a no-write path selected six successful boundaries and a memory-write path selected eight; `finalization-ready` extended those to closure, and `issue-closed` extended them to completion. The frozen manifest identity was:

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

Use historical coverage computation only as an optional diagnostic over complete, independently read legacy comments. A missing manifest, missing finalization record, missing post-close record, failed coverage result, locked Issue, or incomplete comment inventory has no effect on current completion and supplies no reason to mutate or reopen an Issue.

## Return aggregate statistics

When explicitly requested, return privacy-reduced diagnostics in the frozen aggregate shape. Null out fields that cannot be supported; never fill gaps by writing observations:

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

## Preserve compatibility

- Freeze `log_schema_version: 1`, stage/boundary/activity enums, transition-key algorithm, timing semantics, snapshot vocabulary, preview limit, manifest identity, and aggregate field names for read-only dual-read.
- Keep `scripts/delivery_log.py` and its schema-v1 validators for historical diagnostics. Their ability to construct or validate a prospective record does not authorize a write.
- Do not reinterpret an unknown version or malformed record as valid legacy data.
- Do not add a schema-v2 log. Lean Delivery has no stage-log writer, backfill obligation, coverage gate, finalization observation, or post-close observation.
