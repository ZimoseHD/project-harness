#!/usr/bin/env python3
"""Executable normal and fail-closed tests for validation_impact.py."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest

from validation_impact import (
    assess_validation_impact,
    canonical_input_sha256,
    promotion_patch_sha256,
)


class ValidationImpactTests(unittest.TestCase):
    def setUp(self) -> None:
        promotion_patch = {
            "complete": True,
            "truncated": False,
            "files": [
                {
                    "status": "modified",
                    "old_path": "docs/wiki/context.md",
                    "new_path": "docs/wiki/context.md",
                    "old_blob_sha": "a" * 40,
                    "new_blob_sha": "b" * 40,
                }
            ],
        }
        self.input = {
            "prior_base_sha": "1" * 40,
            "prior_head_sha": "2" * 40,
            "current_base_sha": "3" * 40,
            "current_head_sha": "4" * 40,
            "base_relation": "fast-forward",
            "current_base_is_head_ancestor": True,
            "base_delta": {
                "complete": True,
                "truncated": False,
                "files": [
                    {
                        "status": "modified",
                        "old_path": "docs/guide.md",
                        "new_path": "docs/guide.md",
                        "old_blob_sha": "5" * 40,
                        "new_blob_sha": "6" * 40,
                    }
                ],
            },
            "prior_promotion_patch": copy.deepcopy(promotion_patch),
            "current_promotion_patch": copy.deepcopy(promotion_patch),
            "prior_promotion_patch_sha256": promotion_patch_sha256(
                promotion_patch
            ),
            "current_promotion_patch_sha256": promotion_patch_sha256(
                promotion_patch
            ),
            "validation_inventory_complete": True,
            "validation_inventory": [
                {
                    "id": "unit",
                    "dependency_paths": ["src/**", "tests/unit/**"],
                    "global": False,
                },
                {
                    "id": "docs",
                    "dependency_paths": ["docs/**"],
                    "global": False,
                },
                {
                    "id": "integration",
                    "dependency_paths": ["integration/**"],
                    "global": False,
                },
            ],
            "global_trigger_paths_complete": True,
            "global_trigger_paths": [
                ".github/workflows/**",
                "pyproject.toml",
                "**/lockfiles/**",
            ],
        }

    def assess(self, value: dict[str, object] | None = None) -> dict[str, object]:
        return assess_validation_impact(self.input if value is None else value)

    def test_subset_dependency_match_is_incremental(self) -> None:
        result = self.assess()
        self.assertEqual(result["impact_mode"], "incremental")
        self.assertEqual(result["invalidated_validation_ids"], ["docs"])
        self.assertEqual(
            result["retained_validation_ids"], ["integration", "unit"]
        )
        self.assertEqual(
            result["reason_codes"], ["validation-dependency-subset-matched"]
        )
        self.assertEqual(result["input_sha256"], canonical_input_sha256(self.input))

    def test_no_dependency_match_reuses_all_evidence(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"][0].update(  # type: ignore[index]
            old_path="assets/logo.svg",
            new_path="assets/logo.svg",
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "reuse")
        self.assertEqual(result["invalidated_validation_ids"], [])
        self.assertEqual(
            result["retained_validation_ids"], ["docs", "integration", "unit"]
        )
        self.assertEqual(
            result["reason_codes"], ["no-validation-dependency-matched"]
        )

    def test_every_dependency_match_requires_full_validation(self) -> None:
        value = copy.deepcopy(self.input)
        value["validation_inventory"] = [
            {
                "id": "docs-a",
                "dependency_paths": ["docs/**"],
                "global": False,
            },
            {
                "id": "docs-b",
                "dependency_paths": ["**/*.md"],
                "global": False,
            },
        ]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["invalidated_validation_ids"], ["docs-a", "docs-b"]
        )
        self.assertEqual(result["retained_validation_ids"], [])
        self.assertEqual(
            result["reason_codes"], ["all-validation-dependencies-matched"]
        )

    def test_changed_patch_requires_full_validation(self) -> None:
        value = copy.deepcopy(self.input)
        current_patch = value["current_promotion_patch"]
        current_patch["files"][0]["new_blob_sha"] = "c" * 40
        value["current_promotion_patch_sha256"] = promotion_patch_sha256(
            current_patch
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["invalidated_validation_ids"], ["docs", "integration", "unit"]
        )
        self.assertEqual(result["reason_codes"], ["promotion-patch-changed"])

    def test_global_trigger_invalidates_every_validation(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"][0].update(  # type: ignore[index]
            old_path="pyproject.toml",
            new_path="pyproject.toml",
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["reason_codes"], ["global-trigger-path-matched"]
        )

    def test_explicitly_incomplete_inventory_requires_full_validation(self) -> None:
        value = copy.deepcopy(self.input)
        value["validation_inventory_complete"] = False
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["reason_codes"], ["validation-inventory-incomplete"]
        )

    def test_explicitly_incomplete_global_triggers_require_full_validation(
        self,
    ) -> None:
        value = copy.deepcopy(self.input)
        value["global_trigger_paths_complete"] = False
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["reason_codes"],
            ["global-trigger-inventory-incomplete"],
        )

    def test_unknown_global_trigger_completeness_blocks(self) -> None:
        value = copy.deepcopy(self.input)
        value["global_trigger_paths_complete"] = None
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn(
            "global-trigger-completeness-unknown",
            result["reason_codes"],
        )

    def test_empty_non_global_dependency_mapping_requires_full_validation(
        self,
    ) -> None:
        value = copy.deepcopy(self.input)
        value["validation_inventory"][0]["dependency_paths"] = []  # type: ignore[index]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "full")
        self.assertEqual(
            result["reason_codes"],
            ["validation-dependency-mapping-incomplete"],
        )

    def test_global_inventory_item_is_invalidated_by_any_base_change(self) -> None:
        value = copy.deepcopy(self.input)
        value["validation_inventory"].append(  # type: ignore[union-attr]
            {
                "id": "repository-policy",
                "dependency_paths": [],
                "global": True,
            }
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "incremental")
        self.assertEqual(
            result["invalidated_validation_ids"],
            ["docs", "repository-policy"],
        )
        self.assertEqual(
            result["retained_validation_ids"], ["integration", "unit"]
        )

    def test_removed_old_path_is_matched(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"] = [  # type: ignore[index]
            {
                "status": "removed",
                "old_path": "src/legacy.py",
                "new_path": None,
                "old_blob_sha": "a" * 40,
                "new_blob_sha": None,
            }
        ]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "incremental")
        self.assertEqual(result["invalidated_validation_ids"], ["unit"])

    def test_rename_matches_both_old_and_new_paths(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"] = [  # type: ignore[index]
            {
                "status": "renamed",
                "old_path": "src/legacy.py",
                "new_path": "docs/legacy.md",
                "old_blob_sha": "a" * 40,
                "new_blob_sha": "b" * 40,
            }
        ]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "incremental")
        self.assertEqual(
            result["invalidated_validation_ids"], ["docs", "unit"]
        )
        self.assertEqual(result["retained_validation_ids"], ["integration"])

    def test_added_identity_accepts_explicit_missing_old_side(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"] = [  # type: ignore[index]
            {
                "status": "added",
                "old_path": None,
                "new_path": "src/new.py",
                "old_blob_sha": None,
                "new_blob_sha": "a" * 40,
            }
        ]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "incremental")
        self.assertEqual(result["invalidated_validation_ids"], ["unit"])

    def test_unknown_or_unsafe_base_relation_blocks(self) -> None:
        for relation, reason in (
            ("unknown", "base-relation-unknown"),
            ("diverged", "base-not-fast-forward"),
        ):
            with self.subTest(relation=relation):
                value = copy.deepcopy(self.input)
                value["base_relation"] = relation
                result = self.assess(value)
                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(reason, result["reason_codes"])
                self.assertEqual(result["invalidated_validation_ids"], [])
                self.assertEqual(result["retained_validation_ids"], [])

    def test_false_or_unknown_current_ancestry_blocks(self) -> None:
        for ancestry, reason in (
            (False, "current-base-not-head-ancestor"),
            (None, "current-base-ancestry-unknown"),
        ):
            with self.subTest(ancestry=ancestry):
                value = copy.deepcopy(self.input)
                value["current_base_is_head_ancestor"] = ancestry
                result = self.assess(value)
                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(reason, result["reason_codes"])

    def test_incomplete_or_truncated_delta_blocks(self) -> None:
        cases = (
            ("complete", False, "base-delta-incomplete"),
            ("complete", None, "base-delta-completeness-unknown"),
            ("truncated", True, "base-delta-truncated"),
            ("truncated", None, "base-delta-truncation-unknown"),
        )
        for field, replacement, reason in cases:
            with self.subTest(field=field, replacement=replacement):
                value = copy.deepcopy(self.input)
                value["base_delta"][field] = replacement  # type: ignore[index]
                result = self.assess(value)
                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(reason, result["reason_codes"])

    def test_missing_or_malformed_blob_identity_blocks(self) -> None:
        cases = (
            ("old_blob_sha", None),
            ("new_blob_sha", "ABC"),
            ("new_path", None),
        )
        for field, replacement in cases:
            with self.subTest(field=field):
                value = copy.deepcopy(self.input)
                file_identity = value["base_delta"]["files"][0]  # type: ignore[index]
                file_identity[field] = replacement
                result = self.assess(value)
                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(
                    "changed-file-blob-or-shape-missing",
                    result["reason_codes"],
                )

    def test_unknown_status_and_missing_identity_key_block(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"][0]["status"] = "copied"  # type: ignore[index]
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("changed-file-status-unknown", result["reason_codes"])

        missing = copy.deepcopy(self.input)
        del missing["base_delta"]["files"][0]["new_blob_sha"]  # type: ignore[index]
        result = self.assess(missing)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("changed-file-identity-invalid", result["reason_codes"])

        unhashable = copy.deepcopy(self.input)
        unhashable["base_delta"]["files"][0]["status"] = []
        result = self.assess(unhashable)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("changed-file-status-unknown", result["reason_codes"])

    def test_duplicate_changed_file_identity_blocks(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_delta"]["files"].append(
            copy.deepcopy(value["base_delta"]["files"][0])
        )

        result = self.assess(value)

        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn(
            "changed-file-identity-duplicate",
            result["reason_codes"],
        )

    def test_duplicate_old_or_new_side_path_blocks(self) -> None:
        for changed_field, reason in (
            ("old_blob_sha", "changed-file-old-path-duplicate"),
            ("new_blob_sha", "changed-file-new-path-duplicate"),
        ):
            with self.subTest(changed_field=changed_field):
                value = copy.deepcopy(self.input)
                duplicate = copy.deepcopy(value["base_delta"]["files"][0])
                duplicate[changed_field] = "9" * 40
                value["base_delta"]["files"].append(duplicate)

                result = self.assess(value)

                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(reason, result["reason_codes"])

    def test_absolute_parent_and_backslash_paths_block(self) -> None:
        for path in ("/src/file.py", "../src/file.py", r"src\file.py"):
            with self.subTest(path=path):
                value = copy.deepcopy(self.input)
                value["base_delta"]["files"][0].update(  # type: ignore[index]
                    old_path=path,
                    new_path=path,
                )
                result = self.assess(value)
                self.assertEqual(result["impact_mode"], "blocked")
                self.assertIn(
                    "changed-file-path-invalid", result["reason_codes"]
                )

    def test_invalid_dependency_or_trigger_pattern_blocks(self) -> None:
        dependency = copy.deepcopy(self.input)
        inventory_item = dependency["validation_inventory"][0]  # type: ignore[index]
        inventory_item["dependency_paths"] = ["../src/**"]
        result = self.assess(dependency)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn(
            "validation-dependency-path-invalid", result["reason_codes"]
        )

        trigger = copy.deepcopy(self.input)
        trigger["global_trigger_paths"] = ["/pyproject.toml"]
        result = self.assess(trigger)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("global-trigger-path-invalid", result["reason_codes"])

    def test_duplicate_validation_ids_block(self) -> None:
        value = copy.deepcopy(self.input)
        value["validation_inventory"].append(  # type: ignore[union-attr]
            {
                "id": "unit",
                "dependency_paths": ["other/**"],
                "global": False,
            }
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("validation-id-duplicate", result["reason_codes"])

    def test_invalid_commit_or_patch_identity_blocks(self) -> None:
        commit = copy.deepcopy(self.input)
        commit["current_head_sha"] = "unknown"
        result = self.assess(commit)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("commit-identity-unknown", result["reason_codes"])

        patch = copy.deepcopy(self.input)
        patch["current_promotion_patch_sha256"] = "A" * 64
        result = self.assess(patch)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn(
            "promotion-patch-identity-unknown", result["reason_codes"]
        )

        mismatch = copy.deepcopy(self.input)
        mismatch["current_promotion_patch_sha256"] = "8" * 64
        result = self.assess(mismatch)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn(
            "current-promotion-patch-digest-mismatch",
            result["reason_codes"],
        )

    def test_structural_unknowns_and_extra_fields_block(self) -> None:
        missing = copy.deepcopy(self.input)
        del missing["current_head_sha"]
        result = self.assess(missing)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("input-schema-invalid", result["reason_codes"])
        self.assertIn("commit-identity-unknown", result["reason_codes"])

        extra = copy.deepcopy(self.input)
        extra["unbound_fact"] = True
        result = self.assess(extra)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertIn("input-schema-invalid", result["reason_codes"])

    def test_blocked_identity_takes_precedence_over_full_trigger(self) -> None:
        value = copy.deepcopy(self.input)
        value["base_relation"] = "diverged"
        value["validation_inventory_complete"] = False
        value["current_promotion_patch"]["files"][0][
            "new_blob_sha"
        ] = "c" * 40
        value["current_promotion_patch_sha256"] = promotion_patch_sha256(
            value["current_promotion_patch"]
        )
        result = self.assess(value)
        self.assertEqual(result["impact_mode"], "blocked")
        self.assertNotIn(
            "validation-inventory-incomplete", result["reason_codes"]
        )
        self.assertNotIn("promotion-patch-changed", result["reason_codes"])

    def test_canonical_digest_is_independent_of_mapping_key_order(self) -> None:
        expected_json = json.dumps(
            self.input,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        expected = hashlib.sha256(expected_json.encode("utf-8")).hexdigest()
        reordered = dict(reversed(list(self.input.items())))
        self.assertEqual(canonical_input_sha256(self.input), expected)
        self.assertEqual(canonical_input_sha256(reordered), expected)

    def test_canonical_digest_rejects_non_json_and_nonfinite_input(self) -> None:
        with self.assertRaisesRegex(TypeError, "JSON-compatible"):
            canonical_input_sha256({"bad": {1, 2}})  # type: ignore[dict-item]
        with self.assertRaisesRegex(ValueError, "finite canonical JSON"):
            canonical_input_sha256({"bad": float("nan")})

    def test_patch_digest_is_order_independent_and_binds_delete_rename(
        self,
    ) -> None:
        files = [
            {
                "status": "removed",
                "old_path": "docs/old.md",
                "new_path": None,
                "old_blob_sha": "d" * 40,
                "new_blob_sha": None,
            },
            {
                "status": "renamed",
                "old_path": "docs/a.md",
                "new_path": "docs/b.md",
                "old_blob_sha": "e" * 40,
                "new_blob_sha": "f" * 40,
            },
        ]
        first = {"complete": True, "truncated": False, "files": files}
        second = {
            "complete": True,
            "truncated": False,
            "files": list(reversed(copy.deepcopy(files))),
        }

        self.assertEqual(
            promotion_patch_sha256(first),
            promotion_patch_sha256(second),
        )
        second["files"][1]["old_blob_sha"] = "0" * 40
        self.assertNotEqual(
            promotion_patch_sha256(first),
            promotion_patch_sha256(second),
        )


if __name__ == "__main__":
    unittest.main()
