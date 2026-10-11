---
id: document.knowledge.decisions.source-code-hardening
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Decision — Source-Code Hardening and Stable Machine Identity

Date: 2026-09-07  
Status: current

## Decision

PRD-Creator 2.0 makes machine identity and validation boundaries explicit:

1. `validator/api.py` is the one complete PRD validation entrypoint; downstream handoff may not bypass content-purity/freshness checks by calling a lower-level engine directly.
2. Flow 4 acceptance binds the exact reviewed `work/render-data.json` SHA-256 in addition to semantic document version.
3. Machine-owned `*.yaml` state is parsed as YAML through one shared parser; regex/line-emulation YAML parsers are retired.
4. Production Assets/Voice placement uses stable Owner IDs derived from accepted PRD stable IDs, not display-title normalization.
5. Non-Voice Production Assets use stable globally unique `AST-...` IDs.
6. Renderer/validator engine modules use domain-specific names rather than ambiguous sibling `_engine.py` modules.
7. Voice requirements/production parsing is shared by renderer and validator.
8. Versioned delivery is staged before replacing current artifacts.

## Why

The previous implementation was behaviorally well-tested but retained script-era coupling:

- two different code paths could answer whether a PRD was valid;
- acceptance could be reused after same-version render-data changed;
- title normalization acted as machine identity for 04/Voice placement;
- multiple parsers implemented the same Voice grammar;
- YAML-looking state was interpreted by regular expressions/string splitting;
- renderer and validator both exposed a top-level `_engine` name that depended on execution/import context.

These patterns were tolerable while the repository behaved primarily as a CLI bundle. They became the primary source-code risk once the semantic/product architecture matured.

## Compatibility

This is a package-major boundary.

Existing canonical project meaning remains valid authority, but existing internal Production Asset/Voice sources must be regenerated or updated so:

```text
work/asset-requirements.md
→ each section has Owner ID
→ each non-Voice resource has ID: AST-...

work/voice-production.md
→ each gameplay section has Owner ID

work/acceptance.md
→ handoff_ready acceptance has Accepted Render Data SHA256
```

No compatibility fallback silently recreates these values from display titles. Missing identity is a validation error.

## What remains unchanged

- Golden/reference and runtime-template bytes;
- PRD semantic authority and Material Conservation;
- adaptive semantic cardinality from package 1.16;
- page family and visible component grammar;
- project-data boundary;
- Voice downstream authority;
- deterministic full-file rendering philosophy.

## Tooling boundary

PyYAML is the only new runtime dependency because YAML is an explicit persisted state format. Ruff, mypy, and coverage are verification/dev dependencies only.

This decision does not authorize a database, schema framework, plugin registry, dependency-injection system, alternate renderer family, or other generalized infrastructure.
