from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prd_fixture import write_base_project
from tools import prd as operator
from validator.revision import plan_revision

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
