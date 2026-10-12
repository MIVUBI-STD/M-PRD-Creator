from __future__ import annotations

import hashlib
import html as html_lib
import re
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from renderer.pages import flow_pages, global_pages, navigation, overview, package_pages
from shared.issues import Issue

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GOLDEN_GLOBAL_PAGE_IDS = {
    "development-overview": "development-overview",
    "game-system": "shared-systems",
    "data-reset": "shared-data-reset",
    "gameplay-development": "phase-development",
}


@dataclass(frozen=True)
class HtmlCheck:
    name: str
    ok: bool
    detail: str
    issue: Issue | None = None


@dataclass(frozen=True)
class HtmlContractResult:
    checks: tuple[HtmlCheck, ...]
    expected_pages: tuple[str, ...]


class HtmlFacts(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.fragment_hrefs: list[str] = []
        self.title_parts: list[str] = []
        self.document_section_ids: list[str] = []
        self.section_classes: dict[str, set[str]] = {}
        self.render_data_sha256: list[str] = []
        self.asset_requirements_sha256: list[str] = []
        self._in_title = False
        self._in_document_main = False
        self._document_section_depth = 0
        self._current_document_section: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        classes = set(str(data.get("class") or "").split())
        tag_name = tag.lower()
        if tag_name == "main" and "document-main" in classes:
            self._in_document_main = True
        if data.get("id"):
            self.ids.append(str(data["id"]))
        if tag_name == "section" and self._in_document_main:
            self._document_section_depth += 1
            if self._document_section_depth == 1 and data.get("id"):
                section_id = str(data["id"])
                self.document_section_ids.append(section_id)
                self._current_document_section = section_id
                self.section_classes.setdefault(section_id, set()).update(classes)
            elif self._current_document_section:
                self.section_classes.setdefault(self._current_document_section, set()).update(classes)
        elif self._current_document_section:
            self.section_classes.setdefault(self._current_document_section, set()).update(classes)
        if tag_name == "meta" and str(data.get("name") or "").casefold() == "render-data-sha256":
            self.render_data_sha256.append(str(data.get("content") or ""))
        if tag_name == "meta" and str(data.get("name") or "").casefold() == "asset-requirements-sha256":
            self.asset_requirements_sha256.append(str(data.get("content") or ""))
        href = data.get("href")
        if isinstance(href, str) and href.startswith("#") and len(href) > 1:
            self.fragment_hrefs.append(href[1:])
        if tag_name == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        tag_name = tag.lower()
        if tag_name == "title":
            self._in_title = False
        if tag_name == "section" and self._in_document_main and self._document_section_depth:
            if self._document_section_depth == 1:
                self._current_document_section = None
            self._document_section_depth -= 1
        if tag_name == "main" and self._in_document_main:
            self._in_document_main = False
            self._document_section_depth = 0
            self._current_document_section = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def text_en(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("en") or value.get("id") or ""
    return str(value or "")


def _global_page_id(item: dict[str, Any]) -> str:
    item_id = str(item.get("id") or "section")
    return GOLDEN_GLOBAL_PAGE_IDS.get(item_id, f"global-{item_id}")


def expected_page_ids(data: dict[str, Any]) -> list[str]:
    ids = ["summary"]
    for index, item in enumerate(data.get("gameplay_flow", [])):
        ids.append("flow-start" if index == 0 else f"flow-{item['id']}")
    ids += [_global_page_id(item) for item in data.get("global_development", [])]
    for package in data.get("packages", []):
        package_id = package["id"]
        ids += [
            f"dev-{package_id}-requirement",
            f"dev-{package_id}-level",
            f"dev-{package_id}-developer",
        ]
    return ids


def document_composition_errors(data: dict[str, Any], facts: HtmlFacts) -> list[str]:
    failures: list[str] = []
    packages = {package["id"]: package for package in data.get("packages", [])}

    def require(section_id: str, required: set[str]) -> None:
        available = facts.section_classes.get(section_id, set())
        missing = sorted(required - available)
        if missing:
            failures.append(f"{section_id} missing {missing}")

    for index, item in enumerate(data.get("gameplay_flow", [])):
        section_id = "flow-start" if index == 0 else f"flow-{item['id']}"
        required = {"clean-visible", "story-page", "story-flow"}
        source_terms = item.get("terms", []) if index == 0 else packages.get(item["id"], {}).get("terms", [])
        if source_terms:
            required.add("quarry-definition-list")
        require(section_id, required)
    for item in data.get("global_development", []):
        require(
            _global_page_id(item),
            {
                "professional-only",
                "quarry-package-page",
                "phase-package-page",
                "global-development-page",
                "package-tabs",
                "section-context",
                "quarry-development-flow",
                "quarry-dev-table",
                "quarry-note-grid",
            },
        )
    for package in data.get("packages", []):
        package_id = package["id"]
        require(
            f"dev-{package_id}-requirement",
            {
                "professional-only",
                "quarry-package-page",
                "phase-package-page",
                "role-gameplay-overview",
                "package-tabs",
                "phase-context-grid",
                "quarry-overview-table",
                "quarry-sequence",
            },
        )
        require(
            f"dev-{package_id}-level",
            {
                "professional-only",
                "quarry-package-page",
                "phase-package-page",
                "package-tabs",
                "section-context",
                "quarry-design-flow",
                "quarry-build-table",
                "quarry-note-grid",
            },
        )
        require(
            f"dev-{package_id}-developer",
            {
                "professional-only",
                "quarry-package-page",
                "phase-package-page",
                "package-tabs",
                "section-context",
                "quarry-development-flow",
                "quarry-development-table",
                "quarry-score-summary",
                "quarry-note-grid",
            },
        )
    return failures


def _exact_projection_checks(data: dict[str, Any], html_text: str, relative_html: str) -> list[HtmlCheck]:
    """Recreate approved page/navigation HTML without accepting embedded revision metadata as proof."""

    try:
        core = "".join([overview(data), *flow_pages(data), *global_pages(data), *package_pages(data)])
        nav = navigation(data)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        detail = f"canonical HTML projection cannot be reconstructed: {exc}"
        return [
            HtmlCheck(
                "html_core_pages_match_current_projection",
                False,
                detail,
                Issue("PRD_HTML_CORE_CONTENT_DRIFT", "flow3.renderer", detail, path=relative_html),
            )
        ]

    checks: list[HtmlCheck] = []
    for marker, expected, name, code, description in (
        (
            '<main class="document-main">',
            core,
            "html_core_pages_match_current_projection",
            "PRD_HTML_CORE_CONTENT_DRIFT",
            "generated core page content/order",
        ),
        (
            '<nav class="sidebar-nav">',
            nav,
            "html_navigation_matches_current_projection",
            "PRD_HTML_NAV_CONTENT_DRIFT",
            "generated navigation content/order",
        ),
    ):
        marker_at = html_text.find(marker)
        ok = (
            bool(expected)
            and marker_at >= 0
            and html_text.count(marker) == 1
            and html_text.startswith(expected, marker_at + len(marker))
        )
        detail = (
            f"{description} matches the current canonical render projection"
            if ok
            else f"{description} differs from the current canonical render projection"
        )
        checks.append(
            HtmlCheck(
                name,
                ok,
                detail,
                None if ok else Issue(code, "flow3.renderer", detail, path=relative_html),
            )
        )
    return checks


def validate_html_contract(
    project: Path,
    data: dict[str, Any],
    data_path: Path,
    html_path: Path,
) -> HtmlContractResult:
    relative_html = html_path.relative_to(project).as_posix()
    checks: list[HtmlCheck] = []
    expected = expected_page_ids(data)
    html_text = html_path.read_text(encoding="utf-8")
    facts = HtmlFacts()
    try:
        facts.feed(html_text)
    except Exception as exc:
        checks.append(
            HtmlCheck(
                "html_parse",
                False,
                str(exc),
                Issue("PRD_HTML_PARSE_FAILED", "flow3.renderer", str(exc), path=relative_html),
            )
        )
        return HtmlContractResult(tuple(checks), tuple(expected))

    checks.extend(_exact_projection_checks(data, html_text, relative_html))

    actual_render_data_sha = hashlib.sha256(data_path.read_bytes()).hexdigest()
    bindings = facts.render_data_sha256
    binding_ok = (
        len(bindings) == 1 and SHA256_RE.fullmatch(bindings[0]) is not None and bindings[0] == actual_render_data_sha
    )
    if not bindings:
        detail = "rendered HTML is missing render-data-sha256 revision binding"
    elif len(bindings) != 1:
        detail = f"rendered HTML must contain exactly one render-data-sha256 binding; found {len(bindings)}"
    elif SHA256_RE.fullmatch(bindings[0]) is None:
        detail = "rendered HTML render-data-sha256 binding is invalid"
    elif bindings[0] != actual_render_data_sha:
        detail = "rendered HTML is stale relative to work/render-data.json"
    else:
        detail = "rendered HTML is bound to the current render-data revision"
    checks.append(
        HtmlCheck(
            "html_matches_current_render_data",
            binding_ok,
            detail,
            None if binding_ok else Issue("PRD_HTML_RENDER_SHA_STALE", "flow3.renderer", detail, path=relative_html),
        )
    )

    asset_path = project / "work" / "asset-requirements.md"
    asset_bindings = facts.asset_requirements_sha256
    if asset_path.is_file():
        actual_asset_sha = hashlib.sha256(asset_path.read_bytes()).hexdigest()
        asset_binding_ok = (
            len(asset_bindings) == 1
            and SHA256_RE.fullmatch(asset_bindings[0]) is not None
            and asset_bindings[0] == actual_asset_sha
        )
        asset_detail = (
            "rendered HTML is bound to current non-Voice Production Asset requirements"
            if asset_binding_ok
            else "rendered HTML asset-requirements binding is missing, invalid, duplicated, or stale"
        )
    else:
        asset_binding_ok = not asset_bindings
        asset_detail = (
            "no non-Voice Production Asset source or stale binding is present"
            if asset_binding_ok
            else "rendered HTML carries an asset binding but work/asset-requirements.md is absent"
        )
    checks.append(
        HtmlCheck(
            "html_matches_current_asset_requirements",
            asset_binding_ok,
            asset_detail,
            None
            if asset_binding_ok
            else Issue("PRD_HTML_ASSET_SHA_STALE", "flow3.renderer", asset_detail, path=relative_html),
        )
    )

    duplicates = sorted(key for key, count in Counter(facts.ids).items() if count > 1)
    checks.append(
        HtmlCheck(
            "html_ids_unique",
            not duplicates,
            f"duplicate ids: {duplicates}" if duplicates else "no duplicate HTML ids",
            None
            if not duplicates
            else Issue("PRD_HTML_ID_DUPLICATE", "flow3.renderer", f"duplicate ids: {duplicates}", path=relative_html),
        )
    )

    actual_pages = facts.document_section_ids
    core_pages = actual_pages[: len(expected)]
    downstream_pages = actual_pages[len(expected) :]
    invalid_downstream = [
        section_id
        for section_id in downstream_pages
        if "production-assets-page" not in facts.section_classes.get(section_id, set())
    ]
    page_set_ok = core_pages == expected and not invalid_downstream
    page_detail = (
        f"PRD core matches expected order/set: {len(expected)} pages; additive Production Assets pages: {len(downstream_pages)}"
        if page_set_ok
        else f"expected core {expected}; actual prefix {core_pages}; invalid downstream {invalid_downstream}"
    )
    checks.append(
        HtmlCheck(
            "generated_page_set_matches_current_render_data",
            page_set_ok,
            page_detail,
            None
            if page_set_ok
            else Issue("PRD_HTML_PAGE_SET_INVALID", "flow3.renderer", page_detail, path=relative_html),
        )
    )

    composition = document_composition_errors(data, facts)
    composition_ok = not composition
    composition_detail = "required Golden prototype markers are present" if composition_ok else "; ".join(composition)
    checks.append(
        HtmlCheck(
            "document_page_composition",
            composition_ok,
            composition_detail,
            None
            if composition_ok
            else Issue("PRD_HTML_COMPOSITION_INVALID", "flow3.renderer", composition_detail, path=relative_html),
        )
    )

    id_set = set(facts.ids)
    broken = sorted({target for target in facts.fragment_hrefs if target not in id_set})
    navigation_ok = not broken
    navigation_detail = f"broken targets: {broken}" if broken else "all fragment links resolve"
    checks.append(
        HtmlCheck(
            "fragment_navigation_reachable",
            navigation_ok,
            navigation_detail,
            None
            if navigation_ok
            else Issue("PRD_HTML_NAVIGATION_BROKEN", "flow3.renderer", navigation_detail, path=relative_html),
        )
    )

    document = data["document"]
    browser_title = "".join(facts.title_parts).strip()
    title = text_en(document["title"])
    title_ok = bool(title) and title.lower() in html_lib.unescape(browser_title).lower()
    title_detail = f"browser title: {browser_title!r}"
    checks.append(
        HtmlCheck(
            "browser_title_matches_project",
            title_ok,
            title_detail,
            None if title_ok else Issue("PRD_HTML_TITLE_MISMATCH", "flow3.renderer", title_detail, path=relative_html),
        )
    )
    return HtmlContractResult(tuple(checks), tuple(expected))
