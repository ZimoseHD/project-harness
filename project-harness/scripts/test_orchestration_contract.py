from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "project-harness"
REFERENCES = HARNESS / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class LeanOrchestrationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.governance = read(ROOT / "AGENTS.md")
        cls.skill = read(HARNESS / "SKILL.md")
        cls.delivery = read(REFERENCES / "delivery.md")
        cls.definition = read(REFERENCES / "definition.md")
        cls.context_authoring = read(REFERENCES / "context-authoring.md")
        cls.implementation = read(REFERENCES / "implementation.md")
        cls.closeout = read(REFERENCES / "closeout.md")
        cls.promotion = read(REFERENCES / "context-promotion.md")
        cls.evidence = read(REFERENCES / "delivery-evidence-contract.md")
        cls.logs = read(REFERENCES / "delivery-log-contract.md")
        cls.issue_contract = read(REFERENCES / "issue-contract.md")
        cls.product_contract = read(REFERENCES / "product-pr-contract.md")
        cls.issue_transport = read(REFERENCES / "issue-transport.md")
        cls.pr_transport = read(REFERENCES / "pull-request-transport.md")
        cls.openai = read(HARNESS / "agents" / "openai.yaml")

    def test_public_roles_and_host_invocation_stay_stable(self) -> None:
        for role in (
            "init",
            "definition",
            "context-authoring",
            "delivery",
            "implementation",
            "closeout",
            "context-promotion",
        ):
            self.assertRegex(self.skill, rf"`{re.escape(role)}`")
        self.assertIn("$project-harness", self.skill)
        self.assertIn("/project-harness", self.skill)
        self.assertIn("allow_implicit_invocation: false", self.openai)
        self.assertIn("Treat `external-review` as a stopping destination", self.skill)

    def test_config_and_marker_compatibility_remain_stable(self) -> None:
        for fragment in (
            "schema_version: 2",
            "marker_namespace: project-slug",
            "base_branch: develop",
            "product_pr:",
            "memory_pr:",
            "${marker_namespace}:context-authoring",
            "${marker_namespace}:context-promotion-eligible",
            "${marker_namespace}:context-promotion",
        ):
            self.assertIn(fragment, self.skill)
        self.assertIn("schema-v1", self.skill)
        self.assertIn("scripts/config_guard.py", self.skill)

    def test_new_delegation_is_compact_schema_v3(self) -> None:
        match = re.search(
            r"~~~yaml\ndelegation:\n(?P<body>.*?)\n~~~",
            self.skill,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        body = match.group("body")
        for field in (
            "schema_version: 3",
            "parent_role: delivery",
            "delegated_role:",
            "authoritative_sources:",
            "bound_snapshot:",
            "evidence_comments:",
            "persistent_evidence_urls:",
            "user_decision:",
            "allowed_mutations:",
            "next_action:",
        ):
            self.assertIn(field, body)
        for legacy_payload in (
            "evidence_bundle:",
            "evidence_component_identities:",
            "completeness_bindings:",
            "payload_identities:",
        ):
            self.assertNotIn(legacy_payload, body)
        self.assertIn("Emit only delegation schema-v3", self.skill)
        self.assertIn("Dual-read schema-v2 delegation only", self.skill)
        self.assertIn("Dual-read schema-v1", self.skill)

    def test_phase_delegation_consumers_accept_v3_and_legacy_read_only(self) -> None:
        for source in (self.implementation, self.closeout, self.promotion):
            self.assertIn("schema-v3", source)
            self.assertIn("schema-v2", source)
            self.assertIn("schema-v1", source)
        for source in (self.implementation, self.closeout):
            self.assertRegex(source, r"(?i)do not (?:construct, extend, or )?require an Evidence Bundle")

    def test_definition_is_zero_question_by_default(self) -> None:
        self.assertIn("For a clear and low-risk requirement, ask no clarification question", self.definition)
        self.assertIn("Do not run `/grilling` merely", self.definition)
        self.assertIn("does not require an independent Reviewer", self.definition)
        self.assertIn("Require an independent Reviewer when the contract is high-risk", self.definition)
        self.assertIn("deterministic completeness check", self.definition)

    def test_definition_publishes_one_compact_exception_only_change_scope(self) -> None:
        self.assertIn("### 改动范围", self.issue_contract)
        self.assertIn("- 普通业务改动：", self.issue_contract)
        self.assertIn("- 受保护改动：", self.issue_contract)
        self.assertIn("受保护改动：无", self.issue_contract)
        self.assertIn("This list is authoritative for every phase", self.issue_contract)
        for protected_surface in (
            "architecture or module boundaries",
            "public APIs",
            "DTOs or serialization",
            "databases or migrations",
            "message protocols",
            "configuration formats",
            "security or permissions",
            "core dependencies or frameworks",
        ):
            self.assertIn(protected_surface, self.issue_contract)
        self.assertNotRegex(self.issue_contract, r"\|\s*受保护表面\s*\|")
        self.assertIn("ask one decision at a time", self.definition)
        self.assertIn("unresolved decisions can change the delivery contract", self.definition)
        self.assertIn("Express each question in plain language", self.definition)
        self.assertIn("the recommended choice", self.definition)
        self.assertIn("do not bundle decisions", self.definition)
        self.assertIn("protected change within an explicit Issue exception", self.openai)

    def test_implementation_and_closeout_focus_on_current_head_code_evidence(self) -> None:
        self.assertIn("smallest verification set", self.implementation)
        self.assertIn("final head SHA", self.implementation)
        self.assertIn("Do not rerun a current-head check merely", self.closeout)
        self.assertIn("missing, stale, ambiguous", self.closeout)
        self.assertIn("required_checks_known: true", self.closeout)
        self.assertIn("Inspect the complete diff", self.closeout)

    def test_change_scope_guard_reuses_existing_phases_without_a_third_gate(self) -> None:
        self.assertIn("Before the first product-code or test mutation", self.implementation)
        self.assertIn("the complete final product diff", self.implementation)
        self.assertIn("return return-to-definition", self.implementation)
        self.assertIn("remove any unnecessary out-of-scope edit", self.implementation)
        self.assertIn("only when completion requires a broader contract", self.implementation)
        self.assertIn("compare it with the complete final product diff", self.closeout)
        self.assertIn("return to Implementation", self.closeout)
        self.assertIn("return to Definition", self.closeout)
        self.assertIn("Do not add a scope-specific acceptance item", self.closeout)
        self.assertIn("add no mapping table, empty field, or extra ceremony", self.product_contract)
        self.assertIn("cannot authorize, broaden, or retroactively justify", self.context_authoring)
        self.assertIn("open, unmerged legacy task", self.issue_contract)
        self.assertIn("exact already-merged lineage", self.implementation)
        self.assertIn("exact already-merged recovery lineage", self.closeout)
        self.assertIn("Delivery's sole scope-related routing check", self.delivery)
        self.assertIn("never classify a change, map files, or add acceptance evidence", self.delivery)
        self.assertIn("already-merged `no-op` recovery", self.delivery)
        self.assertNotIn("### 改动范围", self.evidence)
        self.assertNotIn("change-scope-conformance", self.skill + self.evidence)

    def test_code_only_admission_is_exact_and_persistent(self) -> None:
        for source in (self.skill, self.delivery, self.evidence, self.closeout):
            self.assertIn("durable-memory-impact", source)
            self.assertIn("all-five-none", source)
        self.assertIn("exactly `无`", self.skill)
        self.assertIn("exact literal `无`", self.product_contract)
        self.assertIn("exactly once", self.evidence)
        self.assertIn("no Context Promotion state", self.skill)
        self.assertRegex(
            self.evidence,
            r"(?:no related|no source-linked|or source-linked) project-memory PR",
        )
        self.assertIn("code_only_verified", self.closeout)
        self.assertIn("promotion_required", self.closeout)

    def test_code_only_path_skips_process_artifacts_and_closes_guardedly(self) -> None:
        self.assertRegex(self.delivery, r"For `code-only`, skip Context Promotion(?: entirely)?")
        for artifact in (
            "no-write proposal",
            "Reviewer PASS",
            "confirmation",
            "terminal callback",
            "Delivery log",
            "finalization comment",
            "post-close comment",
        ):
            self.assertIn(artifact, self.delivery)
        self.assertIn("change-metadata", self.delivery)
        self.assertIn("state_reason: completed", self.delivery)
        self.assertIn("Independently read the Issue back", self.delivery)

    def test_first_new_all_no_write_promotion_has_no_user_gate(self) -> None:
        self.assertRegex(
            self.promotion,
            r"(?s)first new (?:promotion|candidate) round.*?all.*?no_write.*?(?:direct|immediate).*?no-promotion",
        )
        self.assertRegex(
            self.promotion,
            r"(?s)(?:direct|Lean).*?no-promotion.*?(?:without|no).*?(?:proposal|Reviewer|confirmation)",
        )
        self.assertIn("direct-no-promotion-all-no-write", self.promotion)

    def test_direct_no_promotion_has_a_narrow_ephemeral_handoff_exception(self) -> None:
        self.assertIn("A phase result or hand-off is only a search hint", self.evidence)
        self.assertIn("The sole no-artifact exception", self.evidence)
        self.assertIn("reason: direct-no-promotion-all-no-write", self.evidence)
        self.assertIn("not mutation authority", self.evidence)
        self.assertIn("immediately before closure", self.evidence)
        self.assertIn("recovery must classify again", self.evidence)
        self.assertIn("that Context Promotion Owner revalidates", self.delivery)

    def test_actual_memory_write_keeps_strict_review_confirmation_and_merge(self) -> None:
        for source in (self.skill, self.delivery, self.promotion):
            self.assertIn("write proposal", source)
            self.assertIn("Reviewer", source)
            self.assertIn("source-bound", source)
        self.assertIn("awaiting-confirmation", self.delivery)
        self.assertIn("memory-pr-ready", self.delivery)
        self.assertIn("memory-pr-merged", self.delivery)
        self.assertIn("required_checks_known: true", self.delivery)
        self.assertIn("affirmative mergeability", self.delivery)

    def test_write_confirmation_remains_split_turn_and_source_bound(self) -> None:
        self.assertIn("sole active `awaiting-confirmation`", self.delivery)
        self.assertIn("End the turn", self.delivery)
        self.assertIn("On re-entry", self.delivery)
        self.assertIn("Do not call a same-turn input tool", self.promotion)
        self.assertIn("proposal_url", self.skill)
        self.assertIn("proposal_sha256", self.skill)
        self.assertIn("Reject a bare reply", self.skill)

    def test_persisted_write_lineage_and_legacy_migrations_stay_guarded(self) -> None:
        for fragment in (
            "artifact_kind: context-promotion-validation-impact",
            "review_schema_version: 1",
            "migration: confirmed-legacy-ready",
            "migration: confirmed-legacy-already-merged",
            "legacy-full",
            "active tip",
        ):
            self.assertIn(fragment, self.evidence)
        self.assertIn("required_checks_known: true", self.evidence)
        self.assertIn("transport-verified merge provenance", self.evidence)

    def test_product_and_memory_merge_evidence_sets_remain_protocol_owned(self) -> None:
        self.assertIn("merge_kind: product", self.pr_transport)
        self.assertIn("merge_kind: memory", self.pr_transport)
        for fragment in (
            "closeout-pass",
            "issue-callback",
            "eligibility-registration",
            "proposal-artifact",
            "confirmation",
            "reviewer-pass",
            "memory-pr-ready",
        ):
            self.assertIn(fragment, self.pr_transport)

    def test_existing_promotion_lineage_cannot_use_fast_path(self) -> None:
        for source in (self.skill, self.delivery, self.promotion):
            self.assertRegex(source, r"(?i)(?:never|must not|cannot).{0,140}(?:fast path|shortcut|code-only|Lean)")
            self.assertIn("awaiting-confirmation", source)
            self.assertIn("confirmed", source)
        self.assertIn("legacy", self.promotion)
        self.assertIn("active tip", self.evidence)

    def test_new_delivery_does_not_load_or_write_stage_logs(self) -> None:
        delivery_row = next(
            line for line in self.skill.splitlines() if line.startswith("| `delivery` |")
        )
        self.assertNotIn("Delivery stage log contract", delivery_row)
        self.assertIn("Do not load `references/delivery-log-contract.md`", self.skill)
        self.assertIn("Never write, backfill, repair, or require", self.delivery)
        self.assertIn("never require `stage_logs.coverage_level`", self.delivery)
        self.assertIn("Do not require Delivery-log coverage", self.delivery)
        self.assertIn("post-close", self.delivery)

    def test_legacy_log_schema_is_frozen_read_only(self) -> None:
        self.assertIn("record_kind: delivery-stage-observation", self.logs)
        self.assertIn("log_schema_version: 1", self.logs)
        self.assertRegex(self.logs, r"(?i)frozen|read-only")
        self.assertRegex(self.logs, r"(?i)(?:must not|do not).{0,100}(?:write|backfill)")
        self.assertRegex(self.logs, r"(?i)(?:never|must not|do not).{0,120}coverage.{0,80}(?:gate|block|require)")

    def test_transports_keep_atomic_and_irreversible_guards(self) -> None:
        for source in (self.issue_transport, self.pr_transport):
            self.assertIn("baseline", source)
            self.assertIn("immediately before", source)
            self.assertIn("separate fetch", source)
            self.assertIn("verified", source)
            self.assertIn("no-op", source)
            self.assertIn("indeterminate", source)
        for fragment in (
            "required_checks_known: true",
            "mergeable: true",
            "merge_method",
            "merge_provenance",
            "closeout-pass",
            "issue-callback",
            "eligibility-registration",
        ):
            self.assertIn(fragment, self.pr_transport)

    def test_issue_and_product_contract_headings_remain_exact(self) -> None:
        for heading in (
            "## 原始需求 / 问题背景",
            "## 目标",
            "## 非目标与边界",
            "## 持久项目记忆影响",
            "## 已确认决策",
            "## 实施计划",
            "## 验收与验证",
        ):
            self.assertIn(heading, self.issue_contract)
        for heading in (
            "## 关联任务",
            "## 实施基线",
            "## 结果",
            "## 主要改动",
            "## 验证证据",
            "## 持久项目记忆实际影响",
            "## 完成声明",
            "## Closeout",
        ):
            self.assertIn(heading, self.product_contract)

    def test_single_writer_and_merge_authority_remain_bounded(self) -> None:
        for source in (self.skill, self.delivery, self.implementation, self.closeout, self.promotion):
            self.assertRegex(source, r"(?i)(?:sole|only).{0,120}(?:writer|phase writer)")
        self.assertIn("Keep merge and final Issue closure exclusively", self.skill)
        self.assertRegex(self.skill, r"Workers? and Reviewers?")
        self.assertIn("forbid further delegation", self.skill)


if __name__ == "__main__":
    unittest.main()
