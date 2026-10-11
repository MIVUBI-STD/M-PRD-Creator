#!/usr/bin/env python3
"""Static checks for durable PRD-Creator repository mechanics."""

from __future__ import annotations

import py_compile
import re
from pathlib import Path
from urllib.parse import unquote

if __package__:
    from .repository_knowledge import validate_repository_docs
else:
    from repository_knowledge import validate_repository_docs

ROOT = Path(__file__).resolve().parents[1]
KIT_ROOT = ROOT / "kits" / "prd-creator"

CANONICAL_SKILLS = {
    "development-brief",
    "project-document-production",
    "voice-production",
}

KIT_DIRS = {
    "intake",
    "document",
    "production-assets",
    "voice",
    "shared",
    "renderer",
    "validator",
    "template",
}
KIT_ROOT_MARKDOWN = {"README.md", "AGENTS.md", "SKILL.md"}

REQUIRED_FILES = {
    ".gitattributes",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/local-promotion-verify.yml",
    ".github/workflows/prd-verify.yml",
    ".github/workflows/release-verify.yml",
    ".github/workflows/repository-verify.yml",
    ".github/workflows/voice-verify.yml",
    ".gitignore",
    "docs/README.md",
    "planning/README.md",
    "planning/development.md",
    "planning/backlog.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTEXT.md",
    "CONTRIBUTING.md",
    "GITHUB_RULES.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "pyproject.toml",
    "requirements.lock.txt",
    "requirements-dev.lock.txt",
    "tools/prd.py",
    "tools/browser_verify.py",
    "tools/verify_repository.py",
    "tools/repository_knowledge.py",
    "tests/test_prd_repository_knowledge.py",
    "tests/test_prd_golden_reference.py",
    "tests/test_prd_browser_verify.py",
    "tests/test_voice_contracts.py",
    "kits/prd-creator/AGENTS.md",
    "kits/prd-creator/SKILL.md",
    "kits/prd-creator/intake/SOURCE-INTAKE.md",
    "kits/prd-creator/document/CONTENT-CONTRACT.md",
    "kits/prd-creator/document/DESIGN-CONTRACT.md",
    "kits/prd-creator/document/VALIDATION.md",
    "kits/prd-creator/production-assets/CONTRACT.md",
    "kits/prd-creator/renderer/CONTRACT.md",
    "kits/prd-creator/voice/EXTRACTION.md",
    "kits/prd-creator/voice/PERFORMANCE-WRITING.md",
    "kits/prd-creator/voice/VALIDATION.md",
    "kits/prd-creator/template/golden-reference.html",
}

REQUIRED_DIRS = {
    ".agents/skills",
    "docs/foundation",
    "docs/knowledge",
    "tests",
    "workspace",
}

RETIRED_PATHS = {
    ".github/workflows/production-verify.yml",
    "docs/knowledge/index.md",
    "docs/knowledge/minimal-nav.md",
    "docs/knowledge/workspace-map.md",
    "docs/knowledge/flow.md",
    "docs/knowledge/flows",
    "docs/knowledge/maintenance",
    "docs/knowledge/modules",
    "docs/knowledge/sources",
    "docs/knowledge/implementation-map.md",
    "docs/knowledge/decision-log.md",
    "docs/knowledge/decisions/change-decision-guide.md",
    "docs/knowledge/decisions/history-2026-08-29.md",
    "docs/knowledge/workflows",
    "docs/knowledge/reviews/review-graph.md",
    "docs/knowledge/reviews/review-template.md",
    "docs/knowledge/reviews/template.md",
    "docs/knowledge/operations/context-boot-baseline.md",
    "docs/knowledge/operations/task-board.md",
    "docs/foundation/validation-report.md",
    "workspace/saved",
    "docs/knowledge/next-action.md",
    "docs/knowledge/operations/backlog.md",
    "kits/project-document-generator",
    "kits/voice-production-kit",
    "kits/prd-creator/renderer/_engine.py",
    "kits/prd-creator/validator/_engine.py",
    "kits/prd-creator/renderer/production_assets_objective.py",
    "kits/prd-creator/renderer/voice_assets.py",
    "kits/prd-creator/voice/SOUNDMAKER.md",
    "kits/prd-creator/voice/LICENSE",
    "kits/prd-creator/voice/CHANGELOG.md",
    "kits/prd-creator/voice/HISTORICAL-CHANGELOG.md",
    "kits/prd-creator/template/runtime-template.html",
}

MARKDOWN_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "GITHUB_RULES.md",
    ROOT / "CONTEXT.md",
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / ".agents" / "skills",
    ROOT / "docs" / "foundation",
    ROOT / "docs" / "knowledge",
    ROOT / "planning",
    KIT_ROOT,
]

CURRENT_PATH_REFERENCE_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "GITHUB_RULES.md",
    ROOT / "CONTEXT.md",
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / ".agents" / "skills",
    ROOT / "docs" / "foundation",
    ROOT / "docs" / "knowledge" / "README.md",
    ROOT / "planning" / "development.md",
    ROOT / "docs" / "knowledge" / "ownership.md",
    ROOT / "docs" / "knowledge" / "source-authority.md",
    ROOT / "docs" / "knowledge" / "work-routing.md",
    ROOT / "docs" / "knowledge" / "skills",
    KIT_ROOT / "README.md",
    KIT_ROOT / "AGENTS.md",
    KIT_ROOT / "SKILL.md",
    KIT_ROOT / "intake",
    KIT_ROOT / "document",
    KIT_ROOT / "production-assets",
    KIT_ROOT / "voice",
    KIT_ROOT / "renderer" / "CONTRACT.md",
]

CURRENT_WORKFLOW_NAMING_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "CONTEXT.md",
    ROOT / "README.md",
    ROOT / ".agents" / "skills",
    ROOT / "docs" / "foundation",
    ROOT / "docs" / "knowledge" / "README.md",
    ROOT / "planning" / "development.md",
    ROOT / "docs" / "knowledge" / "ownership.md",
    ROOT / "docs" / "knowledge" / "source-authority.md",
    ROOT / "docs" / "knowledge" / "work-routing.md",
    ROOT / "docs" / "knowledge" / "skills",
    ROOT / "docs" / "knowledge" / "operations" / "boot-baseline.md",
    KIT_ROOT / "README.md",
    KIT_ROOT / "AGENTS.md",
    KIT_ROOT / "SKILL.md",
    KIT_ROOT / "intake" / "SOURCE-INTAKE.md",
    KIT_ROOT / "document" / "CONTENT-CONTRACT.md",
    KIT_ROOT / "document" / "VALIDATION.md",
    KIT_ROOT / "production-assets",
    KIT_ROOT / "renderer" / "CONTRACT.md",
    KIT_ROOT / "voice" / "EXTRACTION.md",
    KIT_ROOT / "voice" / "PERFORMANCE-WRITING.md",
    KIT_ROOT / "voice" / "VALIDATION.md",
]

PATH_REFERENCE_PREFIXES = (
    ".agents/",
    ".github/",
    "docs/",
    "planning/",
    "kits/",
    "tests/",
    "tools/",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_PATH_RE = re.compile(r"`((?:\.agents|\.github|docs|kits|tests|tools)/[^`\s]+)`")
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s=]+)$")
ACTION_USE_RE = re.compile(r"(?m)^\s*uses:\s*([^@\s]+)@([^\s#]+)")
IMMUTABLE_ACTION_REF_RE = re.compile(r"^[0-9a-f]{40}$")
NAME_RE = re.compile(r"(?m)^name:\s*([^\s]+)\s*$")
VERSION_RE = re.compile(r"(?m)^version:\s*([^\s]+)\s*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
LEGACY_WORKFLOW_NAME_RE = re.compile(
    r"\bFlow\s+[1-7](?:\s*[\u2013\u2014-]\s*[1-7])?\b|\bnon-Voice\s+`?04\b|\b04\s+Production\s+Assets\b",
    flags=re.IGNORECASE,
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def iter_markdown_under(items: list[Path]) -> list[Path]:
    files: list[Path] = []
    for item in items:
        if item.is_file() and item.suffix.lower() == ".md":
            files.append(item)
        elif item.is_dir():
            files.extend(item.rglob("*.md"))
    return sorted(set(files))


def iter_markdown_files() -> list[Path]:
    return iter_markdown_under(MARKDOWN_ROOTS)


def check_required_surfaces(errors: list[str]) -> None:
    for rel in sorted(REQUIRED_FILES):
        if not (ROOT / rel).is_file():
            fail(errors, f"missing required repository surface: {rel}")
    for rel in sorted(REQUIRED_DIRS):
        if not (ROOT / rel).is_dir():
            fail(errors, f"missing required repository directory: {rel}")


def check_kit_shape(errors: list[str]) -> None:
    kits_root = ROOT / "kits"
    if not kits_root.is_dir():
        fail(errors, "missing kits/ root")
        return

    active_kits = {path.name for path in kits_root.iterdir() if path.is_dir() and not path.name.startswith(".")}
    if active_kits != {"prd-creator"}:
        fail(errors, f"active production kit drift: expected ['prd-creator'], got {sorted(active_kits)}")
        return

    actual_dirs = {path.name for path in KIT_ROOT.iterdir() if path.is_dir() and not path.name.startswith(".")}
    if actual_dirs != KIT_DIRS:
        fail(errors, f"prd-creator domain drift: expected {sorted(KIT_DIRS)}, got {sorted(actual_dirs)}")

    actual_root_md = {path.name for path in KIT_ROOT.glob("*.md")}
    if actual_root_md != KIT_ROOT_MARKDOWN:
        fail(
            errors,
            f"prd-creator root Markdown drift: expected {sorted(KIT_ROOT_MARKDOWN)}, got {sorted(actual_root_md)}",
        )


def parse_skill_metadata(path: Path, errors: list[str]) -> tuple[str | None, str | None]:
    if not path.is_file():
        return None, None
    text = path.read_text(encoding="utf-8")
    name_match = NAME_RE.search(text)
    version_match = VERSION_RE.search(text)
    return (name_match.group(1) if name_match else None, version_match.group(1) if version_match else None)


def check_skill_metadata(errors: list[str]) -> None:
    skill_root = ROOT / ".agents" / "skills"
    actual = {path.name for path in skill_root.iterdir() if path.is_dir() and not path.name.startswith(".")}
    if actual != CANONICAL_SKILLS:
        fail(errors, f"canonical skill set drift: expected {sorted(CANONICAL_SKILLS)}, got {sorted(actual)}")

    for skill in sorted(CANONICAL_SKILLS):
        path = skill_root / skill / "SKILL.md"
        if not path.is_file():
            fail(errors, f"missing SKILL.md for canonical skill: {skill}")
            continue
        name, _ = parse_skill_metadata(path, errors)
        if name != skill:
            fail(errors, f"skill metadata mismatch in {path.relative_to(ROOT)}: expected name {skill!r}, got {name!r}")

    nested = list((ROOT / "kits").glob("**/.agents/skills")) if (ROOT / "kits").exists() else []
    for path in nested:
        fail(errors, f"unexpected nested repository skill root: {path.relative_to(ROOT)}")

    package_skill = KIT_ROOT / "SKILL.md"
    name, version = parse_skill_metadata(package_skill, errors)
    if name != "prd-creator":
        fail(errors, f"package SKILL name must be 'prd-creator', got {name!r}")
    if not version or not SEMVER_RE.fullmatch(version):
        fail(errors, f"package SKILL version must be semantic version metadata, got {version!r}")


def check_retired_paths(errors: list[str]) -> None:
    for rel in sorted(RETIRED_PATHS):
        if (ROOT / rel).exists():
            fail(errors, f"retired repository path must not return: {rel}")

    operations = ROOT / "docs" / "knowledge" / "operations"
    if operations.is_dir():
        for path in sorted(operations.glob("unified-prd-creator-kit-*.md")):
            fail(errors, f"completed migration artifact must not remain active: {path.relative_to(ROOT)}")


def requirement_pins(path: Path, errors: list[str]) -> dict[str, str]:
    pins: dict[str, str] = {}
    if not path.is_file():
        return pins
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN_RE.fullmatch(line)
        if not match:
            fail(errors, f"{path.relative_to(ROOT)}:{lineno} must use exact 'name==version' pinning")
            continue
        name = match.group(1).replace("_", "-").lower()
        if name in pins:
            fail(errors, f"duplicate dependency pin in {path.relative_to(ROOT)}: {name}")
        pins[name] = match.group(2)
    return pins


def check_dependency_locks(errors: list[str]) -> None:
    requirement_pins(ROOT / "requirements.lock.txt", errors)
    requirement_pins(ROOT / "requirements-dev.lock.txt", errors)
    if (KIT_ROOT / "requirements.txt").exists():
        fail(errors, "unexpected kit requirements.txt; root lockfiles own Python dependency pins")


def check_workflow_action_pins(errors: list[str]) -> None:
    workflows = ROOT / ".github" / "workflows"
    for path in sorted(workflows.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for target, ref in ACTION_USE_RE.findall(text):
            if target.startswith("./") or target.startswith("docker://"):
                continue
            if not IMMUTABLE_ACTION_REF_RE.fullmatch(ref):
                fail(
                    errors,
                    f"workflow action must use immutable 40-character commit SHA in {path.relative_to(ROOT)}: "
                    f"{target}@{ref}",
                )


def normalize_link_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().strip("<>")
    if not target:
        return None
    lower = target.lower()
    if (
        target.startswith("#")
        or "://" in target
        or lower.startswith(("mailto:", "tel:", "data:", "skills:", "sandbox:"))
    ):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0]).strip()
    if not target:
        return None
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return source.parent / target


def check_markdown_links(errors: list[str]) -> None:
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = normalize_link_target(path, raw)
            if target is None:
                continue
            try:
                exists = target.resolve().exists()
            except OSError:
                exists = target.exists()
            if not exists:
                fail(errors, f"broken relative link in {path.relative_to(ROOT)}: {raw}")


def normalize_code_path(raw: str) -> str:
    value = raw.rstrip(".,;:)")
    if "<" in value or ">" in value or "*" in value or "{" in value or "}" in value:
        return ""
    return value


def check_explicit_repository_paths(errors: list[str]) -> None:
    for source in iter_markdown_under(CURRENT_PATH_REFERENCE_ROOTS):
        text = source.read_text(encoding="utf-8")
        for raw in CODE_PATH_RE.findall(text):
            rel = normalize_code_path(raw)
            if not rel or not rel.startswith(PATH_REFERENCE_PREFIXES):
                continue
            if (ROOT / rel).exists():
                continue
            fail(errors, f"stale repository path reference in {source.relative_to(ROOT)}: {rel}")


def check_canonical_workflow_naming(errors: list[str]) -> None:
    """Keep current policy on one semantic workflow vocabulary.

    Historical decisions, reviews, and changelog records are intentionally outside
    this check because they may truthfully quote superseded terminology.
    """

    for source in iter_markdown_under(CURRENT_WORKFLOW_NAMING_ROOTS):
        text = source.read_text(encoding="utf-8")
        match = LEGACY_WORKFLOW_NAME_RE.search(text)
        if match:
            fail(
                errors,
                f"legacy workflow name in current policy {source.relative_to(ROOT)}: {match.group(0)!r}",
            )


def check_python_syntax(errors: list[str]) -> None:
    for root in (ROOT / "kits", ROOT / "tools", ROOT / "tests"):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                fail(errors, f"python syntax error in {path.relative_to(ROOT)}: {exc.msg}")


def check_document_routing(errors: list[str]) -> None:
    """One repository-native validator consumes the in-memory document router."""
    for issue in validate_repository_docs(ROOT):
        fail(errors, f"document routing: {issue}")


def main() -> int:
    errors: list[str] = []

    check_required_surfaces(errors)
    check_kit_shape(errors)
    check_skill_metadata(errors)
    check_retired_paths(errors)
    check_dependency_locks(errors)
    check_workflow_action_pins(errors)
    check_markdown_links(errors)
    check_document_routing(errors)
    check_explicit_repository_paths(errors)
    check_canonical_workflow_naming(errors)
    check_python_syntax(errors)

    if errors:
        print("REPOSITORY VERIFY FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REPOSITORY VERIFY PASSED")
    print(f"- canonical skills: {', '.join(sorted(CANONICAL_SKILLS))}")
    print("- active production kit and entrypoints: present")
    print("- package skill metadata: valid")
    print("- retired repository paths: absent")
    print("- external GitHub Actions: immutable commit-SHA pinned")
    print(f"- relative Markdown links checked: {len(iter_markdown_files())} files")
    print("- current explicit repository path references: valid")
    print("- canonical workflow naming: valid")
    print("- runtime/dev dependency pins: valid")
    print("- Python kits/tools/tests: syntax valid")
    print("- historical prose is not rewritten as a machine contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
