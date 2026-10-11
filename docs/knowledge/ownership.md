---
id: document.knowledge.ownership
class: DOCUMENT
domain: knowledge
role: CONTRACT
authority: CANONICAL
lifecycle: ACTIVE
---

# Repository Ownership

Updated: 2026-09-09

Use only to answer **who owns what**. Exact field/schema/procedure contracts remain in the named owners.

## Canonical workflow names

```text
Project Setup
→ Project Requirements
→ PRD Production
   └─ Production Assets when required
→ PRD Handoff
→ Voice Requirements
→ Voice Production
→ Voice Delivery
```

Use these names in all current ownership/routing language. Numbered document/file markers are ordering only.

## Root owners

| Boundary | Owner |
|---|---|
| Project Setup / work modes / boot / authority / continuity / skill budget | `AGENTS.md` |
| GitHub mutation/history/CI/safety | `GITHUB_RULES.md` |
| Stable repository/product orientation | `CONTEXT.md` |
| Repository development intent | `planning/development.md` (topic-scoped); `planning/backlog.md` for non-active proposals |
| Documentation routing / identity | `docs/README.md` + domain routers; `tools/repository_knowledge.py` derives read-only Catalog/Graph/Context candidates |
| Repository document/reachability gate | `tools/verify_repository.py` consumes `tools/repository_knowledge.py` validation |
| Source/state precedence | `docs/knowledge/source-authority.md` |
| Durable decisions/rationale | `docs/knowledge/decisions/` |
| Dated validation evidence | `docs/knowledge/reviews/current-validation.md`; exact-head CI/source remains current authority |

## Product/package owners

| Boundary | Owner |
|---|---|
| Reusable Project Requirements / PRD Production / Production Assets / PRD Handoff semantic judgment | `.agents/skills/project-document-production/SKILL.md` |
| Reusable Voice Requirements / Voice Production / Voice Delivery semantic judgment | `.agents/skills/voice-production/SKILL.md` |
| Package file/mechanical routing | `kits/prd-creator/AGENTS.md` |
| End-to-end Production Execution | `kits/prd-creator/SKILL.md` |
| Project Requirements procedure | `kits/prd-creator/intake/SOURCE-INTAKE.md` |
| PRD semantic completeness | `kits/prd-creator/document/CONTENT-CONTRACT.md` |
| Golden page/component grammar | `kits/prd-creator/document/DESIGN-CONTRACT.md` |
| Production Assets contract | `kits/prd-creator/production-assets/CONTRACT.md` |
| PRD Handoff | `kits/prd-creator/document/VALIDATION.md` |
| Renderer/delivery contract | `kits/prd-creator/renderer/CONTRACT.md` |
| Voice Requirements | `kits/prd-creator/voice/EXTRACTION.md` |
| Voice Production | `kits/prd-creator/voice/PERFORMANCE-WRITING.md` |
| Voice Delivery | `kits/prd-creator/voice/VALIDATION.md` |

`CONTENT-CONTRACT.md` owns what meaning survives. `DESIGN-CONTRACT.md` owns how accepted meaning is represented. Machine schemas do not own product meaning.

## Machine owners

| Boundary | Owner |
|---|---|
| Project Requirements machine state | `kits/prd-creator/shared/intake.py` |
| YAML loading/diagnostics | `kits/prd-creator/shared/state.py` |
| safe persisted paths | `kits/prd-creator/shared/paths.py` |
| acceptance/SHA primitives | `kits/prd-creator/shared/acceptance.py` |
| PRD Handoff state | `kits/prd-creator/shared/handoff.py` |
| render-data vocabulary | `kits/prd-creator/shared/render_schema.py` |
| localization invariants | `kits/prd-creator/shared/localization.py` |
| Production Assets identity/parser | `kits/prd-creator/shared/assets.py` |
| Voice identity/parser | `kits/prd-creator/shared/voice.py` |
| Voice lifecycle state | `kits/prd-creator/shared/lifecycle.py` |
| Production Assets topology | `kits/prd-creator/shared/topology.py` |
| structured validation issues | `kits/prd-creator/shared/issues.py` |

## Renderer / validator owners

| Boundary | Owner |
|---|---|
| reusable HTML primitives | `kits/prd-creator/renderer/core.py` |
| render-data → page families | `kits/prd-creator/renderer/pages.py` |
| deterministic PRD composition | `kits/prd-creator/renderer/prd_render_engine.py` |
| sole Golden shell adapter | `kits/prd-creator/renderer/template_adapter.py` |
| Production Assets + Voice composition | `kits/prd-creator/renderer/production_assets_compositor.py` |
| Voice presentation formatting | `kits/prd-creator/renderer/production_assets.py` |
| transactional delivery | `kits/prd-creator/renderer/delivery.py` |
| canonical Golden source | `kits/prd-creator/template/golden-reference.html` |
| PRD validation orchestration | `kits/prd-creator/validator/prd_validation_engine.py` |
| REQ-to-content location and cross-role review surfaces (not semantic proof) | `kits/prd-creator/validator/traceability.py` |
| derived HTML contract | `kits/prd-creator/validator/html_contract.py` |
| canonical PRD validation API | `kits/prd-creator/validator/api.py` |
| PRD Handoff proof | `kits/prd-creator/validator/validate_handoff.py` |
| Voice mechanical validation | `kits/prd-creator/validator/voice_validation.py` |
| Voice validation CLI | `kits/prd-creator/validator/validate_voice.py` |

## Project-package owners

| Boundary | Owner |
|---|---|
| source identity/provenance | `state/source-inventory.yaml` |
| material requirements | `state/requirement-register.yaml` |
| Project Requirements status/revision binding | `state/intake-state.yaml` |
| canonical PRD meaning | `work/content.md` |
| strict PRD projection | `work/render-data.json` |
| canonical Production Assets | `work/asset-requirements.md` |
| PRD Handoff acceptance | `work/acceptance.md` |
| PRD Handoff state | `state/handoff-state.yaml` |
| canonical Voice Requirements | `work/voice-requirements.md` |
| canonical Voice Production | `work/voice-production.md` |
| Voice Delivery acceptance | `work/voice-acceptance.md` |
| Voice lifecycle state | `state/voice-state.yaml` |
| derived delivery | `output/README.md` + `output/v<document.version>/...` |

Derived output is never hand-patched to reconcile owners. Fix the first wrong canonical/contract owner and regenerate.