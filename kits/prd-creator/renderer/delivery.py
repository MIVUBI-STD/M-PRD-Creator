#!/usr/bin/env python3
"""Build the compact versioned PRD delivery bundle for humans and coding AI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
KIT_ROOT = HERE.parent
if __package__ in (None, ""):
    if str(KIT_ROOT) not in sys.path:
        sys.path.insert(0, str(KIT_ROOT))
    from shared.state import StateError, load_mapping, optional_scalar

    from renderer import render as html_renderer_module
else:
    from shared.state import StateError, load_mapping, optional_scalar

    from . import render as html_renderer_module

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

GUIDANCE = (
    "Use this document as the current accepted product context for development.",
    "A newer explicitly approved change overrides only the affected context; preserve unrelated accepted meaning.",
    "Existing, legacy, template, or unused implementation is evidence, not automatic product authority.",
    "Use `index.json` first and read only the relevant `context.md` line ranges plus any directly related scope.",
    "Prefer the smallest complete implementation and reuse an existing owner only when it has the same responsibility.",
    "Do not add abstraction, fallback, migration, or compatibility behavior without a current need.",
    "If implementation requires a new product decision, surface it instead of inventing it.",
)


def _semver(value: object) -> str:
    raw = str(value or "").strip()
    match = SEMVER_RE.fullmatch(raw)
    if not match:
        raise ValueError(f"document.version must use semantic X.Y.Z form for delivery, got {raw!r}")
    return ".".join(match.groups())


def _slug(value: str) -> str:
    clean = re.sub(r"[`*_~]+", "", value).strip().lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return clean or "section"


def _handoff_status(project: Path) -> str:
    path = project / "state" / "handoff-state.yaml"
    if not path.is_file():
        return ""
    state = load_mapping(path, owner="handoff-state.yaml")
    return optional_scalar(state, "status")


def _strip_first_h1(markdown: str) -> str:
    lines = markdown.strip().splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            del lines[index]
            break
    return "\n".join(lines).strip()


def _demote_headings(markdown: str, by: int) -> str:
    if by <= 0:
        return markdown.strip()
    rendered: list[str] = []
    for line in markdown.strip().splitlines():
        match = HEADING_RE.match(line)
        if not match:
            rendered.append(line)
            continue
        level = min(6, len(match.group(1)) + by)
        rendered.append(f"{'#' * level} {match.group(2)}")
    return "\n".join(rendered).strip()


def _section_source(path: Path, demote_by: int) -> str:
    return _demote_headings(_strip_first_h1(path.read_text(encoding="utf-8")), demote_by)


def build_context(project: Path, title: str, version: str, status: str, *, include_voice: bool = True) -> str:
    work = project / "work"
    content = work / "content.md"
    if not content.is_file():
        raise ValueError(f"missing canonical PRD content: {content}")

    lines = [
        f"# {title} — Development Context",
        "",
        f"PRD Version: v{version}",
        f"Status: {status or 'unknown'}",
        "",
        "## Reading Guidance",
        "",
        *(f"- {rule}" for rule in GUIDANCE),
        "",
        "## Accepted PRD",
        "",
        _section_source(content, 1),
    ]

    asset_requirements = work / "asset-requirements.md"
    voice_requirements = work / "voice-requirements.md"
    if asset_requirements.is_file() or (include_voice and voice_requirements.is_file()):
        lines.extend(["", "## Production Assets"])
        if asset_requirements.is_file():
            lines.extend(["", "### Non-Voice Requirements", "", _section_source(asset_requirements, 2)])
        if include_voice and voice_requirements.is_file():
            lines.extend(["", "### Voice Requirements", "", _section_source(voice_requirements, 2)])
    return "\n".join(lines).rstrip() + "\n"


def _navigation(markdown: str, max_level: int = 4) -> list[dict[str, Any]]:
    lines = markdown.splitlines()
    headings: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, 1):
        match = HEADING_RE.match(line)
        if match:
            headings.append({"level": len(match.group(1)), "title": match.group(2).strip(), "start_line": line_number})
    for index, heading in enumerate(headings):
        end_line = len(lines)
        for later in headings[index + 1 :]:
            if later["level"] <= heading["level"]:
                end_line = later["start_line"] - 1
                break
        heading["end_line"] = end_line

    roots: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    sibling_counts: dict[tuple[str, str], int] = {}
    for heading in headings:
        if heading["level"] > max_level:
            continue
        while stack and stack[-1]["level"] >= heading["level"]:
            stack.pop()
        parent = stack[-1] if stack else None
        parent_id = parent["id"] if parent else ""
        base = _slug(heading["title"])
        count_key = (parent_id, base)
        sibling_counts[count_key] = sibling_counts.get(count_key, 0) + 1
        suffix = f"-{sibling_counts[count_key]}" if sibling_counts[count_key] > 1 else ""
        local_id = f"{base}{suffix}"
        node_id = f"{parent_id}/{local_id}" if parent_id else local_id
        node: dict[str, Any] = {
            "id": node_id,
            "title": heading["title"],
            "lines": [heading["start_line"], heading["end_line"]],
            "_children": [],
            "level": heading["level"],
        }
        if parent:
            parent["_children"].append(node)
        else:
            roots.append(node)
        stack.append(node)

    def compact(node: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": node["id"],
            "title": node["title"],
            "lines": node["lines"],
        }
        children = [compact(child) for child in node["_children"]]
        if children:
            result["children"] = children
        return result

    return [compact(root) for root in roots]


def build_index(project: Path, title: str, version: str, status: str, context: str) -> dict[str, Any]:
    return {
        "project": {
            "id": project.name,
            "title": title,
            "prd_version": version,
            "status": status or "unknown",
        },
        "documents": {
            "human_prd": "prd.html",
            "development_context": "context.md",
            "development_index": "index.json",
        },
        "reading": {
            "primary": "index.json",
            "instruction": (
                "Locate the affected section here, then read only its line range from context.md. "
                "Read broader/global context only when the task actually depends on it."
            ),
        },
        "navigation": _navigation(context),
    }


def _version_key(folder: Path) -> tuple[int, int, int] | None:
    match = SEMVER_RE.fullmatch(folder.name)
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def build_readme(output_root: Path, title: str, version: str, status: str) -> str:
    versions: list[tuple[tuple[int, int, int], str]] = []
    if output_root.is_dir():
        for item in output_root.iterdir():
            if item.is_dir() and (key := _version_key(item)) is not None:
                versions.append((key, item.name))
    current_name = f"v{version}"
    major, minor, patch = version.split(".")
    current_key = (int(major), int(minor), int(patch))
    if current_name not in {name for _, name in versions}:
        versions.append((current_key, current_name))
    versions.sort(reverse=True)
    version_lines = [f"- `{name}`{' — current' if name == current_name else ''}" for _, name in versions]
    return "\n".join(
        [
            f"# {title}",
            "",
            f"Current PRD Version: `{current_name}`",
            f"Status: `{status or 'unknown'}`",
            "",
            "## Start Here",
            "",
            f"- Human review: `{current_name}/prd.html`",
            (
                f"- AI/development: open `{current_name}/index.json` first, then read only the relevant line "
                f"range in `{current_name}/context.md`."
            ),
            "",
            "## Resume Method",
            "",
            "1. Use `index.json` to locate the affected objective/system and its context range.",
            "2. Read only that range in `context.md`, plus directly relevant shared/global sections.",
            "3. Inspect the current implementation for the same scope.",
            "4. Apply the smallest correct change; preserve unrelated accepted behavior.",
            "5. If a new product decision is required, surface it instead of inferring it from legacy/template code.",
            "",
            (
                "The PRD package describes accepted product/development context. Current code/runtime progress remains "
                "owned by the implementation repository."
            ),
            "",
            "## Versions",
            "",
            *version_lines,
            "",
            (
                "Version folders track PRD meaning. Downstream Production Assets may refresh inside the current PRD "
                "version when project meaning itself has not changed."
            ),
            "",
        ]
    )


def _default_html_renderer(template: Path | None, render_data: Path, output: Path) -> None:
    if template is None:
        template = KIT_ROOT / "template" / "golden-reference.html"
    html_renderer_module.render(template, render_data, output)


def _publish_bundle(
    output_root: Path,
    version_dir: Path,
    staged_version: Path,
    staged_readme: Path,
) -> None:
    """Publish a complete version directory and README with rollback on any failure."""

    backup_root = staged_version.parent / "previous"
    backup_version = backup_root / version_dir.name
    backup_readme = backup_root / "README.md"
    backup_root.mkdir(parents=True, exist_ok=True)
    readme_target = output_root / "README.md"

    moved_version = False
    moved_readme = False
    published_version = False
    published_readme = False
    try:
        if version_dir.exists():
            os.replace(version_dir, backup_version)
            moved_version = True
        if readme_target.exists():
            os.replace(readme_target, backup_readme)
            moved_readme = True

        os.replace(staged_version, version_dir)
        published_version = True
        os.replace(staged_readme, readme_target)
        published_readme = True
    except Exception:
        if published_readme and readme_target.exists():
            readme_target.unlink()
        if published_version and version_dir.exists():
            shutil.rmtree(version_dir)
        if moved_version and backup_version.exists():
            os.replace(backup_version, version_dir)
        if moved_readme and backup_readme.exists():
            os.replace(backup_readme, readme_target)
        raise


def build_delivery(
    project: Path,
    *,
    template: Path | None = None,
    html_renderer: Callable[[Path | None, Path, Path], None] | None = None,
) -> dict[str, Path]:
    project = project.resolve()
    render_data_path = project / "work" / "render-data.json"
    if not render_data_path.is_file():
        raise ValueError(f"missing render data: {render_data_path}")
    data = json.loads(render_data_path.read_text(encoding="utf-8"))
    document = data.get("document") if isinstance(data, dict) else None
    if not isinstance(document, dict):
        raise ValueError("render-data.json must contain document metadata")
    title_value = document.get("title")
    title = str(title_value.get("en") if isinstance(title_value, dict) else title_value or "").strip()
    if not title:
        raise ValueError("render-data.document.title is required for delivery")
    version = _semver(document.get("version"))
    status = _handoff_status(project)

    output_root = project / "output"
    version_dir = output_root / f"v{version}"
    targets = {
        "readme": output_root / "README.md",
        "prd": version_dir / "prd.html",
        "context": version_dir / "context.md",
        "index": version_dir / "index.json",
    }
    renderer = html_renderer or _default_html_renderer

    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".prd-delivery-", dir=output_root) as tmp:
        staging_root = Path(tmp)
        staged_version = staging_root / f"v{version}"
        staged_version.mkdir(parents=True)
        staged_readme = staging_root / "README.md"
        staged_prd = staged_version / "prd.html"
        staged_context = staged_version / "context.md"
        staged_index = staged_version / "index.json"

        renderer(template, render_data_path, staged_prd)
        context = build_context(project, title, version, status)
        staged_context.write_text(context, encoding="utf-8")
        staged_index.write_text(
            json.dumps(
                build_index(project, title, version, status, context),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        staged_readme.write_text(
            build_readme(output_root, title, version, status),
            encoding="utf-8",
        )

        required = (staged_prd, staged_context, staged_index, staged_readme)
        if any(not path.is_file() or path.stat().st_size == 0 for path in required):
            raise ValueError("staged delivery is incomplete; current delivery was not modified")

        _publish_bundle(output_root, version_dir, staged_version, staged_readme)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="workspace/active/<project> directory")
    parser.add_argument("--template", type=Path, default=None)
    args = parser.parse_args()
    try:
        outputs = build_delivery(args.project, template=args.template)
    except (OSError, StateError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRD DELIVERY FAILED: {exc}", file=sys.stderr)
        return 2
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
