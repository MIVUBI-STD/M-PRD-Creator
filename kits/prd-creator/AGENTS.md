# PRD Creator Kit Agent Rules

Root `AGENTS.md` owns repository routing, authority, continuity, branch policy, canonical workflow naming, and proof boundaries. This file owns package-level file/mechanical routing and context economy.

## Open the smallest owner

| Need | Owner |
|---|---|
| Project Requirements | `intake/SOURCE-INTAKE.md` |
| PRD semantic completeness | `document/CONTENT-CONTRACT.md` |
| Complex behavior / domain-specific critique | `document/reasoning/BEHAVIOR.md` → `document/reasoning/CAPABILITIES.md` (supporting methods only) |
| Golden visual/component grammar | `document/DESIGN-CONTRACT.md` |
| PRD Handoff | `document/VALIDATION.md` |
| Production Assets meaning | `production-assets/CONTRACT.md` |
| ElevenLabs non-dialogue SFX craft/generation | `production-assets/SOUND-EFFECTS.md` |
| renderer/compositor/delivery | `renderer/CONTRACT.md` |
| Voice Requirements | `voice/EXTRACTION.md` |
| Voice Production / TTS-vs-Dialogue routing | `voice/PERFORMANCE-WRITING.md` |
| Voice Delivery | `voice/VALIDATION.md` |
| end-to-end production | `SKILL.md` |

Do not broad-read the kit. Open an adjacent owner only when an unresolved dependency can change the decision.

## Technical ownership

```text
shared/intake.py          Project Requirements machine state
shared/state.py           strict YAML loading + diagnostics
shared/paths.py           safe project-relative paths
shared/acceptance.py      exact acceptance/SHA primitives
shared/handoff.py         minimal PRD Handoff state
shared/render_schema.py   one render-data vocabulary
shared/localization.py    language/numeric invariants
shared/assets.py          Production Assets Owner/Moment/Asset grammar
shared/sfx.py             offline native SFX request + budget snapshot preflight
shared/voice.py           Voice Requirements/Production grammar
shared/lifecycle.py       Voice state vocabulary
shared/topology.py        accepted Production Assets topology
shared/issues.py          structured validation issues

renderer/core.py                     presentation primitives
renderer/pages.py                    render-data → approved page families
renderer/prd_render_engine.py        deterministic PRD composition
renderer/template_adapter.py         only Golden shell mutation owner
renderer/production_assets_compositor.py  Production Assets + Voice merge
renderer/delivery.py                 transactional versioned delivery
renderer/render.py                   thin CLI/orchestration

validator/prd_validation_engine.py   PRD validation orchestration
validator/html_contract.py           derived HTML contract
validator/api.py                     canonical PRD validation API
validator/traceability.py            REQ-to-content location + cross-role review, no semantic PASS
validator/revision.py                 read-only prior/current REQ delta + known impacted locations
validator/validate_handoff.py        PRD Handoff proof
validator/voice_validation.py        Voice Requirements→Delivery proof
validator/validate.py                thin PRD CLI
validator/validate_voice.py          thin Voice CLI
```

Do not create a second parser/schema/acceptance implementation inside renderer, validator, or helpers.

`tools/prd.py sfx-check` is a read-only adapter to `shared/sfx.py`; it validates a native provider request, not canonical project meaning or generation consent. It never invokes ElevenLabs, reserves budget, or writes project state.

## Machine invariants

### Project Requirements

```text
requirement-register bytes
→ material Proposal exists?
   yes → review/approval required
   no  → continue
→ intake-state.approved_requirement_sha256
```

### Projection

```text
approved requirement SHA
+ canonical content SHA
→ strict render schema
→ deterministic renderer
```

### Production Assets identity

```text
Owner ID → MOM-... → AST-... | VO-...
```

Display titles never join machine data.

### Acceptance and handoff

PRD Handoff binds exact current Render Data and optional Asset Requirement SHA. Voice Delivery binds exact Voice Production SHA.

```yaml
status: handoff_ready
accepted_prd_version: X.Y.Z
```

### Canonical vs derived

```text
Project Requirements state
→ work/content.md
→ work/render-data.json
→ output/v<version>/prd.html

optional work/asset-requirements.md → same Production Assets presentation
optional Voice sources             → same Production Assets presentation
```

Generated HTML/context/index are derived. Repair upstream owners and regenerate instead of hand-patching output.

## Golden boundary

Approved Golden bytes and page/component grammar remain protected. The generated document may use numeric section ordinals; those numbers are presentation order, not workflow names.

## Bounded technical change

```text
observe failure
→ first wrong owner
→ smallest complete correction
→ regenerate invalidated derived output once
→ cheapest proof that can falsify the correction
→ STOP
```

## Verification

During iteration, use targeted proof when one obvious check can settle the change; use `tools/prd.py impact` when proof domains are unclear or cross-domain. Final integration/promotion retains repository checks, full PRD + Voice regression, Ruff, type checking, coverage, and browser/audio evidence when claimed.

## Anti-overdevelopment

Do not add databases, dependency-injection frameworks, alternate PRD exports, caches, generic registries, renderer profiles, scorecards, compatibility layers, or alternate workflow naming systems without a concrete product defect.
