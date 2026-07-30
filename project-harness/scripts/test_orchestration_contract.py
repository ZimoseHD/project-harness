#!/usr/bin/env python3
"""Executable consistency checks for the Project Harness orchestration protocol."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"


def read_text(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def markdown_section(markdown: str, heading: str) -> str:
    """Return one exact level-two Markdown section, including its heading."""
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)",
        markdown,
    )
    if match is None:
        raise AssertionError(f"missing Markdown section: {heading}")
    return match.group(0)


class ProtocolAssertions(unittest.TestCase):
    def assertContainsAll(
        self,
        text: str,
        needles: tuple[str, ...],
        *,
        source: str,
    ) -> None:
        for needle in needles:
            with self.subTest(source=source, required=needle):
                self.assertIn(needle, text)

    def assertInOrder(
        self,
        text: str,
        needles: tuple[str, ...],
        *,
        source: str,
    ) -> None:
        cursor = -1
        for needle in needles:
            position = text.find(needle, cursor + 1)
            with self.subTest(source=source, ordered=needle):
                self.assertGreater(
                    position,
                    cursor,
                    f"{needle!r} is missing or out of order in {source}",
                )
            cursor = position


class OrchestrationContractTests(ProtocolAssertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read_text("SKILL.md")
        cls.delivery = read_text("references/delivery.md")
        cls.definition = read_text("references/definition.md")
        cls.context_authoring = read_text("references/context-authoring.md")
        cls.init = read_text("references/init.md")
        cls.implementation = read_text("references/implementation.md")
        cls.closeout = read_text("references/closeout.md")
        cls.promotion = read_text("references/context-promotion.md")
        cls.evidence = read_text("references/delivery-evidence-contract.md")
        cls.delivery_log = read_text("references/delivery-log-contract.md")
        cls.issue_transport = read_text("references/issue-transport.md")
        cls.pr_transport = read_text("references/pull-request-transport.md")
        cls.openai = read_text("agents/openai.yaml")

    def test_delivery_is_the_normal_exact_entry_and_phase_roles_remain(self) -> None:
        invocation = markdown_section(self.skill, "Require an exact invocation")
        dispatch = markdown_section(self.skill, "Load one top-level operation")

        self.assertContainsAll(
            invocation,
            (
                "role: delivery",
                "role: definition | context-authoring | implementation | closeout | context-promotion",
                "normal automated delivery tail",
                "single compatibility or recovery phase",
            ),
            source="SKILL.md invocation contract",
        )

        expected_rows = {
            "init": "references/init.md",
            "definition": "references/definition.md",
            "context-authoring": "references/context-authoring.md",
            "delivery": "references/delivery.md",
            "implementation": "references/implementation.md",
            "closeout": "references/closeout.md",
            "context-promotion": "references/context-promotion.md",
        }
        actual_rows = dict(
            re.findall(r"(?m)^\| `([^`]+)` \| `([^`]+\.md)` \|", dispatch)
        )
        self.assertEqual(actual_rows, expected_rows)
        for reference in actual_rows.values():
            with self.subTest(reference=reference):
                self.assertTrue((SKILL_ROOT / reference).is_file())

        self.assertContainsAll(
            self.openai,
            (
                "role: delivery",
                "code-capable mode",
                "one Phase Owner per semantic round",
                "direct read-only Workers and Reviewers",
                "automatic configured product and memory PR merges",
                "summarize the exact proposal and finish the turn",
                "explicit source-bound re-entry",
                "persistent stage observations",
                "and Issue closure",
                "role: init for schema-v2 project integration policy",
                "compatibility or recovery",
                "allow_implicit_invocation: false",
            ),
            source="agents/openai.yaml",
        )
        self.assertNotIn("run one feature-iteration phase", self.openai)
        self.assertNotIn("In Plan mode", self.openai)
        self.assertNotIn("request_user_input", self.openai)
        self.assertIn("disable-model-invocation: false", self.skill)
        self.assertContainsAll(
            self.skill,
            (
                "Codex requires the user's `$project-harness` trigger",
                "Claude Code may load the Skill from the user's `/project-harness` trigger or by model selection",
                "`disable-model-invocation: false`",
                "host loading alone never supplies a role",
                "Reject before Harness mutation when the current message lacks that packet",
            ),
            source="cross-host invocation adapter contract",
        )
        for role, text, heading in (
            ("implementation", self.implementation, "Enforce the phase boundary"),
            ("closeout", self.closeout, "Enforce the authority boundary"),
        ):
            boundary = markdown_section(text, heading)
            with self.subTest(host_neutral_standalone_authority=role):
                self.assertContainsAll(
                    boundary,
                    (
                        f"current user message's exact host-valid `role: {role}` packet",
                        "root Skill's invocation-adapter contract",
                        "host/model loading or automatic routing by itself",
                    ),
                    source=f"{role} standalone authority",
                )
                self.assertNotIn("explicit `$project-harness`", boundary)

    def test_upstream_handoffs_describe_the_split_turn_delivery_boundary(self) -> None:
        definition_handoff = markdown_section(self.definition, "6. Hand off and stop")
        context_handoff = markdown_section(
            self.context_authoring,
            "Return a closed result",
        )

        self.assertContainsAll(
            definition_handoff,
            (
                "start the automated Implementation → Closeout → Context Promotion chain",
                "unconfirmed Context Promotion proposal will be summarized at a turn boundary",
                "later explicit source-bound `delivery` re-entry",
            ),
            source="Definition delivery handoff",
        )
        self.assertContainsAll(
            context_handoff,
            (
                "first explicit delivery invocation coordinates every phase through the reviewed Context Promotion proposal",
                "proposal summary supplies the exact later source-bound re-entry",
                "confirmation and any remaining integration",
            ),
            source="Context Authoring delivery handoff",
        )

    def test_delivery_evidence_has_one_authority_and_is_routed_by_role(self) -> None:
        dispatch = markdown_section(self.skill, "Load one top-level operation")
        boundary = markdown_section(self.delivery, "Enforce the coordinator boundary")

        self.assertContainsAll(
            dispatch,
            (
                "**Delivery evidence contract:** `references/delivery-evidence-contract.md`",
                "`delivery` | `references/delivery.md` | Issue transport; Pull Request transport; Delivery evidence contract; Delivery stage log contract",
                "`implementation` | `references/implementation.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract",
                "`closeout` | `references/closeout.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract",
                "`context-promotion` | `references/context-promotion.md` | Issue transport; Pull Request transport; Issue contract; Product PR contract; Delivery evidence contract",
                "The evidence contract lets it validate persistent artifact schemas and predecessor bindings only",
                "grants no phase behavior authority",
            ),
            source="shared evidence routing",
        )
        implementation_row = re.search(
            r"(?m)^\| `implementation` \|.*$",
            dispatch,
        )
        self.assertIsNotNone(implementation_row)
        assert implementation_row is not None
        self.assertNotIn("Delivery evidence contract", implementation_row.group(0))
        self.assertContainsAll(
            boundary,
            (
                "`references/delivery-evidence-contract.md`",
                "Use that contract only for persistent schema, tuple/digest, predecessor, active-tip, and legacy dual-read checks",
                "never use it to perform phase reasoning or produce a phase artifact",
            ),
            source="coordinator evidence boundary",
        )

        signatures = (
            "verdict: PASS | FAIL | BLOCKED",
            "callback: product-acceptance-pass",
            "artifact_kind: context-promotion-proposal",
            "review_kind: context-promotion-no-write",
            "review_kind: context-promotion-write",
            "outcome: awaiting-confirmation",
            "outcome: confirmed",
            "outcome: no-promotion",
            "outcome: memory-pr-ready",
            "outcome: memory-pr-merged",
        )
        documents = {
            path.relative_to(SKILL_ROOT).as_posix(): path.read_text(encoding="utf-8")
            for path in REFERENCES.glob("*.md")
        }
        documents["SKILL.md"] = self.skill
        for signature in signatures:
            with self.subTest(signature=signature):
                sources = [
                    path
                    for path, body in documents.items()
                    if re.search(rf"(?m)^{re.escape(signature)}$", body)
                ]
                self.assertEqual(
                    sources,
                    ["references/delivery-evidence-contract.md"],
                )

    def test_delivery_evidence_fixtures_have_unique_top_level_keys(self) -> None:
        blocks = re.findall(
            r"(?ms)^~~~(?:yaml|text)\n(.*?)\n~~~$",
            self.evidence,
        )
        self.assertGreaterEqual(len(blocks), 12)
        for index, block in enumerate(blocks):
            keys = re.findall(r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):", block)
            with self.subTest(block=index):
                self.assertEqual(
                    len(keys),
                    len(set(keys)),
                    f"duplicate top-level key in evidence block {index}: {keys}",
                )

    def test_delivery_log_has_one_schema_and_fixed_boundaries(self) -> None:
        schema_sources = [
            path.relative_to(SKILL_ROOT).as_posix()
            for path in REFERENCES.glob("*.md")
            if re.search(
                r"(?m)^record_kind: delivery-stage-observation$",
                path.read_text(encoding="utf-8"),
            )
        ]
        self.assertEqual(schema_sources, ["references/delivery-log-contract.md"])

        fixed = markdown_section(self.delivery_log, "Use fixed stages and success boundaries")
        rows = re.findall(
            r"(?m)^\| `([^`]+)` \| `([^`]+)` \| (.*?) \|",
            fixed,
        )
        self.assertEqual(
            rows,
            [
                (
                    "implementation-verified-draft",
                    "implementation",
                    "`verified-draft-pr`",
                ),
                (
                    "closeout-accepted-ready",
                    "closeout",
                    "`accepted-ready-pr`",
                ),
                ("product-merged", "product-integration", "`verified` or `no-op`"),
                (
                    "context-proposal-reviewed",
                    "context-promotion",
                    "`awaiting-confirmation`",
                ),
                ("context-confirmed", "context-confirmation", "`confirmed`"),
                (
                    "context-no-promotion-terminal",
                    "context-promotion",
                    "`no-promotion`",
                ),
                (
                    "memory-pr-ready",
                    "context-promotion",
                    "`verified-memory-pr` or `memory-pr-ready`",
                ),
                ("memory-pr-merged", "memory-integration", "`verified` or `no-op`"),
                (
                    "context-memory-terminal",
                    "context-promotion",
                    "`memory-pr-merged`",
                ),
                ("finalization-ready", "finalization", "`ready-to-close`"),
                ("issue-closed", "finalization", "`verified` or `no-op`"),
            ],
        )

        schema = markdown_section(self.delivery_log, "Write one exact schema")
        self.assertContainsAll(
            schema,
            (
                "log_schema_version: 1",
                "observation_kind: boundary | attempt",
                "transition_key: SHA256",
                "attempt_id:",
                "elapsed_ms: 60000 | null",
                "timing_quality: measured | reconstructed | unknown",
                "change_quality:",
                "repository: measured | reconstructed | unknown | not-applicable",
                "repository_changes: []",
                "github_mutations: []",
                "context_changes: []",
                "raw_user_input_persisted: false",
            ),
            source="Delivery observation schema",
        )

    def test_delivery_logs_are_coordinator_owned_audit_only_comments(self) -> None:
        dispatch = markdown_section(self.skill, "Load one top-level operation")
        delegation = markdown_section(self.skill, "Delegate without expanding authority")
        markers = markdown_section(self.skill, "Preserve persistent markers")
        observational = markdown_section(self.delivery_log, "Keep logs observational")

        self.assertContainsAll(
            dispatch,
            (
                "**Delivery stage log contract:** `references/delivery-log-contract.md`",
                "`delivery` | `references/delivery.md` | Issue transport; Pull Request transport; Delivery evidence contract; Delivery stage log contract",
            ),
            source="Delivery log routing",
        )
        self.assertContainsAll(
            delegation,
            (
                "coordinator alone receives",
                "Issue `add-comment` for exact Delivery stage observations",
                "Never place merge, closure, or Delivery-log authority in a phase envelope",
            ),
            source="Delivery log mutation ownership",
        )
        self.assertContainsAll(
            observational,
            (
                "top-level source Issue comment",
                "Do not add a `${marker_namespace}` marker",
                "Forbid Phase Owners, their direct read-only Workers, and independent Reviewers from writing Delivery observations",
                "Only the Delivery Coordinator owns this audit mutation",
                "Never let an observation authorize phase dispatch, PASS, Context Promotion confirmation, PR merge, Issue closure, or a durable-memory update",
                "audit/compliance defect only",
            ),
            source="Delivery log authority boundary",
        )
        self.assertIn("Keep the three marker names above unchanged", markers)
        self.assertIn("not a recovery authority", self.delivery)
        self.assertIn("stage observation", self.issue_transport)
        self.assertIn(
            "standalone `context-promotion` follows its compatibility closure gate without Delivery observations",
            self.skill,
        )

    def test_delivery_log_identity_snapshots_and_manifest_are_canonical(self) -> None:
        identity = markdown_section(
            self.delivery_log,
            "Calculate a deterministic transition key",
        )
        snapshots = markdown_section(
            self.delivery_log,
            "Canonicalize snapshots and evidence",
        )
        coverage = markdown_section(
            self.delivery_log,
            "Require three coverage levels",
        )

        identity_json = re.search(
            r"~~~json\n(.*?)\n~~~",
            identity,
            re.DOTALL,
        )
        self.assertIsNotNone(identity_json)
        assert identity_json is not None
        self.assertNotIn('"activity"', identity_json.group(1))
        self.assertNotIn('"outcome"', identity_json.group(1))
        self.assertContainsAll(
            identity,
            (
                "Exclude activity, top-level outcome, attempt ID",
                "Use `attempt_id`, not `transition_key`, to distinguish separate live executions",
            ),
            source="Delivery transition identity",
        )
        self.assertContainsAll(
            snapshots,
            (
                "| `implementation-verified-draft` |",
                "| `closeout-accepted-ready` |",
                "| `product-merged` |",
                "| `context-proposal-reviewed` |",
                "| `context-confirmed` |",
                "| `context-no-promotion-terminal` |",
                "| `memory-pr-ready` |",
                "| `memory-pr-merged` |",
                "| `context-memory-terminal` |",
                "| `finalization-ready` |",
                "| `issue-closed` |",
                "target_boundary: null",
                "source_bindings: []",
                "response_kind: null",
                "modification_item_count: null",
                "Reuse the same `attempt_id`",
                "Group aggregate attempt/timing statistics by `attempt_id`",
            ),
            source="Delivery canonical snapshots",
        )
        self.assertContainsAll(
            coverage,
            (
                "manifest_schema_version: 1",
                "path_kind: no-write | memory-write",
                "entries:",
                "observation_url: URL",
                "observation_sha256: SHA256",
                "transition_key: SHA256",
                "sorted keys, compact separators, and no ASCII escaping",
                "`manifest` level is 6/8",
                "`closure` level is 7/9",
                "`completion` level is 8/10",
                "does not build a self-referential completion manifest",
            ),
            source="Delivery canonical coverage manifest",
        )

    def test_delivery_log_timing_changes_privacy_and_recovery_are_explicit(self) -> None:
        timing = markdown_section(self.delivery_log, "Measure time honestly")
        changes = markdown_section(
            self.delivery_log,
            "Summarize modifications without copying them",
        )
        privacy = markdown_section(
            self.delivery_log,
            "Protect user and environment data",
        )
        recovery = markdown_section(
            self.delivery_log,
            "Deduplicate and backfill safely",
        )

        self.assertContainsAll(
            timing,
            (
                "inclusive wall duration",
                "Use a monotonic clock",
                "ending in `Z`",
                "timing_quality: measured",
                "current split-turn confirmation flow must write `user_wait_ms: null`",
                "only after the explicit re-entry arrives",
                "never the interval between turns",
                "Never duplicate one measured span",
                "timing_quality: reconstructed",
                "Use `unknown` only when neither exact timestamp can be established",
                "Never fabricate historical duration",
            ),
            source="Delivery log timing",
        )
        self.assertContainsAll(
            changes,
            (
                "status: added | modified | removed | renamed",
                "operation: create-draft | replace-content | add-comment | mark-ready | convert-to-draft | merge | change-metadata",
                "action: add | update | supersede | no_write",
                "Limit the combined preview lists to 100 entries",
                "final net PR diffs",
                "change_quality",
                "Delivery observation `add-comment` mutations are intentionally excluded",
            ),
            source="Delivery log changes",
        )
        self.assertContainsAll(
            privacy,
            (
                "raw confirmation replies or their digests",
                "legacy `request_user_input` modification text",
                "absolute local paths",
                "map a proposal-bound top-level decision exactly",
                "modification item count",
                "best-effort and never part of boundary coverage",
                "always `no_write` during Context Promotion classification",
            ),
            source="Delivery log privacy",
        )
        self.assertContainsAll(
            recovery,
            (
                "comments completely, including pagination",
                "Return `no-op` only when an existing whole comment exactly matches",
                "harmless audit duplicates",
                "reconstructed observation with null elapsed time",
                "Never repeat a merge, confirmation, or closure mutation",
                "never reopen it to repair logging",
            ),
            source="Delivery log recovery",
        )

    def test_delivery_log_coverage_precedes_issue_close_and_is_reported(self) -> None:
        persistence = markdown_section(
            self.delivery,
            "Persist Delivery stage observations",
        )
        closure = markdown_section(self.delivery, "Close the source Issue")
        result = markdown_section(self.delivery, "Return the delivery result")
        compatibility = markdown_section(self.delivery_log, "Preserve compatibility")

        self.assertContainsAll(
            persistence,
            (
                "For every bounded Phase Owner attempt, merge gate, confirmation round, reconciliation, and finalization gate",
                "scripts/delivery_log.py",
                "comments_complete: true",
                "coordinator's verified mutation-author identity",
                "duplicate observations share one transition key",
                "timing_quality: reconstructed",
                "UUIDv4 `attempt_id`",
                "same Owner continues that round",
                "A re-review or narrow Worker replacement inside the unchanged round does not create another Owner attempt",
            ),
            source="Delivery observation persistence",
        )
        self.assertInOrder(
            closure,
            (
                "every required success boundary",
                "Build the exact 6/8-boundary stage coverage manifest",
                "`finalization-ready` boundary observation",
                "explicit `change-metadata` mutation",
                "Independently read the Issue back",
                "`issue-closed` boundary observation",
                'coverage(..., level="completion")',
            ),
            source="Delivery log closure order",
        )
        self.assertContainsAll(
            closure,
            (
                "still-closed Issue",
                "closed-but-log-pending",
                "never reopen or repeat the close mutation",
                "require it to remain `closed`/`completed`",
                "`locked: false`",
                "never unlock an Issue",
            ),
            source="post-close observation recovery",
        )
        self.assertContainsAll(
            result,
            (
                "stage_logs:",
                "attempt_observations_by_stage: {}",
                "measured_elapsed_ms_by_stage: {}",
                "measured_elapsed_ms_total: 0",
                "unknown_timing_count: 0",
                "user_wait_ms_total: 0",
                "change_items_by_stage: {}",
                "unknown_change_domains_by_stage: {}",
                "final_product_net:",
                "final_memory_net:",
                "issue_closed_observation_url:",
                "coverage_manifest_sha256:",
                "coverage_level: null | manifest | closure | completion",
                "complete paginated reads",
            ),
            source="Delivery log aggregate result",
        )
        self.assertContainsAll(
            compatibility,
            (
                "additive schema version 1",
                "Existing open lineages",
                "unknown timing",
                "Exact standalone or legacy lineages already closed in the first immutable read",
                "completed compatibility no-ops without backfill",
            ),
            source="Delivery log additive migration",
        )

    def test_issue_transport_and_context_promotion_keep_logs_non_authoritative(
        self,
    ) -> None:
        authority = markdown_section(
            self.issue_transport,
            "Require explicit write authority",
        )
        transport_result = markdown_section(
            self.issue_transport,
            "Return the shared result envelope",
        )

        self.assertContainsAll(
            self.issue_transport,
            (
                "complete paginated comment enumeration",
                "source-Issue Delivery observation comments",
            ),
            source="Issue observation transport",
        )
        self.assertContainsAll(
            authority,
            (
                "current `delivery` coordinator",
                "Never accept such a payload from a Phase Owner, Worker, Reviewer, standalone compatibility role",
                "does not decide whether a stage completed or whether log coverage is sufficient",
                "stage observation",
                "still-closed Issue",
                "never reopen it",
                "`closed`/`completed` after comment read-back",
            ),
            source="Issue observation authority",
        )
        self.assertContainsAll(
            transport_result,
            (
                "comments_complete: null",
                "comments_next_cursor: null",
                "locked: false",
                "Set `comments_complete: true` only after every requested page is fetched",
            ),
            source="Issue observation pagination result",
        )
        self.assertContainsAll(
            self.promotion,
            (
                "record_kind: delivery-stage-observation",
                "audit-only single-task chronology",
                "Classify Delivery stage observations as `no_write`",
                "Never write raw confirmation-response text, its digest",
                "do not read, write, or judge Delivery observation coverage",
            ),
            source="Context Promotion log exclusion",
        )

    def test_coordinator_reuses_one_owner_per_semantic_round(self) -> None:
        boundary = markdown_section(self.delivery, "Enforce the coordinator boundary")
        recovery = markdown_section(self.delivery, "Reconstruct the persistent state")
        dispatch = markdown_section(self.delivery, "Dispatch bounded Phase Owners")

        self.assertContainsAll(
            boundary,
            (
                "one Delivery Coordinator",
                "one isolated Phase Owner for every Implementation, Closeout, Context Promotion proposal revision, or terminal-reconciliation semantic round",
                "Keep that Owner live while those bindings and target remain unchanged",
                "Do not replace it because a read is slow, a tool is actively running, one direct Worker fails, or an independent Reviewer returns `FAIL`",
                "only direct read-only Workers or an independent Reviewer",
                "sole phase writer and hand-off producer",
                "Workers and Reviewers cannot delegate further",
                "independently reading each newly produced artifact",
                "`L1 semantic-freshness` probes",
                "Reuse unchanged normalized content from the coordinator-owned Evidence Bundle",
                "Never ask the user to create a new session for a normal transition",
                "coordinator consumes the persistent hand-off",
                "Perform the two permitted merge gates automatically and only in the coordinator",
                "Never open a user decision gate outside Context Promotion",
                "ends a turn and waits for an explicit source-bound re-entry",
            ),
            source="delivery coordinator boundary",
        )
        self.assertContainsAll(
            recovery,
            (
                "Reconstruct the next state from authoritative artifacts",
                "Every transition must already be reconstructible from GitHub",
                "Implementation persists commits, the Draft product PR",
                "Closeout persists an append-only verdict",
                "Product integration persists the PR merge state and merge commit identity",
                "Context Promotion persists proposal, confirmation, Ready/terminal callbacks",
                "Do not add another run marker or local coordinator checkpoint",
                "only the two `awaiting-confirmation` rows apply",
                "legacy reconstruction rows cannot also match",
                "with no schema-v2 `awaiting-confirmation` tip",
                "handle confirmation only in a later bound decision turn",
                "Exact proposal artifact and, for a write, unchanged Draft project-memory PR exist",
                "Resume independent review for the unchanged persisted proposal",
                "do not repeat classification, branch creation, commit, push, PR creation, or artifact persistence",
            ),
            source="delivery recovery contract",
        )
        self.assertContainsAll(
            dispatch,
            (
                "| `implementation` |",
                "| `closeout` |",
                "| `context-promotion` |",
                "persistent evidence URLs",
                "Permitted responsibility",
                "retain the same live Owner until it returns the typed result or the round identity changes",
                "Do not use fixed checkpoint silence as proof of failure",
                "Forbid a Phase Owner from loading `references/delivery.md` or another phase reference",
                "Forbid every Worker or Reviewer from loading additional phase references",
            ),
            source="delivery phase dispatch",
        )

        legacy_session_phrases = (
            "new clean `project-harness` session",
            "Use a clean session for every role",
            "require a repeated `context-promotion` invocation",
        )
        combined = "\n".join(
            (self.skill, self.delivery, self.implementation, self.closeout, self.promotion)
        )
        for phrase in legacy_session_phrases:
            with self.subTest(legacy_session_phrase=phrase):
                self.assertNotIn(phrase, combined)

    def test_fixed_two_hop_delegation_preserves_single_owner_authority(self) -> None:
        delegation = markdown_section(self.skill, "Delegate without expanding authority")
        self.assertContainsAll(
            delegation,
            (
                "parent_role: delivery",
                "delegated_role: implementation | closeout | context-promotion",
                "bound_snapshot:",
                "persistent_evidence_urls: []",
                "allowed_mutations:",
                "repository: []",
                "issue_transport: []",
                "pull_request_transport: []",
                "host parent-child provenance",
                "Phase Owner and sole holder of that phase's mutation set",
                "only direct, narrow, read-only Workers or one fresh independent Reviewer",
                "Give every Worker and Reviewer an empty persistent mutation set",
                "Forbid them from creating descendants",
                "changing tracked files",
                "Owner-provided isolated scratch space",
                "Require the Owner to integrate and independently verify every structured result",
                "Owner—not the Reviewer—to compose and persist every workflow-owned review artifact",
                "Keep one live Owner for one exact combination",
                "A slow read, active tool call, Worker failure, or Reviewer `FAIL` does not create a new semantic round",
                "Forbid every descendant from merging a PR, closing the source Issue, approving a Context Promotion proposal for the user",
            ),
            source="root delegation envelope",
        )

        self.assertContainsAll(
            self.implementation,
            (
                "host-provenance-bound delegation",
                "fixed two-hop delegation topology",
                "Implementation Phase Owner may directly delegate narrow read-only exploration, research, and verification",
                "sole writer and sole owner of the branch",
                "Do not use parallel writers",
                "Forbid source or durable-artifact writes and forbid further delegation",
                "Only the Implementation Phase Owner may return the verified phase hand-off",
            ),
            source="Implementation delegation",
        )
        self.assertContainsAll(
            self.closeout,
            (
                "host-provenance-bound delegation",
                "fixed two-hop delegation topology",
                "Closeout Phase Owner may directly delegate narrow read-only verification",
                "sole phase writer and sole producer of the acceptance verdict",
                "every Worker and Reviewer must remain mutation-free",
                "must not delegate further",
                "no Worker or Reviewer may edit code, write the verdict, mutate GitHub, delegate further, merge, close the Issue, or approve promotion",
            ),
            source="Closeout delegation",
        )
        self.assertContainsAll(
            self.promotion,
            (
                "host-provenance-bound delegation",
                "fixed two-hop delegation topology",
                "Context Promotion Phase Owner may directly delegate narrow read-only evidence, authority, and validation work",
                "sole phase writer and sole producer of proposal artifacts, Reviewer PASS evidence",
                "every Worker and Reviewer must remain mutation-free",
                "must not delegate further",
                "the coordinator retains both PR merge operations and final Issue closure",
                "never merge a PR, and never approve a proposal on the user's behalf",
            ),
            source="Context Promotion delegation",
        )

        combined = "\n".join(
            (delegation, self.implementation, self.closeout, self.promotion)
        )
        self.assertIn("fixed two-hop topology", self.delivery)
        self.assertNotIn("sub-subagent", combined)
        self.assertNotIn("Primary Implementation Agent", combined)

    def test_reviewer_returns_verdict_and_promotion_owner_persists_pass(self) -> None:
        review = markdown_section(self.promotion, "Require independent review")
        evidence_intro = self.evidence

        self.assertContainsAll(
            review,
            (
                "structured, non-persistent PASS or blocking FAIL verdict",
                "Forbid edits, GitHub mutations, further delegation",
                "return its tuple-bound verdict only to the Context Promotion Phase Owner",
                "Reviewer must never persist its own PASS comment or callback",
                "Fix blockers in the same Owner",
                "Context Promotion Phase Owner composes the exact **Reviewer PASS for no-write** artifact",
                "Context Promotion Phase Owner composes the exact **Reviewer PASS for a write** artifact",
            ),
            source="read-only Reviewer and Owner-owned PASS",
        )
        self.assertContainsAll(
            evidence_intro,
            (
                "persistent evidence of an independent Reviewer's returned, tuple-bound read-only verdict",
                "The Reviewer never writes that GitHub comment",
                "Context Promotion Phase Owner is its producer",
                "persists it through the loaded Pull Request transport",
            ),
            source="Reviewer PASS producer ownership",
        )

    def test_delegated_write_authority_is_consistent_across_transports(self) -> None:
        self.assertContainsAll(
            self.issue_transport,
            (
                "current explicit `delivery` invocation",
                "host-provenance-bound delegation",
                "mutation whitelist includes it",
                "current `delivery` coordinator",
                "current explicit standalone `role: context-promotion`",
                "Never accept final closure from a Phase Owner delegated by `delivery`, a Worker, a Reviewer, or any other descendant",
                "serialized delegation envelope",
                "prior hand-off",
            ),
            source="Issue transport authority",
        )
        self.assertContainsAll(
            self.pr_transport,
            (
                "current explicit `delivery` invocation",
                "host-provenance-bound delegation",
                "mutation whitelist includes it",
                "Allow `merge` only to the current `delivery` coordinator",
                "never accept it from a Phase Owner, Worker, Reviewer, or other descendant",
                "serialized delegation envelope",
                "prior hand-off",
            ),
            source="Pull Request transport authority",
        )

        for name, phase in (
            ("Implementation", self.implementation),
            ("Closeout", self.closeout),
            ("Context Promotion", self.promotion),
        ):
            with self.subTest(phase=name):
                self.assertIn("current explicit `delivery` invocation", phase)
                self.assertIn("delegation", phase)

    def test_config_v2_merge_policy_and_v1_dual_read_preflight_are_explicit(
        self,
    ) -> None:
        init_input = markdown_section(
            self.init,
            "Accept only the initialization packet",
        )
        init_v2 = markdown_section(self.init, "Write schema version 2")
        init_v1 = markdown_section(self.init, "Dual-read schema version 1")
        init_lifecycle = markdown_section(
            self.init,
            "Create or verify idempotently",
        )
        delivery_input = markdown_section(self.delivery, "Accept the delivery input")
        root_config = markdown_section(self.skill, "Load project-owned configuration")
        root_policy = markdown_section(self.skill, "Bind repository policy and mutations")

        for source, section in (
            ("init packet", init_input),
            ("schema-v2 config", init_v2),
        ):
            self.assertContainsAll(
                section,
                (
                    "schema_version: 2",
                    "marker_namespace: project-slug",
                    "integration:",
                    "base_branch: develop",
                    "product_pr:",
                    "memory_pr:",
                    "merge_method: merge",
                ),
                source=source,
            )
        self.assertContainsAll(
            init_v2,
            (
                "each `merge_method` to equal exactly `merge`, `squash`, or `rebase`",
                "Product and project-memory methods may differ",
                "Do not infer or normalize any value",
                "scripts/config_guard.py",
                "--migrate-v1",
                "--product-method",
                "--memory-method",
                "outcome: migration-rendered",
                "`rendered_config`",
            ),
            source="schema-v2 policy",
        )
        self.assertContainsAll(
            init_v1,
            (
                "schema_version: 1",
                "Reject extra or duplicate keys",
                "reports exactly one available method",
                "stop before its first mutation",
                "Never create a new schema-v1 file",
                "never silently add integration defaults",
            ),
            source="schema-v1 strict dual-read",
        )
        self.assertContainsAll(
            init_lifecycle,
            (
                "valid schema-v1 config",
                "complete schema-v2 policy with the exact same namespace",
                "require the baseline to remain unchanged",
                "Render one canonical schema-v2 replacement",
                "Never rename an established namespace",
            ),
            source="namespace-preserving v1 migration",
        )
        self.assertContainsAll(
            root_config,
            (
                "Write schema-v2 for every new configuration",
                "Strictly dual-read an existing schema-v1 file",
                "reports exactly one available method",
                "stop before the first lifecycle mutation",
                "hand off to explicit `role: init` schema-v2 migration",
                "preserves the exact namespace",
            ),
            source="root config compatibility",
        )
        self.assertContainsAll(
            delivery_input,
            (
                "Before the first mutation",
                "Parse `.project-harness/config.yaml` with `scripts/config_guard.py`",
                "Bind the validated schema version, namespace, base, policy source, and resolved product/project-memory methods",
                "For schema-v2",
                "For schema-v1 compatibility",
                "contain exactly one method",
                "Return blocked before Implementation and before any mutation",
                "recovery_condition: merge-policy-migration-required",
                "hand off to exact `role: init`",
                "unchanged namespace",
                "authoritative available-method set",
                "both unresolved product/project-memory policy choices",
                "only the user's later explicit `init` packet may complete those fields",
                "recovery_condition: configured-merge-method-unavailable",
                "never choose another enabled method or ask the user to merge manually",
                "merge the exact accepted product PR into `develop` automatically",
                "merge the exact user-confirmed and independently reviewed project-memory PR into `develop` automatically",
            ),
            source="Delivery immutable merge-policy preflight",
        )
        self.assertContainsAll(
            root_policy,
            (
                "Never infer a merge method from enabled repository buttons",
                "ask the user to perform a normal Delivery merge",
                "integration.product_pr.merge_method",
                "integration.memory_pr.merge_method",
                "sole authoritatively available repository method",
                "Before the first Delivery mutation",
                "Perform both permitted merges automatically",
                "never present manual merge as the normal recovery action",
            ),
            source="automatic configured merges",
        )

    def test_delivery_has_two_exact_guarded_merge_gates(self) -> None:
        merge_headings = re.findall(r"(?m)^## (Merge .+)$", self.delivery)
        self.assertEqual(
            merge_headings,
            ["Merge the accepted product PR", "Merge approved project memory"],
        )

        product_merge = markdown_section(self.delivery, "Merge the accepted product PR")
        memory_merge = markdown_section(self.delivery, "Merge approved project memory")
        for name, section, bound_method in (
            (
                "product merge gate",
                product_merge,
                "bound product method",
            ),
            (
                "project-memory merge gate",
                memory_merge,
                "bound project-memory method",
            ),
        ):
            self.assertContainsAll(
                section,
                (
                    "merge method",
                    bound_method,
                    "Immediately re-parse `.project-harness/config.yaml`",
                    "re-resolve repository capability through `scripts/config_guard.py`",
                    "both resolved methods to equal the live preflight baseline",
                    "remain available",
                    "semantic config drift",
                    "changed schema-v1 method uniqueness",
                    "loaded Pull Request transport",
                    "`merge` operation",
                    "Independently",
                    "`develop`",
                    "merge commit identity",
                ),
                source=name,
            )

        merge_guard = markdown_section(self.pr_transport, "Guard an exact merge")
        self.assertContainsAll(
            self.pr_transport,
            (
                "| merge | Merge one exact open Ready PR only for the current `delivery` coordinator.",
                "operation: search | read | create-draft | replace-content | add-comment | replace-comment | read-checks | mark-ready | convert-to-draft | merge",
                "merge_commit_sha: null",
                "merge_method: null",
                "available_merge_methods: []",
                "merge_methods_known: null",
            ),
            source="Pull Request merge surface",
        )
        self.assertContainsAll(
            merge_guard,
            (
                "role: delivery",
                "base ref `develop`",
                "required_checks_known: true",
                "`mergeable: true`",
                "schema-v2 uses the configured product or project-memory method",
                "schema-v1 compatibility uses the sole authoritatively available method",
                "Never choose or substitute a method in the transport",
                "merge_methods_known: true",
                "available_merge_methods",
                "persistent gate evidence URL/digest pairs",
                "Closeout PASS",
                "proposal artifact, confirmation, Reviewer PASS, and memory-pr-ready callback",
                "Compare every expected field, protected field, evidence URL/digest",
                "already merged",
                "Return `no-op` only for an exact match",
                "Do not retry a timeout or missing response",
                "Recover an ambiguous response only by independently fetching the exact PR",
                "merged: true",
                "non-null merge commit identity",
            ),
            source="exact merge guard",
        )
        self.assertIn("Closeout never merges", self.closeout)
        self.assertIn("Do not merge the project-memory PR", self.promotion)

    def test_context_promotion_uses_a_split_turn_source_bound_user_gate(self) -> None:
        invocation = markdown_section(self.skill, "Require an exact invocation")
        delivery_input = markdown_section(self.delivery, "Accept the delivery input")
        relay = markdown_section(
            self.delivery,
            "Relay the Context Promotion confirmation",
        )
        self.assertContainsAll(
            invocation,
            (
                "Before any `delivery` mutation",
                "all paginated source Issue comments",
                "`comments_complete: true`",
                "first-read-closed standalone/legacy compatibility no-op",
                "without Delivery-log backfill, an unlocked Issue, `add-comment`, or a pending user decision",
                "`locked: false`",
                "authenticated Issue `add-comment` capability",
                "human-only acceptance item",
                "persistent confirmation URL/whole-comment digest",
                "Do not require a planning-only or same-turn input tool before Implementation",
                "require the Phase Owner to persist it",
                "independently re-read it in the coordinator",
                "summarize its exact changes and evidence in the final response",
                "wait for a new explicit confirmation re-entry",
                "user_decision:",
                "proposal_sha256: SHA256",
                "decision: approved | revise | pause",
                "sole active `awaiting-confirmation` tip",
                "supplied without one matching active tip",
                "return blocked before mutation and never retain it for a later proposal",
                "A bare reply, prior chat, or copied decision without a current exact role",
                "Context Promotion proposal remains `delivery`'s only live user interaction",
            ),
            source="root split-turn confirmation contract",
        )
        self.assertContainsAll(
            delivery_input,
            (
                "Before the first mutation",
                "complete source Issue and every paginated top-level comment",
                "`comments_complete: true`",
                "first-read-closed standalone/legacy compatibility no-op",
                "does not require an unlocked Issue, `add-comment`, or a pending user decision",
                "remaining path that may mutate or backfill",
                "`locked: false`",
                "`add-comment` capability",
                "persistent explicit confirmation URL and whole-comment digest bound to the exact current acceptance snapshot",
                "If no product snapshot exists yet",
                "root Skill's exact `user_decision` block",
                "current explicit `role: delivery` invocation",
                "claimed bindings, not trusted state",
                "Reject a missing role, bare approval, ambiguous decision",
                "no sole active `awaiting-confirmation` tip matches it",
                "return blocked before mutation and never carry that response forward",
                "Do not require a planning-only or same-turn input tool",
                "code-capable mode",
                "only live user interaction inside a mutable `delivery` remains the Context Promotion confirmation gate",
            ),
            source="delivery split-turn input contract",
        )
        self.assertInOrder(
            relay,
            (
                "Present the user with all proposal details",
                "every candidate conclusion",
                "classification and exact authority-layer destination path",
                "exact proposed context change or category-specific no-write reason",
                "`explicit-user-decision`",
                "exact authority effect",
                "source evidence",
                "project-memory PR URL",
                "In the final response, provide a self-contained summary",
                "exact active proposal callback URL/whole-comment SHA-256",
                "ready-to-send explicit `role: delivery` re-entry packet",
                "`$project-harness` for Codex or `/project-harness` for Claude Code",
                "Approve exact proposal",
                "Pause without integration",
                "Revise exact proposal",
                "end the current turn immediately",
                "On a later current explicit `role: delivery` confirmation re-entry",
                "Immediately after syntactically recognizing the current exact role and `user_decision` packet",
                "Reconstruct the workflow from persistent evidence",
                "On exact approval",
                "Summarize the new revision and end the turn again",
            ),
            source="Context Promotion confirmation relay",
        )
        self.assertContainsAll(
            relay,
            (
                "Do not set an automatic resolution or default",
                "eligibility registration URL/digest",
                "every artifact evidence/current-authority source",
                "`outcome: blocked`",
                "`recovery_condition: awaiting-context-promotion-decision`",
                "Do not call a same-turn input tool",
                "write a `confirmed` callback",
                "Silence and timeout leave the persisted `awaiting-confirmation` tip unchanged",
                "proposal URL/digest to equal the sole active `awaiting-confirmation` whole comment",
                "Any source identity, proposal content, classification, destination",
                "Never span a monotonic timer across turns",
                "`approved` → the `context-confirmed` boundary's `decision: approved`",
                "`revise` → attempt `response_kind: revision-requested`",
                "`pause` → attempt `response_kind: paused`",
                "If that proposal binding cannot be established, return blocked before any mutation and write no observation",
                "without starting an overlapping dispatch timer",
                "attach it only to `context-confirmed`",
                "before any revision phase dispatch",
                "standard non-overlapping phase-dispatch timer",
                "On exact modification items",
                "new `awaiting-confirmation` callback",
                "On pause",
                "This split-turn exchange is the only interactive gate in `delivery`",
            ),
            source="Context Promotion confirmation behavior",
        )

        confirmation = markdown_section(
            self.promotion,
            "Persist and relay the confirmation gate",
        )
        self.assertContainsAll(
            confirmation,
            (
                "final, self-contained summary",
                "ready-to-send explicit `role: context-promotion` re-entry packet",
                "`$project-harness` for Codex or `/project-harness` for Claude Code",
                "end the proposal-producing turn with `awaiting-confirmation`",
                "Do not call a same-turn input tool",
                "write `confirmed`",
                "Bind approval only to the displayed proposal comment URL/digest",
                "Silence or timeout leaves the active proposal unchanged",
                "On a later exact confirmation re-entry",
                "sole active `awaiting-confirmation` whole comment",
                "For `decision: revise`, do not write `confirmed`",
                "For `decision: pause`, make no phase mutation",
            ),
            source="Context Promotion phase confirmation",
        )
        self.assertIn("Closeout must not open the user decision gate", self.delivery)
        self.assertIn("Never open the user decision gate in Closeout", self.closeout)
        self.assertIn(
            "Do not open a user decision gate during Implementation or Closeout",
            self.skill,
        )
        for source, text in (
            ("SKILL.md", self.skill),
            ("delivery.md", self.delivery),
            ("context-promotion.md", self.promotion),
            ("closeout.md", self.closeout),
            ("agents/openai.yaml", self.openai),
        ):
            with self.subTest(source=source):
                self.assertNotIn("request_user_input", text)

    def test_confirmation_reentry_is_current_source_bound_and_fail_closed(self) -> None:
        delegation = markdown_section(self.skill, "Delegate without expanding authority")
        relay = markdown_section(
            self.delivery,
            "Relay the Context Promotion confirmation",
        )
        evidence_confirmation = self.evidence

        self.assertContainsAll(
            delegation,
            (
                "current explicit proposal-bound confirmation re-entry",
                "independently verifying its URL/digest",
                "sole active `awaiting-confirmation` tip",
                "request for a new proposal, not as direct patch authority",
                "host parent-child provenance from the current live `delivery` invocation",
                "serialized envelope, callback, branch, prior run, or hand-off cannot create authority",
            ),
            source="confirmation delegation authority",
        )
        self.assertContainsAll(
            evidence_confirmation,
            (
                "current user's explicit proposal-bound confirmation re-entry",
                "current exact `role: delivery` invocation",
                "current exact `role: context-promotion` invocation",
                "sole active `awaiting-confirmation` whole comment",
                "require its URL/digest to equal that decision",
                "stored or relayed packet",
                "bare reply",
                "prior invocation",
                "silence, timeout, or general delivery intent cannot authorize it",
            ),
            source="persistent confirmation authority",
        )
        self.assertContainsAll(
            relay,
            (
                "Re-read the source, eligibility registration, authority base",
                "every artifact evidence/current-authority source",
                "Reviewer PASS, state callback, and any memory PR tuple",
                "Any source identity, proposal content, classification, destination",
                "PR Body/head/base tuple, validation, or Reviewer drift invalidates the response",
                "return blocked without confirmation or downstream workflow mutation",
                "new artifact, review, callback, summary, and later decision",
                "If no active tip exists or the proposal URL/digest is missing, mismatched, or unreadable",
                "without any observation or other mutation",
                "Do not treat free text as a hidden code or policy patch",
            ),
            source="confirmation drift handling",
        )

    def test_standalone_context_promotion_waits_and_resumes_explicitly(self) -> None:
        confirmation = markdown_section(
            self.promotion,
            "Persist and relay the confirmation gate",
        )
        result = markdown_section(
            self.promotion,
            "Return a persistent phase result",
        )

        self.assertContainsAll(
            confirmation,
            (
                "When standalone, present the same complete details in the final response",
                "proposal callback URL/whole-comment SHA-256",
                "Reviewer PASS identity",
                "complete memory-PR tuple",
                "explicit `role: context-promotion` re-entry packet",
                "end the proposal-producing turn with `awaiting-confirmation`",
                "For `decision: pause`, make no phase mutation and return the existing `awaiting-confirmation` identities",
                "Return blocked without a confirmation mutation for a malformed decision, stale proposal identity, or source drift",
            ),
            source="standalone confirmation boundary",
        )
        self.assertContainsAll(
            result,
            (
                "outcome: awaiting-confirmation | verified-memory-pr",
                "coordinator_action: request-confirmation | merge-memory-pr | close-issue | null",
                "For standalone `awaiting-confirmation`",
                "`coordinator_action: null`",
                "leave `issue_closure: null`",
                "hand off to the user",
                "explicit `role: context-promotion` re-entry packet",
            ),
            source="standalone awaiting-confirmation result",
        )

    def test_cross_turn_confirmation_logging_is_honest(self) -> None:
        relay = markdown_section(
            self.delivery,
            "Relay the Context Promotion confirmation",
        )
        timing = markdown_section(self.delivery_log, "Measure time honestly")
        privacy = markdown_section(
            self.delivery_log,
            "Protect user and environment data",
        )

        self.assertContainsAll(
            relay,
            (
                "append and verify one `context-proposal-reviewed` boundary observation",
                "Silence and timeout leave the persisted `awaiting-confirmation` tip unchanged and create no user-response observation",
                "Set `user_wait_ms: null` for this cross-turn flow",
                "measure only the current re-entry's processing span",
                "never persist raw input or its digest",
            ),
            source="delivery cross-turn logging",
        )
        self.assertContainsAll(
            timing,
            (
                "Preserve non-null `user_wait_ms` only when reading a valid historical observation",
                "current split-turn confirmation flow must write `user_wait_ms: null`",
                "start its monotonic span immediately after syntactically recognizing the current exact role and `user_decision` packet",
                "before reconstructing or re-reading its bound state",
                "never the interval between turns",
            ),
            source="cross-turn timing compatibility",
        )
        self.assertContainsAll(
            privacy,
            (
                "raw confirmation replies or their digests",
                "map a proposal-bound top-level decision exactly",
                "`approved` → the `context-confirmed` boundary's `decision: approved`",
                "`revise` → attempt `response_kind: revision-requested`",
                "`pause` → attempt `response_kind: paused`",
                "Use attempt `response_kind: blocked` only after the displayed proposal URL/digest has independently matched the sole active tip",
                "return blocked without writing an observation or making any other mutation",
                "modification item count",
                "keep both result fields null",
                "A later reviewed proposal has its own `context-proposal-reviewed` boundary",
                "must never be back-linked as the earlier response attempt's result",
                "current-invocation revision/pause/blocked attempt observation is best-effort",
                "do not reconstruct it",
            ),
            source="cross-turn confirmation privacy",
        )

        persistence = markdown_section(
            self.delivery,
            "Persist Delivery stage observations",
        )
        self.assertContainsAll(
            self.delivery_log,
            (
                "require `validate_new_observation` to return no errors before every new observation write",
                "Use the backward-compatible `validate_observation` only when reading existing or historical records",
                "calculating a transition key does not replace the new-write validator",
                "Every new confirmation-response attempt must use `target_boundary: context-confirmed`",
                "use only `revision-requested`, `paused`, or `blocked` with `response_kind == result_kind == outcome`",
                "require `result_url: null` and `result_sha256: null`",
                "A new attempt may not use `result_kind` / `outcome: approved`",
                "may not omit its matching response kind and count",
                "Set all three change-quality domains to `not-applicable`",
                "keep every change list empty",
                "successful `approved` decision is represented only by the `context-confirmed` boundary",
                "exactly one `source_bindings` item with `kind: proposal-callback`",
                "independently matched active `awaiting-confirmation` whole comment",
            ),
            source="delivery log producer/reader validation split",
        )
        self.assertContainsAll(
            persistence,
            (
                "calculate `transition_key`",
                "require `validate_new_observation` to return no errors before every new write",
                "Use `validate_observation` only to dual-read existing/historical records",
            ),
            source="coordinator observation writer",
        )

    def test_confirmation_state_chain_and_legacy_dual_read_are_explicit(self) -> None:
        markers = markdown_section(self.skill, "Preserve persistent markers")
        marker_rows = re.findall(
            r"(?m)^\| `\$\{marker_namespace\}:([^`]+)` \|", markers
        )
        self.assertEqual(
            marker_rows,
            [
                "context-authoring",
                "context-promotion-eligible",
                "context-promotion",
            ],
        )
        self.assertContainsAll(
            markers,
            (
                "`references/delivery-evidence-contract.md`",
                "only to validate independently re-read evidence",
                "one active source-tuple-bound lineage",
                "strict dual-read and additive migration paths",
                "malformed current-schema artifacts are never legacy",
                "does not redefine the contract's outcome enums, predecessor fields, or active-tip algorithm",
            ),
            source="root marker and dual-read contract",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "outcome: awaiting-confirmation",
                "outcome: confirmed",
                "outcome: no-promotion",
                "outcome: memory-pr-ready",
                "outcome: memory-pr-merged",
                "preceding whole comment",
                "completed compatibility no-op",
                "later current explicit source-bound confirmation re-entry before any new merge or close",
            ),
            source="shared marker and dual-read contract",
        )

        state_chain = markdown_section(
            self.promotion,
            "Verify the source and promotion state chain",
        )
        self.assertContainsAll(
            state_chain,
            (
                "`references/delivery-evidence-contract.md`",
                "Validate the current source against that shared contract",
                "Apply only the normal, repair, and legacy migration chains",
                "older confirmation or Ready branch explicitly invalidated",
                "cannot authorize merge or closure",
                "fresh Closeout round",
                "malformed schema-v2 callback is never legacy",
            ),
            source="Context Promotion shared evidence use",
        )
        promotion_lineage = markdown_section(
            self.evidence,
            "Validate active lineages",
        )
        legacy = markdown_section(
            self.evidence,
            "Dual-read legacy promotion callbacks",
        )
        self.assertContainsAll(
            promotion_lineage,
            (
                "`awaiting-confirmation` → `confirmed` → `no-promotion`",
                "`awaiting-confirmation` → `confirmed` → `memory-pr-ready` → `memory-pr-merged`",
                "recoverable nonterminal states",
                "Only `no-promotion` and `memory-pr-merged` are current-format terminal states",
            ),
            source="shared promotion lineage",
        )
        self.assertContainsAll(
            legacy,
            (
                "Dual-read an unversioned legacy",
                "`no-promotion`, `memory-pr-ready`, or `memory-pr-merged`",
                "malformed schema v2, never as legacy",
                "legacy terminal with an already closed Issue is a completed compatibility no-op",
                "unmerged legacy `memory-pr-ready`",
                "`migration: confirmed-legacy-ready`",
            ),
            source="shared legacy dual-read",
        )

    def test_phase_results_are_snapshot_bound_and_coordinator_addressed(self) -> None:
        implementation_result = markdown_section(
            self.implementation,
            "Return a persistent phase result",
        )
        closeout_result = markdown_section(self.closeout, "Return a closed result")
        promotion_result = markdown_section(
            self.promotion,
            "Return a persistent phase result",
        )

        self.assertContainsAll(
            implementation_result,
            (
                "issue_body_sha256:",
                "head_sha:",
                "pr_url:",
                "pr_body_sha256:",
                "base_ref:",
                "base_sha:",
                "recipient: delivery-coordinator | user",
                "evidence_urls: []",
                "For delegated verified-draft-pr",
                "The coordinator must re-read them",
            ),
            source="Implementation result",
        )
        self.assertContainsAll(
            closeout_result,
            (
                "issue_body_sha256:",
                "pr_body_sha256:",
                "head_sha:",
                "base_ref:",
                "base_sha:",
                "acceptance_comment_url:",
                "issue_callback_url:",
                "promotion_registration_url:",
                "recipient: delivery-coordinator | user",
                "For delegated accepted-ready-pr",
                "The coordinator must re-read all of them",
            ),
            source="Closeout result",
        )
        self.assertContainsAll(
            promotion_result,
            (
                "source_pr_body_sha256:",
                "source_head_sha:",
                "source_merge_commit_sha:",
                "eligibility_registration_sha256:",
                "authority_base_sha:",
                "proposal_comment_url:",
                "proposal_comment_sha256:",
                "confirmation_comment_url:",
                "confirmation_comment_sha256:",
                "source_callback_url:",
                "memory_pr_body_sha256:",
                "memory_merge_commit_sha:",
                "issue_closure: null | pending-memory-pr-merge | closed",
                "issue_state_reason: null | completed",
                "recipient: delivery-coordinator | user",
                "only the coordinator may close",
            ),
            source="Context Promotion result",
        )

    def test_closeout_and_merge_prerequisites_are_fail_closed(self) -> None:
        verification = markdown_section(self.closeout, "Verify independently")
        success = markdown_section(self.closeout, "Complete successful acceptance")
        closeout_evidence = markdown_section(
            self.evidence,
            "Persist Closeout evidence",
        )
        recovery = markdown_section(self.delivery, "Reconstruct the persistent state")

        self.assertContainsAll(
            verification,
            (
                "Require `required_checks_known: true`",
                "cannot substitute for this machine-verifiable merge prerequisite",
                "remain BLOCKED while the transport reports false",
                "Never open the user decision gate in Closeout",
            ),
            source="Closeout required-check gate",
        )
        self.assertContainsAll(
            success,
            (
                "verified PASS comment whose payload has `required_checks_known: true`",
                "exact **Product acceptance Issue callback**",
                "exact **Current eligibility registration**",
                "bind its URL and digest",
                "complete the remaining steps idempotently",
            ),
            source="Closeout success evidence",
        )
        self.assertContainsAll(
            closeout_evidence,
            (
                "verdict: PASS | FAIL | BLOCKED",
                "pr_title: TITLE",
                "head_sha: COMMIT",
                "callback: product-acceptance-pass",
                "acceptance_comment_sha256: SHA256",
                "schema_version: 2",
                "issue_callback_sha256: SHA256",
            ),
            source="shared Closeout evidence schemas",
        )
        self.assertContainsAll(
            recovery,
            (
                "required-check knowledge or mergeability is unknown",
                "required checks fail because of the product change",
                "mergeability is false because of a repairable promotion-scope conflict",
                "return to a new cross-turn confirmation summary",
                "Exact unmerged legacy `memory-pr-ready`",
            ),
            source="delivery fail-closed recovery",
        )

    def test_promotion_evidence_and_repair_revisions_require_reconfirmation(self) -> None:
        lineage = markdown_section(self.evidence, "Validate active lineages")
        repair = markdown_section(
            self.promotion,
            "Apply modification requests and promotion-scope repairs",
        )
        confirmation = markdown_section(
            self.promotion,
            "Persist and relay the confirmation gate",
        )
        ready = markdown_section(
            self.promotion,
            "Mark a confirmed project-memory PR Ready",
        )

        self.assertContainsAll(
            self.evidence,
            (
                "revision_reason: initial | user-modification | promotion-scope-repair",
                "A repair from a confirmed tip populates `invalidates_confirmation_*`",
                "also populates `invalidates_ready_*`",
                "`migration: confirmed-legacy-ready`",
            ),
            source="shared promotion revision evidence",
        )
        self.assertContainsAll(
            lineage,
            (
                "promotion-scope repair from an active `confirmed` or `memory-pr-ready` tip",
                "invalidated older branch cannot authorize merge or closure",
                "sole reachable, non-superseded end",
            ),
            source="shared promotion active lineage",
        )
        self.assertContainsAll(
            repair,
            (
                "repairable required-check, title/Body/head/base-tuple, advanced-base, or mergeability defect",
                "repairable authority/current-source drift",
                "convert-to-draft",
                "confirmed no-write authority/source repair has no PR to convert",
                "new artifact, review, state digest, and approval",
                "Never loop a check failure",
            ),
            source="promotion repair loop",
        )
        self.assertContainsAll(
            confirmation,
            (
                "exact **Awaiting-confirmation callback**",
                "exact **Confirmed callback**",
                "every evidence/current-authority source",
                "compare their recorded digests",
                "eligibility registration, authority base",
            ),
            source="promotion confirmation evidence",
        )
        self.assertContainsAll(
            ready,
            (
                "exact **Memory-PR-ready callback**",
                "`migration: confirmed-legacy-ready` variant",
                "only for the unchanged Ready tuple",
            ),
            source="legacy Ready migration",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "eligibility_registration_sha256: SHA256",
                "migration: confirmed-legacy-ready",
                "legacy_evidence_sha256: LEGACY_CALLBACK_SHA256",
            ),
            source="shared legacy Ready schema",
        )

        url_fields = re.findall(
            r"(?m)^eligibility_registration_url:.*$",
            self.evidence,
        )
        digest_fields = re.findall(
            r"(?m)^eligibility_registration_sha256:.*$",
            self.evidence,
        )
        self.assertEqual(len(url_fields), len(digest_fields))
        self.assertGreaterEqual(len(url_fields), 8)

    def test_legacy_eligibility_fixture_has_a_safe_additive_migration(self) -> None:
        markers = markdown_section(self.skill, "Preserve persistent markers")
        match = re.search(
            r"pre-schema-v2 Closeout producer persisted this exact legacy "
            r"eligibility semantic minimum:\n\n~~~text\n(.*?)\n~~~",
            self.evidence,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        assert match is not None
        legacy_fixture = match.group(1).splitlines()
        self.assertEqual(
            legacy_fixture,
            [
                "<!-- ${marker_namespace}:context-promotion-eligible source-pr=456 source-head=COMMIT -->",
                "state: awaiting-merge",
                "issue_url: URL",
                "issue_body_sha256: SHA256",
                "pr_body_sha256: SHA256",
                "base_ref: develop",
                "base_sha: COMMIT",
                "acceptance_comment_url: URL",
            ],
        )
        self.assertNotIn("schema_version:", legacy_fixture)
        self.assertNotIn("acceptance_comment_sha256:", legacy_fixture)
        self.assertNotIn("issue_callback_url:", legacy_fixture)

        legacy = markdown_section(
            self.evidence,
            "Dual-read legacy promotion callbacks",
        )
        closeout_success = markdown_section(
            self.closeout,
            "Complete successful acceptance",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "Do not require the old payload to contain source title",
                "An unmerged product PR must pass a fresh Closeout",
                "already merged historical product PR",
            ),
            source="root legacy eligibility migration",
        )
        self.assertContainsAll(
            legacy,
            (
                "compute and bind both whole-comment digests during the current read",
                "reconstruct the complete five-category assessment",
            ),
            source="legacy callback dual-read",
        )
        self.assertIn(
            "historical field that its producer did not promise",
            self.evidence,
        )
        self.assertContainsAll(
            closeout_success,
            (
                "complete fresh Closeout",
                "active schema-v2 registration is stale while the source head is unchanged",
                "non-superseded tip as active",
                "one-to-one pair",
            ),
            source="Closeout legacy eligibility successor",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "schema_version: 2",
                "previous_registration_url:",
                "previous_registration_sha256:",
                "supersedes_legacy_registration_url:",
                "supersedes_legacy_registration_sha256:",
            ),
            source="shared eligibility successor schema",
        )

    def test_persisted_merge_tuples_and_changed_files_are_complete(self) -> None:
        implementation_result = markdown_section(
            self.implementation,
            "Return a persistent phase result",
        )
        closeout_success = markdown_section(
            self.closeout,
            "Complete successful acceptance",
        )
        closeout_result = markdown_section(self.closeout, "Return a closed result")
        proposal = markdown_section(
            self.promotion,
            "Persist the exact proposal artifact",
        )
        review = markdown_section(self.promotion, "Require independent review")
        ready = markdown_section(
            self.promotion,
            "Mark a confirmed project-memory PR Ready",
        )
        delivery_result = markdown_section(self.delivery, "Return the delivery result")

        self.assertContainsAll(
            implementation_result,
            ("head_ref:", "require `branch == head_ref`"),
            source="Implementation head tuple",
        )
        self.assertContainsAll(
            closeout_success,
            (
                "exact **Product acceptance Issue callback**",
                "exact **Current eligibility registration**",
                "bind its URL and digest",
            ),
            source="Closeout complete tuple",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "pr_title: TITLE",
                "head_ref: BRANCH",
                "head_sha: COMMIT",
                "schema_version: 2",
            ),
            source="shared Closeout complete tuple",
        )
        self.assertContainsAll(
            closeout_result,
            (
                "eligibility_registration_url:",
                "promotion_registration_url:",
                "retained deprecated aliases",
            ),
            source="Closeout compatibility alias",
        )
        self.assertContainsAll(
            proposal,
            (
                "exact **Proposal artifact**",
                "shared cross-field rules",
                "updates both base fields to the same new `develop` SHA",
            ),
            source="promotion artifact tuple",
        )
        self.assertContainsAll(
            review,
            (
                "exact **Reviewer PASS for a write**",
                "exact sorted artifact/transport view",
            ),
            source="write Reviewer PASS schema",
        )
        self.assertContainsAll(
            ready,
            (
                "exact **Memory-PR-ready callback**",
                "exact sorted artifact/Reviewer identities",
            ),
            source="memory Ready evidence",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "source_head_ref: BRANCH",
                "memory_pr_title: TITLE",
                "memory_head_ref: BRANCH",
                "memory_head_ref: BRANCH | null",
                "changed_files:",
                "status: added | modified | removed | renamed",
                "blob_sha: SHA | null",
                "`authority_base_sha == memory_base_sha`",
                "review_kind: context-promotion-write",
            ),
            source="shared promotion tuple schemas",
        )
        self.assertContainsAll(
            delivery_result,
            (
                "product_head_ref:",
                "memory_head_ref:",
                "issue_state_reason: null | completed",
                "proposal_comment_*` becomes `promotion_proposal_*",
                "source_callback_*` becomes `promotion_terminal_*",
            ),
            source="delivery result field mapping",
        )

    def test_promotion_author_identity_active_tip_and_supersession_are_explicit(self) -> None:
        lineage = markdown_section(self.evidence, "Validate active lineages")
        repair = markdown_section(
            self.promotion,
            "Apply modification requests and promotion-scope repairs",
        )
        result = markdown_section(
            self.promotion,
            "Return a persistent phase result",
        )
        self.assertContainsAll(
            self.evidence,
            (
                "Establish its `mutation_author_login` as the trusted workflow author",
                "transport-returned author login",
                "current user's explicit proposal-bound confirmation re-entry",
                "host-provenance-bound `user_decision`",
                "Define the active tip as the sole reachable, non-superseded end",
                "multiple active or unsuperseded confirmed revisions",
            ),
            source="promotion trusted active chain",
        )
        self.assertIn("sole reachable, non-superseded end", lineage)
        self.assertContainsAll(
            repair,
            (
                "changes a write proposal to all-`no_write`",
                "state: superseded-by-context-promotion",
                "non-active and must never be merged or reused",
                "create a new branch/Draft memory PR",
                "Allow the closure gate to ignore only an exact open Draft memory PR",
            ),
            source="write-to-no-write supersession",
        )
        self.assertContainsAll(
            result,
            (
                "return-to-definition",
                "role: delivery | external-review | context-promotion | definition",
                "exact requested product-contract change",
            ),
            source="typed promotion return",
        )

    def test_transport_exposes_guard_inputs_and_verified_merge_provenance(self) -> None:
        merge_guard = markdown_section(self.pr_transport, "Guard an exact merge")
        check_evidence = markdown_section(
            self.pr_transport,
            "Report check evidence conservatively",
        )
        envelope = markdown_section(
            self.pr_transport,
            "Return the shared result envelope",
        )
        self.assertContainsAll(
            merge_guard,
            (
                "`merge_kind: product` or `merge_kind: memory`",
                "do not accept caller-defined evidence names",
                "actual merge method as exactly `merge`, `squash`, or `rebase`",
                "Produce `merge_provenance` only from an authoritative merge event",
                "A caller-supplied or copied expected base is not provenance",
            ),
            source="deterministic merge inputs",
        )
        self.assertContainsAll(
            check_evidence,
            (
                "Normalize the applicable required subset separately as `required_checks`",
                "`success`, `failure`, `pending`, `missing`, or `unavailable`",
                "`required_checks_known: true`",
            ),
            source="required-check mapping",
        )
        self.assertContainsAll(
            envelope,
            (
                "merge_provenance:",
                "guarded_base_sha:",
                "guarded_head_sha:",
                "available_merge_methods: []",
                "merge_methods_known: null",
                "required_checks:",
            ),
            source="transport guard snapshot",
        )
        for name, transport in (
            ("Issue transport", self.issue_transport),
            ("Pull Request transport", self.pr_transport),
        ):
            self.assertContainsAll(
                transport,
                (
                    "authenticated_actor:",
                    "login: null",
                    "id: null",
                    "mutation_author_login: null",
                    "verified: false",
                    "Independently resolve the selected transport's authenticated actor login/ID",
                ),
                source=f"{name} authenticated identity",
            )

    def test_completed_delivery_closes_and_independently_verifies_the_issue(self) -> None:
        closure = markdown_section(self.delivery, "Close the source Issue")
        result = markdown_section(self.delivery, "Return the delivery result")

        self.assertContainsAll(
            closure,
            (
                "Closeout-accepted product head is merged into `develop`",
                "one exact non-invalidated schema-v2 `confirmed` callback",
                "ends in either verified `no-promotion`",
                "`memory-pr-merged` callback",
                "sole active schema-v2 tip is the exact `legacy-reconciliation` confirmation",
                "legacy callback supplies terminal outcome evidence without creating a duplicate terminal",
                "explicit `change-metadata` mutation",
                "setting `state: closed` and `state_reason: completed`",
                "Independently read the Issue back",
                "Accept only `verified` or `no-op`",
                "`state: closed`",
                "`read_back_verified: true`",
                "Do not use a closing keyword",
            ),
            source="delivery Issue closure gate",
        )
        closure_judgment = markdown_section(
            self.promotion,
            "Judge source Issue closure",
        )
        self.assertContainsAll(
            closure_judgment,
            (
                "schema-v2 `confirmed` callback with `proposal_kind: legacy-reconciliation`",
                "legacy callback supplies terminal outcome evidence",
                "active schema-v2 confirmation supplies current closure authority",
                "do not require or create a duplicate terminal",
            ),
            source="legacy terminal closure exception",
        )
        self.assertContainsAll(
            result,
            (
                "outcome: completed | return-to-definition | blocked",
                "product_merge_commit_sha:",
                "promotion_proposal_sha256:",
                "promotion_confirmation_sha256:",
                "promotion_terminal_outcome:",
                "memory_merge_commit_sha:",
                "issue_closure: open | closed",
                "issue_state_verified: false",
                "Return `completed` only with `issue_closure: closed`, `issue_state_verified: true`",
            ),
            source="delivery terminal result",
        )
        self.assertContainsAll(
            self.issue_transport,
            (
                "current `delivery` coordinator",
                "current explicit standalone `role: context-promotion`",
                "Never accept final closure from a Phase Owner delegated by `delivery`, a Worker, a Reviewer, or any other descendant",
                "| Change metadata |",
                "explicit state/state reason",
                "perform a separate fetch",
                "read_back_verified: true | false | null",
            ),
            source="Issue close transport",
        )

    def test_legacy_no_promotion_cannot_hide_a_new_write(self) -> None:
        legacy = markdown_section(
            self.evidence,
            "Dual-read legacy promotion callbacks",
        )
        no_promotion = markdown_section(
            self.promotion,
            "Complete confirmed no-promotion",
        )
        closure = markdown_section(
            self.promotion,
            "Judge source Issue closure",
        )

        self.assertContainsAll(
            legacy,
            (
                "closure-only legacy `no-promotion` or `memory-pr-merged`",
                "preserves the exact terminal outcome",
                "if reassessment of legacy `no-promotion` finds a write",
                "normal Ready → coordinator merge → current `memory-pr-merged` path",
                "`proposal_kind: write`",
                "`revision_reason: legacy-reassessment`",
                "both predecessor/evidence pairs",
                "complete five-category assessment",
            ),
            source="legacy no-promotion migration",
        )
        self.assertContainsAll(
            no_promotion,
            (
                "keeps every durable category `no_write`",
                "all memory-PR fields null",
                "old terminal as superseded evidence",
                "require a new `memory-pr-merged` terminal before closure",
            ),
            source="legacy no-promotion completion",
        )
        self.assertIn(
            "schema-v2 write branch that binds and supersedes legacy no-promotion is closable only from its own active `memory-pr-merged` terminal",
            closure,
        )
        self.assertIn(
            "exact predecessor legacy callback as superseded audit evidence, not as a conflicting active terminal",
            closure,
        )
        delivery_closure = markdown_section(self.delivery, "Close the source Issue")
        self.assertIn(
            "exact legacy `no-promotion` predecessor bound and superseded by the active schema-v2 write branch is audit evidence rather than a conflict",
            delivery_closure,
        )

    def test_confirmed_is_persisted_recovery_not_a_success_result(self) -> None:
        confirmation = markdown_section(
            self.promotion,
            "Persist and relay the confirmation gate",
        )
        result = markdown_section(
            self.promotion,
            "Return a persistent phase result",
        )
        relay = markdown_section(
            self.delivery,
            "Relay the Context Promotion confirmation",
        )

        self.assertContainsAll(
            confirmation,
            (
                "exact **Confirmed callback**",
                "Do not return `confirmed` as a successful phase result",
                "continue an unchanged normal all-`no_write` proposal to schema-v2 `no-promotion`",
                "write that supersedes legacy `no-promotion`",
                "return that existing terminal plus the new confirmation as terminal evidence",
                "continue to the applicable migrated schema-v2 `memory-pr-ready` or `memory-pr-merged`",
                "fresh Context Promotion reconciler resumes from it without requesting approval again",
            ),
            source="confirmed continuation",
        )
        self.assertIn(
            "proposal_kind: write | no-write | legacy-reconciliation",
            self.evidence,
        )
        outcome_line = re.search(r"(?m)^outcome: .+$", result)
        self.assertIsNotNone(outcome_line)
        assert outcome_line is not None
        self.assertNotIn("confirmed", outcome_line.group(0))
        self.assertContainsAll(
            relay,
            (
                "Require that Owner to persist and return the `confirmed` callback",
                "the Coordinator only re-reads and validates them",
                "Continue in the same confirmation-continuation invocation",
                "`confirmed` alone is a recoverable interrupted state, not a successful phase result",
            ),
            source="coordinator confirmed handling",
        )

    def test_already_merged_recovery_uses_exact_guard_or_explicit_legacy_exception(
        self,
    ) -> None:
        recovery = markdown_section(self.delivery, "Reconstruct the persistent state")
        product = markdown_section(self.delivery, "Merge the accepted product PR")
        memory = markdown_section(self.delivery, "Merge approved project memory")

        self.assertContainsAll(
            recovery,
            (
                "product merge gate's already-merged `no-op` recovery",
                "project-memory merge gate's already-merged `no-op` recovery",
                "complete current gate evidence, method, provenance, checks, and tuple",
                "explicit read-only legacy integration exception",
            ),
            source="already-merged recovery routing",
        )
        self.assertContainsAll(
            product,
            (
                "Use this same operation for current-format already-merged recovery",
                "accept only its exact `no-op`",
                "historical legacy integration row is a read-only compatibility exception",
                "must not be reported as a current-format transport `no-op`",
            ),
            source="product already-merged guard",
        )
        self.assertContainsAll(
            memory,
            (
                "Use this same operation for current-format already-merged recovery",
                "accept only its exact `no-op`",
                "every required check successful",
                "verified merge provenance",
            ),
            source="memory already-merged guard",
        )

    def test_standalone_context_reconciliation_uses_the_same_merged_checks(
        self,
    ) -> None:
        source = markdown_section(
            self.promotion,
            "Verify the source and promotion state chain",
        )
        memory = markdown_section(
            self.promotion,
            "Reconcile a merged project-memory PR",
        )

        for name, section in (
            ("merged product source admission", source),
            ("merged memory reconciliation", memory),
        ):
            self.assertContainsAll(
                section,
                (
                    "required_checks_known: true",
                    "every required check currently successful",
                    "actual merge method equal to the bound Harness integration policy",
                    "sole authoritatively available method captured by schema-v1 compatibility preflight",
                    "transport-verified merge provenance",
                    "Do not require post-merge mergeability",
                ),
                source=name,
            )
        self.assertIn("whether delegated or standalone", source)
        self.assertIn(
            "Apply these checks equally under delegated and standalone entry",
            memory,
        )
        policy = markdown_section(self.skill, "Bind repository policy and mutations")
        self.assertContainsAll(
            policy,
            (
                "For a new merge mutation",
                "For exact already-merged schema-v2 recovery",
                "require the actual method to equal the configured method",
                "schema-v1 recovery retains its strict historical policy check",
                "mergeability/provenance",
                "never present manual merge as the normal recovery action",
            ),
            source="root mergeability scope",
        )


if __name__ == "__main__":
    unittest.main()
