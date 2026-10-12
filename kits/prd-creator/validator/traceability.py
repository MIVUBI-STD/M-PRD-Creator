"""Read-only requirement location evidence and semantic review prompts.

PRD-TRACE markers prove location, never semantic correctness.
"""

from __future__ import annotations

import hashlib
import json
import re
from itertools import islice
from pathlib import Path
from typing import Any

from shared.intake import SourceRecord, load_intake_state, load_requirement_register, load_source_inventory, sha256_file
from shared.issues import Issue
from shared.paths import resolve_project_path
from shared.state import StateError

MARKER = re.compile(r"^\s*<!-- PRD-TRACE: (REQ-\d{3,}) -->\s*$")
HINT = re.compile(r"<!--\s*PRD-TRACE\b", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
CONTENT = "work/content.md"
HTML_CODE_START = re.compile(r"^<(pre|code|script|style)\b", re.IGNORECASE)
SOURCE_LINES = re.compile(r"^(.+?)#L([1-9][0-9]*)(?:-L([1-9][0-9]*))?$")


def _is_indented_code(line: str) -> bool:
    """CommonMark indented code is not live PRD evidence."""
    spaces = len(line) - len(line.lstrip(" "))
    return spaces >= 4 or line[spaces:].startswith("\t")


def _issue(code: str, message: str, line: int | None = None, field: str = "") -> dict[str, object]:
    return Issue(code, "prd.traceability", message, path=CONTENT, line=line, field=field).as_dict()


def _next_claim(lines: list[str], index: int) -> tuple[int, str] | None:
    for offset in range(index + 1, min(index + 5, len(lines))):
        text = lines[offset].strip()
        if not text:
            continue
        if (
            _is_indented_code(lines[offset])
            or text.startswith(("#", "<!--", "\x60\x60\x60", "~~~"))
            or text in {"---", "***", "___"}
            or HTML_CODE_START.match(text)
        ):
            return None
        return offset + 1, text[:240]
    return None


def _retained_source_excerpt(project: Path, locator: str, source: SourceRecord) -> dict[str, object]:
    """Read only an exact, bounded locator from a current retained text source."""
    if source.retention != "repository" or source.status != "current" or source.inspection == "blocked":
        return {}
    match = SOURCE_LINES.fullmatch(locator)
    if match is None or match.group(1) != source.path:
        return {}
    first = int(match.group(2))
    last = int(match.group(3) or match.group(2))
    if last < first or last - first >= 8:
        return {}
    try:
        path = resolve_project_path(project, source.path, must_exist=True)
        with path.open(encoding="utf-8") as stream:
            excerpt = list(islice(stream, first - 1, last))
    except (OSError, UnicodeError, ValueError):
        return {}
    if len(excerpt) != last - first + 1 or sum(map(len, excerpt)) > 2400:
        return {}
    return {"source_excerpt_lines": [first, last], "source_excerpt": "".join(excerpt).rstrip("\r\n")}

def approval_binding(project: Path, current_sha: str) -> dict[str, Any]:
    """Report existing intake approval freshness without claiming semantic approval."""
    try:
        state = load_intake_state(project / "state" / "intake-state.yaml")
    except (OSError, StateError) as exc:
        return {"status": "unavailable", "reason": str(exc)}
    return {
        "status": "current" if state.approved_requirement_sha256 == current_sha else "stale",
        "intake_status": state.status,
    }


def projection_binding(project: Path, current_sha: str) -> str:
    """Check only current render-data requirement/content SHA bindings."""
    path = project / "work" / "render-data.json"
    if not path.is_file():
        return "not_present"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return "unreadable"
    if not isinstance(value, dict):
        return "unreadable"
    try:
        actual_content_sha = hashlib.sha256((project / "work" / "content.md").read_bytes()).hexdigest()
    except OSError:
        return "unavailable"
    bindings_current = (
        value.get("approved_requirement_sha256") == current_sha
        and value.get("canonical_content_sha256") == actual_content_sha
    )
    return "current" if bindings_current else "stale"


def _review_cases(project: Path) -> list[dict[str, Any]]:
    """Expose comparable gameplay/design/developer fields; never infer agreement."""
    path = project / "work" / "render-data.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    packages = data.get("packages")
    if not isinstance(packages, list):
        return []
    result = []
    for package in packages:
        if not isinstance(package, dict):
            continue
        gameplay = package.get("gameplay")
        level = package.get("level_design")
        developer = package.get("developer")
        if not all(isinstance(section, dict) for section in (gameplay, level, developer)):
            continue
        mode_data = gameplay.get("result_model")
        mode = mode_data.get("mode") if isinstance(mode_data, dict) else None
        result_key = "scoring" if mode == "scored" else "completion_data"
        result.append(
            {
                "package_id": package.get("id"),
                "semantic_status": "NOT_VERIFIED",
                "result_mode": mode,
                "compare": {
                    "gameplay.start_condition": gameplay.get("start_condition"),
                    "gameplay.end_condition": gameplay.get("end_condition"),
                    "gameplay.blocked_or_fail_condition": gameplay.get("blocked_or_fail_condition"),
                    "gameplay.result": gameplay.get("result"),
                    "gameplay.player_flow": gameplay.get("player_flow"),
                    "level_design.flow": level.get("flow"),
                    "level_design.requirements": level.get("requirements"),
                    "developer.flow": developer.get("flow"),
                    "developer.requirements": developer.get("requirements"),
                    "developer.reset": developer.get("reset"),
                    "developer.reset_result": developer.get("reset_result"),
                    "developer.result": developer.get(result_key),
                    "package.acceptance": package.get("acceptance"),
                },
                "questions": [
                    "Does the Level Design route support the Gameplay objective and exit?",
                    "Do Developer lifecycle and reset match interruption and recovery?",
                    "Do the result mode, stored data and acceptance conditions agree?",
                ],
            }
        )
    return result


def assess(project: Path) -> dict[str, Any]:
    """Locate optional inline REQ markers without altering canonical sources."""
    project = project.resolve()
    report: dict[str, Any] = {
        "status": "unavailable",
        "semantic_verified": False,
        "requirements": [],
        "unmapped": [],
        "issues": [],
        "review_cases": [],
        "review_approval_binding": "unavailable",
        "review_projection_binding": "unavailable",
    }
    try:
        sources = load_source_inventory(project / "state/source-inventory.yaml", project)
        requirements = load_requirement_register(project / "state/requirement-register.yaml", sources)
        lines = (project / CONTENT).read_text(encoding="utf-8").splitlines()
    except (OSError, StateError, UnicodeError) as exc:
        report["issues"] = [_issue("PRD_TRACE_SOURCE_UNAVAILABLE", str(exc))]
        return report

    current_sha = sha256_file(project / "state/requirement-register.yaml")
    approval = approval_binding(project, current_sha)
    projection = projection_binding(project, current_sha)
    report["review_approval_binding"] = approval["status"]
    report["review_projection_binding"] = projection
    if approval["status"] == "current" and projection == "current":
        report["review_cases"] = _review_cases(project)

    by_source = {source.source_id: source for source in sources}
    mapped: dict[str, list[dict[str, object]]] = {req.requirement_id: [] for req in requirements}
    issues: list[dict[str, object]] = []
    heading = ""
    marker_count = 0
    fence: str | None = None
    html_code: str | None = None
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if _is_indented_code(line):
            continue
        if html_code is not None:
            if re.search(rf"</{html_code}\s*>", stripped, re.IGNORECASE):
                html_code = None
            continue
        html_start = HTML_CODE_START.match(stripped)
        if html_start is not None:
            tag = html_start.group(1).lower()
            if re.search(rf"</{tag}\s*>", stripped, re.IGNORECASE) is None:
                html_code = tag
            continue
        opening = next((token for token in (chr(96) * 3, "~~~") if stripped.startswith(token)), None)
        if opening is not None:
            fence = opening
            continue
        title = HEADING.fullmatch(line.strip())
        if title:
            heading = title.group(1)
        if not HINT.search(line):
            continue
        marker_count += 1
        match = MARKER.fullmatch(line)
        if not match:
            issues.append(_issue("PRD_TRACE_FORMAT_INVALID", "Use standalone PRD-TRACE marker", i + 1))
            continue
        req_id = match.group(1)
        if req_id not in mapped:
            issues.append(_issue("PRD_TRACE_UNKNOWN_REQUIREMENT", "Unknown current requirement " + req_id, i + 1))
            continue
        claim = _next_claim(lines, i)
        if claim is None:
            issues.append(_issue("PRD_TRACE_DETACHED", req_id + " must precede PRD prose", i + 1))
            continue
        line_number, excerpt = claim
        mapped[req_id].append({"marker_line": i + 1, "claim_line": line_number, "heading": heading, "excerpt": excerpt})

    missing = []
    for requirement in requirements:
        matches = mapped[requirement.requirement_id]
        if not matches:
            missing.append(requirement.requirement_id)
        report["requirements"].append(
            {
                "id": requirement.requirement_id,
                "statement": requirement.statement,
                "area": requirement.area,
                "evidence_locator": requirement.evidence_locator,
                "evidence_status": requirement.evidence_status,
                "source_evidence": [
                    {
                        "id": sid,
                        "role": by_source[sid].role,
                        "status": by_source[sid].status,
                        "inspection": by_source[sid].inspection,
                        "retention": by_source[sid].retention,
                        "path": by_source[sid].path,
                        **_retained_source_excerpt(project, requirement.evidence_locator, by_source[sid]),
                    }
                    for sid in requirement.provenance
                ],
                "mapping": "LOCATED_NOT_SEMANTICALLY_VERIFIED" if matches else "UNMAPPED",
                "locations": matches,
            }
        )
    if marker_count:
        issues.extend(_issue("PRD_TRACE_UNMAPPED", req_id + " has no PRD location", field=req_id) for req_id in missing)
    report["unmapped"] = missing
    report["mapped_count"] = len(requirements) - len(missing)
    report["total_requirements"] = len(requirements)
    report["issues"] = issues
    if not marker_count:
        report["status"] = "unreviewed"
    elif any(item["code"] != "PRD_TRACE_UNMAPPED" for item in issues):
        report["status"] = "invalid"
    elif missing:
        report["status"] = "incomplete"
    else:
        report["status"] = "mapped_unverified"
    return report
