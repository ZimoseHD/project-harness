#!/usr/bin/env python3
"""Pure, deterministic validation-impact classification for base drift.

The caller supplies already collected Git identities, a complete base delta,
promotion-patch identities, and a validation dependency inventory.  This
module performs no repository reads, network operations, authorization
decisions, or mutations.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Literal, TypedDict


ImpactMode = Literal["reuse", "incremental", "full", "blocked"]
ChangedFileStatus = Literal["added", "modified", "removed", "renamed"]

_EXPECTED_INPUT_FIELDS = frozenset(
    {
        "prior_base_sha",
        "prior_head_sha",
        "current_base_sha",
        "current_head_sha",
        "base_relation",
        "current_base_is_head_ancestor",
        "base_delta",
        "prior_promotion_patch",
        "current_promotion_patch",
        "prior_promotion_patch_sha256",
        "current_promotion_patch_sha256",
        "validation_inventory_complete",
        "validation_inventory",
        "global_trigger_paths_complete",
        "global_trigger_paths",
    }
)
_EXPECTED_BASE_DELTA_FIELDS = frozenset({"complete", "truncated", "files"})
_EXPECTED_CHANGED_FILE_FIELDS = frozenset(
    {
        "status",
        "old_path",
        "new_path",
        "old_blob_sha",
        "new_blob_sha",
    }
)
_EXPECTED_VALIDATION_FIELDS = frozenset({"id", "dependency_paths", "global"})
_CHANGED_FILE_STATUSES = frozenset({"added", "modified", "removed", "renamed"})
_GIT_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z", re.ASCII)
_SHA256 = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_VALIDATION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z", re.ASCII)


class ChangedFileIdentity(TypedDict):
    """One complete changed-file identity from ``prior_base..current_base``."""

    status: ChangedFileStatus
    old_path: str | None
    new_path: str | None
    old_blob_sha: str | None
    new_blob_sha: str | None


class BaseDelta(TypedDict):
    """A complete, non-truncated set of base-drift file identities."""

    complete: bool
    truncated: bool
    files: list[ChangedFileIdentity]


class PromotionPatch(TypedDict):
    """A complete base-to-head promotion patch identity."""

    complete: bool
    truncated: bool
    files: list[ChangedFileIdentity]


# One validation and its fnmatch-style repository path dependencies.
ValidationInventoryItem = TypedDict(
    "ValidationInventoryItem",
    {
        "id": str,
        "dependency_paths": list[str],
        "global": bool,
    },
)


class ValidationImpactInput(TypedDict):
    """Canonical inputs required to classify validation evidence impact."""

    prior_base_sha: str
    prior_head_sha: str
    current_base_sha: str
    current_head_sha: str
    base_relation: str
    current_base_is_head_ancestor: bool
    base_delta: BaseDelta
    prior_promotion_patch: PromotionPatch
    current_promotion_patch: PromotionPatch
    prior_promotion_patch_sha256: str
    current_promotion_patch_sha256: str
    validation_inventory_complete: bool
    validation_inventory: list[ValidationInventoryItem]
    global_trigger_paths_complete: bool
    global_trigger_paths: list[str]


class ValidationImpactResult(TypedDict):
    """Deterministic impact classification and evidence binding."""

    impact_mode: ImpactMode
    invalidated_validation_ids: list[str]
    retained_validation_ids: list[str]
    reason_codes: list[str]
    input_sha256: str


def canonical_input_sha256(input_data: Mapping[str, object]) -> str:
    """Return the SHA-256 of compact, key-sorted UTF-8 JSON input.

    The input must be JSON-compatible and all mapping keys must be strings.
    Array order remains significant; callers should therefore preserve the
    order of their captured changed-file and inventory evidence.
    """

    def validate_json_value(value: object, path: str) -> None:
        if value is None or isinstance(value, (str, bool, int, float)):
            return
        if isinstance(value, Mapping):
            for key, nested in value.items():
                if not isinstance(key, str):
                    raise TypeError(f"{path}: every mapping key must be a string")
                validate_json_value(nested, f"{path}.{key}")
            return
        if isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            for index, nested in enumerate(value):
                validate_json_value(nested, f"{path}[{index}]")
            return
        raise TypeError(f"{path}: value is not JSON-compatible")

    if not isinstance(input_data, Mapping):
        raise TypeError("validation-impact input must be a mapping")
    validate_json_value(input_data, "input")
    try:
        canonical = json.dumps(
            input_data,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "validation-impact input must be finite canonical JSON"
        ) from error
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def promotion_patch_sha256(patch: Mapping[str, object]) -> str:
    """Return the canonical identity of one complete base-to-head patch.

    File order from the transport is irrelevant. The canonical order is the
    tuple ``(status, old_path, new_path, old_blob_sha, new_blob_sha)`` with
    null values represented as empty strings for sorting; the hashed JSON
    retains the original nulls and exact field names.
    """
    reasons: list[str] = []
    _parse_base_delta(patch, reasons)
    if reasons:
        raise ValueError(
            "invalid promotion patch identity: " + "; ".join(reasons)
        )

    files = patch["files"]
    assert _is_sequence(files)
    normalized_files = [dict(file_identity) for file_identity in files]
    normalized_files.sort(
        key=lambda item: (
            item["status"],
            item["old_path"] or "",
            item["new_path"] or "",
            item["old_blob_sha"] or "",
            item["new_blob_sha"] or "",
        )
    )
    canonical_patch = {
        "complete": True,
        "truncated": False,
        "files": normalized_files,
    }
    return canonical_input_sha256(canonical_patch)


def _append_reason(reasons: list[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def _is_sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _is_git_oid(value: object) -> bool:
    return isinstance(value, str) and _GIT_OID.fullmatch(value) is not None


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and _SHA256.fullmatch(value) is not None


def _is_repo_path_pattern(value: object) -> bool:
    """Accept only already-normalized, relative POSIX fnmatch patterns."""
    if (
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or value.endswith("/")
        or "\\" in value
    ):
        return False
    components = value.split("/")
    return all(component not in {"", ".", ".."} for component in components)


def _exact_fields(value: Mapping[object, object], expected: frozenset[str]) -> bool:
    return all(isinstance(key, str) for key in value) and set(value) == expected


def _validate_changed_file(
    value: object,
    reasons: list[str],
) -> tuple[str, ...] | None:
    """Validate one identity and return every old/new path it touches."""
    if not isinstance(value, Mapping) or not _exact_fields(
        value, _EXPECTED_CHANGED_FILE_FIELDS
    ):
        _append_reason(reasons, "changed-file-identity-invalid")
        return None

    status = value.get("status")
    old_path = value.get("old_path")
    new_path = value.get("new_path")
    old_blob = value.get("old_blob_sha")
    new_blob = value.get("new_blob_sha")

    if not isinstance(status, str) or status not in _CHANGED_FILE_STATUSES:
        _append_reason(reasons, "changed-file-status-unknown")
        return None

    old_path_valid = old_path is None or _is_repo_path_pattern(old_path)
    new_path_valid = new_path is None or _is_repo_path_pattern(new_path)
    if not old_path_valid or not new_path_valid:
        _append_reason(reasons, "changed-file-path-invalid")
        return None

    if status == "added":
        shape_is_valid = (
            old_path is None
            and old_blob is None
            and isinstance(new_path, str)
            and _is_git_oid(new_blob)
        )
    elif status == "removed":
        shape_is_valid = (
            isinstance(old_path, str)
            and _is_git_oid(old_blob)
            and new_path is None
            and new_blob is None
        )
    elif status == "modified":
        shape_is_valid = (
            isinstance(old_path, str)
            and old_path == new_path
            and _is_git_oid(old_blob)
            and _is_git_oid(new_blob)
        )
    else:
        shape_is_valid = (
            isinstance(old_path, str)
            and isinstance(new_path, str)
            and old_path != new_path
            and _is_git_oid(old_blob)
            and _is_git_oid(new_blob)
        )

    if not shape_is_valid:
        _append_reason(reasons, "changed-file-blob-or-shape-missing")
        return None

    return tuple(
        path for path in (old_path, new_path) if isinstance(path, str)
    )


def _parse_base_delta(
    value: object,
    reasons: list[str],
) -> list[tuple[str, ...]]:
    if not isinstance(value, Mapping) or not _exact_fields(
        value, _EXPECTED_BASE_DELTA_FIELDS
    ):
        _append_reason(reasons, "base-delta-schema-invalid")
        return []

    complete = value.get("complete")
    truncated = value.get("truncated")
    files = value.get("files")

    if complete is not True:
        _append_reason(
            reasons,
            "base-delta-incomplete"
            if complete is False
            else "base-delta-completeness-unknown",
        )
    if truncated is not False:
        _append_reason(
            reasons,
            "base-delta-truncated"
            if truncated is True
            else "base-delta-truncation-unknown",
        )
    if not _is_sequence(files):
        _append_reason(reasons, "base-delta-files-unknown")
        return []

    changed_paths: list[tuple[str, ...]] = []
    seen_identities: set[tuple[object, ...]] = set()
    seen_old_paths: set[str] = set()
    seen_new_paths: set[str] = set()
    for item in files:
        paths = _validate_changed_file(item, reasons)
        if paths is not None:
            assert isinstance(item, Mapping)
            identity = tuple(
                item.get(field)
                for field in (
                    "status",
                    "old_path",
                    "new_path",
                    "old_blob_sha",
                    "new_blob_sha",
                )
            )
            if identity in seen_identities:
                _append_reason(reasons, "changed-file-identity-duplicate")
                continue
            seen_identities.add(identity)
            old_path = item.get("old_path")
            new_path = item.get("new_path")
            duplicate_side = False
            if isinstance(old_path, str):
                if old_path in seen_old_paths:
                    _append_reason(
                        reasons, "changed-file-old-path-duplicate"
                    )
                    duplicate_side = True
                seen_old_paths.add(old_path)
            if isinstance(new_path, str):
                if new_path in seen_new_paths:
                    _append_reason(
                        reasons, "changed-file-new-path-duplicate"
                    )
                    duplicate_side = True
                seen_new_paths.add(new_path)
            if duplicate_side:
                continue
            changed_paths.append(paths)
    return changed_paths


def _parse_validation_inventory(
    value: object,
    reasons: list[str],
) -> list[tuple[str, tuple[str, ...], bool]]:
    if not _is_sequence(value):
        _append_reason(reasons, "validation-inventory-invalid")
        return []

    parsed: list[tuple[str, tuple[str, ...], bool]] = []
    seen_ids: set[str] = set()
    for item in value:
        if not isinstance(item, Mapping) or not _exact_fields(
            item, _EXPECTED_VALIDATION_FIELDS
        ):
            _append_reason(reasons, "validation-inventory-invalid")
            continue

        validation_id = item.get("id")
        dependency_paths = item.get("dependency_paths")
        is_global = item.get("global")
        item_valid = True

        if (
            not isinstance(validation_id, str)
            or _VALIDATION_ID.fullmatch(validation_id) is None
        ):
            _append_reason(reasons, "validation-id-invalid")
            item_valid = False
        elif validation_id in seen_ids:
            _append_reason(reasons, "validation-id-duplicate")
            item_valid = False

        if not _is_sequence(dependency_paths) or any(
            not _is_repo_path_pattern(pattern) for pattern in dependency_paths
        ):
            _append_reason(reasons, "validation-dependency-path-invalid")
            item_valid = False

        if not isinstance(is_global, bool):
            _append_reason(reasons, "validation-global-flag-unknown")
            item_valid = False

        if item_valid:
            assert isinstance(validation_id, str)
            assert _is_sequence(dependency_paths)
            seen_ids.add(validation_id)
            parsed.append(
                (
                    validation_id,
                    tuple(str(pattern) for pattern in dependency_paths),
                    is_global,
                )
            )
    return parsed


def _parse_path_patterns(
    value: object,
    reasons: list[str],
) -> tuple[str, ...]:
    if not _is_sequence(value) or any(
        not _is_repo_path_pattern(pattern) for pattern in value
    ):
        _append_reason(reasons, "global-trigger-path-invalid")
        return ()
    return tuple(str(pattern) for pattern in value)


def _any_path_matches(
    changed_paths: Sequence[tuple[str, ...]],
    patterns: Sequence[str],
) -> bool:
    return any(
        fnmatch.fnmatchcase(path, pattern)
        for identity_paths in changed_paths
        for path in identity_paths
        for pattern in patterns
    )


def _result(
    *,
    mode: ImpactMode,
    invalidated: Sequence[str],
    retained: Sequence[str],
    reasons: Sequence[str],
    input_sha256: str,
) -> ValidationImpactResult:
    return {
        "impact_mode": mode,
        "invalidated_validation_ids": sorted(invalidated),
        "retained_validation_ids": sorted(retained),
        "reason_codes": list(reasons),
        "input_sha256": input_sha256,
    }


def assess_validation_impact(
    input_data: Mapping[str, object],
) -> ValidationImpactResult:
    """Classify which prior validation results survive a base advance.

    Structural ambiguity, unknown ancestry, a non-fast-forward base relation,
    an incomplete/truncated delta, or an incomplete file/blob identity blocks
    classification.  Once those identity prerequisites are sound:

    * a changed promotion patch, a global-trigger match, or an explicitly
      incomplete dependency inventory requires a full validation run;
    * matching only some validation dependencies permits an incremental run;
    * an equivalent patch with no dependency match permits evidence reuse.

    Rename and deletion entries are matched against every non-null old and new
    path, so dependencies cannot be bypassed by changing path identity.
    """
    input_digest = canonical_input_sha256(input_data)
    blockers: list[str] = []

    if not _exact_fields(input_data, _EXPECTED_INPUT_FIELDS):
        _append_reason(blockers, "input-schema-invalid")

    for field in (
        "prior_base_sha",
        "prior_head_sha",
        "current_base_sha",
        "current_head_sha",
    ):
        if not _is_git_oid(input_data.get(field)):
            _append_reason(blockers, "commit-identity-unknown")

    base_relation = input_data.get("base_relation")
    if base_relation != "fast-forward":
        _append_reason(
            blockers,
            "base-relation-unknown"
            if not isinstance(base_relation, str) or base_relation == "unknown"
            else "base-not-fast-forward",
        )

    ancestry = input_data.get("current_base_is_head_ancestor")
    if ancestry is not True:
        _append_reason(
            blockers,
            "current-base-not-head-ancestor"
            if ancestry is False
            else "current-base-ancestry-unknown",
        )

    changed_paths = _parse_base_delta(input_data.get("base_delta"), blockers)

    prior_patch = input_data.get("prior_promotion_patch_sha256")
    current_patch = input_data.get("current_promotion_patch_sha256")
    if not _is_sha256(prior_patch) or not _is_sha256(current_patch):
        _append_reason(blockers, "promotion-patch-identity-unknown")
    for label in ("prior", "current"):
        patch_records = input_data.get(f"{label}_promotion_patch")
        try:
            if not isinstance(patch_records, Mapping):
                raise ValueError("patch must be a mapping")
            derived_digest = promotion_patch_sha256(patch_records)
        except ValueError:
            _append_reason(blockers, "promotion-patch-records-invalid")
            continue
        supplied_digest = input_data.get(
            f"{label}_promotion_patch_sha256"
        )
        if _is_sha256(supplied_digest) and supplied_digest != derived_digest:
            _append_reason(
                blockers,
                f"{label}-promotion-patch-digest-mismatch",
            )

    inventory_complete = input_data.get("validation_inventory_complete")
    if not isinstance(inventory_complete, bool):
        _append_reason(blockers, "validation-inventory-completeness-unknown")

    inventory = _parse_validation_inventory(
        input_data.get("validation_inventory"), blockers
    )
    global_trigger_paths_complete = input_data.get(
        "global_trigger_paths_complete"
    )
    if not isinstance(global_trigger_paths_complete, bool):
        _append_reason(blockers, "global-trigger-completeness-unknown")
    global_trigger_paths = _parse_path_patterns(
        input_data.get("global_trigger_paths"), blockers
    )

    if blockers:
        return _result(
            mode="blocked",
            invalidated=(),
            retained=(),
            reasons=blockers,
            input_sha256=input_digest,
        )

    validation_ids = [item[0] for item in inventory]
    full_reasons: list[str] = []
    if prior_patch != current_patch:
        _append_reason(full_reasons, "promotion-patch-changed")
    if inventory_complete is False:
        _append_reason(full_reasons, "validation-inventory-incomplete")
    if global_trigger_paths_complete is False:
        _append_reason(full_reasons, "global-trigger-inventory-incomplete")
    if any(
        not dependencies and not is_global
        for _, dependencies, is_global in inventory
    ):
        _append_reason(full_reasons, "validation-dependency-mapping-incomplete")
    if _any_path_matches(changed_paths, global_trigger_paths):
        _append_reason(full_reasons, "global-trigger-path-matched")

    if full_reasons:
        return _result(
            mode="full",
            invalidated=validation_ids,
            retained=(),
            reasons=full_reasons,
            input_sha256=input_digest,
        )

    invalidated = {
        validation_id
        for validation_id, dependencies, is_global in inventory
        if (is_global and bool(changed_paths))
        or _any_path_matches(changed_paths, dependencies)
    }
    retained = set(validation_ids) - invalidated

    if not invalidated:
        return _result(
            mode="reuse",
            invalidated=(),
            retained=retained,
            reasons=("no-validation-dependency-matched",),
            input_sha256=input_digest,
        )
    if retained:
        return _result(
            mode="incremental",
            invalidated=invalidated,
            retained=retained,
            reasons=("validation-dependency-subset-matched",),
            input_sha256=input_digest,
        )
    return _result(
        mode="full",
        invalidated=invalidated,
        retained=(),
        reasons=("all-validation-dependencies-matched",),
        input_sha256=input_digest,
    )
