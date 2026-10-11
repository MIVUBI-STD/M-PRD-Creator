from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkflowNamingContracts(unittest.TestCase):
    def test_production_assets_navigation_has_no_numeric_workflow_alias(self) -> None:
        source = (ROOT / "kits/prd-creator/renderer/production_assets_compositor.py").read_text(encoding="utf-8")
        self.assertNotIn('data-full-index="04"', source)
        self.assertNotIn(">04</span>", source)

    def test_active_workspace_policy_has_no_retired_flow_names(self) -> None:
        policy = (ROOT / "workspace" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Flow 2", policy)
        self.assertNotIn("Flow 3", policy)
        self.assertNotIn("Flow 4", policy)
        self.assertNotIn("Flow 5", policy)
        self.assertIn("Project Requirements", policy)
        self.assertIn("Production Assets", policy)

    def test_renderer_error_uses_project_requirements(self) -> None:
        source = (ROOT / "kits" / "prd-creator" / "renderer" / "render.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("current Flow 2", source)
        self.assertIn("current Project Requirements", source)

    def test_root_readme_uses_canonical_human_workflow_names(self) -> None:
        source = (ROOT / "README.md").read_text(encoding="utf-8")
        expected = (
            "Project Setup\n"
            "→ Project Requirements\n"
            "→ PRD Production\n"
            "   └─ Production Assets when required\n"
            "→ PRD Handoff\n"
            "→ Voice Requirements when Voice is justified\n"
            "→ Voice Production\n"
            "→ Voice Delivery"
        )
        self.assertIn(expected, source)


if __name__ == "__main__":
    unittest.main()
