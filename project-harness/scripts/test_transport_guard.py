#!/usr/bin/env python3
"""Executable Project Harness normal and failure-path checks for transport guards."""

from __future__ import annotations

import unittest

from transport_guard import (
    changed_protected_fields,
    content_decision,
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


if __name__ == "__main__":
    unittest.main()
