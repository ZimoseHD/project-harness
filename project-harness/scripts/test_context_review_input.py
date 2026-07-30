#!/usr/bin/env python3
"""Tests for the canonical Context Promotion review-input helper."""

from __future__ import annotations

import copy
import unittest

from context_review_input import (
    canonicalize_review_input,
    review_input_sha256,
)


def manifest() -> dict[str, object]:
    return {
        "review_input_schema_version": 1,
        "review_policy_version": 1,
        "review_kind": "context-promotion-write",
        "effective_review_tier": "r1-documentary",
        "reviewed_items": [
            {"id": "CONTEXT-2", "tier": "r1-documentary"},
            {"id": "CONTEXT-1", "tier": "r1-documentary"},
        ],
        "source": {
            "issue_url": "https://github.example/o/r/issues/7",
            "issue_body_sha256": "a" * 64,
            "source_pr_url": "https://github.example/o/r/pull/8",
            "source_pr_title": "docs: context",
            "source_pr_body_sha256": "b" * 64,
            "source_head_ref": "task/context",
            "source_head_sha": "c" * 40,
            "source_merge_commit_sha": "d" * 40,
        },
        "eligibility": {
            "url": "https://github.example/o/r/pull/8#issuecomment-1",
            "sha256": "e" * 64,
        },
        "proposal": {
            "url": "https://github.example/o/r/pull/8#issuecomment-2",
            "sha256": "f" * 64,
        },
        "memory": {
            "url": "https://github.example/o/r/pull/9",
            "title": "docs: promote context",
            "body_sha256": "1" * 64,
            "head_ref": "memory/context",
            "head_sha": "2" * 40,
            "base_ref": "develop",
            "base_sha": "3" * 40,
        },
        "changed_files": [
            {
                "path": "docs/wiki/z.md",
                "status": "added",
                "previous_path": None,
                "blob_sha": "4" * 40,
            },
            {
                "path": "docs/wiki/a.md",
                "status": "modified",
                "previous_path": None,
                "blob_sha": "5" * 40,
            },
        ],
        "validation_impact": {
            "url": "https://github.example/o/r/pull/9#issuecomment-3",
            "sha256": "6" * 64,
        },
        "executed_validation": [
            {
                "command": "python3 docs_check.py",
                "result": "PASS",
                "evidence": "https://github.example/o/r/pull/9#issuecomment-4",
            }
        ],
    }


class ContextReviewInputTests(unittest.TestCase):
    def test_canonicalizes_repeated_fields_and_is_deterministic(self) -> None:
        first = manifest()
        second = copy.deepcopy(first)
        second["reviewed_items"].reverse()
        second["changed_files"].reverse()

        canonical = canonicalize_review_input(first)

        self.assertEqual(
            [item["id"] for item in canonical["reviewed_items"]],
            ["CONTEXT-1", "CONTEXT-2"],
        )
        self.assertEqual(
            review_input_sha256(first),
            review_input_sha256(second),
        )

    def test_digest_binds_persistent_proposal_diff_and_impact(self) -> None:
        first = manifest()
        mutations = []
        proposal = copy.deepcopy(first)
        proposal["proposal"]["sha256"] = "9" * 64
        mutations.append(proposal)
        changed_file = copy.deepcopy(first)
        changed_file["changed_files"][0]["blob_sha"] = "9" * 40
        mutations.append(changed_file)
        impact = copy.deepcopy(first)
        impact["validation_impact"]["sha256"] = "9" * 64
        mutations.append(impact)

        for changed in mutations:
            with self.subTest(changed=changed):
                self.assertNotEqual(
                    review_input_sha256(first),
                    review_input_sha256(changed),
                )

    def test_no_write_requires_null_memory_impact_and_empty_diff(self) -> None:
        value = manifest()
        value["review_kind"] = "context-promotion-no-write"
        value["effective_review_tier"] = "r0-no-write"
        for item in value["reviewed_items"]:
            item["tier"] = "r0-no-write"
        value["memory"] = None
        value["changed_files"] = []
        value["validation_impact"] = None

        self.assertRegex(review_input_sha256(value), r"^[0-9a-f]{64}$")

    def test_kind_specific_shapes_fail_closed(self) -> None:
        cases = []
        no_memory = manifest()
        no_memory["memory"] = None
        cases.append(no_memory)
        no_diff = manifest()
        no_diff["changed_files"] = []
        cases.append(no_diff)
        no_write_impact = manifest()
        no_write_impact["review_kind"] = "context-promotion-no-write"
        no_write_impact["effective_review_tier"] = "r0-no-write"
        no_write_impact["memory"] = None
        no_write_impact["changed_files"] = []
        cases.append(no_write_impact)

        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    review_input_sha256(value)

    def test_unknown_fields_duplicates_and_failed_validation_block(self) -> None:
        extra = manifest()
        extra["unknown"] = True
        with self.assertRaisesRegex(ValueError, "exactly"):
            review_input_sha256(extra)

        duplicate = manifest()
        duplicate["reviewed_items"][1]["id"] = "CONTEXT-2"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            review_input_sha256(duplicate)

        failed = manifest()
        failed["executed_validation"][0]["result"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "must equal PASS"):
            review_input_sha256(failed)

        boolean_schema = manifest()
        boolean_schema["review_input_schema_version"] = True
        with self.assertRaisesRegex(ValueError, "must equal 1"):
            review_input_sha256(boolean_schema)

        unhashable_kind = manifest()
        unhashable_kind["review_kind"] = []
        with self.assertRaisesRegex(ValueError, "unknown"):
            review_input_sha256(unhashable_kind)

    def test_lower_effective_tier_duplicate_path_and_local_locator_block(
        self,
    ) -> None:
        tier = manifest()
        tier["reviewed_items"][0]["tier"] = "r3-normative"
        with self.assertRaisesRegex(ValueError, "must not be lower"):
            review_input_sha256(tier)

        duplicate_path = manifest()
        duplicate_path["changed_files"][1]["path"] = "docs/wiki/z.md"
        with self.assertRaisesRegex(ValueError, "duplicate paths"):
            review_input_sha256(duplicate_path)

        local = manifest()
        local["source"]["issue_url"] = "/home/user/private.md"
        with self.assertRaisesRegex(ValueError, "HTTPS URL"):
            review_input_sha256(local)

        all_r0 = manifest()
        for item in all_r0["reviewed_items"]:
            item["tier"] = "r0-no-write"
        with self.assertRaisesRegex(ValueError, "non-R0"):
            review_input_sha256(all_r0)


if __name__ == "__main__":
    unittest.main()
