#!/usr/bin/env python3
"""Canonical Context Promotion Reviewer input identities.

This module is deterministic and side-effect free. It validates and sorts the
semantic evidence manifest consumed by a fresh Reviewer, then returns the
stable SHA-256 persisted in a versioned Reviewer PASS.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import copy
from hashlib import sha256
import json
import re
from typing import Any
from urllib.parse import urlsplit


REVIEW_INPUT_SCHEMA_VERSION = 1
REVIEW_POLICY_VERSION = 1

_TOP_FIELDS = frozenset(
    {
        "review_input_schema_version",
        "review_policy_version",
        "review_kind",
        "effective_review_tier",
        "reviewed_items",
        "source",
        "eligibility",
        "proposal",
        "memory",
        "changed_files",
        "validation_impact",
        "executed_validation",
    }
)
_SOURCE_FIELDS = frozenset(
    {
        "issue_url",
        "issue_body_sha256",
        "source_pr_url",
        "source_pr_title",
        "source_pr_body_sha256",
        "source_head_ref",
        "source_head_sha",
        "source_merge_commit_sha",
    }
)
_PAIR_FIELDS = frozenset({"url", "sha256"})
_MEMORY_FIELDS = frozenset(
    {
        "url",
        "title",
        "body_sha256",
        "head_ref",
        "head_sha",
        "base_ref",
        "base_sha",
    }
)
_REVIEWED_ITEM_FIELDS = frozenset({"id", "tier"})
_CHANGED_FILE_FIELDS = frozenset(
    {"path", "status", "previous_path", "blob_sha"}
)
_VALIDATION_FIELDS = frozenset({"command", "result", "evidence"})
_TIERS = frozenset(
    {
        "r0-no-write",
        "r1-documentary",
        "r2-stable-context",
        "r3-normative",
    }
)
_WRITE_TIERS = _TIERS - {"r0-no-write"}
_TIER_RANK = {
    "r0-no-write": 0,
    "r1-documentary": 1,
    "r2-stable-context": 2,
    "r3-normative": 3,
}
_STATUSES = frozenset({"added", "modified", "removed", "renamed"})
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


def _is_sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _exact_fields(
    value: Mapping[object, object],
    expected: frozenset[str],
    path: str,
) -> None:
    if not all(isinstance(key, str) for key in value) or set(value) != expected:
        raise ValueError(f"{path} must have exactly: {', '.join(sorted(expected))}")


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} must be a non-empty string")
    return value


def _sha256(value: object, path: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{path} must be a lowercase SHA-256")
    return value


def _git_oid(value: object, path: str) -> str:
    if not isinstance(value, str) or _GIT_OID_RE.fullmatch(value) is None:
        raise ValueError(f"{path} must be a lowercase Git object ID")
    return value


def _https_url(value: object, path: str) -> str:
    url = _string(value, path)
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{path} must be an HTTPS URL")
    return url


def _repo_path(value: object, path: str) -> str:
    text = _string(value, path)
    if (
        text.startswith(("/", "\\", "~"))
        or "\\" in text
        or any(part in {"", ".", ".."} for part in text.split("/"))
    ):
        raise ValueError(f"{path} must be a normalized repository-relative path")
    return text


def _pair(value: object, path: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{path} must be a mapping")
    _exact_fields(value, _PAIR_FIELDS, path)
    return {
        "url": _https_url(value.get("url"), f"{path}.url"),
        "sha256": _sha256(value.get("sha256"), f"{path}.sha256"),
    }


def canonicalize_review_input(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return the exact sorted canonical review-input object."""
    if not isinstance(manifest, Mapping):
        raise ValueError("review input must be a mapping")
    _exact_fields(manifest, _TOP_FIELDS, "review_input")
    value = copy.deepcopy(dict(manifest))

    if (
        isinstance(value["review_input_schema_version"], bool)
        or not isinstance(value["review_input_schema_version"], int)
        or value["review_input_schema_version"] != REVIEW_INPUT_SCHEMA_VERSION
    ):
        raise ValueError("review_input_schema_version must equal 1")
    if (
        isinstance(value["review_policy_version"], bool)
        or not isinstance(value["review_policy_version"], int)
        or value["review_policy_version"] != REVIEW_POLICY_VERSION
    ):
        raise ValueError("review_policy_version must equal 1")

    review_kind = value["review_kind"]
    if not isinstance(review_kind, str) or review_kind not in {
        "context-promotion-no-write",
        "context-promotion-write",
    }:
        raise ValueError("review_kind is unknown")
    effective_tier = value["effective_review_tier"]
    allowed_tiers = _TIERS if review_kind.endswith("no-write") else _WRITE_TIERS
    if not isinstance(effective_tier, str) or effective_tier not in allowed_tiers:
        raise ValueError("effective_review_tier is invalid for review_kind")

    reviewed_items = value["reviewed_items"]
    if not _is_sequence(reviewed_items) or not reviewed_items:
        raise ValueError("reviewed_items must be a non-empty list")
    normalized_items: list[dict[str, str]] = []
    for index, item in enumerate(reviewed_items):
        path = f"reviewed_items[{index}]"
        if not isinstance(item, Mapping):
            raise ValueError(f"{path} must be a mapping")
        _exact_fields(item, _REVIEWED_ITEM_FIELDS, path)
        tier = item.get("tier")
        if not isinstance(tier, str) or tier not in _TIERS:
            raise ValueError(f"{path}.tier is unknown")
        normalized_items.append(
            {"id": _string(item.get("id"), f"{path}.id"), "tier": tier}
        )
    normalized_items.sort(key=lambda item: item["id"])
    if len({item["id"] for item in normalized_items}) != len(normalized_items):
        raise ValueError("reviewed_items contains duplicate IDs")
    if max(_TIER_RANK[item["tier"]] for item in normalized_items) > _TIER_RANK[
        effective_tier
    ]:
        raise ValueError(
            "effective_review_tier must not be lower than an item tier"
        )
    if (
        review_kind == "context-promotion-write"
        and all(item["tier"] == "r0-no-write" for item in normalized_items)
    ):
        raise ValueError("write review requires at least one non-R0 item")
    value["reviewed_items"] = normalized_items

    source = value["source"]
    if not isinstance(source, Mapping):
        raise ValueError("source must be a mapping")
    _exact_fields(source, _SOURCE_FIELDS, "source")
    value["source"] = {
        "issue_url": _https_url(source.get("issue_url"), "source.issue_url"),
        "issue_body_sha256": _sha256(
            source.get("issue_body_sha256"), "source.issue_body_sha256"
        ),
        "source_pr_url": _https_url(
            source.get("source_pr_url"), "source.source_pr_url"
        ),
        "source_pr_title": _string(
            source.get("source_pr_title"), "source.source_pr_title"
        ),
        "source_pr_body_sha256": _sha256(
            source.get("source_pr_body_sha256"),
            "source.source_pr_body_sha256",
        ),
        "source_head_ref": _string(
            source.get("source_head_ref"), "source.source_head_ref"
        ),
        "source_head_sha": _git_oid(
            source.get("source_head_sha"), "source.source_head_sha"
        ),
        "source_merge_commit_sha": _git_oid(
            source.get("source_merge_commit_sha"),
            "source.source_merge_commit_sha",
        ),
    }
    value["eligibility"] = _pair(value["eligibility"], "eligibility")
    value["proposal"] = _pair(value["proposal"], "proposal")

    memory = value["memory"]
    if memory is None:
        if review_kind != "context-promotion-no-write":
            raise ValueError("write review requires memory")
    else:
        if review_kind != "context-promotion-write":
            raise ValueError("no-write review requires memory: null")
        if not isinstance(memory, Mapping):
            raise ValueError("memory must be a mapping or null")
        _exact_fields(memory, _MEMORY_FIELDS, "memory")
        if memory.get("base_ref") != "develop":
            raise ValueError("memory.base_ref must equal develop")
        value["memory"] = {
            "url": _https_url(memory.get("url"), "memory.url"),
            "title": _string(memory.get("title"), "memory.title"),
            "body_sha256": _sha256(
                memory.get("body_sha256"), "memory.body_sha256"
            ),
            "head_ref": _string(memory.get("head_ref"), "memory.head_ref"),
            "head_sha": _git_oid(memory.get("head_sha"), "memory.head_sha"),
            "base_ref": "develop",
            "base_sha": _git_oid(memory.get("base_sha"), "memory.base_sha"),
        }

    changed_files = value["changed_files"]
    if not _is_sequence(changed_files):
        raise ValueError("changed_files must be a list")
    normalized_files: list[dict[str, object]] = []
    for index, item in enumerate(changed_files):
        path = f"changed_files[{index}]"
        if not isinstance(item, Mapping):
            raise ValueError(f"{path} must be a mapping")
        _exact_fields(item, _CHANGED_FILE_FIELDS, path)
        status = item.get("status")
        if not isinstance(status, str) or status not in _STATUSES:
            raise ValueError(f"{path}.status is unknown")
        current_path = _repo_path(item.get("path"), f"{path}.path")
        previous_path = item.get("previous_path")
        if status == "renamed":
            previous_path = _repo_path(
                previous_path, f"{path}.previous_path"
            )
            if previous_path == current_path:
                raise ValueError(f"{path} rename paths must differ")
        elif previous_path is not None:
            raise ValueError(f"{path}.previous_path must be null")
        blob_sha = item.get("blob_sha")
        if status == "removed":
            if blob_sha is not None:
                raise ValueError(f"{path}.blob_sha must be null for removed")
        else:
            blob_sha = _git_oid(blob_sha, f"{path}.blob_sha")
        normalized_files.append(
            {
                "path": current_path,
                "status": status,
                "previous_path": previous_path,
                "blob_sha": blob_sha,
            }
        )
    normalized_files.sort(
        key=lambda item: (
            str(item["path"]),
            str(item["status"]),
            str(item["previous_path"] or ""),
            str(item["blob_sha"] or ""),
        )
    )
    if len({item["path"] for item in normalized_files}) != len(
        normalized_files
    ):
        raise ValueError("changed_files contains duplicate paths")
    if review_kind == "context-promotion-no-write" and normalized_files:
        raise ValueError("no-write review requires changed_files: []")
    if review_kind == "context-promotion-write" and not normalized_files:
        raise ValueError("write review requires non-empty changed_files")
    value["changed_files"] = normalized_files

    impact = value["validation_impact"]
    if impact is not None:
        if review_kind == "context-promotion-no-write":
            raise ValueError("no-write review requires validation_impact: null")
        value["validation_impact"] = _pair(
            impact, "validation_impact"
        )

    executed = value["executed_validation"]
    if not _is_sequence(executed):
        raise ValueError("executed_validation must be a list")
    normalized_validation: list[dict[str, str]] = []
    for index, item in enumerate(executed):
        path = f"executed_validation[{index}]"
        if not isinstance(item, Mapping):
            raise ValueError(f"{path} must be a mapping")
        _exact_fields(item, _VALIDATION_FIELDS, path)
        if item.get("result") != "PASS":
            raise ValueError(f"{path}.result must equal PASS")
        normalized_validation.append(
            {
                "command": _string(item.get("command"), f"{path}.command"),
                "result": "PASS",
                "evidence": _string(item.get("evidence"), f"{path}.evidence"),
            }
        )
    normalized_validation.sort(
        key=lambda item: (
            item["command"],
            item["result"],
            item["evidence"],
        )
    )
    value["executed_validation"] = normalized_validation

    return value


def review_input_sha256(manifest: Mapping[str, Any]) -> str:
    """Return the SHA-256 of the strict canonical review-input manifest."""
    canonical = canonicalize_review_input(manifest)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()
