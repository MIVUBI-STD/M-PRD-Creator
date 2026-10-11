from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prd_fixture import set_completion_only, write_base_project, write_render_data
from tools import prd as operator
from validator import api as prd_api
from validator.traceability import assess

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "tools" / "prd.py"
MARKED_CONTENT = (
    "# Contract Fixture\n\n"
    "<!-- PRD-TRACE: REQ-001 -->\n"
    "Preserve the approved fixture experience, including the full Core Trial journey.\n"
)


class RequirementTraceContracts(unittest.TestCase):
    def make_project(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name)
        write_base_project(project)
        return project

    def update_content(self, project: Path, content: str) -> None:
        (project / "work" / "content.md").write_text(content, encoding="utf-8")
        data = json.loads((project / "work" / "render-data.json").read_text(encoding="utf-8"))
        write_render_data(project, data)

    def test_unannotated_legacy_input_is_not_claimed_semantically_verified(self) -> None:
        project = self.make_project()
        payload = assess(project)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(payload["unmapped"], ["REQ-001"])
        self.assertFalse(payload["semantic_verified"])
        self.assertEqual(payload["review_cases"][0]["semantic_status"], "NOT_VERIFIED")
        self.assertEqual(payload["review_cases"][0]["result_mode"], "scored")

        operator.build_delivery(project)
        validated = prd_api.validate(project)
        self.assertEqual(validated["status"], "pass", validated["errors"])
        self.assertEqual(validated["traceability"]["status"], "unreviewed")
        self.assertFalse(validated["traceability"]["semantic_verified"])

    def test_bound_marker_locates_claim_but_never_claims_meaning(self) -> None:
        project = self.make_project()
        self.update_content(project, MARKED_CONTENT)
        payload = assess(project)
        self.assertEqual(payload["status"], "mapped_unverified")
        self.assertEqual(payload["mapped_count"], 1)
        self.assertEqual(payload["unmapped"], [])
        location = payload["requirements"][0]["locations"][0]
        self.assertEqual(location["heading"], "Contract Fixture")
        self.assertIn("Core Trial", location["excerpt"])

        operator.build_delivery(project)
        validated = prd_api.validate(project)
        self.assertEqual(validated["status"], "pass", validated["errors"])
        self.assertEqual(validated["traceability"]["status"], "mapped_unverified")
        self.assertFalse(validated["traceability"]["semantic_verified"])

    def test_marker_does_not_certify_unrelated_semantics(self) -> None:
        project = self.make_project()
        self.update_content(
            project,
            "# Contract Fixture\n\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "This claim describes an unrelated game with no Core Trial.\n",
        )
        payload = assess(project)
        self.assertEqual(payload["status"], "mapped_unverified")
        self.assertFalse(payload["semantic_verified"])

    def test_unknown_marker_is_rejected_even_when_render_succeeds(self) -> None:
        project = self.make_project()
        self.update_content(
            project,
            MARKED_CONTENT + "\n<!-- PRD-TRACE: REQ-999 -->\nThis claim has no matching register entry.\n",
        )
        payload = assess(project)
        self.assertEqual(payload["status"], "invalid")
        self.assertIn("PRD_TRACE_UNKNOWN_REQUIREMENT", {issue["code"] for issue in payload["issues"]})

        operator.build_delivery(project)
        validated = prd_api.validate(project)
        self.assertEqual(validated["status"], "fail")
        self.assertIn("PRD_TRACE_UNKNOWN_REQUIREMENT", {issue["code"] for issue in validated["issues"]})

    def test_incomplete_opt_in_trace_is_explicit_not_a_false_pass(self) -> None:
        project = self.make_project()
        req_path = project / "state" / "requirement-register.yaml"
        req_path.write_text(
            req_path.read_text(encoding="utf-8")
            + "  - id: REQ-002\n"
            + "    area: developer\n"
            + "    statement: Reset the session after interruption.\n"
            + "    provenance: [SRC-001]\n",
            encoding="utf-8",
        )
        self.update_content(project, MARKED_CONTENT)
        payload = assess(project)
        self.assertEqual(payload["status"], "incomplete")
        self.assertEqual(payload["unmapped"], ["REQ-002"])
        self.assertIn("PRD_TRACE_UNMAPPED", {issue["code"] for issue in payload["issues"]})

    def test_detached_and_malformed_markers_are_structural_errors(self) -> None:
        project = self.make_project()
        for sample, expected_code in (
            ("# Fixture\n<!-- PRD-TRACE: REQ-001 -->\n## Another Section\nProse\n", "PRD_TRACE_DETACHED"),
            ("# Fixture\n<!-- PRD-TRACE: REQ-1 -->\nProse\n", "PRD_TRACE_FORMAT_INVALID"),
        ):
            with self.subTest(sample=sample):
                self.update_content(project, sample)
                payload = assess(project)
                self.assertEqual(payload["status"], "invalid")
                self.assertIn(expected_code, {issue["code"] for issue in payload["issues"]})

    def test_existing_evidence_metadata_is_preserved_for_review(self) -> None:
        project = self.make_project()
        register = project / "state" / "requirement-register.yaml"
        register.write_text(
            register.read_text(encoding="utf-8")
            + "    evidence_locator: design-note.md#reconnect\n"
            + "    evidence_status: conflict\n",
            encoding="utf-8",
        )
        payload = assess(project)
        requirement = payload["requirements"][0]
        self.assertEqual(requirement["evidence_locator"], "design-note.md#reconnect")
        self.assertEqual(requirement["evidence_status"], "conflict")
        self.assertEqual(requirement["source_evidence"][0]["role"], "authoritative")

    def test_completion_only_exposes_the_correct_developer_review_surface(self) -> None:
        project = self.make_project()
        data = json.loads((project / "work/render-data.json").read_text(encoding="utf-8"))
        set_completion_only(data)
        write_render_data(project, data)
        payload = assess(project)
        case = payload["review_cases"][0]
        self.assertEqual(case["result_mode"], "completion_only")
        self.assertFalse(case["semantic_status"] == "PASS")
        self.assertFalse(case["compare"]["developer.result"]["produces_score"])
        self.assertIn("developer.reset", case["compare"])
        self.assertIn("gameplay.player_flow", case["compare"])
        self.assertIn("level_design.requirements", case["compare"])
        self.assertIn("developer.requirements", case["compare"])

    def test_operator_trace_reports_unreviewed_without_claiming_success(self) -> None:
        project = self.make_project()
        command = subprocess.run(
            [sys.executable, str(OPERATOR), "trace", str(project)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(command.returncode, 1, command.stderr)
        payload = json.loads(command.stdout)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertFalse(payload["semantic_verified"])

        self.update_content(project, MARKED_CONTENT)
        command = subprocess.run(
            [sys.executable, str(OPERATOR), "trace", str(project)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(command.returncode, 0, command.stderr)
        self.assertEqual(json.loads(command.stdout)["status"], "mapped_unverified")


if __name__ == "__main__":
    unittest.main()
