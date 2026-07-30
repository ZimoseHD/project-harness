#!/usr/bin/env python3
"""Executable normal and failure-path checks for evidence bundle guards."""

from __future__ import annotations

import copy
from hashlib import sha256
import json
import unittest

from evidence_bundle import (
    build_bundle,
    derive_component_identities,
    validate_bundle,
)


def manifest() -> dict[str, object]:
    return {
        "bundle_schema_version": 1,
        "scope": "context-promotion",
        "semantic_round_key": "a" * 64,
        "provenance": {
            "authenticated_actor_login": "octocat",
            "authenticated_actor_id": 1,
            "mutation_author_login": "octocat",
            "transport_family": "github-app",
        },
        "completeness": {
            "issue_body": True,
            "workflow_comments": True,
            "related_pr_search": True,
            "product_pr": True,
            "authority_sources": True,
            "memory_pr": True,
            "diff": True,
            "checks": True,
        },
        "completeness_bindings": {
            "issue_body": ["issue-body"],
            "workflow_comments": ["workflow-comments"],
            "related_pr_search": ["related-pr-search"],
            "product_pr": ["product-pr"],
            "authority_sources": ["authority"],
            "memory_pr": ["memory-pr"],
            "diff": ["product-diff"],
            "checks": ["checks"],
        },
        "semantic_snapshot": {
            "round_binding": {
                "delegated_role": "context-promotion",
                "issue": {"number": 7},
                "next_action": "review",
            },
            "payload_identities": {},
        },
        "liveness_snapshot": {
            "issue_state": "open",
            "required_checks_digest": "b" * 64,
            "payload_identities": {},
        },
        "payloads": [
            {
                "id": "issue-body",
                "kind": "github-markdown",
                "locator": "https://github.example/owner/repo/issues/7",
                "snapshot_class": "semantic",
                "source_identity": "issue-body-sha256:" + "c" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": "需求\r\n\r\n",
            },
            {
                "id": "authority",
                "kind": "repository-file",
                "locator": "wiki/current.md",
                "snapshot_class": "semantic",
                "source_identity": "git-blob:" + "d" * 40,
                "content_sha256": "0" * 64,
                "normalized_content": "现行规则",
            },
            {
                "id": "product-diff",
                "kind": "git-diff",
                "locator": "git:0123456789abcdef:product.diff",
                "snapshot_class": "semantic",
                "source_identity": "git-diff:" + "e" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": "diff --git a/a b/a\n",
            },
            {
                "id": "workflow-comments",
                "kind": "transport-result",
                "locator": "https://github.example/owner/repo/issues/7#comments",
                "snapshot_class": "semantic",
                "source_identity": "complete-comments:" + "1" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": '{"complete":true,"comments":[]}',
            },
            {
                "id": "related-pr-search",
                "kind": "transport-result",
                "locator": "https://github.example/owner/repo/pulls",
                "snapshot_class": "semantic",
                "source_identity": "complete-pr-search:" + "2" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": '{"complete":true,"pulls":[]}',
            },
            {
                "id": "product-pr",
                "kind": "transport-result",
                "locator": "https://github.example/owner/repo/pull/8",
                "snapshot_class": "semantic",
                "source_identity": "pr-tuple:" + "3" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": '{"number":8,"state":"closed"}',
            },
            {
                "id": "memory-pr",
                "kind": "transport-result",
                "locator": "https://github.example/owner/repo/pulls?head=memory",
                "snapshot_class": "semantic",
                "source_identity": "verified-absence:" + "4" * 64,
                "content_sha256": "0" * 64,
                "normalized_content": '{"complete":true,"pulls":[]}',
            },
            {
                "id": "checks",
                "kind": "transport-result",
                "locator": "https://github.example/owner/repo/commit/eeee/checks",
                "snapshot_class": "liveness",
                "source_identity": "checks-head:" + "e" * 40,
                "content_sha256": "0" * 64,
                "normalized_content": '{"required_checks_known":true}',
            },
        ],
    }


class EvidenceBundleTests(unittest.TestCase):
    def test_builds_normalized_valid_bundle_without_mutating_manifest(self) -> None:
        source = manifest()
        original = copy.deepcopy(source)

        bundle = build_bundle(source)
        issue_payload = next(
            payload
            for payload in bundle["payloads"]
            if payload["id"] == "issue-body"
        )

        self.assertEqual(source, original)
        self.assertEqual(
            issue_payload["normalized_content"],
            "需求\n",
        )
        self.assertEqual(
            issue_payload["content_sha256"],
            sha256("需求\n".encode("utf-8")).hexdigest(),
        )
        self.assertEqual(
            issue_payload["source_identity"],
            "content-sha256:" + issue_payload["content_sha256"],
        )
        expected_round_binding = bundle["semantic_snapshot"]["round_binding"]
        expected_round_json = json.dumps(
            expected_round_binding,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        self.assertEqual(
            bundle["semantic_round_key"],
            sha256(expected_round_json.encode("utf-8")).hexdigest(),
        )
        self.assertRegex(bundle["bundle_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(validate_bundle(bundle), [])

    def test_digest_is_deterministic_across_mapping_key_order(self) -> None:
        first = manifest()
        second = {
            key: first[key]
            for key in reversed(tuple(first))
        }
        second["semantic_snapshot"] = {
            key: first["semantic_snapshot"][key]  # type: ignore[index]
            for key in reversed(tuple(first["semantic_snapshot"]))  # type: ignore[arg-type]
        }
        second = copy.deepcopy(second)
        second["payloads"].reverse()
        for binding in second["completeness_bindings"].values():
            binding.reverse()

        first_bundle = build_bundle(first)
        second_bundle = build_bundle(second)

        self.assertEqual(first_bundle["bundle_sha256"], second_bundle["bundle_sha256"])
        self.assertEqual(first_bundle, second_bundle)

    def test_accepts_opaque_actor_id_and_remote_git_locator(self) -> None:
        source = manifest()
        source["provenance"]["authenticated_actor_id"] = "U_kwDOBoundActor"
        source["payloads"][2]["locator"] = (
            "git://github.example/owner/repo@0123456789abcdef:product.diff"
        )

        self.assertEqual(validate_bundle(build_bundle(source)), [])

    def test_reports_incomplete_duplicate_and_payload_digest_drift(self) -> None:
        bundle = build_bundle(manifest())
        bundle["completeness"]["checks"] = False
        bundle["completeness_bindings"]["checks"] = []
        duplicate = copy.deepcopy(bundle["payloads"][0])
        duplicate["normalized_content"] = "changed\n"
        bundle["payloads"].append(duplicate)

        errors = validate_bundle(bundle)

        self.assertTrue(any("duplicates payload id" in error for error in errors))
        self.assertTrue(
            any("does not match normalized_content" in error for error in errors)
        )
        self.assertTrue(
            any("bundle_sha256 does not match" in error for error in errors)
        )
        self.assertTrue(
            any(
                "completeness.checks is required but incomplete" in error
                for error in validate_bundle(bundle, {"checks"})
            )
        )

    def test_rejects_unknown_schema_missing_completeness_and_absolute_path(self) -> None:
        bundle = build_bundle(manifest())
        bundle["bundle_schema_version"] = 2
        del bundle["completeness"]["diff"]
        bundle["payloads"][0]["locator"] = "/home/user/private.md"

        errors = validate_bundle(bundle)

        self.assertTrue(any("must equal 1" in error for error in errors))
        self.assertTrue(
            any("completeness is missing fields: diff" in error for error in errors)
        )
        self.assertTrue(any("absolute local path" in error for error in errors))

    def test_rejects_boolean_schema_version_and_bundle_digest_drift(self) -> None:
        bundle = build_bundle(manifest())
        bundle["bundle_schema_version"] = True
        bundle["semantic_snapshot"]["round_binding"]["issue"]["number"] = 8

        errors = validate_bundle(bundle)

        self.assertTrue(any("must equal 1" in error for error in errors))
        self.assertTrue(
            any("does not match semantic_snapshot" in error for error in errors)
        )
        self.assertTrue(
            any("bundle_sha256 does not match" in error for error in errors)
        )

    def test_builder_rejects_unknown_fields(self) -> None:
        invalid = manifest()
        invalid["unexpected"] = True

        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            build_bundle(invalid)

    def test_incomplete_components_are_structural_cache_misses(self) -> None:
        source = manifest()
        source["completeness"]["memory_pr"] = False
        source["completeness_bindings"]["memory_pr"] = []

        bundle = build_bundle(source)

        self.assertEqual(validate_bundle(bundle), [])
        self.assertTrue(
            any(
                "completeness.memory_pr is required but incomplete" in error
                for error in validate_bundle(bundle, {"memory_pr"})
            )
        )

    def test_complete_component_requires_a_bound_existing_payload(self) -> None:
        empty = manifest()
        empty["completeness_bindings"]["checks"] = []
        with self.assertRaisesRegex(
            ValueError,
            "completeness_bindings.checks must bind at least one",
        ):
            build_bundle(empty)

        missing = manifest()
        missing["completeness_bindings"]["checks"] = ["missing-payload"]
        with self.assertRaisesRegex(
            ValueError,
            "references unknown payload IDs",
        ):
            build_bundle(missing)

    def test_consumer_binds_scope_and_outer_semantic_snapshot(self) -> None:
        source = manifest()
        expected_identities = derive_component_identities(source)
        bundle = build_bundle(source)

        self.assertEqual(
            validate_bundle(
                bundle,
                {"issue_body", "authority_sources"},
                expected_scope="context-promotion",
                expected_round_binding=source["semantic_snapshot"][
                    "round_binding"
                ],
                expected_component_identities={
                    "issue_body": expected_identities["issue_body"],
                    "authority_sources": expected_identities[
                        "authority_sources"
                    ],
                },
            ),
            [],
        )
        errors = validate_bundle(
            bundle,
            expected_scope="closeout",
            expected_round_binding={"wrong": "round"},
        )
        self.assertTrue(any("does not match expected_scope" in e for e in errors))
        self.assertTrue(
            any("does not match the expected delegation" in e for e in errors)
        )

    def test_consumer_cross_checks_current_component_identities(self) -> None:
        source = manifest()
        expected_identities = derive_component_identities(source)
        bundle = build_bundle(source)
        issue_identity = expected_identities["issue_body"]["issue-body"]
        round_binding = bundle["semantic_snapshot"]["round_binding"]
        self.assertEqual(
            validate_bundle(
                bundle,
                {"issue_body"},
                expected_scope="context-promotion",
                expected_round_binding=round_binding,
                expected_component_identities={
                    "issue_body": {"issue-body": issue_identity}
                },
            ),
            [],
        )

        stale = copy.deepcopy(issue_identity)
        stale["source_identity"] = "issue-body-sha256:" + "9" * 64
        errors = validate_bundle(
            bundle,
            {"issue_body"},
            expected_scope="context-promotion",
            expected_round_binding=round_binding,
            expected_component_identities={
                "issue_body": {"issue-body": stale}
            },
        )
        self.assertTrue(
            any("current transport identity" in error for error in errors)
        )

        wrong_class_source = manifest()
        next(
            payload
            for payload in wrong_class_source["payloads"]
            if payload["id"] == "issue-body"
        )["snapshot_class"] = "liveness"
        wrong_class_bundle = build_bundle(wrong_class_source)
        errors = validate_bundle(
            wrong_class_bundle,
            {"issue_body"},
            expected_scope="context-promotion",
            expected_round_binding=round_binding,
            expected_component_identities={
                "issue_body": expected_identities["issue_body"]
            },
        )
        self.assertTrue(
            any("current transport identity" in error for error in errors)
        )

    def test_snapshot_identity_cannot_point_at_stale_payload_bytes(self) -> None:
        bundle = build_bundle(manifest())
        bundle["semantic_snapshot"]["payload_identities"]["issue-body"][
            "source_identity"
        ] = "issue-body-sha256:" + "f" * 64

        errors = validate_bundle(bundle)

        self.assertTrue(
            any("does not match the bound payload identity" in e for e in errors)
        )
        self.assertTrue(
            any("bundle_sha256 does not match" in e for e in errors)
        )

    def test_malformed_scope_and_snapshot_identity_fail_without_crashing(
        self,
    ) -> None:
        bundle = build_bundle(manifest())
        bundle["scope"] = []
        bundle["semantic_snapshot"]["payload_identities"][7] = {
            "locator": "wiki/stale.md",
            "snapshot_class": "semantic",
            "source_identity": "git-blob:" + "7" * 40,
            "content_sha256": "7" * 64,
        }

        errors = validate_bundle(bundle)

        self.assertTrue(any("bundle.scope must be" in error for error in errors))
        self.assertTrue(any("non-string IDs" in error for error in errors))

    def test_successor_semantic_payload_keeps_the_same_round_key(self) -> None:
        bundle = build_bundle(manifest())
        successor = copy.deepcopy(bundle)
        successor.pop("bundle_sha256")
        successor["payloads"].append(
            {
                "id": "new-authority",
                "kind": "repository-file",
                "locator": "wiki/new.md",
                "snapshot_class": "semantic",
                "source_identity": "git-blob:" + "f" * 40,
                "content_sha256": "0" * 64,
                "normalized_content": "new authority",
            }
        )
        successor["completeness_bindings"]["authority_sources"].append(
            "new-authority"
        )

        rebuilt = build_bundle(successor)

        self.assertEqual(
            rebuilt["semantic_round_key"],
            bundle["semantic_round_key"],
        )
        self.assertNotEqual(rebuilt["bundle_sha256"], bundle["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
