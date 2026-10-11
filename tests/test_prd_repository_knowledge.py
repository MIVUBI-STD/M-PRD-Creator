from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.repository_knowledge import load_catalog, route_index, search_documents, validate_repository_docs


def doc(resource: str, domain: str, role: str, text: str) -> str:
    return (
        "---\n"
        f"id: {resource}\n"
        "class: DOCUMENT\n"
        f"domain: {domain}\n"
        f"role: {role}\n"
        "authority: CANONICAL\n"
        "lifecycle: ACTIVE\n"
        "---\n\n"
        + text
    )


class RepositoryKnowledgeContracts(unittest.TestCase):
    def _root(self, directory: str) -> Path:
        root = Path(directory)
        files = {
            "docs/README.md": doc(
                "document.docs.router",
                "docs",
                "ROUTER",
                "# Docs\n[Foundation](foundation/README.md)\n",
            ),
            "docs/foundation/README.md": doc(
                "document.foundation.router",
                "foundation",
                "ROUTER",
                "# Foundation\n[PRD](prd.md)\n",
            ),
            "docs/foundation/prd.md": doc(
                "document.foundation.prd",
                "foundation",
                "CONTRACT",
                "# PRD\nApproved requirements drive production.\n",
            ),
        }
        for path, content in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return root

    def test_registered_routes_are_reachable(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = self._root(folder)
            self.assertEqual(validate_repository_docs(root), [])
            catalog = load_catalog(root)
            edges, routes = route_index(catalog, root)
            self.assertEqual(len(edges), 3)
            self.assertEqual(routes["document.foundation.prd"][-1], "document.foundation.prd")
            self.assertEqual(search_documents("approved requirements", root)[0]["path"], "docs/foundation/prd.md")

    def test_duplicate_ids_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = self._root(folder)
            (root / "docs/foundation/copy.md").write_text(
                doc("document.foundation.prd", "foundation", "CONTRACT", "# Another PRD"),
                encoding="utf-8",
            )
            self.assertIn("duplicate document identity", " ".join(validate_repository_docs(root)))

    def test_unrouted_canonical_is_not_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = self._root(folder)
            (root / "docs/foundation/unused.md").write_text(
                doc("document.foundation.unused", "foundation", "CONTRACT", "# Hidden"),
                encoding="utf-8",
            )
            self.assertIn("unreachable canonical document", " ".join(validate_repository_docs(root)))

    def test_historical_documents_are_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = self._root(folder)
            old = root / "docs/knowledge/reviews/history/previous.md"
            old.parent.mkdir(parents=True, exist_ok=True)
            old.write_text("# Frozen history\n", encoding="utf-8")
            self.assertEqual(validate_repository_docs(root), [])
            self.assertEqual(len(load_catalog(root)), 3)
            history = load_catalog(root, include_history=True)
            self.assertTrue(any(d.authority == "HISTORICAL" for d in history.values()))

    def test_missing_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = self._root(folder)
            (root / "docs/foundation/prd.md").write_text("# No metadata", encoding="utf-8")
            self.assertIn("missing six-field metadata", " ".join(validate_repository_docs(root)))

    def test_current_repository_routing_contract(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_repository_docs(root), [])


if __name__ == "__main__":
    unittest.main()
