from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any

from renderer.delivery import build_context, build_index
from shared.acceptance import required_value_issues, sha_binding_issues
from shared.handoff import load_handoff_state
from shared.issues import Issue, SourceParseError
from shared.lifecycle import VoiceState, load_voice_state
from shared.paths import ProjectPathError, resolve_project_path
from shared.state import StateError
from shared.topology import owner_targets, production_page_id
from shared.voice import (
    VoiceEntry,
    VoiceProduction,
    VoiceRequirement,
    parse_production,
    parse_requirements,
    selected_voice,
)

from . import validate_handoff as handoff_validator

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_PRD_REVISION_RE = re.compile(r"(?mi)^\s*Source PRD revision:\s*(\S+)\s*$")
SOURCE_REQUIREMENTS_RE = re.compile(
    r"(?mi)^\s*Source Voice Requirements:\s*(\S+)\s*/\s*(.+?)\s*\|\s*sha256:([0-9a-f]{64})\s*$"
)
META_RE_TEMPLATE = r'<meta\s+content="([0-9a-f]{{64}})"\s+name="{name}"\s*/?>'
REQUIREMENTS_READY_STATUSES = {"voice_requirements_ready"}
SCRIPT_STATUSES = {"voice_script_ready", "voice_validation", "needs_revision", "voice_delivery_ready"}
VALIDATABLE_STATUSES = REQUIREMENTS_READY_STATUSES | SCRIPT_STATUSES | {"no_voice_required"}
VOICE_ACCEPTANCE_REQUIRED = {
    "Status": {"voice_delivery_ready"},
    "Mechanical": {"PASS"},
    "Voice Script Readiness": {"PASS"},
    "Communication Conservation": {"PASS"},
    "Project HTML Visual": {"PASS", "NOT PROVEN"},
    "Critical": {"0"},
    "Major": {"0"},
}
VOICE_ACCEPTED_SHA_LABEL = "Accepted Voice Production SHA256"


def _issue(
    code: str,
    owner: str,
    message: str,
    *,
    path: str = "",
    line: int | None = None,
    field: str = "",
) -> Issue:
    return Issue(code, owner, message, path=path, line=line, field=field)


def _load_render_data(project: Path) -> tuple[dict[str, Any], str, str]:
    path = project / "work" / "render-data.json"
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Current render-data.json root must be an object")
    document = data.get("document")
    if not isinstance(document, dict):
        raise ValueError("Current render-data.json must contain document metadata")
    revision = str(document.get("version") or "").strip()
    if not revision:
        raise ValueError("Current render-data document.version is required for Voice")
    return data, revision, hashlib.sha256(raw).hexdigest()


def _accepted_revision(project: Path, voice_state: VoiceState) -> tuple[str, list[Issue], list[str]]:
    issues: list[Issue] = []
    try:
        upstream = handoff_validator.validate(project)
    except (OSError, StateError, ProjectPathError, ValueError, json.JSONDecodeError) as exc:
        upstream = {"status": "fail", "errors": [str(exc)]}
    raw_warnings = upstream.get("warnings")
    upstream_warnings = (
        [item for item in raw_warnings if isinstance(item, str)]
        if isinstance(raw_warnings, list)
        else []
    )
    if upstream.get("status") != "pass":
        detail = "; ".join(str(item) for item in upstream.get("errors", [])[:5]) or "unknown handoff failure"
        issues.append(
            _issue(
                "VOICE_UPSTREAM_HANDOFF_INVALID",
                "flow5.voice_requirement",
                "Upstream PRD handoff validation failed: " + detail,
                path="state/handoff-state.yaml",
            )
        )

    try:
        handoff_path = resolve_project_path(
            project,
            voice_state.source_handoff,
            owner="voice-state.yaml.source_handoff",
            must_exist=True,
        )
        handoff = load_handoff_state(handoff_path)
    except (OSError, ProjectPathError, StateError) as exc:
        issues.append(
            _issue(
                "VOICE_SOURCE_HANDOFF_INVALID",
                "flow5.voice_requirement",
                str(exc),
                path="state/voice-state.yaml",
                field="source_handoff",
            )
        )
        return "", issues, upstream_warnings
    if handoff.status != "handoff_ready":
        issues.append(
            _issue(
                "VOICE_SOURCE_HANDOFF_NOT_READY",
                "flow5.voice_requirement",
                f"Upstream PRD handoff status is {handoff.status!r}, expected 'handoff_ready'",
                path="state/handoff-state.yaml",
                field="status",
            )
        )
    return handoff.accepted_prd_version, issues, upstream_warnings


def _state_identity_issues(
    voice_state: VoiceState,
    accepted_revision: str,
    current_revision: str,
    current_render_sha: str,
) -> list[Issue]:
    issues: list[Issue] = []
    if voice_state.source_handoff != "state/handoff-state.yaml":
        issues.append(
            _issue(
                "VOICE_STATE_HANDOFF_PATH_INVALID",
                "voice.lifecycle",
                f"source_handoff={voice_state.source_handoff!r}, expected 'state/handoff-state.yaml'",
                path="state/voice-state.yaml",
                field="source_handoff",
            )
        )
    if voice_state.source_prd_revision != accepted_revision:
        issues.append(
            _issue(
                "VOICE_STATE_REVISION_STALE",
                "voice.lifecycle",
                f"source_prd_revision={voice_state.source_prd_revision!r}, expected {accepted_revision!r}",
                path="state/voice-state.yaml",
                field="source_prd_revision",
            )
        )
    if current_revision != accepted_revision:
        issues.append(
            _issue(
                "VOICE_CURRENT_PRD_REVISION_STALE",
                "flow3.projection",
                f"current render-data document.version={current_revision!r}, expected accepted revision {accepted_revision!r}",
                path="work/render-data.json",
                field="document.version",
            )
        )
    if voice_state.source_prd_sha256 != current_render_sha:
        issues.append(
            _issue(
                "VOICE_STATE_PRD_SHA_STALE",
                "voice.lifecycle",
                "source_prd_sha256 does not match current accepted work/render-data.json bytes",
                path="state/voice-state.yaml",
                field="source_prd_sha256",
            )
        )
    canonical = {
        "canonical_prd": "work/content.md",
        "requirements": "work/voice-requirements.md",
        "production": "work/voice-production.md",
    }
    for field, expected in canonical.items():
        actual = getattr(voice_state, field)
        if actual != expected:
            issues.append(
                _issue(
                    "VOICE_STATE_PATH_INVALID",
                    "voice.lifecycle",
                    f"{field}={actual!r}, expected {expected!r}",
                    path="state/voice-state.yaml",
                    field=field,
                )
            )
    expected_html = f"output/v{accepted_revision}/prd.html"
    if voice_state.project_html and voice_state.project_html != expected_html:
        issues.append(
            _issue(
                "VOICE_STATE_HTML_PATH_INVALID",
                "voice.lifecycle",
                f"project_html={voice_state.project_html!r}, expected {expected_html!r}",
                path="state/voice-state.yaml",
                field="project_html",
            )
        )
    return issues


def _requirements_revision_issues(path: Path, accepted_revision: str) -> list[Issue]:
    revisions = SOURCE_PRD_REVISION_RE.findall(path.read_text(encoding="utf-8"))
    if len(revisions) != 1:
        return [
            _issue(
                "VOICE_REQUIREMENT_SOURCE_REVISION_INVALID",
                "flow5.voice_requirement",
                "voice-requirements.md must define exactly one Source PRD revision",
                path="work/voice-requirements.md",
                field="Source PRD revision",
            )
        ]
    current = revisions[0].strip()
    if current != accepted_revision:
        return [
            _issue(
                "VOICE_REQUIREMENT_SOURCE_REVISION_STALE",
                "flow5.voice_requirement",
                f"Source PRD revision={current!r}, expected {accepted_revision!r}",
                path="work/voice-requirements.md",
                field="Source PRD revision",
            )
        ]
    return []


def _requirements_owner_issues(
    render_data: dict[str, Any],
    requirements: dict[str, VoiceRequirement],
) -> list[Issue]:
    valid_owners = owner_targets(render_data)
    return [
        _issue(
            "VOICE_REQUIREMENT_OWNER_INVALID",
            "flow5.voice_requirement",
            f"Owner ID does not match accepted PRD topology: {requirement.owner_id}",
            path="work/voice-requirements.md",
            field=requirement.voice_id,
        )
        for requirement in requirements.values()
        if requirement.owner_id not in valid_owners
    ]


def _production_binding_issues(
    requirements_path: Path,
    production_path: Path,
    accepted_revision: str,
) -> list[Issue]:
    matches = SOURCE_REQUIREMENTS_RE.findall(production_path.read_text(encoding="utf-8"))
    if len(matches) != 1:
        return [
            _issue(
                "VOICE_PRODUCTION_SOURCE_BINDING_INVALID",
                "flow6.voice_production",
                "voice-production.md must define exactly one Source Voice Requirements binding with revision, canonical path, and sha256",
                path="work/voice-production.md",
                field="Source Voice Requirements",
            )
        ]
    revision, source_path, source_sha = (part.strip() for part in matches[0])
    issues: list[Issue] = []
    if revision != accepted_revision:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_SOURCE_REVISION_STALE",
                "flow6.voice_production",
                f"Source Voice Requirements revision={revision!r}, expected {accepted_revision!r}",
                path="work/voice-production.md",
                field="Source Voice Requirements",
            )
        )
    if source_path != "work/voice-requirements.md":
        issues.append(
            _issue(
                "VOICE_PRODUCTION_SOURCE_PATH_INVALID",
                "flow6.voice_production",
                f"Source Voice Requirements path={source_path!r}, expected 'work/voice-requirements.md'",
                path="work/voice-production.md",
                field="Source Voice Requirements",
            )
        )
    actual_sha = hashlib.sha256(requirements_path.read_bytes()).hexdigest()
    if SHA256_RE.fullmatch(source_sha) is None or source_sha != actual_sha:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_SOURCE_SHA_STALE",
                "flow6.voice_production",
                "Source Voice Requirements sha256 does not match current work/voice-requirements.md bytes",
                path="work/voice-production.md",
                field="Source Voice Requirements",
            )
        )
    return issues


def _production_parity_issues(
    render_data: dict[str, Any],
    requirements: dict[str, VoiceRequirement],
    production: VoiceProduction,
) -> list[Issue]:
    issues: list[Issue] = []
    valid_owners = owner_targets(render_data)
    production_by_id: dict[str, tuple[str, VoiceEntry]] = {}
    for section in production.sections:
        if section.owner_id not in valid_owners:
            issues.append(
                _issue(
                    "VOICE_PRODUCTION_OWNER_INVALID",
                    "flow6.voice_production",
                    f"Owner ID does not match accepted PRD topology: {section.owner_id}",
                    path="work/voice-production.md",
                    field="Owner ID",
                )
            )
        for entry in section.entries:
            production_by_id[entry.voice_id] = (section.owner_id, entry)

    missing = sorted(set(requirements) - set(production_by_id))
    extra = sorted(set(production_by_id) - set(requirements))
    if missing:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_IDS_MISSING",
                "flow6.voice_production",
                "Script missing Voice IDs: " + ", ".join(missing),
                path="work/voice-production.md",
            )
        )
    if extra:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_IDS_EXTRA",
                "flow6.voice_production",
                "Script has extra Voice IDs: " + ", ".join(extra),
                path="work/voice-production.md",
            )
        )

    for voice_id in sorted(set(requirements) & set(production_by_id)):
        requirement = requirements[voice_id]
        owner_id, entry = production_by_id[voice_id]
        if owner_id != requirement.owner_id:
            issues.append(
                _issue(
                    "VOICE_OWNER_MISMATCH",
                    "flow6.voice_production",
                    f"production={owner_id!r}, requirement={requirement.owner_id!r}",
                    path="work/voice-production.md",
                    field=voice_id,
                )
            )
        if requirement.voice_type.casefold() != entry.voice_type.casefold():
            issues.append(
                _issue(
                    "VOICE_TYPE_MISMATCH",
                    "flow6.voice_production",
                    f"Type differs from Flow 5 requirement for {voice_id}",
                    path="work/voice-production.md",
                    field=voice_id,
                )
            )
        if requirement.speaker.casefold() != entry.speaker.casefold():
            issues.append(
                _issue(
                    "VOICE_SPEAKER_MISMATCH",
                    "flow6.voice_production",
                    f"Speaker differs from Flow 5 requirement for {voice_id}",
                    path="work/voice-production.md",
                    field=voice_id,
                )
            )
    return issues


def _meta_sha(source: str, name: str) -> str:
    matches = re.findall(META_RE_TEMPLATE.format(name=re.escape(name)), source, flags=re.I)
    return matches[0] if len(matches) == 1 else ""


def _html_issues(
    path: Path,
    render_data: dict[str, Any],
    requirements_path: Path,
    production_path: Path,
    requirements: dict[str, VoiceRequirement],
    production: VoiceProduction,
) -> list[Issue]:
    source = path.read_text(encoding="utf-8")
    issues: list[Issue] = []
    html_path = path.as_posix()
    if 'id="production-assets-style"' not in source or 'id="production-assets-script"' not in source:
        issues.append(
            _issue(
                "VOICE_HTML_RESOURCES_MISSING",
                "flow7.voice_delivery",
                "Project HTML missing current Production Assets presentation resources",
                path=html_path,
            )
        )
    if "Production Assets" not in source or "production-assets-nav" not in source:
        issues.append(
            _issue(
                "VOICE_HTML_NAVIGATION_MISSING",
                "flow7.voice_delivery",
                "Project HTML missing Production Assets Voice navigation",
                path=html_path,
            )
        )

    requirements_sha = hashlib.sha256(requirements_path.read_bytes()).hexdigest()
    production_sha = hashlib.sha256(production_path.read_bytes()).hexdigest()
    if _meta_sha(source, "voice-requirements-sha256") != requirements_sha:
        issues.append(
            _issue(
                "VOICE_HTML_REQUIREMENTS_SHA_STALE",
                "flow7.voice_delivery",
                "Project HTML is stale relative to current voice-requirements.md bytes",
                path=html_path,
            )
        )
    if _meta_sha(source, "voice-production-sha256") != production_sha:
        issues.append(
            _issue(
                "VOICE_HTML_PRODUCTION_SHA_STALE",
                "flow7.voice_delivery",
                "Project HTML is stale relative to current voice-production.md bytes",
                path=html_path,
            )
        )

    entries = {
        entry.voice_id: (section.owner_id, entry) for section in production.sections for entry in section.entries
    }
    if source.count('class="pa-row pa-row-voice"') != len(entries):
        issues.append(
            _issue(
                "VOICE_HTML_ROW_COUNT_MISMATCH",
                "flow7.voice_delivery",
                "Project HTML compact Voice row count differs from canonical production",
                path=html_path,
            )
        )

    section_blocks = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r'<section\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</section>',
            source,
            re.S | re.I,
        )
    }
    for voice_id, requirement in requirements.items():
        pair = entries.get(voice_id)
        if pair is None:
            continue
        owner_id, entry = pair
        page_id = production_page_id(render_data, owner_id)
        block = section_blocks.get(page_id, "")
        if not block:
            issues.append(
                _issue(
                    "VOICE_HTML_OWNER_PAGE_MISSING",
                    "flow7.voice_delivery",
                    f"Project HTML missing Production Assets page for Voice owner {owner_id}: {page_id}",
                    path=html_path,
                    field=voice_id,
                )
            )
            continue
        if f'data-moment-id="{html.escape(requirement.moment_id, quote=True)}"' not in block:
            issues.append(
                _issue(
                    "VOICE_HTML_MOMENT_MISSING",
                    "flow7.voice_delivery",
                    f"Project HTML missing canonical Moment ID {requirement.moment_id}",
                    path=html_path,
                    field=voice_id,
                )
            )
        prompt_id = f"voice-prompt-{voice_id.lower()}"
        matches = re.findall(
            rf'<pre class="voice-script-text" id="{re.escape(prompt_id)}">(.*?)</pre>',
            block,
            flags=re.S,
        )
        if len(matches) != 1:
            issues.append(
                _issue(
                    "VOICE_HTML_PROMPT_COUNT_INVALID",
                    "flow7.voice_delivery",
                    f"Project HTML must contain exact Voice prompt panel once in {page_id}",
                    path=html_path,
                    field=voice_id,
                )
            )
            continue
        if html.unescape(matches[0]) != entry.performance:
            issues.append(
                _issue(
                    "VOICE_HTML_PROMPT_STALE",
                    "flow7.voice_delivery",
                    "Project HTML performance text differs from canonical production",
                    path=html_path,
                    field=voice_id,
                )
            )
        identity = html.escape(f"{entry.speaker} — {entry.title}", quote=True)
        if identity not in block:
            issues.append(
                _issue(
                    "VOICE_HTML_IDENTITY_MISSING",
                    "flow7.voice_delivery",
                    "Project HTML missing compact Voice identity",
                    path=html_path,
                    field=voice_id,
                )
            )
    return issues


def _voice_delivery_context_issues(project: Path, data: dict[str, Any], revision: str) -> list[Issue]:
    """Verify complete Voice content at final delivery, not at upstream PRD Handoff."""

    base = f"output/v{revision}"
    context_ref = f"{base}/context.md"
    index_ref = f"{base}/index.json"
    try:
        context_file = resolve_project_path(project, context_ref, must_exist=True)
        index_file = resolve_project_path(project, index_ref, must_exist=True)
        context = context_file.read_text(encoding="utf-8")
        index = json.loads(index_file.read_text(encoding="utf-8"))
        lines = context.splitlines()
        if len(lines) < 4 or not lines[3].startswith("Status: "):
            raise ValueError("context.md is missing the generated status header")
        status = lines[3].removeprefix("Status: ").strip()
        if status not in {"unknown", "needs_revision", "development_ready", "handoff_ready"}:
            raise ValueError(f"context.md contains unsupported status {status!r}")
        title_data = data["document"]["title"]
        title = str(title_data.get("en") if isinstance(title_data, dict) else title_data or "").strip()
        if not title:
            raise ValueError("current PRD document title is missing")
        current_context = build_context(project, title, revision, status)
    except (OSError, UnicodeError, ValueError, ProjectPathError, KeyError, TypeError) as exc:
        return [
            _issue(
                "VOICE_CONTEXT_UNAVAILABLE",
                "flow7.voice_delivery",
                f"Current Voice context or index cannot be validated: {exc}",
                path=context_ref,
            )
        ]

    issues: list[Issue] = []
    if context != current_context:
        issues.append(
            _issue(
                "VOICE_CONTEXT_STALE",
                "flow7.voice_delivery",
                "Voice context.md differs from current requirements and accepted PRD sources",
                path=context_ref,
            )
        )
    if index != build_index(project, title, revision, status, context):
        issues.append(
            _issue(
                "VOICE_INDEX_STALE",
                "flow7.voice_delivery",
                "Voice index.json navigation does not match the delivered context",
                path=index_ref,
            )
        )
    return issues


def _delivery_selection_issues(production: VoiceProduction, state: VoiceState) -> list[Issue]:
    if state.status != "voice_delivery_ready":
        return []
    speakers = sorted({entry.speaker for section in production.sections for entry in section.entries})
    return [
        _issue(
            "VOICE_CAST_SELECTION_MISSING",
            "flow6.voice_production",
            f"voice_delivery_ready requires a Voice Cast selection/profile for speaker: {speaker}",
            path="work/voice-production.md",
            field=speaker,
        )
        for speaker in speakers
        if not selected_voice(production.cast, speaker)
    ]


def _voice_acceptance_issues(project: Path, production_path: Path, state: VoiceState) -> list[Issue]:
    if state.status != "voice_delivery_ready":
        return []
    path = project / "work" / "voice-acceptance.md"
    if not path.is_file():
        return [
            _issue(
                "VOICE_ACCEPTANCE_MISSING",
                "flow7.voice_acceptance",
                "voice_delivery_ready requires work/voice-acceptance.md",
                path="work/voice-acceptance.md",
            )
        ]
    text = path.read_text(encoding="utf-8")
    issues = required_value_issues(
        text,
        VOICE_ACCEPTANCE_REQUIRED,
        owner="flow7.voice_acceptance",
        path="work/voice-acceptance.md",
        code_prefix="VOICE_ACCEPTANCE",
    )
    issues.extend(
        sha_binding_issues(
            text,
            VOICE_ACCEPTED_SHA_LABEL,
            hashlib.sha256(production_path.read_bytes()).hexdigest(),
            owner="flow7.voice_acceptance",
            path="work/voice-acceptance.md",
            code="VOICE_ACCEPTANCE_PRODUCTION_SHA",
        )
    )
    return issues


def _result(
    state: VoiceState | None,
    issues: list[Issue],
    requirements: int,
    entries: int,
    sections: int,
    html_state: str,
    *,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "status": "pass" if not issues else "fail",
        "warnings": list(warnings or []),
        "errors": [str(issue) for issue in issues],
        "issues": [issue.as_dict() for issue in issues],
        "voice_status": state.status if state is not None else "invalid",
        "requirements": requirements,
        "script_entries": entries,
        "sections": sections,
        "project_html": html_state,
    }


def validate(project: Path) -> dict[str, Any]:
    project = project.resolve()
    state_path = project / "state" / "voice-state.yaml"
    try:
        voice_state = load_voice_state(state_path)
    except (OSError, StateError) as exc:
        return _result(
            None,
            [
                _issue(
                    "VOICE_STATE_INVALID",
                    "voice.lifecycle",
                    str(exc),
                    path="state/voice-state.yaml",
                )
            ],
            0,
            0,
            0,
            "not_provided",
        )

    if voice_state.status not in VALIDATABLE_STATUSES:
        return _result(
            voice_state,
            [
                _issue(
                    "VOICE_STATUS_NOT_VALIDATABLE",
                    "voice.lifecycle",
                    f"Voice validation cannot claim readiness for status {voice_state.status!r}; expected one of: "
                    + ", ".join(sorted(VALIDATABLE_STATUSES)),
                    path="state/voice-state.yaml",
                    field="status",
                )
            ],
            0,
            0,
            0,
            "not_provided",
        )

    issues: list[Issue] = []
    try:
        render_data, current_revision, current_render_sha = _load_render_data(project)
    except FileNotFoundError:
        return _result(
            voice_state,
            [
                _issue(
                    "VOICE_RENDER_DATA_MISSING",
                    "flow3.projection",
                    "Current render-data.json is missing",
                    path="work/render-data.json",
                )
            ],
            0,
            0,
            0,
            "not_provided",
        )
    except json.JSONDecodeError as exc:
        return _result(
            voice_state,
            [
                _issue(
                    "VOICE_RENDER_DATA_JSON_INVALID",
                    "flow3.projection",
                    str(exc),
                    path="work/render-data.json",
                    line=exc.lineno,
                )
            ],
            0,
            0,
            0,
            "not_provided",
        )
    except (OSError, ValueError) as exc:
        return _result(
            voice_state,
            [_issue("VOICE_RENDER_DATA_INVALID", "flow3.projection", str(exc), path="work/render-data.json")],
            0,
            0,
            0,
            "not_provided",
        )

    accepted_revision, upstream_issues, upstream_warnings = _accepted_revision(project, voice_state)
    issues.extend(upstream_issues)
    issues.extend(_state_identity_issues(voice_state, accepted_revision, current_revision, current_render_sha))

    if voice_state.status == "no_voice_required":
        production_path = project / "work" / "voice-production.md"
        if production_path.exists():
            issues.append(
                _issue(
                    "VOICE_NO_VOICE_PRODUCTION_PRESENT",
                    "voice.lifecycle",
                    "no_voice_required must not retain an active voice-production.md",
                    path="work/voice-production.md",
                )
            )
        return _result(voice_state, issues, 0, 0, 0, "not_applicable", warnings=upstream_warnings)

    try:
        requirements_path = resolve_project_path(
            project,
            voice_state.requirements,
            owner="voice-state.yaml.requirements",
            must_exist=True,
        )
        requirements = parse_requirements(requirements_path)
    except SourceParseError as exc:
        issues.append(exc.as_issue())
        return _result(voice_state, issues, 0, 0, 0, "not_required_yet", warnings=upstream_warnings)
    except (OSError, ProjectPathError, ValueError) as exc:
        issues.append(
            _issue(
                "VOICE_REQUIREMENTS_INVALID",
                "flow5.voice_requirement",
                str(exc),
                path="work/voice-requirements.md",
            )
        )
        return _result(voice_state, issues, 0, 0, 0, "not_required_yet", warnings=upstream_warnings)

    try:
        issues.extend(_requirements_revision_issues(requirements_path, accepted_revision))
    except OSError as exc:
        issues.append(
            _issue(
                "VOICE_REQUIREMENTS_UNREADABLE",
                "flow5.voice_requirement",
                str(exc),
                path="work/voice-requirements.md",
            )
        )
        return _result(voice_state, issues, len(requirements), 0, 0, "not_required_yet", warnings=upstream_warnings)
    issues.extend(_requirements_owner_issues(render_data, requirements))

    if voice_state.status in REQUIREMENTS_READY_STATUSES:
        return _result(voice_state, issues, len(requirements), 0, 0, "not_required_yet", warnings=upstream_warnings)

    try:
        production_path = resolve_project_path(
            project,
            voice_state.production,
            owner="voice-state.yaml.production",
            must_exist=True,
        )
        production = parse_production(production_path)
    except SourceParseError as exc:
        issues.append(exc.as_issue())
        return _result(voice_state, issues, len(requirements), 0, 0, "not_provided", warnings=upstream_warnings)
    except (OSError, ProjectPathError, ValueError) as exc:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_INVALID",
                "flow6.voice_production",
                str(exc),
                path="work/voice-production.md",
            )
        )
        return _result(voice_state, issues, len(requirements), 0, 0, "not_provided", warnings=upstream_warnings)

    try:
        issues.extend(_production_binding_issues(requirements_path, production_path, accepted_revision))
    except OSError as exc:
        issues.append(
            _issue(
                "VOICE_PRODUCTION_BINDING_UNREADABLE",
                "flow6.voice_production",
                str(exc),
                path="work/voice-production.md",
                field="Source Voice Requirements",
            )
        )
    issues.extend(_production_parity_issues(render_data, requirements, production))
    issues.extend(_delivery_selection_issues(production, voice_state))

    html_state = "not_provided"
    if voice_state.project_html:
        try:
            html_path = resolve_project_path(
                project,
                voice_state.project_html,
                owner="voice-state.yaml.project_html",
                must_exist=True,
            )
        except (OSError, ProjectPathError) as exc:
            issues.append(
                _issue(
                    "VOICE_HTML_PATH_INVALID",
                    "flow7.voice_delivery",
                    str(exc),
                    path="state/voice-state.yaml",
                    field="project_html",
                )
            )
            html_state = "missing"
        else:
            try:
                html_issues = _html_issues(
                    html_path,
                    render_data,
                    requirements_path,
                    production_path,
                    requirements,
                    production,
                )
            except (OSError, ValueError) as exc:
                html_issues = [
                    _issue(
                        "VOICE_HTML_VALIDATION_FAILED",
                        "flow7.voice_delivery",
                        str(exc),
                        path=voice_state.project_html,
                    )
                ]
            issues.extend(html_issues)
            html_state = "passed" if not html_issues else "failed"
    elif voice_state.status == "voice_delivery_ready":
        issues.append(
            _issue(
                "VOICE_HTML_REQUIRED",
                "flow7.voice_delivery",
                "voice_delivery_ready requires project_html in voice-state.yaml",
                path="state/voice-state.yaml",
                field="project_html",
            )
        )
        html_state = "missing"

    if voice_state.status == "voice_delivery_ready":
        issues.extend(_voice_delivery_context_issues(project, render_data, current_revision))

    try:
        issues.extend(_voice_acceptance_issues(project, production_path, voice_state))
    except OSError as exc:
        issues.append(
            _issue(
                "VOICE_ACCEPTANCE_UNREADABLE",
                "flow7.voice_acceptance",
                str(exc),
                path="work/voice-acceptance.md",
            )
        )

    return _result(
        voice_state,
        issues,
        len(requirements),
        sum(len(section.entries) for section in production.sections),
        len(production.sections),
        html_state,
        warnings=upstream_warnings,
    )
