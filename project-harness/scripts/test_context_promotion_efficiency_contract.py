#!/usr/bin/env python3
"""Contract checks for Context Promotion efficiency without weakened gates."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def markdown_section(markdown: str, heading: str, *, level: int = 2) -> str:
    """Return one exact Markdown section, including its heading."""
    hashes = "#" * level
    match = re.search(
        rf"(?ms)^{re.escape(hashes)} {re.escape(heading)}\n"
        rf".*?(?=^#{{1,{level}}} |\Z)",
        markdown,
    )
    if match is None:
        raise AssertionError(f"missing Markdown section: {hashes} {heading}")
    return match.group(0)


def section_containing(markdown: str, needle: str, *, level: int = 2) -> str:
    """Return the unique section at ``level`` that contains ``needle``."""
    sections = re.findall(
        rf"(?ms)^#{{{level}}} .+?\n.*?(?=^#{{1,{level}}} |\Z)",
        markdown,
    )
    matches = [section for section in sections if needle in section]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one level-{level} section containing {needle!r}, "
            f"found {len(matches)}"
        )
    return matches[0]


def fenced_block_containing(markdown: str, needle: str) -> str:
    """Return the unique fenced block containing ``needle``."""
    blocks = re.findall(
        r"(?ms)^(?:~~~|```)[A-Za-z0-9_-]*\n(.*?)\n(?:~~~|```)$",
        markdown,
    )
    matches = [block for block in blocks if needle in block]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one fenced block containing {needle!r}, "
            f"found {len(matches)}"
        )
    return matches[0]


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

    def assertMatchesAll(
        self,
        text: str,
        patterns: tuple[str, ...],
        *,
        source: str,
    ) -> None:
        for pattern in patterns:
            with self.subTest(source=source, pattern=pattern):
                self.assertRegex(text, re.compile(pattern, re.IGNORECASE | re.DOTALL))

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


class ContextPromotionEfficiencyContractTests(ProtocolAssertions):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read_text("SKILL.md")
        cls.delivery = read_text("references/delivery.md")
        cls.promotion = read_text("references/context-promotion.md")
        cls.evidence = read_text("references/delivery-evidence-contract.md")
        cls.delivery_log = read_text("references/delivery-log-contract.md")
        cls.issue_transport = read_text("references/issue-transport.md")
        cls.pr_transport = read_text("references/pull-request-transport.md")

    def test_delegation_v2_and_schema_v1_full_read_fallback_are_consistent(
        self,
    ) -> None:
        delegation = markdown_section(
            self.skill,
            "Delegate without expanding authority",
        )
        dispatch = markdown_section(
            self.delivery,
            "Dispatch bounded Phase Owners",
        )
        phase_input = markdown_section(
            self.promotion,
            "Reuse one exact Evidence Bundle",
        )

        self.assertContainsAll(
            delegation,
            (
                "delegation:",
                "schema_version: 2",
                "evidence_bundle:",
                "bundle_sha256:",
            ),
            source="delegation schema-v2 envelope",
        )
        fallback_pattern = (
            r"schema-v1.{0,240}(?:complete|full).{0,60}"
            r"(?:fresh[- ]read|full[- ]read|read)"
        )
        for source, text in (
            ("root delegation compatibility", delegation),
            ("Delivery dispatch compatibility", dispatch),
            ("Context Promotion delegated input", phase_input),
        ):
            with self.subTest(source=source):
                self.assertRegex(
                    text,
                    re.compile(fallback_pattern, re.IGNORECASE | re.DOTALL),
                )
                self.assertNotRegex(
                    text,
                    re.compile(
                        r"schema-v1.{0,160}(?:upgrade|reinterpret|treat).{0,80}"
                        r"(?:as|to) schema-v2",
                        re.IGNORECASE | re.DOTALL,
                    ),
                )

    def test_evidence_bundle_is_digest_bound_operation_local_and_non_authoritative(
        self,
    ) -> None:
        delegation = markdown_section(
            self.skill,
            "Delegate without expanding authority",
        )
        evidence_scope = markdown_section(self.evidence, "Apply the contract")
        logs = markdown_section(self.delivery_log, "Keep logs observational")

        self.assertContainsAll(
            delegation,
            (
                "evidence_bundle:",
                "semantic_round_key:",
                "bundle_sha256:",
                "operation-local",
                "completeness_bindings:",
                "evidence_component_identities:",
                "derive_component_identities",
                "expected_round_binding",
                "expected_component_identities",
                "liveness-only successor Bundle",
            ),
            source="operation-local Evidence Bundle",
        )
        for source, text in (
            ("root Evidence Bundle boundary", delegation),
            ("persistent evidence boundary", evidence_scope),
        ):
            with self.subTest(source=source):
                self.assertMatchesAll(
                    text,
                    (
                        r"Evidence Bundle.{0,240}"
                        r"(?:non-persistent|not persistent|never as persistent)",
                        r"Evidence Bundle.{0,240}"
                        r"(?:non-authoritative|does not authorize|never authorizes"
                        r"|never as.{0,80}(?:mutation )?authority)",
                    ),
                    source=source,
                )

        self.assertMatchesAll(
            delegation,
            (
                r"Evidence Bundle.{0,260}(?:never|must not|do not).{0,180}"
                r"Delivery observation",
                r"Evidence Bundle.{0,320}(?:never|must not|do not).{0,220}"
                r"(?:project memory|project-memory)",
            ),
            source="Bundle persistence exclusions",
        )
        self.assertContainsAll(
            logs,
            (
                "Evidence Bundle",
                "Delivery observation",
            ),
            source="Delivery-log Bundle exclusion",
        )
        self.assertMatchesAll(
            logs,
            (
                r"(?:Never|Do not|must not).{0,120}Evidence Bundle",
                r"Evidence Bundle.{0,280}(?:project memory|project-memory)",
            ),
            source="Delivery-log non-persistence",
        )

    def test_l0_through_l3_tuple_layers_keep_transport_and_terminal_guards(
        self,
    ) -> None:
        layers = markdown_section(
            self.skill,
            "Delegate without expanding authority",
        )

        self.assertInOrder(
            layers,
            (
                "`L0 bundle-integrity`",
                "`L1 semantic-freshness`",
                "`L2 atomic-mutation-guard`",
                "`L3 irreversible-gate`",
            ),
            source="tuple verification layers",
        )
        self.assertContainsAll(
            layers,
            (
                "A Bundle never replaces this layer",
                "A Bundle never authorizes merge or close",
            ),
            source="Bundle cannot replace mutation or irreversible gates",
        )

        self.assertContainsAll(
            self.delivery,
            (
                "`L0 bundle-integrity`",
                "`L1 semantic-freshness`",
                "`L2 atomic-mutation-guard`",
                "`L3 irreversible-gate`",
            ),
            source="Delivery layer consumers",
        )
        self.assertContainsAll(
            self.promotion,
            (
                "`L0 bundle-integrity`",
                "`L1 semantic-freshness`",
                "`L2 atomic-mutation-guard`",
                "`L3 irreversible-gate`",
            ),
            source="Context Promotion layer consumers",
        )
        self.assertContainsAll(
            self.issue_transport,
            ("`L2 atomic-mutation-guard`", "`L3 irreversible-gate`"),
            source="Issue transport guards",
        )
        self.assertContainsAll(
            self.pr_transport,
            ("`L2 atomic-mutation-guard`", "`L3 irreversible-gate`"),
            source="Pull Request transport guards",
        )

    def test_review_tiers_map_by_risk_but_keep_independence_and_confirmation(
        self,
    ) -> None:
        tier_policy = markdown_section(
            self.promotion,
            "Calculate the review tier",
        )
        review = markdown_section(
            self.promotion,
            "Require independent review",
        )
        delegation = markdown_section(
            self.skill,
            "Delegate without expanding authority",
        )
        relay = markdown_section(
            self.delivery,
            "Relay the Context Promotion confirmation",
        )

        self.assertMatchesAll(
            tier_policy,
            (
                r"`r0-no-write`.{0,180}`no_write`",
                r"`r1-documentary`.{0,220}`wiki_knowledge`.{0,120}"
                r"`milestone_evidence`",
                r"`r2-stable-context`.{0,180}`stable_context`",
                r"`r3-normative`.{0,220}`decision`.{0,120}`stable_rule`",
                r"effective_review_tier.{0,100}(?:highest|maximum|max)",
                r"mixed proposal.{0,220}(?:fresh|independent).{0,80}Reviewer",
            ),
            source="Context Promotion review-tier policy",
        )
        self.assertContainsAll(
            delegation,
            (
                "fresh",
                "read-only",
                "independent Reviewer",
                "PASS",
                "FAIL",
            ),
            source="Reviewer independence remains global",
        )
        self.assertContainsAll(
            review,
            (
                "fresh read-only Reviewer",
                "structured",
                "PASS",
                "FAIL",
            ),
            source="Reviewer remains independent at every effective tier",
        )
        self.assertContainsAll(
            relay,
            (
                "awaiting-confirmation",
                "user_decision",
                "end the current turn",
                "later current explicit",
            ),
            source="confirmation gate remains split-turn and source-bound",
        )
        self.assertIn("source-bound user confirmation", tier_policy)

    def test_reviewer_pass_is_versioned_and_old_unversioned_pass_is_legacy_full(
        self,
    ) -> None:
        no_write = markdown_section(
            self.evidence,
            "Reviewer PASS for no-write",
            level=3,
        )
        write = markdown_section(
            self.evidence,
            "Reviewer PASS for a write",
            level=3,
        )
        compatibility = markdown_section(self.evidence, "Preserve compatibility")
        canonical_input = markdown_section(
            self.evidence,
            "Context Promotion canonical review input",
            level=3,
        )
        review = markdown_section(
            self.promotion,
            "Require independent review",
        )

        versioned_fields = (
            "review_schema_version: 1",
            "review_policy_version: 1",
            "effective_review_tier:",
            "review_input_sha256:",
            "reviewed_items:",
        )
        for source, section in (
            ("no-write Reviewer PASS", no_write),
            ("write Reviewer PASS", write),
        ):
            self.assertContainsAll(
                section,
                versioned_fields,
                source=source,
            )

        for source, section in (
            ("evidence compatibility", compatibility),
            ("Context Promotion review compatibility", review),
        ):
            self.assertContainsAll(
                section,
                (
                    "unversioned Reviewer PASS",
                    "legacy-full",
                    "r3-normative",
                ),
                source=source,
            )
        self.assertMatchesAll(
            compatibility,
            (
                r"unversioned Reviewer PASS.{0,240}"
                r"(?:must not|never|do not).{0,100}"
                r"(?:rewrite|upgrade|downgrade|reinterpret)",
            ),
            source="legacy Reviewer PASS is not silently rewritten",
        )
        self.assertContainsAll(
            canonical_input,
            (
                "review_input_schema_version: 1",
                "scripts/context_review_input.py",
                "consumed_bundle_sha256",
                "do not include operation-local payload IDs",
                "Bundle container digest",
            ),
            source="deterministic canonical review input",
        )

    def test_validation_impact_is_markerless_and_cannot_reuse_old_head_ci(
        self,
    ) -> None:
        impact = section_containing(
            self.evidence,
            "artifact_kind: context-promotion-validation-impact",
            level=3,
        )
        impact_block = fenced_block_containing(
            impact,
            "artifact_kind: context-promotion-validation-impact",
        )
        repair = markdown_section(
            self.promotion,
            "Apply modification requests and promotion-scope repairs",
        )
        memory_merge = markdown_section(
            self.delivery,
            "Merge approved project memory",
        )
        merge_guard = markdown_section(
            self.pr_transport,
            "Guard an exact merge",
        )

        self.assertIn(
            "context-promotion-validation-impact",
            impact,
        )
        self.assertRegex(
            impact,
            re.compile(
                r"(?:without a workflow marker|markerless)",
                re.IGNORECASE,
            ),
        )
        self.assertNotIn("${marker_namespace}", impact_block)
        self.assertContainsAll(
            impact,
            (
                "prior_promotion_patch:",
                "current_promotion_patch:",
                "promotion_patch_sha256",
                "global_trigger_paths_complete: true",
                "disjoint union",
                "helper result exactly",
            ),
            source="deterministic validation-impact evidence",
        )
        self.assertContainsAll(
            repair,
            (
                "validation-impact artifact",
                "old lineage full-validation fallback",
                "The exact current head required CI is never reused",
                "old-head check",
            ),
            source="Context Promotion validation fallback",
        )
        for source, section in (
            ("Delivery memory merge gate", memory_merge),
            ("Pull Request merge guard", merge_guard),
        ):
            self.assertMatchesAll(
                section,
                (
                    r"exact current head.{0,120}"
                    r"(?:required CI|required[- ]check)",
                    r"(?:Never|Do not|must not).{0,120}"
                    r"(?:reuse|carry forward).{0,180}"
                    r"(?:old|previous)[- ]head"
                    r".{0,80}(?:required CI|required[- ]check|check)",
                ),
                source=source,
            )

    def test_observation_writes_use_targeted_readback_but_full_reads_remain(
        self,
    ) -> None:
        dedupe = markdown_section(
            self.delivery_log,
            "Deduplicate and backfill safely",
        )
        persistence = markdown_section(
            self.delivery,
            "Persist Delivery stage observations",
        )
        issue_operations = markdown_section(
            self.issue_transport,
            "Execute only atomic Issue operations",
        )
        issue_protection = markdown_section(
            self.issue_transport,
            "Protect every mutation",
        )
        coverage = markdown_section(
            self.delivery_log,
            "Require three coverage levels",
        )

        obsolete_rule = (
            "Before writing, require the Issue transport to enumerate all "
            "source Issue comments completely"
        )
        self.assertNotIn(obsolete_rule, dedupe)
        for source, section in (
            ("Delivery observation persistence", persistence),
            ("Delivery-log deduplication", dedupe),
        ):
            self.assertContainsAll(
                section,
                (
                    "normal observation write",
                    "comment ID",
                    "in-memory",
                    "ambiguous",
                    "recovery",
                    "final coverage",
                    "complete pagination",
                ),
                source=source,
            )
            self.assertMatchesAll(
                section,
                (
                    r"normal observation write.{0,260}"
                    r"(?:does not|need not|without).{0,100}"
                    r"(?:complete|full).{0,80}pag(?:e|ination)",
                    r"ambiguous.{0,260}(?:complete|full).{0,80}"
                    r"pag(?:e|ination)",
                    r"recovery.{0,260}(?:complete|full).{0,80}"
                    r"pag(?:e|ination)",
                    r"final coverage.{0,260}(?:complete|full).{0,80}"
                    r"pag(?:e|ination)",
                ),
                source=source,
            )

        self.assertMatchesAll(
            issue_operations + "\n" + issue_protection,
            (
                r"normal observation write.{0,260}(?:comment ID|exact comment)",
                r"ambiguous.{0,260}(?:every|all|complete).{0,80}"
                r"(?:comment page|pagination)",
                r"(?:coverage|recovery).{0,260}(?:every|all|complete).{0,80}"
                r"(?:comment page|pagination)",
            ),
            source="Issue transport targeted and exhaustive reads",
        )
        self.assertContainsAll(
            coverage,
            (
                "complete pagination",
                "final coverage",
            ),
            source="final observation coverage remains exhaustive",
        )

    def test_markers_callback_versions_and_merge_guard_remain_unchanged(
        self,
    ) -> None:
        markers = markdown_section(self.skill, "Preserve persistent markers")
        compatibility = markdown_section(self.evidence, "Preserve compatibility")
        merge_guard = markdown_section(
            self.pr_transport,
            "Guard an exact merge",
        )

        marker_rows = re.findall(
            r"(?m)^\| `(\$\{marker_namespace\}:[^`]+)` "
            r"\| `([^`]+)` \| (.*?) \|$",
            markers,
        )
        self.assertEqual(
            marker_rows,
            [
                (
                    "${marker_namespace}:context-authoring",
                    "context-authoring",
                    "`implementation`; `delivery`",
                ),
                (
                    "${marker_namespace}:context-promotion-eligible",
                    "closeout",
                    "`context-promotion`; `delivery`",
                ),
                (
                    "${marker_namespace}:context-promotion",
                    "context-promotion",
                    "`context-promotion`; `delivery`; conflict checks in `closeout`",
                ),
            ],
        )

        callback_contracts = (
            ("Awaiting-confirmation callback", "awaiting-confirmation"),
            ("Confirmed callback", "confirmed"),
            ("No-promotion terminal", "no-promotion"),
            ("Memory-PR-ready callback", "memory-pr-ready"),
            ("Memory-PR-merged terminal", "memory-pr-merged"),
        )
        for heading, outcome in callback_contracts:
            section = markdown_section(self.evidence, heading, level=3)
            with self.subTest(callback=heading):
                self.assertContainsAll(
                    section,
                    (
                        "schema_version: 2",
                        f"outcome: {outcome}",
                    ),
                    source=heading,
                )

        self.assertContainsAll(
            compatibility,
            (
                "marker forms",
                "schema versions",
                "digest algorithms",
            ),
            source="persistent callback compatibility",
        )
        self.assertContainsAll(
            merge_guard,
            (
                "role: delivery",
                "required_checks_known: true",
                "mergeable: true",
                "caller-supplied persistent gate evidence URL/digest pairs",
                "Immediately before merge",
                "independently re-read every evidence comment",
                "Never weaken a merge gate",
            ),
            source="irreversible merge guard",
        )
        self.assertMatchesAll(
            merge_guard,
            (
                r"(?:Evidence |A )Bundle.{0,220}(?:does not|cannot|never).{0,80}"
                r"(?:replace|substitute).{0,120}(?:merge guard|`L3`)",
            ),
            source="Bundle cannot replace the merge guard",
        )


if __name__ == "__main__":
    unittest.main()
