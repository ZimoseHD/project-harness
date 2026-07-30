#!/usr/bin/env python3
"""Build and validate operation-local Project Harness evidence bundles.

The helpers in this module are deterministic and have no filesystem or network
side effects.  A bundle carries normalized evidence payloads for one semantic
round; it is a transport optimization, not durable workflow authority.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import copy
from hashlib import sha256
import json
import math
from pathlib import PurePosixPath
import re
from typing import Any
from urllib.parse import urlsplit


BUNDLE_SCHEMA_VERSION = 1

SCOPES = frozenset({"implementation", "closeout", "context-promotion"})
TOP_LEVEL_FIELDS = frozenset(
    {
        "bundle_schema_version",
        "scope",
        "semantic_round_key",
        "provenance",
        "completeness",
        "completeness_bindings",
        "semantic_snapshot",
        "liveness_snapshot",
        "payloads",
        "bundle_sha256",
    }
)
PROVENANCE_FIELDS = frozenset(
    {
        "authenticated_actor_login",
        "authenticated_actor_id",
        "mutation_author_login",
        "transport_family",
    }
)
TRANSPORT_FAMILIES = frozenset({"github-app", "gh"})
COMPLETENESS_FIELDS = frozenset(
    {
        "issue_body",
        "workflow_comments",
        "related_pr_search",
        "product_pr",
        "authority_sources",
        "memory_pr",
        "diff",
        "checks",
    }
)
PAYLOAD_FIELDS = frozenset(
    {
        "id",
        "kind",
        "locator",
        "snapshot_class",
        "source_identity",
        "content_sha256",
        "normalized_content",
    }
)
PAYLOAD_IDENTITY_FIELDS = frozenset(
    {"locator", "snapshot_class", "source_identity", "content_sha256"}
)
SNAPSHOT_CLASSES = frozenset({"semantic", "liveness"})

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SOURCE_IDENTITY_RE = re.compile(r"^content-sha256:([0-9a-f]{64})$")
_WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _normalize_content(content: str) -> str:
    """Use LF line endings and exactly one trailing newline."""
    return content.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"


def _content_sha256(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _bundle_digest(bundle: Mapping[str, object]) -> str:
    unsigned = {key: value for key, value in bundle.items() if key != "bundle_sha256"}
    return _content_sha256(_canonical_json(unsigned))


def _semantic_round_digest(round_binding: Mapping[str, object]) -> str:
    return _content_sha256(_canonical_json(round_binding))


def _exact_fields(
    value: Mapping[str, object],
    expected: frozenset[str],
    path: str,
    errors: list[str],
) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(
        actual - expected,
        key=lambda field: str(field),
    )
    if missing:
        errors.append(f"{path} is missing fields: {', '.join(missing)}")
    if unexpected:
        displayed = [
            field if isinstance(field, str) else repr(field)
            for field in unexpected
        ]
        errors.append(f"{path} has unexpected fields: {', '.join(displayed)}")


def _nonempty_string(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")


def _valid_locator(locator: str) -> bool:
    """Accept HTTPS URLs, repo-relative POSIX paths, and explicit git locators."""
    if not locator or locator != locator.strip() or "\n" in locator or "\r" in locator:
        return False

    parsed = urlsplit(locator)
    if parsed.scheme:
        if parsed.scheme == "https":
            return bool(parsed.netloc)
        if parsed.scheme == "git":
            if locator.startswith("git://"):
                return bool(parsed.netloc)
            git_target = locator.removeprefix("git:")
            return (
                bool(git_target)
                and not git_target.startswith(("/", "\\", "~"))
                and not _WINDOWS_ABSOLUTE_RE.match(git_target)
            )
        return False

    if (
        locator.startswith(("/", "\\", "~"))
        or _WINDOWS_ABSOLUTE_RE.match(locator)
        or "\\" in locator
    ):
        return False

    path = PurePosixPath(locator)
    return (
        not path.is_absolute()
        and str(path) not in {"", "."}
        and ".." not in path.parts
    )


def _validate_json_value(value: object, path: str, errors: list[str]) -> None:
    """Reject values outside the unambiguous JSON data model."""
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            errors.append(f"{path} must not contain non-finite numbers")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"{path} keys must be strings")
                continue
            _validate_json_value(item, f"{path}.{key}", errors)
        return
    errors.append(f"{path} contains a non-JSON value")


def _validate_bundle(
    bundle: object,
    *,
    require_bundle_digest: bool,
    required_components: frozenset[str] = frozenset(),
) -> list[str]:
    errors: list[str] = []
    if not isinstance(bundle, Mapping):
        return ["bundle must be a mapping"]

    expected_top_level = (
        TOP_LEVEL_FIELDS
        if require_bundle_digest
        else TOP_LEVEL_FIELDS - {"bundle_sha256"}
    )
    _exact_fields(bundle, expected_top_level, "bundle", errors)

    schema_version = bundle.get("bundle_schema_version")
    if (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
        or schema_version != BUNDLE_SCHEMA_VERSION
    ):
        errors.append(
            "bundle.bundle_schema_version must equal "
            f"{BUNDLE_SCHEMA_VERSION}, got {schema_version!r}"
        )

    scope = bundle.get("scope")
    if not isinstance(scope, str) or scope not in SCOPES:
        errors.append(
            "bundle.scope must be implementation, closeout, or context-promotion"
        )

    semantic_round_key = bundle.get("semantic_round_key")
    if not isinstance(semantic_round_key, str) or not _SHA256_RE.fullmatch(
        semantic_round_key
    ):
        errors.append("bundle.semantic_round_key must be a lowercase SHA-256")

    provenance = bundle.get("provenance")
    if not isinstance(provenance, Mapping):
        errors.append("bundle.provenance must be a mapping")
    else:
        _exact_fields(provenance, PROVENANCE_FIELDS, "bundle.provenance", errors)
        _nonempty_string(
            provenance.get("authenticated_actor_login"),
            "bundle.provenance.authenticated_actor_login",
            errors,
        )
        actor_id = provenance.get("authenticated_actor_id")
        valid_numeric_id = (
            isinstance(actor_id, int)
            and not isinstance(actor_id, bool)
            and actor_id > 0
        )
        valid_opaque_id = isinstance(actor_id, str) and bool(actor_id.strip())
        if not valid_numeric_id and not valid_opaque_id:
            errors.append(
                "bundle.provenance.authenticated_actor_id must be a positive "
                "integer or non-empty opaque string"
            )
        _nonempty_string(
            provenance.get("mutation_author_login"),
            "bundle.provenance.mutation_author_login",
            errors,
        )
        transport_family = provenance.get("transport_family")
        if (
            not isinstance(transport_family, str)
            or transport_family not in TRANSPORT_FAMILIES
        ):
            errors.append(
                "bundle.provenance.transport_family must be github-app or gh"
            )

    completeness = bundle.get("completeness")
    if not isinstance(completeness, Mapping):
        errors.append("bundle.completeness must be a mapping")
    else:
        _exact_fields(
            completeness, COMPLETENESS_FIELDS, "bundle.completeness", errors
        )
        for field in sorted(COMPLETENESS_FIELDS):
            value = completeness.get(field)
            if not isinstance(value, bool):
                errors.append(
                    f"bundle.completeness.{field} must be a boolean"
                )
            elif field in required_components and value is not True:
                errors.append(
                    f"bundle.completeness.{field} is required but incomplete"
                )

    for field in ("semantic_snapshot", "liveness_snapshot"):
        snapshot = bundle.get(field)
        if not isinstance(snapshot, Mapping):
            errors.append(f"bundle.{field} must be a mapping")
        else:
            _validate_json_value(snapshot, f"bundle.{field}", errors)

    payloads = bundle.get("payloads")
    seen_ids: set[str] = set()
    payload_identities: dict[str, dict[str, str]] = {}
    payload_classes: dict[str, str] = {}
    if not isinstance(payloads, list):
        errors.append("bundle.payloads must be a list")
    else:
        for index, payload in enumerate(payloads):
            path = f"bundle.payloads[{index}]"
            if not isinstance(payload, Mapping):
                errors.append(f"{path} must be a mapping")
                continue
            _exact_fields(payload, PAYLOAD_FIELDS, path, errors)

            payload_id = payload.get("id")
            _nonempty_string(payload_id, f"{path}.id", errors)
            if isinstance(payload_id, str) and payload_id:
                if payload_id in seen_ids:
                    errors.append(f"{path}.id duplicates payload id {payload_id!r}")
                seen_ids.add(payload_id)

            _nonempty_string(payload.get("kind"), f"{path}.kind", errors)

            locator = payload.get("locator")
            if not isinstance(locator, str) or not _valid_locator(locator):
                errors.append(
                    f"{path}.locator must be an HTTPS URL, repo-relative path, "
                    "or git locator, and must not be an absolute local path"
                )

            snapshot_class = payload.get("snapshot_class")
            if (
                not isinstance(snapshot_class, str)
                or snapshot_class not in SNAPSHOT_CLASSES
            ):
                errors.append(
                    f"{path}.snapshot_class must be semantic or liveness"
                )

            source_identity = payload.get("source_identity")
            _nonempty_string(
                source_identity,
                f"{path}.source_identity",
                errors,
            )

            content = payload.get("normalized_content")
            if not isinstance(content, str):
                errors.append(f"{path}.normalized_content must be a string")
            else:
                if _normalize_content(content) != content:
                    errors.append(
                        f"{path}.normalized_content must use LF and exactly one "
                        "trailing newline"
                    )
                content_digest = payload.get("content_sha256")
                if not isinstance(content_digest, str) or not _SHA256_RE.fullmatch(
                    content_digest
                ):
                    errors.append(
                        f"{path}.content_sha256 must be a lowercase SHA-256"
                    )
                elif content_digest != _content_sha256(content):
                    errors.append(
                        f"{path}.content_sha256 does not match normalized_content"
                    )
                if (
                    isinstance(source_identity, str)
                    and isinstance(content_digest, str)
                    and _SHA256_RE.fullmatch(content_digest)
                    and (
                        _SOURCE_IDENTITY_RE.fullmatch(source_identity) is None
                        or source_identity
                        != f"content-sha256:{content_digest}"
                    )
                ):
                    errors.append(
                        f"{path}.source_identity must bind content_sha256"
                    )
            if (
                isinstance(payload_id, str)
                and payload_id
                and isinstance(locator, str)
                and _valid_locator(locator)
                and isinstance(snapshot_class, str)
                and snapshot_class in SNAPSHOT_CLASSES
                and isinstance(source_identity, str)
                and source_identity.strip()
                and isinstance(payload.get("content_sha256"), str)
                and _SHA256_RE.fullmatch(payload["content_sha256"])
            ):
                payload_classes[payload_id] = snapshot_class
                payload_identities[payload_id] = {
                    "locator": locator,
                    "snapshot_class": snapshot_class,
                    "source_identity": source_identity,
                    "content_sha256": payload["content_sha256"],
                }

    for snapshot_name, snapshot_class in (
        ("semantic_snapshot", "semantic"),
        ("liveness_snapshot", "liveness"),
    ):
        snapshot = bundle.get(snapshot_name)
        if not isinstance(snapshot, Mapping):
            continue
        identities = snapshot.get("payload_identities")
        if not isinstance(identities, Mapping):
            errors.append(
                f"bundle.{snapshot_name}.payload_identities must be a mapping"
            )
            continue
        expected_ids = {
            payload_id
            for payload_id, actual_class in payload_classes.items()
            if actual_class == snapshot_class
        }
        actual_ids = {
            payload_id
            for payload_id in identities
            if isinstance(payload_id, str)
        }
        invalid_identity_ids = [
            repr(payload_id)
            for payload_id in identities
            if not isinstance(payload_id, str)
        ]
        if invalid_identity_ids:
            errors.append(
                f"bundle.{snapshot_name}.payload_identities has non-string IDs: "
                + ", ".join(sorted(invalid_identity_ids))
            )
        if actual_ids != expected_ids:
            missing = sorted(expected_ids - actual_ids)
            unexpected = sorted(actual_ids - expected_ids)
            if missing:
                errors.append(
                    f"bundle.{snapshot_name}.payload_identities is missing IDs: "
                    + ", ".join(missing)
                )
            if unexpected:
                errors.append(
                    f"bundle.{snapshot_name}.payload_identities has unexpected IDs: "
                    + ", ".join(unexpected)
                )
        for payload_id, identity in identities.items():
            path = (
                f"bundle.{snapshot_name}.payload_identities.{payload_id}"
            )
            if not isinstance(payload_id, str):
                continue
            if not isinstance(identity, Mapping):
                errors.append(f"{path} must be a mapping")
                continue
            _exact_fields(identity, PAYLOAD_IDENTITY_FIELDS, path, errors)
            if payload_id in payload_identities and identity != payload_identities[
                payload_id
            ]:
                errors.append(
                    f"{path} does not match the bound payload identity"
                )

    semantic_snapshot = bundle.get("semantic_snapshot")
    round_binding = (
        semantic_snapshot.get("round_binding")
        if isinstance(semantic_snapshot, Mapping)
        else None
    )
    if (
        isinstance(round_binding, Mapping)
        and isinstance(semantic_round_key, str)
        and _SHA256_RE.fullmatch(semantic_round_key)
    ):
        try:
            expected_round_key = _semantic_round_digest(round_binding)
        except (TypeError, ValueError):
            expected_round_key = None
        if (
            expected_round_key is not None
            and semantic_round_key != expected_round_key
        ):
            errors.append(
                "bundle.semantic_round_key does not match "
                "semantic_snapshot.round_binding"
            )
    elif isinstance(semantic_snapshot, Mapping):
        errors.append(
            "bundle.semantic_snapshot.round_binding must be a mapping"
        )

    completeness_bindings = bundle.get("completeness_bindings")
    if not isinstance(completeness_bindings, Mapping):
        errors.append("bundle.completeness_bindings must be a mapping")
    else:
        _exact_fields(
            completeness_bindings,
            COMPLETENESS_FIELDS,
            "bundle.completeness_bindings",
            errors,
        )
        for field in sorted(COMPLETENESS_FIELDS):
            binding = completeness_bindings.get(field)
            path = f"bundle.completeness_bindings.{field}"
            if (
                not isinstance(binding, list)
                or any(
                    not isinstance(payload_id, str) or not payload_id
                    for payload_id in binding
                )
                or len(set(binding)) != len(binding)
            ):
                errors.append(
                    f"{path} must be a unique list of non-empty payload IDs"
                )
                continue
            missing_payloads = sorted(set(binding) - seen_ids)
            if missing_payloads:
                errors.append(
                    f"{path} references unknown payload IDs: "
                    + ", ".join(missing_payloads)
                )
            component_complete = (
                completeness.get(field)
                if isinstance(completeness, Mapping)
                else None
            )
            if component_complete is True and not binding:
                errors.append(
                    f"{path} must bind at least one completeness payload"
                )
            if component_complete is False and binding:
                errors.append(
                    f"{path} must be empty while the component is incomplete"
                )

    if require_bundle_digest:
        bundle_digest = bundle.get("bundle_sha256")
        if not isinstance(bundle_digest, str) or not _SHA256_RE.fullmatch(
            bundle_digest
        ):
            errors.append("bundle.bundle_sha256 must be a lowercase SHA-256")
        else:
            try:
                expected_digest = _bundle_digest(bundle)
            except (TypeError, ValueError):
                expected_digest = None
            if expected_digest is not None and bundle_digest != expected_digest:
                errors.append(
                    "bundle.bundle_sha256 does not match the canonical bundle"
                )

    _validate_json_value(bundle, "bundle", errors)
    try:
        _canonical_json(bundle)
    except (TypeError, ValueError):
        errors.append("bundle must be canonical-JSON serializable")

    return errors


def derive_component_identities(
    manifest: Mapping[str, Any],
) -> dict[str, dict[str, dict[str, str]]]:
    """Derive the outer component map from original transport payloads.

    This operates on the pre-Bundle manifest so a consumer does not derive its
    expected identities from the Bundle it is about to validate.
    """
    if not isinstance(manifest, Mapping):
        raise ValueError("evidence component manifest must be a mapping")
    payloads = manifest.get("payloads")
    bindings = manifest.get("completeness_bindings")
    if not isinstance(payloads, list) or not isinstance(bindings, Mapping):
        raise ValueError(
            "component identity derivation requires payloads and "
            "completeness_bindings"
        )
    _binding_errors: list[str] = []
    _exact_fields(
        bindings,
        COMPLETENESS_FIELDS,
        "completeness_bindings",
        _binding_errors,
    )
    if _binding_errors:
        raise ValueError("; ".join(_binding_errors))

    identities: dict[str, dict[str, str]] = {}
    for index, payload in enumerate(payloads):
        path = f"payloads[{index}]"
        if not isinstance(payload, Mapping):
            raise ValueError(f"{path} must be a mapping")
        payload_id = payload.get("id")
        kind = payload.get("kind")
        locator = payload.get("locator")
        snapshot_class = payload.get("snapshot_class")
        content = payload.get("normalized_content")
        if not isinstance(payload_id, str) or not payload_id:
            raise ValueError(f"{path}.id must be a non-empty string")
        if payload_id in identities:
            raise ValueError(f"{path}.id duplicates {payload_id!r}")
        if not isinstance(kind, str) or not kind:
            raise ValueError(f"{path}.kind must be a non-empty string")
        if not isinstance(locator, str) or not _valid_locator(locator):
            raise ValueError(f"{path}.locator is invalid")
        if (
            not isinstance(snapshot_class, str)
            or snapshot_class not in SNAPSHOT_CLASSES
        ):
            raise ValueError(f"{path}.snapshot_class is invalid")
        if not isinstance(content, str):
            raise ValueError(f"{path}.normalized_content must be a string")
        normalized = _normalize_content(content)
        content_digest = _content_sha256(normalized)
        identities[payload_id] = {
            "locator": locator,
            "snapshot_class": snapshot_class,
            "source_identity": f"content-sha256:{content_digest}",
            "content_sha256": content_digest,
        }

    result: dict[str, dict[str, dict[str, str]]] = {}
    for component in sorted(COMPLETENESS_FIELDS):
        payload_ids = bindings.get(component)
        if (
            not isinstance(payload_ids, list)
            or any(
                not isinstance(payload_id, str) or not payload_id
                for payload_id in payload_ids
            )
            or len(set(payload_ids)) != len(payload_ids)
        ):
            raise ValueError(
                f"completeness_bindings.{component} must be a unique "
                "payload-ID list"
            )
        missing = sorted(set(payload_ids) - set(identities))
        if missing:
            raise ValueError(
                f"completeness_bindings.{component} references unknown IDs: "
                + ", ".join(missing)
            )
        result[component] = {
            payload_id: copy.deepcopy(identities[payload_id])
            for payload_id in sorted(payload_ids)
        }
    return result


def build_bundle(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return a normalized, independently digest-bound copy of ``manifest``.

    ``semantic_round_key``, ``bundle_sha256``, and each payload
    ``content_sha256`` are derived fields. Supplied values are replaced so
    callers cannot accidentally bind stale digests. A structurally valid
    manifest may have incomplete components; consumers declare their required
    components when validating a completed boundary.
    """
    if not isinstance(manifest, Mapping):
        raise ValueError("invalid evidence bundle manifest: manifest must be a mapping")

    bundle = copy.deepcopy(dict(manifest))
    bundle.pop("bundle_sha256", None)

    payloads = bundle.get("payloads")
    if isinstance(payloads, list):
        for payload in payloads:
            if not isinstance(payload, dict):
                continue
            content = payload.get("normalized_content")
            if isinstance(content, str):
                normalized = _normalize_content(content)
                payload["normalized_content"] = normalized
                content_digest = _content_sha256(normalized)
                payload["content_sha256"] = content_digest
                payload["source_identity"] = (
                    f"content-sha256:{content_digest}"
                )
        if all(
            isinstance(payload, dict)
            and isinstance(payload.get("id"), str)
            for payload in payloads
        ):
            payloads.sort(key=lambda payload: payload["id"])

    completeness_bindings = bundle.get("completeness_bindings")
    if isinstance(completeness_bindings, dict):
        for binding in completeness_bindings.values():
            if isinstance(binding, list) and all(
                isinstance(payload_id, str) for payload_id in binding
            ):
                binding.sort()

    for snapshot_name, snapshot_class in (
        ("semantic_snapshot", "semantic"),
        ("liveness_snapshot", "liveness"),
    ):
        snapshot = bundle.get(snapshot_name)
        if isinstance(snapshot, dict) and isinstance(payloads, list):
            snapshot["payload_identities"] = {
                payload["id"]: {
                    "locator": payload["locator"],
                    "snapshot_class": payload["snapshot_class"],
                    "source_identity": payload["source_identity"],
                    "content_sha256": payload["content_sha256"],
                }
                for payload in payloads
                if isinstance(payload, dict)
                and payload.get("snapshot_class") == snapshot_class
                and all(
                    isinstance(payload.get(field), str)
                    for field in (
                        "id",
                        "locator",
                        "source_identity",
                        "content_sha256",
                    )
                )
            }

    semantic_snapshot = bundle.get("semantic_snapshot")
    if isinstance(semantic_snapshot, Mapping):
        round_binding = semantic_snapshot.get("round_binding")
        try:
            if isinstance(round_binding, Mapping):
                bundle["semantic_round_key"] = _semantic_round_digest(
                    round_binding
                )
        except (TypeError, ValueError):
            pass

    errors = _validate_bundle(bundle, require_bundle_digest=False)
    if errors:
        raise ValueError("invalid evidence bundle manifest: " + "; ".join(errors))

    bundle["bundle_sha256"] = _bundle_digest(bundle)
    return bundle


def validate_bundle(
    bundle: object,
    required_components: Iterable[str] = (),
    *,
    expected_scope: str | None = None,
    expected_round_binding: Mapping[str, object] | None = None,
    expected_component_identities: (
        Mapping[str, Mapping[str, Mapping[str, str]]] | None
    ) = None,
) -> list[str]:
    """Return deterministic validation errors for one consumer boundary."""
    required = frozenset(required_components)
    unknown = sorted(required - COMPLETENESS_FIELDS)
    errors = [
        "required_components contains unknown fields: " + ", ".join(unknown)
    ] if unknown else []
    known_required = required & COMPLETENESS_FIELDS
    if known_required:
        if expected_scope is None:
            errors.append(
                "expected_scope is required when components are required"
            )
        if expected_round_binding is None:
            errors.append(
                "expected_round_binding is required when components are required"
            )
        if expected_component_identities is None:
            errors.append(
                "expected_component_identities is required when components "
                "are required"
            )
        elif not isinstance(expected_component_identities, Mapping):
            errors.append(
                "expected_component_identities must be a mapping"
            )
        else:
            missing_expected = sorted(
                known_required - set(expected_component_identities)
            )
            if missing_expected:
                errors.append(
                    "expected_component_identities is missing required "
                    "components: " + ", ".join(missing_expected)
                )
    errors.extend(
        _validate_bundle(
            bundle,
            require_bundle_digest=True,
            required_components=known_required,
        )
    )
    if expected_scope is not None:
        if not isinstance(expected_scope, str) or expected_scope not in SCOPES:
            errors.append("expected_scope is unknown")
        elif (
            not isinstance(bundle, Mapping)
            or bundle.get("scope") != expected_scope
        ):
            errors.append("bundle.scope does not match expected_scope")
    if expected_round_binding is not None:
        if not isinstance(expected_round_binding, Mapping):
            errors.append("expected_round_binding must be a mapping")
            expected_round_binding = None
    if expected_round_binding is not None:
        try:
            expected_round_key = _semantic_round_digest(
                expected_round_binding
            )
        except (TypeError, ValueError):
            errors.append(
                "expected_round_binding must be canonical-JSON serializable"
            )
        else:
            semantic_snapshot = (
                bundle.get("semantic_snapshot")
                if isinstance(bundle, Mapping)
                else None
            )
            if (
                not isinstance(semantic_snapshot, Mapping)
                or semantic_snapshot.get("round_binding")
                != expected_round_binding
                or bundle.get("semantic_round_key") != expected_round_key
            ):
                errors.append(
                    "bundle semantic round does not match the expected "
                    "delegation binding"
                )
    if isinstance(expected_component_identities, Mapping):
        unknown_components = sorted(
            repr(component)
            for component in expected_component_identities
            if (
                not isinstance(component, str)
                or component not in COMPLETENESS_FIELDS
            )
        )
        if unknown_components:
            errors.append(
                "expected_component_identities contains unknown components: "
                + ", ".join(unknown_components)
            )
        bindings = (
            bundle.get("completeness_bindings")
            if isinstance(bundle, Mapping)
            else None
        )
        current_payload_identities: dict[str, dict[str, str]] = {}
        payloads = (
            bundle.get("payloads") if isinstance(bundle, Mapping) else None
        )
        if isinstance(payloads, list):
            for payload in payloads:
                if not isinstance(payload, Mapping):
                    continue
                payload_id = payload.get("id")
                if (
                    isinstance(payload_id, str)
                    and all(
                        isinstance(payload.get(field), str)
                        for field in (
                            "locator",
                            "snapshot_class",
                            "source_identity",
                            "content_sha256",
                        )
                    )
                ):
                    current_payload_identities[payload_id] = {
                        "locator": payload["locator"],
                        "snapshot_class": payload["snapshot_class"],
                        "source_identity": payload["source_identity"],
                        "content_sha256": payload["content_sha256"],
                    }
        for component, expected_identities in (
            expected_component_identities.items()
        ):
            if component not in COMPLETENESS_FIELDS:
                continue
            if not isinstance(expected_identities, Mapping):
                errors.append(
                    f"expected_component_identities.{component} "
                    "must be a mapping"
                )
                continue
            actual_ids = (
                bindings.get(component)
                if isinstance(bindings, Mapping)
                else None
            )
            if not isinstance(actual_ids, list) or set(actual_ids) != set(
                expected_identities
            ):
                errors.append(
                    f"bundle completeness binding for {component} does not "
                    "match expected component payload IDs"
                )
                continue
            for payload_id, expected_identity in expected_identities.items():
                if (
                    not isinstance(expected_identity, Mapping)
                    or set(expected_identity) != PAYLOAD_IDENTITY_FIELDS
                    or current_payload_identities.get(payload_id)
                    != expected_identity
                ):
                    errors.append(
                        f"bundle payload identity for {component}/{payload_id} "
                        "does not match the current transport identity"
                    )
    return errors
