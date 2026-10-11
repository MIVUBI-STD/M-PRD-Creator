#!/usr/bin/env python3
"""Render PRD data through the exact approved Golden presentation shell."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT_ROOT = HERE.parent
if __package__ in (None, ""):
    if str(KIT_ROOT) not in sys.path:
        sys.path.insert(0, str(KIT_ROOT))
    from shared.intake import load_intake_state
    from shared.render_schema import validate_projection_schema
    from shared.state import StateError

    from renderer import prd_render_engine as engine
    from renderer import production_assets_compositor as production_assets
    from renderer.core import slug, txt
    from renderer.template_adapter import TemplateAdapter
else:
    from shared.intake import load_intake_state
    from shared.render_schema import validate_projection_schema
    from shared.state import StateError

    from . import prd_render_engine as engine
    from . import production_assets_compositor as production_assets
    from .core import slug, txt
    from .template_adapter import TemplateAdapter


def _load_projection(render_data: Path) -> dict:
    data = json.loads(render_data.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("render-data root must be an object")
    validate_projection_schema(data)

    work = render_data.parent
    project = work.parent
    content_path = work / "content.md"
    if content_path.is_file():
        actual_content_sha = hashlib.sha256(content_path.read_bytes()).hexdigest()
        if data["canonical_content_sha256"] != actual_content_sha:
            raise ValueError(
                "render-data canonical_content_sha256 does not match current sibling work/content.md bytes"
            )

    intake_path = project / "state" / "intake-state.yaml"
    if intake_path.is_file():
        try:
            intake = load_intake_state(intake_path)
        except StateError as exc:
            raise ValueError(f"current Project Requirements intake state is invalid: {exc}") from exc
        if data["approved_requirement_sha256"] != intake.approved_requirement_sha256:
            raise ValueError(
                "render-data approved_requirement_sha256 does not match current Project Requirements approval"
            )
    return data


def _augment_production_assets(render_data: Path, output: Path) -> None:
    production_assets.augment_project_html(
        render_data,
        output,
        render_data.parent / "voice-production.md",
    )


def render(template: Path, render_data: Path, output: Path) -> None:
    data = _load_projection(render_data)
    source = template.read_text(encoding="utf-8")
    if engine.STORAGE_PREFIX_TOKEN in source:
        engine.render(template, render_data, output)
        _augment_production_assets(render_data, output)
        return

    namespace = slug(txt(data["document"]["title"])["en"])
    adapter = TemplateAdapter.prepare_reference_shell(
        source,
        namespace=namespace,
        runtime_token=engine.STORAGE_PREFIX_TOKEN,
    )
    with tempfile.TemporaryDirectory(prefix="prd-golden-") as tmp:
        prepared_path = Path(tmp) / "runtime-template.html"
        prepared_path.write_text(adapter.source, encoding="utf-8")
        engine.render(prepared_path, render_data, output)
    _augment_production_assets(render_data, output)


def main() -> int:
    default_template = KIT_ROOT / "template" / "golden-reference.html"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("render_data", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--template", type=Path, default=default_template)
    args = parser.parse_args()
    try:
        render(args.template, args.render_data, args.output)
        print(args.output)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRD RENDER FAILED: {exc}", file=sys.stderr)
        return 2


validate = engine.validate


if __name__ == "__main__":
    raise SystemExit(main())
