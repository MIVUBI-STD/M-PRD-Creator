from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import verify_repository


class RepositoryVerifyContracts(unittest.TestCase):
    def test_explicit_repository_path_check_rejects_missing_concrete_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            note = root / "note.md"
            note.write_text("Owner: `kits/prd-creator/template/runtime-template.html`\n", encoding="utf-8")

            errors: list[str] = []
            with (
                patch.object(verify_repository, "ROOT", root),
                patch.object(verify_repository, "CURRENT_PATH_REFERENCE_ROOTS", [note]),
            ):
                verify_repository.check_explicit_repository_paths(errors)

            self.assertEqual(
                errors,
                ["stale repository path reference in note.md: kits/prd-creator/template/runtime-template.html"],
            )

    def test_explicit_repository_path_check_accepts_existing_path_and_skips_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "kits" / "prd-creator" / "AGENTS.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("ok\n", encoding="utf-8")
            note = root / "note.md"
            note.write_text(
                "Existing: `kits/prd-creator/AGENTS.md`\nIllustrative: `tools/<name>.py`\n",
                encoding="utf-8",
            )

            errors: list[str] = []
            with (
                patch.object(verify_repository, "ROOT", root),
                patch.object(verify_repository, "CURRENT_PATH_REFERENCE_ROOTS", [note]),
            ):
                verify_repository.check_explicit_repository_paths(errors)

            self.assertEqual(errors, [])

    def test_historical_notes_are_outside_current_path_reference_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            current = root / "current.md"
            current.write_text("Current: `kits/prd-creator/AGENTS.md`\n", encoding="utf-8")
            historical = root / "reviews" / "history.md"
            historical.parent.mkdir(parents=True)
            historical.write_text("Old: `kits/retired/path.py`\n", encoding="utf-8")
            active = root / "kits" / "prd-creator" / "AGENTS.md"
            active.parent.mkdir(parents=True)
            active.write_text("ok\n", encoding="utf-8")

            errors: list[str] = []
            with (
                patch.object(verify_repository, "ROOT", root),
                patch.object(verify_repository, "CURRENT_PATH_REFERENCE_ROOTS", [current]),
            ):
                verify_repository.check_explicit_repository_paths(errors)

            self.assertEqual(errors, [])

    def test_naming_verifier_covers_active_workspace_and_detects_legacy_labels(self) -> None:
        self.assertIn(
            verify_repository.ROOT / "workspace" / "README.md",
            verify_repository.CURRENT_WORKFLOW_NAMING_ROOTS,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "workspace.md"
            source.write_text("Flow 2 should not be current operator vocabulary.\n", encoding="utf-8")
            errors: list[str] = []
            with (
                patch.object(verify_repository, "ROOT", root),
                patch.object(verify_repository, "CURRENT_WORKFLOW_NAMING_ROOTS", [source]),
            ):
                verify_repository.check_canonical_workflow_naming(errors)
            self.assertEqual(len(errors), 1)
            self.assertIn("legacy workflow name", errors[0])


if __name__ == "__main__":
    unittest.main()
