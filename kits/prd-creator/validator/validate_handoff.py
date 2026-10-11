#!/usr/bin/env python3
"""Validate optional Voice work against the current accepted PRD handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
KIT_ROOT = HERE.parent
if __package__ in (None, ""):
    if str(KIT_ROOT) not in sys.path:
        sys.path.insert(0, str(KIT_ROOT))
    from shared.acceptance import required_value_issues, sha_binding_issues
    from shared.handoff import load_handoff_state
    from shared.issues import Issue
    from shared.paths import ProjectPathError, resolve_project_path
    from shared.state import StateError

    from validator import api as prd_api
else:
    from shared.acceptance import required_value_issues, sha_binding_issues
    from shared.handoff import load_handoff_state
    from shared.issues import Issue
    from shared.paths import ProjectPathError, resolve_project_path
    from shared.state import StateError

    from . import api as prd_api

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
ACCEPTANCE_REQUIRED = {
    "Status": {"handoff_ready"},
    "Mechanical": {"PASS"},
    "Semantic Readiness": {"PASS"},
    "Material Conservation": {"PASS"},
    "Visual sanity": {"PASS", "NOT PROVEN"},
    "Critical": {"0"},
    "Major": {"0"},
}
ACCEPTED_RENDER_LABEL = "Accepted Render Data SHA256"
ACCEPTED_ASSET_LABEL = "Accepted Asset Requirements SHA256"


def acceptance_issues(
    path: Path,
    expected_render_sha: str,
    expected_asset_sha: str,
) -> list[Issue]:
    if not path.is_file():
        return [
            Issue(
                "PRD_ACCEPTANCE_MISSING",
                "flow4.acceptance",
                "missing acceptance artifact",
                path="work/acceptance.md",
            )
        ]

    text = path.read_text(encoding="utf-8")
    issues = required_value_issues(
        text,
        ACCEPTANCE_REQUIRED,
        owner="flow4.acceptance",
        path="work/acceptance.md",
        code_prefix="PRD_ACCEPTANCE",
    )
    issues.extend(
        sha_binding_issues(
            text,
            ACCEPTED_RENDER_LABEL,
            expected_render_sha,
            owner="flow4.acceptance",
            path="work/acceptance.md",
            code="PRD_ACCEPTANCE_RENDER_SHA",
        )
    )
    issues.extend(
        sha_binding_issues(
            text,
            ACCEPTED_ASSET_LABEL,
            expected_asset_sha,
            owner="flow4.acceptance",
            path="work/acceptance.md",
            code="PRD_ACCEPTANCE_ASSET_SHA",
            allow_none=True,
        )
    )
    return issues


def validate_acceptance(
    path: Path,
    expected_render_sha: str,
    expected_asset_sha: str,
) -> tuple[bool, str]:
    """Compatibility helper for callers/tests that need the historical bool/detail API."""

    findings = acceptance_issues(path, expected_render_sha, expected_asset_sha)
    if findings:
        return False, "; ".join(str(issue) for issue in findings)
    return (
        True,
        "acceptance.md authorizes the exact current render-data and non-Voice asset-requirements revisions",
    )


def expected_refs(version: str) -> dict[str, str]:
    base = f"output/v{version}"
    return {
        "content": "work/content.md",
        "render_data": "work/render-data.json",
        "html": f"{base}/prd.html",
        "context": f"{base}/context.md",
        "index": f"{base}/index.json",
        "acceptance": "work/acceptance.md",
        "handoff": "output/README.md",
    }


def _result(
    errors: list[str],
    checks: list[dict[str, str]],
    issues: list[Issue | dict[str, object]],
) -> dict[str, Any]:
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "checks": checks,
        "issues": [item.as_dict() if isinstance(item, Issue) else item for item in issues],
    }


def validate(project: Path) -> dict[str, Any]:
    project = project.resolve()
    state_path = project / "state" / "handoff-state.yaml"
    data_path = project / "work" / "render-data.json"
    acceptance_path = project / "work" / "acceptance.md"
    asset_path = project / "work" / "asset-requirements.md"
    errors: list[str] = []
    checks: list[dict[str, str]] = []
    issues: list[Issue | dict[str, object]] = []

    def check(
        name: str,
        ok: bool,
        detail: str,
        *,
        code: str,
        owner: str = "flow4.handoff",
        path: str = "",
        field: str = "",
        record_issue: bool = True,
    ) -> None:
        checks.append({"check": name, "status": "pass" if ok else "fail", "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")
            if record_issue:
                issues.append(Issue(code, owner, detail, path=path, field=field))

    check(
        "handoff_state_exists",
        state_path.is_file(),
        str(state_path),
        code="HANDOFF_STATE_MISSING",
        path="state/handoff-state.yaml",
    )
    check(
        "render_data_exists",
        data_path.is_file(),
        str(data_path),
        code="HANDOFF_RENDER_DATA_MISSING",
        path="work/render-data.json",
    )
    if errors:
        return _result(errors, checks, issues)

    try:
        state = load_handoff_state(state_path)
    except (OSError, StateError) as exc:
        detail = str(exc)
        errors.append(f"handoff_state: {detail}")
        issues.append(
            Issue(
                "HANDOFF_STATE_INVALID",
                "flow4.handoff",
                detail,
                path="state/handoff-state.yaml",
            )
        )
        return _result(errors, checks, issues)

    check(
        "handoff_status_ready",
        state.status == "handoff_ready",
        "handoff_ready" if state.status == "handoff_ready" else f"status is {state.status!r}, expected 'handoff_ready'",
        code="HANDOFF_STATUS_NOT_READY",
        path="state/handoff-state.yaml",
        field="status",
    )

    current_prd = prd_api.validate(project)
    current_prd_ok = current_prd.get("status") == "pass"
    current_prd_errors = [str(item) for item in current_prd.get("errors", [])]
    check(
        "current_prd_complete_validation",
        current_prd_ok,
        "canonical PRD validation passes, including Flow 2 approval, projection schema, content purity, and freshness"
        if current_prd_ok
        else "; ".join(current_prd_errors[:5]) or "canonical PRD validation failed",
        code="HANDOFF_UPSTREAM_PRD_INVALID",
        owner="flow4.validation",
    )
    if not current_prd_ok:
        for issue in current_prd.get("issues", []):
            if isinstance(issue, dict):
                issues.append(issue)

    try:
        data_bytes = data_path.read_bytes()
        data = json.loads(data_bytes.decode("utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        detail = str(exc)
        errors.append(f"render_data_json: {detail}")
        issues.append(
            Issue(
                "HANDOFF_RENDER_DATA_INVALID",
                "flow4.handoff",
                detail,
                path="work/render-data.json",
                line=exc.lineno if isinstance(exc, json.JSONDecodeError) else None,
            )
        )
        return _result(errors, checks, issues)

    current_render_sha = hashlib.sha256(data_bytes).hexdigest()
    current_asset_sha = hashlib.sha256(asset_path.read_bytes()).hexdigest() if asset_path.is_file() else "none"
    doc = data.get("document") if isinstance(data, dict) else None
    current_version = str(doc.get("version") or "").strip() if isinstance(doc, dict) else ""
    check(
        "current_prd_version_present",
        bool(current_version),
        f"current document.version is {current_version!r}"
        if current_version
        else "render-data.document.version is required for handoff",
        code="HANDOFF_VERSION_MISSING",
        path="work/render-data.json",
        field="document.version",
    )
    check(
        "current_prd_version_semantic",
        bool(SEMVER_RE.fullmatch(current_version)),
        f"current document.version is {current_version!r}; expected X.Y.Z",
        code="HANDOFF_VERSION_INVALID",
        path="work/render-data.json",
        field="document.version",
    )
    check(
        "handoff_revision_matches_current_prd",
        bool(current_version) and state.accepted_prd_version == current_version,
        f"accepted_prd_version={state.accepted_prd_version!r}, current document.version={current_version!r}",
        code="HANDOFF_VERSION_STALE",
        path="state/handoff-state.yaml",
        field="accepted_prd_version",
    )

    refs = expected_refs(current_version) if SEMVER_RE.fullmatch(current_version) else {}
    refs_ok = bool(refs)
    ref_details: list[str] = []
    if not refs:
        ref_details.append("cannot resolve versioned handoff paths until document.version uses X.Y.Z")
    else:
        for field, ref in refs.items():
            try:
                resolve_project_path(
                    project,
                    ref,
                    owner=f"derived handoff artifact {field}",
                    must_exist=True,
                )
            except ProjectPathError as exc:
                refs_ok = False
                ref_details.append(str(exc))
    check(
        "handoff_artifact_references_current",
        refs_ok,
        "canonical handoff artifact paths are derived from the accepted PRD version and all artifacts exist"
        if refs_ok
        else "; ".join(ref_details),
        code="HANDOFF_REFERENCES_INVALID",
        path="state/handoff-state.yaml",
    )

    delivery_ok = bool(refs)
    delivery_details: list[str] = []
    if refs:
        try:
            context_text = resolve_project_path(project, refs["context"], must_exist=True).read_text(encoding="utf-8")
            readme_text = resolve_project_path(project, refs["handoff"], must_exist=True).read_text(encoding="utf-8")
            index_data = json.loads(
                resolve_project_path(project, refs["index"], must_exist=True).read_text(encoding="utf-8")
            )
            index_project = index_data.get("project") if isinstance(index_data, dict) else None
            index_version = (
                str(index_project.get("prd_version") or "").strip() if isinstance(index_project, dict) else ""
            )
            if f"PRD Version: v{current_version}" not in context_text:
                delivery_ok = False
                delivery_details.append("context.md PRD version does not match current document.version")
            if f"Current PRD Version: `v{current_version}`" not in readme_text:
                delivery_ok = False
                delivery_details.append("output/README.md current version does not match document.version")
            if index_version != current_version:
                delivery_ok = False
                delivery_details.append(
                    f"index.json project.prd_version={index_version!r}, expected {current_version!r}"
                )
        except (OSError, ProjectPathError, json.JSONDecodeError) as exc:
            delivery_ok = False
            delivery_details.append(f"delivery metadata unreadable: {exc}")
    check(
        "delivery_revision_matches_current_prd",
        delivery_ok,
        "context.md, index.json, and output/README.md identify the current PRD revision"
        if delivery_ok
        else "; ".join(delivery_details) or "delivery metadata could not be verified",
        code="HANDOFF_DELIVERY_STALE",
        owner="flow4.delivery",
    )

    acceptance_findings = acceptance_issues(
        acceptance_path,
        current_render_sha,
        current_asset_sha,
    )
    acceptance_ok = not acceptance_findings
    acceptance_detail = (
        "acceptance.md authorizes the exact current render-data and non-Voice asset-requirements revisions"
        if acceptance_ok
        else "; ".join(str(issue) for issue in acceptance_findings)
    )
    check(
        "acceptance_allows_handoff",
        acceptance_ok,
        acceptance_detail,
        code="HANDOFF_ACCEPTANCE_INVALID",
        owner="flow4.acceptance",
        path="work/acceptance.md",
        record_issue=False,
    )
    issues.extend(acceptance_findings)

    return _result(errors, checks, issues)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="workspace/active/<project> directory")
    args = parser.parse_args()
    result = validate(args.project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
