#!/usr/bin/env python3
"""Executable normal and failure-path checks for delivery log guards."""

from __future__ import annotations

import copy
from hashlib import sha256
import json
import unittest

from delivery_log import (
    BOUNDARY_OUTCOMES,
    BOUNDARY_STAGE_MAP,
    COMMON_BOUNDARIES,
    NO_WRITE_BOUNDARIES,
    WRITE_BOUNDARIES,
    coverage,
    transition_key,
    validate_new_observation,
    validate_observation,
)


ISSUE_URL = "https://github.example/owner/repo/issues/7"
PRODUCT_PR_URL = "https://github.example/owner/repo/pull/9"
MEMORY_PR_URL = "https://github.example/owner/memory/pull/10"
LIVE_ATTEMPT_ID = "550e8400-e29b-41d4-a716-446655440000"
OTHER_ATTEMPT_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

BOUNDARY_ACTIVITIES = {
    "implementation-verified-draft": "initial",
    "closeout-accepted-ready": "accept",
    "product-merged": "integrate",
    "context-proposal-reviewed": "propose",
    "context-confirmed": "confirm",
    "context-no-promotion-terminal": "reconcile",
    "memory-pr-ready": "finalize",
    "memory-pr-merged": "integrate",
    "context-memory-terminal": "reconcile",
    "finalization-ready": "closure-gate",
    "issue-closed": "finalize",
}


def canonical_sha256(value: object) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def evidence(kind: str, url: str, digest: str) -> dict[str, str]:
    return {"kind": kind, "url": url, "sha256": digest}


class DeliveryLogTests(unittest.TestCase):
    def product_tuple(self) -> dict[str, object]:
        return {
            "product_pr_url": PRODUCT_PR_URL,
            "product_pr_title": "Deliver feature",
            "product_pr_body_sha256": "b" * 64,
            "head_ref": "task/7",
            "head_sha": "1" * 40,
            "base_ref": "develop",
            "base_sha": "2" * 40,
        }

    def memory_tuple(self) -> dict[str, object]:
        return {
            "memory_pr_url": MEMORY_PR_URL,
            "memory_pr_title": "Promote durable context",
            "memory_pr_body_sha256": "3" * 64,
            "memory_head_ref": "memory/7",
            "memory_head_sha": "4" * 40,
            "memory_base_ref": "develop",
            "memory_base_sha": "5" * 40,
        }

    def comment_pair(self, name: str, digit: str) -> tuple[str, str]:
        return (
            f"{PRODUCT_PR_URL}#issuecomment-{name}",
            digit * 64,
        )

    def proposal_state(self) -> dict[str, str]:
        artifact_url, artifact_sha = self.comment_pair("proposal", "6")
        callback_url, callback_sha = self.comment_pair("proposal-callback", "7")
        review_url, review_sha = self.comment_pair("review", "8")
        confirmation_url, confirmation_sha = self.comment_pair("confirmation", "9")
        return {
            "proposal_artifact_url": artifact_url,
            "proposal_artifact_sha256": artifact_sha,
            "proposal_comment_url": callback_url,
            "proposal_comment_sha256": callback_sha,
            "review_url": review_url,
            "review_sha256": review_sha,
            "confirmation_comment_url": confirmation_url,
            "confirmation_comment_sha256": confirmation_sha,
        }

    def boundary_snapshots(
        self,
        boundary: str,
        *,
        memory_write: bool,
    ) -> tuple[dict[str, object], dict[str, object], list[dict[str, str]]]:
        product = self.product_tuple()
        memory = self.memory_tuple()
        proposal = self.proposal_state()
        acceptance_url, acceptance_sha = self.comment_pair("acceptance", "a")
        callback_url, callback_sha = self.comment_pair("issue-callback", "c")
        eligibility_url, eligibility_sha = self.comment_pair("eligibility", "d")
        ready_url, ready_sha = self.comment_pair("ready", "e")
        terminal_url, terminal_sha = self.comment_pair("terminal", "f")

        if boundary == "implementation-verified-draft":
            input_snapshot = {
                "base_ref": "develop",
                "base_sha": "2" * 40,
                "prior_head_sha": None,
            }
            output_snapshot = product
            required = [
                evidence(
                    "product-pr",
                    str(product["product_pr_url"]),
                    str(product["product_pr_body_sha256"]),
                )
            ]
        elif boundary == "closeout-accepted-ready":
            input_snapshot = product
            output_snapshot = {
                "acceptance_comment_url": acceptance_url,
                "acceptance_comment_sha256": acceptance_sha,
                "issue_callback_url": callback_url,
                "issue_callback_sha256": callback_sha,
                "eligibility_registration_url": eligibility_url,
                "eligibility_registration_sha256": eligibility_sha,
                "pr_state": "ready",
            }
            required = [
                evidence("product-pr", PRODUCT_PR_URL, "b" * 64),
                evidence("acceptance-comment", acceptance_url, acceptance_sha),
                evidence("issue-callback", callback_url, callback_sha),
                evidence(
                    "eligibility-registration", eligibility_url, eligibility_sha
                ),
            ]
        elif boundary == "product-merged":
            input_snapshot = {
                **product,
                "acceptance_comment_url": acceptance_url,
                "acceptance_comment_sha256": acceptance_sha,
                "issue_callback_url": callback_url,
                "issue_callback_sha256": callback_sha,
                "eligibility_registration_url": eligibility_url,
                "eligibility_registration_sha256": eligibility_sha,
            }
            output_snapshot = {
                "merge_method": "squash",
                "merge_commit_sha": "6" * 40,
                "merged_head_sha": "1" * 40,
                "merged_base_ref": "develop",
            }
            required = [
                evidence("product-pr", PRODUCT_PR_URL, "b" * 64),
                evidence("acceptance-comment", acceptance_url, acceptance_sha),
                evidence("issue-callback", callback_url, callback_sha),
                evidence(
                    "eligibility-registration", eligibility_url, eligibility_sha
                ),
            ]
        elif boundary == "context-proposal-reviewed":
            input_snapshot = {
                "product_pr_url": PRODUCT_PR_URL,
                "source_head_sha": "1" * 40,
                "source_merge_commit_sha": "6" * 40,
                "eligibility_registration_url": eligibility_url,
                "eligibility_registration_sha256": eligibility_sha,
                "authority_base_sha": "7" * 40,
            }
            memory_values = memory if memory_write else {
                field: None for field in memory
            }
            output_snapshot = {
                "proposal_artifact_url": proposal["proposal_artifact_url"],
                "proposal_artifact_sha256": proposal[
                    "proposal_artifact_sha256"
                ],
                "proposal_comment_url": proposal["proposal_comment_url"],
                "proposal_comment_sha256": proposal[
                    "proposal_comment_sha256"
                ],
                "review_url": proposal["review_url"],
                "review_sha256": proposal["review_sha256"],
                **memory_values,
            }
            required = [
                evidence(
                    "eligibility-registration", eligibility_url, eligibility_sha
                ),
                evidence(
                    "proposal-artifact",
                    proposal["proposal_artifact_url"],
                    proposal["proposal_artifact_sha256"],
                ),
                evidence(
                    "proposal-callback",
                    proposal["proposal_comment_url"],
                    proposal["proposal_comment_sha256"],
                ),
                evidence(
                    "review", proposal["review_url"], proposal["review_sha256"]
                ),
            ]
            if memory_write:
                required.append(evidence("memory-pr", MEMORY_PR_URL, "3" * 64))
        elif boundary == "context-confirmed":
            memory_values = memory if memory_write else {
                field: None for field in memory
            }
            input_snapshot = {
                "proposal_artifact_url": proposal["proposal_artifact_url"],
                "proposal_artifact_sha256": proposal[
                    "proposal_artifact_sha256"
                ],
                "proposal_comment_url": proposal["proposal_comment_url"],
                "proposal_comment_sha256": proposal[
                    "proposal_comment_sha256"
                ],
                "review_url": proposal["review_url"],
                "review_sha256": proposal["review_sha256"],
                **memory_values,
            }
            output_snapshot = {
                "confirmation_comment_url": proposal["confirmation_comment_url"],
                "confirmation_comment_sha256": proposal[
                    "confirmation_comment_sha256"
                ],
                "decision": "approved",
            }
            required = [
                evidence(
                    "proposal-artifact",
                    proposal["proposal_artifact_url"],
                    proposal["proposal_artifact_sha256"],
                ),
                evidence(
                    "proposal-callback",
                    proposal["proposal_comment_url"],
                    proposal["proposal_comment_sha256"],
                ),
                evidence(
                    "review", proposal["review_url"], proposal["review_sha256"]
                ),
                evidence(
                    "confirmation-callback",
                    proposal["confirmation_comment_url"],
                    proposal["confirmation_comment_sha256"],
                ),
            ]
            if memory_write:
                required.append(evidence("memory-pr", MEMORY_PR_URL, "3" * 64))
        elif boundary == "context-no-promotion-terminal":
            input_snapshot = proposal
            output_snapshot = {
                "terminal_comment_url": terminal_url,
                "terminal_comment_sha256": terminal_sha,
                "terminal_outcome": "no-promotion",
            }
            required = [
                evidence(
                    "proposal-artifact",
                    proposal["proposal_artifact_url"],
                    proposal["proposal_artifact_sha256"],
                ),
                evidence(
                    "confirmation-callback",
                    proposal["confirmation_comment_url"],
                    proposal["confirmation_comment_sha256"],
                ),
                evidence("terminal-callback", terminal_url, terminal_sha),
            ]
        elif boundary == "memory-pr-ready":
            input_snapshot = proposal
            output_snapshot = {
                **memory,
                "ready_comment_url": ready_url,
                "ready_comment_sha256": ready_sha,
            }
            required = [
                evidence(
                    "proposal-artifact",
                    proposal["proposal_artifact_url"],
                    proposal["proposal_artifact_sha256"],
                ),
                evidence(
                    "review", proposal["review_url"], proposal["review_sha256"]
                ),
                evidence(
                    "confirmation-callback",
                    proposal["confirmation_comment_url"],
                    proposal["confirmation_comment_sha256"],
                ),
                evidence("memory-pr", MEMORY_PR_URL, "3" * 64),
                evidence("ready-callback", ready_url, ready_sha),
            ]
        elif boundary == "memory-pr-merged":
            input_snapshot = {
                **memory,
                "ready_comment_url": ready_url,
                "ready_comment_sha256": ready_sha,
            }
            output_snapshot = {
                "merge_method": "squash",
                "merge_commit_sha": "8" * 40,
                "merged_head_sha": "4" * 40,
                "merged_base_ref": "develop",
            }
            required = [
                evidence("memory-pr", MEMORY_PR_URL, "3" * 64),
                evidence("ready-callback", ready_url, ready_sha),
            ]
        elif boundary == "context-memory-terminal":
            input_snapshot = {
                "memory_pr_url": MEMORY_PR_URL,
                "memory_pr_body_sha256": "3" * 64,
                "memory_head_sha": "4" * 40,
                "merge_method": "squash",
                "merge_commit_sha": "8" * 40,
                "ready_comment_url": ready_url,
                "ready_comment_sha256": ready_sha,
            }
            output_snapshot = {
                "terminal_comment_url": terminal_url,
                "terminal_comment_sha256": terminal_sha,
                "terminal_outcome": "memory-pr-merged",
            }
            required = [
                evidence("memory-pr", MEMORY_PR_URL, "3" * 64),
                evidence("ready-callback", ready_url, ready_sha),
                evidence("terminal-callback", terminal_url, terminal_sha),
            ]
        elif boundary == "finalization-ready":
            return self.finalization_snapshots(memory_write=memory_write)
        elif boundary == "issue-closed":
            final_url, final_sha = self.comment_pair("finalization", "0")
            finalization_input, _, _ = self.finalization_snapshots(
                memory_write=memory_write
            )
            input_snapshot = {
                "path_kind": "memory-write" if memory_write else "no-write",
                "coverage_manifest_sha256": finalization_input[
                    "coverage_manifest_sha256"
                ],
                "finalization_observation_url": final_url,
                "finalization_observation_sha256": final_sha,
            }
            output_snapshot = {"state": "closed", "state_reason": "completed"}
            required = [evidence("finalization-observation", final_url, final_sha)]
        else:
            raise AssertionError(f"unknown test boundary: {boundary}")

        return input_snapshot, output_snapshot, required

    def finalization_snapshots(
        self,
        *,
        memory_write: bool,
    ) -> tuple[dict[str, object], dict[str, object], list[dict[str, str]]]:
        path_kind = "memory-write" if memory_write else "no-write"
        boundaries = COMMON_BOUNDARIES + (
            WRITE_BOUNDARIES if memory_write else NO_WRITE_BOUNDARIES
        )
        entries: list[dict[str, object]] = []
        for index, boundary in enumerate(boundaries):
            observation_url = f"{ISSUE_URL}#issuecomment-stage-{index}"
            _, _, boundary_evidence = self.boundary_snapshots(
                boundary,
                memory_write=memory_write,
            )
            entry_evidence = sorted(
                boundary_evidence,
                key=lambda item: (item["kind"], item["url"], item["sha256"]),
            )
            entries.append(
                {
                    "boundary": boundary,
                    "observation_url": observation_url,
                    "observation_sha256": format(index + 2, "x") * 64,
                    "transition_key": format(index + 3, "x") * 64,
                    "evidence": entry_evidence,
                }
            )
        manifest = {
            "manifest_schema_version": 1,
            "path_kind": path_kind,
            "issue_url": ISSUE_URL,
            "issue_body_sha256": "a" * 64,
            "entries": entries,
        }
        top_evidence = [
            evidence(
                "stage-observation",
                str(entry["observation_url"]),
                str(entry["observation_sha256"]),
            )
            for entry in entries
        ]
        top_evidence.extend(
            item
            for item in entries[-1]["evidence"]  # type: ignore[union-attr]
            if item["kind"] == "terminal-callback"
        )
        return (
            {
                "path_kind": path_kind,
                "coverage_manifest": manifest,
                "coverage_manifest_sha256": canonical_sha256(manifest),
            },
            {"ready": True},
            top_evidence,
        )

    def change_summary(self) -> dict[str, object]:
        return {
            "repository_changes": [
                {
                    "path": "src/service.py",
                    "status": "modified",
                    "previous_path": None,
                    "additions": 3,
                    "deletions": 1,
                    "before_blob_sha": "1" * 40,
                    "after_blob_sha": "2" * 40,
                }
            ],
            "github_mutations": [
                {
                    "operation": "add-comment",
                    "target_url": ISSUE_URL,
                    "before": None,
                    "after": "comment-created",
                    "result_url": f"{ISSUE_URL}#issuecomment-10",
                    "result_sha256": "c" * 64,
                }
            ],
            "context_changes": [],
            "truncated": False,
            "omitted_count": 0,
        }

    def issue_close_summary(self) -> dict[str, object]:
        return {
            "repository_changes": [],
            "github_mutations": [
                {
                    "operation": "change-metadata",
                    "target_url": ISSUE_URL,
                    "before": "open",
                    "after": "closed/completed",
                    "result_url": ISSUE_URL,
                    "result_sha256": None,
                }
            ],
            "context_changes": [],
            "truncated": False,
            "omitted_count": 0,
        }

    def observation(
        self,
        boundary_name: str = "implementation-verified-draft",
        *,
        memory_write: bool = False,
        **overrides: object,
    ) -> dict[str, object]:
        input_snapshot, output_snapshot, required = self.boundary_snapshots(
            boundary_name,
            memory_write=memory_write,
        )
        record: dict[str, object] = {
            "record_kind": "delivery-stage-observation",
            "log_schema_version": 1,
            "observation_kind": "boundary",
            "transition_key": "0" * 64,
            "attempt_id": LIVE_ATTEMPT_ID,
            "boundary": boundary_name,
            "stage": BOUNDARY_STAGE_MAP[boundary_name],
            "activity": BOUNDARY_ACTIVITIES[boundary_name],
            "attempt": 1,
            "outcome": (
                "verified"
                if boundary_name == "issue-closed"
                else sorted(BOUNDARY_OUTCOMES[boundary_name])[0]
            ),
            "issue_url": ISSUE_URL,
            "issue_body_sha256": "a" * 64,
            "observed_at": "2026-07-28T10:00:02.250Z",
            "started_at": "2026-07-28T10:00:00Z",
            "finished_at": "2026-07-28T10:00:02Z",
            "elapsed_ms": 2000,
            "timing_scope": "coordinator-wall",
            "timing_quality": "measured",
            "user_wait_ms": None,
            "change_quality": {
                "repository": "measured",
                "github": "measured",
                "context": "measured",
            },
            "input_snapshot": input_snapshot,
            "output_snapshot": output_snapshot,
            "change_summary": (
                self.issue_close_summary()
                if boundary_name == "issue-closed"
                else self.change_summary()
            ),
            "evidence": sorted(
                required,
                key=lambda item: (item["kind"], item["url"], item["sha256"]),
            ),
            "raw_user_input_persisted": False,
            "reason_code": "stage-complete",
        }
        record.update(overrides)
        record["transition_key"] = transition_key(record)
        return record

    def attempt(self, **overrides: object) -> dict[str, object]:
        source = evidence("product-pr", PRODUCT_PR_URL, "b" * 64)
        result_url = f"{ISSUE_URL}#issuecomment-blocked"
        result_sha = "d" * 64
        record: dict[str, object] = {
            "record_kind": "delivery-stage-observation",
            "log_schema_version": 1,
            "observation_kind": "attempt",
            "transition_key": "0" * 64,
            "attempt_id": LIVE_ATTEMPT_ID,
            "boundary": None,
            "stage": "implementation",
            "activity": "repair",
            "attempt": 2,
            "outcome": "blocked",
            "issue_url": ISSUE_URL,
            "issue_body_sha256": "a" * 64,
            "observed_at": "2026-07-28T10:00:02.250Z",
            "started_at": "2026-07-28T10:00:00Z",
            "finished_at": "2026-07-28T10:00:02Z",
            "elapsed_ms": 2000,
            "timing_scope": "coordinator-wall",
            "timing_quality": "measured",
            "user_wait_ms": None,
            "change_quality": {
                "repository": "reconstructed",
                "github": "reconstructed",
                "context": "not-applicable",
            },
            "input_snapshot": {
                "target_boundary": "implementation-verified-draft",
                "source_bindings": [source],
            },
            "output_snapshot": {
                "result_kind": "blocked",
                "result_url": result_url,
                "result_sha256": result_sha,
                "response_kind": None,
                "modification_item_count": None,
            },
            "change_summary": self.change_summary(),
            "evidence": [
                evidence("blocked", result_url, result_sha),
                source,
            ],
            "raw_user_input_persisted": False,
            "reason_code": "required-check-failed",
        }
        record.update(overrides)
        record["transition_key"] = transition_key(record)
        return record

    def test_all_boundary_schemas_and_attempt_are_valid(self) -> None:
        no_write = COMMON_BOUNDARIES + NO_WRITE_BOUNDARIES
        memory_write = COMMON_BOUNDARIES + WRITE_BOUNDARIES
        for boundary in no_write + ("finalization-ready", "issue-closed"):
            with self.subTest(path="no-write", boundary=boundary):
                self.assertEqual(
                    validate_observation(self.observation(boundary)),
                    [],
                )
        for boundary in memory_write + ("finalization-ready", "issue-closed"):
            with self.subTest(path="memory-write", boundary=boundary):
                self.assertEqual(
                    validate_observation(
                        self.observation(boundary, memory_write=True)
                    ),
                    [],
                )
        self.assertEqual(validate_observation(self.attempt()), [])

    def test_schema_snapshot_and_evidence_fail_closed(self) -> None:
        invalid = self.observation()
        invalid["log_schema_version"] = 2
        invalid["input_snapshot"]["unexpected"] = "value"  # type: ignore[index]
        invalid["evidence"] = []
        errors = validate_observation(invalid)
        self.assertTrue(any("log_schema_version" in error for error in errors))
        self.assertTrue(any("input_snapshot.unexpected" in error for error in errors))
        self.assertTrue(
            any(
                "requires exactly its canonical snapshot bindings" in error
                for error in errors
            )
        )

        duplicate_evidence = self.observation()
        duplicate_evidence["evidence"].append(  # type: ignore[union-attr]
            copy.deepcopy(duplicate_evidence["evidence"][0])  # type: ignore[index]
        )
        self.assertTrue(
            any(
                "requires exactly its canonical snapshot bindings" in error
                for error in validate_observation(duplicate_evidence)
            )
        )

        partial_memory = self.observation(
            "context-proposal-reviewed",
            memory_write=True,
        )
        partial_memory["output_snapshot"]["memory_head_sha"] = None  # type: ignore[index]
        self.assertTrue(
            any(
                "must be all-null or complete" in error
                for error in validate_observation(partial_memory)
            )
        )

    def test_attempt_snapshot_response_and_attempt_id_rules(self) -> None:
        invalid = self.attempt()
        invalid["attempt_id"] = None
        invalid["output_snapshot"]["result_sha256"] = None  # type: ignore[index]
        invalid["evidence"] = []
        errors = validate_observation(invalid)
        self.assertTrue(any("attempt observations require" in error for error in errors))
        self.assertTrue(any("must both be null or both populated" in error for error in errors))
        self.assertTrue(any("must exactly equal" in error for error in errors))

        source = evidence(
            "proposal-callback",
            f"{PRODUCT_PR_URL}#proposal-callback",
            "6" * 64,
        )
        response = self.attempt(
            stage="context-confirmation",
            activity="confirm",
            outcome="paused",
            change_quality={
                "repository": "not-applicable",
                "github": "not-applicable",
                "context": "not-applicable",
            },
            input_snapshot={
                "target_boundary": "context-confirmed",
                "source_bindings": [source],
            },
            output_snapshot={
                "result_kind": "paused",
                "result_url": None,
                "result_sha256": None,
                "response_kind": "paused",
                "modification_item_count": 2,
            },
            change_summary={
                "repository_changes": [],
                "github_mutations": [],
                "context_changes": [],
                "truncated": False,
                "omitted_count": 0,
            },
            evidence=[source],
        )
        self.assertEqual(validate_observation(response), [])
        self.assertTrue(
            any(
                "paused requires zero" in error
                for error in validate_new_observation(response)
            )
        )

        response["output_snapshot"]["modification_item_count"] = 0  # type: ignore[index]
        response["transition_key"] = transition_key(response)
        self.assertEqual(validate_new_observation(response), [])

        mutating_response = copy.deepcopy(response)
        mutating_response["change_quality"] = {
            "repository": "reconstructed",
            "github": "reconstructed",
            "context": "not-applicable",
        }
        mutating_response["change_summary"] = self.change_summary()
        mutating_response["transition_key"] = transition_key(mutating_response)
        self.assertEqual(validate_observation(mutating_response), [])
        mutating_errors = validate_new_observation(mutating_response)
        self.assertTrue(
            any(
                "all domains not-applicable" in error
                for error in mutating_errors
            )
        )
        self.assertTrue(
            any(
                "requires no reported mutations" in error
                for error in mutating_errors
            )
        )

        unbound = copy.deepcopy(response)
        unbound["input_snapshot"]["source_bindings"] = []  # type: ignore[index]
        unbound["evidence"] = []
        unbound["transition_key"] = transition_key(unbound)
        self.assertEqual(validate_observation(unbound), [])
        self.assertTrue(
            any(
                "requires exactly one proposal-callback binding" in error
                for error in validate_new_observation(unbound)
            )
        )

        unbound_blocked = copy.deepcopy(unbound)
        unbound_blocked["outcome"] = "blocked"
        unbound_blocked["output_snapshot"]["result_kind"] = "blocked"  # type: ignore[index]
        unbound_blocked["output_snapshot"]["response_kind"] = None  # type: ignore[index]
        unbound_blocked["output_snapshot"]["modification_item_count"] = None  # type: ignore[index]
        unbound_blocked["transition_key"] = transition_key(unbound_blocked)
        self.assertEqual(validate_observation(unbound_blocked), [])
        self.assertTrue(
            any(
                "new confirmation attempt requires exactly one "
                "proposal-callback binding" in error
                for error in validate_new_observation(unbound_blocked)
            )
        )

        bound_blocked = copy.deepcopy(unbound_blocked)
        bound_blocked["input_snapshot"]["source_bindings"] = [source]  # type: ignore[index]
        bound_blocked["evidence"] = [source]
        bound_blocked["transition_key"] = transition_key(bound_blocked)
        self.assertEqual(validate_new_observation(bound_blocked), [])

        wrong_binding = copy.deepcopy(response)
        wrong_source = evidence(
            "proposal-artifact",
            f"{PRODUCT_PR_URL}#proposal",
            "7" * 64,
        )
        wrong_binding["input_snapshot"]["source_bindings"] = [wrong_source]  # type: ignore[index]
        wrong_binding["evidence"] = [wrong_source]
        wrong_binding["transition_key"] = transition_key(wrong_binding)
        self.assertEqual(validate_observation(wrong_binding), [])
        self.assertTrue(
            any(
                "requires exactly one proposal-callback binding" in error
                for error in validate_new_observation(wrong_binding)
            )
        )

        wrong_target = copy.deepcopy(response)
        wrong_target["input_snapshot"]["target_boundary"] = None  # type: ignore[index]
        wrong_target["transition_key"] = transition_key(wrong_target)
        self.assertEqual(validate_observation(wrong_target), [])
        self.assertTrue(
            any(
                "requires 'context-confirmed'" in error
                for error in validate_new_observation(wrong_target)
            )
        )

        for mismatched_response, count in (
            ("revision-requested", 1),
            ("blocked", 0),
        ):
            with self.subTest(response_result_mismatch=mismatched_response):
                mismatch = copy.deepcopy(response)
                mismatch["output_snapshot"]["response_kind"] = mismatched_response  # type: ignore[index]
                mismatch["output_snapshot"]["modification_item_count"] = count  # type: ignore[index]
                mismatch["transition_key"] = transition_key(mismatch)
                self.assertEqual(validate_observation(mismatch), [])
                self.assertTrue(
                    any(
                        "must equal result_kind and outcome" in error
                        for error in validate_new_observation(mismatch)
                    )
                )

        approved_response = copy.deepcopy(response)
        approved_response["outcome"] = "approved"
        approved_response["output_snapshot"]["result_kind"] = "approved"  # type: ignore[index]
        approved_response["output_snapshot"]["response_kind"] = "approved"  # type: ignore[index]
        approved_response["transition_key"] = transition_key(approved_response)
        self.assertEqual(validate_observation(approved_response), [])
        self.assertTrue(
            any(
                "must use the context-confirmed boundary" in error
                for error in validate_new_observation(approved_response)
            )
        )

        for omitted_response in ("approved", "revision-requested", "paused"):
            with self.subTest(omitted_response=omitted_response):
                omission = copy.deepcopy(response)
                omission["outcome"] = omitted_response
                omission["output_snapshot"]["result_kind"] = omitted_response  # type: ignore[index]
                omission["output_snapshot"]["response_kind"] = None  # type: ignore[index]
                omission["output_snapshot"]["modification_item_count"] = None  # type: ignore[index]
                omission["transition_key"] = transition_key(omission)
                self.assertEqual(validate_observation(omission), [])
                omission_errors = validate_new_observation(omission)
                if omitted_response == "approved":
                    self.assertTrue(
                        any(
                            "must use the context-confirmed boundary" in error
                            for error in omission_errors
                        )
                    )
                else:
                    self.assertTrue(
                        any(
                            "requires the matching response" in error
                            for error in omission_errors
                        )
                    )

        for response_with_result, count in (
            ("revision-requested", 1),
            ("paused", 0),
            ("blocked", 0),
        ):
            with self.subTest(non_null_response_result=response_with_result):
                result = evidence(
                    response_with_result,
                    f"{PRODUCT_PR_URL}#{response_with_result}-result",
                    "8" * 64,
                )
                invalid_result = copy.deepcopy(response)
                invalid_result["outcome"] = response_with_result
                invalid_result["output_snapshot"]["result_kind"] = response_with_result  # type: ignore[index]
                invalid_result["output_snapshot"]["result_url"] = result["url"]  # type: ignore[index]
                invalid_result["output_snapshot"]["result_sha256"] = result["sha256"]  # type: ignore[index]
                invalid_result["output_snapshot"]["response_kind"] = response_with_result  # type: ignore[index]
                invalid_result["output_snapshot"]["modification_item_count"] = count  # type: ignore[index]
                invalid_result["evidence"] = sorted(
                    [source, result],
                    key=lambda item: (item["kind"], item["url"], item["sha256"]),
                )
                invalid_result["transition_key"] = transition_key(invalid_result)
                self.assertEqual(validate_observation(invalid_result), [])
                self.assertTrue(
                    any(
                        "new confirmation response requires both null" in error
                        for error in validate_new_observation(invalid_result)
                    )
                )

        revision = copy.deepcopy(response)
        revision["outcome"] = "revision-requested"
        revision["output_snapshot"]["result_kind"] = "revision-requested"  # type: ignore[index]
        revision["output_snapshot"]["response_kind"] = "revision-requested"  # type: ignore[index]
        revision["transition_key"] = transition_key(revision)
        self.assertTrue(
            any(
                "revision-requested requires a positive integer" in error
                for error in validate_new_observation(revision)
            )
        )
        revision["output_snapshot"]["modification_item_count"] = 1  # type: ignore[index]
        revision["transition_key"] = transition_key(revision)
        self.assertEqual(validate_new_observation(revision), [])

        approved = copy.deepcopy(response)
        approved["outcome"] = "approved"
        approved["output_snapshot"]["result_kind"] = "approved"  # type: ignore[index]
        approved["output_snapshot"]["response_kind"] = "approved"  # type: ignore[index]
        approved["output_snapshot"]["modification_item_count"] = 1  # type: ignore[index]
        approved["transition_key"] = transition_key(approved)
        self.assertTrue(
            any(
                "approved requires zero" in error
                for error in validate_new_observation(approved)
            )
        )

        response["output_snapshot"]["response_kind"] = "raw-answer"  # type: ignore[index]
        self.assertTrue(
            any("unknown response" in error for error in validate_observation(response))
        )
        for malformed_response in ([], {}):
            with self.subTest(
                nested_response=type(malformed_response).__name__,
            ):
                malformed = copy.deepcopy(response)
                malformed["output_snapshot"]["response_kind"] = malformed_response  # type: ignore[index]
                self.assertTrue(
                    any(
                        "unknown response" in error
                        for error in validate_new_observation(malformed)
                    )
                )

    def test_timing_and_attempt_id_quality_rules(self) -> None:
        reconstructed = self.observation(
            started_at=None,
            elapsed_ms=None,
            timing_quality="reconstructed",
            attempt_id=None,
        )
        self.assertEqual(validate_observation(reconstructed), [])
        reconstructed_with_live_id = copy.deepcopy(reconstructed)
        reconstructed_with_live_id["attempt_id"] = LIVE_ATTEMPT_ID
        self.assertTrue(
            any(
                "boundaries require null" in error
                for error in validate_observation(reconstructed_with_live_id)
            )
        )

        unknown = self.observation(
            started_at=None,
            finished_at=None,
            elapsed_ms=None,
            timing_quality="unknown",
            attempt_id=None,
        )
        self.assertEqual(validate_observation(unknown), [])

        measured_without_id = self.observation()
        measured_without_id["attempt_id"] = None
        self.assertTrue(
            any(
                "measured observations require" in error
                for error in validate_observation(measured_without_id)
            )
        )

        bad_uuid = self.observation()
        bad_uuid["attempt_id"] = "550E8400-E29B-41D4-A716-446655440000"
        self.assertTrue(
            any("canonical lowercase UUIDv4" in error for error in validate_observation(bad_uuid))
        )

        confirmation = self.observation(
            "context-confirmed",
            activity="confirm",
            elapsed_ms=2500,
            user_wait_ms=2000,
        )
        self.assertEqual(validate_observation(confirmation), [])
        self.assertTrue(
            any(
                "new split-turn observations require null" in error
                for error in validate_new_observation(confirmation)
            )
        )
        confirmation["user_wait_ms"] = 2501
        self.assertTrue(
            any("must not exceed" in error for error in validate_observation(confirmation))
        )

    def test_change_quality_is_domain_specific(self) -> None:
        unknown = self.observation()
        unknown["change_quality"] = {
            "repository": "unknown",
            "github": "not-applicable",
            "context": "not-applicable",
        }
        unknown["change_summary"] = {
            "repository_changes": [],
            "github_mutations": [],
            "context_changes": [],
            "truncated": False,
            "omitted_count": 0,
        }
        unknown["reason_code"] = "change-delta-unavailable"
        self.assertEqual(validate_observation(unknown), [])

        disguised = copy.deepcopy(unknown)
        disguised["change_summary"]["repository_changes"] = [  # type: ignore[index]
            self.change_summary()["repository_changes"][0]  # type: ignore[index]
        ]
        self.assertTrue(
            any(
                "unknown requires an empty repository_changes" in error
                for error in validate_observation(disguised)
            )
        )
        missing_reason = copy.deepcopy(unknown)
        missing_reason["reason_code"] = None
        self.assertTrue(
            any(
                "requires a non-empty code" in error
                for error in validate_observation(missing_reason)
            )
        )

        independent = self.observation(
            timing_quality="reconstructed",
            started_at=None,
            elapsed_ms=None,
            attempt_id=None,
            change_quality={
                "repository": "measured",
                "github": "reconstructed",
                "context": "not-applicable",
            },
        )
        independent["change_summary"]["context_changes"] = []  # type: ignore[index]
        self.assertEqual(validate_observation(independent), [])

    def test_change_preview_and_privacy_fail_closed(self) -> None:
        at_limit = self.observation()
        repository_change = self.change_summary()["repository_changes"][0]  # type: ignore[index]
        at_limit["change_summary"] = {
            "repository_changes": [
                dict(repository_change, path=f"src/file-{index:03}.py")
                for index in range(100)
            ],
            "github_mutations": [],
            "context_changes": [],
            "truncated": True,
            "omitted_count": 4,
        }
        self.assertEqual(validate_observation(at_limit), [])
        over_limit = copy.deepcopy(at_limit)
        over_limit["change_summary"]["repository_changes"].append(  # type: ignore[index]
            dict(repository_change, path="src/zzzz.py")
        )
        self.assertTrue(
            any("more than 100" in error for error in validate_observation(over_limit))
        )

        raw = self.observation()
        raw["raw_user_input_persisted"] = True
        self.assertTrue(
            any("raw_user_input_persisted" in error for error in validate_observation(raw))
        )
        raw["output_snapshot"] = {"raw_user_response": "verbatim"}
        self.assertTrue(
            any("raw user input" in error for error in validate_observation(raw))
        )
        raw["output_snapshot"] = {
            "confirmation_response": {
                "decision": "revise",
                "modification_items": ["verbatim"],
            }
        }
        self.assertTrue(
            any("raw user input" in error for error in validate_observation(raw))
        )

    def test_transition_key_excludes_execution_metadata_and_outcome(self) -> None:
        original = self.observation("product-merged", outcome="verified")
        changed = copy.deepcopy(original)
        changed.update(
            {
                "activity": "recover",
                "outcome": "no-op",
                "attempt_id": OTHER_ATTEMPT_ID,
                "attempt": 9,
                "observed_at": "2026-07-28T11:00:03Z",
                "started_at": "2026-07-28T11:00:00Z",
                "finished_at": "2026-07-28T11:00:03Z",
                "elapsed_ms": 3000,
                "change_quality": {
                    "repository": "reconstructed",
                    "github": "reconstructed",
                    "context": "not-applicable",
                },
                "change_summary": {
                    "repository_changes": [],
                    "github_mutations": [],
                    "context_changes": [],
                    "truncated": False,
                    "omitted_count": 0,
                },
                "reason_code": "already-persisted",
            }
        )
        self.assertEqual(transition_key(original), transition_key(changed))

        unsorted = copy.deepcopy(original)
        unsorted["evidence"] = list(reversed(unsorted["evidence"]))  # type: ignore[arg-type]
        self.assertTrue(
            any(
                "must be sorted" in error
                for error in validate_observation(unsorted)
            )
        )

        changed_output = copy.deepcopy(original)
        changed_output["output_snapshot"]["merge_commit_sha"] = "9" * 40  # type: ignore[index]
        self.assertNotEqual(
            transition_key(original),
            transition_key(changed_output),
        )
        self.assertTrue(
            any(
                "does not match" in error
                for error in validate_observation(changed_output)
            )
        )

    def test_issue_closed_fresh_and_recovery_semantics(self) -> None:
        verified = self.observation("issue-closed", outcome="verified")
        self.assertEqual(validate_observation(verified), [])

        recovered = self.observation(
            "issue-closed",
            outcome="no-op",
            timing_quality="reconstructed",
            started_at=None,
            elapsed_ms=None,
            attempt_id=None,
            change_quality={
                "repository": "not-applicable",
                "github": "unknown",
                "context": "not-applicable",
            },
            change_summary={
                "repository_changes": [],
                "github_mutations": [],
                "context_changes": [],
                "truncated": False,
                "omitted_count": 0,
            },
            reason_code="historical-close-delta-unavailable",
        )
        self.assertEqual(validate_observation(recovered), [])
        self.assertEqual(transition_key(verified), transition_key(recovered))

        unknown = copy.deepcopy(recovered)
        unknown.update(
            {
                "timing_quality": "unknown",
                "finished_at": None,
                "change_quality": {
                    "repository": "not-applicable",
                    "github": "unknown",
                    "context": "not-applicable",
                },
                "change_summary": {
                    "repository_changes": [],
                    "github_mutations": [],
                    "context_changes": [],
                    "truncated": False,
                    "omitted_count": 0,
                },
                "reason_code": "historical-close-delta-unavailable",
            }
        )
        self.assertEqual(validate_observation(unknown), [])

        reconstructed_mutation = copy.deepcopy(recovered)
        reconstructed_mutation["change_quality"]["github"] = "reconstructed"  # type: ignore[index]
        reconstructed_mutation["change_summary"] = self.issue_close_summary()
        reconstructed_errors = validate_observation(reconstructed_mutation)
        self.assertTrue(
            any(
                "GitHub change quality must be unknown" in error
                for error in reconstructed_errors
            )
        )
        self.assertTrue(
            any(
                "GitHub mutations must be empty" in error
                for error in reconstructed_errors
            )
        )

        false_live_no_op = copy.deepcopy(verified)
        false_live_no_op["outcome"] = "no-op"
        self.assertTrue(
            any(
                "no-op: requires reconstructed or unknown timing" in error
                for error in validate_observation(false_live_no_op)
            )
        )

        missing_mutation = copy.deepcopy(verified)
        missing_mutation["change_summary"]["github_mutations"] = []  # type: ignore[index]
        self.assertTrue(
            any(
                "requires exactly one" in error
                for error in validate_observation(missing_mutation)
            )
        )

    def test_finalization_manifest_is_exact_and_digest_bound(self) -> None:
        finalization = self.observation("finalization-ready")
        self.assertEqual(validate_observation(finalization), [])

        drift = copy.deepcopy(finalization)
        drift["input_snapshot"]["coverage_manifest_sha256"] = "f" * 64  # type: ignore[index]
        self.assertTrue(
            any(
                "does not match the canonical manifest" in error
                for error in validate_observation(drift)
            )
        )

        source_drift = copy.deepcopy(finalization)
        source_drift["input_snapshot"]["coverage_manifest"][  # type: ignore[index]
            "issue_body_sha256"
        ] = "f" * 64
        source_drift["input_snapshot"]["coverage_manifest_sha256"] = canonical_sha256(  # type: ignore[index]
            source_drift["input_snapshot"]["coverage_manifest"]  # type: ignore[index]
        )
        self.assertTrue(
            any(
                "coverage_manifest.issue_body_sha256: must match issue_body_sha256"
                in error
                for error in validate_observation(source_drift)
            )
        )

        missing_stage = copy.deepcopy(finalization)
        missing_stage["evidence"].pop()  # type: ignore[union-attr]
        self.assertTrue(
            any(
                "must exactly bind manifest observations" in error
                for error in validate_observation(missing_stage)
            )
        )

    def test_malformed_boundary_values_fail_closed_without_crashing(self) -> None:
        for malformed_record in (None, [], "bad"):
            with self.subTest(
                validator="new-write",
                malformed=type(malformed_record).__name__,
            ):
                self.assertEqual(
                    validate_new_observation(malformed_record),  # type: ignore[arg-type]
                    ["record: must be an object"],
                )

        for boundary in ("finalization-ready", "issue-closed"):
            for malformed in ([], {}):
                with self.subTest(boundary=boundary, malformed=type(malformed).__name__):
                    record = self.observation(boundary)
                    record["input_snapshot"]["path_kind"] = malformed  # type: ignore[index]
                    self.assertTrue(
                        any(
                            "path_kind: must be 'no-write' or 'memory-write'"
                            in error
                            for error in validate_observation(record)
                        )
                    )

        memory_terminal = self.observation(
            "context-memory-terminal",
            memory_write=True,
        )
        memory_terminal["output_snapshot"]["terminal_outcome"] = "no-promotion"  # type: ignore[index]
        self.assertTrue(
            any(
                "terminal_outcome: must be 'memory-pr-merged'" in error
                for error in validate_observation(memory_terminal)
            )
        )

    def records_for(
        self,
        boundaries: tuple[str, ...],
        *,
        memory_write: bool,
    ) -> list[dict[str, object]]:
        return [
            self.observation(
                boundary,
                memory_write=memory_write,
                attempt=index + 1,
            )
            for index, boundary in enumerate(boundaries)
        ]

    def observation_binding(
        self,
        record: dict[str, object],
        label: str,
    ) -> dict[str, object]:
        observation_url = f"{ISSUE_URL}#issuecomment-observation-{label}"
        observation_sha256 = sha256(
            f"{observation_url}\n{record['transition_key']}".encode("utf-8")
        ).hexdigest()
        return {
            "observation_url": observation_url,
            "observation_sha256": observation_sha256,
            "record": record,
        }

    def source_bindings_for(
        self,
        *,
        memory_write: bool,
    ) -> list[dict[str, object]]:
        boundaries = COMMON_BOUNDARIES + (
            WRITE_BOUNDARIES if memory_write else NO_WRITE_BOUNDARIES
        )
        return [
            self.observation_binding(record, f"source-{index}-{boundary}")
            for index, (boundary, record) in enumerate(
                zip(
                    boundaries,
                    self.records_for(boundaries, memory_write=memory_write),
                )
            )
        ]

    def finalization_binding_for(
        self,
        source_bindings: list[dict[str, object]],
        *,
        memory_write: bool,
        label: str = "finalization",
    ) -> dict[str, object]:
        path_kind = "memory-write" if memory_write else "no-write"
        boundaries = COMMON_BOUNDARIES + (
            WRITE_BOUNDARIES if memory_write else NO_WRITE_BOUNDARIES
        )
        entries: list[dict[str, object]] = []
        for boundary, binding in zip(boundaries, source_bindings):
            record = binding["record"]
            assert isinstance(record, dict)
            entries.append(
                {
                    "boundary": boundary,
                    "observation_url": binding["observation_url"],
                    "observation_sha256": binding["observation_sha256"],
                    "transition_key": record["transition_key"],
                    "evidence": copy.deepcopy(record["evidence"]),
                }
            )
        manifest = {
            "manifest_schema_version": 1,
            "path_kind": path_kind,
            "issue_url": ISSUE_URL,
            "issue_body_sha256": "a" * 64,
            "entries": entries,
        }
        finalization = self.observation(
            "finalization-ready",
            memory_write=memory_write,
        )
        finalization["input_snapshot"] = {
            "path_kind": path_kind,
            "coverage_manifest": manifest,
            "coverage_manifest_sha256": canonical_sha256(manifest),
        }
        terminal_evidence = [
            item
            for item in entries[-1]["evidence"]  # type: ignore[union-attr]
            if item["kind"] == "terminal-callback"
        ]
        finalization["evidence"] = sorted(
            [
                evidence(
                    "stage-observation",
                    str(entry["observation_url"]),
                    str(entry["observation_sha256"]),
                )
                for entry in entries
            ]
            + terminal_evidence,
            key=lambda item: (item["kind"], item["url"], item["sha256"]),
        )
        finalization["transition_key"] = transition_key(finalization)
        return self.observation_binding(finalization, label)

    def completion_binding_for(
        self,
        finalization_binding: dict[str, object],
        *,
        memory_write: bool,
        label: str = "completion",
    ) -> dict[str, object]:
        finalization = finalization_binding["record"]
        assert isinstance(finalization, dict)
        finalization_input = finalization["input_snapshot"]
        assert isinstance(finalization_input, dict)
        completion = self.observation(
            "issue-closed",
            memory_write=memory_write,
        )
        completion["input_snapshot"] = {
            "path_kind": "memory-write" if memory_write else "no-write",
            "coverage_manifest_sha256": finalization_input[
                "coverage_manifest_sha256"
            ],
            "finalization_observation_url": finalization_binding[
                "observation_url"
            ],
            "finalization_observation_sha256": finalization_binding[
                "observation_sha256"
            ],
        }
        completion["evidence"] = [
            evidence(
                "finalization-observation",
                str(finalization_binding["observation_url"]),
                str(finalization_binding["observation_sha256"]),
            )
        ]
        completion["transition_key"] = transition_key(completion)
        return self.observation_binding(completion, label)

    def test_three_coverage_levels_require_exact_comment_bindings(self) -> None:
        no_write_boundaries = COMMON_BOUNDARIES + NO_WRITE_BOUNDARIES
        raw_records = self.records_for(
            no_write_boundaries,
            memory_write=False,
        )
        self.assertEqual(
            coverage(raw_records, False, level="manifest"),
            (False, ["observation-binding"]),
        )

        bindings = self.source_bindings_for(memory_write=False)
        self.assertEqual(coverage(bindings, False, level="manifest"), (True, []))

        non_exact_binding = copy.deepcopy(bindings)
        non_exact_binding[0]["trusted"] = True
        self.assertEqual(
            coverage(non_exact_binding, False, level="manifest"),
            (False, ["observation-binding"]),
        )

        self.assertEqual(
            coverage(bindings, False, level="closure"),
            (False, ["finalization-ready"]),
        )
        finalization = self.finalization_binding_for(
            bindings,
            memory_write=False,
        )
        bindings.append(finalization)
        self.assertEqual(coverage(bindings, False, level="closure"), (True, []))
        self.assertEqual(
            coverage(bindings, False, level="completion"),
            (False, ["issue-closed"]),
        )
        bindings.append(
            self.completion_binding_for(
                finalization,
                memory_write=False,
            )
        )
        self.assertEqual(
            coverage(bindings, False, level="completion"),
            (True, []),
        )

        source_record = bindings[0]["record"]
        malformed_bindings = (
            copy.deepcopy(source_record),
            {"record": copy.deepcopy(source_record)},
            {**copy.deepcopy(bindings[0]), "trusted": True},
        )
        for index, malformed in enumerate(malformed_bindings):
            with self.subTest(malformed_binding=index):
                self.assertEqual(
                    coverage(
                        bindings + [malformed],  # type: ignore[list-item]
                        False,
                        level="completion",
                    ),
                    (False, ["observation-binding"]),
                )

        ignored_valid_bindings = [
            self.observation_binding(self.attempt(), "ignored-attempt"),
            self.observation_binding(
                self.observation("memory-pr-ready", memory_write=True),
                "ignored-other-path-boundary",
            ),
        ]
        self.assertEqual(
            coverage(
                bindings + ignored_valid_bindings,
                False,
                level="completion",
            ),
            (True, []),
        )

        write_bindings = self.source_bindings_for(memory_write=True)
        write_finalization = self.finalization_binding_for(
            write_bindings,
            memory_write=True,
            label="write-finalization",
        )
        write_bindings.append(write_finalization)
        write_bindings.append(
            self.completion_binding_for(
                write_finalization,
                memory_write=True,
                label="write-completion",
            )
        )
        self.assertEqual(
            coverage(write_bindings, True, level="completion"),
            (True, []),
        )

        with self.assertRaisesRegex(ValueError, "manifest.*closure.*completion"):
            coverage(write_bindings, True, level="close")

    def test_coverage_rejects_source_and_observation_ambiguity(self) -> None:
        bindings = self.source_bindings_for(memory_write=False)
        mixed_source = copy.deepcopy(bindings)
        mixed_record = mixed_source[0]["record"]
        assert isinstance(mixed_record, dict)
        mixed_record["issue_body_sha256"] = "f" * 64
        mixed_record["transition_key"] = transition_key(mixed_record)
        self.assertEqual(
            coverage(mixed_source, False, level="manifest"),
            (False, ["source-identity"]),
        )

        exact_duplicate = bindings + [copy.deepcopy(bindings[0])]
        self.assertEqual(
            coverage(exact_duplicate, False, level="manifest"),
            (False, ["observation-identity"]),
        )

        alternate_record = copy.deepcopy(bindings[0]["record"])
        assert isinstance(alternate_record, dict)
        alternate_record["attempt"] = 99
        alternate_record["transition_key"] = transition_key(alternate_record)
        distinct_duplicate = bindings + [
            self.observation_binding(
                alternate_record,
                "distinct-implementation-duplicate",
            )
        ]
        self.assertEqual(
            coverage(distinct_duplicate, False, level="manifest"),
            (False, ["implementation-verified-draft"]),
        )

        finalization = self.finalization_binding_for(
            bindings,
            memory_write=False,
        )
        alternate_finalization = self.observation_binding(
            copy.deepcopy(finalization["record"]),  # type: ignore[arg-type]
            "alternate-finalization",
        )
        self.assertEqual(
            coverage(
                bindings + [finalization, alternate_finalization],
                False,
                level="closure",
            ),
            (False, ["finalization-ready"]),
        )

    def test_coverage_binds_manifest_and_completion_identity(self) -> None:
        source_bindings = self.source_bindings_for(memory_write=False)
        finalization = self.finalization_binding_for(
            source_bindings,
            memory_write=False,
        )
        completion = self.completion_binding_for(
            finalization,
            memory_write=False,
        )

        replacement_bindings = copy.deepcopy(source_bindings)
        replacement_record = replacement_bindings[0]["record"]
        assert isinstance(replacement_record, dict)
        replacement_output = replacement_record["output_snapshot"]
        assert isinstance(replacement_output, dict)
        replacement_output["product_pr_title"] = "Unrelated implementation"
        replacement_record["transition_key"] = transition_key(replacement_record)
        replacement_bindings[0] = self.observation_binding(
            replacement_record,
            "replacement-implementation",
        )
        replaced_manifest = self.finalization_binding_for(
            replacement_bindings,
            memory_write=False,
            label="replacement-finalization",
        )
        self.assertEqual(
            coverage(
                source_bindings + [replaced_manifest],
                False,
                level="closure",
            ),
            (False, ["finalization-ready"]),
        )

        unrelated_finalization = self.observation_binding(
            copy.deepcopy(finalization["record"]),  # type: ignore[arg-type]
            "unrelated-finalization",
        )
        unrelated_completion = self.completion_binding_for(
            unrelated_finalization,
            memory_write=False,
            label="unrelated-completion",
        )
        self.assertEqual(
            coverage(
                source_bindings + [finalization, unrelated_completion],
                False,
                level="completion",
            ),
            (False, ["issue-closed"]),
        )

        write_bindings = self.source_bindings_for(memory_write=True)
        write_finalization = self.finalization_binding_for(
            write_bindings,
            memory_write=True,
            label="path-finalization",
        )
        mismatched_path = self.completion_binding_for(
            write_finalization,
            memory_write=False,
            label="path-mismatch-completion",
        )
        self.assertEqual(
            coverage(
                write_bindings + [write_finalization, mismatched_path],
                True,
                level="completion",
            ),
            (False, ["issue-closed"]),
        )

        mismatched_digest = copy.deepcopy(completion)
        mismatched_record = mismatched_digest["record"]
        assert isinstance(mismatched_record, dict)
        mismatched_input = mismatched_record["input_snapshot"]
        assert isinstance(mismatched_input, dict)
        mismatched_input["coverage_manifest_sha256"] = "f" * 64
        mismatched_record["transition_key"] = transition_key(mismatched_record)
        mismatched_digest = self.observation_binding(
            mismatched_record,
            "manifest-digest-mismatch",
        )
        self.assertEqual(
            coverage(
                source_bindings + [finalization, mismatched_digest],
                False,
                level="completion",
            ),
            (False, ["issue-closed"]),
        )


if __name__ == "__main__":
    unittest.main()
