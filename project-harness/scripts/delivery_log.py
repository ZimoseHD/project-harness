#!/usr/bin/env python3
"""Pure validation and coverage guards for Project Harness delivery logs.

The functions in this module have no filesystem or network side effects.  They
validate one versioned observation, derive its durable transition identity, and
check whether caller-verified whole-comment bindings cover one exact delivery
branch through its manifest, finalization, and completion links.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import PurePosixPath
import re
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID


RECORD_KIND = "delivery-stage-observation"
LOG_SCHEMA_VERSION = 1
TIMING_SCOPE = "coordinator-wall"

OBSERVATION_KINDS = frozenset({"attempt", "boundary"})
TIMING_QUALITIES = frozenset({"measured", "reconstructed", "unknown"})
ACTIVITIES = frozenset(
    {
        "initial",
        "repair",
        "resume",
        "revalidate",
        "accept",
        "reconcile",
        "integrate",
        "recover",
        "propose",
        "revise",
        "confirm",
        "finalize",
        "closure-gate",
    }
)

BOUNDARY_STAGE_MAP: Mapping[str, str] = {
    "implementation-verified-draft": "implementation",
    "closeout-accepted-ready": "closeout",
    "product-merged": "product-integration",
    "context-proposal-reviewed": "context-promotion",
    "context-confirmed": "context-confirmation",
    "context-no-promotion-terminal": "context-promotion",
    "memory-pr-ready": "context-promotion",
    "memory-pr-merged": "memory-integration",
    "context-memory-terminal": "context-promotion",
    "finalization-ready": "finalization",
    "issue-closed": "finalization",
}

STAGES = frozenset(BOUNDARY_STAGE_MAP.values())

BOUNDARY_OUTCOMES: Mapping[str, frozenset[str]] = {
    "implementation-verified-draft": frozenset({"verified-draft-pr"}),
    "closeout-accepted-ready": frozenset({"accepted-ready-pr"}),
    "product-merged": frozenset({"verified", "no-op"}),
    "context-proposal-reviewed": frozenset({"awaiting-confirmation"}),
    "context-confirmed": frozenset({"confirmed"}),
    "context-no-promotion-terminal": frozenset({"no-promotion"}),
    "memory-pr-ready": frozenset({"verified-memory-pr", "memory-pr-ready"}),
    "memory-pr-merged": frozenset({"verified", "no-op"}),
    "context-memory-terminal": frozenset({"memory-pr-merged"}),
    "finalization-ready": frozenset({"ready-to-close"}),
    "issue-closed": frozenset({"verified", "no-op"}),
}

COMMON_BOUNDARIES = (
    "implementation-verified-draft",
    "closeout-accepted-ready",
    "product-merged",
    "context-proposal-reviewed",
    "context-confirmed",
)
NO_WRITE_BOUNDARIES = (
    "context-no-promotion-terminal",
)
WRITE_BOUNDARIES = (
    "memory-pr-ready",
    "memory-pr-merged",
    "context-memory-terminal",
)
FINALIZATION_BOUNDARY = "finalization-ready"
COMPLETION_BOUNDARY = "issue-closed"
COVERAGE_LEVELS = frozenset({"manifest", "closure", "completion"})
OBSERVATION_BINDING_FIELDS = frozenset(
    {"observation_url", "observation_sha256", "record"}
)

CHANGE_LIST_FIELDS = (
    "repository_changes",
    "github_mutations",
    "context_changes",
)
CHANGE_QUALITY_TO_LIST = {
    "repository": "repository_changes",
    "github": "github_mutations",
    "context": "context_changes",
}
CHANGE_QUALITY_VALUES = frozenset(
    {"measured", "reconstructed", "unknown", "not-applicable"}
)
CHANGE_SUMMARY_FIELDS = frozenset(
    (*CHANGE_LIST_FIELDS, "truncated", "omitted_count")
)
MAX_CHANGE_PREVIEW_ITEMS = 100

REQUIRED_FIELDS = frozenset(
    {
        "record_kind",
        "log_schema_version",
        "observation_kind",
        "boundary",
        "attempt_id",
        "stage",
        "activity",
        "attempt",
        "outcome",
        "issue_url",
        "issue_body_sha256",
        "observed_at",
        "started_at",
        "finished_at",
        "elapsed_ms",
        "timing_scope",
        "timing_quality",
        "user_wait_ms",
        "input_snapshot",
        "output_snapshot",
        "change_summary",
        "change_quality",
        "evidence",
        "raw_user_input_persisted",
        "reason_code",
        "transition_key",
    }
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_RFC3339_UTC_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$"
)
_MACHINE_CODE_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_GIT_OBJECT_ID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_CONTEXT_ITEM_ID_RE = re.compile(r"^CONTEXT-[1-9][0-9]*$")
_FORBIDDEN_PERSISTED_KEYS = frozenset(
    {
        "raw_user_input",
        "raw_user_response",
        "request_user_input_response",
        "confirmation_reply",
        "confirmation_response",
        "user_decision",
        "modification_items",
        "user_input",
        "user_response",
    }
)

MEMORY_PR_TUPLE_FIELDS = frozenset(
    {
        "memory_pr_url",
        "memory_pr_title",
        "memory_pr_body_sha256",
        "memory_head_ref",
        "memory_head_sha",
        "memory_base_ref",
        "memory_base_sha",
    }
)

BOUNDARY_SNAPSHOT_FIELDS: Mapping[
    str, tuple[frozenset[str], frozenset[str]]
] = {
    "implementation-verified-draft": (
        frozenset({"base_ref", "base_sha", "prior_head_sha"}),
        frozenset(
            {
                "product_pr_url",
                "product_pr_title",
                "product_pr_body_sha256",
                "head_ref",
                "head_sha",
                "base_ref",
                "base_sha",
            }
        ),
    ),
    "closeout-accepted-ready": (
        frozenset(
            {
                "product_pr_url",
                "product_pr_title",
                "product_pr_body_sha256",
                "head_ref",
                "head_sha",
                "base_ref",
                "base_sha",
            }
        ),
        frozenset(
            {
                "acceptance_comment_url",
                "acceptance_comment_sha256",
                "issue_callback_url",
                "issue_callback_sha256",
                "eligibility_registration_url",
                "eligibility_registration_sha256",
                "pr_state",
            }
        ),
    ),
    "product-merged": (
        frozenset(
            {
                "product_pr_url",
                "product_pr_title",
                "product_pr_body_sha256",
                "head_ref",
                "head_sha",
                "base_ref",
                "base_sha",
                "acceptance_comment_url",
                "acceptance_comment_sha256",
                "issue_callback_url",
                "issue_callback_sha256",
                "eligibility_registration_url",
                "eligibility_registration_sha256",
            }
        ),
        frozenset(
            {
                "merge_method",
                "merge_commit_sha",
                "merged_head_sha",
                "merged_base_ref",
            }
        ),
    ),
    "context-proposal-reviewed": (
        frozenset(
            {
                "product_pr_url",
                "source_head_sha",
                "source_merge_commit_sha",
                "eligibility_registration_url",
                "eligibility_registration_sha256",
                "authority_base_sha",
            }
        ),
        frozenset(
            {
                "proposal_artifact_url",
                "proposal_artifact_sha256",
                "proposal_comment_url",
                "proposal_comment_sha256",
                "review_url",
                "review_sha256",
                *MEMORY_PR_TUPLE_FIELDS,
            }
        ),
    ),
    "context-confirmed": (
        frozenset(
            {
                "proposal_artifact_url",
                "proposal_artifact_sha256",
                "proposal_comment_url",
                "proposal_comment_sha256",
                "review_url",
                "review_sha256",
                *MEMORY_PR_TUPLE_FIELDS,
            }
        ),
        frozenset(
            {
                "confirmation_comment_url",
                "confirmation_comment_sha256",
                "decision",
            }
        ),
    ),
    "context-no-promotion-terminal": (
        frozenset(
            {
                "proposal_artifact_url",
                "proposal_artifact_sha256",
                "proposal_comment_url",
                "proposal_comment_sha256",
                "review_url",
                "review_sha256",
                "confirmation_comment_url",
                "confirmation_comment_sha256",
            }
        ),
        frozenset(
            {
                "terminal_comment_url",
                "terminal_comment_sha256",
                "terminal_outcome",
            }
        ),
    ),
    "memory-pr-ready": (
        frozenset(
            {
                "proposal_artifact_url",
                "proposal_artifact_sha256",
                "proposal_comment_url",
                "proposal_comment_sha256",
                "review_url",
                "review_sha256",
                "confirmation_comment_url",
                "confirmation_comment_sha256",
            }
        ),
        frozenset(
            {
                *MEMORY_PR_TUPLE_FIELDS,
                "ready_comment_url",
                "ready_comment_sha256",
            }
        ),
    ),
    "memory-pr-merged": (
        frozenset(
            {
                *MEMORY_PR_TUPLE_FIELDS,
                "ready_comment_url",
                "ready_comment_sha256",
            }
        ),
        frozenset(
            {
                "merge_method",
                "merge_commit_sha",
                "merged_head_sha",
                "merged_base_ref",
            }
        ),
    ),
    "context-memory-terminal": (
        frozenset(
            {
                "memory_pr_url",
                "memory_pr_body_sha256",
                "memory_head_sha",
                "merge_method",
                "merge_commit_sha",
                "ready_comment_url",
                "ready_comment_sha256",
            }
        ),
        frozenset(
            {
                "terminal_comment_url",
                "terminal_comment_sha256",
                "terminal_outcome",
            }
        ),
    ),
    "finalization-ready": (
        frozenset(
            {"path_kind", "coverage_manifest", "coverage_manifest_sha256"}
        ),
        frozenset({"ready"}),
    ),
    "issue-closed": (
        frozenset(
            {
                "path_kind",
                "coverage_manifest_sha256",
                "finalization_observation_url",
                "finalization_observation_sha256",
            }
        ),
        frozenset({"state", "state_reason"}),
    ),
}

ATTEMPT_INPUT_FIELDS = frozenset({"target_boundary", "source_bindings"})
ATTEMPT_OUTPUT_FIELDS = frozenset(
    {
        "result_kind",
        "result_url",
        "result_sha256",
        "response_kind",
        "modification_item_count",
    }
)

BOUNDARY_EVIDENCE_BINDINGS: Mapping[
    str, tuple[tuple[str, str, str, str], ...]
] = {
    "implementation-verified-draft": (
        ("product-pr", "output", "product_pr_url", "product_pr_body_sha256"),
    ),
    "closeout-accepted-ready": (
        ("product-pr", "input", "product_pr_url", "product_pr_body_sha256"),
        (
            "acceptance-comment",
            "output",
            "acceptance_comment_url",
            "acceptance_comment_sha256",
        ),
        (
            "issue-callback",
            "output",
            "issue_callback_url",
            "issue_callback_sha256",
        ),
        (
            "eligibility-registration",
            "output",
            "eligibility_registration_url",
            "eligibility_registration_sha256",
        ),
    ),
    "product-merged": (
        ("product-pr", "input", "product_pr_url", "product_pr_body_sha256"),
        (
            "acceptance-comment",
            "input",
            "acceptance_comment_url",
            "acceptance_comment_sha256",
        ),
        ("issue-callback", "input", "issue_callback_url", "issue_callback_sha256"),
        (
            "eligibility-registration",
            "input",
            "eligibility_registration_url",
            "eligibility_registration_sha256",
        ),
    ),
    "context-proposal-reviewed": (
        (
            "eligibility-registration",
            "input",
            "eligibility_registration_url",
            "eligibility_registration_sha256",
        ),
        (
            "proposal-artifact",
            "output",
            "proposal_artifact_url",
            "proposal_artifact_sha256",
        ),
        (
            "proposal-callback",
            "output",
            "proposal_comment_url",
            "proposal_comment_sha256",
        ),
        ("review", "output", "review_url", "review_sha256"),
    ),
    "context-confirmed": (
        (
            "proposal-artifact",
            "input",
            "proposal_artifact_url",
            "proposal_artifact_sha256",
        ),
        (
            "proposal-callback",
            "input",
            "proposal_comment_url",
            "proposal_comment_sha256",
        ),
        ("review", "input", "review_url", "review_sha256"),
        (
            "confirmation-callback",
            "output",
            "confirmation_comment_url",
            "confirmation_comment_sha256",
        ),
    ),
    "context-no-promotion-terminal": (
        (
            "proposal-artifact",
            "input",
            "proposal_artifact_url",
            "proposal_artifact_sha256",
        ),
        (
            "confirmation-callback",
            "input",
            "confirmation_comment_url",
            "confirmation_comment_sha256",
        ),
        (
            "terminal-callback",
            "output",
            "terminal_comment_url",
            "terminal_comment_sha256",
        ),
    ),
    "memory-pr-ready": (
        (
            "proposal-artifact",
            "input",
            "proposal_artifact_url",
            "proposal_artifact_sha256",
        ),
        ("review", "input", "review_url", "review_sha256"),
        (
            "confirmation-callback",
            "input",
            "confirmation_comment_url",
            "confirmation_comment_sha256",
        ),
        ("memory-pr", "output", "memory_pr_url", "memory_pr_body_sha256"),
        (
            "ready-callback",
            "output",
            "ready_comment_url",
            "ready_comment_sha256",
        ),
    ),
    "memory-pr-merged": (
        ("memory-pr", "input", "memory_pr_url", "memory_pr_body_sha256"),
        (
            "ready-callback",
            "input",
            "ready_comment_url",
            "ready_comment_sha256",
        ),
    ),
    "context-memory-terminal": (
        ("memory-pr", "input", "memory_pr_url", "memory_pr_body_sha256"),
        (
            "ready-callback",
            "input",
            "ready_comment_url",
            "ready_comment_sha256",
        ),
        (
            "terminal-callback",
            "output",
            "terminal_comment_url",
            "terminal_comment_sha256",
        ),
    ),
    "issue-closed": (
        (
            "finalization-observation",
            "input",
            "finalization_observation_url",
            "finalization_observation_sha256",
        ),
    ),
}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_plain_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _is_uuid4(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = UUID(value)
    except ValueError:
        return False
    return parsed.version == 4 and str(parsed) == value


def _is_https_url(value: Any) -> bool:
    if not _is_nonempty_string(value) or any(
        character.isspace() for character in value
    ):
        return False
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and bool(hostname)
        and parsed.username is None
        and parsed.password is None
    )


def _parse_rfc3339_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or _RFC3339_UTC_RE.fullmatch(value) is None:
        return None
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)
    except ValueError:
        return None


def _machine_code_is_valid(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) <= 128
        and _MACHINE_CODE_RE.fullmatch(value) is not None
    )


def _relative_path_is_valid(value: Any) -> bool:
    if (
        not _is_nonempty_string(value)
        or "\\" in value
        or "\x00" in value
        or value.startswith("/")
        or value.endswith("/")
    ):
        return False
    parts = value.split("/")
    return (
        all(part not in {"", ".", ".."} for part in parts)
        and PurePosixPath(value).as_posix() == value
    )


def _nullable_nonnegative_integer_is_valid(value: Any) -> bool:
    return value is None or (_is_plain_integer(value) and value >= 0)


def _nullable_git_object_id_is_valid(value: Any) -> bool:
    return value is None or (
        isinstance(value, str) and _GIT_OBJECT_ID_RE.fullmatch(value) is not None
    )


def _nullable_sha256_is_valid(value: Any) -> bool:
    return value is None or _is_sha256(value)


def _concise_state_is_valid(value: Any, *, nullable: bool) -> bool:
    if value is None:
        return nullable
    return (
        _is_nonempty_string(value)
        and "\n" not in value
        and "\r" not in value
    )


def _json_value_errors(value: Any, path: str, active: set[int]) -> list[str]:
    """Return deterministic errors for a canonical, privacy-safe JSON value."""
    if value is None or isinstance(value, (str, bool, int)):
        return []
    if isinstance(value, float):
        if math.isfinite(value):
            return []
        return [f"{path}: non-finite numbers are not permitted"]

    if isinstance(value, Mapping):
        object_id = id(value)
        if object_id in active:
            return [f"{path}: cyclic values are not permitted"]
        active.add(object_id)
        errors: list[str] = []
        for key in sorted(value, key=lambda candidate: str(candidate)):
            if not isinstance(key, str):
                errors.append(f"{path}: object keys must be strings")
                continue
            if key.lower().replace("-", "_") in _FORBIDDEN_PERSISTED_KEYS:
                errors.append(f"{path}.{key}: raw user input must not be persisted")
            errors.extend(_json_value_errors(value[key], f"{path}.{key}", active))
        active.remove(object_id)
        return errors

    if isinstance(value, list):
        object_id = id(value)
        if object_id in active:
            return [f"{path}: cyclic values are not permitted"]
        active.add(object_id)
        errors = [
            error
            for index, item in enumerate(value)
            for error in _json_value_errors(item, f"{path}[{index}]", active)
        ]
        active.remove(object_id)
        return errors

    return [f"{path}: value must be JSON-compatible"]


def _validate_snapshot(value: Any, field: str) -> list[str]:
    if not isinstance(value, Mapping):
        return [f"{field}: must be an object"]
    return _json_value_errors(value, field, set())


def _validate_change_summary(value: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["change_summary: must be an object"]

    errors: list[str] = []
    missing = sorted(CHANGE_SUMMARY_FIELDS - set(value))
    extra = sorted(set(value) - CHANGE_SUMMARY_FIELDS, key=lambda item: str(item))
    errors.extend(f"change_summary.{field}: missing required field" for field in missing)
    errors.extend(f"change_summary.{field}: unknown field" for field in extra)

    preview_count = 0
    for field in CHANGE_LIST_FIELDS:
        items = value.get(field)
        if not isinstance(items, list):
            errors.append(f"change_summary.{field}: must be a list")
            continue
        preview_count += len(items)
        for index, item in enumerate(items):
            path = f"change_summary.{field}[{index}]"
            if field == "repository_changes":
                errors.extend(_validate_repository_change(item, path))
            elif field == "github_mutations":
                errors.extend(_validate_github_mutation(item, path))
            else:
                errors.extend(_validate_context_change(item, path))
        if field == "repository_changes" and all(
            isinstance(item, Mapping) and _relative_path_is_valid(item.get("path"))
            for item in items
        ):
            paths = [item["path"] for item in items]
            if paths != sorted(paths):
                errors.append(
                    "change_summary.repository_changes: must be sorted by path"
                )
    if preview_count > MAX_CHANGE_PREVIEW_ITEMS:
        errors.append(
            "change_summary: preview contains more than 100 items across all categories"
        )

    truncated = value.get("truncated")
    omitted_count = value.get("omitted_count")
    if not isinstance(truncated, bool):
        errors.append("change_summary.truncated: must be a boolean")
    if not _is_plain_integer(omitted_count) or omitted_count < 0:
        errors.append("change_summary.omitted_count: must be a non-negative integer")
    elif truncated is True and omitted_count == 0:
        errors.append(
            "change_summary.omitted_count: must be positive when truncated is true"
        )
    elif truncated is False and omitted_count != 0:
        errors.append(
            "change_summary.omitted_count: must be zero when truncated is false"
        )

    return errors


def _validate_exact_fields(
    value: Any,
    path: str,
    expected_fields: frozenset[str],
) -> tuple[list[str], Mapping[str, Any] | None]:
    if not isinstance(value, Mapping):
        return [f"{path}: must be an object"], None
    missing = sorted(expected_fields - set(value))
    extra = sorted(set(value) - expected_fields, key=lambda field: str(field))
    errors = [f"{path}.{field}: missing required field" for field in missing]
    errors.extend(f"{path}.{field}: unknown field" for field in extra)
    return errors, value


def _validate_repository_change(value: Any, path: str) -> list[str]:
    expected_fields = frozenset(
        {
            "path",
            "status",
            "previous_path",
            "additions",
            "deletions",
            "before_blob_sha",
            "after_blob_sha",
        }
    )
    errors, item = _validate_exact_fields(value, path, expected_fields)
    if item is None:
        return errors

    status = item.get("status")
    if not isinstance(status, str) or status not in {
        "added",
        "modified",
        "removed",
        "renamed",
    }:
        errors.append(
            f"{path}.status: must be 'added', 'modified', 'removed', or 'renamed'"
        )
    if not _relative_path_is_valid(item.get("path")):
        errors.append(f"{path}.path: must be a normalized relative POSIX path")

    previous_path = item.get("previous_path")
    if previous_path is not None and not _relative_path_is_valid(previous_path):
        errors.append(
            f"{path}.previous_path: must be null or a normalized relative POSIX path"
        )
    for field in ("additions", "deletions"):
        if not _nullable_nonnegative_integer_is_valid(item.get(field)):
            errors.append(f"{path}.{field}: must be null or a non-negative integer")

    for field in ("before_blob_sha", "after_blob_sha"):
        if not _nullable_git_object_id_is_valid(item.get(field)):
            errors.append(
                f"{path}.{field}: must be null or a lowercase 40/64-character Git object ID"
            )

    return errors


def _validate_github_mutation(value: Any, path: str) -> list[str]:
    expected_fields = frozenset(
        {
            "operation",
            "target_url",
            "before",
            "after",
            "result_url",
            "result_sha256",
        }
    )
    errors, item = _validate_exact_fields(value, path, expected_fields)
    if item is None:
        return errors

    operation = item.get("operation")
    if not isinstance(operation, str) or operation not in {
        "create-draft",
        "replace-content",
        "add-comment",
        "mark-ready",
        "convert-to-draft",
        "merge",
        "change-metadata",
    }:
        errors.append(f"{path}.operation: unknown GitHub mutation")
    if not _is_https_url(item.get("target_url")):
        errors.append(f"{path}.target_url: must be an absolute HTTPS URL")
    if not _concise_state_is_valid(item.get("before"), nullable=True):
        errors.append(f"{path}.before: must be null or a concise single-line state")
    if not _concise_state_is_valid(item.get("after"), nullable=False):
        errors.append(f"{path}.after: must be a concise single-line state")
    if not _is_https_url(item.get("result_url")):
        errors.append(f"{path}.result_url: must be an absolute HTTPS URL")
    if not _nullable_sha256_is_valid(item.get("result_sha256")):
        errors.append(
            f"{path}.result_sha256: must be null or a lowercase SHA-256 digest"
        )
    return errors


def _validate_context_change(value: Any, path: str) -> list[str]:
    expected_fields = frozenset(
        {
            "item_id",
            "action",
            "classification",
            "destination",
            "proposal_artifact_url",
            "proposal_artifact_sha256",
        }
    )
    errors, item = _validate_exact_fields(value, path, expected_fields)
    if item is None:
        return errors

    item_id = item.get("item_id")
    if not isinstance(item_id, str) or _CONTEXT_ITEM_ID_RE.fullmatch(item_id) is None:
        errors.append(f"{path}.item_id: must match CONTEXT-<positive integer>")

    action = item.get("action")
    classification = item.get("classification")
    destination = item.get("destination")
    if not isinstance(action, str) or action not in {
        "add",
        "update",
        "supersede",
        "no_write",
    }:
        errors.append(f"{path}.action: unknown Context Promotion action")
    if not isinstance(classification, str) or classification not in {
        "decision",
        "stable_rule",
        "wiki_knowledge",
        "stable_context",
        "milestone_evidence",
        "no_write",
    }:
        errors.append(f"{path}.classification: unknown Context classification")
    if destination is not None and not _relative_path_is_valid(destination):
        errors.append(
            f"{path}.destination: must be null or a normalized relative POSIX path"
        )
    if not _is_https_url(item.get("proposal_artifact_url")):
        errors.append(
            f"{path}.proposal_artifact_url: must be an absolute HTTPS URL"
        )
    if not _is_sha256(item.get("proposal_artifact_sha256")):
        errors.append(
            f"{path}.proposal_artifact_sha256: must be a lowercase SHA-256 digest"
        )
    return errors


def _validate_evidence(value: Any, path: str = "evidence") -> list[str]:
    if not isinstance(value, list):
        return [f"{path}: must be a list"]

    errors: list[str] = []
    expected_fields = frozenset({"kind", "url", "sha256"})
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{item_path}: must be an object")
            continue

        missing = sorted(expected_fields - set(item))
        extra = sorted(set(item) - expected_fields, key=lambda field: str(field))
        errors.extend(
            f"{item_path}.{field}: missing required field" for field in missing
        )
        errors.extend(f"{item_path}.{field}: unknown field" for field in extra)

        kind = item.get("kind")
        if not _machine_code_is_valid(kind):
            errors.append(
                f"{item_path}.kind: must be a lowercase kebab-case code"
            )

        if not _is_https_url(item.get("url")):
            errors.append(f"{item_path}.url: must be an absolute HTTPS URL")
        if not _is_sha256(item.get("sha256")):
            errors.append(
                f"{item_path}.sha256: must be a lowercase SHA-256 digest"
            )

    tuples = _evidence_tuples(value)
    if len(tuples) == len(value) and tuples != sorted(tuples):
        errors.append(f"{path}: must be sorted by kind, URL, and digest")
    return errors


def _evidence_tuples(value: Any) -> list[tuple[str, str, str]]:
    if not isinstance(value, list):
        return []
    tuples: list[tuple[str, str, str]] = []
    for item in value:
        if not isinstance(item, Mapping):
            continue
        kind = item.get("kind")
        url = item.get("url")
        digest = item.get("sha256")
        if isinstance(kind, str) and isinstance(url, str) and isinstance(digest, str):
            tuples.append((kind, url, digest))
    return tuples


def _canonical_json_sha256(value: Any) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def _validate_snapshot_values(
    snapshot: Mapping[str, Any],
    path: str,
    *,
    nullable_fields: frozenset[str] = frozenset(),
) -> list[str]:
    errors: list[str] = []
    git_sha_fields = {
        field
        for field in snapshot
        if isinstance(field, str)
        and field.endswith("_sha")
        and not field.endswith("_sha256")
    }
    for field, value in snapshot.items():
        field_path = f"{path}.{field}"
        if not isinstance(field, str):
            continue
        if value is None:
            if field not in nullable_fields:
                errors.append(f"{field_path}: must not be null")
            continue
        if field.endswith("_url"):
            if not _is_https_url(value):
                errors.append(f"{field_path}: must be an absolute HTTPS URL")
        elif field.endswith("_sha256"):
            if not _is_sha256(value):
                errors.append(
                    f"{field_path}: must be a lowercase SHA-256 digest"
                )
        elif field in git_sha_fields:
            if not _nullable_git_object_id_is_valid(value):
                errors.append(
                    f"{field_path}: must be a lowercase 40/64-character Git object ID"
                )
        elif field in {"base_ref", "memory_base_ref", "merged_base_ref"}:
            if value != "develop":
                errors.append(f"{field_path}: must be 'develop'")
        elif field == "merge_method":
            if not isinstance(value, str) or value not in {
                "merge",
                "squash",
                "rebase",
            }:
                errors.append(f"{field_path}: unknown merge method")
        elif field == "pr_state":
            if value != "ready":
                errors.append(f"{field_path}: must be 'ready'")
        elif field == "decision":
            if value != "approved":
                errors.append(f"{field_path}: must be 'approved'")
        elif field == "terminal_outcome":
            if not isinstance(value, str) or value not in {
                "no-promotion",
                "memory-pr-merged",
            }:
                errors.append(f"{field_path}: unknown terminal outcome")
        elif field == "path_kind":
            if not isinstance(value, str) or value not in {
                "no-write",
                "memory-write",
            }:
                errors.append(f"{field_path}: must be 'no-write' or 'memory-write'")
        elif field == "ready":
            if value is not True:
                errors.append(f"{field_path}: must be true")
        elif field == "state":
            if value != "closed":
                errors.append(f"{field_path}: must be 'closed'")
        elif field == "state_reason":
            if value != "completed":
                errors.append(f"{field_path}: must be 'completed'")
        elif field == "coverage_manifest":
            if not isinstance(value, Mapping):
                errors.append(f"{field_path}: must be an object")
        elif not _concise_state_is_valid(value, nullable=False):
            errors.append(f"{field_path}: must be a non-empty single-line value")
    return errors


def _validate_memory_tuple(
    snapshot: Mapping[str, Any],
    path: str,
) -> tuple[list[str], bool]:
    values = [snapshot.get(field) for field in MEMORY_PR_TUPLE_FIELDS]
    all_null = all(value is None for value in values)
    all_present = all(value is not None for value in values)
    if not all_null and not all_present:
        return [f"{path}: nullable memory PR tuple must be all-null or complete"], False
    return [], all_present


def _validate_boundary_evidence(
    boundary: str,
    input_snapshot: Mapping[str, Any],
    output_snapshot: Mapping[str, Any],
    evidence: Any,
    *,
    memory_write: bool,
) -> list[str]:
    if boundary == "finalization-ready":
        return _validate_finalization_manifest(
            input_snapshot,
            output_snapshot,
            evidence,
        )

    errors: list[str] = []
    current = Counter(_evidence_tuples(evidence))
    bindings = list(BOUNDARY_EVIDENCE_BINDINGS.get(boundary, ()))
    if boundary in {"context-proposal-reviewed", "context-confirmed"}:
        if memory_write:
            bindings.append(
                (
                    "memory-pr",
                    "output" if boundary == "context-proposal-reviewed" else "input",
                    "memory_pr_url",
                    "memory_pr_body_sha256",
                )
            )
        elif any(kind == "memory-pr" for kind, _, _ in current):
            errors.append("evidence: memory-pr is permitted only for a write tuple")

    expected_items: list[tuple[str, str, str]] = []
    for kind, section_name, url_field, digest_field in bindings:
        snapshot = (
            input_snapshot if section_name == "input" else output_snapshot
        )
        url = snapshot.get(url_field)
        digest = snapshot.get(digest_field)
        if not isinstance(url, str) or not isinstance(digest, str):
            errors.append(
                f"evidence: cannot bind malformed {section_name}.{url_field}/{digest_field}"
            )
            continue
        expected_items.append((kind, url, digest))
    expected_counter = Counter(expected_items)
    if current != expected_counter:
        errors.append(
            f"evidence: {boundary} requires exactly its canonical snapshot bindings"
        )
    return errors


def _validate_manifest_entry(
    value: Any,
    path: str,
    expected_boundary: str,
    *,
    memory_write: bool,
) -> list[str]:
    fields = frozenset(
        {
            "boundary",
            "observation_url",
            "observation_sha256",
            "transition_key",
            "evidence",
        }
    )
    errors, entry = _validate_exact_fields(value, path, fields)
    if entry is None:
        return errors
    if entry.get("boundary") != expected_boundary:
        errors.append(f"{path}.boundary: must be {expected_boundary!r}")
    if not _is_https_url(entry.get("observation_url")):
        errors.append(f"{path}.observation_url: must be an absolute HTTPS URL")
    for field in ("observation_sha256", "transition_key"):
        if not _is_sha256(entry.get(field)):
            errors.append(f"{path}.{field}: must be a lowercase SHA-256 digest")
    errors.extend(_validate_evidence(entry.get("evidence"), f"{path}.evidence"))
    tuples = _evidence_tuples(entry.get("evidence"))
    if tuples != sorted(tuples):
        errors.append(f"{path}.evidence: must be sorted by kind, URL, and digest")
    expected_kinds = [
        binding[0]
        for binding in BOUNDARY_EVIDENCE_BINDINGS.get(expected_boundary, ())
    ]
    if (
        memory_write
        and expected_boundary
        in {"context-proposal-reviewed", "context-confirmed"}
    ):
        expected_kinds.append("memory-pr")
    if Counter(kind for kind, _, _ in tuples) != Counter(expected_kinds):
        errors.append(
            f"{path}.evidence: must use the exact {expected_boundary} evidence kinds"
        )
    return errors


def _validate_finalization_manifest(
    input_snapshot: Mapping[str, Any],
    output_snapshot: Mapping[str, Any],
    evidence: Any,
) -> list[str]:
    errors: list[str] = []
    if output_snapshot.get("ready") is not True:
        errors.append("output_snapshot.ready: must be true")

    manifest_fields = frozenset(
        {
            "manifest_schema_version",
            "path_kind",
            "issue_url",
            "issue_body_sha256",
            "entries",
        }
    )
    manifest_errors, manifest = _validate_exact_fields(
        input_snapshot.get("coverage_manifest"),
        "input_snapshot.coverage_manifest",
        manifest_fields,
    )
    errors.extend(manifest_errors)
    if manifest is None:
        return errors

    path_kind = input_snapshot.get("path_kind")
    if not isinstance(path_kind, str) or path_kind not in {
        "no-write",
        "memory-write",
    }:
        errors.append("input_snapshot.path_kind: must be 'no-write' or 'memory-write'")
        return errors
    if (
        not _is_plain_integer(manifest.get("manifest_schema_version"))
        or manifest.get("manifest_schema_version") != 1
    ):
        errors.append(
            "input_snapshot.coverage_manifest.manifest_schema_version: must be integer 1"
        )
    if manifest.get("path_kind") != path_kind:
        errors.append(
            "input_snapshot.coverage_manifest.path_kind: must match input_snapshot.path_kind"
        )
    if not _is_https_url(manifest.get("issue_url")):
        errors.append(
            "input_snapshot.coverage_manifest.issue_url: must be an absolute HTTPS URL"
        )
    if not _is_sha256(manifest.get("issue_body_sha256")):
        errors.append(
            "input_snapshot.coverage_manifest.issue_body_sha256: must be a lowercase SHA-256 digest"
        )

    expected_boundaries = COMMON_BOUNDARIES + (
        WRITE_BOUNDARIES if path_kind == "memory-write" else NO_WRITE_BOUNDARIES
    )
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        errors.append("input_snapshot.coverage_manifest.entries: must be a list")
        return errors
    if len(entries) != len(expected_boundaries):
        errors.append(
            "input_snapshot.coverage_manifest.entries: wrong path boundary count"
        )
    for index, expected_boundary in enumerate(expected_boundaries):
        if index >= len(entries):
            break
        errors.extend(
            _validate_manifest_entry(
                entries[index],
                f"input_snapshot.coverage_manifest.entries[{index}]",
                expected_boundary,
                memory_write=path_kind == "memory-write",
            )
        )

    try:
        expected_digest = _canonical_json_sha256(manifest)
    except (TypeError, ValueError):
        errors.append(
            "input_snapshot.coverage_manifest: must be canonical JSON-compatible"
        )
    else:
        if input_snapshot.get("coverage_manifest_sha256") != expected_digest:
            errors.append(
                "input_snapshot.coverage_manifest_sha256: does not match the canonical manifest"
            )

    if any(errors):
        return errors

    expected_evidence = [
        (
            "stage-observation",
            entry["observation_url"],
            entry["observation_sha256"],
        )
        for entry in entries
    ]
    terminal_evidence = [
        item
        for item in _evidence_tuples(entries[-1]["evidence"])
        if item[0] == "terminal-callback"
    ]
    if len(terminal_evidence) != 1:
        errors.append(
            "input_snapshot.coverage_manifest: terminal entry requires one terminal-callback evidence"
        )
        return errors
    expected_evidence.extend(terminal_evidence)
    if Counter(_evidence_tuples(evidence)) != Counter(expected_evidence):
        errors.append(
            "evidence: finalization-ready must exactly bind manifest observations and terminal callback"
        )
    return errors


def _validate_attempt_snapshots(
    record: Mapping[str, Any],
    input_snapshot: Mapping[str, Any],
    output_snapshot: Mapping[str, Any],
    evidence: Any,
) -> list[str]:
    errors: list[str] = []
    target_boundary = input_snapshot.get("target_boundary")
    if target_boundary is not None:
        target_stage = (
            BOUNDARY_STAGE_MAP.get(target_boundary)
            if isinstance(target_boundary, str)
            else None
        )
        if target_stage is None:
            errors.append("input_snapshot.target_boundary: unknown boundary")
        elif record.get("stage") != target_stage:
            errors.append(
                "stage: must match input_snapshot.target_boundary for an attempt"
            )

    source_bindings = input_snapshot.get("source_bindings")
    errors.extend(
        _validate_evidence(source_bindings, "input_snapshot.source_bindings")
    )
    source_tuples = _evidence_tuples(source_bindings)
    if source_tuples != sorted(source_tuples):
        errors.append(
            "input_snapshot.source_bindings: must be sorted by kind, URL, and digest"
        )

    result_kind = output_snapshot.get("result_kind")
    if not _machine_code_is_valid(result_kind):
        errors.append(
            "output_snapshot.result_kind: must be a lowercase kebab-case code"
        )
    elif record.get("outcome") != result_kind:
        errors.append("outcome: attempt must equal output_snapshot.result_kind")

    result_url = output_snapshot.get("result_url")
    result_digest = output_snapshot.get("result_sha256")
    if (result_url is None) != (result_digest is None):
        errors.append(
            "output_snapshot.result_url/result_sha256: must both be null or both populated"
        )
    elif result_url is not None:
        if not _is_https_url(result_url):
            errors.append(
                "output_snapshot.result_url: must be an absolute HTTPS URL"
            )
        if not _is_sha256(result_digest):
            errors.append(
                "output_snapshot.result_sha256: must be a lowercase SHA-256 digest"
            )

    response_kind = output_snapshot.get("response_kind")
    modification_count = output_snapshot.get("modification_item_count")
    if (response_kind is None) != (modification_count is None):
        errors.append(
            "output_snapshot.response_kind/modification_item_count: must both be null or both populated"
        )
    elif response_kind is not None:
        if not isinstance(response_kind, str) or response_kind not in {
            "approved",
            "revision-requested",
            "paused",
            "blocked",
        }:
            errors.append("output_snapshot.response_kind: unknown response")
        if not _is_plain_integer(modification_count) or modification_count < 0:
            errors.append(
                "output_snapshot.modification_item_count: must be a non-negative integer"
            )
        if (
            record.get("stage") != "context-confirmation"
            or record.get("activity") != "confirm"
            or record.get("timing_quality") != "measured"
            or not _is_uuid4(record.get("attempt_id"))
        ):
            errors.append(
                "output_snapshot.response_kind: requires a live measured context-confirmation/confirm attempt"
            )

    expected_evidence = list(source_tuples)
    if (
        isinstance(result_url, str)
        and isinstance(result_digest, str)
        and isinstance(result_kind, str)
    ):
        expected_evidence.append((result_kind, result_url, result_digest))
    if Counter(_evidence_tuples(evidence)) != Counter(expected_evidence):
        errors.append(
            "evidence: attempt evidence must exactly equal source and result bindings"
        )
    return errors


def _validate_snapshots_and_bindings(record: Mapping[str, Any]) -> list[str]:
    input_errors, input_snapshot = _validate_exact_fields(
        record.get("input_snapshot"),
        "input_snapshot",
        (
            ATTEMPT_INPUT_FIELDS
            if record.get("observation_kind") == "attempt"
            else (
                BOUNDARY_SNAPSHOT_FIELDS.get(
                    record.get("boundary"), (frozenset(), frozenset())
                )[0]
                if isinstance(record.get("boundary"), str)
                else frozenset()
            )
        ),
    )
    output_errors, output_snapshot = _validate_exact_fields(
        record.get("output_snapshot"),
        "output_snapshot",
        (
            ATTEMPT_OUTPUT_FIELDS
            if record.get("observation_kind") == "attempt"
            else (
                BOUNDARY_SNAPSHOT_FIELDS.get(
                    record.get("boundary"), (frozenset(), frozenset())
                )[1]
                if isinstance(record.get("boundary"), str)
                else frozenset()
            )
        ),
    )
    errors = input_errors + output_errors
    if input_snapshot is None or output_snapshot is None:
        return errors
    errors.extend(_json_value_errors(input_snapshot, "input_snapshot", set()))
    errors.extend(_json_value_errors(output_snapshot, "output_snapshot", set()))

    if record.get("observation_kind") == "attempt":
        errors.extend(
            _validate_attempt_snapshots(
                record,
                input_snapshot,
                output_snapshot,
                record.get("evidence"),
            )
        )
        return errors

    boundary = record.get("boundary")
    nullable_input = (
        MEMORY_PR_TUPLE_FIELDS
        if boundary == "context-confirmed"
        else frozenset({"prior_head_sha"})
        if boundary == "implementation-verified-draft"
        else frozenset()
    )
    nullable_output = (
        MEMORY_PR_TUPLE_FIELDS
        if boundary == "context-proposal-reviewed"
        else frozenset()
    )
    errors.extend(
        _validate_snapshot_values(
            input_snapshot,
            "input_snapshot",
            nullable_fields=nullable_input,
        )
    )
    errors.extend(
        _validate_snapshot_values(
            output_snapshot,
            "output_snapshot",
            nullable_fields=nullable_output,
        )
    )

    memory_write = False
    if boundary == "context-proposal-reviewed":
        tuple_errors, memory_write = _validate_memory_tuple(
            output_snapshot, "output_snapshot"
        )
        errors.extend(tuple_errors)
    elif boundary == "context-confirmed":
        tuple_errors, memory_write = _validate_memory_tuple(
            input_snapshot, "input_snapshot"
        )
        errors.extend(tuple_errors)

    if boundary == "finalization-ready":
        manifest = input_snapshot.get("coverage_manifest")
        if isinstance(manifest, Mapping):
            if manifest.get("issue_url") != record.get("issue_url"):
                errors.append(
                    "input_snapshot.coverage_manifest.issue_url: must match issue_url"
                )
            if manifest.get("issue_body_sha256") != record.get(
                "issue_body_sha256"
            ):
                errors.append(
                    "input_snapshot.coverage_manifest.issue_body_sha256: must match issue_body_sha256"
                )
    if boundary == "context-no-promotion-terminal":
        if output_snapshot.get("terminal_outcome") != "no-promotion":
            errors.append(
                "output_snapshot.terminal_outcome: must be 'no-promotion'"
            )
    elif boundary == "context-memory-terminal":
        if output_snapshot.get("terminal_outcome") != "memory-pr-merged":
            errors.append(
                "output_snapshot.terminal_outcome: must be 'memory-pr-merged'"
            )

    if isinstance(boundary, str):
        errors.extend(
            _validate_boundary_evidence(
                boundary,
                input_snapshot,
                output_snapshot,
                record.get("evidence"),
                memory_write=memory_write,
            )
        )
    return errors


def _validate_issue_closed_semantics(record: Mapping[str, Any]) -> list[str]:
    if (
        record.get("observation_kind") != "boundary"
        or record.get("boundary") != "issue-closed"
    ):
        return []

    errors: list[str] = []
    change_quality = record.get("change_quality")
    github_quality = (
        change_quality.get("github")
        if isinstance(change_quality, Mapping)
        else None
    )
    change_summary = record.get("change_summary")
    github_mutations = (
        change_summary.get("github_mutations")
        if isinstance(change_summary, Mapping)
        else None
    )

    exact_close_mutation = (
        isinstance(github_mutations, list)
        and len(github_mutations) == 1
        and isinstance(github_mutations[0], Mapping)
        and github_mutations[0].get("operation") == "change-metadata"
        and github_mutations[0].get("target_url") == record.get("issue_url")
    )

    if record.get("outcome") == "verified":
        if (
            record.get("timing_quality") != "measured"
            or not _is_uuid4(record.get("attempt_id"))
        ):
            errors.append(
                "issue-closed verified: requires measured timing and a live attempt_id"
            )
        if github_quality != "measured":
            errors.append(
                "issue-closed verified: requires measured GitHub change quality"
            )
        if not exact_close_mutation:
            errors.append(
                "issue-closed verified: requires exactly one source-Issue change-metadata mutation"
            )
    elif record.get("outcome") == "no-op":
        if record.get("timing_quality") not in (
            "reconstructed",
            "unknown",
        ):
            errors.append(
                "issue-closed no-op: requires reconstructed or unknown timing"
            )
        if record.get("attempt_id") is not None:
            errors.append("issue-closed no-op: requires a null attempt_id")
        if github_quality != "unknown":
            errors.append(
                "issue-closed no-op: GitHub change quality must be unknown"
            )
        if github_mutations != []:
            errors.append(
                "issue-closed no-op: GitHub mutations must be empty"
            )
    return errors


def validate_observation(record: Mapping[str, Any]) -> list[str]:
    """Validate one ``delivery-stage-observation`` schema-v1 record.

    The returned list is empty only for a complete valid observation.  Error
    strings are deterministic and field-qualified so callers may persist a
    reason code without copying sensitive values.
    """
    if not isinstance(record, Mapping):
        return ["record: must be an object"]

    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    extra = sorted(set(record) - REQUIRED_FIELDS, key=lambda field: str(field))
    errors.extend(f"{field}: missing required field" for field in missing)
    errors.extend(f"{field}: unknown field" for field in extra)

    if record.get("record_kind") != RECORD_KIND:
        errors.append(f"record_kind: must be {RECORD_KIND!r}")
    if (
        not _is_plain_integer(record.get("log_schema_version"))
        or record.get("log_schema_version") != LOG_SCHEMA_VERSION
    ):
        errors.append("log_schema_version: must be integer 1")

    observation_kind = record.get("observation_kind")
    if not isinstance(observation_kind, str) or observation_kind not in OBSERVATION_KINDS:
        errors.append("observation_kind: must be 'attempt' or 'boundary'")

    stage = record.get("stage")
    if not isinstance(stage, str) or stage not in STAGES:
        errors.append("stage: unknown delivery stage")

    boundary = record.get("boundary")
    if observation_kind == "attempt":
        if boundary is not None:
            errors.append("boundary: must be null for an attempt observation")
    elif observation_kind == "boundary":
        expected_stage = (
            BOUNDARY_STAGE_MAP.get(boundary)
            if isinstance(boundary, str)
            else None
        )
        if expected_stage is None:
            errors.append("boundary: unknown delivery boundary")
        elif stage != expected_stage:
            errors.append(
                f"stage: boundary {boundary!r} requires stage {expected_stage!r}"
            )
        allowed_outcomes = (
            BOUNDARY_OUTCOMES.get(boundary)
            if isinstance(boundary, str)
            else None
        )
        if (
            allowed_outcomes is not None
            and (
                not isinstance(record.get("outcome"), str)
                or record.get("outcome") not in allowed_outcomes
            )
        ):
            expected = " or ".join(repr(value) for value in sorted(allowed_outcomes))
            errors.append(f"outcome: boundary {boundary!r} requires {expected}")

    if (
        not isinstance(record.get("activity"), str)
        or record.get("activity") not in ACTIVITIES
    ):
        errors.append("activity: unknown delivery activity")
    if not _is_plain_integer(record.get("attempt")) or record.get("attempt", 0) < 1:
        errors.append("attempt: must be a positive integer")
    if not _machine_code_is_valid(record.get("outcome")):
        errors.append("outcome: must be a lowercase kebab-case code")
    if record.get("reason_code") is not None and not _machine_code_is_valid(
        record.get("reason_code")
    ):
        errors.append("reason_code: must be null or a lowercase kebab-case code")

    if not _is_https_url(record.get("issue_url")):
        errors.append("issue_url: must be an absolute HTTPS URL")
    if not _is_sha256(record.get("issue_body_sha256")):
        errors.append("issue_body_sha256: must be a lowercase SHA-256 digest")

    observed_at = _parse_rfc3339_utc(record.get("observed_at"))
    if observed_at is None:
        errors.append("observed_at: must be an RFC3339 UTC timestamp ending in Z")

    timing_scope = record.get("timing_scope")
    if timing_scope != TIMING_SCOPE:
        errors.append(f"timing_scope: must be {TIMING_SCOPE!r}")

    timing_quality = record.get("timing_quality")
    if (
        not isinstance(timing_quality, str)
        or timing_quality not in TIMING_QUALITIES
    ):
        errors.append(
            "timing_quality: must be 'measured', 'reconstructed', or 'unknown'"
        )

    attempt_id = record.get("attempt_id")
    if attempt_id is not None and not _is_uuid4(attempt_id):
        errors.append("attempt_id: must be null or a canonical lowercase UUIDv4")
    if observation_kind == "attempt" and not _is_uuid4(attempt_id):
        errors.append("attempt_id: attempt observations require a UUIDv4")
    elif timing_quality == "measured" and not _is_uuid4(attempt_id):
        errors.append("attempt_id: measured observations require a UUIDv4")
    elif (
        observation_kind == "boundary"
        and (timing_quality == "reconstructed" or timing_quality == "unknown")
        and attempt_id is not None
    ):
        errors.append(
            "attempt_id: reconstructed or unknown-timing boundaries require null"
        )

    started_value = record.get("started_at")
    finished_value = record.get("finished_at")
    started_at = (
        _parse_rfc3339_utc(started_value) if started_value is not None else None
    )
    finished_at = (
        _parse_rfc3339_utc(finished_value) if finished_value is not None else None
    )
    if started_value is not None and started_at is None:
        errors.append("started_at: must be null or an RFC3339 UTC timestamp ending in Z")
    if finished_value is not None and finished_at is None:
        errors.append(
            "finished_at: must be null or an RFC3339 UTC timestamp ending in Z"
        )

    elapsed_ms = record.get("elapsed_ms")
    if timing_quality == "measured":
        if started_at is None:
            errors.append("started_at: measured timing requires a timestamp")
        if finished_at is None:
            errors.append("finished_at: measured timing requires a timestamp")
        if not _is_plain_integer(elapsed_ms) or elapsed_ms < 0:
            errors.append("elapsed_ms: measured timing requires a non-negative integer")
    elif timing_quality == "reconstructed" or timing_quality == "unknown":
        if elapsed_ms is not None:
            errors.append(
                "elapsed_ms: reconstructed or unknown timing must not claim a duration"
            )
        if timing_quality == "reconstructed":
            if finished_at is None:
                errors.append(
                    "finished_at: reconstructed timing requires a trustworthy terminal timestamp"
                )
        elif started_value is not None or finished_value is not None:
            errors.append(
                "started_at/finished_at: unknown timing requires null timestamps"
            )

    if started_at is not None and finished_at is not None:
        if finished_at < started_at:
            errors.append("finished_at: must not precede started_at")
        if observed_at is not None and observed_at < finished_at:
            errors.append("observed_at: must not precede finished_at")

    user_wait_ms = record.get("user_wait_ms")
    if user_wait_ms is not None:
        if not _is_plain_integer(user_wait_ms) or user_wait_ms < 0:
            errors.append("user_wait_ms: must be null or a non-negative integer")
        else:
            if (
                record.get("stage") != "context-confirmation"
                or record.get("activity") != "confirm"
            ):
                errors.append(
                    "user_wait_ms: may be recorded only for context-confirmation/confirm"
                )
            if timing_quality != "measured":
                errors.append("user_wait_ms: requires measured timing")
            elif _is_plain_integer(elapsed_ms) and user_wait_ms > elapsed_ms:
                errors.append("user_wait_ms: must not exceed elapsed_ms")

    errors.extend(_validate_change_summary(record.get("change_summary")))
    errors.extend(_validate_evidence(record.get("evidence")))
    errors.extend(_validate_snapshots_and_bindings(record))

    change_quality = record.get("change_quality")
    if not isinstance(change_quality, Mapping):
        errors.append("change_quality: must be an object")
    else:
        quality_fields = frozenset(CHANGE_QUALITY_TO_LIST)
        missing_quality = sorted(quality_fields - set(change_quality))
        extra_quality = sorted(
            set(change_quality) - quality_fields,
            key=lambda field: str(field),
        )
        errors.extend(
            f"change_quality.{field}: missing required field"
            for field in missing_quality
        )
        errors.extend(
            f"change_quality.{field}: unknown field" for field in extra_quality
        )

        change_summary = record.get("change_summary")
        unknown_present = False
        for quality_field, list_field in CHANGE_QUALITY_TO_LIST.items():
            quality = change_quality.get(quality_field)
            if (
                not isinstance(quality, str)
                or quality not in CHANGE_QUALITY_VALUES
            ):
                errors.append(
                    f"change_quality.{quality_field}: unknown change quality"
                )
                continue
            if quality == "unknown":
                unknown_present = True
            if (
                quality in {"unknown", "not-applicable"}
                and (
                    not isinstance(change_summary, Mapping)
                    or change_summary.get(list_field) != []
                )
            ):
                errors.append(
                    f"change_quality.{quality_field}: {quality} requires an empty {list_field}"
                )

        if unknown_present and not _machine_code_is_valid(
            record.get("reason_code")
        ):
            errors.append(
                "reason_code: unknown change quality requires a non-empty code"
            )

    errors.extend(_validate_issue_closed_semantics(record))

    if record.get("raw_user_input_persisted") is not False:
        errors.append("raw_user_input_persisted: must be false")

    persisted_transition_key = record.get("transition_key")
    if not _is_sha256(persisted_transition_key):
        errors.append("transition_key: must be a lowercase SHA-256 digest")
    elif not errors:
        try:
            expected_transition_key = _compute_transition_key(record)
        except (KeyError, TypeError, ValueError):
            errors.append(
                "transition_key: durable transition identity is not canonical JSON"
            )
        else:
            if persisted_transition_key != expected_transition_key:
                errors.append(
                    "transition_key: does not match the durable transition identity"
                )

    return errors


def validate_new_observation(record: Mapping[str, Any]) -> list[str]:
    """Validate a record for a new split-turn protocol write.

    ``validate_observation`` remains the schema-v1 reader and therefore accepts
    historical same-turn confirmation timing and response/count combinations.
    New writers must additionally satisfy the split-turn confirmation policy
    enforced here.
    """
    errors = validate_observation(record)
    if not isinstance(record, Mapping):
        return errors

    if record.get("user_wait_ms") is not None:
        errors.append(
            "user_wait_ms: new split-turn observations require null"
        )

    input_snapshot = record.get("input_snapshot")
    target_boundary = (
        input_snapshot.get("target_boundary")
        if isinstance(input_snapshot, Mapping)
        else None
    )
    source_bindings = (
        input_snapshot.get("source_bindings")
        if isinstance(input_snapshot, Mapping)
        else None
    )
    source_tuples = _evidence_tuples(source_bindings)
    is_confirmation_attempt = (
        record.get("observation_kind") == "attempt"
        and (
            record.get("stage") == "context-confirmation"
            or record.get("activity") == "confirm"
            or target_boundary == "context-confirmed"
        )
    )
    if is_confirmation_attempt:
        if target_boundary != "context-confirmed":
            errors.append(
                "input_snapshot.target_boundary: new confirmation attempt "
                "requires 'context-confirmed'"
            )
        if (
            len(source_tuples) != 1
            or source_tuples[0][0] != "proposal-callback"
        ):
            errors.append(
                "input_snapshot.source_bindings: new confirmation attempt "
                "requires exactly one proposal-callback binding"
            )

    output_snapshot = record.get("output_snapshot")
    if isinstance(output_snapshot, Mapping):
        response_kind = output_snapshot.get("response_kind")
        result_kind = output_snapshot.get("result_kind")
        modification_count = output_snapshot.get("modification_item_count")
        if response_kind == "approved" or result_kind == "approved":
            errors.append(
                "output_snapshot.result_kind/response_kind: new approved "
                "confirmation must use the context-confirmed boundary"
            )
        if (
            isinstance(result_kind, str)
            and result_kind in {"revision-requested", "paused"}
            and response_kind != result_kind
        ):
            errors.append(
                "output_snapshot.response_kind: new revision-requested or "
                "paused result requires the matching response"
            )
        if isinstance(response_kind, str) and response_kind in {
            "approved",
            "revision-requested",
            "paused",
            "blocked",
        }:
            if (
                output_snapshot.get("result_url") is not None
                or output_snapshot.get("result_sha256") is not None
            ):
                errors.append(
                    "output_snapshot.result_url/result_sha256: new "
                    "confirmation response requires both null"
                )
            if response_kind != "approved" and (
                output_snapshot.get("result_kind") != response_kind
                or record.get("outcome") != response_kind
            ):
                errors.append(
                    "output_snapshot.response_kind: new confirmation "
                    "response must equal result_kind and outcome"
                )
            if record.get("change_quality") != {
                "repository": "not-applicable",
                "github": "not-applicable",
                "context": "not-applicable",
            }:
                errors.append(
                    "change_quality: new confirmation response requires all "
                    "domains not-applicable"
                )
            change_summary = record.get("change_summary")
            if not isinstance(change_summary, Mapping) or any(
                (
                    change_summary.get("repository_changes") != [],
                    change_summary.get("github_mutations") != [],
                    change_summary.get("context_changes") != [],
                    change_summary.get("truncated") is not False,
                    change_summary.get("omitted_count") != 0,
                )
            ):
                errors.append(
                    "change_summary: new confirmation response requires no "
                    "reported mutations"
                )
        if (
            isinstance(response_kind, str)
            and response_kind in {"approved", "paused"}
            and modification_count != 0
        ):
            errors.append(
                "output_snapshot.modification_item_count: "
                f"{response_kind} requires zero"
            )
        elif (
            response_kind == "revision-requested"
            and (
                not _is_plain_integer(modification_count)
                or modification_count < 1
            )
        ):
            errors.append(
                "output_snapshot.modification_item_count: "
                "revision-requested requires a positive integer"
            )

    return errors


def _compute_transition_key(record: Mapping[str, Any]) -> str:
    evidence = sorted(
        (
            {
                "kind": item["kind"],
                "url": item["url"],
                "sha256": item["sha256"],
            }
            for item in record["evidence"]
        ),
        key=lambda item: (item["kind"], item["url"], item["sha256"]),
    )
    durable_identity = {
        "log_schema_version": record["log_schema_version"],
        "observation_kind": record["observation_kind"],
        "boundary": record["boundary"],
        "stage": record["stage"],
        "issue_url": record["issue_url"],
        "issue_body_sha256": record["issue_body_sha256"],
        "input_snapshot": record["input_snapshot"],
        "output_snapshot": record["output_snapshot"],
        "evidence": evidence,
    }
    canonical = json.dumps(
        durable_identity,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def transition_key(record: Mapping[str, Any]) -> str:
    """Return the durable transition SHA-256 for an otherwise valid record.

    Activity, top-level outcome, attempt ID, timestamps, elapsed/user-wait time,
    attempt number, change quality/preview, reason code, and the persisted key
    itself are deliberately excluded.  This function may therefore be used to
    populate ``transition_key`` initially or independently recompute it during
    read-back.  Evidence is sorted so transport enumeration order does not
    change the transition identity.
    """
    try:
        computed = _compute_transition_key(record)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("invalid delivery observation identity") from error

    candidate = dict(record)
    candidate["transition_key"] = computed
    errors = validate_observation(candidate)
    if errors:
        raise ValueError("invalid delivery observation: " + "; ".join(errors))
    return computed


def _validated_observation_binding(
    value: Any,
) -> tuple[str, str, Mapping[str, Any]] | None:
    """Return one exact, schema-valid whole-comment binding or ``None``.

    The caller remains responsible for establishing transport author, complete
    enumeration, immutable read-back, and current workflow lineage.  This pure
    guard only makes that already-established comment URL/digest identity
    executable when validating the manifest and closure chain.
    """
    if not isinstance(value, Mapping) or set(value) != OBSERVATION_BINDING_FIELDS:
        return None
    observation_url = value.get("observation_url")
    observation_sha256 = value.get("observation_sha256")
    record = value.get("record")
    if (
        not _is_https_url(observation_url)
        or not _is_sha256(observation_sha256)
        or not isinstance(record, Mapping)
    ):
        return None
    try:
        errors = validate_observation(record)
    except (KeyError, RecursionError, TypeError, ValueError):
        return None
    if errors:
        return None
    return observation_url, observation_sha256, record


def _manifest_matches_bindings(
    finalization: tuple[str, str, Mapping[str, Any]],
    source_boundaries: tuple[str, ...],
    selected: Mapping[str, tuple[str, str, Mapping[str, Any]]],
    *,
    expected_path_kind: str,
) -> bool:
    finalization_record = finalization[2]
    input_snapshot = finalization_record.get("input_snapshot")
    if not isinstance(input_snapshot, Mapping):
        return False
    if input_snapshot.get("path_kind") != expected_path_kind:
        return False
    manifest = input_snapshot.get("coverage_manifest")
    if not isinstance(manifest, Mapping):
        return False
    if (
        manifest.get("path_kind") != expected_path_kind
        or manifest.get("issue_url") != finalization_record.get("issue_url")
        or manifest.get("issue_body_sha256")
        != finalization_record.get("issue_body_sha256")
    ):
        return False
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != len(source_boundaries):
        return False

    for expected_boundary, entry in zip(source_boundaries, entries):
        binding = selected.get(expected_boundary)
        if binding is None or not isinstance(entry, Mapping):
            return False
        observation_url, observation_sha256, record = binding
        if (
            entry.get("boundary") != expected_boundary
            or entry.get("observation_url") != observation_url
            or entry.get("observation_sha256") != observation_sha256
            or entry.get("transition_key") != record.get("transition_key")
            or entry.get("evidence") != record.get("evidence")
        ):
            return False
    return True


def _completion_matches_finalization(
    completion: tuple[str, str, Mapping[str, Any]],
    finalization: tuple[str, str, Mapping[str, Any]],
    *,
    expected_path_kind: str,
) -> bool:
    completion_record = completion[2]
    finalization_url, finalization_sha256, finalization_record = finalization
    completion_input = completion_record.get("input_snapshot")
    finalization_input = finalization_record.get("input_snapshot")
    if not isinstance(completion_input, Mapping) or not isinstance(
        finalization_input, Mapping
    ):
        return False
    return (
        completion_record.get("issue_url") == finalization_record.get("issue_url")
        and completion_record.get("issue_body_sha256")
        == finalization_record.get("issue_body_sha256")
        and completion_input.get("path_kind") == expected_path_kind
        and finalization_input.get("path_kind") == expected_path_kind
        and completion_input.get("coverage_manifest_sha256")
        == finalization_input.get("coverage_manifest_sha256")
        and completion_input.get("finalization_observation_url")
        == finalization_url
        and completion_input.get("finalization_observation_sha256")
        == finalization_sha256
    )


def coverage(
    bindings: Iterable[Mapping[str, Any]],
    memory_required: bool,
    level: str = "manifest",
) -> tuple[bool, list[str]]:
    """Check an exact verified-observation chain for one delivery path.

    Every input item must have exactly ``observation_url``,
    ``observation_sha256``, and ``record``.  The URL/digest must identify the
    independently re-read whole comment represented by the valid schema-v1
    record; bare records never satisfy any coverage level.  This function does
    not establish transport trust itself.

    Any malformed, non-exact, or schema-invalid binding fails the complete
    check with ``observation-binding``.  Exact valid attempt bindings and exact
    valid boundary bindings outside the requested path are ignored only after
    validation; they never satisfy a required boundary.

    ``manifest`` requires one unambiguous binding for each of the 6/8 source
    boundaries.  ``closure`` additionally requires one ``finalization-ready``
    binding whose manifest entries exactly match those source bindings.
    ``completion`` additionally requires one ``issue-closed`` binding that
    exactly references the selected finalization comment and manifest digest.
    Duplicate or conflicting relevant bindings fail closed.
    """
    if not isinstance(memory_required, bool):
        raise TypeError("memory_required must be a boolean")
    if not isinstance(level, str) or level not in COVERAGE_LEVELS:
        raise ValueError("level must be 'manifest', 'closure', or 'completion'")

    source_boundaries = COMMON_BOUNDARIES + (
        WRITE_BOUNDARIES if memory_required else NO_WRITE_BOUNDARIES
    )
    required = source_boundaries
    if level in {"closure", "completion"}:
        required += (FINALIZATION_BOUNDARY,)
    if level == "completion":
        required += (COMPLETION_BOUNDARY,)

    relevant_names = set(required)
    relevant_bindings = []
    for value in bindings:
        binding = _validated_observation_binding(value)
        if binding is None:
            return False, ["observation-binding"]
        if (
            binding[2].get("observation_kind") == "boundary"
            and binding[2].get("boundary") in relevant_names
        ):
            relevant_bindings.append(binding)

    source_identities = {
        (binding[2].get("issue_url"), binding[2].get("issue_body_sha256"))
        for binding in relevant_bindings
    }
    if len(source_identities) > 1:
        return False, ["source-identity"]

    observation_urls = [binding[0] for binding in relevant_bindings]
    if len(observation_urls) != len(set(observation_urls)):
        return False, ["observation-identity"]

    grouped: dict[str, list[tuple[str, str, Mapping[str, Any]]]] = {}
    for binding in relevant_bindings:
        boundary = binding[2].get("boundary")
        if isinstance(boundary, str):
            grouped.setdefault(boundary, []).append(binding)

    selected = {
        boundary: candidates[0]
        for boundary, candidates in grouped.items()
        if len(candidates) == 1
    }
    expected_path_kind = "memory-write" if memory_required else "no-write"
    present = {
        boundary for boundary in source_boundaries if boundary in selected
    }

    finalization = selected.get(FINALIZATION_BOUNDARY)
    if (
        finalization is not None
        and all(boundary in selected for boundary in source_boundaries)
        and _manifest_matches_bindings(
            finalization,
            source_boundaries,
            selected,
            expected_path_kind=expected_path_kind,
        )
    ):
        present.add(FINALIZATION_BOUNDARY)

    completion = selected.get(COMPLETION_BOUNDARY)
    if (
        completion is not None
        and finalization is not None
        and FINALIZATION_BOUNDARY in present
        and _completion_matches_finalization(
            completion,
            finalization,
            expected_path_kind=expected_path_kind,
        )
    ):
        present.add(COMPLETION_BOUNDARY)

    missing = [boundary for boundary in required if boundary not in present]
    return not missing, missing
