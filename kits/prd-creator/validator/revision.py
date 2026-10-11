"""Read-only impact of an explicit prior requirement register on current PRD content.

A REQ marker identifies a location, never a semantic match or safe rewrite scope.
No baseline is inferred from chat history, generated HTML or Git commit recency.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from shared.intake import REQUIREMENT_FIELDS, REQUIREMENT_ID_RE, load_intake_state
from shared.state import StateError, list_of_mappings, load_mapping, require_scalar

from .traceability import assess

MEANING_FIELDS = {"statement", "area", "resolution", "recovery_class", "affects", "impact"}


def _register(path: Path) -> dict[str, dict[str, Any]]:
    """Read snapshot identities without reinterpreting historical source authority."""
    root = load_mapping(path, owner="requirement-register.yaml")
    unknown = sorted(set(root) - {"requirements"})
    if unknown:
        raise StateError("requirement-register.yaml contains unsupported field(s): " + ", ".join(unknown))
    rows = list_of_mappings(root, "requirements", owner="requirement-register.yaml")
    if not rows:
        raise StateError("requirement-register.yaml.requirements must not be empty")
    result: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(rows):
        owner = f"requirement-register.yaml.requirements[{index}]"
        extra = sorted(set(entry) - REQUIREMENT_FIELDS)
        if extra:
            raise StateError(f"{owner} contains unsupported field(s): {', '.join(extra)}")
        identifier = require_scalar(entry, "id", owner=owner)
        require_scalar(entry, "area", owner=owner)
        require_scalar(entry, "statement", owner=owner)
        provenance = entry.get("provenance")
        if not isinstance(provenance, list) or not provenance or not all(isinstance(x, str) for x in provenance):
            raise StateError(f"{owner}.provenance must contain source IDs")
        if REQUIREMENT_ID_RE.fullmatch(identifier) is None:
            raise StateError(f"{owner}.id must be a REQ-### identity")
        if identifier in result:
            raise StateError(f"duplicate requirement id: {identifier}")
        result[identifier] = entry
    return result


def _approval_binding(project: Path, current_sha: str) -> dict[str, Any]:
    try:
        state = load_intake_state(project / "state" / "intake-state.yaml")
    except (OSError, StateError) as exc:
        return {"status": "unavailable", "reason": str(exc)}
    return {
        "status": "current" if state.approved_requirement_sha256 == current_sha else "stale",
        "intake_status": state.status,
    }


def _projection_binding(project: Path, current_sha: str) -> str:
    path = project / "work" / "render-data.json"
    if not path.is_file():
        return "not_present"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return "unreadable"
    if not isinstance(value, dict):
        return "unreadable"
    return "current" if value.get("approved_requirement_sha256") == current_sha else "stale"


def plan_revision(project: Path, before: Path) -> dict[str, Any]:
    """Compare two explicit snapshots and report only grounded impacted locations."""
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"revision requires an existing project directory: {project}")
    previous_path = before.resolve()
    current_path = (project / "state" / "requirement-register.yaml").resolve()
    if previous_path == current_path:
        raise ValueError("--before must reference a distinct prior snapshot, not the current register")
    previous = _register(previous_path)
    current = _register(current_path)
    prior_sha = hashlib.sha256(previous_path.read_bytes()).hexdigest()
    current_sha = hashlib.sha256(current_path.read_bytes()).hexdigest()
    byte_change = prior_sha != current_sha
    trace = assess(project)
    known = {item["id"]: item for item in trace["requirements"]}
    orphaned = trace["issues"]
    changes: list[dict[str, Any]] = []
    unchanged = []
    marker = object()

    for identifier in sorted(set(previous) | set(current)):
        old = previous.get(identifier)
        new = current.get(identifier)
        if old is not None and new is not None and old == new:
            unchanged.append(identifier)
            continue
        kind = "added" if old is None else "removed" if new is None else "modified"
        changed_fields = (
            sorted(key for key in set(old) | set(new) if old.get(key, marker) != new.get(key, marker))
            if old is not None and new is not None
            else []
        )
        locations = list(known.get(identifier, {}).get("locations", []))
        orphan_lines = [
            issue["line"]
            for issue in orphaned
            if issue.get("code") == "PRD_TRACE_UNKNOWN_REQUIREMENT"
            and issue.get("message") == "Unknown current requirement " + identifier
            and isinstance(issue.get("line"), int)
        ]
        changes.append(
            {
                "id": identifier,
                "kind": kind,
                "changed_fields": changed_fields,
                "change_scope": (
                    "potential_meaning" if kind != "modified" or bool(set(changed_fields) & MEANING_FIELDS)
                    else "evidence_or_approval"
                ),
                "locations": locations,
                "orphaned_marker_lines": orphan_lines,
                "mapping": (
                    "REMOVED_REVIEW_REQUIRED" if kind == "removed"
                    else "LOCATED_NOT_SEMANTICALLY_VERIFIED" if locations
                    else "LOCATION_UNKNOWN"
                ),
            }
        )

    located = bool(changes) and trace["status"] == "mapped_unverified" and all(
        change["kind"] == "modified" and bool(change["locations"]) for change in changes
    )
    if not byte_change:
        status = "no_change"
    elif not changes:
        status = "byte_only_change"
    elif located:
        status = "targeted_review_required"
    else:
        status = "scope_unknown"

    return {
        "status": status,
        "semantic_verified": False,
        "project": project.name,
        "baseline_sha256": prior_sha,
        "current_sha256": current_sha,
        "bytes_changed": byte_change,
        "changed_requirements": changes,
        "unchanged_requirement_ids": unchanged,
        "trace_status": trace["status"],
        "trace_issues": trace["issues"],
        "scope": "KNOWN_LOCATIONS_ONLY" if located else "NOT_PROVEN",
        "approval_binding": _approval_binding(project, current_sha),
        "render_data_binding": _projection_binding(project, current_sha),
        "not_proven": [
            "semantic conservation and cross-role consistency",
            "that unmarked downstream dependencies are unaffected",
            "source changes outside the supplied requirement snapshots",
        ],
        "next_action": (
            "No requirement register bytes changed; check other project sources separately."
            if status == "no_change"
            else "Reconcile exact SHA bindings and derived delivery; parsed requirements did not change."
            if status == "byte_only_change"
            else "Review listed requirement changes and current content locations; preserve unrelated content, "
            "reconcile source approval and downstream acceptance before regenerating."
        ),
    }
