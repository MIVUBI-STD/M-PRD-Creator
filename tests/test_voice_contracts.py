from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prd_fixture import (
    acceptance_text,
    handoff_state_text,
    render_data,
    write_base_project,
    write_render_data,
)

ROOT = Path(__file__).resolve().parents[1]
OPERATOR = ROOT / "tools" / "prd.py"
VALIDATOR = ROOT / "kits" / "prd-creator" / "validator" / "validate_voice.py"
DELIVERY = ROOT / "kits" / "prd-creator" / "renderer" / "delivery.py"


def run_cli(*args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def requirements(extra_id: bool = False, type_override: str | None = None) -> str:
    intro_type = type_override or "Main Story"
    text = f"""# Contract Fixture Voice Requirements

Source PRD revision: 1.0.0
Voice system: Narrator and Guide direct communication.

## Intro
Owner ID: journey:journey-begins

### VO-INTRO-01 — Welcome
- Type: {intro_type}
- Function: briefing
- Necessity: required
- Speaker: Narrator
- Channel: Direct
- Trigger: Trial start before active play begins.
- Purpose: Tell the player to begin the trial.
- Moment ID: MOM-INTRO-ARRIVAL
- Moment: Introduction Arrival
- Timing Constraint: Must fit the 3-second opening slot.
- Must communicate:
  - Begin the trial.
- Must not add/repeat:
  - No additional project facts.
- Source refs:
  - REQ-001

## Ending
Owner ID: package:core

### VO-END-01 — Complete
- Type: Direct NPC Dialogue
- Function: completion
- Necessity: required
- Speaker: Guide
- Channel: Direct
- Trigger: Trial completion after the final objective resolves.
- Purpose: Acknowledge that the trial is complete.
- Moment ID: MOM-CORE-COMPLETE
- Moment: Core Trial Completion
- Must communicate:
  - The trial is complete.
- Must not add/repeat:
  - No additional reward.
- Source refs:
  - REQ-001
"""
    if extra_id:
        text += """
### VO-EXTRA-01 — Unsupported Extra
- Type: Main Story
- Function: reminder
- Necessity: supporting
- Speaker: Guide
- Channel: Direct
- Trigger: A later completion reminder would play.
- Purpose: Exercise missing-ID parity.
- Moment ID: MOM-CORE-COMPLETE
- Moment: Core Trial Completion
- Must communicate:
  - The trial remains complete.
- Must not add/repeat:
  - No new reward.
- Source refs:
  - REQ-001
"""
    return text


SCRIPT = """# Contract Fixture Voice Production
Source Voice Requirements: 1.0.0 / work/voice-requirements.md | sha256:{requirements_sha}

Voice Cast:
- Narrator: William Shanks - Rich and Deep
- Guide: Clara - Calm and Clear

## Intro
Owner ID: journey:journey-begins

### VO-INTRO-01 — Welcome
Type: Main Story
Speaker: Narrator
Estimated Duration: 2–3 seconds
```performance
[calm]
Begin the trial.
```

## Ending
Owner ID: package:core

### VO-END-01 — Complete
Type: Direct NPC Dialogue
Speaker: Guide
Estimated Duration: 2–3 seconds
```performance
[clear]
The trial is complete.
```
"""


def voice_state(project: Path, status: str = "voice_script_ready", *, include_html: bool = False) -> str:
    source_sha = hashlib.sha256((project / "work" / "render-data.json").read_bytes()).hexdigest()
    lines = [
        f"status: {status}",
        "source_handoff: state/handoff-state.yaml",
        "source_prd_revision: 1.0.0",
        f"source_prd_sha256: {source_sha}",
        "canonical_prd: work/content.md",
        "requirements: work/voice-requirements.md",
        "production: work/voice-production.md",
    ]
    if include_html:
        lines.append("project_html: output/v1.0.0/prd.html")
    return "\n".join(lines) + "\n"


def voice_acceptance(production_path: Path) -> str:
    digest = hashlib.sha256(production_path.read_bytes()).hexdigest()
    return (
        "# Voice Acceptance\n"
        "Status: voice_delivery_ready\n"
        "Mechanical: PASS\n"
        "Voice Script Readiness: PASS\n"
        "Communication Conservation: PASS\n"
        "Project HTML Visual: NOT PROVEN\n"
        "Audio Evidence: not_provided\n"
        "Critical: 0\n"
        "Major: 0\n"
        f"Accepted Voice Production SHA256: {digest}\n"
    )


class VoiceProductionContracts(unittest.TestCase):
    def refresh_prd_handoff(self, project: Path) -> None:
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        (project / "work" / "acceptance.md").write_text(
            acceptance_text(project),
            encoding="utf-8",
        )
        (project / "state" / "handoff-state.yaml").write_text(
            handoff_state_text(),
            encoding="utf-8",
        )

    def make_project(
        self,
        requirements_text: str | None = None,
        script_text: str = SCRIPT,
        *,
        status: str = "voice_script_ready",
        include_html: bool = False,
        include_acceptance: bool = False,
    ) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name)
        write_base_project(project, render_data())

        self.refresh_prd_handoff(project)

        req_text = requirements_text if requirements_text is not None else requirements()
        req_path = project / "work" / "voice-requirements.md"
        req_path.write_text(req_text, encoding="utf-8")
        bound_script = script_text.replace(
            "{requirements_sha}",
            hashlib.sha256(req_path.read_bytes()).hexdigest(),
        )
        production_path = project / "work" / "voice-production.md"
        production_path.write_text(bound_script, encoding="utf-8")
        (project / "state" / "voice-state.yaml").write_text(
            voice_state(project, status, include_html=include_html),
            encoding="utf-8",
        )

        if include_html:
            delivered = run_cli(DELIVERY, project)
            self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        if include_acceptance:
            (project / "work" / "voice-acceptance.md").write_text(
                voice_acceptance(production_path),
                encoding="utf-8",
            )
        return project

    def test_operator_status_keeps_upstream_trace_warning_with_voice_present(self) -> None:
        project = self.make_project(status="voice_script_ready")
        status = run_cli(OPERATOR, "status", project, "--json")
        self.assertEqual(status.returncode, 0, status.stderr or status.stdout)
        payload = json.loads(status.stdout)
        self.assertEqual(payload["mechanical_status"], "clear")
        self.assertEqual(payload["handoff"]["status"], "pass")
        self.assertEqual(payload["voice"]["status"], "pass")
        self.assertTrue(
            any("traceability is unreviewed" in warning for warning in payload["warnings"])
        )
        self.assertTrue(
            any("does not authenticate" in warning for warning in payload["warnings"])
        )
        self.assertFalse(payload["semantic_review_authenticated"])

    def test_operator_status_keeps_upstream_warning_before_voice_production(self) -> None:
        project = self.make_project(status="voice_requirements_ready")
        (project / "work" / "voice-production.md").unlink()
        status = run_cli(OPERATOR, "status", project, "--json")
        self.assertEqual(status.returncode, 0, status.stderr or status.stdout)
        payload = json.loads(status.stdout)
        self.assertTrue(
            any("traceability is unreviewed" in warning for warning in payload["warnings"])
        )
        self.assertEqual(payload["voice"]["status"], "pass")

    def test_validator_happy_path_needs_no_docx_export(self) -> None:
        project = self.make_project()
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertIn("VOICE VALIDATION PASS", validated.stdout)
        self.assertIn("project_html=not_provided", validated.stdout)
        self.assertNotIn("docx=", validated.stdout.casefold())

    def test_flow5_requirements_can_be_validated_before_script_readiness(self) -> None:
        project = self.make_project(status="voice_requirements_ready")
        (project / "work" / "voice-production.md").unlink()
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertIn("status=voice_requirements_ready", validated.stdout)
        self.assertIn("script_entries=0", validated.stdout)

    def test_validator_accepts_current_project_html_identity_contract(self) -> None:
        project = self.make_project(include_html=True)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertIn("project_html=passed", validated.stdout)

    def test_voice_delivery_rejects_stale_context_without_rejecting_prd_handoff(self) -> None:
        project = self.make_project(
            status="voice_delivery_ready",
            include_html=True,
            include_acceptance=True,
        )
        context = project / "output" / "v1.0.0" / "context.md"
        text = context.read_text(encoding="utf-8")
        self.assertIn("Tell the player to begin the trial.", text)
        context.write_text(
            text.replace("Tell the player to begin the trial.", "New unsourced Voice wording.", 1),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_CONTEXT_STALE", validated.stdout)
        self.assertNotIn("VOICE_UPSTREAM_HANDOFF_INVALID", validated.stdout)

    def test_voice_delivery_rejects_stale_index(self) -> None:
        project = self.make_project(
            status="voice_delivery_ready",
            include_html=True,
            include_acceptance=True,
        )
        index_file = project / "output" / "v1.0.0" / "index.json"
        index = json.loads(index_file.read_text(encoding="utf-8"))
        index["navigation"] = []
        index_file.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_INDEX_STALE", validated.stdout)

    def test_validator_rejects_missing_voice_prompt_in_project_html(self) -> None:
        project = self.make_project(include_html=True)
        html_path = project / "output" / "v1.0.0" / "prd.html"
        source = html_path.read_text(encoding="utf-8")
        source, count = re.subn(
            r'<pre class="voice-script-text" id="voice-prompt-vo-intro-01">.*?</pre>',
            "",
            source,
            count=1,
            flags=re.S,
        )
        self.assertEqual(count, 1)
        html_path.write_text(source, encoding="utf-8")
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1)
        self.assertIn("VOICE_HTML_PROMPT_COUNT_INVALID", validated.stdout)

    def test_validator_rejects_same_revision_requirement_bytes_changed_after_script_binding(self) -> None:
        project = self.make_project()
        req = project / "work" / "voice-requirements.md"
        req.write_text(
            req.read_text(encoding="utf-8").replace(
                "Tell the player to begin the trial.",
                "Tell the player to begin the trial immediately.",
                1,
            ),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_PRODUCTION_SOURCE_SHA_STALE", validated.stdout)

    def test_validator_rejects_voice_state_from_stale_prd_revision(self) -> None:
        project = self.make_project()
        state = project / "state" / "voice-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "source_prd_revision: 1.0.0",
                "source_prd_revision: 0.9.0",
            ),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_STATE_REVISION_STALE", validated.stdout)

    def test_validator_rejects_same_version_prd_bytes_changed_after_flow5_binding(self) -> None:
        project = self.make_project()
        original_state = (project / "state" / "voice-state.yaml").read_text(encoding="utf-8")
        payload = json.loads((project / "work" / "render-data.json").read_text(encoding="utf-8"))
        payload["overview"]["project_context"] = "A changed same-version accepted fixture context."
        write_render_data(project, payload)
        self.refresh_prd_handoff(project)
        (project / "state" / "voice-state.yaml").write_text(original_state, encoding="utf-8")

        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_STATE_PRD_SHA_STALE", validated.stdout)

    def test_no_voice_required_is_bound_to_exact_prd_bytes(self) -> None:
        project = self.make_project(status="no_voice_required")
        (project / "work" / "voice-production.md").unlink()
        original_state = (project / "state" / "voice-state.yaml").read_text(encoding="utf-8")
        payload = json.loads((project / "work" / "render-data.json").read_text(encoding="utf-8"))
        payload["overview"]["project_context"] = "A same-version revision that may change Voice need."
        write_render_data(project, payload)
        self.refresh_prd_handoff(project)
        (project / "state" / "voice-state.yaml").write_text(original_state, encoding="utf-8")

        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_STATE_PRD_SHA_STALE", validated.stdout)

    def test_no_voice_required_rejects_active_production_source(self) -> None:
        project = self.make_project(status="no_voice_required")
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_NO_VOICE_PRODUCTION_PRESENT", validated.stdout)

    def test_validator_rejects_unknown_voice_state_field(self) -> None:
        project = self.make_project()
        state = project / "state" / "voice-state.yaml"
        state.write_text(state.read_text(encoding="utf-8") + 'note: "voice #1"\n', encoding="utf-8")
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_STATE_INVALID", validated.stdout)

    def test_validator_rejects_unsafe_voice_state_path(self) -> None:
        project = self.make_project()
        state = project / "state" / "voice-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "requirements: work/voice-requirements.md",
                "requirements: ../outside.md",
            ),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_STATE_INVALID", validated.stdout)

    def test_validator_rejects_nonready_upstream_handoff(self) -> None:
        project = self.make_project()
        handoff = project / "state" / "handoff-state.yaml"
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace("status: handoff_ready", "status: needs_revision"),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_UPSTREAM_HANDOFF_INVALID", validated.stdout)

    def test_validator_rejects_missing_voice_id_parity(self) -> None:
        project = self.make_project(requirements(extra_id=True))
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_PRODUCTION_IDS_MISSING", validated.stdout)

    def test_validator_rejects_type_mismatch(self) -> None:
        project = self.make_project(requirements(type_override="Direct NPC Dialogue"))
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_TYPE_MISMATCH", validated.stdout)

    def test_validator_rejects_speaker_mismatch(self) -> None:
        script = SCRIPT.replace("Speaker: Narrator", "Speaker: Guide", 1)
        project = self.make_project(script_text=script)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_SPEAKER_MISMATCH", validated.stdout)

    def test_validator_rejects_owner_mismatch(self) -> None:
        script = SCRIPT.replace("Owner ID: package:core", "Owner ID: shared", 1)
        project = self.make_project(script_text=script)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_OWNER_MISMATCH", validated.stdout)

    def test_validator_rejects_duplicate_owner_id(self) -> None:
        script = SCRIPT.replace("Owner ID: package:core", "Owner ID: journey:journey-begins", 1)
        project = self.make_project(script_text=script)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1)
        self.assertIn("VOICE_OWNER_DUPLICATE", validated.stdout)

    def test_validator_accepts_natural_baseline_without_initial_performance_tag(self) -> None:
        script = SCRIPT.replace("[calm]\nBegin the trial.", "Begin the trial.", 1)
        project = self.make_project(script_text=script)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
        self.assertIn("VOICE VALIDATION PASS", validated.stdout)

    def test_voice_delivery_ready_requires_current_acceptance(self) -> None:
        project = self.make_project(
            status="voice_delivery_ready",
            include_html=True,
            include_acceptance=True,
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)

    def test_voice_delivery_ready_rejects_stale_production_acceptance(self) -> None:
        project = self.make_project(
            status="voice_delivery_ready",
            include_html=True,
            include_acceptance=True,
        )
        production = project / "work" / "voice-production.md"
        production.write_text(
            production.read_text(encoding="utf-8").replace(
                "Estimated Duration: 2–3 seconds",
                "Estimated Duration: 2–4 seconds",
                1,
            ),
            encoding="utf-8",
        )
        delivered = run_cli(DELIVERY, project)
        self.assertEqual(delivered.returncode, 0, delivered.stderr or delivered.stdout)
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_ACCEPTANCE_PRODUCTION_SHA_STALE", validated.stdout)

    def test_voice_delivery_ready_requires_cast_selection_for_every_speaker(self) -> None:
        script = SCRIPT.replace("- Guide: Clara - Calm and Clear\n", "", 1)
        project = self.make_project(
            script_text=script,
            status="voice_script_ready",
            include_html=True,
        )
        state = project / "state" / "voice-state.yaml"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "status: voice_script_ready",
                "status: voice_delivery_ready",
                1,
            ),
            encoding="utf-8",
        )
        production = project / "work" / "voice-production.md"
        (project / "work" / "voice-acceptance.md").write_text(
            voice_acceptance(production),
            encoding="utf-8",
        )
        validated = run_cli(VALIDATOR, project)
        self.assertEqual(validated.returncode, 1, validated.stderr or validated.stdout)
        self.assertIn("VOICE_CAST_SELECTION_MISSING", validated.stdout)

    def test_delivery_ready_renderer_rejects_pending_cast_selection(self) -> None:
        script = SCRIPT.replace("- Guide: Clara - Calm and Clear\n", "", 1)
        project = self.make_project(script_text=script, status="voice_script_ready")
        state = project / "state" / "voice-state.yaml"
        state.write_text(
            voice_state(project, "voice_delivery_ready", include_html=True),
            encoding="utf-8",
        )
        delivered = run_cli(DELIVERY, project)
        self.assertNotEqual(delivered.returncode, 0)
        self.assertIn("cannot render unresolved Voice Cast", delivered.stderr)

    def test_validator_has_no_docx_runtime_path(self) -> None:
        source = VALIDATOR.read_text(encoding="utf-8")
        self.assertNotIn("from docx import", source)
        self.assertNotIn("def validate_docx(", source)
        self.assertNotIn("Voice Production.docx", source)


if __name__ == "__main__":
    unittest.main()
