from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from prd_fixture import (
    acceptance_text,
    asset_model_text,
    handoff_state_text,
    render_data,
    set_completion_only,
    write_base_project,
    write_render_data,
)

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_VALIDATOR = ROOT / "kits" / "prd-creator" / "validator" / "validate_handoff.py"
RENDERER = ROOT / "kits" / "prd-creator" / "renderer" / "render.py"
DELIVERY = ROOT / "kits" / "prd-creator" / "renderer" / "delivery.py"
VALIDATOR = ROOT / "kits" / "prd-creator" / "validator" / "validate.py"
OPERATOR = ROOT / "tools" / "prd.py"


def run_cli(*args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class PrdHandoffContracts(unittest.TestCase):
    def make_project(
        self,
        *,
        current_version: str = "1.0.0",
        accepted_version: str | None = None,
        status: str = "handoff_ready",
        with_assets: bool = False,
    ) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name)
        data = render_data()
        data["document"]["version"] = current_version
        write_base_project(project, data)
        if with_assets:
            (project / "work" / "asset-requirements.md").write_text(
                asset_model_text(),
                encoding="utf-8",
            )

        version_dir = project / "output" / f"v{current_version}"
        version_dir.mkdir(parents=True, exist_ok=True)
        rendered = run_cli(
            RENDERER,
            project / "work" / "render-data.json",
            version_dir / "prd.html",
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)

        accepted = accepted_version if accepted_version is not None else current_version
        (version_dir / "context.md").write_text(
            f"# Contract — Development Context\n\nPRD Version: v{current_version}\n",
            encoding="utf-8",
        )
        (version_dir / "index.json").write_text(
            json.dumps({"project": {"prd_version": current_version}}, indent=2) + "\n",
            encoding="utf-8",
        )
        (project / "output" / "README.md").write_text(
            f"# Contract\n\nCurrent PRD Version: `v{accepted}`\n",
            encoding="utf-8",
        )
        acceptance = acceptance_text(project, status=status)
        (project / "work" / "acceptance.md").write_text(acceptance, encoding="utf-8")
        state_text = (
            handoff_state_text(current_version)
            .replace(
                "status: handoff_ready",
                f"status: {status}",
                1,
            )
            .replace(
                f"accepted_prd_version: {current_version}",
                f"accepted_prd_version: {accepted}",
                1,
            )
        )
        (project / "state" / "handoff-state.yaml").write_text(state_text, encoding="utf-8")
        return project

    def make_two_package_project(self) -> Path:
        """Synthetic scored Core Trial plus completion-only Capture Trial."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        project = Path(temporary.name)
        data = render_data()
        capture = deepcopy(data["packages"][0])
        capture["id"] = "capture"
        capture["title"] = "Capture Trial"
        capture["package_label"] = "Capture Trial"
        capture["terms"] = []
        set_completion_only({"packages": [capture]})
        capture["gameplay"]["context"] = "Players enter the capture area for one completion-only objective."
        capture["gameplay"]["purpose"] = "Record one successful capture without creating an Objective Score."
        capture["gameplay"]["main_objective"] = "Activate the capture beacon and reach the exit."
        capture["gameplay"]["result"] = "One completion flag is recorded; no score is awarded."
        capture["gameplay"]["end_condition"] = "The capture beacon is activated and the exit is open."
        capture["gameplay"]["blocked_or_fail_condition"] = "Disconnect cancels the run without a completion flag."
        capture["gameplay"]["player_flow"][0]["title"] = "Enter Capture"
        capture["gameplay"]["player_flow"][0]["action"] = "Enter the assigned capture area."
        capture["gameplay"]["player_flow"][0]["result"] = "Capture activation becomes available."
        capture["developer"]["overview"] = "Own capture state, completion recording, interruption, and reset."
        capture["developer"]["flow"][2]["description"] = "Record one completion flag without any score."
        capture["developer"]["flow"][3]["description"] = "Open the capture exit and prepare its state for reset."
        capture["developer"]["requirements"][0]["items"][0]["details"] = (
            "Activate the beacon only for the assigned capture session."
        )
        capture["developer"]["requirements"][0]["items"][0]["result"] = (
            "One valid session can record one completion flag."
        )
        capture["developer"]["reset"] = [
            "Clear the capture flag, inventory changes and active session before reuse."
        ]
        capture["developer"]["reset_result"] = "The beacon, exit and completion flag return to initial state."
        capture["level_design"]["overview"] = "Readable beacon, capture route and exit with no scoring display."
        capture["level_design"]["requirements"][0]["items"][0]["object"] = "Capture Beacon"
        capture["level_design"]["requirements"][0]["items"][0]["gameplay_function"] = (
            "Gives the player one clear completion-only capture interaction."
        )
        capture["acceptance"] = [
            "Capture can start only for the assigned player and session.",
            "One valid capture creates a completion flag and no score.",
            "Disconnect clears the capture state and the beacon can be reused.",
        ]
        data["packages"].append(capture)

        flow = deepcopy(data["gameplay_flow"][1])
        flow["id"] = "capture"
        flow["title"] = "Capture Trial"
        flow["narrative_context"] = "After the scored trial, reach the capture beacon and finish without scoring."
        flow["beats"] = [
            {"title": "Locate Beacon", "description": "Follow the marked route to the capture beacon."},
            {"title": "Complete Capture", "description": "Activate the beacon once and receive completion feedback."},
        ]
        flow["next_destination"] = "Project exit"
        data["gameplay_flow"].append(flow)
        data["overview"]["facts"][2]["value"] = "Two packages: a scored trial and a completion-only capture."
        data["overview"]["main_experience"] = "Complete one scored trial, then one capture without a score."

        write_base_project(project, data)
        requirements = (
            "requirements:\n"
            "  - id: REQ-001\n"
            "    area: gameplay\n"
            "    statement: Core Trial awards one score for valid completion.\n"
            "    provenance: [SRC-001]\n"
            "  - id: REQ-002\n"
            "    area: developer\n"
            "    statement: Capture Trial disconnect resets the player session.\n"
            "    provenance: [SRC-001]\n"
            "  - id: REQ-003\n"
            "    area: gameplay\n"
            "    statement: Capture Trial records completion without score.\n"
            "    provenance: [SRC-001]\n"
            "  - id: REQ-004\n"
            "    area: developer\n"
            "    statement: Both packages release temporary state after completion.\n"
            "    provenance: [SRC-001]\n"
        )
        requirement_path = project / "state" / "requirement-register.yaml"
        requirement_path.write_text(requirements, encoding="utf-8")
        requirement_sha = hashlib.sha256(requirement_path.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: false\napproved_requirement_sha256: {requirement_sha}\n",
            encoding="utf-8",
        )
        (project / "work" / "content.md").write_text(
            "# Two-Package Synthetic Map\n\n"
            "## Core Trial Gameplay\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "The scored Core Trial records one score only after valid completion.\n\n"
            "## Capture Trial Developer\n"
            "<!-- PRD-TRACE: REQ-002 -->\n"
            "Disconnect cancels Capture Trial and resets player session data.\n\n"
            "## Capture Trial Completion\n"
            "<!-- PRD-TRACE: REQ-003 -->\n"
            "A valid capture records one completion flag but never a score.\n\n"
            "## Shared Session Cleanup\n"
            "<!-- PRD-TRACE: REQ-004 -->\n"
            "Both packages release their temporary state before reuse.\n",
            encoding="utf-8",
        )
        assets = (
            asset_model_text()
            + "\n## Capture Trial\n"
            "Owner ID: package:capture\n\n"
            "### 3D Models\n\n"
            "#### Capture Beacon\n"
            "ID: AST-CAPTURE-BEACON\n"
            "Moment ID: MOM-CAPTURE-FINISH\n"
            "Moment: Capture Finish\n"
            "Type: MODEL\n"
            "Function: Visible capture point for the completion-only objective.\n"
            "Visual Brief: Readable beacon that marks the completion interaction.\n"
        )
        (project / "work" / "asset-requirements.md").write_text(assets, encoding="utf-8")
        write_render_data(project, data)
        return project

    @staticmethod
    def accept_two_package_project(project: Path) -> None:
        """Simulate explicit fixture acceptance; the production code never auto-approves."""
        (project / "work" / "acceptance.md").write_text(
            acceptance_text(project), encoding="utf-8"
        )
        (project / "state" / "handoff-state.yaml").write_text(
            handoff_state_text(), encoding="utf-8"
        )

    def validate(self, project: Path):
        return run_cli(HANDOFF_VALIDATOR, project)

    def test_multi_package_scored_and_completion_delivery_passes_exact_handoff(self) -> None:
        project = self.make_two_package_project()
        built = run_cli(DELIVERY, project)
        self.assertEqual(built.returncode, 0, built.stderr or built.stdout)

        html = (project / "output" / "v1.0.0" / "prd.html").read_text(encoding="utf-8")
        for marker in (
            'id="dev-core-developer"',
            'id="dev-capture-developer"',
            'id="flow-capture"',
            "Capture Beacon",
        ):
            self.assertIn(marker, html)

        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        payload = json.loads(validated.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(len(payload["expected_pages"]), 14)
        self.assertEqual(payload["traceability"]["status"], "mapped_unverified")
        self.assertFalse(payload["traceability"]["semantic_verified"])

        self.accept_two_package_project(project)
        handoff = self.validate(project)
        self.assertEqual(handoff.returncode, 0, handoff.stderr or handoff.stdout)
        self.assertEqual(json.loads(handoff.stdout)["status"], "pass")

    def test_changed_accepted_requirement_preserves_delivery_until_reacceptance(self) -> None:
        project = self.make_two_package_project()
        built = run_cli(DELIVERY, project)
        self.assertEqual(built.returncode, 0, built.stderr or built.stdout)
        self.accept_two_package_project(project)
        self.assertEqual(self.validate(project).returncode, 0)

        output = project / "output"
        before = {
            path.relative_to(output): path.read_bytes()
            for path in output.rglob("*")
            if path.is_file()
        }
        old_acceptance = (project / "work" / "acceptance.md").read_bytes()
        register = project / "state" / "requirement-register.yaml"
        baseline = project / "prior-approved-register.yaml"
        baseline.write_bytes(register.read_bytes())
        register.write_text(
            register.read_text(encoding="utf-8").replace(
                "Capture Trial disconnect resets the player session.",
                "Capture Trial disconnect resets inventory, completion flags and player session.",
            ),
            encoding="utf-8",
        )
        revision = run_cli(OPERATOR, "revision", project, "--before", baseline)
        self.assertEqual(revision.returncode, 0, revision.stderr or revision.stdout)
        revision_data = json.loads(revision.stdout)
        self.assertEqual(revision_data["status"], "targeted_review_required")
        self.assertEqual(revision_data["changed_requirements"][0]["id"], "REQ-002")
        self.assertEqual(revision_data["changed_requirements"][0]["changed_fields"], ["statement"])
        self.assertEqual(revision_data["approval_binding"]["status"], "stale")
        self.assertEqual(revision_data["render_data_binding"], "stale")

        self.assertEqual(self.validate(project).returncode, 1)
        blocked = run_cli(DELIVERY, project)
        self.assertEqual(blocked.returncode, 2, blocked.stderr or blocked.stdout)
        self.assertIn("current Project Requirements register bytes", blocked.stderr)
        for name, previous_bytes in before.items():
            self.assertEqual((output / name).read_bytes(), previous_bytes, name)

        approval_sha = hashlib.sha256(register.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: false\napproved_requirement_sha256: {approval_sha}\n",
            encoding="utf-8",
        )
        still_stale = run_cli(DELIVERY, project)
        self.assertEqual(still_stale.returncode, 2)
        self.assertIn("render-data approved_requirement_sha256", still_stale.stderr)

        content_path = project / "work" / "content.md"
        content_path.write_text(
            content_path.read_text(encoding="utf-8").replace(
                "Disconnect cancels Capture Trial and resets player session data.",
                "Disconnect resets Capture Trial inventory, completion flags and player session data.",
            ),
            encoding="utf-8",
        )
        data_path = project / "work" / "render-data.json"
        write_render_data(project, json.loads(data_path.read_text(encoding="utf-8")))
        rebuilt = run_cli(DELIVERY, project)
        self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr or rebuilt.stdout)
        self.assertEqual((project / "work" / "acceptance.md").read_bytes(), old_acceptance)

        # A newly rendered bundle is not an implicitly accepted revision.
        old_handoff = self.validate(project)
        self.assertEqual(old_handoff.returncode, 1)
        self.assertIn("Accepted Render Data SHA256", old_handoff.stdout)

        self.accept_two_package_project(project)
        accepted = self.validate(project)
        self.assertEqual(accepted.returncode, 0, accepted.stderr or accepted.stdout)
        self.assertEqual(json.loads(accepted.stdout)["status"], "pass")

    def test_removed_requirement_marker_cannot_be_accepted_even_with_fresh_hashes(self) -> None:
        project = self.make_two_package_project()
        self.assertEqual(run_cli(DELIVERY, project).returncode, 0)
        self.accept_two_package_project(project)
        self.assertEqual(self.validate(project).returncode, 0)

        register = project / "state" / "requirement-register.yaml"
        old_register = register.read_text(encoding="utf-8")
        removed = (
            "  - id: REQ-003\n"
            "    area: gameplay\n"
            "    statement: Capture Trial records completion without score.\n"
            "    provenance: [SRC-001]\n"
        )
        self.assertIn(removed, old_register)
        register.write_text(old_register.replace(removed, ""), encoding="utf-8")
        approval_sha = hashlib.sha256(register.read_bytes()).hexdigest()
        (project / "state" / "intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: false\napproved_requirement_sha256: {approval_sha}\n",
            encoding="utf-8",
        )
        render_path = project / "work" / "render-data.json"
        write_render_data(project, json.loads(render_path.read_text(encoding="utf-8")))
        self.assertEqual(run_cli(DELIVERY, project).returncode, 0)
        self.accept_two_package_project(project)

        rejected = self.validate(project)
        self.assertEqual(rejected.returncode, 1)
        result = json.loads(rejected.stdout)
        self.assertIn(
            "PRD_TRACE_UNKNOWN_REQUIREMENT",
            {issue["code"] for issue in result["issues"]},
        )

    def test_current_handoff_allows_flow5_entry(self) -> None:
        project = self.make_project()
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertEqual(json.loads(validated.stdout)["status"], "pass")

    def test_same_version_stale_prd_content_cannot_authorize_flow5(self) -> None:
        project = self.make_project()
        (project / "work" / "content.md").write_text(
            "# Contract PRD\n\nChanged after acceptance without regeneration.\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("current_prd_complete_validation", validated.stdout)

    def test_same_version_regenerated_projection_requires_new_acceptance_binding(self) -> None:
        project = self.make_project()
        data_path = project / "work" / "render-data.json"
        data = json.loads(data_path.read_text(encoding="utf-8"))
        data["overview"]["project_context"] = "Changed projection under the same semantic version."
        write_render_data(project, data)
        rendered = run_cli(RENDERER, data_path, project / "output" / "v1.0.0" / "prd.html")
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("Accepted Render Data SHA256", validated.stdout)

    def test_same_version_asset_edit_requires_new_acceptance_binding(self) -> None:
        project = self.make_project(with_assets=True)
        asset_path = project / "work" / "asset-requirements.md"
        asset_path.write_text(
            asset_model_text().replace("Central interaction target", "Updated interaction target"),
            encoding="utf-8",
        )
        rendered = run_cli(
            RENDERER,
            project / "work" / "render-data.json",
            project / "output" / "v1.0.0" / "prd.html",
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("Accepted Asset Requirements SHA256", validated.stdout)

    def test_content_purity_failure_cannot_authorize_handoff(self) -> None:
        project = self.make_project()
        data_path = project / "work" / "render-data.json"
        data = json.loads(data_path.read_text(encoding="utf-8"))
        data["overview"]["project_context"] = "Follow the Golden HTML Reference exactly."
        write_render_data(project, data)
        rendered = run_cli(RENDERER, data_path, project / "output" / "v1.0.0" / "prd.html")
        self.assertEqual(rendered.returncode, 0, rendered.stderr or rendered.stdout)
        acceptance = project / "work" / "acceptance.md"
        text = acceptance.read_text(encoding="utf-8")
        new_sha = hashlib.sha256(data_path.read_bytes()).hexdigest()
        old_line = next(line for line in text.splitlines() if line.startswith("Accepted Render Data SHA256:"))
        acceptance.write_text(
            text.replace(old_line, f"Accepted Render Data SHA256: {new_sha}"),
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("content_purity", validated.stdout)

    def test_pending_review_cannot_authorize_flow5(self) -> None:
        project = self.make_project(status="needs_revision")
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("handoff_status_ready", validated.stdout)

    def test_stale_handoff_version_cannot_authorize_newer_prd(self) -> None:
        project = self.make_project(current_version="1.1.0", accepted_version="1.0.0")
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("handoff_revision_matches_current_prd", validated.stdout)

    def test_handoff_requires_existing_current_artifact_references(self) -> None:
        project = self.make_project()
        (project / "output" / "v1.0.0" / "context.md").unlink()
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("handoff_artifact_references_current", validated.stdout)

    def test_stale_delivery_metadata_cannot_authorize_handoff(self) -> None:
        project = self.make_project()
        index_path = project / "output" / "v1.0.0" / "index.json"
        index_path.write_text(
            json.dumps({"project": {"prd_version": "0.9.0"}}, indent=2) + "\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("delivery_revision_matches_current_prd", validated.stdout)

    def test_nonsemantic_version_cannot_authorize_handoff(self) -> None:
        project = self.make_project(current_version="Final Review")
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("current_prd_version_semantic", validated.stdout)

    def test_required_acceptance_gates_block_handoff_when_failed(self) -> None:
        variants = {
            "Status": "needs_revision",
            "Mechanical": "FAIL",
            "Semantic Readiness": "FAIL",
            "Material Conservation": "FAIL",
            "Visual sanity": "FAIL",
            "Critical": "1",
            "Major": "2",
        }
        for label, value in variants.items():
            with self.subTest(label=label):
                project = self.make_project()
                path = project / "work" / "acceptance.md"
                lines = path.read_text(encoding="utf-8").splitlines()
                path.write_text(
                    "\n".join(f"{label}: {value}" if line.startswith(f"{label}:") else line for line in lines) + "\n",
                    encoding="utf-8",
                )
                validated = self.validate(project)
                self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
                self.assertIn("acceptance_allows_handoff", validated.stdout)

    def test_missing_asset_acceptance_binding_cannot_authorize_flow5(self) -> None:
        project = self.make_project()
        path = project / "work" / "acceptance.md"
        path.write_text(
            "\n".join(
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if not line.startswith("Accepted Asset Requirements SHA256:")
            )
            + "\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("Accepted Asset Requirements SHA256", validated.stdout)

    def test_handoff_rejects_redundant_derived_path_field(self) -> None:
        project = self.make_project()
        path = project / "state" / "handoff-state.yaml"
        path.write_text(
            path.read_text(encoding="utf-8") + "content: work/content.md\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("unsupported field", validated.stdout)
        self.assertIn("content", validated.stdout)

    def test_handoff_rejects_unknown_state_field(self) -> None:
        project = self.make_project()
        path = project / "state" / "handoff-state.yaml"
        path.write_text(
            path.read_text(encoding="utf-8") + "next_step: flow_5\n",
            encoding="utf-8",
        )
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("unsupported field", validated.stdout)

    def test_visual_not_proven_is_valid_without_claiming_pass(self) -> None:
        project = self.make_project()
        validated = self.validate(project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertIn(
            "Visual sanity: NOT PROVEN",
            (project / "work" / "acceptance.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
