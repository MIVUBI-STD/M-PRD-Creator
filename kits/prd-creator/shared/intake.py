from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .issues import Issue
from .paths import ProjectPathError, resolve_project_path
from .state import StateError, list_of_mappings, load_mapping, require_bool, require_scalar

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_ID_RE = re.compile(r"^SRC-\d{3,}$")
REQUIREMENT_ID_RE = re.compile(r"^REQ-\d{3,}$")
SOURCE_ROLES = {"authoritative", "supporting", "reference", "generated"}
SOURCE_STATUSES = {"current", "superseded"}
SOURCE_INSPECTIONS = {"full", "targeted", "blocked"}
SOURCE_RETENTIONS = {"repository", "external"}
REQUIREMENT_RECOVERY = {"", "source", "completion", "proposal", "blocked"}
REQUIREMENT_APPROVAL = {"", "pending", "approved", "rejected"}
INTAKE_STATUSES = {"collecting_sources", "audit_in_progress", "needs_decision", "blocked", "ready_for_prd"}

SOURCE_ROOT_FIELDS = {"sources"}
SOURCE_FIELDS = {
    "id",
    "type",
    "role",
    "origin",
    "summary",
    "status",
    "inspection",
    "inspection_scope",
    "retention",
    "path",
    "filename",
    "sha256",
    "identity",
    "notes",
}
REQUIREMENT_ROOT_FIELDS = {"requirements"}
REQUIREMENT_FIELDS = {
    "id",
    "area",
    "statement",
    "provenance",
    "impact",
    "recovery_class",
    "approval_status",
    "resolution",
    "affects",
    "evidence_locator",
    "evidence_status",
}
INTAKE_FIELDS = {"status", "preview_approved", "approved_requirement_sha256"}


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    role: str
    status: str
    inspection: str
    retention: str
    path: str


@dataclass(frozen=True)
class RequirementRecord:
    requirement_id: str
    area: str
    statement: str
    provenance: tuple[str, ...]
    recovery_class: str
    approval_status: str
    evidence_locator: str = ""
    evidence_status: str = ""


@dataclass(frozen=True)
class IntakeState:
    status: str
    preview_approved: bool
    approved_requirement_sha256: str


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_inventory(path: Path, project: Path) -> tuple[SourceRecord, ...]:
    root = load_mapping(path, owner="source-inventory.yaml")
    _reject_unknown(root, SOURCE_ROOT_FIELDS, "source-inventory.yaml")
    entries = list_of_mappings(root, "sources", owner="source-inventory.yaml")
    if not entries:
        raise StateError("source-inventory.yaml.sources must contain at least one source")

    seen: set[str] = set()
    records: list[SourceRecord] = []
    for index, entry in enumerate(entries):
        owner = f"source-inventory.yaml.sources[{index}]"
        _reject_unknown(entry, SOURCE_FIELDS, owner)
        source_id = require_scalar(entry, "id", owner=owner)
        if SOURCE_ID_RE.fullmatch(source_id) is None:
            raise StateError(f"{owner}.id must use SRC-### stable identity")
        if source_id in seen:
            raise StateError(f"duplicate source id: {source_id}")
        seen.add(source_id)

        role = require_scalar(entry, "role", owner=owner).casefold()
        if role not in SOURCE_ROLES:
            raise StateError(f"{owner}.role={role!r} is unsupported")
        status = str(entry.get("status") or "current").strip().casefold()
        if status not in SOURCE_STATUSES:
            raise StateError(f"{owner}.status={status!r} is unsupported")
        inspection = require_scalar(entry, "inspection", owner=owner).casefold()
        if inspection not in SOURCE_INSPECTIONS:
            raise StateError(f"{owner}.inspection={inspection!r} is unsupported")
        if inspection == "targeted" and not str(entry.get("inspection_scope") or "").strip():
            raise StateError(f"{owner}.inspection_scope is required when inspection=targeted")

        retention = str(entry.get("retention") or "").strip().casefold()
        if retention and retention not in SOURCE_RETENTIONS:
            raise StateError(f"{owner}.retention={retention!r} is unsupported")
        ref = str(entry.get("path") or "").strip()
        recorded_sha = str(entry.get("sha256") or "").strip().casefold()
        if recorded_sha and SHA256_RE.fullmatch(recorded_sha) is None:
            raise StateError(f"{owner}.sha256 must be a lowercase SHA-256 digest")

        if retention == "repository":
            if not ref:
                raise StateError(f"{owner}.path is required when retention=repository")
            if not recorded_sha:
                raise StateError(f"{owner}.sha256 is required when retention=repository")
            try:
                retained = resolve_project_path(project, ref, owner=f"{owner}.path", must_exist=True)
            except ProjectPathError as exc:
                raise StateError(str(exc)) from exc
            actual_sha = sha256_file(retained)
            if actual_sha != recorded_sha:
                raise StateError(f"{owner}.sha256 does not match current retained source bytes")
        elif ref:
            try:
                resolve_project_path(project, ref, owner=f"{owner}.path", must_exist=False)
            except ProjectPathError as exc:
                raise StateError(str(exc)) from exc

        records.append(SourceRecord(source_id, role, status, inspection, retention, ref))
    return tuple(records)


def load_requirement_register(path: Path, sources: tuple[SourceRecord, ...]) -> tuple[RequirementRecord, ...]:
    root = load_mapping(path, owner="requirement-register.yaml")
    _reject_unknown(root, REQUIREMENT_ROOT_FIELDS, "requirement-register.yaml")
    entries = list_of_mappings(root, "requirements", owner="requirement-register.yaml")
    if not entries:
        raise StateError("requirement-register.yaml.requirements must contain at least one requirement")

    source_ids = {record.source_id for record in sources}
    seen: set[str] = set()
    records: list[RequirementRecord] = []
    for index, entry in enumerate(entries):
        owner = f"requirement-register.yaml.requirements[{index}]"
        _reject_unknown(entry, REQUIREMENT_FIELDS, owner)
        requirement_id = require_scalar(entry, "id", owner=owner)
        if REQUIREMENT_ID_RE.fullmatch(requirement_id) is None:
            raise StateError(f"{owner}.id must use REQ-### stable identity")
        if requirement_id in seen:
            raise StateError(f"duplicate requirement id: {requirement_id}")
        seen.add(requirement_id)

        area = require_scalar(entry, "area", owner=owner)
        statement = require_scalar(entry, "statement", owner=owner)
        raw_provenance = entry.get("provenance")
        if (
            not isinstance(raw_provenance, list)
            or not raw_provenance
            or not all(isinstance(item, str) for item in raw_provenance)
        ):
            raise StateError(f"{owner}.provenance must be a non-empty array of SRC-### ids")
        provenance = tuple(item.strip() for item in raw_provenance)
        if len(provenance) != len(set(provenance)):
            raise StateError(f"{owner}.provenance must not contain duplicates")
        dangling = [source_id for source_id in provenance if source_id not in source_ids]
        if dangling:
            raise StateError(f"{owner}.provenance references unknown source id(s): {', '.join(dangling)}")

        recovery = str(entry.get("recovery_class") or "").strip().casefold()
        approval = str(entry.get("approval_status") or "").strip().casefold()
        if recovery not in REQUIREMENT_RECOVERY:
            raise StateError(f"{owner}.recovery_class={recovery!r} is unsupported")
        if approval not in REQUIREMENT_APPROVAL:
            raise StateError(f"{owner}.approval_status={approval!r} is unsupported")
        if recovery == "proposal" and approval not in {"pending", "approved", "rejected"}:
            raise StateError(f"{owner}.approval_status is required for proposal requirements")
        if recovery in {"proposal", "blocked"} and not str(entry.get("resolution") or "").strip():
            raise StateError(f"{owner}.resolution is required for {recovery} requirements")

        # Preserve optional source-evidence pointers for the trace reviewer.
        # Their contents are claims to inspect, not proof of truth or a new approval gate.
        evidence_locator = str(entry.get("evidence_locator") or "").strip()
        evidence_status = str(entry.get("evidence_status") or "").strip()
        records.append(
            RequirementRecord(
                requirement_id,
                area,
                statement,
                provenance,
                recovery,
                approval,
                evidence_locator,
                evidence_status,
            )
        )
    return tuple(records)


def load_intake_state(path: Path) -> IntakeState:
    state = load_mapping(path, owner="intake-state.yaml")
    _reject_unknown(state, INTAKE_FIELDS, "intake-state.yaml")
    status = require_scalar(state, "status", owner="intake-state.yaml").casefold()
    if status not in INTAKE_STATUSES:
        raise StateError(f"intake-state.yaml.status={status!r} is unsupported")
    preview = (
        require_bool(state, "preview_approved", owner="intake-state.yaml") if "preview_approved" in state else False
    )
    approved_sha = str(state.get("approved_requirement_sha256") or "").strip().casefold()
    if approved_sha and SHA256_RE.fullmatch(approved_sha) is None:
        raise StateError("intake-state.yaml.approved_requirement_sha256 must be a lowercase SHA-256 digest")
    if status == "ready_for_prd":
        if not approved_sha:
            raise StateError("ready_for_prd requires approved_requirement_sha256")
    elif preview or approved_sha:
        raise StateError("preview approval/hash may exist only when status=ready_for_prd")
    return IntakeState(status, preview, approved_sha)


def _state_issue(exc: Exception, *, path: str) -> Issue:
    line = exc.line if isinstance(exc, StateError) else None
    return Issue("FLOW2_STATE_INVALID", "flow2.state", str(exc), path=path, line=line)


def validate_flow2_state(project: Path) -> list[Issue]:
    issues: list[Issue] = []
    source_path = project / "state" / "source-inventory.yaml"
    requirement_path = project / "state" / "requirement-register.yaml"
    intake_path = project / "state" / "intake-state.yaml"

    try:
        sources = load_source_inventory(source_path, project)
    except (OSError, StateError) as exc:
        return [_state_issue(exc, path="state/source-inventory.yaml")]
    try:
        requirements = load_requirement_register(requirement_path, sources)
    except (OSError, StateError) as exc:
        return [_state_issue(exc, path="state/requirement-register.yaml")]
    try:
        intake = load_intake_state(intake_path)
    except (OSError, StateError) as exc:
        return [_state_issue(exc, path="state/intake-state.yaml")]

    current_authoritative_sources = {
        record.source_id for record in sources if record.status == "current" and record.role == "authoritative"
    }
    for source in sources:
        if source.status == "current" and source.inspection == "blocked":
            issues.append(
                Issue(
                    "SOURCE_INSPECTION_BLOCKED",
                    "flow2.source",
                    "current source inspection is blocked",
                    path="state/source-inventory.yaml",
                    field=source.source_id,
                )
            )
    for requirement in requirements:
        if requirement.recovery_class == "blocked":
            issues.append(
                Issue(
                    "REQUIREMENT_BLOCKED",
                    "flow2.requirement",
                    "requirement recovery remains blocked",
                    path="state/requirement-register.yaml",
                    field=requirement.requirement_id,
                )
            )
        if requirement.approval_status == "pending":
            issues.append(
                Issue(
                    "REQUIREMENT_APPROVAL_PENDING",
                    "flow2.requirement",
                    "material proposal approval is still pending",
                    path="state/requirement-register.yaml",
                    field=requirement.requirement_id,
                )
            )
        if requirement.approval_status == "rejected":
            issues.append(
                Issue(
                    "REQUIREMENT_REJECTED_ACTIVE",
                    "flow2.requirement",
                    "rejected proposal must be removed or superseded before readiness",
                    path="state/requirement-register.yaml",
                    field=requirement.requirement_id,
                )
            )
        approved_proposal = requirement.recovery_class == "proposal" and requirement.approval_status == "approved"
        has_current_authority = any(source_id in current_authoritative_sources for source_id in requirement.provenance)
        if not approved_proposal and not has_current_authority:
            issues.append(
                Issue(
                    "REQUIREMENT_NO_CURRENT_AUTHORITY",
                    "flow2.requirement",
                    "requirement is not grounded in a current authoritative source or an approved Proposal",
                    path="state/requirement-register.yaml",
                    field=requirement.requirement_id,
                )
            )

    requires_preview_approval = any(
        requirement.recovery_class == "proposal" and requirement.approval_status == "approved"
        for requirement in requirements
    )
    actual_requirement_sha = sha256_file(requirement_path)
    if intake.status != "ready_for_prd":
        issues.append(
            Issue(
                "FLOW2_NOT_READY",
                "flow2.state",
                f"status is {intake.status!r}, expected 'ready_for_prd'",
                path="state/intake-state.yaml",
                field="status",
            )
        )
    elif requires_preview_approval and not intake.preview_approved:
        issues.append(
            Issue(
                "FLOW2_PROPOSAL_APPROVAL_REQUIRED",
                "flow2.approval",
                "approved material Proposal requires Simple Chat Preview approval evidence",
                path="state/intake-state.yaml",
                field="preview_approved",
            )
        )
    elif intake.approved_requirement_sha256 != actual_requirement_sha:
        issues.append(
            Issue(
                "FLOW2_APPROVAL_STALE",
                "flow2.approval",
                "Flow 2 requirement revision binding does not match current requirement-register bytes",
                path="state/intake-state.yaml",
                field="approved_requirement_sha256",
            )
        )
    return issues


def _reject_unknown(mapping: dict[str, Any], allowed: set[str], owner: str) -> None:
    unknown = sorted(set(mapping) - allowed)
    if unknown:
        raise StateError(f"{owner} contains unsupported field(s): {', '.join(unknown)}")
