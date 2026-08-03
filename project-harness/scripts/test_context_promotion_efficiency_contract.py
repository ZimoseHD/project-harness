from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "project-harness"
REFERENCES = HARNESS / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class LeanEfficiencyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read(HARNESS / "SKILL.md")
        cls.delivery = read(REFERENCES / "delivery.md")
        cls.definition = read(REFERENCES / "definition.md")
        cls.closeout = read(REFERENCES / "closeout.md")
        cls.promotion = read(REFERENCES / "context-promotion.md")
        cls.evidence = read(REFERENCES / "delivery-evidence-contract.md")
        cls.logs = read(REFERENCES / "delivery-log-contract.md")
        cls.issue_transport = read(REFERENCES / "issue-transport.md")
        cls.pr_transport = read(REFERENCES / "pull-request-transport.md")

    def test_root_skill_stays_within_progressive_disclosure_budget(self) -> None:
        body = self.skill.split("---", 2)[-1]
        self.assertLess(len(body.split()), 5000)
        self.assertLess(len(self.skill.splitlines()), 260)

    def test_normal_dispatch_omits_bundle_payload_fanout(self) -> None:
        envelope = re.search(
            r"~~~yaml\ndelegation:\n(?P<body>.*?)\n~~~", self.skill, re.DOTALL
        )
        self.assertIsNotNone(envelope)
        body = envelope.group("body")
        self.assertIn("schema_version: 3", body)
        for forbidden in (
            "bundle_schema_version",
            "bundle_sha256",
            "evidence_component_identities",
            "payloads:",
            "completeness:",
        ):
            self.assertNotIn(forbidden, body)
        self.assertIn("Do not attach an Evidence Bundle", self.delivery)

    def test_targeted_reads_replace_default_complete_pagination(self) -> None:
        self.assertIn("Do not enumerate every Issue comment page", self.skill)
        self.assertIn("Request complete comment pagination only", self.delivery)
        self.assertIn("ambiguous", self.delivery)
        self.assertIn("legacy", self.delivery)

    def test_definition_and_closeout_are_proportional(self) -> None:
        self.assertIn("clear and low-risk requirement, ask no clarification question", self.definition)
        self.assertIn("does not require an independent Reviewer", self.definition)
        self.assertIn("Reuse a validation result only when", self.closeout)
        self.assertIn("Do not rerun a current-head check merely", self.closeout)
        self.assertIn("Rerun the narrow applicable command", self.closeout)

    def test_code_only_happy_path_has_no_promotion_choreography(self) -> None:
        section = self.delivery.split("## Select code-only or Context Promotion", 1)[1]
        section = section.split("## Relay a real memory-write confirmation", 1)[0]
        self.assertIn("skip Context Promotion", section)
        for skipped in (
            "no-write proposal",
            "Reviewer PASS",
            "confirmation",
            "terminal callback",
            "Delivery log",
            "post-close comment",
        ):
            self.assertIn(skipped, section)
        self.assertNotIn("request-confirmation", section)

    def test_direct_no_promotion_does_not_persist_r0_choreography(self) -> None:
        self.assertRegex(
            self.promotion,
            r"(?s)(?:first new|new Lean).*?(?:all.*?no_write|no write remains).*?(?:direct|immediate).*?no-promotion",
        )
        self.assertRegex(
            self.promotion,
            r"(?s)(?:direct|Lean).*?no-promotion.*?(?:do not|without).*?proposal",
        )
        self.assertRegex(
            self.promotion,
            r"(?s)(?:direct|Lean).*?no-promotion.*?(?:do not|without).*?(?:Reviewer|confirmation)",
        )

    def test_write_path_loads_strict_evidence_only_when_needed(self) -> None:
        self.assertIn("If any write remains", self.skill)
        self.assertIn("proposal artifact", self.delivery)
        self.assertIn("fresh independent Reviewer PASS", self.delivery)
        self.assertIn("awaiting-confirmation", self.delivery)
        self.assertIn("memory-pr-merged", self.delivery)
        self.assertIn("validation-impact", self.evidence)

    def test_existing_lineages_always_win_over_lean_shortcuts(self) -> None:
        for source in (self.delivery, self.promotion):
            self.assertRegex(
                source,
                r"(?is)(?:existing|persisted|valid).*?(?:lineage|state).*?(?:never|do not|must not).*?(?:fast path|shortcut|Lean|code-only)",
            )
        for state in (
            "awaiting-confirmation",
            "confirmed",
            "memory-pr-ready",
            "memory-pr-merged",
        ):
            self.assertIn(state, self.promotion)

    def test_stage_logs_are_not_a_runtime_cost_or_completion_gate(self) -> None:
        self.assertIn("frozen", self.logs.lower())
        self.assertIn("read-only", self.logs.lower())
        self.assertRegex(self.logs, r"(?i)(?:must not|do not).{0,120}(?:write|backfill)")
        self.assertIn("never require `stage_logs.coverage_level`", self.delivery)
        self.assertIn("Do not require Delivery-log coverage", self.delivery)
        self.assertNotIn("delivery_log.py", self.delivery)

    def test_legacy_helpers_remain_available_without_new_runtime_use(self) -> None:
        for script in (
            "delivery_log.py",
            "evidence_bundle.py",
            "context_review_input.py",
            "validation_impact.py",
        ):
            self.assertTrue((HARNESS / "scripts" / script).is_file())
        self.assertIn("legacy", self.skill.lower())
        self.assertIn("legacy", self.logs.lower())

    def test_irreversible_safety_checks_are_not_reduced(self) -> None:
        for fragment in (
            "required_checks_known: true",
            "mergeable: true",
            "merge_methods_known: true",
            "merge_provenance",
            "independently",
        ):
            self.assertIn(fragment, self.pr_transport)
        self.assertIn("immediately before merge", self.pr_transport.lower())
        self.assertIn("change-metadata", self.issue_transport)
        self.assertIn("separate fetch", self.issue_transport)


if __name__ == "__main__":
    unittest.main()
