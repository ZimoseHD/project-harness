#!/usr/bin/env python3
"""Executable normal and failure-path checks for config_guard.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from config_guard import (
    ConfigError,
    build_v2_migration_payload,
    parse_config,
    render_config,
    render_v2_migration,
    resolve_merge_policy,
    validate_config,
)


SCRIPT = Path(__file__).with_name("config_guard.py")

V1_TEXT = """\
schema_version: 1
marker_namespace: "westwell-tcs"
"""

V2_TEXT = """\
schema_version: 2
marker_namespace: "westwell-tcs"
integration:
  base_branch: develop
  product_pr:
    merge_method: merge
  memory_pr:
    merge_method: squash
"""


class ConfigParserTests(unittest.TestCase):
    def test_parses_valid_v1_and_v2_with_comments(self) -> None:
        v1 = parse_config("# Harness config\n" + V1_TEXT)
        v2 = parse_config(V2_TEXT.replace("develop", "develop # integration base"))

        self.assertEqual(
            v1,
            {"schema_version": 1, "marker_namespace": "westwell-tcs"},
        )
        self.assertEqual(validate_config(v1), [])
        self.assertEqual(validate_config(v2), [])
        self.assertEqual(
            v2["integration"]["product_pr"]["merge_method"],
            "merge",
        )

    def test_rejects_duplicate_keys_at_every_level(self) -> None:
        duplicate_root = V1_TEXT + 'marker_namespace: "other"\n'
        duplicate_nested = V2_TEXT.replace(
            "    merge_method: merge\n",
            "    merge_method: merge\n    merge_method: squash\n",
        )
        for label, text in {
            "root": duplicate_root,
            "nested": duplicate_nested,
        }.items():
            with self.subTest(label=label):
                with self.assertRaisesRegex(ConfigError, "duplicate key"):
                    parse_config(text)

    def test_rejects_unsupported_yaml_and_bad_indentation(self) -> None:
        cases = {
            "tab": "schema_version:\t1\n",
            "sequence": "schema_version: [1]\n",
            "odd indentation": (
                "schema_version: 2\n"
                'marker_namespace: "westwell-tcs"\n'
                "integration:\n"
                " base_branch: develop\n"
            ),
            "skipped level": (
                "schema_version: 2\n"
                'marker_namespace: "westwell-tcs"\n'
                "integration:\n"
                "    base_branch: develop\n"
            ),
            "empty": "# no configuration\n",
        }
        for label, text in cases.items():
            with self.subTest(label=label):
                with self.assertRaises(ConfigError):
                    parse_config(text)

    def test_rejects_unknown_keys_in_v1_v2_and_nested_policies(self) -> None:
        cases = {
            "v1 integration": parse_config(
                V1_TEXT + "integration:\n  base_branch: develop\n"
            ),
            "v2 root": parse_config(V2_TEXT + "merge_method: merge\n"),
            "integration": parse_config(
                V2_TEXT.replace(
                    "  base_branch: develop\n",
                    "  base_branch: develop\n  strategy: automatic\n",
                )
            ),
            "product policy": parse_config(
                V2_TEXT.replace(
                    "    merge_method: merge\n",
                    "    merge_method: merge\n    automatic: enabled\n",
                )
            ),
        }
        for label, config in cases.items():
            with self.subTest(label=label):
                self.assertTrue(
                    any("unknown key" in error for error in validate_config(config))
                )

    def test_rejects_invalid_namespaces(self) -> None:
        invalid_values = (
            "Westwell-TCS",
            "westwell_tcs",
            "westwell:tcs",
            "",
            "a" * 64,
            "context-promotion",
            123,
        )
        for value in invalid_values:
            with self.subTest(value=value):
                errors = validate_config(
                    {"schema_version": 1, "marker_namespace": value}
                )
                self.assertTrue(
                    any("marker_namespace" in error for error in errors)
                )

    def test_rejects_unsupported_version_and_missing_keys(self) -> None:
        unsupported = {
            "schema_version": 3,
            "marker_namespace": "westwell-tcs",
        }
        missing = {"schema_version": 2, "marker_namespace": "westwell-tcs"}
        self.assertTrue(
            any("schema_version" in error for error in validate_config(unsupported))
        )
        self.assertIn(
            "config.integration: required key is missing",
            validate_config(missing),
        )

    def test_rejects_non_develop_base_and_invalid_merge_methods(self) -> None:
        non_develop = parse_config(V2_TEXT.replace("develop", "main"))
        invalid_product = parse_config(
            V2_TEXT.replace("merge_method: merge", "merge_method: octopus")
        )
        invalid_memory = parse_config(
            V2_TEXT.replace("merge_method: squash", "merge_method: automatic")
        )

        self.assertIn(
            "config.integration.base_branch: must be exactly develop",
            validate_config(non_develop),
        )
        self.assertTrue(
            any(
                "product_pr.merge_method" in error
                for error in validate_config(invalid_product)
            )
        )
        self.assertTrue(
            any(
                "memory_pr.merge_method" in error
                for error in validate_config(invalid_memory)
            )
        )


class MergePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.v1 = parse_config(V1_TEXT)
        self.v2 = parse_config(V2_TEXT)

    def test_v2_resolves_separate_product_and_memory_methods(self) -> None:
        result = resolve_merge_policy(
            self.v2,
            ["squash", "merge", "rebase"],
        )
        self.assertEqual(result["outcome"], "resolved")
        self.assertEqual(result["base_branch"], "develop")
        self.assertEqual(result["product_merge_method"], "merge")
        self.assertEqual(result["memory_merge_method"], "squash")
        self.assertEqual(
            result["available_methods"],
            ["merge", "rebase", "squash"],
        )
        self.assertEqual(result["policy_source"], "config-v2")

    def test_v2_blocks_when_either_configured_method_is_unavailable(self) -> None:
        result = resolve_merge_policy(self.v2, ["merge"])
        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["product_merge_method"], "merge")
        self.assertEqual(result["memory_merge_method"], "squash")
        self.assertIn("squash", result["reason"])

    def test_v1_unique_method_applies_to_both_pr_classes(self) -> None:
        for method in ("merge", "squash", "rebase"):
            with self.subTest(method=method):
                result = resolve_merge_policy(self.v1, [method])
                self.assertEqual(result["outcome"], "resolved")
                self.assertEqual(result["product_merge_method"], method)
                self.assertEqual(result["memory_merge_method"], method)
                self.assertEqual(
                    result["policy_source"],
                    "repository-single-method-v1",
                )

    def test_v1_multiple_methods_requires_migration(self) -> None:
        result = resolve_merge_policy(self.v1, ["squash", "merge"])
        self.assertEqual(result["outcome"], "migration-required")
        self.assertEqual(result["available_methods"], ["merge", "squash"])
        self.assertIsNone(result["product_merge_method"])
        self.assertIsNone(result["memory_merge_method"])

    def test_v1_no_available_method_blocks(self) -> None:
        result = resolve_merge_policy(self.v1, [])
        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("no supported merge method", result["reason"])

    def test_resolution_blocks_invalid_config_or_capability_values(self) -> None:
        invalid_config = {"schema_version": 1, "marker_namespace": "INVALID"}
        invalid_config_result = resolve_merge_policy(invalid_config, ["merge"])
        invalid_method_result = resolve_merge_policy(self.v1, ["octopus"])
        scalar_methods_result = resolve_merge_policy(self.v1, "merge")

        self.assertEqual(invalid_config_result["outcome"], "blocked")
        self.assertEqual(invalid_config_result["reason"], "invalid-config")
        self.assertTrue(invalid_config_result["validation_errors"])
        self.assertEqual(invalid_method_result["outcome"], "blocked")
        self.assertIn("unsupported", invalid_method_result["reason"])
        self.assertEqual(scalar_methods_result["outcome"], "blocked")
        self.assertIn("iterable", scalar_methods_result["reason"])


class MigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.v1 = parse_config(V1_TEXT)

    def test_migration_preserves_namespace_and_supports_distinct_methods(self) -> None:
        payload = build_v2_migration_payload(self.v1, "rebase", "merge")
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["marker_namespace"], "westwell-tcs")
        self.assertEqual(payload["integration"]["base_branch"], "develop")
        self.assertEqual(
            payload["integration"]["product_pr"]["merge_method"],
            "rebase",
        )
        self.assertEqual(
            payload["integration"]["memory_pr"]["merge_method"],
            "merge",
        )
        self.assertEqual(validate_config(payload), [])

    def test_migration_render_is_canonical_and_round_trips(self) -> None:
        rendered = render_v2_migration(self.v1, "merge", "squash")
        self.assertEqual(rendered, V2_TEXT)
        self.assertEqual(parse_config(rendered), build_v2_migration_payload(
            self.v1,
            "merge",
            "squash",
        ))
        self.assertEqual(render_config(parse_config(V1_TEXT)), V1_TEXT)

    def test_migration_rejects_wrong_source_base_or_methods(self) -> None:
        v2 = parse_config(V2_TEXT)
        cases = (
            lambda: build_v2_migration_payload(v2, "merge", "merge"),
            lambda: build_v2_migration_payload(
                self.v1,
                "merge",
                "merge",
                base_branch="main",
            ),
            lambda: build_v2_migration_payload(self.v1, "octopus", "merge"),
            lambda: build_v2_migration_payload(self.v1, "merge", "automatic"),
            lambda: build_v2_migration_payload(  # type: ignore[arg-type]
                self.v1,
                ["merge"],
                "merge",
            ),
        )
        for operation in cases:
            with self.subTest(operation=operation):
                with self.assertRaises(ConfigError):
                    operation()


class ConfigGuardCliTests(unittest.TestCase):
    def run_cli(
        self,
        content: str,
        *args: str,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), *args],
                text=True,
                capture_output=True,
                check=False,
            )
        return result, json.loads(result.stdout)

    def test_cli_validates_file_with_machine_readable_json(self) -> None:
        result, payload = self.run_cli(V2_TEXT)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["outcome"], "valid")
        self.assertEqual(payload["errors"], [])
        self.assertEqual(payload["config"]["schema_version"], 2)

    def test_cli_reports_duplicate_key_as_json(self) -> None:
        result, payload = self.run_cli(
            V1_TEXT + 'marker_namespace: "other"\n'
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["outcome"], "invalid")
        self.assertIn("duplicate key", payload["errors"][0])

    def test_cli_resolves_v2_policy(self) -> None:
        result, payload = self.run_cli(
            V2_TEXT,
            "--available-method",
            "merge",
            "--available-method",
            "squash",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["outcome"], "resolved")
        self.assertEqual(payload["product_merge_method"], "merge")
        self.assertEqual(payload["memory_merge_method"], "squash")

    def test_cli_uses_distinct_exit_for_v1_migration_requirement(self) -> None:
        result, payload = self.run_cli(
            V1_TEXT,
            "--available-method",
            "merge",
            "--available-method",
            "squash",
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["outcome"], "migration-required")

    def test_cli_renders_v1_migration_as_machine_readable_json(self) -> None:
        result, payload = self.run_cli(
            V1_TEXT,
            "--migrate-v1",
            "--product-method",
            "rebase",
            "--memory-method",
            "merge",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["outcome"], "migration-rendered")
        self.assertEqual(
            payload["source_config"]["marker_namespace"],
            "westwell-tcs",
        )
        self.assertEqual(
            payload["migration_config"],
            build_v2_migration_payload(
                parse_config(V1_TEXT),
                "rebase",
                "merge",
            ),
        )
        self.assertEqual(
            payload["rendered_config"],
            render_v2_migration(
                parse_config(V1_TEXT),
                "rebase",
                "merge",
            ),
        )

    def test_cli_rejects_migration_from_non_v1_source(self) -> None:
        result, payload = self.run_cli(
            V2_TEXT,
            "--migrate-v1",
            "--product-method",
            "merge",
            "--memory-method",
            "squash",
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["outcome"], "invalid")
        self.assertIn("schema_version 1", payload["errors"][0])

    def test_cli_rejects_missing_migration_methods(self) -> None:
        cases = (
            (),
            ("--product-method", "merge"),
            ("--memory-method", "squash"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result, payload = self.run_cli(
                    V1_TEXT,
                    "--migrate-v1",
                    *arguments,
                )
                self.assertEqual(result.returncode, 1)
                self.assertEqual(payload["outcome"], "invalid")
                self.assertIn("requires", payload["errors"][0])

    def test_cli_rejects_illegal_migration_methods(self) -> None:
        for flag, product_method, memory_method in (
            ("product", "octopus", "merge"),
            ("memory", "merge", "automatic"),
        ):
            with self.subTest(flag=flag):
                result, payload = self.run_cli(
                    V1_TEXT,
                    "--migrate-v1",
                    "--product-method",
                    product_method,
                    "--memory-method",
                    memory_method,
                )
                self.assertEqual(result.returncode, 1)
                self.assertEqual(payload["outcome"], "invalid")
                self.assertIn("must be merge, squash, or rebase", payload["errors"][0])


if __name__ == "__main__":
    unittest.main()
