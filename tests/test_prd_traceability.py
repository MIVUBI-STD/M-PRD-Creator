from __future__ import annotations

import hashlib
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
        self.assertTrue(any("traceability is unreviewed" in warning for warning in validated["warnings"]))

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

    def test_trace_markers_in_example_code_fences_are_ignored(self) -> None:
        project = self.make_project()
        self.update_content(
            project,
            "# Contract Fixture\n\n"
            "~~~markdown\n"
            "<!-- PRD-TRACE: REQ-999 -->\n"
            "~~~\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "The approved Core Trial remains intact.\n",
        )
        payload = assess(project)
        self.assertEqual(payload["status"], "mapped_unverified")
        self.assertEqual(payload["mapped_count"], 1)
        self.assertEqual(payload["issues"], [])

    def test_trace_markers_inside_indented_code_are_not_evidence(self) -> None:
        project = self.make_project()
        for indent in ("    ", "\t", "  \t"):
            with self.subTest(indent=repr(indent)):
                self.update_content(
                    project,
                    "# Contract Fixture\n\n"
                    + indent + "<!-- PRD-TRACE: REQ-001 -->\n"
                    + indent + "An example, not a live requirement claim.\n",
                )
                payload = assess(project)
                self.assertEqual(payload["status"], "unreviewed")
                self.assertEqual(payload["mapped_count"], 0)
                self.assertEqual(payload["issues"], [])

    def test_marker_cannot_bind_to_following_indented_code(self) -> None:
        project = self.make_project()
        self.update_content(
            project,
            "# Contract Fixture\n\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "    This is code, not a substantive Markdown paragraph.\n",
        )
        payload = assess(project)
        self.assertEqual(payload["status"], "invalid")
        self.assertIn("PRD_TRACE_DETACHED", {issue["code"] for issue in payload["issues"]})

    def test_html_code_example_does_not_count_as_requirement_evidence(self) -> None:
        project = self.make_project()
        self.update_content(
            project,
            "# Contract Fixture\n\n"
            "<pre class=\"language-markdown\">\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "An example, not a requirement.\n"
            "</pre>\n",
        )
        payload = assess(project)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(payload["mapped_count"], 0)
        self.assertEqual(payload["issues"], [])

    def test_marker_does_not_bind_to_fence_or_thematic_break(self) -> None:
        project = self.make_project()
        for non_claim in ("~~~python", "---", "<pre>"):
            with self.subTest(non_claim=non_claim):
                self.update_content(
                    project,
                    "# Contract Fixture\n\n"
                    "<!-- PRD-TRACE: REQ-001 -->\n" + non_claim + "\n",
                )
                payload = assess(project)
                self.assertEqual(payload["status"], "invalid")
                self.assertIn("PRD_TRACE_DETACHED", {item["code"] for item in payload["issues"]})

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
        self.assertEqual(
            requirement["source_evidence"][0],
            {
                "id": "SRC-001",
                "role": "authoritative",
                "status": "current",
                "inspection": "full",
                "retention": "",
                "path": "",
            },
        )
        self.assertFalse(payload["semantic_verified"])

    def test_source_review_exposes_retained_path_without_claiming_semantics(self) -> None:
        project = self.make_project()
        evidence = project / "source-note.md"
        evidence.write_text("Approved fixture source.\n", encoding="utf-8")
        inventory = project / "state/source-inventory.yaml"
        inventory.write_text(
            inventory.read_text(encoding="utf-8")
            + "    retention: repository\n"
            + "    path: source-note.md\n"
            + f"    sha256: {hashlib.sha256(evidence.read_bytes()).hexdigest()}\n",
            encoding="utf-8",
        )
        report = assess(project)
        source = report["requirements"][0]["source_evidence"][0]
        self.assertEqual(source["path"], "source-note.md")
        self.assertEqual(source["retention"], "repository")
        self.assertEqual(source["inspection"], "full")
        self.assertEqual(source["role"], "authoritative")
        self.assertEqual(report["status"], "unreviewed")
        self.assertFalse(report["semantic_verified"])

    def test_retained_line_locator_previews_exact_text_without_semantic_proof(self) -> None:
        project = self.make_project()
        source_path = project / "source-note.md"
        source_path.write_text("Session rules\nArena assignment persists\nRun progress resets\n", encoding="utf-8")
        inventory = project / "state/source-inventory.yaml"
        inventory.write_text(
            inventory.read_text(encoding="utf-8")
            + "    retention: repository\n"
            + "    path: source-note.md\n"
            + f"    sha256: {hashlib.sha256(source_path.read_bytes()).hexdigest()}\n",
            encoding="utf-8",
        )
        register = project / "state/requirement-register.yaml"
        base_register = register.read_text(encoding="utf-8")
        for locator, expected in (
            ("source-note.md#L2-L3", "Arena assignment persists\nRun progress resets"),
            ("source-note.md#L2", "Arena assignment persists"),
            ("another.md#L2", None),
            ("source-note.md#L4", None),
            ("source-note.md#L3-L2", None),
            ("source-note.md#L1-L9", None),
            ("../source-note.md#L2", None),
            ("source-note.md#reconnect", None),
        ):
            with self.subTest(locator=locator):
                register.write_text(base_register + f"    evidence_locator: {locator}\n", encoding="utf-8")
                report = assess(project)
                source = report["requirements"][0]["source_evidence"][0]
                self.assertFalse(report["semantic_verified"])
                if expected is None:
                    self.assertNotIn("source_excerpt", source)
                else:
                    self.assertEqual(source["source_excerpt"], expected)
                    self.assertEqual(source["source_excerpt_lines"], [2, 3] if "L2-L3" in locator else [2, 2])

    def test_review_cases_refuse_stale_content_projection(self) -> None:
        project = self.make_project()
        current = assess(project)
        self.assertEqual(current["review_approval_binding"], "current")
        self.assertEqual(current["review_projection_binding"], "current")
        self.assertEqual(len(current["review_cases"]), 1)

        (project / "work/content.md").write_text(
            "# Updated canonical meaning\n\nThe session has changed.\n", encoding="utf-8"
        )
        stale = assess(project)
        self.assertEqual(stale["review_approval_binding"], "current")
        self.assertEqual(stale["review_projection_binding"], "stale")
        self.assertEqual(stale["review_cases"], [])
        self.assertFalse(stale["semantic_verified"])

    def test_review_cases_refuse_stale_project_requirements(self) -> None:
        project = self.make_project()
        register = project / "state/requirement-register.yaml"
        register.write_text(register.read_text(encoding="utf-8") + "\n# Changed since approval\n", encoding="utf-8")
        stale = assess(project)
        self.assertEqual(stale["review_approval_binding"], "stale")
        self.assertEqual(stale["review_projection_binding"], "stale")
        self.assertEqual(stale["review_cases"], [])
        self.assertEqual(stale["status"], "unreviewed")

    def test_review_cases_refuse_unreadable_render_projection(self) -> None:
        project = self.make_project()
        (project / "work/render-data.json").write_text("{broken", encoding="utf-8")
        report = assess(project)
        self.assertEqual(report["review_approval_binding"], "current")
        self.assertEqual(report["review_projection_binding"], "unreadable")
        self.assertEqual(report["review_cases"], [])

    def test_review_cases_refuse_stale_intake_approval_with_current_projection(self) -> None:
        project = self.make_project()
        intake_path = project / "state/intake-state.yaml"
        current_hash = json.loads((project / "work/render-data.json").read_text(encoding="utf-8"))[
            "approved_requirement_sha256"
        ]
        intake_path.write_text(
            intake_path.read_text(encoding="utf-8").replace(current_hash, "f" * 64), encoding="utf-8"
        )
        report = assess(project)
        self.assertEqual(report["review_approval_binding"], "stale")
        self.assertEqual(report["review_projection_binding"], "current")
        self.assertEqual(report["review_cases"], [])

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
