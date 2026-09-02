#!/usr/bin/env python3
"""Executable Project Harness normal and failure-path checks for transport guards."""

from __future__ import annotations

import unittest

from transport_guard import (
    changed_protected_fields,
    content_decision,
    exact_merge_guard,
    recover_ambiguous_mutation,
    select_active_candidate,
    verify_readback,
)


class TransportGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = {
            "repository": "owner/repo",
            "pr_number": 7,
            "state": "open",
            "is_draft": True,
            "head_ref": "task/7",
            "head_sha": "head-a",
            "base_ref": "main",
            "base_sha": "base-a",
            "body_sha256": "body-a",
        }

    def test_markdown_equivalence_is_no_op(self) -> None:
        self.assertEqual(content_decision("same\r\n", "same\n\n"), "no-op")
        self.assertEqual(content_decision("before", "after"), "mutation-required")

    def test_unchanged_baseline_has_no_conflicts(self) -> None:
        self.assertEqual(changed_protected_fields(self.snapshot, dict(self.snapshot)), [])

    def test_concurrent_ref_and_body_changes_are_blocking(self) -> None:
        latest = dict(self.snapshot, head_sha="head-b", body_sha256="body-b")
        self.assertEqual(
            changed_protected_fields(self.snapshot, latest),
            ["head_sha", "body_sha256"],
        )

    def test_unique_candidate_and_ambiguity(self) -> None:
        candidate = {"pr_number": 7, "state": "open"}
        self.assertEqual(select_active_candidate([candidate]), candidate)
        self.assertIsNone(select_active_candidate([{"pr_number": 6, "state": "closed"}]))
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            select_active_candidate([candidate, {"pr_number": 8, "state": "open"}])

    def test_readback_reports_exact_mismatches(self) -> None:
        actual = dict(self.snapshot, is_draft=False)
        verified, mismatches = verify_readback(
            self.snapshot,
            actual,
            ("pr_number", "is_draft", "head_sha"),
        )
        self.assertFalse(verified)
        self.assertEqual(mismatches, ["is_draft"])

    def test_ambiguous_recovery_requires_state_and_evidence(self) -> None:
        fields = ("pr_number", "body_sha256", "head_sha")
        self.assertEqual(
            recover_ambiguous_mutation(
                self.snapshot,
                dict(self.snapshot),
                fields,
                operation_evidence=True,
            ),
            "verified",
        )
        self.assertEqual(
            recover_ambiguous_mutation(
                self.snapshot,
                dict(self.snapshot),
                fields,
                operation_evidence=False,
            ),
            "indeterminate",
        )
        self.assertEqual(
            recover_ambiguous_mutation(
                self.snapshot,
                dict(self.snapshot, head_sha="head-b"),
                fields,
                operation_evidence=True,
            ),
            "indeterminate",
        )

    def _merge_snapshot(self) -> dict[str, object]:
        return {
            "title": "Deliver feature",
            "body_sha256": "1" * 64,
            "state": "open",
            "is_draft": False,
            "merged": False,
            "merge_commit_sha": None,
            "merge_method": None,
            "head_ref": "task/7",
            "head_sha": "head-a",
            "base_ref": "develop",
            "base_sha": "base-a",
            "required_checks_known": True,
            "required_checks": {
                "build": "success",
                "test": "success",
            },
            "mergeable": True,
        }

    def _expected_merge_tuple(self) -> dict[str, str]:
        return {
            "title": "Deliver feature",
            "body_sha256": "1" * 64,
            "head_ref": "task/7",
            "head_sha": "head-a",
            "base_ref": "develop",
            "base_sha": "base-a",
        }

    def _required_evidence(self) -> dict[str, tuple[str, str]]:
        return {
            "review-pass": (
                "https://github.com/owner/repo/pull/7#issuecomment-1",
                "a" * 64,
            ),
        }

    def _merge_guard(
        self,
        current: dict[str, object],
        *,
        expected: dict[str, str] | None = None,
        required_evidence: dict[str, tuple[str, str]] | None = None,
        current_evidence: dict[str, tuple[str, str]] | None = None,
        merge_kind: str = "product",
        merge_method: str = "squash",
        ambiguous_mutation: bool = False,
    ) -> str:
        expected_evidence = (
            self._required_evidence()
            if required_evidence is None
            else required_evidence
        )
        freshly_read_evidence = (
            dict(expected_evidence)
            if current_evidence is None
            else current_evidence
        )
        return exact_merge_guard(
            self._expected_merge_tuple() if expected is None else expected,
            current,
            expected_evidence,
            merge_method,
            merge_kind=merge_kind,  # type: ignore[arg-type]
            current_evidence=freshly_read_evidence,
            ambiguous_mutation=ambiguous_mutation,
        )

    def test_exact_merge_guard_allows_only_complete_successful_gate(self) -> None:
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
            ),
            "proceed",
        )

        blocked_snapshots = {
            "draft": dict(self._merge_snapshot(), is_draft=True),
            "unknown required checks": dict(
                self._merge_snapshot(),
                required_checks_known=False,
            ),
            "failed required check": dict(
                self._merge_snapshot(),
                required_checks={"build": "failure"},
            ),
            "unknown mergeability": dict(self._merge_snapshot(), mergeable=None),
            "merge conflict": dict(self._merge_snapshot(), mergeable=False),
        }
        for reason, snapshot in blocked_snapshots.items():
            with self.subTest(reason=reason):
                self.assertEqual(
                    self._merge_guard(
                        snapshot,
                    ),
                    "blocked",
                )

    def test_empty_known_required_set_ignores_raw_pending_for_all_methods(
        self,
    ) -> None:
        snapshot = dict(
            self._merge_snapshot(),
            required_checks_known=True,
            required_checks={},
            raw_combined_status="pending",
            legacy_status_context_count=0,
        )
        for merge_method in ("merge", "squash", "rebase"):
            with self.subTest(merge_method=merge_method):
                self.assertEqual(
                    self._merge_guard(
                        snapshot,
                        merge_method=merge_method,
                    ),
                    "proceed",
                )

    def test_guard_is_indifferent_to_platform_url_forms(self) -> None:
        evidence = {
            "review-pass": (
                "https://gitlab.com/group/subgroup/repo/-/merge_requests/7#note_12",
                "a" * 64,
            )
        }
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=evidence,
                current_evidence=dict(evidence),
            ),
            "proceed",
        )

    def test_exact_merge_guard_blocks_tuple_or_base_drift(self) -> None:
        for field, changed in {
            "title": "Changed title",
            "body_sha256": "2" * 64,
            "head_ref": "task/other",
            "head_sha": "head-b",
            "base_ref": "main",
            "base_sha": "base-b",
        }.items():
            snapshot = self._merge_snapshot()
            snapshot[field] = changed
            with self.subTest(field=field):
                self.assertEqual(
                    self._merge_guard(
                        snapshot,
                    ),
                    "blocked",
                )

        expected = self._expected_merge_tuple()
        expected["base_ref"] = "main"
        snapshot = self._merge_snapshot()
        snapshot["base_ref"] = "main"
        self.assertEqual(
            self._merge_guard(
                snapshot,
                expected=expected,
            ),
            "blocked",
        )

        merged = dict(
            snapshot,
            state="closed",
            merged=True,
            merge_commit_sha="merge-a",
            merge_method="squash",
            merge_provenance={
                "verified": True,
                "source": "merge-event",
                "guarded_base_sha": "base-a",
                "guarded_head_sha": "head-a",
                "merge_commit_sha": "merge-a",
            },
        )
        self.assertEqual(
            self._merge_guard(
                merged,
                expected=expected,
            ),
            "blocked",
        )
        self.assertEqual(
            self._merge_guard(
                merged,
                expected=expected,
                ambiguous_mutation=True,
            ),
            "indeterminate",
        )

    def test_exact_merge_guard_blocks_closed_unmerged_and_incomplete_inputs(self) -> None:
        closed_unmerged = dict(self._merge_snapshot(), state="closed")
        self.assertEqual(
            self._merge_guard(
                closed_unmerged,
            ),
            "blocked",
        )
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                merge_method=" ",
            ),
            "blocked",
        )
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                merge_method="bananas",
            ),
            "blocked",
        )

        incomplete_evidence = self._required_evidence()
        incomplete_evidence["review-pass"] = ("", "a" * 64)
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=incomplete_evidence,
            ),
            "blocked",
        )

        malformed_evidence = self._required_evidence()
        malformed_evidence["review-pass"] = (
            "https://github.com/owner/repo/pull/7#issuecomment-1",
            "not-a-sha256",
        )
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=malformed_evidence,
            ),
            "blocked",
        )

    def test_exact_merge_guard_requires_exact_evidence_keys_and_fresh_values(self) -> None:
        evidence = self._required_evidence()
        product_names = tuple(evidence)
        memory_evidence = {
            "proposal": (
                "https://github.com/owner/repo/pull/8#issuecomment-1",
                "d" * 64,
            ),
            "confirmation": (
                "https://github.com/owner/repo/pull/7#issuecomment-4",
                "e" * 64,
            ),
        }
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=memory_evidence,
                merge_kind="memory",
            ),
            "proceed",
        )

        cases = {
            "missing expected key": {
                "required_evidence": {
                    name: evidence[name] for name in product_names[:-1]
                },
                "current_evidence": None,
            },
            "extra expected key": {
                "required_evidence": memory_evidence,
                "current_evidence": None,
            },
            "missing current key": {
                "required_evidence": evidence,
                "current_evidence": {
                    name: evidence[name] for name in product_names[:-1]
                },
            },
            "extra current key": {
                "required_evidence": evidence,
                "current_evidence": memory_evidence,
            },
        }
        for reason, arguments in cases.items():
            with self.subTest(reason=reason):
                self.assertEqual(
                    self._merge_guard(
                        self._merge_snapshot(),
                        **arguments,
                    ),
                    "blocked",
                )

        arbitrary_evidence = {
            "foo": (
                "https://github.com/owner/repo/pull/7#issuecomment-99",
                "9" * 64,
            )
        }
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=arbitrary_evidence,
            ),
            "blocked",
        )
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                merge_kind="unknown",
            ),
            "blocked",
        )
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence=memory_evidence,
                merge_kind="product",
            ),
            "blocked",
        )

        for changed_pair in (
            (
                "https://github.com/owner/repo/pull/7#issuecomment-changed",
                "a" * 64,
            ),
            (
                "https://github.com/owner/repo/pull/7#issuecomment-1",
                "e" * 64,
            ),
        ):
            current_evidence = dict(evidence)
            current_evidence["review-pass"] = changed_pair
            with self.subTest(current_drift=changed_pair):
                self.assertEqual(
                    self._merge_guard(
                        self._merge_snapshot(),
                        current_evidence=current_evidence,
                    ),
                    "blocked",
                )

    def test_express_merge_requires_an_exactly_empty_evidence_set(self) -> None:
        self.assertEqual(
            self._merge_guard(
                self._merge_snapshot(),
                required_evidence={},
                current_evidence={},
                merge_kind="express",
            ),
            "proceed",
        )

        for reason, arguments in {
            "unexpected expected evidence": {
                "required_evidence": self._required_evidence(),
                "current_evidence": None,
            },
            "unexpected current evidence": {
                "required_evidence": {},
                "current_evidence": self._required_evidence(),
            },
        }.items():
            with self.subTest(reason=reason):
                self.assertEqual(
                    self._merge_guard(
                        self._merge_snapshot(),
                        merge_kind="express",
                        **arguments,
                    ),
                    "blocked",
                )

    def test_exact_already_merged_is_no_op_but_conflicting_identity_blocks(self) -> None:
        merged = dict(
            self._merge_snapshot(),
            state="closed",
            merged=True,
            merge_commit_sha="merge-a",
            merge_method="squash",
            merge_provenance={
                "verified": True,
                "source": "merge-event",
                "guarded_base_sha": "base-a",
                "guarded_head_sha": "head-a",
                "merge_commit_sha": "merge-a",
            },
        )
        self.assertEqual(
            self._merge_guard(
                merged,
            ),
            "no-op",
        )

        for field, changed in {
            "title": "Changed title",
            "merge_commit_sha": None,
            "merged": False,
            "is_draft": True,
            "required_checks_known": False,
            "required_checks": {"build": "failure"},
        }.items():
            conflicting = dict(merged)
            conflicting[field] = changed
            with self.subTest(field=field):
                self.assertEqual(
                    self._merge_guard(
                        conflicting,
                    ),
                    "blocked",
                )

        missing_current_evidence = self._required_evidence()
        missing_current_evidence.pop("review-pass")
        self.assertEqual(
            self._merge_guard(
                merged,
                current_evidence=missing_current_evidence,
            ),
            "blocked",
        )

        self.assertEqual(
            self._merge_guard(
                dict(merged, merge_method="merge"),
            ),
            "blocked",
        )

    def test_merged_base_tip_may_advance_only_with_exact_guarded_base(self) -> None:
        advanced = dict(
            self._merge_snapshot(),
            state="closed",
            merged=True,
            merge_commit_sha="merge-a",
            merge_method="squash",
            base_sha="base-live-new",
            merge_provenance={
                "verified": True,
                "source": "merge-event",
                "guarded_base_sha": "base-a",
                "guarded_head_sha": "head-a",
                "merge_commit_sha": "merge-a",
            },
        )
        self.assertEqual(self._merge_guard(advanced), "no-op")

        conflicting_guard = dict(
            advanced,
            merge_provenance=dict(
                advanced["merge_provenance"],
                guarded_base_sha="base-other",
            ),
        )
        self.assertEqual(self._merge_guard(conflicting_guard), "blocked")

        premerge_advanced = dict(
            self._merge_snapshot(),
            base_sha="base-live-new",
            merge_provenance={
                "verified": True,
                "source": "merge-event",
                "guarded_base_sha": "base-a",
                "guarded_head_sha": "head-a",
                "merge_commit_sha": "merge-a",
            },
        )
        self.assertEqual(self._merge_guard(premerge_advanced), "blocked")

        missing_provenance = dict(advanced)
        missing_provenance.pop("merge_provenance")
        self.assertEqual(self._merge_guard(missing_provenance), "blocked")

    def test_ambiguous_merge_recovery_is_exact_or_indeterminate(self) -> None:
        merged = dict(
            self._merge_snapshot(),
            state="closed",
            merged=True,
            merge_commit_sha="merge-a",
            merge_method="squash",
            merge_provenance={
                "verified": True,
                "source": "merge-event",
                "guarded_base_sha": "base-a",
                "guarded_head_sha": "head-a",
                "merge_commit_sha": "merge-a",
            },
        )
        self.assertEqual(
            self._merge_guard(
                merged,
                ambiguous_mutation=True,
            ),
            "no-op",
        )

        for field, changed in {
            "title": "Changed title",
            "state": "open",
            "merged": False,
            "merge_commit_sha": None,
        }.items():
            not_proven = dict(merged)
            not_proven[field] = changed
            with self.subTest(field=field):
                self.assertEqual(
                    self._merge_guard(
                        not_proven,
                        ambiguous_mutation=True,
                    ),
                    "indeterminate",
                )

        missing_current_evidence = self._required_evidence()
        missing_current_evidence.pop("review-pass")
        self.assertEqual(
            self._merge_guard(
                merged,
                current_evidence=missing_current_evidence,
                ambiguous_mutation=True,
            ),
            "indeterminate",
        )


if __name__ == "__main__":
    unittest.main()
