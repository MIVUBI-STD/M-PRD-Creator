from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from prd_fixture import render_data, write_base_project, write_render_data
from test_prd_contracts import RENDERER, VALIDATOR, run_cli


class Flow2StateConsistencyContracts(unittest.TestCase):
    def make_project(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name)
        write_base_project(project, render_data())
        rendered = run_cli(
            RENDERER,
            project / "work" / "render-data.json",
            project / "output" / "v1.0.0" / "prd.html",
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        return project

    def validate(self, project: Path):
        return run_cli(VALIDATOR, project)

    @staticmethod
    def refresh_approval(project: Path) -> None:
        requirement_path = project / "state" / "requirement-register.yaml"
        digest = hashlib.sha256(requirement_path.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: true\napproved_requirement_sha256: {digest}\n",
            encoding="utf-8",
        )

    def assert_flow2_failure(self, project: Path, needle: str) -> None:
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        result = json.loads(validated.stdout)
        joined = "\n".join(result["errors"])
        self.assertIn("flow2_state_current", joined)
        self.assertIn(needle, joined)

    def test_ready_allows_authoritative_only_without_preview_approval(self) -> None:
        project = self.make_project()
        state = project / "state" / "intake-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace("preview_approved: true\n", "", 1),
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        result = json.loads(validated.stdout)
        self.assertFalse(any("Proposal approval is declared" in item for item in result["warnings"]))

    def test_ready_rejects_duplicate_preview_approval_key(self) -> None:
        project = self.make_project()
        state = project / "state" / "intake-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "preview_approved: true\n",
                "preview_approved: true\npreview_approved: false\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "duplicate YAML mapping key")

    def test_ready_allows_explicit_preview_not_approved_without_proposal(self) -> None:
        project = self.make_project()
        requirement_path = project / "state" / "requirement-register.yaml"
        digest = hashlib.sha256(requirement_path.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: false\napproved_requirement_sha256: {digest}\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)

    def test_ready_rejects_approved_proposal_without_preview_approval(self) -> None:
        project = self.make_project()
        requirement_path = project / "state" / "requirement-register.yaml"
        requirement_path.write_text(
            "requirements:\n"
            "  - id: REQ-001\n"
            "    area: gameplay\n"
            "    statement: Approved fixture decision.\n"
            "    provenance: [SRC-001]\n"
            "    impact: high\n"
            "    recovery_class: proposal\n"
            "    approval_status: approved\n"
            "    resolution: User approval is required for this material choice.\n",
            encoding="utf-8",
        )
        digest = hashlib.sha256(requirement_path.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\napproved_requirement_sha256: {digest}\n",
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "FLOW2_PROPOSAL_APPROVAL_REQUIRED")

    def test_ready_rejects_stale_requirement_approval_hash(self) -> None:
        project = self.make_project()
        requirement_path = project / "state" / "requirement-register.yaml"
        requirement_path.write_text(
            requirement_path.read_text(encoding="utf-8").replace(
                "Preserve the approved fixture experience.",
                "Preserve the newly changed fixture experience.",
            ),
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "FLOW2_APPROVAL_STALE")

    def test_ready_rejects_missing_or_empty_required_persisted_state(self) -> None:
        variants = {
            "missing source inventory": ("source-inventory.yaml", None),
            "missing requirement register": ("requirement-register.yaml", None),
            "empty source inventory": ("source-inventory.yaml", "sources:\n"),
            "empty requirement register": ("requirement-register.yaml", "requirements:\n"),
        }
        for name, (filename, replacement) in variants.items():
            with self.subTest(name=name):
                project = self.make_project()
                path = project / "state" / filename
                if replacement is None:
                    path.unlink()
                else:
                    path.write_text(replacement, encoding="utf-8")
                self.assert_flow2_failure(project, filename)

    def test_ready_rejects_pending_or_blocked_requirement(self) -> None:
        variants = {
            "pending": (
                "recovery_class: proposal\n    approval_status: pending\n    resolution: Proposed fixture default.\n",
                "REQUIREMENT_APPROVAL_PENDING",
            ),
            "blocked": (
                "recovery_class: blocked\n    resolution: Required evidence is unavailable.\n",
                "REQUIREMENT_BLOCKED",
            ),
        }
        for name, (extra, needle) in variants.items():
            with self.subTest(name=name):
                project = self.make_project()
                (project / "state" / "requirement-register.yaml").write_text(
                    "requirements:\n"
                    "  - id: REQ-001\n"
                    "    area: gameplay\n"
                    "    statement: Material fixture decision.\n"
                    "    provenance: [SRC-001]\n"
                    "    impact: high\n"
                    f"    {extra}",
                    encoding="utf-8",
                )
                self.refresh_approval(project)
                self.assert_flow2_failure(project, needle)

    def test_ready_rejects_dangling_provenance(self) -> None:
        project = self.make_project()
        path = project / "state" / "requirement-register.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace("[SRC-001]", "[SRC-999]"),
            encoding="utf-8",
        )
        self.refresh_approval(project)
        self.assert_flow2_failure(project, "unknown source id")

    def test_ready_rejects_current_blocked_source_inspection(self) -> None:
        project = self.make_project()
        (project / "state" / "source-inventory.yaml").write_text(
            "sources:\n"
            "  - id: SRC-001\n"
            "    type: instruction\n"
            "    role: authoritative\n"
            "    status: current\n"
            "    origin: user\n"
            "    summary: Current fixture authority.\n"
            "    inspection: blocked\n",
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "SOURCE_INSPECTION_BLOCKED")

    def test_ready_allows_superseded_blocked_source_when_current_provenance_exists(self) -> None:
        project = self.make_project()
        (project / "state" / "source-inventory.yaml").write_text(
            "sources:\n"
            "  - id: SRC-001\n"
            "    type: instruction\n"
            "    role: authoritative\n"
            "    status: superseded\n"
            "    origin: user\n"
            "    summary: Legacy fixture authority.\n"
            "    inspection: blocked\n"
            "  - id: SRC-002\n"
            "    type: instruction\n"
            "    role: authoritative\n"
            "    status: current\n"
            "    origin: user\n"
            "    summary: Current fixture authority.\n"
            "    inspection: full\n",
            encoding="utf-8",
        )
        requirement = project / "state" / "requirement-register.yaml"
        requirement.write_text(
            requirement.read_text(encoding="utf-8").replace("[SRC-001]", "[SRC-002]"),
            encoding="utf-8",
        )
        self.refresh_approval(project)
        render_data_path = project / "work" / "render-data.json"
        current_data = json.loads(render_data_path.read_text(encoding="utf-8"))
        write_render_data(project, current_data)
        rendered = run_cli(
            RENDERER,
            render_data_path,
            project / "output" / "v1.0.0" / "prd.html",
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)

    def test_ready_rejects_retained_source_hash_mismatch(self) -> None:
        project = self.make_project()
        source_dir = project / "source" / "originals"
        source_dir.mkdir(parents=True)
        retained = source_dir / "brief.txt"
        retained.write_text("current source bytes\n", encoding="utf-8")
        wrong_sha = "f" * 64
        (project / "state" / "source-inventory.yaml").write_text(
            "sources:\n"
            "  - id: SRC-001\n"
            "    type: file\n"
            "    role: authoritative\n"
            "    status: current\n"
            "    origin: client\n"
            "    summary: Current source.\n"
            "    inspection: full\n"
            "    retention: repository\n"
            "    path: source/originals/brief.txt\n"
            f"    sha256: {wrong_sha}\n",
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "does not match current retained source bytes")

    def test_ready_rejects_unsafe_retained_source_path(self) -> None:
        project = self.make_project()
        (project / "state" / "source-inventory.yaml").write_text(
            "sources:\n"
            "  - id: SRC-001\n"
            "    type: file\n"
            "    role: authoritative\n"
            "    status: current\n"
            "    origin: client\n"
            "    summary: Current source.\n"
            "    inspection: full\n"
            "    retention: repository\n"
            "    path: ../outside.txt\n"
            "    sha256: " + "f" * 64 + "\n",
            encoding="utf-8",
        )
        self.assert_flow2_failure(project, "non-canonical path segment")

    def test_ready_allows_approved_proposal_with_current_provenance(self) -> None:
        project = self.make_project()
        requirement = project / "state" / "requirement-register.yaml"
        requirement.write_text(
            "requirements:\n"
            "  - id: REQ-001\n"
            "    area: gameplay\n"
            "    statement: Approved fixture decision.\n"
            "    provenance: [SRC-001]\n"
            "    impact: high\n"
            "    evidence_status: conflict\n"
            "    recovery_class: proposal\n"
            "    approval_status: approved\n"
            "    resolution: Higher-authority preview approval resolves the conflict.\n",
            encoding="utf-8",
        )
        self.refresh_approval(project)
        write_render_data(project, render_data())
        rendered = run_cli(
            RENDERER,
            project / "work" / "render-data.json",
            project / "output" / "v1.0.0" / "prd.html",
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        result = json.loads(validated.stdout)
        self.assertEqual(result["status"], "pass")
        self.assertTrue(
            any("do not independently authenticate a user's decision" in item for item in result["warnings"])
        )


if __name__ == "__main__":
    unittest.main()
