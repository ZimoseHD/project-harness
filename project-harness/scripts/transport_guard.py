#!/usr/bin/env python3
"""Pure guards for deterministic Pull Request transport decisions.

This module does not call GitHub. It makes the conflict, idempotency, candidate,
read-back, and ambiguous-recovery rules executable so a transport caller can
validate snapshots obtained through its single authenticated GitHub transport.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal

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

EXACT_MERGE_FIELDS = (
    "title",
    "body_sha256",
    "head_ref",
    "head_sha",
    "base_ref",
    "base_sha",
)

MergeDecision = Literal["proceed", "no-op", "blocked", "indeterminate"]
MergeKind = Literal["product", "memory"]

PRODUCT_MERGE_EVIDENCE_NAMES = (
    "closeout-pass",
    "issue-callback",
    "eligibility-registration",
)

MEMORY_MERGE_EVIDENCE_NAMES = (
    "proposal-artifact",
    "confirmation",
    "reviewer-pass",
    "memory-pr-ready",
)

MERGE_EVIDENCE_NAMES: Mapping[str, tuple[str, ...]] = {
    "product": PRODUCT_MERGE_EVIDENCE_NAMES,
    "memory": MEMORY_MERGE_EVIDENCE_NAMES,
}

SUPPORTED_MERGE_METHODS = frozenset({"merge", "squash", "rebase"})
SUPPORTED_MERGE_PROVENANCE_SOURCES = frozenset(
    {"merge-event", "commit-provenance", "mutation-readback"}
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


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _guarded_base_matches(
    expected: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    allow_live_base_advance: bool,
) -> bool:
    """Verify an open base or transport-produced post-merge provenance."""
    expected_base_sha = expected.get("base_sha")
    live_base_sha = current.get("base_sha")

    if not _nonempty_string(expected_base_sha):
        return False
    if not allow_live_base_advance:
        return live_base_sha == expected_base_sha

    provenance = current.get("merge_provenance")
    return (
        isinstance(provenance, Mapping)
        and provenance.get("verified") is True
        and provenance.get("source") in SUPPORTED_MERGE_PROVENANCE_SOURCES
        and provenance.get("guarded_base_sha") == expected_base_sha
        and provenance.get("guarded_head_sha") == expected.get("head_sha")
        and provenance.get("merge_commit_sha") == current.get("merge_commit_sha")
    )


def _exact_merge_tuple_matches(
    expected: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    allow_live_base_advance: bool,
) -> bool:
    """Return true only for a complete, exact guarded merge tuple."""
    return all(
        _nonempty_string(expected.get(field))
        and current.get(field) == expected.get(field)
        for field in EXACT_MERGE_FIELDS
        if field != "base_sha"
    ) and _guarded_base_matches(
        expected,
        current,
        allow_live_base_advance=allow_live_base_advance,
    )


def _required_checks_succeeded(current: Mapping[str, Any]) -> bool:
    """Validate the normalized required-check map in a PR/check snapshot."""
    if current.get("required_checks_known") is not True:
        return False

    required_checks = current.get("required_checks")
    if not isinstance(required_checks, Mapping):
        return False

    return all(
        _nonempty_string(name) and status == "success"
        for name, status in required_checks.items()
    )


def _evidence_pair_is_complete(pair: Any) -> bool:
    return (
        isinstance(pair, tuple)
        and len(pair) == 2
        and _nonempty_string(pair[0])
        and isinstance(pair[1], str)
        and len(pair[1]) == 64
        and all(character in "0123456789abcdef" for character in pair[1])
    )


def _persistent_evidence_matches(
    required_evidence_names: Iterable[str],
    expected_evidence: Mapping[str, tuple[str, str]],
    current_evidence: Mapping[str, tuple[str, str]],
) -> bool:
    """Validate exact evidence-key sets and freshly read URL/digest values."""
    names = tuple(required_evidence_names)
    if (
        not names
        or any(not _nonempty_string(name) for name in names)
        or len(set(names)) != len(names)
        or set(expected_evidence) != set(names)
        or set(current_evidence) != set(names)
    ):
        return False

    return all(
        _evidence_pair_is_complete(expected_evidence[name])
        and _evidence_pair_is_complete(current_evidence[name])
        and current_evidence[name] == expected_evidence[name]
        for name in names
    )


def exact_merge_guard(
    expected: Mapping[str, Any],
    current: Mapping[str, Any],
    required_evidence: Mapping[str, tuple[str, str]],
    merge_method: str,
    *,
    merge_kind: MergeKind,
    current_evidence: Mapping[str, tuple[str, str]],
    ambiguous_mutation: bool = False,
) -> MergeDecision:
    """Decide whether an exact, evidence-gated Pull Request merge may proceed.

    ``expected`` must contain non-empty ``title``, ``body_sha256``, ``head_ref``,
    ``head_sha``, ``base_ref``, and ``base_sha`` values. ``current`` is the
    independently fetched PR/check snapshot and must contain a normalized
    ``required_checks`` mapping from required check name to exact status.
    ``merge_kind`` selects the protocol-owned exact product or memory gate-key
    set; callers cannot weaken that set. ``required_evidence`` maps those keys
    to expected immutable
    ``(url, sha256_digest)`` pairs; ``current_evidence`` contains the same
    pairs from an independent read immediately before the decision.

    For a merged read, ``current.merge_provenance`` must be a verified record
    produced by the selected transport; copying the expected base into that
    field is not evidence. This pure guard does not decide which evidence or
    merge method is authoritative and never performs the merge.
    """
    required_evidence_names = MERGE_EVIDENCE_NAMES.get(merge_kind)
    if required_evidence_names is None:
        return "indeterminate" if ambiguous_mutation else "blocked"
    if expected.get("base_ref") != "develop":
        return "indeterminate" if ambiguous_mutation else "blocked"

    is_merged_snapshot = (
        current.get("state") == "closed" and current.get("merged") is True
    )
    tuple_matches = _exact_merge_tuple_matches(
        expected,
        current,
        allow_live_base_advance=is_merged_snapshot,
    )
    evidence_matches = _persistent_evidence_matches(
        required_evidence_names,
        required_evidence,
        current_evidence,
    )
    merge_method_is_known = merge_method in SUPPORTED_MERGE_METHODS
    exact_merged_identity = (
        tuple_matches
        and is_merged_snapshot
        and current.get("is_draft") is False
        and _required_checks_succeeded(current)
        and _nonempty_string(current.get("merge_commit_sha"))
        and current.get("merge_method") == merge_method
    )

    if ambiguous_mutation:
        if exact_merged_identity and evidence_matches and merge_method_is_known:
            return "no-op"
        return "indeterminate"

    if exact_merged_identity:
        if evidence_matches and merge_method_is_known:
            return "no-op"
        return "blocked"

    if current.get("state") != "open" or current.get("merged") is not False:
        return "blocked"
    if current.get("is_draft") is not False:
        return "blocked"
    if not tuple_matches:
        return "blocked"
    if not _required_checks_succeeded(current):
        return "blocked"
    if current.get("mergeable") is not True:
        return "blocked"
    if not merge_method_is_known:
        return "blocked"
    if not evidence_matches:
        return "blocked"

    return "proceed"
