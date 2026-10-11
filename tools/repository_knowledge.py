#!/usr/bin/env python3
"""Read-only, in-memory routing for the repository's canonical documents."""

from __future__ import annotations

import argparse
import json
import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("id", "class", "domain", "role", "authority", "lifecycle")
ROLES = {"ROUTER", "WORKFLOW", "CONTRACT", "DOMAIN", "ARCHITECTURE", "GUIDE"}
AUTHORITIES = {"CANONICAL", "REFERENCE", "HISTORICAL", "DERIVED"}
ROUTER_ID = "document.docs.router"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ID_RE = re.compile(r"^document\.[a-z0-9]+(?:[.-][a-z0-9]+)*$")
LEGACY_HISTORY = {
    "docs/knowledge/decisions/buildit-parity-reassessment.md",
    "docs/knowledge/decisions/operating-parity-gates.md",
    "docs/knowledge/reviews/astra-routing-pilot.md",
}


class KnowledgeError(ValueError):
    """Invalid repository document identity or routing contract."""


@dataclass(frozen=True)
class Document:
    id: str
    path: str
    domain: str
    role: str
    authority: str
    lifecycle: str
    body: str


def _historical(path: str) -> bool:
    return "/reviews/history/" in path or path in LEGACY_HISTORY


def _metadata(text: str, path: str) -> tuple[dict[str, str], str]:
    normalized = text.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0] != "---":
        raise KnowledgeError(f"{path}: active document missing six-field metadata")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise KnowledgeError(f"{path}: unterminated document metadata") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or ":" not in line:
            raise KnowledgeError(f"{path}: invalid document metadata line {line!r}")
        key, value = (part.strip() for part in line.split(":", 1))
        if not key or not value or key in values:
            raise KnowledgeError(f"{path}: missing/duplicate metadata field {key!r}")
        values[key] = value
    if set(values) != set(FIELDS):
        raise KnowledgeError(f"{path}: expected exactly {FIELDS}, got {sorted(values)}")
    if not ID_RE.fullmatch(values["id"]) or values["class"] != "DOCUMENT":
        raise KnowledgeError(f"{path}: invalid document class/id")
    domain = path.split("/")[1] if path != "docs/README.md" else "docs"
    if values["domain"] != domain or values["role"] not in ROLES:
        raise KnowledgeError(f"{path}: invalid document domain/role")
    if values["authority"] not in AUTHORITIES or values["lifecycle"] not in {"ACTIVE", "RETIRED"}:
        raise KnowledgeError(f"{path}: invalid document authority/lifecycle")
    return values, "\n".join(lines[end + 1 :])


def load_catalog(root: Path = ROOT, *, include_history: bool = False) -> dict[str, Document]:
    """Return one deterministic catalog derived from current document files."""
    result: dict[str, Document] = {}
    directory = root / "docs"
    if not directory.is_dir():
        raise KnowledgeError("docs/ directory missing")
    for file in sorted(directory.rglob("*.md")):
        path = file.relative_to(root).as_posix()
        if _historical(path):
            if not include_history:
                continue
            historical_id = "document.history." + re.sub(r"[^a-z0-9]+", ".", path.lower().removesuffix(".md")).strip(
                "."
            )
            doc = Document(
                historical_id,
                path,
                "history",
                "GUIDE",
                "HISTORICAL",
                "ACTIVE",
                file.read_text(encoding="utf-8"),
            )
        else:
            metadata, body = _metadata(file.read_text(encoding="utf-8"), path)
            if metadata["authority"] == "HISTORICAL" and not include_history:
                continue
            if metadata["lifecycle"] != "ACTIVE":
                continue
            doc = Document(
                metadata["id"],
                path,
                metadata["domain"],
                metadata["role"],
                metadata["authority"],
                metadata["lifecycle"],
                body,
            )
        if doc.id in result:
            raise KnowledgeError(f"duplicate document identity {doc.id}: {result[doc.id].path} and {path}")
        result[doc.id] = doc
    return result


def _targets(root: Path, doc: Document) -> list[str]:
    """Resolve explicit local Markdown links; never infer semantic graph edges."""
    targets: list[str] = []
    for found in LINK_RE.finditer(doc.body):
        raw = unquote(found.group(1).strip().strip("<>").split("#", 1)[0].split("?", 1)[0])
        if not raw or raw.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", raw, re.I):
            continue
        target = (root / raw.lstrip("/")) if raw.startswith("/") else (root / doc.path).parent / raw
        try:
            rel = target.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
        if rel.startswith("docs/") and rel.endswith(".md"):
            targets.append(rel)
    return sorted(set(targets))


def route_index(catalog: dict[str, Document], root: Path = ROOT) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Build explicit edges and shortest root-router paths; no persistent graph."""
    by_path = {doc.path: doc.id for doc in catalog.values()}
    edges = {doc.id: sorted({by_path[p] for p in _targets(root, doc) if p in by_path}) for doc in catalog.values()}
    routes: dict[str, list[str]] = {}
    if ROUTER_ID in catalog:
        routes[ROUTER_ID] = [ROUTER_ID]
        pending = deque([ROUTER_ID])
        while pending:
            current = pending.popleft()
            for nxt in edges[current]:
                if nxt not in routes:
                    routes[nxt] = [*routes[current], nxt]
                    pending.append(nxt)
    return edges, routes


def validate_repository_docs(root: Path = ROOT) -> list[str]:
    """Validate canonical document reachability and identity, not product semantics."""
    try:
        catalog = load_catalog(root)
        edges, routes = route_index(catalog, root)
    except (KnowledgeError, OSError, UnicodeError) as exc:
        return [str(exc)]
    errors: list[str] = []
    if ROUTER_ID not in catalog or catalog[ROUTER_ID].path != "docs/README.md":
        errors.append("missing canonical docs/README.md router")
    for doc in catalog.values():
        if doc.authority == "CANONICAL" and doc.id not in routes:
            errors.append(f"unreachable canonical document {doc.id}: {doc.path}")
        if doc.role == "ROUTER" and not edges[doc.id]:
            errors.append(f"document router has no current registered destinations: {doc.path}")
    return sorted(errors)


def search_documents(
    query: str,
    root: Path = ROOT,
    *,
    domain: str | None = None,
    include_history: bool = False,
) -> list[dict]:
    catalog = load_catalog(root, include_history=include_history)
    _, routes = route_index(catalog, root)
    tokens = set(re.findall(r"[a-z0-9]+", query.casefold()))
    matches: list[dict] = []
    for doc in catalog.values():
        if domain and doc.domain != domain:
            continue
        title = next((line[2:].casefold() for line in doc.body.splitlines() if line.startswith("# ")), "")
        searchable = doc.body.lower()
        score = sum(
            6 * (term in doc.id) + 3 * (term in doc.path.lower()) + 2 * (term in title) + (term in searchable)
            for term in tokens
        )
        if tokens and score > 0:
            matches.append(
                {
                    "id": doc.id,
                    "path": doc.path,
                    "domain": doc.domain,
                    "authority": doc.authority,
                    "score": score,
                    "route": routes.get(doc.id, []),
                }
            )
    return sorted(matches, key=lambda row: (-row["score"], row["id"]))[:10]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--summary", action="store_true")
    selector.add_argument("--id")
    selector.add_argument("--query")
    parser.add_argument("--domain", choices=("docs", "foundation", "knowledge", "history"))
    parser.add_argument("--include-history", action="store_true")
    args = parser.parse_args()
    try:
        catalog = load_catalog(ROOT, include_history=args.include_history)
        edges, routes = route_index(catalog)
        if args.summary:
            result = {
                "documents": len(catalog),
                "explicit_edges": sum(map(len, edges.values())),
                "reachable": len(routes),
                "by_domain": {
                    domain: sum(d.domain == domain for d in catalog.values())
                    for domain in sorted({d.domain for d in catalog.values()})
                },
                "validation": validate_repository_docs(ROOT),
            }
        elif args.id:
            if args.id not in catalog:
                parser.error("unknown document id: " + args.id)
            doc = catalog[args.id]
            result = {
                "id": doc.id,
                "path": doc.path,
                "domain": doc.domain,
                "role": doc.role,
                "authority": doc.authority,
                "routes_to": edges[doc.id],
                "route": routes.get(doc.id, []),
            }
        else:
            result = {
                "query": args.query,
                "matches": search_documents(
                    args.query,
                    ROOT,
                    domain=args.domain,
                    include_history=args.include_history,
                ),
            }
    except (KnowledgeError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
