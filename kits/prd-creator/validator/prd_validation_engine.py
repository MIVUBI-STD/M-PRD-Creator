from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from shared.assets import parse_asset_requirements
from shared.intake import load_intake_state, validate_flow2_state
from shared.issues import Issue, SourceParseError
from shared.render_schema import ProjectionError, validate_projection_schema
from shared.state import StateError
from shared.topology import require_owner

from .html_contract import validate_html_contract

OPEN_RE = re.compile(r"\b(?:TBD|TODO|FIXME|INSERT\s+(?:TEXT|VALUE)|USE\s+APPROVED\s+AMOUNT)\b|\[OPEN\]", re.I)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
WEIGHT_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*%?\s*$")


def text_en(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("en") or value.get("id") or ""
    return str(value or "")


def scoring_weight(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        if isinstance(value, (int, float)):
            weight = float(value)
        elif isinstance(value, str):
            match = WEIGHT_RE.fullmatch(value)
            if match is None:
                return None
            weight = float(match.group(1))
        else:
            return None
    except (OverflowError, ValueError):
        return None
    return weight if math.isfinite(weight) and 0 <= weight <= 100 else None


def _scoring_weight_issues(data: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    for package in data.get("packages", []):
        package_id = package["id"]
        developer = package["developer"]
        scoring = developer.get("scoring")
        if not isinstance(scoring, dict):
            continue
        components = scoring.get("components", [])
        if not isinstance(components, list) or not components:
            continue
        parsed: list[float] = []
        for index, component in enumerate(components):
            weight = scoring_weight(component.get("weight") if isinstance(component, dict) else None)
            if weight is None:
                issues.append(
                    Issue(
                        "PRD_SCORING_WEIGHT_INVALID",
                        "flow3.projection",
                        "scoring component weight must be a finite percentage between 0 and 100",
                        path="work/render-data.json",
                        field=f"packages.{package_id}.developer.scoring.components[{index}].weight",
                    )
                )
            else:
                parsed.append(weight)
        if len(parsed) == len(components) and abs(sum(parsed) - 100.0) > 1e-9:
            issues.append(
                Issue(
                    "PRD_SCORING_WEIGHT_TOTAL_INVALID",
                    "flow3.projection",
                    f"scoring weights total {sum(parsed):g}, expected 100",
                    path="work/render-data.json",
                    field=f"packages.{package_id}.developer.scoring.components",
                )
            )
    return issues


def _asset_source_issues(project: Path, data: dict[str, Any]) -> list[Issue]:
    path = project / "work" / "asset-requirements.md"
    if not path.is_file():
        return []
    try:
        assets = parse_asset_requirements(path)
        for section in assets.sections:
            require_owner(data, section.owner_id)
    except SourceParseError as exc:
        return [exc.as_issue()]
    except (OSError, ValueError) as exc:
        return [
            Issue(
                "PRD_ASSET_SOURCE_INVALID",
                "production_assets.source",
                str(exc),
                path="work/asset-requirements.md",
            )
        ]
    return []


def validate(project: Path) -> dict[str, Any]:
    project = project.resolve()
    content_path = project / "work" / "content.md"
    data_path = project / "work" / "render-data.json"
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, str]] = []
    structured: list[Issue] = []

    def check(name: str, ok: bool, detail: str, issue: Issue | None = None) -> None:
        checks.append({"check": name, "status": "pass" if ok else "fail", "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")
            if issue is not None:
                structured.append(issue)

    flow2_issues = validate_flow2_state(project, warnings=warnings)
    check(
        "flow2_state_current",
        not flow2_issues,
        "Flow 2 approval is bound to the current requirement-register revision"
        if not flow2_issues
        else "; ".join(str(issue) for issue in flow2_issues),
    )
    structured.extend(flow2_issues)
    check(
        "canonical_content_exists",
        content_path.is_file(),
        str(content_path),
        Issue("PRD_CONTENT_MISSING", "flow3.content", "canonical content is missing", path="work/content.md"),
    )
    check(
        "render_data_exists",
        data_path.is_file(),
        str(data_path),
        Issue("PRD_PROJECTION_MISSING", "flow3.projection", "render-data is missing", path="work/render-data.json"),
    )
    if errors:
        return _result(errors, warnings, checks, structured)

    content = content_path.read_text(encoding="utf-8")
    check(
        "canonical_content_has_no_open_placeholders",
        OPEN_RE.search(content) is None,
        "content.md contains no unresolved placeholder token",
        Issue(
            "PRD_CONTENT_PLACEHOLDER",
            "flow3.content",
            "canonical content contains an unresolved placeholder",
            path="work/content.md",
        ),
    )

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"render_data_json: {exc}")
        structured.append(
            Issue(
                "PRD_PROJECTION_JSON_INVALID",
                "flow3.projection",
                str(exc),
                path="work/render-data.json",
                line=exc.lineno,
            )
        )
        return _result(errors, warnings, checks, structured)
    if not isinstance(data, dict):
        errors.append("render_data_root: render-data must be an object")
        structured.append(
            Issue(
                "PRD_PROJECTION_ROOT_INVALID",
                "flow3.projection",
                "render-data root must be an object",
                path="work/render-data.json",
            )
        )
        return _result(errors, warnings, checks, structured)

    try:
        validate_projection_schema(data)
    except ProjectionError as exc:
        check(
            "projection_schema",
            False,
            str(exc),
            Issue(
                "PRD_PROJECTION_SCHEMA_INVALID",
                "flow3.projection",
                str(exc),
                path="work/render-data.json",
            ),
        )
        return _result(errors, warnings, checks, structured)
    check("projection_schema", True, "render-data uses the one canonical projection field shape")

    try:
        intake = load_intake_state(project / "state" / "intake-state.yaml")
    except (OSError, StateError) as exc:
        check(
            "projection_matches_approved_requirements",
            False,
            str(exc),
            Issue(
                "PRD_PROJECTION_REQUIREMENT_BINDING_INVALID",
                "flow3.projection",
                str(exc),
                path="state/intake-state.yaml",
                line=exc.line if isinstance(exc, StateError) else None,
            ),
        )
    else:
        declared_requirement_sha = str(data["approved_requirement_sha256"])
        requirement_binding_ok = declared_requirement_sha == intake.approved_requirement_sha256
        check(
            "projection_matches_approved_requirements",
            requirement_binding_ok,
            "render-data is bound to the exact Flow 2 requirement revision"
            if requirement_binding_ok
            else "render-data approved_requirement_sha256 does not match current Flow 2 approval",
            Issue(
                "PRD_PROJECTION_REQUIREMENT_STALE",
                "flow3.projection",
                "render-data approved_requirement_sha256 does not match current Flow 2 approval",
                path="work/render-data.json",
                field="approved_requirement_sha256",
            ),
        )

    actual_content_sha = hashlib.sha256(content_path.read_bytes()).hexdigest()
    declared_content_sha = str(data["canonical_content_sha256"])
    content_binding_ok = declared_content_sha == actual_content_sha
    check(
        "render_data_matches_canonical_content",
        content_binding_ok,
        "render-data is bound to the current canonical content revision"
        if content_binding_ok
        else "render-data projection is stale relative to work/content.md",
        Issue(
            "PRD_PROJECTION_STALE",
            "flow3.projection",
            "render-data canonical_content_sha256 does not match current content.md bytes",
            path="work/render-data.json",
            field="canonical_content_sha256",
        ),
    )

    scoring_issues = _scoring_weight_issues(data)
    check(
        "scoring_weights",
        not scoring_issues,
        "scoring weights are coherent" if not scoring_issues else "; ".join(str(issue) for issue in scoring_issues),
    )
    structured.extend(scoring_issues)

    asset_issues = _asset_source_issues(project, data)
    check(
        "asset_requirements_source",
        not asset_issues,
        "non-Voice Production Asset source is valid against accepted topology"
        if not asset_issues
        else "; ".join(str(issue) for issue in asset_issues),
    )
    structured.extend(asset_issues)

    document = data["document"]
    current_version = text_en(document["version"]).strip()
    version_ok = SEMVER_RE.fullmatch(current_version) is not None
    check(
        "document_version_semantic",
        version_ok,
        f"document.version={current_version!r}",
        Issue(
            "PRD_VERSION_INVALID",
            "flow3.projection",
            f"document.version={current_version!r}; expected semantic X.Y.Z",
            path="work/render-data.json",
            field="document.version",
        ),
    )
    html_path = project / "output" / f"v{current_version}" / "prd.html"
    check(
        "rendered_html_exists",
        html_path.is_file(),
        str(html_path),
        Issue(
            "PRD_HTML_MISSING",
            "flow3.renderer",
            "current rendered PRD HTML is missing",
            path=f"output/v{current_version}/prd.html",
        ),
    )
    if errors:
        return _result(errors, warnings, checks, structured)

    html_result = validate_html_contract(project, data, data_path, html_path)
    for html_check in html_result.checks:
        check(html_check.name, html_check.ok, html_check.detail, html_check.issue)

    return _result(
        errors,
        warnings,
        checks,
        structured,
        expected_pages=list(html_result.expected_pages),
    )


def _result(
    errors: list[str],
    warnings: list[str],
    checks: list[dict[str, str]],
    issues: list[Issue],
    *,
    expected_pages: list[str] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "issues": [issue.as_dict() for issue in issues],
    }
    if expected_pages is not None:
        result["expected_pages"] = expected_pages
    return result
