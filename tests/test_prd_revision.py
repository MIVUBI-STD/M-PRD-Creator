from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from prd_fixture import render_data, set_completion_only, write_base_project, write_render_data
from tools import prd as operator
from validator.revision import plan_revision
from validator.traceability import assess

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "tools" / "prd.py"


class TargetedRevisionContracts(unittest.TestCase):
    def make_project(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        project = Path(temporary.name)
        write_base_project(project)
        return project

    def before(self, project: Path) -> Path:
        prior = project / "previous-requirements.yaml"
        prior.write_bytes((project / "state/requirement-register.yaml").read_bytes())
        return prior

    def mark(self, project: Path, req_id: str = "REQ-001") -> None:
        (project / "work/content.md").write_text(
            "# Contract Fixture\n\n" + f"<!-- PRD-TRACE: {req_id} -->\n" + "The fixture remains valid.\n",
            encoding="utf-8",
        )

    def test_unchanged_register_has_no_claimed_revision(self) -> None:
        project = self.make_project()
        result = plan_revision(project, self.before(project))
        self.assertEqual(result["status"], "no_change")
        self.assertFalse(result["bytes_changed"])
        self.assertEqual(result["changed_requirements"], [])
        self.assertEqual(result["unchanged_requirement_ids"], ["REQ-001"])
        self.assertFalse(result["semantic_verified"])
        self.assertEqual(result["approval_binding"]["status"], "current")
        self.assertEqual(result["render_data_binding"], "current")

    def test_modified_requirement_uses_existing_marker_without_rewriting_content(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        self.mark(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(
            register.read_text(encoding="utf-8").replace(
                "Preserve the approved fixture experience.",
                "Preserve the approved fixture experience and reset after interruption.",
            ),
            encoding="utf-8",
        )
        content_before = (project / "work/content.md").read_bytes()
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "targeted_review_required")
        self.assertEqual(result["scope"], "KNOWN_LOCATIONS_ONLY")
        self.assertEqual(len(result["changed_requirements"]), 1)
        change = result["changed_requirements"][0]
        self.assertEqual(change["id"], "REQ-001")
        self.assertEqual(change["kind"], "modified")
        self.assertEqual(change["changed_fields"], ["statement"])
        self.assertEqual(change["mapping"], "LOCATED_NOT_SEMANTICALLY_VERIFIED")
        self.assertEqual(change["locations"][0]["heading"], "Contract Fixture")
        self.assertEqual(result["approval_binding"]["status"], "stale")
        self.assertEqual(result["render_data_binding"], "stale")
        self.assertEqual((project / "work/content.md").read_bytes(), content_before)

    def test_added_requirement_forces_unknown_scope_until_mapped(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        self.mark(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(
            register.read_text(encoding="utf-8")
            + "  - id: REQ-002\n"
            + "    area: developer\n"
            + "    statement: Preserve reset handling after interruption.\n"
            + "    provenance: [SRC-001]\n",
            encoding="utf-8",
        )
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "scope_unknown")
        self.assertEqual(result["unchanged_requirement_ids"], ["REQ-001"])
        self.assertEqual(result["changed_requirements"][0]["id"], "REQ-002")
        self.assertEqual(result["changed_requirements"][0]["mapping"], "LOCATION_UNKNOWN")
        self.assertFalse(result["semantic_verified"])

    def test_removed_requirement_surfaces_orphaned_marker(self) -> None:
        project = self.make_project()
        register = project / "state/requirement-register.yaml"
        extra = (
            "  - id: REQ-002\n"
            "    area: gameplay\n"
            "    statement: Present a retry cue.\n"
            "    provenance: [SRC-001]\n"
        )
        register.write_text(register.read_text(encoding="utf-8") + extra, encoding="utf-8")
        previous = self.before(project)
        register.write_text(register.read_text(encoding="utf-8").replace(extra, ""), encoding="utf-8")
        self.mark(project, "REQ-002")
        result = plan_revision(project, previous)
        self.assertEqual(result["status"], "scope_unknown")
        removed = result["changed_requirements"][0]
        self.assertEqual(removed["kind"], "removed")
        self.assertEqual(removed["id"], "REQ-002")
        self.assertEqual(removed["mapping"], "REMOVED_REVIEW_REQUIRED")
        self.assertTrue(removed["orphaned_marker_lines"])

    def test_only_textual_yaml_formatting_changed(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(register.read_text(encoding="utf-8") + "\n# formatting only\n", encoding="utf-8")
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "byte_only_change")
        self.assertTrue(result["bytes_changed"])
        self.assertEqual(result["changed_requirements"], [])
        self.assertEqual(result["approval_binding"]["status"], "stale")

    def test_evidence_only_change_does_not_assert_content_rewrite(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        self.mark(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(register.read_text(encoding="utf-8") + "    evidence_status: conflict\n", encoding="utf-8")
        result = plan_revision(project, baseline)
        change = result["changed_requirements"][0]
        self.assertEqual(change["change_scope"], "evidence_or_approval")
        self.assertEqual(change["changed_fields"], ["evidence_status"])
        self.assertFalse(result["semantic_verified"])

    def test_legacy_content_does_not_produce_invented_locations(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(register.read_text(encoding="utf-8") + "    evidence_status: reviewed\n", encoding="utf-8")
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "scope_unknown")
        self.assertEqual(result["trace_status"], "unreviewed")
        self.assertEqual(result["changed_requirements"][0]["locations"], [])

    def test_same_file_and_duplicate_snapshot_fail_closed(self) -> None:
        project = self.make_project()
        current = project / "state/requirement-register.yaml"
        with self.assertRaisesRegex(ValueError, "distinct prior snapshot"):
            plan_revision(project, current)
        baseline = self.before(project)
        baseline.write_text(
            baseline.read_text(encoding="utf-8")
            + "  - id: REQ-001\n"
            + "    area: gameplay\n"
            + "    statement: Duplicate identity.\n"
            + "    provenance: [SRC-001]\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "duplicate requirement id"):
            plan_revision(project, baseline)

    def test_content_change_does_not_falsely_claim_fresh_projection(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        (project / "work/content.md").write_text(
            "# Contract Fixture\n\nA revised implementation claim.\n", encoding="utf-8"
        )
        report = plan_revision(project, baseline)
        self.assertEqual(report["status"], "no_change")
        self.assertEqual(report["approval_binding"]["status"], "current")
        self.assertEqual(report["render_data_binding"], "stale")
        self.assertEqual(report["baseline_authority"], "NOT_VERIFIED_EXPLICIT_SNAPSHOT")
        self.assertFalse(report["semantic_verified"])

    def test_representative_scored_and_completion_packages_revise_only_known_locations(self) -> None:
        project = self.make_project()
        payload = render_data()
        capture = deepcopy(payload["packages"][0])
        capture["id"] = "capture"
        capture["title"] = "Capture Trial"
        capture["package_label"] = "Completion Trial"
        capture["terms"] = []
        set_completion_only({"packages": [capture]})
        capture["gameplay"]["result"] = "Record one capture-completion flag without awarding points."
        capture["developer"]["flow"][2]["description"] = "Record completion once, without calculating score."
        capture["acceptance"] = [
            "Capture Trial starts only for the assigned session.",
            "Capture completion records one completion-only result.",
            "Disconnect clears the capture session without a score.",
        ]
        payload["packages"].append(capture)
        flow = deepcopy(payload["gameplay_flow"][1])
        flow["id"] = "capture"
        flow["title"] = "Capture Trial"
        flow["next_destination"] = "Final exit"
        payload["gameplay_flow"].append(flow)

        register_path = project / "state/requirement-register.yaml"
        requirements = [
            ("REQ-001", "gameplay", "Core Trial awards a score only for valid completion."),
            ("REQ-002", "developer", "Core Trial reset clears session state after interruption."),
            ("REQ-003", "gameplay", "Capture Trial records completion without a score."),
            ("REQ-004", "developer", "Disconnect invalidates the active session and requires restart."),
        ]

        def register_text(items: list[tuple[str, str, str]]) -> str:
            return "requirements:\n" + "".join(
                f"  - id: {rid}\n"
                f"    area: {area}\n"
                f"    statement: {statement}\n"
                "    provenance: [SRC-001]\n"
                for rid, area, statement in items
            )

        register_path.write_text(register_text(requirements), encoding="utf-8")
        sha = hashlib.sha256(register_path.read_bytes()).hexdigest()
        (project / "state/intake-state.yaml").write_text(
            f"status: ready_for_prd\npreview_approved: true\napproved_requirement_sha256: {sha}\n",
            encoding="utf-8",
        )
        content_path = project / "work/content.md"
        content_path.write_text(
            "# Two-Package Synthetic Game\n\n"
            "## Core Trial Gameplay\n"
            "<!-- PRD-TRACE: REQ-001 -->\n"
            "Core Trial awards one valid score upon completion.\n\n"
            "## Core Trial Developer\n"
            "<!-- PRD-TRACE: REQ-002 -->\n"
            "An interrupted Core Trial must reset before session reuse.\n\n"
            "## Capture Trial Completion\n"
            "<!-- PRD-TRACE: REQ-003 -->\n"
            "Capture Trial records completion but never awards points.\n\n"
            "## Shared Session Handoff\n"
            "<!-- PRD-TRACE: REQ-004 -->\n"
            "A disconnect invalidates the current session and requires restart.\n",
            encoding="utf-8",
        )
        write_render_data(project, payload)
        trace = assess(project)
        self.assertEqual(trace["status"], "mapped_unverified")
        self.assertEqual(trace["mapped_count"], 4)
        self.assertEqual(
            [case["result_mode"] for case in trace["review_cases"]],
            ["scored", "completion_only"],
        )
        self.assertTrue(all(case["semantic_status"] == "NOT_VERIFIED" for case in trace["review_cases"]))

        baseline = self.before(project)
        (project / "state/handoff-state.yaml").write_text(
            "status: handoff_ready\naccepted_prd_version: 1.0.0\n", encoding="utf-8"
        )
        (project / "work/voice-requirements.md").write_text(
            "# Voice Requirements\n\nPending synthetic review.\n", encoding="utf-8"
        )
        revised = register_text(
            [
                requirements[0],
                ("REQ-002", "developer", "Core Trial reset clears inventory and score on interruption."),
                requirements[2],
                requirements[3],
            ]
        )
        register_path.write_text(revised, encoding="utf-8")
        untouched = content_path.read_bytes()
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "targeted_review_required")
        self.assertEqual(result["unchanged_requirement_ids"], ["REQ-001", "REQ-003", "REQ-004"])
        self.assertEqual(len(result["changed_requirements"]), 1)
        self.assertEqual(result["changed_requirements"][0]["id"], "REQ-002")
        self.assertEqual(result["changed_requirements"][0]["locations"][0]["heading"], "Core Trial Developer")
        self.assertEqual(result["approval_binding"]["status"], "stale")
        self.assertEqual(result["render_data_binding"], "stale")
        self.assertIn("semantic conservation and cross-role consistency", result["not_proven"])
        self.assertEqual(
            operator.impact_payload(["state/requirement-register.yaml"], project=project)["recommended_checks"],
            ["prd", "handoff", "voice"],
        )
        self.assertEqual(content_path.read_bytes(), untouched)

    def test_representative_removed_requirement_requires_human_scope_review(self) -> None:
        project = self.make_project()
        register_path = project / "state/requirement-register.yaml"
        prior_text = register_path.read_text(encoding="utf-8")
        removed = (
            "  - id: REQ-002\n"
            "    area: gameplay\n"
            "    statement: A second package owns a completion-only result.\n"
            "    provenance: [SRC-001]\n"
        )
        register_path.write_text(prior_text + removed, encoding="utf-8")
        baseline = self.before(project)
        register_path.write_text(prior_text, encoding="utf-8")
        self.mark(project, "REQ-002")
        before_bytes = (project / "work/content.md").read_bytes()
        result = plan_revision(project, baseline)
        self.assertEqual(result["status"], "scope_unknown")
        self.assertEqual(result["changed_requirements"][0]["mapping"], "REMOVED_REVIEW_REQUIRED")
        self.assertTrue(result["changed_requirements"][0]["orphaned_marker_lines"])
        self.assertEqual((project / "work/content.md").read_bytes(), before_bytes)

    def test_cli_report_is_read_only_and_reuses_impact_checks(self) -> None:
        project = self.make_project()
        baseline = self.before(project)
        register = project / "state/requirement-register.yaml"
        register.write_text(register.read_text(encoding="utf-8") + "    evidence_status: conflict\n", encoding="utf-8")
        previous_bytes = register.read_bytes()
        proc = subprocess.run(
            [sys.executable, str(OPERATOR), "revision", str(project), "--before", str(baseline)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "scope_unknown")
        self.assertEqual(result["recommended_checks"], ["prd"])
        self.assertEqual(register.read_bytes(), previous_bytes)


if __name__ == "__main__":
    unittest.main()
