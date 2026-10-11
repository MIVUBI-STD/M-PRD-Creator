from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prd_fixture import (
    asset_model_text,
    asset_ui_text,
    render_data,
    set_completion_only,
    write_base_project,
    write_render_data,
)

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "kits" / "prd-creator" / "renderer" / "render.py"
DELIVERY = ROOT / "kits" / "prd-creator" / "renderer" / "delivery.py"
VALIDATOR = ROOT / "kits" / "prd-creator" / "validator" / "validate.py"
GOLDEN_TEMPLATE = ROOT / "kits" / "prd-creator" / "template" / "golden-reference.html"

BILINGUAL_SCALARS = {
    "approved_requirement_sha256",
    "canonical_content_sha256",
    "id",
    "key",
    "code",
    "version",
    "brand_mark",
    "languages",
    "roles",
    "weight",
    "step",
    "formula",
    "mode",
}


def run_cli(*args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def bilingual_render_data() -> dict:
    def localized(value: object, field: str | None = None) -> object:
        if isinstance(value, dict):
            keys = set(value)
            if keys and keys.issubset({"en", "id"}):
                return value
            return {key: localized(child, key) for key, child in value.items()}
        if isinstance(value, list):
            return [localized(child, field) for child in value]
        if isinstance(value, str) and value and field not in BILINGUAL_SCALARS:
            indonesian = f"ID · {value}".replace("without", "tanpa")
            return {"en": value, "id": indonesian}
        return value

    data = localized(render_data())
    assert isinstance(data, dict)
    data["document"]["languages"] = ["en", "id"]
    return data


class ProjectDocumentContracts(unittest.TestCase):
    def make_project(self, data: dict | None = None) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name)
        write_base_project(project, data)
        return project

    def render(
        self,
        project: Path,
        template: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        args: list[Path | str] = [
            RENDERER,
            project / "work" / "render-data.json",
            project / "output" / "v1.0.0" / "prd.html",
        ]
        if template is not None:
            args.extend(["--template", template])
        return run_cli(*args)

    def validate(self, project: Path) -> subprocess.CompletedProcess[str]:
        return run_cli(VALIDATOR, project)

    def test_full_golden_contract_renders_and_validates(self) -> None:
        project = self.make_project()
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        for marker in (
            "Global Gameplay Direction",
            "Gameplay Context",
            "Main Objective",
            "Gameplay Information",
            "Build and Visual Requirements",
            "Development Requirements",
            'id="flow-start"',
            'id="development-overview"',
            'id="dev-core-developer"',
            'class="flow quarry-development-flow"',
            'class="production-table quarry-build-table"',
            'class="production-table quarry-development-table"',
        ):
            self.assertIn(marker, html)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        result = json.loads(validated.stdout)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["expected_pages"]), 10)

    def test_default_render_is_byte_identical_to_explicit_canonical_golden(self) -> None:
        default_project = self.make_project()
        explicit_project = self.make_project()
        default_render = self.render(default_project)
        explicit_render = self.render(explicit_project, GOLDEN_TEMPLATE)
        self.assertEqual(default_render.returncode, 0, default_render.stderr or default_render.stdout)
        self.assertEqual(explicit_render.returncode, 0, explicit_render.stderr or explicit_render.stdout)
        default_html = default_project / "output" / "v1.0.0" / "prd.html"
        explicit_html = explicit_project / "output" / "v1.0.0" / "prd.html"
        self.assertEqual(default_html.read_bytes(), explicit_html.read_bytes())

    def test_renderer_rejects_missing_mandatory_functions(self) -> None:
        variants = {
            "missing global function": lambda data: data["global_development"].pop(2),
            "missing package flow page": lambda data: data["gameplay_flow"].pop(),
            "missing document scope": lambda data: data["overview"].update({"document_scope": ""}),
            "missing gameplay time": lambda data: data["packages"][0]["gameplay"].update({"gameplay_time": ""}),
            "missing design flow": lambda data: data["packages"][0]["level_design"].update({"flow": []}),
            "missing developer reset": lambda data: data["packages"][0]["developer"].update({"reset": []}),
            "missing acceptance": lambda data: data["packages"][0].update({"acceptance": []}),
        }
        for name, mutate in variants.items():
            with self.subTest(name=name):
                data = render_data()
                mutate(data)
                project = self.make_project(data)
                self.assertEqual(self.render(project).returncode, 2)

    def test_non_scored_package_uses_completion_not_scoring_language(self) -> None:
        data = render_data()
        set_completion_only(data)
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        self.assertIn("No Objective Score", html)
        self.assertIn("Completion Criteria", html)
        self.assertNotIn(">Scoring Criteria</b><", html)

    def test_percentage_string_does_not_render_double_percent(self) -> None:
        data = render_data()
        data["packages"][0]["developer"]["scoring"]["components"][0]["weight"] = "100%"
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        self.assertIn("100%", html)
        self.assertNotIn("100%%", html)

    def test_bilingual_document_rejects_implicit_translation(self) -> None:
        data = bilingual_render_data()
        data["packages"][0]["gameplay"]["main_objective"] = "English-only objective."
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("must use an explicit en/id localized value", rendered.stderr)

    def test_bilingual_document_rejects_numeric_drift(self) -> None:
        data = bilingual_render_data()
        data["packages"][0]["gameplay"]["result_model"]["summary"] = {
            "en": "Completion contributes 100% of Fixture Score.",
            "id": "Completion menyumbang 80% dari Fixture Score.",
        }
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("numeric/unit/dimension/coordinate/stable-ID invariants", rendered.stderr)

    def test_bilingual_document_rejects_unit_drift(self) -> None:
        data = bilingual_render_data()
        data["packages"][0]["gameplay"]["gameplay_time"] = {
            "en": "Complete within 10 seconds.",
            "id": "Selesaikan dalam 12 detik.",
        }
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("numeric/unit/dimension/coordinate/stable-ID invariants", rendered.stderr)

    def test_bilingual_document_rejects_material_negation_drift(self) -> None:
        data = bilingual_render_data()
        data["packages"][0]["gameplay"]["blocked_or_fail_condition"] = {
            "en": "The player must not leave the route.",
            "id": "Pemain meninggalkan rute.",
        }
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("material negation count", rendered.stderr)

    def test_validator_rejects_stale_html_after_projection_change(self) -> None:
        project = self.make_project()
        self.assertEqual(self.render(project).returncode, 0)
        updated = render_data()
        updated["overview"]["project_context"] = "Updated controlled fixture context."
        write_render_data(project, updated)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1)
        self.assertIn("html_matches_current_render_data", validated.stdout)

    def test_renderer_rejects_stale_content_hash(self) -> None:
        project = self.make_project()
        (project / "work" / "content.md").write_text(
            "# Contract Fixture\n\nChanged after projection.\n",
            encoding="utf-8",
        )
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("canonical_content_sha256", rendered.stderr)

    def test_renderer_rejects_stale_flow2_approval_hash(self) -> None:
        project = self.make_project()
        state = project / "state" / "intake-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "approved_requirement_sha256: ",
                "approved_requirement_sha256: " + ("0" * 64) + " # stale ",
                1,
            ),
            encoding="utf-8",
        )
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("approved_requirement_sha256", rendered.stderr)

    def test_renderer_rejects_changed_requirement_bytes_before_writing_html(self) -> None:
        project = self.make_project()
        first = self.render(project)
        self.assertEqual(first.returncode, 0, first.stderr or first.stdout)
        html_path = project / "output" / "v1.0.0" / "prd.html"
        old_html = html_path.read_bytes()

        requirement_path = project / "state" / "requirement-register.yaml"
        requirement_path.write_text(
            requirement_path.read_text(encoding="utf-8") + "\n# Changed after approval\n",
            encoding="utf-8",
        )
        rejected = self.render(project)
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("current Project Requirements register bytes", rejected.stderr)
        self.assertEqual(html_path.read_bytes(), old_html)

    def test_projection_rejects_unknown_compatibility_field(self) -> None:
        data = render_data()
        data["packages"][0]["gameplay"]["estimated_time"] = "legacy alias"
        project = self.make_project(data)
        rendered = self.render(project)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("unsupported projection field", rendered.stderr)

    def test_glossary_json_is_script_safe(self) -> None:
        data = render_data()
        payload = "Before </script><script>window.injected=true</script> after"
        data["packages"][0]["terms"][0]["definition"] = payload
        project = self.make_project(data)
        self.assertEqual(self.render(project).returncode, 0)
        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        self.assertNotIn(payload, html)
        self.assertIn(r"\u003c/script\u003e", html)

    def test_default_golden_strips_sample_identity_but_keeps_golden_runtime(self) -> None:
        project = self.make_project()
        self.assertEqual(self.render(project).returncode, 0)
        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        self.assertNotIn('name="golden-sample-id"', html)
        self.assertIn("prd-contract-fixture-document-theme", html)
        self.assertNotIn("aftershock-document-theme", html)

    def test_template_requires_current_golden_shell_markers(self) -> None:
        project = self.make_project()
        broken = project / "broken-template.html"
        broken.write_text(
            GOLDEN_TEMPLATE.read_text(encoding="utf-8").replace(
                '<nav class="sidebar-nav">',
                '<nav class="sidebar-nav-broken">',
                1,
            ),
            encoding="utf-8",
        )
        rendered = self.render(project, broken)
        self.assertEqual(rendered.returncode, 2)
        self.assertIn("sidebar navigation marker", rendered.stderr)

    def test_versioned_delivery_and_validator_share_prd_path(self) -> None:
        project = self.make_project()
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        current_prd = project / "output" / "v1.0.0" / "prd.html"
        self.assertTrue(current_prd.is_file())
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        payload = json.loads(validated.stdout)
        rendered_check = next(item for item in payload["checks"] if item["check"] == "rendered_html_exists")
        self.assertIn("v1.0.0/prd.html", rendered_check["detail"].replace("\\", "/"))

    def test_validator_accepts_valid_additive_production_assets_pages(self) -> None:
        project = self.make_project()
        (project / "work" / "asset-requirements.md").write_text(asset_model_text(), encoding="utf-8")
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        payload = json.loads(validated.stdout)
        page_check = next(
            item for item in payload["checks"] if item["check"] == "generated_page_set_matches_current_render_data"
        )
        self.assertIn("additive Production Assets pages: 1", page_check["detail"])

    def test_validator_rejects_stale_non_voice_asset_requirements(self) -> None:
        project = self.make_project()
        asset_path = project / "work" / "asset-requirements.md"
        asset_path.write_text(asset_model_text(), encoding="utf-8")
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        self.assertEqual(self.validate(project).returncode, 0)
        asset_path.write_text(
            asset_model_text().replace("Central interaction target", "Revised central interaction target"),
            encoding="utf-8",
        )
        stale = self.validate(project)
        self.assertEqual(stale.returncode, 1)
        payload = json.loads(stale.stdout)
        check = next(item for item in payload["checks"] if item["check"] == "html_matches_current_asset_requirements")
        self.assertIn("stale", check["detail"])

    def test_validator_rejects_stale_asset_binding_after_source_removal(self) -> None:
        project = self.make_project()
        asset_path = project / "work" / "asset-requirements.md"
        asset_path.write_text(asset_ui_text(), encoding="utf-8")
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        asset_path.unlink()
        stale = self.validate(project)
        self.assertEqual(stale.returncode, 1)
        payload = json.loads(stale.stdout)
        check = next(item for item in payload["checks"] if item["check"] == "html_matches_current_asset_requirements")
        self.assertIn("binding", check["detail"])

    def test_current_validator_and_renderer_use_named_package_engines(self) -> None:
        kit = ROOT / "kits" / "prd-creator"
        validator_dir = kit / "validator"
        renderer_dir = kit / "renderer"
        self.assertTrue((validator_dir / "prd_validation_engine.py").is_file())
        self.assertTrue((validator_dir / "html_contract.py").is_file())
        self.assertTrue((validator_dir / "voice_validation.py").is_file())
        self.assertTrue((renderer_dir / "prd_render_engine.py").is_file())
        self.assertTrue((renderer_dir / "template_adapter.py").is_file())
        self.assertFalse((validator_dir / "_engine.py").exists())
        self.assertFalse((renderer_dir / "_engine.py").exists())
        validator_source = (validator_dir / "prd_validation_engine.py").read_text(encoding="utf-8")
        renderer_source = (renderer_dir / "prd_render_engine.py").read_text(encoding="utf-8")
        compositor_source = (renderer_dir / "production_assets_compositor.py").read_text(encoding="utf-8")
        self.assertNotIn("sys.path.insert", validator_source)
        self.assertNotIn("sys.path.insert", renderer_source)
        self.assertNotIn("apply_result_summaries", renderer_source)
        self.assertIn("TemplateAdapter", compositor_source)
        self.assertNotIn("def _insert(", compositor_source)


if __name__ == "__main__":
    unittest.main()
