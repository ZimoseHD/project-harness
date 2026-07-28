#!/usr/bin/env python3
"""Pure guards for deterministic Pull Request transport decisions.

This module does not call GitHub. It makes the conflict, idempotency, candidate,
read-back, and ambiguous-recovery rules executable so a transport caller can
validate snapshots obtained through its single authenticated GitHub transport.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from markdown_digest import markdown_sha256


DEFAULT_PROTECTED_FIELDS = (
    "repository",
    "pr_number",
    "state",
    "is_draft",
    "head_ref",
    "head_sha",
    "base_ref",
    "base_sha",
    "body_sha256",
)


def content_decision(current: str, desired: str) -> str:
    """Classify an exact replacement as idempotent or mutation-requiring."""
    if markdown_sha256(current) == markdown_sha256(desired):
        return "no-op"
    return "mutation-required"


def changed_protected_fields(
    baseline: Mapping[str, Any],
    latest: Mapping[str, Any],
    fields: Iterable[str] = DEFAULT_PROTECTED_FIELDS,
) -> list[str]:
    """List protected baseline fields that changed or disappeared."""
    return [field for field in fields if baseline.get(field) != latest.get(field)]


def select_active_candidate(candidates: Iterable[Mapping[str, Any]]) -> dict[str, Any] | None:
    """Return the sole open candidate, or fail closed on ambiguity."""
    active = [dict(candidate) for candidate in candidates if candidate.get("state") == "open"]
    if not active:
        return None
    if len(active) != 1:
        raise ValueError("ambiguous active Pull Request candidates")
    return active[0]


def verify_readback(
    expected: Mapping[str, Any],
    actual: Mapping[str, Any],
    fields: Iterable[str],
) -> tuple[bool, list[str]]:
    """Verify every requested/protected field after a mutation."""
    mismatches = [field for field in fields if expected.get(field) != actual.get(field)]
    return not mismatches, mismatches


def recover_ambiguous_mutation(
    expected: Mapping[str, Any],
    actual: Mapping[str, Any],
    fields: Iterable[str],
    *,
    operation_evidence: bool,
) -> str:
    """Recover only when exact state and independent operation evidence agree."""
    matches, _ = verify_readback(expected, actual, fields)
    if operation_evidence and matches:
        return "verified"
    return "indeterminate"
