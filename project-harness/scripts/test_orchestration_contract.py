from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "project-harness"
REFERENCES = HARNESS / "references"
SCRIPTS = HARNESS / "scripts"

sys.path.insert(0, str(SCRIPTS))

import transport_guard  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class OrchestrationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.governance = read(ROOT / "AGENTS.md")
        cls.skill = read(HARNESS / "SKILL.md")
        cls.migration = read(HARNESS / "MIGRATION.md")
        cls.delivery = read(REFERENCES / "delivery.md")
        cls.spec = read(REFERENCES / "spec.md")
        cls.implementation = read(REFERENCES / "implementation.md")
        cls.review = read(REFERENCES / "review.md")
        cls.promotion = read(REFERENCES / "context-promotion.md")
        cls.express = read(REFERENCES / "express.md")
        cls.evidence = read(REFERENCES / "evidence-contract.md")
        cls.issue_contract = read(REFERENCES / "issue-contract.md")
        cls.product_contract = read(REFERENCES / "product-pr-contract.md")
        cls.issue_transport = read(REFERENCES / "issue-transport.md")
        cls.pr_transport = read(REFERENCES / "pull-request-transport.md")
        cls.openai = read(HARNESS / "agents" / "openai.yaml")
        cls.active_texts = (
            cls.skill,
            cls.delivery,
            cls.spec,
            cls.implementation,
            cls.review,
            cls.promotion,
            cls.express,
            cls.evidence,
            cls.issue_contract,
            cls.product_contract,
            cls.issue_transport,
            cls.pr_transport,
            cls.openai,
        )

    def test_public_roles_and_host_invocation_stay_stable(self) -> None:
        for role in (
            "init",
            "spec",
            "implementation",
            "review",
            "context-promotion",
            "delivery",
            "express",
        ):
            self.assertRegex(self.skill, rf"`{re.escape(role)}`")
        self.assertIn("$project-harness", self.skill)
        self.assertIn("/project-harness", self.skill)
        self.assertIn("allow_implicit_invocation: false", self.openai)

    def test_path_selection_requires_one_user_confirmation(self) -> None:
        self.assertIn("recommend path 1 or path 2 with a one-line rationale", self.skill)
        self.assertIn("one explicit user confirmation", self.skill)
        self.assertIn("Never infer a role", self.skill)

    def test_subagent_use_is_unconstrained(self) -> None:
        self.assertIn("no fixed topology", self.skill)
        self.assertIn("no mandatory Worker or Reviewer", self.skill)
        self.assertIn("Subagent 使用不受约束", self.governance)

    def test_removed_v1_machinery_is_absent_from_active_files(self) -> None:
        for token in (
            "Phase Owner",
            "Evidence Bundle",
            "delivery-stage-observation",
            "context-promotion-eligible",
            "eligibility-registration",
            "closeout-pass",
            "issue-callback",
            "schema-v3",
            "`definition`",
            "`closeout`",
            "`context-authoring`",
            "delivery-log",
            "validation_impact",
            "context_review_input",
            "evidence_bundle",
            "Reviewer PASS",
        ):
            for text in self.active_texts:
                self.assertNotIn(token, text)
        self.assertIn("delivery-stage-observation", self.migration)

    def test_config_and_single_marker_stay_stable(self) -> None:
        for fragment in (
            "schema_version: 2",
            "marker_namespace: project-slug",
            "base_branch: develop",
            "product_pr:",
            "memory_pr:",
            "scripts/config_guard.py",
        ):
            self.assertIn(fragment, self.skill)
        self.assertIn("schema-v1", self.skill)
        self.assertIn("${marker_namespace}:context-promotion", self.evidence)

    def test_spec_requires_a_grilled_confirmed_plan(self) -> None:
        self.assertIn("grilling", self.spec)
        self.assertIn("explicitly confirmed by the user", self.spec)
        self.assertIn("ask no further clarification question", self.spec)
        self.assertIn("受保护改动：无", self.spec)
        self.assertIn("one decision at a time", self.spec)
        self.assertIn("受保护改动：无", self.openai)

    def test_issue_contract_keeps_compact_scope_and_protected_surfaces(self) -> None:
        for heading in (
            "## 原始需求 / 问题背景",
            "## 目标",
            "## 非目标与边界",
            "### 改动范围",
            "## 持久项目记忆影响",
            "## 已确认决策",
            "## 实施计划",
            "## 验收与验证",
        ):
            self.assertIn(heading, self.issue_contract)
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
        self.assertNotIn("Context Authoring", self.issue_contract)

    def test_product_contract_headings_and_memory_rows(self) -> None:
        for heading in (
            "## 关联任务",
            "## 实施基线",
            "## 结果",
            "## 主要改动",
            "## 验证证据",
            "## 持久项目记忆实际影响",
            "## 完成声明",
            "## Review",
        ):
            self.assertIn(heading, self.product_contract)
        self.assertNotIn("## Closeout", self.product_contract)
        self.assertIn("Refs", self.product_contract)
        self.assertIn("closing keyword", self.product_contract)
        self.assertIn("exact literal `无`", self.product_contract)
        for category in (
            "decision",
            "stable_rule",
            "wiki_knowledge",
            "stable_context",
            "milestone_evidence",
        ):
            self.assertIn(category, self.product_contract)

    def test_review_checks_exactly_three_items(self) -> None:
        for item in ("issue-scope", "unit-tests", "durable-memory-impact"):
            self.assertIn(item, self.review)
            self.assertIn(item, self.evidence)
        self.assertIn("required_checks_known: true", self.review)
        self.assertIn("complete final product diff", self.review)
        self.assertIn("all-five-none", self.review)
        self.assertIn("return_stage: null | implementation | spec", self.evidence)

    def test_code_only_admission_is_exact(self) -> None:
        for source in (self.skill, self.delivery, self.evidence, self.review):
            self.assertIn("durable-memory-impact", source)
            self.assertIn("all-five-none", source)
        self.assertIn("exactly `无`", self.skill)
        self.assertIn("no Context Promotion state or related project-memory PR exists", self.skill)

    def test_memory_write_keeps_source_bound_confirmation(self) -> None:
        for source in (self.skill, self.delivery, self.promotion):
            self.assertIn("awaiting-confirmation", source)
            self.assertIn("confirmed", source)
        self.assertIn("source-bound", self.skill)
        self.assertIn("proposal_url", self.skill)
        self.assertIn("proposal_sha256", self.skill)
        self.assertIn("Reject a bare reply", self.skill)
        self.assertIn("memory-pr-merged", self.promotion)
        self.assertIn("no mandatory independent Reviewer", self.promotion)
        self.assertIn("direct-no-promotion-all-no-write", self.promotion)
        self.assertIn("direct-no-promotion-all-no-write", self.evidence)

    def test_merge_evidence_key_sets_match_the_guard(self) -> None:
        self.assertEqual(transport_guard.PRODUCT_MERGE_EVIDENCE_NAMES, ("review-pass",))
        self.assertEqual(
            transport_guard.MEMORY_MERGE_EVIDENCE_NAMES,
            ("proposal", "confirmation"),
        )
        self.assertEqual(transport_guard.EXPRESS_MERGE_EVIDENCE_NAMES, ())
        self.assertIn("`review-pass`", self.pr_transport)
        self.assertIn("`proposal` and `confirmation`", self.pr_transport)
        self.assertIn("merge_kind: express", self.pr_transport)
        self.assertIn("empty set", self.pr_transport)
        self.assertIn("merge_kind: express", self.express)

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
        ):
            self.assertIn(fragment, self.pr_transport)

    def test_issue_closure_stays_explicit(self) -> None:
        self.assertIn("change-metadata", self.delivery)
        self.assertIn("state_reason: completed", self.delivery)
        self.assertIn("Do not use closing keywords", self.skill)

    def test_express_path_keeps_its_safety_boundary(self) -> None:
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
            self.assertIn(protected_surface, self.express)
        self.assertIn("upgrade to path 1", self.express)
        self.assertIn("role: spec", self.express)
        self.assertIn("memory_candidates", self.express)
        self.assertIn("## 需求", self.express)

    def test_skill_stays_compact(self) -> None:
        self.assertLessEqual(len(self.skill.splitlines()), 260)
        self.assertLessEqual(len(self.skill.split()), 5000)

    def test_openai_prompt_matches_the_two_paths(self) -> None:
        for fragment in ("role: spec", "role: delivery", "role: express", "grilling", "role: init"):
            self.assertIn(fragment, self.openai)
        for legacy in ("closeout", "definition", "context-authoring"):
            self.assertNotIn(legacy, self.openai)


if __name__ == "__main__":
    unittest.main()
