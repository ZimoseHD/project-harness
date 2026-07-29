#!/usr/bin/env python3
"""Strict, deterministic guards for Project Harness configuration.

The module parses only the small YAML mapping subset used by
``.project-harness/config.yaml``. It has no network or filesystem mutation
side effects. Repository capabilities must be supplied by the caller as an
already discovered set of available merge methods.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


SUPPORTED_SCHEMA_VERSIONS = (1, 2)
SUPPORTED_MERGE_METHODS = ("merge", "squash", "rebase")
SUPPORTED_MERGE_METHOD_SET = frozenset(SUPPORTED_MERGE_METHODS)
INTEGRATION_BASE_BRANCH = "develop"
MARKER_NAMESPACE_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$", re.ASCII
)
RESERVED_MARKER_SUFFIXES = frozenset(
    {
        "context-authoring",
        "context-promotion-eligible",
        "context-promotion",
    }
)

_KEY_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$", re.ASCII)
_PLAIN_SCALAR_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$", re.ASCII)
_INTEGER_PATTERN = re.compile(r"^[+-]?[0-9]+$", re.ASCII)


class ConfigError(ValueError):
    """Report a strict configuration parse or migration error."""


def _strip_yaml_comment(line: str) -> str:
    """Remove a YAML-style comment outside a quoted scalar."""
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(line):
        character = line[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quote = None
        elif quote == "'":
            if character == "'" and index + 1 < len(line) and line[index + 1] == "'":
                index += 1
            elif character == "'":
                quote = None
        elif character in {"'", '"'}:
            quote = character
        elif character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
        index += 1
    return line.rstrip()


def _parse_single_quoted_scalar(token: str, line_number: int) -> str:
    if len(token) < 2 or token[-1] != "'":
        raise ConfigError(f"line {line_number}: unterminated single-quoted scalar")

    value: list[str] = []
    index = 1
    end = len(token) - 1
    while index < end:
        character = token[index]
        if character != "'":
            value.append(character)
            index += 1
            continue
        if index + 1 < end and token[index + 1] == "'":
            value.append("'")
            index += 2
            continue
        raise ConfigError(f"line {line_number}: invalid single-quoted scalar")
    return "".join(value)


def _parse_scalar(token: str, line_number: int) -> Any:
    if not token:
        raise ConfigError(f"line {line_number}: empty scalar")
    if token.startswith('"'):
        try:
            value = json.loads(token)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"line {line_number}: invalid double-quoted scalar"
            ) from error
        if not isinstance(value, str):
            raise ConfigError(f"line {line_number}: scalar must be a string")
        return value
    if token.startswith("'"):
        return _parse_single_quoted_scalar(token, line_number)
    if _INTEGER_PATTERN.fullmatch(token):
        return int(token, 10)
    if not _PLAIN_SCALAR_PATTERN.fullmatch(token):
        raise ConfigError(
            f"line {line_number}: unsupported YAML scalar syntax"
        )
    return token


def parse_config(text: str) -> dict[str, Any]:
    """Parse the exact mapping/scalar YAML subset used by Harness config.

    Accept mappings indented by exactly two spaces per level, blank lines,
    comments, plain ASCII scalars, quoted strings, and decimal integers.
    Reject duplicate keys, tabs, sequences, flow collections, aliases, tags,
    block scalars, multi-document input, and irregular indentation.
    """
    if not isinstance(text, str):
        raise ConfigError("configuration content must be text")

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-2, root)]

    for line_number, original_line in enumerate(
        text.replace("\r\n", "\n").replace("\r", "\n").split("\n"),
        start=1,
    ):
        if "\t" in original_line:
            raise ConfigError(f"line {line_number}: tabs are not supported")

        line = _strip_yaml_comment(original_line)
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        if indent % 2 != 0:
            raise ConfigError(
                f"line {line_number}: indentation must use two-space levels"
            )
        content = line[indent:]
        match = _KEY_PATTERN.fullmatch(content)
        if match is None:
            raise ConfigError(
                f"line {line_number}: expected one mapping key and scalar"
            )

        key, raw_value = match.groups()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent_indent, parent = stack[-1]
        if indent != parent_indent + 2:
            raise ConfigError(
                f"line {line_number}: unexpected indentation level"
            )
        if key in parent:
            raise ConfigError(
                f"line {line_number}: duplicate key {key!r}"
            )

        scalar = raw_value.strip()
        if scalar:
            parent[key] = _parse_scalar(scalar, line_number)
            continue

        child: dict[str, Any] = {}
        parent[key] = child
        stack.append((indent, child))

    if not root:
        raise ConfigError("configuration is empty")
    return root


def _check_exact_keys(
    value: Mapping[str, Any],
    *,
    expected: frozenset[str],
    path: str,
    errors: list[str],
) -> None:
    keys = set(value)
    non_string_keys = [key for key in keys if not isinstance(key, str)]
    if non_string_keys:
        errors.append(f"{path}: every key must be a string")
    string_keys = {key for key in keys if isinstance(key, str)}
    for key in sorted(expected - string_keys):
        errors.append(f"{path}.{key}: required key is missing")
    for key in sorted(string_keys - expected):
        errors.append(f"{path}.{key}: unknown key")


def _as_mapping(
    value: Any,
    *,
    path: str,
    errors: list[str],
) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        errors.append(f"{path}: must be a mapping")
        return None
    return value


def _validate_namespace(value: Any, errors: list[str]) -> None:
    path = "config.marker_namespace"
    if not isinstance(value, str):
        errors.append(f"{path}: must be an explicit string")
        return
    if not 1 <= len(value) <= 63:
        errors.append(f"{path}: must contain 1-63 characters")
        return
    if MARKER_NAMESPACE_PATTERN.fullmatch(value) is None:
        errors.append(
            f"{path}: must be a lowercase ASCII kebab-case slug"
        )
        return
    if value in RESERVED_MARKER_SUFFIXES:
        errors.append(f"{path}: must not equal a workflow marker suffix")


def _validate_merge_method(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or value not in SUPPORTED_MERGE_METHOD_SET:
        errors.append(f"{path}: must be merge, squash, or rebase")


def validate_config(config: Mapping[str, Any]) -> list[str]:
    """Return every deterministic schema-v1/v2 validation error."""
    if not isinstance(config, Mapping):
        return ["config: must be a mapping"]

    errors: list[str] = []
    schema_version = config.get("schema_version")
    valid_version = (
        isinstance(schema_version, int)
        and not isinstance(schema_version, bool)
        and schema_version in SUPPORTED_SCHEMA_VERSIONS
    )

    if not valid_version:
        errors.append("config.schema_version: must be integer 1 or 2")
        expected_root = frozenset(
            {"schema_version", "marker_namespace", "integration"}
        )
    elif schema_version == 1:
        expected_root = frozenset({"schema_version", "marker_namespace"})
    else:
        expected_root = frozenset(
            {"schema_version", "marker_namespace", "integration"}
        )
    _check_exact_keys(
        config,
        expected=expected_root,
        path="config",
        errors=errors,
    )

    if "marker_namespace" in config:
        _validate_namespace(config["marker_namespace"], errors)

    if schema_version != 2 or not valid_version or "integration" not in config:
        return errors

    integration = _as_mapping(
        config["integration"],
        path="config.integration",
        errors=errors,
    )
    if integration is None:
        return errors
    _check_exact_keys(
        integration,
        expected=frozenset({"base_branch", "product_pr", "memory_pr"}),
        path="config.integration",
        errors=errors,
    )

    if (
        "base_branch" in integration
        and integration["base_branch"] != INTEGRATION_BASE_BRANCH
    ):
        errors.append(
            "config.integration.base_branch: must be exactly develop"
        )

    for pr_kind in ("product_pr", "memory_pr"):
        if pr_kind not in integration:
            continue
        path = f"config.integration.{pr_kind}"
        pr_policy = _as_mapping(integration[pr_kind], path=path, errors=errors)
        if pr_policy is None:
            continue
        _check_exact_keys(
            pr_policy,
            expected=frozenset({"merge_method"}),
            path=path,
            errors=errors,
        )
        if "merge_method" in pr_policy:
            _validate_merge_method(
                pr_policy["merge_method"],
                f"{path}.merge_method",
                errors,
            )

    return errors


def _normalize_available_methods(
    available_methods: Iterable[str],
) -> tuple[list[str], str | None]:
    if isinstance(available_methods, (str, bytes)):
        return [], "available merge methods must be an iterable of method names"
    try:
        supplied_methods = list(available_methods)
    except TypeError:
        return [], "available merge methods must be iterable"

    invalid = sorted(
        {
            repr(method)
            for method in supplied_methods
            if not isinstance(method, str)
            or method not in SUPPORTED_MERGE_METHOD_SET
        }
    )
    if invalid:
        return [], (
            "available merge methods contain unsupported values: "
            + ", ".join(invalid)
        )
    return sorted(set(supplied_methods)), None


def _policy_result(
    *,
    outcome: str,
    schema_version: int | None,
    available_methods: list[str],
    product_merge_method: str | None,
    memory_merge_method: str | None,
    policy_source: str | None,
    reason: str | None,
    validation_errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "schema_version": schema_version,
        "base_branch": INTEGRATION_BASE_BRANCH,
        "product_merge_method": product_merge_method,
        "memory_merge_method": memory_merge_method,
        "available_methods": available_methods,
        "policy_source": policy_source,
        "reason": reason,
        "validation_errors": validation_errors or [],
    }


def resolve_merge_policy(
    config: Mapping[str, Any],
    available_methods: Iterable[str],
) -> dict[str, Any]:
    """Resolve configured merge policy against authoritative capabilities.

    Schema v2 selects its explicit product and memory methods. Schema v1 keeps
    compatibility only when the repository exposes exactly one supported
    method, using that method for both PR classes. Multiple v1 methods require
    explicit migration instead of choosing one.
    """
    validation_errors = validate_config(config)
    schema_version = config.get("schema_version")
    if validation_errors:
        return _policy_result(
            outcome="blocked",
            schema_version=(
                schema_version
                if isinstance(schema_version, int)
                and not isinstance(schema_version, bool)
                else None
            ),
            available_methods=[],
            product_merge_method=None,
            memory_merge_method=None,
            policy_source=None,
            reason="invalid-config",
            validation_errors=validation_errors,
        )

    methods, method_error = _normalize_available_methods(available_methods)
    if method_error is not None:
        return _policy_result(
            outcome="blocked",
            schema_version=schema_version,
            available_methods=[],
            product_merge_method=None,
            memory_merge_method=None,
            policy_source=None,
            reason=method_error,
        )

    if schema_version == 1:
        if len(methods) == 1:
            return _policy_result(
                outcome="resolved",
                schema_version=1,
                available_methods=methods,
                product_merge_method=methods[0],
                memory_merge_method=methods[0],
                policy_source="repository-single-method-v1",
                reason=None,
            )
        if len(methods) > 1:
            return _policy_result(
                outcome="migration-required",
                schema_version=1,
                available_methods=methods,
                product_merge_method=None,
                memory_merge_method=None,
                policy_source=None,
                reason="schema-v1 cannot choose among multiple merge methods",
            )
        return _policy_result(
            outcome="blocked",
            schema_version=1,
            available_methods=[],
            product_merge_method=None,
            memory_merge_method=None,
            policy_source=None,
            reason="no supported merge method is authoritatively available",
        )

    integration = config["integration"]
    product_method = integration["product_pr"]["merge_method"]
    memory_method = integration["memory_pr"]["merge_method"]
    unavailable = [
        method
        for method in (product_method, memory_method)
        if method not in methods
    ]
    if unavailable:
        return _policy_result(
            outcome="blocked",
            schema_version=2,
            available_methods=methods,
            product_merge_method=product_method,
            memory_merge_method=memory_method,
            policy_source="config-v2",
            reason=(
                "configured merge method is not authoritatively available: "
                + ", ".join(dict.fromkeys(unavailable))
            ),
        )
    return _policy_result(
        outcome="resolved",
        schema_version=2,
        available_methods=methods,
        product_merge_method=product_method,
        memory_merge_method=memory_method,
        policy_source="config-v2",
        reason=None,
    )


def build_v2_migration_payload(
    v1_config: Mapping[str, Any],
    product_merge_method: str,
    memory_merge_method: str,
    *,
    base_branch: str = INTEGRATION_BASE_BRANCH,
) -> dict[str, Any]:
    """Build a schema-v2 payload while preserving the exact v1 namespace."""
    errors = validate_config(v1_config)
    if errors:
        raise ConfigError("invalid schema-v1 source: " + "; ".join(errors))
    if v1_config.get("schema_version") != 1:
        raise ConfigError("migration source must use schema_version 1")
    if base_branch != INTEGRATION_BASE_BRANCH:
        raise ConfigError("integration base branch must be exactly develop")
    for name, method in (
        ("product_merge_method", product_merge_method),
        ("memory_merge_method", memory_merge_method),
    ):
        if (
            not isinstance(method, str)
            or method not in SUPPORTED_MERGE_METHOD_SET
        ):
            raise ConfigError(f"{name} must be merge, squash, or rebase")

    payload = {
        "schema_version": 2,
        "marker_namespace": v1_config["marker_namespace"],
        "integration": {
            "base_branch": INTEGRATION_BASE_BRANCH,
            "product_pr": {"merge_method": product_merge_method},
            "memory_pr": {"merge_method": memory_merge_method},
        },
    }
    payload_errors = validate_config(payload)
    if payload_errors:
        raise ConfigError("invalid migration payload: " + "; ".join(payload_errors))
    return payload


def render_config(config: Mapping[str, Any]) -> str:
    """Render a valid schema-v1/v2 config in one canonical YAML form."""
    errors = validate_config(config)
    if errors:
        raise ConfigError("cannot render invalid config: " + "; ".join(errors))

    namespace = json.dumps(config["marker_namespace"], ensure_ascii=True)
    if config["schema_version"] == 1:
        return (
            "schema_version: 1\n"
            f"marker_namespace: {namespace}\n"
        )

    integration = config["integration"]
    return (
        "schema_version: 2\n"
        f"marker_namespace: {namespace}\n"
        "integration:\n"
        f"  base_branch: {integration['base_branch']}\n"
        "  product_pr:\n"
        f"    merge_method: {integration['product_pr']['merge_method']}\n"
        "  memory_pr:\n"
        f"    merge_method: {integration['memory_pr']['merge_method']}\n"
    )


def render_v2_migration(
    v1_config: Mapping[str, Any],
    product_merge_method: str,
    memory_merge_method: str,
    *,
    base_branch: str = INTEGRATION_BASE_BRANCH,
) -> str:
    """Build and canonically render a namespace-preserving v1 migration."""
    return render_config(
        build_v2_migration_payload(
            v1_config,
            product_merge_method,
            memory_merge_method,
            base_branch=base_branch,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Strictly validate a Project Harness config, resolve its merge "
            "policy against caller-supplied capabilities, or render an exact "
            "schema-v1 to schema-v2 migration without writing the file."
        )
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Config path, or - to read UTF-8 content from standard input.",
    )
    parser.add_argument(
        "--available-method",
        action="append",
        dest="available_methods",
        help=(
            "Authoritatively available merge method; repeat for every method. "
            "When supplied, also resolve the merge policy."
        ),
    )
    parser.add_argument(
        "--migrate-v1",
        action="store_true",
        help=(
            "Render a canonical schema-v2 migration from an exact schema-v1 "
            "source without writing any file."
        ),
    )
    parser.add_argument(
        "--product-method",
        help="Product PR merge method for --migrate-v1.",
    )
    parser.add_argument(
        "--memory-method",
        help="Project-memory PR merge method for --migrate-v1.",
    )
    return parser.parse_args()


def _emit_json(payload: Mapping[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def main() -> int:
    args = parse_args()
    try:
        text = (
            sys.stdin.read()
            if str(args.path) == "-"
            else args.path.read_text(encoding="utf-8")
        )
        config = parse_config(text)
    except (ConfigError, OSError, UnicodeError) as error:
        _emit_json({"outcome": "invalid", "config": None, "errors": [str(error)]})
        return 1

    errors = validate_config(config)
    if errors:
        _emit_json({"outcome": "invalid", "config": config, "errors": errors})
        return 1

    migration_method_argument_present = (
        args.product_method is not None or args.memory_method is not None
    )
    if args.migrate_v1:
        if args.available_methods is not None:
            _emit_json(
                {
                    "outcome": "invalid",
                    "config": config,
                    "errors": [
                        "--migrate-v1 cannot be combined with "
                        "--available-method"
                    ],
                }
            )
            return 1
        missing_arguments = [
            flag
            for flag, value in (
                ("--product-method", args.product_method),
                ("--memory-method", args.memory_method),
            )
            if value is None
        ]
        if missing_arguments:
            _emit_json(
                {
                    "outcome": "invalid",
                    "config": config,
                    "errors": [
                        "--migrate-v1 requires "
                        + " and ".join(missing_arguments)
                    ],
                }
            )
            return 1
        try:
            migration_config = build_v2_migration_payload(
                config,
                args.product_method,
                args.memory_method,
            )
            rendered_config = render_config(migration_config)
        except ConfigError as error:
            _emit_json(
                {
                    "outcome": "invalid",
                    "config": config,
                    "errors": [str(error)],
                }
            )
            return 1
        _emit_json(
            {
                "outcome": "migration-rendered",
                "source_config": config,
                "migration_config": migration_config,
                "rendered_config": rendered_config,
                "errors": [],
            }
        )
        return 0

    if migration_method_argument_present:
        _emit_json(
            {
                "outcome": "invalid",
                "config": config,
                "errors": [
                    "--product-method and --memory-method require --migrate-v1"
                ],
            }
        )
        return 1

    if args.available_methods is None:
        _emit_json({"outcome": "valid", "config": config, "errors": []})
        return 0

    result = resolve_merge_policy(config, args.available_methods)
    _emit_json({"config": config, **result})
    if result["outcome"] == "resolved":
        return 0
    if result["outcome"] == "migration-required":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
