#!/usr/bin/env python3
"""Thin mechanical operator CLI for PRD-Creator project workflows."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KIT_ROOT = ROOT / "kits" / "prd-creator"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(KIT_ROOT) not in sys.path:
    sys.path.insert(0, str(KIT_ROOT))

from renderer.delivery import build_delivery  # noqa: E402
from shared.sfx import preflight as sfx_preflight  # noqa: E402
from shared.state import StateError  # noqa: E402
from validator import api as prd_api  # noqa: E402
from validator import validate_handoff as handoff_validator  # noqa: E402
from validator import voice_validation  # noqa: E402
from validator.traceability import assess as assess_traceability  # noqa: E402
from validator.revision import plan_revision  # noqa: E402

from tools.browser_verify import BrowserVerifyError  # noqa: E402
from tools.browser_verify import verify as verify_browser  # noqa: E402

VOICE_PRE_UPSTREAM_CODES = {
    "VOICE_STATE_INVALID",
    "VOICE_STATUS_NOT_VALIDATABLE",
    "VOICE_RENDER_DATA_MISSING",
    "VOICE_RENDER_DATA_JSON_INVALID",
    "VOICE_RENDER_DATA_INVALID",
}

PROJECT_PRD_PATHS = {
    "state/source-inventory.yaml",
    "state/requirement-register.yaml",
    "state/intake-state.yaml",
    "work/content.md",
    "work/render-data.json",
    "work/asset-requirements.md",
}
PROJECT_HANDOFF_PATHS = {
    "work/acceptance.md",
    "state/handoff-state.yaml",
}
PROJECT_VOICE_PATHS = {
    "work/voice-requirements.md",
    "work/voice-production.md",
    "work/voice-acceptance.md",
    "state/voice-state.yaml",
}
VISUAL_REPO_PREFIXES = (
    "kits/prd-creator/template/",
    "kits/prd-creator/renderer/static/",
)
VISUAL_REPO_PATHS = {
    "kits/prd-creator/renderer/core.py",
    "kits/prd-creator/renderer/pages.py",
    "kits/prd-creator/renderer/prd_render_engine.py",
    "kits/prd-creator/renderer/template_adapter.py",
    "kits/prd-creator/renderer/render.py",
    "kits/prd-creator/renderer/delivery.py",
    "kits/prd-creator/renderer/production_assets.py",
    "kits/prd-creator/renderer/production_assets_compositor.py",
    "tools/browser_verify.py",
    "tests/test_prd_browser_verify.py",
}
VOICE_REPO_PREFIXES = ("kits/prd-creator/voice/",)
VOICE_REPO_PATHS = {
    "kits/prd-creator/renderer/production_assets.py",
    "kits/prd-creator/renderer/production_assets_compositor.py",
    "kits/prd-creator/validator/voice_validation.py",
    "kits/prd-creator/validator/validate_voice.py",
    "tests/test_voice_contracts.py",
    "tests/test_prd_voice_assets.py",
}
PRD_REPO_PREFIXES = (
    "kits/prd-creator/intake/",
    "kits/prd-creator/document/",
    "kits/prd-creator/production-assets/",
    "kits/prd-creator/renderer/",
    "kits/prd-creator/shared/",
    "kits/prd-creator/validator/",
    "kits/prd-creator/template/",
)
FULL_REGRESSION_PATHS = {
    ".github/workflows/local-promotion-verify.yml",
    ".github/workflows/release-verify.yml",
}


def _first_issue(result: dict[str, Any]) -> dict[str, Any] | None:
    issues = result.get("issues")
    if isinstance(issues, list):
        for issue in issues:
            if isinstance(issue, dict):
                return {
                    key: issue[key]
                    for key in ("code", "owner", "message", "path", "field", "line", "severity")
                    if key in issue and issue[key] not in (None, "")
                }
    errors = result.get("errors")
    if isinstance(errors, list) and errors:
        return {
            "code": "UNSTRUCTURED_VALIDATION_ERROR",
            "owner": "unknown",
            "message": str(errors[0]),
        }
    return None


def _issue_codes(result: dict[str, Any]) -> set[str]:
    issues = result.get("issues")
    if not isinstance(issues, list):
        return set()
    return {str(issue.get("code")) for issue in issues if isinstance(issue, dict) and issue.get("code")}


def _domain(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": str(result.get("status") or "fail"),
        "first_issue": _first_issue(result),
    }


def _passed() -> dict[str, Any]:
    return {"status": "pass", "first_issue": None}


def _not_present() -> dict[str, Any]:
    return {"status": "not_present", "first_issue": None}


def _handoff_proves_prd(result: dict[str, Any]) -> bool:
    checks = result.get("checks")
    if not isinstance(checks, list):
        return False
    return any(
        isinstance(check, dict)
        and check.get("check") == "current_prd_complete_validation"
        and check.get("status") == "pass"
        for check in checks
    )


def _prd_from_handoff(project: Path, handoff_result: dict[str, Any]) -> dict[str, Any]:
    if _handoff_proves_prd(handoff_result):
        return _passed()
    return _domain(prd_api.validate(project))


def _voice_proves_upstream(result: dict[str, Any]) -> bool:
    codes = _issue_codes(result)
    return not (codes & VOICE_PRE_UPSTREAM_CODES) and "VOICE_UPSTREAM_HANDOFF_INVALID" not in codes


def status_payload(project: Path) -> dict[str, Any]:
    project = project.resolve()
    handoff_state = project / "state" / "handoff-state.yaml"
    voice_state = project / "state" / "voice-state.yaml"

    # Start from the deepest present stage. A healthy downstream validator already
    # proves its upstream chain, so status does not replay the same proof.
    if voice_state.is_file():
        voice_result = voice_validation.validate(project)
        voice = _domain(voice_result)
        if handoff_state.is_file() and _voice_proves_upstream(voice_result):
            prd = _passed()
            handoff = _passed()
        elif handoff_state.is_file():
            handoff_result = handoff_validator.validate(project)
            handoff = _domain(handoff_result)
            prd = _prd_from_handoff(project, handoff_result)
        else:
            prd = _domain(prd_api.validate(project))
            handoff = _not_present()
    elif handoff_state.is_file():
        handoff_result = handoff_validator.validate(project)
        handoff = _domain(handoff_result)
        prd = _prd_from_handoff(project, handoff_result)
        voice = _not_present()
    else:
        prd = _domain(prd_api.validate(project))
        handoff = _not_present()
        voice = _not_present()

    stages = (("prd", prd), ("handoff", handoff), ("voice", voice))
    first_issue = next(
        (stage["first_issue"] for _, stage in stages if isinstance(stage.get("first_issue"), dict)),
        None,
    )
    failed = next((name for name, stage in stages if stage["status"] not in {"pass", "not_present"}), None)
    if failed is not None and first_issue is None:
        first_issue = {
            "code": "VALIDATION_FAILURE_WITHOUT_ISSUE",
            "owner": f"{failed}.validation",
            "message": f"{failed.upper()} validator reported a non-pass status without an actionable issue.",
        }
    blocked = failed is not None or first_issue is not None

    if first_issue is not None:
        owner = str(first_issue.get("owner") or "unknown")
        code = str(first_issue.get("code") or "unknown")
        location = str(first_issue.get("path") or "").strip()
        field = str(first_issue.get("field") or "").strip()
        if field:
            location = f"{location}:{field}" if location else field
        target = f" at {location}" if location else ""
        next_action = f"Fix the first wrong owner {owner} ({code}){target}, then rerun status."
    elif handoff["status"] == "not_present":
        next_action = "PRD mechanical validation passes. Handoff state is not present; no handoff readiness is claimed."
    elif voice["status"] == "not_present":
        next_action = "PRD handoff validation passes. Voice state is not present; no Voice readiness is claimed."
    else:
        next_action = "All present mechanical validation stages pass."

    return {
        "project": project.name,
        "mechanical_status": "blocked" if blocked else "clear",
        "proof_scope": "mechanical_only",
        "prd": prd,
        "handoff": handoff,
        "voice": voice,
        "first_issue": first_issue,
        "next_action": next_action,
    }


def _normalize_changed_path(raw: str) -> str:
    value = raw.strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value.strip("/")


def _git_changed_paths(base: str | None) -> list[str]:
    command = ["git", "diff", "--name-only"]
    if base:
        command.append(base)
    command.append("--")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "git diff failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def impact_payload(changed_paths: list[str], *, project: Path | None = None) -> dict[str, Any]:
    if project is not None:
        project = project.resolve()
        if not project.is_dir():
            raise ValueError(f"impact --project requires an existing directory: {project}")

    normalized_paths: set[str] = set()
    for raw in changed_paths:
        path = _normalize_changed_path(raw)
        if not path:
            continue
        if project is not None:
            candidate = Path(raw.strip().replace("\\", "/"))
            if not candidate.is_absolute():
                candidate = ROOT / candidate
            try:
                path = candidate.resolve().relative_to(project).as_posix()
            except ValueError:
                pass
        normalized_paths.add(path)
    changed = sorted(normalized_paths)
    checks: set[str] = set()
    owners: set[str] = set()
    derived_edits: list[str] = []
    browser_required = False
    full_regression_required = False

    for path in changed:
        if path.startswith("output/"):
            derived_edits.append(path)
            owners.add("derived_output")
            continue

        if path in PROJECT_PRD_PATHS:
            checks.add("prd")
            owners.add("project_prd")
            continue
        if path in PROJECT_HANDOFF_PATHS:
            checks.add("handoff")
            owners.add("project_handoff")
            continue
        if path in PROJECT_VOICE_PATHS:
            checks.add("voice")
            owners.add("project_voice")
            if path in {"work/voice-requirements.md", "work/voice-production.md"}:
                checks.add("prd")
            continue

        is_repo_path = (
            path.startswith("kits/")
            or path.startswith("tests/")
            or path.startswith("tools/")
            or path.startswith(".github/")
            or path.startswith("docs/")
            or path.startswith("planning/")
            or path.startswith(".agents/")
            or path
            in {
                "AGENTS.md",
                "GITHUB_RULES.md",
                "CONTEXT.md",
                "README.md",
                "CONTRIBUTING.md",
                "SECURITY.md",
                "CHANGELOG.md",
                "LICENSE",
                ".gitattributes",
                ".gitignore",
                "pyproject.toml",
                "requirements.lock.txt",
                "requirements-dev.lock.txt",
                "workspace/README.md",
                "workspace/active/README.md",
                "workspace/archive/README.md",
            }
        )
        if is_repo_path:
            checks.add("repository")
            owners.add("repository")

        if path in {"pyproject.toml", "requirements.lock.txt", "requirements-dev.lock.txt"}:
            checks.update({"prd", "voice"})
            owners.add("shared_toolchain")

        if (
            path.startswith(PRD_REPO_PREFIXES)
            or path.startswith("tests/test_prd_")
            or path
            in {
                "tests/prd_fixture.py",
                "tools/prd.py",
            }
        ):
            checks.add("prd")
            owners.add("prd_system")

        if path.startswith(VOICE_REPO_PREFIXES) or path in VOICE_REPO_PATHS:
            checks.add("voice")
            owners.add("voice_system")

        if path.startswith("kits/prd-creator/shared/"):
            checks.add("voice")

        if path.startswith(VISUAL_REPO_PREFIXES) or path in VISUAL_REPO_PATHS:
            browser_required = True
            owners.add("visual_runtime")

        if path in FULL_REGRESSION_PATHS:
            full_regression_required = True

        if not is_repo_path:
            owners.add("unknown")
            checks.add("repository")

    # Existing project state determines which optional downstream gates exist.
    # This is affected-check planning, not a claim that a SHA is already stale.
    changed_set = set(changed)
    project_prd_changed = bool(changed_set & PROJECT_PRD_PATHS)
    project_handoff_changed = bool(changed_set & PROJECT_HANDOFF_PATHS)
    project_voice_changed = bool(changed_set & PROJECT_VOICE_PATHS)
    potential_downstream: list[str] = []
    stale_if_present: list[str] = []
    not_proven: list[str] = []

    if project_prd_changed:
        potential_downstream = ["PRD Production", "PRD Handoff", "Voice Requirements", "Voice Delivery"]
        stale_if_present = [
            "accepted Project Requirements / PRD SHA bindings",
            "PRD Handoff acceptance and versioned delivery",
            "downstream Voice source and production bindings",
        ]
        not_proven = ["semantic acceptance", "browser visual quality"]
    elif project_handoff_changed:
        potential_downstream = ["PRD Handoff", "Voice Requirements", "Voice Delivery"]
        stale_if_present = ["accepted PRD Handoff and downstream Voice binding"]
        not_proven = ["semantic acceptance"]

    if project_voice_changed:
        for scope in ("Voice Requirements", "Voice Production", "Voice Delivery"):
            if scope not in potential_downstream:
                potential_downstream.append(scope)
        if not stale_if_present:
            stale_if_present = ["Voice production and delivery SHA bindings"]
        not_proven.append("audio/actor/pronunciation quality")

    if project is not None and (project_prd_changed or project_handoff_changed):
        handoff_present = any((project / name).is_file() for name in ("work/acceptance.md", "state/handoff-state.yaml"))
        voice_present = any(
            (project / name).is_file()
            for name in (
                "state/voice-state.yaml",
                "work/voice-requirements.md",
                "work/voice-production.md",
                "work/voice-acceptance.md",
            )
        )
        if project_prd_changed and (handoff_present or voice_present):
            checks.add("handoff")
        if voice_present:
            checks.add("voice")

    if browser_required:
        checks.add("browser")
    if full_regression_required:
        checks.add("full_regression")

    order = ["repository", "prd", "handoff", "voice", "browser", "full_regression"]
    recommended_checks = [item for item in order if item in checks]

    if derived_edits:
        next_action = (
            "Do not keep direct derived-output edits. Repair the canonical owner and regenerate, "
            "then run only the checks listed for the canonical change."
        )
    elif not changed:
        next_action = "No changed paths were provided or detected."
    elif recommended_checks:
        next_action = "Run only the recommended checks in order; promotion still requires the full Local gate."
    else:
        next_action = "No production validation domain is affected."

    return {
        "changed": changed,
        "owners": sorted(owners),
        "recommended_checks": recommended_checks,
        "browser_required": browser_required,
        "full_regression_required": full_regression_required,
        "derived_edits": derived_edits,
        "potential_downstream": potential_downstream,
        "stale_if_present": stale_if_present,
        "not_proven": sorted(set(not_proven)),
        "project_scope": str(project) if project is not None else None,
        "next_action": next_action,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _print_status(payload: dict[str, Any]) -> None:
    print(f"Project: {payload['project']}")
    print(f"Mechanical: {str(payload['mechanical_status']).upper()}")
    print("Proof: mechanical only (semantic, visual, and audio quality are separate).")
    for label in ("prd", "handoff", "voice"):
        stage = payload[label]
        print(f"{label.upper()}: {str(stage['status']).upper()}")
    issue = payload.get("first_issue")
    if isinstance(issue, dict):
        code = issue.get("code", "unknown")
        owner = issue.get("owner", "unknown")
        message = issue.get("message", "")
        print(f"First issue: {code} [{owner}] {message}")
        location = str(issue.get("path") or "").strip()
        field = str(issue.get("field") or "").strip()
        if location or field:
            suffix = f":{field}" if field else ""
            print(f"Location: {location}{suffix}")
    print(f"Next: {payload['next_action']}")


def _print_impact(payload: dict[str, Any]) -> None:
    changed = payload["changed"]
    print(f"Changed: {len(changed)}")
    for path in changed:
        print(f"- {path}")
    checks = payload["recommended_checks"]
    print("Checks: " + (", ".join(checks) if checks else "none"))
    if payload["derived_edits"]:
        print("Derived edits: regenerate from canonical source")
    print(f"Next: {payload['next_action']}")


def _relative_outputs(project: Path, outputs: dict[str, Path]) -> dict[str, str]:
    project = project.resolve()
    rendered: dict[str, str] = {}
    for label, path in outputs.items():
        resolved = path.resolve()
        try:
            rendered[label] = resolved.relative_to(project).as_posix()
        except ValueError:
            rendered[label] = resolved.as_posix()
    return rendered


def _result_exit(result: dict[str, Any]) -> int:
    _print_json(result)
    return 0 if result.get("status") == "pass" else 1


def _current_prd_html(project: Path) -> Path:
    data_path = project / "work" / "render-data.json"
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("render-data root must be an object")
    document = raw.get("document")
    if not isinstance(document, dict):
        raise ValueError("render-data.document must be an object")
    version = str(document.get("version") or "").strip()
    if not version:
        raise ValueError("render-data.document.version is required")
    return project / "output" / f"v{version}" / "prd.html"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    impact_parser = subparsers.add_parser(
        "impact",
        help="route changed paths to the smallest sufficient validation domains",
    )
    impact_parser.add_argument("changed", nargs="*", help="changed project/repository paths")
    impact_parser.add_argument("--git-base", help="read changed paths from git diff against this ref")
    impact_parser.add_argument(
        "--project",
        type=Path,
        help="optional exact project package for checking present downstream handoff/Voice artifacts",
    )
    impact_parser.add_argument("--json", action="store_true", dest="as_json")

    trace_parser = subparsers.add_parser(
        "trace", help="locate current REQ-ID evidence and prepare cross-role semantic review"
    )
    trace_parser.add_argument("project", type=Path)

    revision_parser = subparsers.add_parser(
        "revision",
        help="compare an explicit prior requirement register with current project state (read-only)",
    )
    revision_parser.add_argument("project", type=Path)
    revision_parser.add_argument(
        "--before",
        type=Path,
        required=True,
        help="prior saved requirement-register.yaml snapshot, distinct from current register",
    )

    status_parser = subparsers.add_parser("status", help="show compact mechanical project status and first wrong owner")
    status_parser.add_argument("project", type=Path)
    status_parser.add_argument("--json", action="store_true", dest="as_json")

    browser_parser = subparsers.add_parser(
        "browser",
        help="verify the current validated PRD in real Chrome and emit visual/runtime evidence",
    )
    browser_parser.add_argument("project", type=Path)
    browser_parser.add_argument("--screenshot", type=Path, help="optional PNG evidence path")

    for command, help_text in (
        ("build", "build the canonical versioned delivery bundle"),
        ("validate", "run canonical PRD validation"),
        ("handoff", "run canonical PRD handoff validation"),
        ("voice", "run canonical Voice validation"),
    ):
        command_parser = subparsers.add_parser(command, help=help_text)
        command_parser.add_argument("project", type=Path)

    sfx_parser = subparsers.add_parser(
        "sfx-check", help="offline SFX request and budget snapshot check; never generates"
    )
    sfx_parser.add_argument("request", type=Path, help="native ElevenLabs SFX-v2 JSON body, not a project manifest")
    sfx_parser.add_argument(
        "--request-limit", type=int, required=True, help="finite API-attempt cap from execution notes"
    )
    sfx_parser.add_argument(
        "--requests-used", type=int, required=True, help="all dispatched attempts, including unresolved"
    )
    sfx_parser.add_argument("--unresolved-requests", type=int, required=True, help="unresolved subset of requests-used")
    sfx_parser.add_argument("--max-duration-seconds", type=float, required=True, help="per-attempt duration cap")

    args = parser.parse_args()

    try:
        if args.command == "sfx-check":
            return _result_exit(
                sfx_preflight(
                    args.request,
                    request_limit=args.request_limit,
                    requests_used=args.requests_used,
                    unresolved_requests=args.unresolved_requests,
                    max_duration_seconds=args.max_duration_seconds,
                )
            )
        if args.command == "impact":
            changed = list(args.changed)
            if args.git_base is not None:
                changed.extend(_git_changed_paths(args.git_base))
            elif not changed:
                changed.extend(_git_changed_paths(None))
            payload = impact_payload(changed, project=args.project)
            if args.as_json:
                _print_json(payload)
            else:
                _print_impact(payload)
            return 0

        project = args.project.resolve()
        if args.command == "trace":
            traced = assess_traceability(project)
            _print_json(traced)
            return 0 if traced["status"] == "mapped_unverified" else 1
        if args.command == "revision":
            planned = plan_revision(project, args.before)
            planned["recommended_checks"] = (
                impact_payload(["state/requirement-register.yaml"], project=project)["recommended_checks"]
                if planned["bytes_changed"]
                else []
            )
            _print_json(planned)
            return 0
        if args.command == "status":
            payload = status_payload(project)
            if args.as_json:
                _print_json(payload)
            else:
                _print_status(payload)
            return 1 if payload["mechanical_status"] == "blocked" else 0
        if args.command == "build":
            outputs = build_delivery(project)
            _print_json(
                {
                    "status": "pass",
                    "operation": "build",
                    "proof_scope": "generated_artifacts_only",
                    "handoff_verified": False,
                    "outputs": _relative_outputs(project, outputs),
                }
            )
            return 0
        if args.command == "validate":
            return _result_exit(prd_api.validate(project))
        if args.command == "browser":
            current_prd = prd_api.validate(project)
            if current_prd.get("status") != "pass":
                return _result_exit(current_prd)
            screenshot = args.screenshot.resolve() if args.screenshot is not None else None
            return _result_exit(verify_browser(_current_prd_html(project), screenshot))
        if args.command == "handoff":
            return _result_exit(handoff_validator.validate(project))
        if args.command == "voice":
            return _result_exit(voice_validation.validate(project))
    except (BrowserVerifyError, OSError, StateError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRD OPERATOR FAILED: {exc}", file=sys.stderr)
        return 2

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
